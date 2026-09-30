import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.player import Player
from app.models.team import Team
from app.models.season import Season, SeasonStatus
from app.models.stats import PlayerGameStats
from app.models.game import Game
from app.models.history import PlayerSeasonStats, TeamSeasonStats
from app.services.offseason_service import OffseasonService

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_archive_multi_position_season_stats(db_session):
    # 1. Create season and teams
    season = Season(id=1, year=2025, status=SeasonStatus.REGULAR_SEASON, is_active=True)
    team1 = Team(id=1, name="Lions", city="Detroit", abbreviation="DET", conference="NFC", division="North")
    team2 = Team(id=2, name="Packers", city="Green Bay", abbreviation="GB", conference="NFC", division="North")
    db_session.add_all([season, team1, team2])

    # 2. Create players across different positions
    qb = Player(id=1, first_name="Jared", last_name="Goff", position="QB", team_id=1, overall_rating=85)
    de = Player(id=2, first_name="Aidan", last_name="Hutchinson", position="DE", team_id=1, overall_rating=90)
    cb = Player(id=3, first_name="Brian", last_name="Branch", position="CB", team_id=1, overall_rating=86)
    k = Player(id=4, first_name="Jake", last_name="Bates", position="K", team_id=1, overall_rating=78)
    ol = Player(id=5, first_name="Penei", last_name="Sewell", position="OT", team_id=1, overall_rating=92)
    db_session.add_all([qb, de, cb, k, ol])

    # 3. Create a game and PlayerGameStats for all positions
    game = Game(id=1, season_id=1, week=1, home_team_id=1, away_team_id=2, is_played=True, home_score=24, away_score=17)
    db_session.add(game)

    pgs_qb = PlayerGameStats(player_id=1, game_id=1, team_id=1, season_id=1, pass_attempts=30, pass_completions=22, pass_yards=280, pass_tds=2)
    pgs_de = PlayerGameStats(player_id=2, game_id=1, team_id=1, season_id=1, tackles_solo=5, sacks=2.5, tackles_for_loss=3, qb_pressures=6)
    pgs_cb = PlayerGameStats(player_id=3, game_id=1, team_id=1, season_id=1, tackles_solo=4, interceptions=1, pass_deflections=2)
    pgs_k = PlayerGameStats(player_id=4, game_id=1, team_id=1, season_id=1, fg_att=2, fg_made=2)
    pgs_ol = PlayerGameStats(player_id=5, game_id=1, team_id=1, season_id=1, pancakes=4, sacks_allowed=0)
    db_session.add_all([pgs_qb, pgs_de, pgs_cb, pgs_k, pgs_ol])
    db_session.commit()

    # 4. Run OffseasonService.archive_season_stats
    service = OffseasonService(db_session)
    archived = service.archive_season_stats(1)
    assert archived == 5

    # 5. Verify PlayerSeasonStats
    qb_stats = db_session.query(PlayerSeasonStats).filter_by(player_id=1).first()
    assert qb_stats.pass_yards == 280
    assert qb_stats.pass_tds == 2
    assert qb_stats.year == 2025

    de_stats = db_session.query(PlayerSeasonStats).filter_by(player_id=2).first()
    assert de_stats.sacks == 2.5
    assert de_stats.tackles_solo == 5
    assert de_stats.tackles_for_loss == 3
    assert de_stats.qb_pressures == 6

    cb_stats = db_session.query(PlayerSeasonStats).filter_by(player_id=3).first()
    assert cb_stats.interceptions == 1
    assert cb_stats.pass_deflections == 2

    k_stats = db_session.query(PlayerSeasonStats).filter_by(player_id=4).first()
    assert k_stats.fg_made == 2

    ol_stats = db_session.query(PlayerSeasonStats).filter_by(player_id=5).first()
    assert ol_stats.pancakes == 4


def test_career_stats_accumulation_across_multiple_seasons(db_session):
    # 1. Seasons and Teams
    season1 = Season(id=1, year=2025, status=SeasonStatus.REGULAR_SEASON, is_active=False)
    season2 = Season(id=2, year=2026, status=SeasonStatus.REGULAR_SEASON, is_active=True)
    team = Team(id=1, name="Lions", city="Detroit", abbreviation="DET", conference="NFC", division="North")
    db_session.add_all([season1, season2, team])

    # 2. Multi-position Players
    qb = Player(id=1, first_name="Jared", last_name="Goff", position="QB", team_id=1, overall_rating=85)
    de = Player(id=2, first_name="Aidan", last_name="Hutchinson", position="DE", team_id=1, overall_rating=90)
    cb = Player(id=3, first_name="Brian", last_name="Branch", position="CB", team_id=1, overall_rating=86)
    k = Player(id=4, first_name="Jake", last_name="Bates", position="K", team_id=1, overall_rating=78)
    ol = Player(id=5, first_name="Penei", last_name="Sewell", position="OT", team_id=1, overall_rating=92)
    db_session.add_all([qb, de, cb, k, ol])

    # 3. Season 1 Games & Stats
    game_s1 = Game(id=1, season_id=1, week=1, home_team_id=1, away_team_id=1, is_played=True)
    db_session.add(game_s1)
    db_session.add_all([
        PlayerGameStats(player_id=1, game_id=1, team_id=1, season_id=1, pass_yards=280, pass_tds=2),
        PlayerGameStats(player_id=2, game_id=1, team_id=1, season_id=1, tackles_solo=5, sacks=2.5, tackles_for_loss=3, qb_pressures=6),
        PlayerGameStats(player_id=3, game_id=1, team_id=1, season_id=1, tackles_solo=4, interceptions=1, pass_deflections=2),
        PlayerGameStats(player_id=4, game_id=1, team_id=1, season_id=1, fg_att=2, fg_made=2),
        PlayerGameStats(player_id=5, game_id=1, team_id=1, season_id=1, pancakes=4, sacks_allowed=0),
    ])
    db_session.commit()

    service = OffseasonService(db_session)
    service.archive_season_stats(1)

    # 4. Season 2 Games & Stats
    game_s2 = Game(id=2, season_id=2, week=1, home_team_id=1, away_team_id=1, is_played=True)
    db_session.add(game_s2)
    db_session.add_all([
        PlayerGameStats(player_id=1, game_id=2, team_id=1, season_id=2, pass_yards=320, pass_tds=3),
        PlayerGameStats(player_id=2, game_id=2, team_id=1, season_id=2, tackles_solo=6, sacks=3.0, tackles_for_loss=2, qb_pressures=8),
        PlayerGameStats(player_id=3, game_id=2, team_id=1, season_id=2, tackles_solo=5, interceptions=2, pass_deflections=3),
        PlayerGameStats(player_id=4, game_id=2, team_id=1, season_id=2, fg_att=3, fg_made=3),
        PlayerGameStats(player_id=5, game_id=2, team_id=1, season_id=2, pancakes=6, sacks_allowed=0),
    ])
    db_session.commit()
    service.archive_season_stats(2)

    # 5. Verify Season-by-Season Archive (2 records per player)
    for pid in [1, 2, 3, 4, 5]:
        records = db_session.query(PlayerSeasonStats).filter_by(player_id=pid).order_by(PlayerSeasonStats.year).all()
        assert len(records) == 2
        assert records[0].year == 2025
        assert records[1].year == 2026

    # 6. Verify Career Cumulative Totals
    hutch_career = service._calculate_career_stats(2)
    assert hutch_career["games_played"] == 2
    assert hutch_career["sacks"] == 5.5
    assert hutch_career["tackles_solo"] == 11
    assert hutch_career["tackles_for_loss"] == 5
    assert hutch_career["qb_pressures"] == 14

    branch_career = service._calculate_career_stats(3)
    assert branch_career["games_played"] == 2
    assert branch_career["interceptions"] == 3
    assert branch_career["pass_deflections"] == 5
    assert branch_career["tackles_solo"] == 9

    bates_career = service._calculate_career_stats(4)
    assert bates_career["games_played"] == 2
    assert bates_career["fg_made"] == 5
    assert bates_career["fg_att"] == 5

    sewell_career = service._calculate_career_stats(5)
    assert sewell_career["games_played"] == 2
    assert sewell_career["pancakes"] == 10

    goff_career = service._calculate_career_stats(1)
    assert goff_career["games_played"] == 2
    assert goff_career["pass_yards"] == 600
    assert goff_career["pass_tds"] == 5


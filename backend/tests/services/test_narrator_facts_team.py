import pytest

from app.models.game import Game, GameType
from app.models.history import SeasonHistory, TeamSeasonStats
from app.models.season import Season, SeasonStatus
from app.models.team import Team
from app.models.weekly_recap import WeeklyRecap
from app.schemas.narrator import NarrationContextRequest
from app.services.narrator_facts_service import NarratorFactsService
from app.services.storyline_service import Storyline, StorylineType, storyline_service


def test_build_fact_packet_mid_season_played_game(db_session):
    """Test FactPacket builder with mid-season played game, season stats, recap, and storyline."""
    chiefs = Team(
        id=1,
        city="Kansas City",
        name="Chiefs",
        abbreviation="KC",
        conference="AFC",
        division="West",
        wins=4,
        losses=1,
        ties=0,
        prestige=92,
        elo_rating=1640.0,
    )
    bills = Team(
        id=2,
        city="Buffalo",
        name="Bills",
        abbreviation="BUF",
        conference="AFC",
        division="East",
        wins=3,
        losses=2,
        ties=0,
    )
    season = Season(
        id=10,
        year=2026,
        current_week=6,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
    )
    played_game = Game(
        id=100,
        season_id=10,
        season=2026,
        week=5,
        home_team_id=1,
        away_team_id=2,
        home_score=31,
        away_score=24,
        is_played=True,
        is_playoff=False,
        game_type=GameType.PRIMETIME,
    )
    unplayed_game = Game(
        id=101,
        season_id=10,
        season=2026,
        week=6,
        home_team_id=2,
        away_team_id=1,
        home_score=0,
        away_score=0,
        is_played=False,
        is_playoff=False,
        game_type=GameType.REGULAR,
    )
    team_stats = TeamSeasonStats(
        team_id=1,
        year=2026,
        wins=4,
        losses=1,
        ties=0,
        points_for=148,
        points_against=105,
        division_rank=1,
    )
    recap = WeeklyRecap(
        season_id=10,
        week=5,
        summary_text="Kansas City outlasted Buffalo 31-24 under the primetime lights.",
        surprising_result="Jets stun Ravens in overtime.",
    )
    db_session.add_all([chiefs, bills, season, played_game, unplayed_game, team_stats, recap])
    db_session.commit()

    storyline_service._active_storylines["streak_1_10"] = Storyline(
        storyline_type=StorylineType.HOT_STREAK,
        team_id=1,
        start_week=3,
    )
    try:
        service = NarratorFactsService(db_session)
        req = NarrationContextRequest(page="dashboard", team_id=1)
        packet = service.build_fact_packet(req)

        assert packet.page == "dashboard"
        assert packet.team_name == "Kansas City Chiefs"
        assert packet.team_record == "4-1"
        assert packet.season_year == 2026
        assert packet.current_week == 6

        categories = {f.category for f in packet.facts}
        assert "last_game" in categories
        assert "season" in categories
        assert "franchise" in categories
        assert "storyline" in categories

        last_game_facts = [f for f in packet.facts if f.category == "last_game"]
        assert any("31-24" in f.value and "Buffalo Bills" in f.value for f in last_game_facts)
    finally:
        storyline_service._active_storylines.pop("streak_1_10", None)


def test_build_fact_packet_championship_history(db_session):
    """Test FactPacket builder extracts franchise Super Bowl championships and runner-up finishes."""
    team = Team(
        id=1,
        city="San Francisco",
        name="49ers",
        abbreviation="SF",
        conference="NFC",
        division="West",
        wins=6,
        losses=2,
        ties=0,
        prestige=88,
        established_year=1946,
    )
    rival = Team(
        id=2,
        city="Seattle",
        name="Seahawks",
        abbreviation="SEA",
        conference="NFC",
        division="West",
        wins=4,
        losses=4,
        ties=0,
    )
    season = Season(
        id=11,
        year=2026,
        current_week=9,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
    )
    hist_2024 = SeasonHistory(year=2024, champion_team_id=1, runner_up_team_id=2)
    hist_2025 = SeasonHistory(year=2025, champion_team_id=1, runner_up_team_id=2)
    db_session.add_all([team, rival, season, hist_2024, hist_2025])
    db_session.commit()

    service = NarratorFactsService(db_session)
    req = NarrationContextRequest(page="trophy-room", team_id=1)
    packet = service.build_fact_packet(req)

    franchise_facts = [f for f in packet.facts if f.category == "franchise"]
    assert any("2" in f.value and ("2024" in f.value or "2025" in f.value) for f in franchise_facts)


def test_build_fact_packet_preseason_week1_no_games_played(db_session):
    """Test FactPacket builder handles Week 1 / Preseason when zero games have been played."""
    team = Team(
        id=1,
        city="Detroit",
        name="Lions",
        abbreviation="DET",
        conference="NFC",
        division="North",
        wins=0,
        losses=0,
        ties=0,
        prestige=82,
    )
    season = Season(
        id=12,
        year=2026,
        current_week=1,
        is_active=True,
        status=SeasonStatus.PRE_SEASON,
    )
    db_session.add_all([team, season])
    db_session.commit()

    service = NarratorFactsService(db_session)
    req = NarrationContextRequest(page="season", team_id=1)
    packet = service.build_fact_packet(req)

    assert packet.team_name == "Detroit Lions"
    assert packet.team_record == "0-0"
    assert packet.season_year == 2026
    assert packet.current_week == 1
    assert len(packet.facts) >= 2
    assert any(f.category == "last_game" and "0" in f.value for f in packet.facts)

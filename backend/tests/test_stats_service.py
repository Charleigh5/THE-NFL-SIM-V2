import pytest
from app.services.stats_service import StatsService
from app.models.season import Season
from app.models.team import Team
from app.models.player import Player, Position
from app.models.game import Game
from app.models.stats import PlayerGameStats


def test_get_league_leaders_passing(db_session):
    """Test getting passing yards leaders."""
    # Setup
    service = StatsService(db_session)
    
    # Create Season
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    # Create Teams
    team1 = Team(name="Team1", city="City1", abbreviation="T1", conference="AFC", division="North", prestige=80)
    team2 = Team(name="Team2", city="City2", abbreviation="T2", conference="NFC", division="South", prestige=80)
    db_session.add_all([team1, team2])
    db_session.commit()
    
    # Create Players
    qb1 = Player(first_name="QB", last_name="One", position=Position.QB, team_id=team1.id, overall_rating=90)
    qb2 = Player(first_name="QB", last_name="Two", position=Position.QB, team_id=team2.id, overall_rating=85)
    db_session.add_all([qb1, qb2])
    db_session.commit()
    
    # Create Games
    game1 = Game(season_id=season.id, home_team_id=team1.id, away_team_id=team2.id, week=1, is_played=True, home_score=28, away_score=21)
    game2 = Game(season_id=season.id, home_team_id=team1.id, away_team_id=team2.id, week=2, is_played=True, home_score=31, away_score=24)
    db_session.add_all([game1, game2])
    db_session.commit()
    
    # Create Stats
    # QB1: 300 + 250 = 550 yards
    stats1 = PlayerGameStats(player_id=qb1.id, game_id=game1.id, team_id=team1.id, pass_yards=300, pass_tds=2)
    stats2 = PlayerGameStats(player_id=qb1.id, game_id=game2.id, team_id=team1.id, pass_yards=250, pass_tds=1)
    
    # QB2: 400 + 0 = 400 yards
    stats3 = PlayerGameStats(player_id=qb2.id, game_id=game1.id, team_id=team2.id, pass_yards=400, pass_tds=3)
    
    db_session.add_all([stats1, stats2, stats3])
    db_session.commit()
    
    # Test Passing Yards
    leaders = service.get_league_leaders(season.id, "passing_yards", limit=5)
    
    assert len(leaders) == 2
    assert leaders[0].player_id == qb1.id
    assert leaders[0].value == 550
    assert leaders[0].stat_type == "passing_yards"
    assert leaders[0].team == "City1 Team1"
    
    assert leaders[1].player_id == qb2.id
    assert leaders[1].value == 400


def test_get_league_leaders_passing_tds(db_session):
    """Test getting passing TD leaders."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="AFC", division="North", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    qb = Player(first_name="QB", last_name="One", position=Position.QB, team_id=team.id, overall_rating=90)
    db_session.add(qb)
    db_session.commit()
    
    game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add(game)
    db_session.commit()
    
    stats = PlayerGameStats(player_id=qb.id, game_id=game.id, team_id=team.id, pass_yards=300, pass_tds=4)
    db_session.add(stats)
    db_session.commit()
    
    leaders = service.get_league_leaders(season.id, "passing_tds", limit=5)
    assert len(leaders) == 1
    assert leaders[0].value == 4
    assert leaders[0].stat_type == "passing_tds"


def test_get_league_leaders_rushing(db_session):
    """Test getting rushing yards leaders."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="NFC", division="South", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    rb1 = Player(first_name="RB", last_name="One", position=Position.RB, team_id=team.id, overall_rating=88)
    rb2 = Player(first_name="RB", last_name="Two", position=Position.RB, team_id=team.id, overall_rating=82)
    db_session.add_all([rb1, rb2])
    db_session.commit()
    
    game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add(game)
    db_session.commit()
    
    stats1 = PlayerGameStats(player_id=rb1.id, game_id=game.id, team_id=team.id, rush_yards=150, rush_tds=2)
    stats2 = PlayerGameStats(player_id=rb2.id, game_id=game.id, team_id=team.id, rush_yards=80, rush_tds=1)
    db_session.add_all([stats1, stats2])
    db_session.commit()
    
    leaders = service.get_league_leaders(season.id, "rushing_yards", limit=5)
    assert len(leaders) == 2
    assert leaders[0].value == 150
    assert leaders[1].value == 80
    assert leaders[0].stat_type == "rushing_yards"


def test_get_league_leaders_receiving(db_session):
    """Test getting receiving yards leaders."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="AFC", division="East", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    wr = Player(first_name="WR", last_name="One", position=Position.WR, team_id=team.id, overall_rating=91)
    db_session.add(wr)
    db_session.commit()
    
    game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add(game)
    db_session.commit()
    
    stats = PlayerGameStats(player_id=wr.id, game_id=game.id, team_id=team.id, rec_yards=120, rec_tds=2)
    db_session.add(stats)
    db_session.commit()
    
    leaders = service.get_league_leaders(season.id, "receiving_yards", limit=5)
    assert len(leaders) == 1
    assert leaders[0].value == 120
    assert leaders[0].stat_type == "receiving_yards"


def test_get_league_leaders_limit(db_session):
    """Test that limit parameter works correctly."""
    service = StatsService(db_session)
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="T", city="C", abbreviation="T", conference="C", division="D", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add(game)
    db_session.commit()
    
    # Create 3 players
    players = []
    for i in range(3):
        p = Player(first_name=f"P{i}", last_name="L", position=Position.RB, team_id=team.id, overall_rating=80)
        db_session.add(p)
        players.append(p)
    db_session.commit()
    
    # Add stats (descending order: 30, 20, 10)
    for i, p in enumerate(players):
        s = PlayerGameStats(player_id=p.id, game_id=game.id, team_id=team.id, rush_yards=(3-i)*10)
        db_session.add(s)
    db_session.commit()
    
    # Limit 2
    leaders = service.get_league_leaders(season.id, "rushing_yards", limit=2)
    assert len(leaders) == 2
    assert leaders[0].value == 30  # P0 (first player) has 30
    assert leaders[1].value == 20  # P1 has 20


def test_get_league_leaders_empty_results(db_session):
    """Test behavior when no stats exist for the season."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    # No games or stats created
    leaders = service.get_league_leaders(season.id, "passing_yards", limit=5)
    assert len(leaders) == 0


def test_get_league_leaders_multiple_games(db_session):
    """Test that stats are properly aggregated across multiple games."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="AFC", division="North", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    qb = Player(first_name="Aaron", last_name="Rodgers", position=Position.QB, team_id=team.id, overall_rating=92)
    db_session.add(qb)
    db_session.commit()
    
    # Create 3 games
    games = []
    for i in range(3):
        game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=i+1, is_played=True)
        db_session.add(game)
        games.append(game)
    db_session.commit()
    
    # Add stats for each game (100, 200, 150 yards)
    yards = [100, 200, 150]
    for game, yard_total in zip(games, yards):
        stats = PlayerGameStats(player_id=qb.id, game_id=game.id, team_id=team.id, pass_yards=yard_total, pass_tds=2)
        db_session.add(stats)
    db_session.commit()
    
    leaders = service.get_league_leaders(season.id, "passing_yards", limit=5)
    assert len(leaders) == 1
    assert leaders[0].value == 450  # 100 + 200 + 150


def test_get_league_leaders_different_seasons(db_session):
    """Test that stats are correctly filtered by season."""
    service = StatsService(db_session)
    
    # Create two seasons
    season1 = Season(year=2023)
    season2 = Season(year=2024)
    db_session.add_all([season1, season2])
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="AFC", division="North", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    qb = Player(first_name="QB", last_name="One", position=Position.QB, team_id=team.id, overall_rating=90)
    db_session.add(qb)
    db_session.commit()
    
    # Create game in season 1
    game1 = Game(season_id=season1.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    # Create game in season 2
    game2 = Game(season_id=season2.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add_all([game1, game2])
    db_session.commit()
    
    # Stats for season 1 (300 yards)
    stats1 = PlayerGameStats(player_id=qb.id, game_id=game1.id, team_id=team.id, pass_yards=300)
    # Stats for season 2 (500 yards)
    stats2 = PlayerGameStats(player_id=qb.id, game_id=game2.id, team_id=team.id, pass_yards=500)
    db_session.add_all([stats1, stats2])
    db_session.commit()
    
    # Query season 2 only
    leaders = service.get_league_leaders(season2.id, "passing_yards", limit=5)
    assert len(leaders) == 1
    assert leaders[0].value == 500  # Only season 2 stats


def test_invalid_stat_type(db_session):
    """Test that invalid stat type raises ValueError."""
    service = StatsService(db_session)
    with pytest.raises(ValueError):
        service.get_league_leaders(1, "invalid_stat")


def test_get_league_leaders_all_stat_types(db_session):
    """Test all six stat types are supported."""
    service = StatsService(db_session)
    
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()
    
    team = Team(name="Team", city="City", abbreviation="T", conference="AFC", division="North", prestige=80)
    db_session.add(team)
    db_session.commit()
    
    qb = Player(first_name="QB", last_name="One", position=Position.QB, team_id=team.id, overall_rating=90)
    rb = Player(first_name="RB", last_name="One", position=Position.RB, team_id=team.id, overall_rating=85)
    wr = Player(first_name="WR", last_name="One", position=Position.WR, team_id=team.id, overall_rating=88)
    db_session.add_all([qb, rb, wr])
    db_session.commit()
    
    game = Game(season_id=season.id, home_team_id=team.id, away_team_id=team.id, week=1, is_played=True)
    db_session.add(game)
    db_session.commit()
    
    qb_stats = PlayerGameStats(player_id=qb.id, game_id=game.id, team_id=team.id, pass_yards=300, pass_tds=3)
    rb_stats = PlayerGameStats(player_id=rb.id, game_id=game.id, team_id=team.id, rush_yards=120, rush_tds=2)
    wr_stats = PlayerGameStats(player_id=wr.id, game_id=game.id, team_id=team.id, rec_yards=100, rec_tds=1)
    db_session.add_all([qb_stats, rb_stats, wr_stats])
    db_session.commit()
    
    # Test all stat types
    stat_types = ["passing_yards", "passing_tds", "rushing_yards", "rushing_tds", "receiving_yards", "receiving_tds"]
    for stat_type in stat_types:
        leaders = service.get_league_leaders(season.id, stat_type, limit=5)
        assert isinstance(leaders, list)
        assert all(leader.stat_type == stat_type for leader in leaders)


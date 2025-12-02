import pytest
from app.models.team import Team
from app.models.player import Player, Position
from app.models.season import Season
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.services.stats_service import StatsService

def test_get_league_leaders(db_session):
    # Setup
    season = Season(year=2024)
    db_session.add(season)
    db_session.commit()

    team = Team(name="Test Team", city="City", abbreviation="TST", conference="AFC", division="North")
    db_session.add(team)
    db_session.commit()

    p1 = Player(first_name="QB", last_name="One", position=Position.QB, team_id=team.id)
    p2 = Player(first_name="QB", last_name="Two", position=Position.QB, team_id=team.id)
    db_session.add_all([p1, p2])
    db_session.commit()

    game = Game(season_id=season.id, season=2024, week=1, home_team_id=team.id, away_team_id=team.id)
    db_session.add(game)
    db_session.commit()

    # Add stats
    # P1: 300 yards
    stats1 = PlayerGameStats(
        player_id=p1.id,
        game_id=game.id,
        team_id=team.id,
        season_id=season.id,
        pass_yards=300,
        pass_tds=3
    )
    # P2: 200 yards
    stats2 = PlayerGameStats(
        player_id=p2.id,
        game_id=game.id,
        team_id=team.id,
        season_id=season.id,
        pass_yards=200,
        pass_tds=1
    )
    db_session.add_all([stats1, stats2])
    db_session.commit()

    # Test
    service = StatsService(db_session)
    leaders = service.get_league_leaders(season.id, "passing_yards", limit=5)

    assert len(leaders) == 2
    assert leaders[0].player_id == p1.id
    assert leaders[0].value == 300
    assert leaders[1].player_id == p2.id
    assert leaders[1].value == 200

    # Test limit
    leaders_limit = service.get_league_leaders(season.id, "passing_yards", limit=1)
    assert len(leaders_limit) == 1
    assert leaders_limit[0].player_id == p1.id

    # Test other stat
    leaders_td = service.get_league_leaders(season.id, "passing_tds", limit=5)
    assert leaders_td[0].value == 3
    assert leaders_td[1].value == 1

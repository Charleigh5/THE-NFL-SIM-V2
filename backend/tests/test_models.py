import pytest
from app.models.team import Team
from app.models.player import Player, Position
from app.models.season import Season, SeasonStatus
from app.models.game import Game

def test_create_team(db_session):
    team = Team(
        name="Test Team",
        city="Test City",
        abbreviation="TST",
        conference="AFC",
        division="North"
    )
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)

    assert team.id is not None
    assert team.name == "Test Team"
    assert team.city == "Test City"
    assert team.abbreviation == "TST"
    assert team.wins == 0  # Default value

def test_create_player(db_session):
    team = Team(
        name="Player Team",
        city="Player City",
        abbreviation="PLT",
        conference="NFC",
        division="South"
    )
    db_session.add(team)
    db_session.commit()

    player = Player(
        first_name="John",
        last_name="Doe",
        position=Position.QB,
        team_id=team.id,
        overall_rating=85
    )
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)

    assert player.id is not None
    assert player.first_name == "John"
    assert player.position == "QB"
    assert player.team_id == team.id
    assert player.team.name == "Player Team"
    assert player.overall_rating == 85
    assert player.morale == 50 # Default

def test_create_season(db_session):
    season = Season(
        year=2025,
        status=SeasonStatus.REGULAR_SEASON
    )
    db_session.add(season)
    db_session.commit()
    db_session.refresh(season)

    assert season.id is not None
    assert season.year == 2025
    assert season.current_week == 1
    assert season.status == SeasonStatus.REGULAR_SEASON

def test_create_game(db_session):
    season = Season(year=2026)
    home_team = Team(name="Home", city="City", abbreviation="HOM", conference="AFC", division="East")
    away_team = Team(name="Away", city="City", abbreviation="AWY", conference="AFC", division="East")

    db_session.add(season)
    db_session.add(home_team)
    db_session.add(away_team)
    db_session.commit()

    game = Game(
        season_id=season.id,
        season=2026,
        week=1,
        home_team_id=home_team.id,
        away_team_id=away_team.id
    )
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)

    assert game.id is not None
    assert game.season_id == season.id
    assert game.home_team_id == home_team.id
    assert game.away_team_id == away_team.id
    assert game.is_played is False

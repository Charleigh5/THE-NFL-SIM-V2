import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
import app.models  # Ensure all models are registered
from app.models.team import Team
from app.models.season import Season, SeasonStatus
from app.services.schedule_generator import ScheduleGenerator
from app.services.nflverse_service import map_team_abbr, NflverseService
from app.core.seed import seed_teams


@pytest.fixture
def test_db():
    """Create a completely isolated in-memory SQLite database for test execution."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine)
    db = TestingSession()
    seed_teams(db)
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_team_abbr_mapping():
    """Verify team abbreviation mapping between nflverse and our DB."""
    assert map_team_abbr("LA") == "LAR"
    assert map_team_abbr("WSH") == "WAS"
    assert map_team_abbr("JAX") == "JAX"
    assert map_team_abbr("LV") == "LV"
    assert map_team_abbr("KC") == "KC"
    assert map_team_abbr("SF") == "SF"


def test_load_real_schedule_2026(test_db):
    """Verify loading authentic 2026 NFL schedule produces 272 regular season games."""
    generator = ScheduleGenerator(test_db)
    games = generator.load_real_schedule(season_id=2, year=2026)

    # Must contain 272 games (17 games * 32 teams / 2)
    assert len(games) == 272

    weeks = {g.week for g in games}
    assert weeks == set(range(1, 19))

    # All games must start unplayed
    assert all(not g.is_played for g in games)
    assert all(not g.is_preseason for g in games)
    assert all(not g.is_playoff for g in games)
    assert all(g.season == 2026 for g in games)
    assert all(g.home_team_id is not None and g.away_team_id is not None for g in games)


def test_generate_schedule_prefers_real_for_2026(test_db):
    """Verify generate_schedule utilizes authentic real schedule for 2026."""
    teams = test_db.query(Team).all()
    generator = ScheduleGenerator(test_db)
    games = generator.generate_schedule(season_id=2, teams=teams, year=2026, prefer_real=True)

    assert len(games) == 272


def test_nflverse_service_default_2026():
    """Verify NflverseService defaults to 2026 season."""
    service = NflverseService()
    assert service.season == 2026

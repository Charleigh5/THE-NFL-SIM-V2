import asyncio
import os
import sys

# Ensure the repo root is on sys.path so imports like `backend.*` resolve when running tests
# from the `backend/` directory (pytest rootdir).
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    # Keep CWD (`backend/`) as the first entry so `import app.*` resolves to `backend/app/*`.
    sys.path.insert(1, _PROJECT_ROOT)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_async_db, get_db
from app.main import app
from app.models.base import Base

# Use a file-based SQLite database for testing to allow sharing between sync and async
TEST_DB_FILE = "test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
TEST_ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

import logging

from sqlalchemy import event

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_player(
    id: int = 1,
    first_name: str = "Test",
    last_name: str = "Player",
    position: str = "QB",
    overall_rating: int = 75,
    height: int = 74,  # 6'2" default
    weight: int = 215,
    age: int = 27,  # Default age
    team_id: int = 1,
    **kwargs
):
    """
    Factory function for creating Player instances with all required NOT NULL fields.
    Best practice: Use this instead of direct Player() to ensure consistency.
    """
    from app.models.player import Player
    return Player(
        id=id,
        first_name=first_name,
        last_name=last_name,
        position=position,
        overall_rating=overall_rating,
        height=height,
        weight=weight,
        age=age,
        team_id=team_id,
        **kwargs
    )


@pytest.fixture(scope="session", autouse=True)
def _debug_import_paths():
    """Temporary diagnostics: show how `app` resolves + the leading sys.path entries."""
    logger.info("PYTEST DEBUG: sys.executable=%s", sys.executable)
    logger.info("PYTEST DEBUG: cwd=%s", os.getcwd())
    logger.info("PYTEST DEBUG: sys.path[:8]=%s", sys.path[:8])
    try:
        import app as app_pkg  # noqa: F401

        logger.info("PYTEST DEBUG: app.__file__=%s", getattr(app_pkg, "__file__", None))
        logger.info("PYTEST DEBUG: app.__package__=%s", getattr(app_pkg, "__package__", None))
    except Exception:
        logger.exception("PYTEST DEBUG: failed to import `app` during conftest diagnostics")
    yield

# Create engines
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
async_engine = create_async_engine(
    TEST_ASYNC_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Enable WAL mode for concurrency
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

@event.listens_for(async_engine.sync_engine, "connect")
def set_sqlite_pragma_async(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncTestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine,
    expire_on_commit=False  # Prevent MissingGreenlet on relationship access after commit
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Remove existing test db if any
    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except OSError:
            pass

    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables and remove file
    Base.metadata.drop_all(bind=engine)

    # Dispose engines to release file locks
    engine.dispose()
    asyncio.run(async_engine.dispose())

    if os.path.exists(TEST_DB_FILE):
        try:
            os.remove(TEST_DB_FILE)
        except OSError:
            pass
    if os.path.exists(f"{TEST_DB_FILE}-wal"):
        try:
            os.remove(f"{TEST_DB_FILE}-wal")
        except OSError:
            pass
    if os.path.exists(f"{TEST_DB_FILE}-shm"):
        try:
            os.remove(f"{TEST_DB_FILE}-shm")
        except OSError:
            pass

@pytest.fixture(scope="function")
def db_session():
    # Establish a connection and begin a transaction for each test function
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
async def async_db_session():
    """Function-scoped async session with proper isolation."""
    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()  # Ensure clean state after each test

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture for FastAPI TestClient that overrides the get_db and get_async_db dependencies.
    """
    def override_get_db():
        yield db_session

    async def override_get_async_db():
        # We need a new async session for the request, but it should see the data committed by db_session
        # Since we are using a file DB, data committed by db_session is visible to new connections.
        # However, db_session in the fixture has an open transaction.
        # If we want the async session to see uncommitted data from db_session, that's hard with SQLite.
        # So tests should commit data they want the API to see.
        async with AsyncTestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_async_db] = override_get_async_db

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def async_client(async_db_session):
    """
    Fixture for httpx AsyncClient.
    """
    from httpx import ASGITransport, AsyncClient

    async def override_get_async_db():
        yield async_db_session

    app.dependency_overrides[get_async_db] = override_get_async_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture(scope="function", autouse=True)
async def clear_tables(async_db_session):
    """Clear all tables before each test."""
    from sqlalchemy import text
    # Disable foreign key checks to allow deleting in any order
    await async_db_session.execute(text("PRAGMA foreign_keys=OFF"))

    for table in reversed(Base.metadata.sorted_tables):
        await async_db_session.execute(table.delete())

    await async_db_session.execute(text("PRAGMA foreign_keys=ON"))
    await async_db_session.commit()

@pytest.fixture(scope="function")
async def sample_teams(async_db_session):
    """Create sample teams for testing."""
    from app.models.team import Team

    teams = [
        Team(
            id=1,
            name="Chiefs",
            city="Kansas City",
            abbreviation="KC",
            conference="AFC",
            division="West",
            salary_cap_space=55000000.0,
        ),
        Team(
            id=2,
            name="Bills",
            city="Buffalo",
            abbreviation="BUF",
            conference="AFC",
            division="East",
            salary_cap_space=65000000.0,
        )
    ]
    async_db_session.add_all(teams)
    await async_db_session.commit()
    return teams

@pytest.fixture(scope="function")
async def sample_players(async_db_session, sample_teams):
    """Create sample players for testing."""
    from app.models.player import Player

    players = [
        Player(
            id=1,
            team_id=1,
            first_name="Patrick",
            last_name="Mahomes",
            position="QB",
            age=28,
            height=75,  # 6'3"
            weight=225,
            overall_rating=99,
            contract_salary=50000000,
            contract_years=5,
            injury_status="ACTIVE"
        ),
        Player(
            id=2,
            team_id=1,
            first_name="Travis",
            last_name="Kelce",
            position="TE",
            age=34,
            height=77,  # 6'5"
            weight=250,
            overall_rating=92,
            contract_salary=15000000,
            contract_years=2,
            injury_status="ACTIVE"
        ),
        Player(
            id=3,
            team_id=2,
            first_name="Josh",
            last_name="Allen",
            position="QB",
            age=27,
            height=77,  # 6'5"
            weight=237,
            overall_rating=98,
            contract_salary=45000000,
            contract_years=4,
            injury_status="ACTIVE"
        )
    ]
    async_db_session.add_all(players)
    await async_db_session.commit()
    return players

@pytest.fixture(autouse=True)
def override_session_local(monkeypatch):
    """Override SessionLocal to use test database globally."""
    # Patch the SessionLocal in the database module which is imported by others
    monkeypatch.setattr("app.core.database.SessionLocal", TestingSessionLocal)

    # Also patch where it might have been imported directly (if needed)
    monkeypatch.setattr("app.api.endpoints.trades.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.api.endpoints.season.SessionLocal", TestingSessionLocal)


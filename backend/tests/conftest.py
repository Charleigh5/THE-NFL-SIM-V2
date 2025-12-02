import pytest
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.models.base import Base
from app.main import app
from app.core.database import get_db, get_async_db

# Use a file-based SQLite database for testing to allow sharing between sync and async
TEST_DB_FILE = "test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"
TEST_ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_FILE}"

from sqlalchemy import event
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    class_=AsyncSession, autocommit=False, autoflush=False, bind=async_engine
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
    async with AsyncTestingSessionLocal() as session:
        yield session

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
    from httpx import AsyncClient, ASGITransport

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

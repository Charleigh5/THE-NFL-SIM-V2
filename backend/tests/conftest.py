import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Import Base from your application's database module
# You might need to adjust this import based on your actual project structure
from app.models.base import Base

# Import your FastAPI application instance
# You might need to adjust this import based on your actual project structure
from app.main import app

# Use an in-memory SQLite database for testing for speed and isolation
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    # Create tables for all models defined in Base
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop all tables after the session is over
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    # Establish a connection and begin a transaction for each test function
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Rollback the transaction and close the connection after each test
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture for FastAPI TestClient that overrides the get_db dependency
    to use the test database session.
    """
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear() # Clear overrides after the test

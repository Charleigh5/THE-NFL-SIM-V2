
import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.core.database import get_db
from app.models.base import Base
from app.models.season import Season, SeasonStatus
from app.models.team import Team

# Setup in-memory DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_module(module):
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create dummy team
    team = Team(
        id=1,
        name="Test Team",
        city="Test City",
        abbreviation="TST",
        conference="AFC",
        division="North"
    )
    db.add(team)
    
    # Create dummy season
    season = Season(
        id=1,
        year=2024,
        current_week=18,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON
    )
    db.add(season)
    db.commit()
    db.close()

def test_generate_playoffs_invalid_season():
    # Test with non-existent season
    response = client.post("/api/season/999/playoffs/generate")
    # Expect 400 because Service raises ValueError("Season not found") which decorator maps to 400
    assert response.status_code == 400
    assert "Season not found" in response.json()["detail"]["message"]

def test_start_offseason_invalid_season():
    # Test with non-existent season
    response = client.post("/api/season/999/offseason/start")
    # Expect 400 because Service raises ValueError("Season not found") which decorator maps to 400
    assert response.status_code == 400
    assert "Season not found" in response.json()["detail"]["message"]

def test_get_team_salary_cap_invalid_team():
    # Test with non-existent team
    response = client.get("/api/season/team/999/salary-cap")
    # Expect 400 because Service raises ValueError("Team 999 not found") which decorator maps to 400
    assert response.status_code == 400
    assert "Team 999 not found" in response.json()["detail"]["message"]

if __name__ == "__main__":
    # Manually run tests if executed as script
    setup_module(None)
    try:
        test_generate_playoffs_invalid_season()
        print("test_generate_playoffs_invalid_season PASSED")
        test_start_offseason_invalid_season()
        print("test_start_offseason_invalid_season PASSED")
        test_get_team_salary_cap_invalid_team()
        print("test_get_team_salary_cap_invalid_team PASSED")
    except AssertionError as e:
        print(f"FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

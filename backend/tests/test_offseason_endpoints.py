
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db

# Override dependency
def override_get_db():
    try:
        db = MagicMock()
        yield db
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@patch("app.services.salary_cap_service.SalaryCapService.get_team_cap_breakdown")
def test_get_team_salary_cap_endpoint(mock_get_breakdown):
    mock_response = {
        "team_id": 1,
        "team_name": "Test Team",
        "total_cap": 200000000,
        "used_cap": 150000000,
        "available_cap": 50000000,
        "cap_percentage": 75.0,
        "top_contracts": [],
        "position_breakdown": [],
        "league_avg_available": 40000000,
        "projected_rookie_impact": 10000000
    }
    mock_get_breakdown.return_value = mock_response
    
    # Pass season_id to avoid DB query for active season
    response = client.get("/api/season/team/1/salary-cap?season_id=1")
    
    assert response.status_code == 200
    assert response.json() == mock_response

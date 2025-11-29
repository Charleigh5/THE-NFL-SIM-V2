import requests
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="function")
def season(request):
    """Fixture to initialize a season and return its ID."""
    year = 2025 + hash(str(request.node.nodeid)) % 10000
    url = f"{BASE_URL}/api/season/init"
    payload = {
        "year": year,
        "total_weeks": 18,
        "playoff_weeks": 4
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['id']
    else:
        pytest.fail(f"Failed to initialize season: {response.text}")

def test_get_current_season():
    """Test getting current season."""
    url = f"{BASE_URL}/api/season/current"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "year" in data
    assert "current_week" in data

def test_get_schedule(season):
    """Test getting schedule."""
    url = f"{BASE_URL}/api/season/{season}/schedule"
    response = requests.get(url)
    assert response.status_code == 200

def test_get_schedule_for_week(season):
    """Test getting schedule for a specific week."""
    url = f"{BASE_URL}/api/season/{season}/schedule?week=1"
    response = requests.get(url)
    assert response.status_code == 200

def test_get_standings(season):
    """Test getting standings."""
    url = f"{BASE_URL}/api/season/{season}/standings"
    response = requests.get(url)
    assert response.status_code == 200

def test_advance_week(season):
    """Test advancing week."""
    # Get current week first
    response = requests.get(f"{BASE_URL}/api/season/{season}")
    assert response.status_code == 200
    current_week = response.json()['current_week']
    print(f"Current week before advancing: {current_week}")

    url = f"{BASE_URL}/api/season/{season}/advance-week"
    response = requests.post(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Current week after advancing: {data['current_week']}")
    assert data["current_week"] == current_week + 1


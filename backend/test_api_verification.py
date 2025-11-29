import requests
import pytest

BASE_URL = "http://localhost:8000/api"

@pytest.mark.parametrize("name, method, url, expected_status", [
    ("1.2 Get All Teams", "GET", f"{BASE_URL}/teams", 200),
    ("1.3a Get Team by ID (Valid)", "GET", f"{BASE_URL}/teams/1", 200),
    ("1.3b Get Team by ID (Invalid)", "GET", f"{BASE_URL}/teams/999", 404),
    ("1.4 Get Team Roster", "GET", f"{BASE_URL}/teams/1/roster", 200),
    ("1.5a Get Player by ID (Valid)", "GET", f"{BASE_URL}/players/1", 200),
    ("1.5b Get Player by ID (Invalid)", "GET", f"{BASE_URL}/players/9999", 404),
])
def test_api_endpoints(name, method, url, expected_status):
    """Test an API endpoint and record results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    if method == "GET":
        response = requests.get(url)
    else:
        response = requests.post(url)
    
    assert response.status_code == expected_status


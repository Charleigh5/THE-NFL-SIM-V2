"""
Test script to verify Season API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_season_init():
    """Test season initialization."""
    print("=" * 60)
    print("TEST 1: Initialize Season 2025")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/season/init"
    payload = {
        "year": 2025,
        "total_weeks": 18,
        "playoff_weeks": 4
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Season Created Successfully!")
            print(f"  - Season ID: {data['id']}")
            print(f"  - Year: {data['year']}")
            print(f"  - Current Week: {data['current_week']}")
            print(f"  - Status: {data['status']}")
            return data['id']
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"⚠ Season already exists. Using existing season.")
            # Get current season instead
            current_response = requests.get(f"{BASE_URL}/api/season/current")
            if current_response.status_code == 200:
                data = current_response.json()
                print(f"  - Season ID: {data['id']}")
                return data['id']
        else:
            print(f"✗ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def test_get_current_season():
    """Test getting current season."""
    print("\n" + "=" * 60)
    print("TEST 2: Get Current Season")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/season/current"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Current Season Retrieved!")
            print(f"  - Season ID: {data['id']}")
            print(f"  - Year: {data['year']}")
            print(f"  - Week: {data['current_week']}")
            return data['id']
        else:
            print(f"✗ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def test_get_schedule(season_id, week=None):
    """Test getting schedule."""
    print("\n" + "=" * 60)
    if week:
        print(f"TEST 3: Get Week {week} Schedule")
    else:
        print("TEST 3: Get Full Schedule")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/season/{season_id}/schedule"
    if week:
        url += f"?week={week}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            games = response.json()
            print(f"✓ Schedule Retrieved!")
            print(f"  - Total Games: {len(games)}")
            
            if games:
                print(f"\n  First 3 games:")
                for game in games[:3]:
                    print(f"    Week {game['week']}: Team {game['home_team_id']} vs Team {game['away_team_id']}")
            return True
        else:
            print(f"✗ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_get_standings(season_id):
    """Test getting standings."""
    print("\n" + "=" * 60)
    print("TEST 4: Get Standings")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/season/{season_id}/standings"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            standings = response.json()
            print(f"✓ Standings Retrieved!")
            print(f"  - Total Teams: {len(standings)}")
            
            if standings:
                print(f"\n  Top 5 Teams:")
                for i, team in enumerate(standings[:5], 1):
                    print(f"    {i}. {team['team_name']}: {team['wins']}-{team['losses']}-{team['ties']} ({team['win_pct']:.3f})")
            return True
        else:
            print(f"✗ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_advance_week(season_id):
    """Test advancing week."""
    print("\n" + "=" * 60)
    print("TEST 5: Advance to Week 2")
    print("=" * 60)
    
    url = f"{BASE_URL}/api/season/{season_id}/advance-week"
    
    try:
        response = requests.post(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Week Advanced!")
            print(f"  - Current Week: {data['current_week']}")
            print(f"  - Status: {data['status']}")
            print(f"  - Message: {data['message']}")
            return True
        else:
            print(f"✗ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n🏈 NFL SIM - Season API Test Suite\n")
    
    # Test 1: Initialize Season
    season_id = test_season_init()
    if not season_id:
        print("\n❌ Season initialization failed. Cannot proceed with other tests.")
        return
    
    # Test 2: Get Current Season
    current_season_id = test_get_current_season()
    
    # Test 3: Get Schedule
    test_get_schedule(season_id, week=1)
    
    # Test 4: Get Standings (will be empty since no games played)
    test_get_standings(season_id)
    
    # Test 5: Advance Week
    test_advance_week(season_id)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()

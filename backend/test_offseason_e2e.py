import requests
import json
import time

BASE_URL = "http://localhost:8000/api/season"
SEASON_YEAR = 2025

def print_step(step):
    print(f"\n{'='*50}\n{step}\n{'='*50}")

def get_current_season():
    try:
        response = requests.get(f"{BASE_URL}/current")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def init_season():
    print_step("Initializing Season")
    payload = {
        "year": SEASON_YEAR,
        "total_weeks": 18,
        "playoff_weeks": 4
    }
    try:
        response = requests.post(f"{BASE_URL}/init", json=payload)
        if response.status_code == 200:
            print(f"Season {SEASON_YEAR} initialized successfully.")
            return response.json()["id"]
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"Season {SEASON_YEAR} already exists.")
            season = get_current_season()
            if season:
                return season["id"]
            # Fallback if current fails but init says exists (maybe inactive?)
            # Just assume ID 1 for now or try to fetch by ID
            return 1
        else:
            print(f"Failed to initialize season: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def simulate_to_offseason(season_id):
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    print(f"Current Status: {season['status']}, Week: {season['current_week']}")
    
    # Regular Season
    if season['status'] == "REGULAR_SEASON":
        print_step("Simulating Regular Season")
        while season['current_week'] <= 18:
            print(f"Simulating Week {season['current_week']}...")
            requests.post(f"{BASE_URL}/{season_id}/simulate-week", params={"week": season['current_week']})
            season = requests.get(f"{BASE_URL}/{season_id}").json()
            
        # Generate Playoffs
        print("Generating Playoffs...")
        requests.post(f"{BASE_URL}/{season_id}/playoffs/generate")
        season = requests.get(f"{BASE_URL}/{season_id}").json()

    # Playoffs
    if season['status'] == "POST_SEASON":
        print_step("Simulating Playoffs")
        while season['status'] == "POST_SEASON":
            print(f"Simulating Playoff Week {season['current_week']}...")
            
            # Simulate games
            requests.post(f"{BASE_URL}/{season_id}/simulate-week", params={"week": season['current_week']})
            
            # Advance round
            resp = requests.post(f"{BASE_URL}/{season_id}/playoffs/advance")
            
            # Check if we are stuck
            new_season = requests.get(f"{BASE_URL}/{season_id}").json()
            if new_season['current_week'] == season['current_week'] and new_season['status'] == season['status']:
                # Maybe we need to manually trigger offseason start if we are at week 22 and games are done?
                # The advance_round logic in backend should handle it, but let's see.
                # If we are at Super Bowl (Week 22) and it's played, advance_round should have done something.
                # If it didn't, maybe we need to break and let the next step handle it.
                print("Stuck at same week/status. Breaking loop.")
                break
            season = new_season
            
            # Check if we moved to offseason (week > 22 or status changed)
            if season['status'] == "OFF_SEASON":
                break
            if season['current_week'] > 22: # Safety break
                break

    print(f"Reached Status: {season['status']}")
    return season['status'] == "OFF_SEASON"

def test_offseason_flow(season_id):
    print_step("Testing Offseason Flow")
    
    # 1. Start Offseason
    print("Starting Offseason...")
    resp = requests.post(f"{BASE_URL}/{season_id}/offseason/start")
    if resp.status_code == 200:
        print("✅ Offseason started successfully")
    else:
        print(f"❌ Failed to start offseason: {resp.text}")
        return

    # 2. Simulate Draft
    print("\nSimulating Draft...")
    resp = requests.post(f"{BASE_URL}/{season_id}/draft/simulate")
    if resp.status_code == 200:
        print("✅ Draft simulated successfully")
    else:
        print(f"❌ Failed to simulate draft: {resp.text}")
        return

    # 3. Simulate Free Agency
    print("\nSimulating Free Agency...")
    resp = requests.post(f"{BASE_URL}/{season_id}/free-agency/simulate")
    if resp.status_code == 200:
        print("✅ Free Agency simulated successfully")
    else:
        print(f"❌ Failed to simulate free agency: {resp.text}")
        return

    print("\n🎉 Offseason End-to-End Test Passed!")

def main():
    season_id = init_season()
    if not season_id:
        return

    # Fast forward to offseason if needed
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    if season['status'] != "OFF_SEASON":
        if not simulate_to_offseason(season_id):
            print("Failed to reach offseason state.")
            return

    test_offseason_flow(season_id)

if __name__ == "__main__":
    main()

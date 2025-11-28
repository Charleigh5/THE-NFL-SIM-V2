import requests
import time
import json

BASE_URL = "http://localhost:8000/api/season"
SEASON_YEAR = 2025

def print_step(step):
    print(f"\n{'='*50}\n{step}\n{'='*50}")

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
            print(f"Season {SEASON_YEAR} already exists. Fetching ID...")
            # Fetch existing season ID (assuming we can get it from current or by ID)
            # For simplicity, let's try to get the season by year if possible, or just assume ID 1 or fetch current
            response = requests.get(f"{BASE_URL}/current")
            if response.status_code == 200:
                season = response.json()
                if season["year"] == SEASON_YEAR:
                    print(f"Found existing season {SEASON_YEAR} with ID {season['id']}")
                    return season["id"]
            print("Could not find existing season ID easily.")
            return None
        else:
            print(f"Failed to initialize season: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def simulate_regular_season(season_id):
    print_step("Simulating Regular Season")
    for week in range(1, 19):
        print(f"Simulating Week {week}...")
        response = requests.post(f"{BASE_URL}/{season_id}/simulate-week", params={"week": week})
        if response.status_code == 200:
            print(f"Week {week} simulated.")
        else:
            print(f"Failed to simulate week {week}: {response.text}")
            return False
    return True

def generate_playoffs(season_id):
    print_step("Generating Playoffs")
    response = requests.post(f"{BASE_URL}/{season_id}/playoffs/generate")
    if response.status_code == 200:
        print("Playoff bracket generated.")
        return True
    else:
        print(f"Failed to generate playoffs: {response.text}")
        return False

def get_bracket(season_id):
    print_step("Fetching Bracket")
    response = requests.get(f"{BASE_URL}/{season_id}/playoffs/bracket")
    if response.status_code == 200:
        bracket = response.json()
        print(f"Bracket has {len(bracket)} matchups.")
        for m in bracket:
            print(f"{m['round']} - {m['matchup_code']}: {m['home_team_id']} vs {m['away_team_id']} (Winner: {m['winner_id']})")
        return bracket
    else:
        print(f"Failed to fetch bracket: {response.text}")
        return None

def simulate_playoff_round(season_id, week, round_name):
    print_step(f"Simulating {round_name} (Week {week})")
    response = requests.post(f"{BASE_URL}/{season_id}/simulate-week", params={"week": week})
    if response.status_code == 200:
        results = response.json()
        print(f"Simulated {results['games_simulated']} games.")
        for gid, res in results['results'].items():
            print(f"  Game {gid}: {res['home_score']}-{res['away_score']} (Winner: {res['winner']})")
        return True
    else:
        print(f"Failed to simulate {round_name}: {response.text}")
        return False

def advance_round(season_id):
    print_step("Advancing Playoff Round")
    response = requests.post(f"{BASE_URL}/{season_id}/playoffs/advance")
    if response.status_code == 200:
        print("Round advanced successfully.")
        return True
    else:
        print(f"Failed to advance round: {response.text}")
        return False

def main():
    season_id = init_season()
    if not season_id:
        return

    # Check current status
    response = requests.get(f"{BASE_URL}/{season_id}")
    season = response.json()
    print(f"Current Season Status: {season['status']}, Week: {season['current_week']}")

    if season['status'] == "REGULAR_SEASON":
        current_week = season['current_week']
        if current_week <= 18:
            # Finish regular season
            for week in range(current_week, 19):
                print(f"Simulating Week {week}...")
                requests.post(f"{BASE_URL}/{season_id}/simulate-week", params={"week": week})
        
        # Check if we need to generate playoffs
        season = requests.get(f"{BASE_URL}/{season_id}").json()
        if season['status'] == "REGULAR_SEASON" and season['current_week'] > 18:
             # It should have auto-switched or we need to trigger it?
             # The advance_week endpoint handles transition, but simulate_week also does auto-advance.
             # Let's try generating playoffs.
             pass

    # Generate Playoffs if needed
    # Try generating, if it fails it might be because it's already generated or not ready
    if season['status'] == "REGULAR_SEASON" or (season['status'] == "POST_SEASON" and season['current_week'] == 19):
         # Try generating
         print("Attempting to generate playoffs...")
         resp = requests.post(f"{BASE_URL}/{season_id}/playoffs/generate")
         print(f"Generate response: {resp.status_code} - {resp.text}")

    # Now we should be in POST_SEASON
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    print(f"Status after regular season: {season['status']}")
    
    if season['status'] != "POST_SEASON":
        print("Failed to reach POST_SEASON. Exiting.")
        return

    # Wild Card Round (Week 19)
    if season['current_week'] == 19:
        get_bracket(season_id)
        simulate_playoff_round(season_id, 19, "Wild Card Round")
        advance_round(season_id)
    
    # Divisional Round (Week 20)
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    if season['current_week'] == 20:
        simulate_playoff_round(season_id, 20, "Divisional Round")
        advance_round(season_id)

    # Conference Round (Week 21)
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    if season['current_week'] == 21:
        simulate_playoff_round(season_id, 21, "Conference Round")
        advance_round(season_id)

    # Super Bowl (Week 22)
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    if season['current_week'] == 22:
        simulate_playoff_round(season_id, 22, "Super Bowl")
        advance_round(season_id)

    # Final Check
    season = requests.get(f"{BASE_URL}/{season_id}").json()
    print(f"Final Season Status: {season['status']}")
    get_bracket(season_id)

if __name__ == "__main__":
    main()

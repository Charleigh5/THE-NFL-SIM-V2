import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def get_current_season():
    try:
        response = requests.get(f"{BASE_URL}/api/season/current")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend.")
        sys.exit(1)

def init_season():
    print("Initializing new season...")
    # Trying 2024, or 2025 if 2024 exists
    year = 2024

    # Check if 2024 exists
    try:
        current = get_current_season()
        if current and current['year'] == year:
            print(f"Season {year} already active. Using it.")
            return current
    except:
        pass

    payload = {
        "year": year,
        "total_weeks": 18,
        "playoff_weeks": 4
    }
    response = requests.post(f"{BASE_URL}/api/season/init", json=payload)

    if response.status_code == 400 and "already exists" in response.text:
        # If it exists but isn't active/current, we might need to find it or just use current
        # For simplicity, let's assume if it exists we can use it.
        # But if we want a fresh start, we might need to clear DB.
        # Since I can't easily clear DB via API, I'll try 2025.
        payload["year"] = 2025
        response = requests.post(f"{BASE_URL}/api/season/init", json=payload)

    if response.status_code != 200:
        print(f"Failed to init season: {response.text}")
        # Fallback to current season if available
        current = get_current_season()
        if current:
            print(f"Falling back to current season {current['year']}")
            return current
        sys.exit(1)

    return response.json()

def simulate_season(season_id, total_weeks):
    print(f"Simulating Season {season_id}...")

    while True:
        # Get status
        season = requests.get(f"{BASE_URL}/api/season/{season_id}").json()
        current_week = season['current_week']
        status = season['status']

        print(f"Status: {status}, Week: {current_week}")

        if status == "OFF_SEASON":
            print("Season complete!")
            break

        if status == "POST_SEASON":
            # Check if playoffs are done?
            # The API advance_week handles transition to offseason eventually
            pass

        # Simulate Week
        print(f"Simulating Week {current_week}...")
        start_time = time.time()
        resp = requests.post(
            f"{BASE_URL}/api/season/{season_id}/simulate-week",
            params={"play_count": 50} # Fast sim
        )
        if resp.status_code != 200:
            print(f"Error simulating week: {resp.text}")
            break

        duration = time.time() - start_time
        print(f"Week {current_week} done in {duration:.2f}s")

        # Check if we should stop (safety break)
        if current_week > 25: # Super bowl is usually week 22 or so
            print("Safety break triggered.")
            break

def fetch_results(season_id):
    print("Fetching season results...")

    results = {}

    # 1. Summary (Standings & Leaders)
    summary_resp = requests.get(f"{BASE_URL}/api/season/summary")
    if summary_resp.status_code == 200:
        summary = summary_resp.json()
        results['standings'] = summary.get('standings')
        results['league_leaders'] = summary.get('league_leaders')
        results['season_info'] = summary.get('season')
        results['playoff_bracket'] = summary.get('playoff_bracket')

    # 2. Projected Awards (Defense/MVP)
    awards_resp = requests.get(f"{BASE_URL}/api/season/{season_id}/awards/projected")
    if awards_resp.status_code == 200:
        results['awards'] = awards_resp.json()

    return results

def main():
    # 1. Init
    season = init_season()
    season_id = season['id']
    total_weeks = season['total_weeks']

    # 2. Sim
    simulate_season(season_id, total_weeks)

    # 3. Results
    results = fetch_results(season_id)

    # 4. Save
    with open("season_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Results saved to season_results.json")

    # Print a quick summary to console
    print("\n" + "="*50)
    print("SEASON SUMMARY")
    print("="*50)

    if results.get('standings'):
        print("\nConference Standings:")
        for conf in results['standings']:
            print(f"\n{conf['conference']}")
            for div in conf['divisions']:
                print(f"  {div['division']}")
                for team in div['teams']:
                    print(f"    {team['team_name']:20} {team['wins']}-{team['losses']}-{team['ties']}")

    if results.get('league_leaders'):
        leaders = results['league_leaders']
        print("\nLeague Leaders:")
        if leaders.get('passing_yards'):
            print("\n  Passing Yards:")
            for p in leaders['passing_yards'][:5]:
                print(f"    {p['name']} ({p['team']}): {p['value']}")
        if leaders.get('rushing_yards'):
            print("\n  Rushing Yards:")
            for p in leaders['rushing_yards'][:5]:
                print(f"    {p['name']} ({p['team']}): {p['value']}")
        if leaders.get('receiving_yards'):
            print("\n  Receiving Yards:")
            for p in leaders['receiving_yards'][:5]:
                print(f"    {p['name']} ({p['team']}): {p['value']}")

    if results.get('awards'):
        awards = results['awards']
        if awards.get('dpoy'):
             print("\n  Top Defenders (DPOY Candidates):")
             for p in awards['dpoy'][:5]:
                 print(f"    {p['name']} ({p['team']}) - Score: {p['score']:.1f}")
                 print(f"      {p['stats']}")

if __name__ == "__main__":
    main()

"""
Test batch simulation of a week.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def main():
    print("\n🏈 NFL SIM - Batch Simulation Test\n")
    
    # Get current season
    print("=" * 60)
    print("Getting Current Season...")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/season/current")
    if response.status_code != 200:
        print(f"✗ Failed to get current season: {response.text}")
        return
    
    season = response.json()
    print(f"✓ Season {season['year']} - Week {season['current_week']}")
    print(f"  Status: {season['status']}")
    
    # Simulate Week 1
    print("\n" + "=" * 60)
    print(f"Simulating Week {season['current_week']}...")
    print("=" * 60)
    print("(This may take a minute...)\n")
    
    sim_response = requests.post(
        f"{BASE_URL}/api/season/{season['id']}/simulate-week",
        params={"play_count": 50}  # Reduced for faster testing
    )
    
    if sim_response.status_code != 200:
        print(f"✗ Simulation failed: {sim_response.text}")
        return
    
    results = sim_response.json()
    
    print(f"✓ Simulation Complete!")
    print(f"  Games Simulated: {results.get('games_simulated', 0)}")
    print(f"\n  Results:")
    
    for game_id, game_result in results.get('results', {}).items():
        home_score = game_result['home_score']
        away_score = game_result['away_score']
        winner = game_result['winner']
        print(f"    Game {game_id}: Team {game_result['home_team_id']} vs Team {game_result['away_team_id']}")
        print(f"      Final Score: {home_score}-{away_score} ({winner} wins)")
    
    # Get updated standings
    print("\n" + "=" * 60)
    print("Updated Standings:")
    print("=" * 60)
    
    standings_response = requests.get(f"{BASE_URL}/api/season/{season['id']}/standings")
    if standings_response.status_code == 200:
        standings = standings_response.json()
        
        print("\nTop 10 Teams:")
        for i, team in enumerate(standings[:10], 1):
            record = f"{team['wins']}-{team['losses']}-{team['ties']}"
            pf = team['points_for']
            pa = team['points_against']
            print(f"  {i:2d}. {team['team_name']:25s} {record:7s} PF:{pf:3d} PA:{pa:3d}")
    
    print("\n" + "=" * 60)
    print("✅ BATCH SIMULATION TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()

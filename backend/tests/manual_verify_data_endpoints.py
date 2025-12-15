import requests
import sys

BASE_URL = "http://localhost:8000/api/data"

def test_teams():
    print("Testing /teams...")
    try:
        r = requests.get(f"{BASE_URL}/teams")
        r.raise_for_status()
        data = r.json()
        print(f"Success! Found {data['count']} teams.")
        if data['count'] > 0:
            print(f"Sample team: {data['teams'][0]['name']}")
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit(1)

def test_players():
    print("\nTesting /players...")
    try:
        r = requests.get(f"{BASE_URL}/players?limit=5")
        r.raise_for_status()
        data = r.json()
        print(f"Success! Found {data['count']} players.")
        if data['count'] > 0:
            print(f"Sample player: {data['players'][0]['first_name']} {data['players'][0]['last_name']}")
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit(1)

def test_game_state():
    print("\nTesting /game-state/1...")
    try:
        r = requests.get(f"{BASE_URL}/game-state/1")
        if r.status_code == 404:
            print("Game 1 not found (expected if DB is fresh/empty of games)")
        else:
            r.raise_for_status()
            data = r.json()
            print(f"Success! Game State: {data}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_teams()
    test_players()
    test_game_state()

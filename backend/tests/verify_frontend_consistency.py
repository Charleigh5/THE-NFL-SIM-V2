import asyncio
import websockets
import httpx
import json
import sys

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/simulation/live"

async def verify_consistency():
    print("Verifying Frontend Consistency...")
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("Connected to WebSocket")
            
            # Start Simulation
            async with httpx.AsyncClient() as client:
                print("Starting live simulation...")
                response = await client.post(f"{BASE_URL}/api/simulation/start-live", json={"num_plays": 5})
                if response.status_code != 200:
                    print(f"FAIL: Failed to start simulation: {response.text}")
                    return
                
                data = response.json()
                game_id = data.get("game_id")
                print(f"Simulation started. Game ID: {game_id}")
                
                # Listen for updates
                ws_plays = []
                ws_state = None
                
                try:
                    # Listen for 5 plays worth of time or until we get 5 plays
                    while len(ws_plays) < 5:
                        message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                        data = json.loads(message)
                        
                        if data["type"] == "PLAY_RESULT":
                            print(f"Received Play: {data['payload']['description']}")
                            ws_plays.append(data['payload'])
                        elif data["type"] == "GAME_UPDATE":
                            ws_state = data['payload']
                            # print(f"Received State Update: Score {ws_state['homeScore']}-{ws_state['awayScore']}")
                            
                except asyncio.TimeoutError:
                    print("Timeout waiting for plays")
                
                # Stop Simulation (if not already done)
                await client.post(f"{BASE_URL}/api/simulation/stop")
                print("Simulation stopped")
                
                # Fetch Results from API
                print(f"Fetching results for Game ID {game_id}...")
                response = await client.get(f"{BASE_URL}/api/simulation/results/{game_id}")
                if response.status_code != 200:
                    print(f"FAIL: Failed to fetch results: {response.text}")
                    return
                    
                db_data = response.json()
                db_plays = db_data["results"].get("plays", [])
                
                # Compare
                print("Comparing WS data with DB data...")
                
                # Compare number of plays
                print(f"WS Plays: {len(ws_plays)}, DB Plays: {len(db_plays)}")
                
                if len(ws_plays) == len(db_plays):
                    print("PASS: Play count matches")
                else:
                    print("WARN: Play count mismatch (might be timing)")
                    
                # Compare content of first play
                if len(ws_plays) > 0 and len(db_plays) > 0:
                    ws_p = ws_plays[0]
                    db_p = db_plays[0]
                    # Check description match
                    if ws_p['description'] == db_p['description']:
                        print("PASS: Play content matches")
                    else:
                        print(f"FAIL: Play content mismatch. WS: {ws_p['description']}, DB: {db_p['description']}")
                
                # Compare Score
                if ws_state:
                    if ws_state['homeScore'] == db_data['home_score']:
                        print("PASS: Home score matches")
                    else:
                        print(f"FAIL: Home score mismatch. WS: {ws_state['homeScore']}, DB: {db_data['home_score']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_consistency())

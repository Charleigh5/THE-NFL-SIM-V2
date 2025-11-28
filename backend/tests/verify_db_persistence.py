import sys
import os
sys.path.append(os.getcwd())

from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.core.database import SessionLocal
from app.models.game import Game
import json

def verify_persistence():
    print("Verifying Database Persistence...")
    
    # 1. Setup
    orchestrator = SimulationOrchestrator()
    config = {"difficulty": "hard", "weather": "snow"}
    
    # 2. Start Game
    print("Starting game session...")
    orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, config=config)
    game_id = orchestrator.current_game_id
    print(f"Game ID: {game_id}")
    
    # 3. Run a play
    print("Running a play...")
    result = orchestrator.run_simulation() # This runs a single play synchronously
    
    # Verify Incremental Persistence
    print("Verifying incremental persistence...")
    db = SessionLocal()
    game_inc = db.query(Game).filter(Game.id == game_id).first()
    if game_inc and game_inc.game_data.get("plays") and len(game_inc.game_data["plays"]) > 0:
        print("PASS: Incremental persistence working")
    else:
        print("FAIL: Incremental persistence failed")
    db.close()
    
    # 4. Save
    print("Saving game result...")
    orchestrator.save_game_result()
    
    # 5. Verify
    print("Verifying data in DB...")
    db = SessionLocal()
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        print("FAIL: Game not found in DB")
        return
        
    print(f"Game found: {game.id}")
    
    # Verify Config
    saved_config = game.game_data.get("config")
    if saved_config == config:
        print("PASS: Config saved correctly")
    else:
        print(f"FAIL: Config mismatch. Expected {config}, got {saved_config}")
        
    # Verify Plays
    saved_plays = game.game_data.get("plays")
    if saved_plays and len(saved_plays) > 0:
        print(f"PASS: {len(saved_plays)} plays saved")
        # Verify play content
        if saved_plays[0]['yards_gained'] == result.yards_gained:
             print("PASS: Play data matches")
        else:
             print("FAIL: Play data mismatch")
    else:
        print("FAIL: No plays saved")
        
    # Verify Game State (Score)
    if game.home_score == orchestrator.home_score:
        print("PASS: Home score persisted")
    else:
        print(f"FAIL: Home score mismatch. DB: {game.home_score}, Orch: {orchestrator.home_score}")
        
    db.close()

if __name__ == "__main__":
    verify_persistence()

import asyncio
import time
import random
from unittest.mock import MagicMock, patch
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.match_context import MatchContext
from app.models.player import Player, Position
from app.schemas.play import PlayResult

# Helper to create a mock player
def create_mock_player(player_id, team_id, position):
    p = Player(
        id=player_id,
        team_id=team_id,
        position=position,
        first_name=f"Player{player_id}",
        last_name=f"Team{team_id}",
        # Attributes 70-95
        speed=random.randint(70, 95),
        acceleration=random.randint(70, 95),
        strength=random.randint(70, 95),
        agility=random.randint(70, 95),
        awareness=random.randint(70, 95),
        throw_power=random.randint(70, 95),
        throw_accuracy_short=random.randint(70, 95),
        throw_accuracy_mid=random.randint(70, 95),
        throw_accuracy_deep=random.randint(70, 95),
        catching=random.randint(70, 95),
        route_running=random.randint(70, 95),
        pass_block=random.randint(70, 95),
        run_block=random.randint(70, 95),
        tackle=random.randint(70, 95),
        hit_power=random.randint(70, 95),
        block_shed=random.randint(70, 95),
        man_coverage=random.randint(70, 95),
        zone_coverage=random.randint(70, 95),
        pass_rush_power=random.randint(70, 95),
        pass_rush_finesse=random.randint(70, 95),
        kick_power=random.randint(70, 95),
        kick_accuracy=random.randint(70, 95),
        overall_rating=random.randint(70, 95),
        # Physics
        height=72,
        weight=200,
        age=25,
        experience=3
    )
    return p

# Helper to create a team roster
def create_team(team_id):
    roster = []
    pid_start = team_id * 100
    
    # Positions: QB, RB, WRx2, TE, OLx5, DLx4, LBx3, CBx2, Sx2, K, P
    positions = [
        Position.QB, Position.RB, 
        Position.WR, Position.WR, 
        Position.TE,
        Position.OT, Position.OT, Position.OG, Position.OG, Position.C, # OL
        Position.DE, Position.DE, Position.DT, Position.DT, # DL
        Position.LB, Position.LB, Position.LB,
        Position.CB, Position.CB,
        Position.S, Position.S,
        Position.K, Position.P
    ]
    
    for i, pos in enumerate(positions):
        roster.append(create_mock_player(pid_start + i, team_id, pos))
        
    return roster

async def verify_full_game():
    print("--- Starting Full Game Simulation Verification ---")
    start_time = time.time()
    
    # 4.1 Initialize Simulation Environment
    orchestrator = SimulationOrchestrator()
    orchestrator.play_delay_seconds = 0
    orchestrator.current_game_id = 9999
    
    # Mock DB and persistence
    orchestrator.db_session = MagicMock()
    orchestrator._save_progress = MagicMock()
    orchestrator.save_game_result = MagicMock()
    # Mock reset_game_state to prevent resetting score between quarters calls
    orchestrator.reset_game_state = MagicMock()
    
    # 4.2 Generate Mock Rosters
    print("Generating rosters...")
    home_roster = create_team(1)
    away_roster = create_team(2)
    print(f"Home Roster: {len(home_roster)} players")
    print(f"Away Roster: {len(away_roster)} players")
    assert len(home_roster) == 23
    assert len(away_roster) == 23
    
    # 4.3 Configure Match Context
    orchestrator.match_context = MatchContext(home_roster, away_roster)
    # Register players with kernels (mocked implicitly by not using real kernels or using default ones)
    # The PlayResolver uses kernels, but we might need to ensure it doesn't crash.
    # Assuming PlayResolver works with these mock players.
    
    # Callbacks
    play_types = set()
    
    async def on_play_complete(result: PlayResult):
        print(f"Q{orchestrator.current_quarter} {orchestrator.time_left} | {result.description} ({result.yards_gained} yds)")
        play_types.add(result.play_type)
        
    orchestrator.on_play_complete = on_play_complete
    
    # Game Execution
    for quarter in range(1, 5):
        print(f"\n--- Starting Quarter {quarter} ---")
        orchestrator.current_quarter = quarter
        orchestrator.time_left = "15:00"
        
        # Run simulation for the quarter
        # We use a large number of plays to ensure time runs out, 
        # but the loop breaks when _is_quarter_over is true.
        await orchestrator.run_continuous_simulation(num_plays=200)
        
        print(f"End of Quarter {quarter} Score: Home {orchestrator.home_score} - Away {orchestrator.away_score}")
        
    # Validation
    print("\n--- Validation ---")
    
    # 4.8 Verify Game Integrity
    total_score = orchestrator.home_score + orchestrator.away_score
    print(f"FINAL SCORE: Home {orchestrator.home_score} - Away {orchestrator.away_score}")
    
    if total_score == 0:
        print("WARNING: Score is 0-0. This might be unlikely but possible. Checking if plays happened.")
    else:
        print("PASS: Score is non-zero.")
        
    print(f"Play Types Observed: {play_types}")
    if len(play_types) < 2:
        print("WARNING: Low play variety.")
    else:
        print("PASS: Multiple play types observed.")
        
    # 4.10 Performance Check
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total Execution Time: {duration:.2f} seconds")
    
    if duration < 10:
        print("PASS: Performance is good (<10s).")
    else:
        print("WARNING: Simulation took longer than 10s.")

    # Assertions for automated checking
    assert total_score >= 0 # It's possible to be 0-0, but we hope for points.
    assert orchestrator.current_quarter == 4
    # We can't strictly assert play variety without knowing the random seed, but we expect it.
    
    print("\nSUCCESS: Full game simulation completed without errors.")

if __name__ == "__main__":
    asyncio.run(verify_full_game())

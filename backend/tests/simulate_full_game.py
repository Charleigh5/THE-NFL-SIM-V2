
import asyncio
import sys
import os
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.models.player import Player
from app.orchestrator.match_context import MatchContext

async def run_full_game():
    print("Initializing Full Game Simulation...")
    
    orchestrator = SimulationOrchestrator()
    orchestrator.play_delay_seconds = 0 # Speed up simulation
    
    # Mock Database Session to avoid needing a real DB connection for this test
    # We will manually hydrate the MatchContext with mock players
    orchestrator.db_session = MagicMock()
    orchestrator.current_game_id = 9999 # Dummy ID
    
    # Create Mock Players
    def create_team(team_id, prefix):
        players = []
        positions = ["QB", "RB", "WR", "WR", "TE", "OT", "OT", "OG", "OG", "C",
                     "DE", "DE", "DT", "DT", "LB", "LB", "LB", "CB", "CB", "S", "S", "K", "P"]
        for i, pos in enumerate(positions):
            p = Player(
                id=team_id*100 + i,
                first_name=f"{prefix}",
                last_name=f"{pos}",
                position=pos,
                team_id=team_id,
                speed=random.randint(70, 95),
                throw_accuracy_short=random.randint(70, 90),
                throw_accuracy_mid=random.randint(70, 90),
                throw_accuracy_deep=random.randint(70, 90),
                route_running=random.randint(70, 90),
                man_coverage=random.randint(70, 90),
                overall_rating=random.randint(70, 90),
                strength=random.randint(70, 90),
                tackle=random.randint(70, 90)
            )
            players.append(p)
        return players

    import random
    home_roster = create_team(1, "Home")
    away_roster = create_team(2, "Away")
    
    print(f"Created rosters: Home ({len(home_roster)}), Away ({len(away_roster)})")
    
    orchestrator.match_context = MatchContext(home_roster, away_roster)
    
    # Mock the save methods to avoid DB errors
    orchestrator._save_progress = MagicMock()
    orchestrator.save_game_result = MagicMock()
    
    # Mock callbacks
    async def on_play(result):
        print(f"PLAY: {result.description}")
        
    async def on_update(state):
        # Print score updates
        pass
        
    orchestrator.on_play_complete = on_play
    orchestrator.on_game_update = on_update
    
    # Run Simulation
    # We'll run enough plays to likely finish a game or at least a quarter
    # The orchestrator stops when quarter is over. We might need to loop quarters.
    
    print("\n--- KICKOFF ---")
    
    for q in range(1, 5):
        print(f"\nStarting Quarter {q}")
        orchestrator.current_quarter = q
        orchestrator.time_left = "15:00"
        
        # Run quarter
        # We pass a large number of plays, it should stop when time runs out
        await orchestrator.run_continuous_simulation(num_plays=200)
        
        print(f"End of Quarter {q}. Score: Home {orchestrator.home_score} - Away {orchestrator.away_score}")
        
    print("\n--- FINAL SCORE ---")
    print(f"Home: {orchestrator.home_score}")
    print(f"Away: {orchestrator.away_score}")
    
    if orchestrator.home_score == 0 and orchestrator.away_score == 0:
        print("WARNING: Score is 0-0. Check if scoring logic is working.")
    else:
        print("Simulation produced a result.")

if __name__ == "__main__":
    asyncio.run(run_full_game())

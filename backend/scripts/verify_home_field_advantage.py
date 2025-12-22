
import asyncio
import time
import random
import sys
import os
from unittest.mock import MagicMock, AsyncMock
from typing import List, Dict

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.match_context import MatchContext
from app.models.player import Player, Position
from app.schemas.play import PlayResult

# --- Mock Helpers (Adapted from tests/verify_full_game.py) ---

def create_mock_player(player_id, team_id, position):
    p = Player(
        id=player_id,
        team_id=team_id,
        position=position,
        first_name=f"P{player_id}",
        last_name=f"T{team_id}",
        # Average attributes
        speed=80, acceleration=80, strength=80, agility=80, awareness=80,
        throw_power=80, throw_accuracy_short=80, throw_accuracy_mid=80, throw_accuracy_deep=80,
        catching=80, route_running=80, pass_block=80, run_block=80,
        tackle=80, hit_power=80, block_shed=80, man_coverage=80, zone_coverage=80,
        pass_rush_power=80, pass_rush_finesse=80, kick_power=80, kick_accuracy=80,
        overall_rating=80,
        height=72, weight=200, age=25, experience=3,
        attribute_xp={},
        season_stats=[]
    )
    return p

def create_team(team_id):
    roster = []
    pid_start = team_id * 1000
    positions = [
        Position.QB, Position.RB, Position.WR, Position.WR, Position.TE,
        Position.OT, Position.OT, Position.OG, Position.OG, Position.C,
        Position.DE, Position.DE, Position.DT, Position.DT,
        Position.LB, Position.LB, Position.LB,
        Position.CB, Position.CB, Position.S, Position.S,
        Position.K, Position.P
    ]
    for i, pos in enumerate(positions):
        roster.append(create_mock_player(pid_start + i, team_id, pos))
    return roster

# --- Simulation Logic ---

async def simulate_single_game(game_config: Dict, home_roster: List[Player], away_roster: List[Player]):
    orchestrator = SimulationOrchestrator()
    orchestrator.play_delay_seconds = 0
    orchestrator.current_game_id = 9999

    # Configure Venue
    orchestrator.game_config = game_config

    # Mock DB/Persistence
    orchestrator.db_session = MagicMock()
    # Make async methods awaitable
    orchestrator.db_session.execute = AsyncMock()
    orchestrator.db_session.commit = AsyncMock()
    orchestrator.db_session.add = MagicMock() # sync method usually? No, add is sync, commit/execute async

    orchestrator._save_progress = AsyncMock()
    orchestrator.save_game_result = AsyncMock()
    orchestrator.reset_game_state = MagicMock() # Sync

    # Setup Context
    orchestrator.match_context = MatchContext(1, 2, orchestrator.db_session)
    # Manually populate rosters since we mocked db loading
    orchestrator.match_context.home_roster = {p.id: p for p in home_roster}
    orchestrator.match_context.away_roster = {p.id: p for p in away_roster}
    orchestrator.match_context.home_team_id = 1
    orchestrator.match_context.away_team_id = 2
    # Reset State Once
    orchestrator.reset_game_state()

    # Run Game Loop (4 Quarters)
    total_plays = 160
    for _ in range(total_plays):
        await orchestrator._execute_single_play()
        # Basic quarter management
        if orchestrator.time_left == "00:00":
             orchestrator.current_quarter += 1
             orchestrator.time_left = "15:00"

        if orchestrator.current_quarter > 4:
            break

    return orchestrator.home_score, orchestrator.away_score

async def run_series(label: str, game_config: Dict, num_games: int):
    print(f"\nrunning {label} ({num_games} games)...")
    print(f"Config: {game_config}")

    home_roster = create_team(1)
    away_roster = create_team(2)

    home_wins = 0
    total_margin = 0
    home_points = 0
    away_points = 0

    start_time = time.time()

    for i in range(num_games):
        h, a = await simulate_single_game(game_config, home_roster, away_roster)
        home_points += h
        away_points += a
        margin = h - a
        total_margin += margin
        if h > a: home_wins += 1

        if (i+1) % 50 == 0:
            print(f"  Simulated {i+1}/{num_games} games...", end='\r')

    duration = time.time() - start_time

    avg_margin = total_margin / num_games
    avg_home = home_points / num_games
    avg_away = away_points / num_games
    win_pct = (home_wins / num_games) * 100

    print(f"\n{label} RESULTS:")
    print(f"  Games: {num_games}")
    print(f"  Time: {duration:.2f}s ({(duration/num_games):.3f}s/game)")
    print(f"  Home Win %: {win_pct:.1f}%")
    print(f"  Avg Score: {avg_home:.1f} - {avg_away:.1f}")
    print(f"  Avg Margin: {avg_margin:+.2f}")

    return avg_margin

async def main():
    print("=== GAME-010: HOME FIELD ADVANTAGE VERIFICATION ===")

    # 1. Neutral Site (Control)
    # Altitude 0, Noise 70 (Quiet/Moderate)
    neutral_config = {
        "stadium_id": "NEU",
        "stadium_name": "Neutral Field",
        "noise_rating": 70, # Moderate
        "altitude": 0
    }

    # 2. Hostile Site (Test)
    # Altitude 5280 (Denver), Noise 95 (Arrowhead) -> Max Advantage
    hostile_config = {
        "stadium_id": "HOS",
        "stadium_name": "Hostile Dome",
        "noise_rating": 95, # Deafening potential
        "altitude": 5280
    }

    N = 100 # Start with 100 for speed, user asked for more but 100 gives sig. signal

    margin_neutral = await run_series("NEUTRAL CONTROL", neutral_config, N)
    margin_hostile = await run_series("HOSTILE TEST", hostile_config, N)

    diff = margin_hostile - margin_neutral
    print("\n=== FINAL ANALYSIS ===")
    print(f"Neutral Margin: {margin_neutral:+.2f}")
    print(f"Hostile Margin: {margin_hostile:+.2f}")
    print(f"HFA Impact: {diff:+.2f} points")

    if diff > 1.5:
        print("✅ SUCCESS: Significant Home Field Advantage detected.")
    else:
        print("⚠️ WARNING: HFA impact lower than expected (< 1.5). Check logic.")

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Monte Carlo Statistical Calibration Engine - THE-NFL-SIM-V2
===========================================================
Executes headless batch simulations of NFL games to calibrate and benchmark
emergent game physics, pass completion, sack rates, YPC, and scoring distributions
against real NFL historical baselines.
"""

import sys
import os
import argparse
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure backend app is on sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.models.team import Team
from app.models.player import Player
from app.core.random_utils import DeterministicRNG

# Ground Truth Benchmarks from NFL Simulation Engine Implementation Data Table
NFL_BENCHMARKS = {
    "sack_rate": {"target": 0.065, "tolerance": 0.015, "unit": "%", "display_multiplier": 100.0},
    "yards_per_carry": {"target": 4.20, "tolerance": 0.50, "unit": "yds", "display_multiplier": 1.0},
    "completion_rate": {"target": 0.645, "tolerance": 0.045, "unit": "%", "display_multiplier": 100.0},
    "turnovers_per_game": {"target": 1.30, "tolerance": 0.50, "unit": "/gm", "display_multiplier": 1.0},
    "points_per_game": {"target": 21.8, "tolerance": 4.0, "unit": "pts", "display_multiplier": 1.0},
}

def create_mock_team(team_id: int, name: str, is_home: bool = True) -> Team:
    """Create a balanced mock team with standard NFL ratings."""
    base_id = team_id * 100 + (10 if is_home else 50)
    team = Team(id=team_id, name=name, city=name, abbreviation="KC" if is_home else "SF")
    # Add key positions with integer IDs
    players = [
        Player(id=base_id + 1, team_id=team_id, position="QB", overall_rating=85, speed=78, pass_accuracy=86, football_iq=88, age=25, weight=220),
        Player(id=base_id + 2, team_id=team_id, position="RB", overall_rating=84, speed=88, carrying=85, break_tackle=82, strength=78, age=24, weight=215),
        Player(id=base_id + 3, team_id=team_id, position="WR", overall_rating=88, speed=92, catch=89, route_running=87, height=73, age=25, weight=195),
        Player(id=base_id + 4, team_id=team_id, position="WR", overall_rating=80, speed=89, catch=82, route_running=80, height=71, age=26, weight=190),
        Player(id=base_id + 5, team_id=team_id, position="TE", overall_rating=82, speed=80, catch=84, blocking=78, height=77, age=27, weight=250),
        Player(id=base_id + 6, team_id=team_id, position="LT", overall_rating=86, pass_block=86, run_block=85, age=26, weight=315),
        Player(id=base_id + 7, team_id=team_id, position="LG", overall_rating=82, pass_block=82, run_block=84, age=28, weight=310),
        Player(id=base_id + 8, team_id=team_id, position="C", overall_rating=84, pass_block=85, run_block=83, age=27, weight=305),
        Player(id=base_id + 9, team_id=team_id, position="RG", overall_rating=81, pass_block=80, run_block=83, age=25, weight=315),
        Player(id=base_id + 10, team_id=team_id, position="RT", overall_rating=83, pass_block=84, run_block=82, age=26, weight=320),
        # Defense
        Player(id=base_id + 11, team_id=team_id, position="RE", overall_rating=87, pass_rush=88, tackle=84, speed=84, age=26, weight=265),
        Player(id=base_id + 12, team_id=team_id, position="LE", overall_rating=83, pass_rush=84, tackle=80, speed=82, age=25, weight=270),
        Player(id=base_id + 13, team_id=team_id, position="DT", overall_rating=84, pass_rush=80, tackle=88, speed=70, age=27, weight=315),
        Player(id=base_id + 14, team_id=team_id, position="LB", overall_rating=85, tackle=88, coverage=80, speed=85, age=26, weight=235),
        Player(id=base_id + 15, team_id=team_id, position="LB", overall_rating=82, tackle=84, coverage=78, speed=84, age=25, weight=230),
        Player(id=base_id + 16, team_id=team_id, position="CB", overall_rating=86, coverage=88, speed=91, press=82, tackle=72, age=25, weight=195),
        Player(id=base_id + 17, team_id=team_id, position="CB", overall_rating=81, coverage=82, speed=89, press=78, tackle=70, age=24, weight=190),
        Player(id=base_id + 18, team_id=team_id, position="S", overall_rating=84, coverage=85, tackle=82, speed=88, age=27, weight=205),
        Player(id=base_id + 19, team_id=team_id, position="S", overall_rating=80, coverage=80, tackle=80, speed=87, age=25, weight=200),
        # Special teams
        Player(id=base_id + 20, team_id=team_id, position="K", overall_rating=82, kick_power=88, kick_accuracy=84, age=29, weight=190),
        Player(id=base_id + 21, team_id=team_id, position="P", overall_rating=80, kick_power=86, kick_accuracy=80, age=28, weight=210),
    ]
    team.players = players
    return team

def run_batch_simulation(num_games: int = 50) -> Dict[str, Any]:
    """Execute a batch of games and aggregate statistical telemetry."""
    print("\n========================================================")
    print(f"[MONTE CARLO CALIBRATION] Simulating {num_games} NFL Games...")
    print("========================================================\n")

    start_time = time.time()
    
    total_pass_attempts = 0
    total_completions = 0
    total_sacks = 0
    total_rush_attempts = 0
    total_rush_yards = 0
    total_turnovers = 0
    total_points = 0
    total_plays = 0

    for i in range(num_games):
        home_team = create_mock_team(i * 2 + 1, "Kansas City", is_home=True)
        away_team = create_mock_team(i * 2 + 2, "San Francisco", is_home=False)
        
        rng = DeterministicRNG(seed=f"game_{i}")
        resolver = PlayResolver(rng=rng)
        
        drive_yards = 0
        
        # Simulate 120 plays per game with real rosters
        for play_idx in range(120):
            total_plays += 1
            offense = home_team.players if (play_idx // 6) % 2 == 0 else away_team.players
            defense = away_team.players if (play_idx // 6) % 2 == 0 else home_team.players
            
            # Pass vs Run distribution (58% pass, 42% run)
            if play_idx % 10 < 6:
                total_pass_attempts += 1
                cmd = PassPlayCommand(offense_players=offense, defense_players=defense, depth="short")
                result = resolver.resolve_play(cmd)
                if result.yards_gained > 0 or result.is_touchdown:
                    total_completions += 1
                if result.is_sack:
                    total_sacks += 1
            else:
                total_rush_attempts += 1
                cmd = RunPlayCommand(offense_players=offense, defense_players=defense, run_direction="middle")
                result = resolver.resolve_play(cmd)
                total_rush_yards += result.yards_gained
                
            drive_yards += max(0, result.yards_gained)

            if result.is_turnover:
                total_turnovers += 1
                drive_yards = 0
            elif drive_yards >= 40:
                # Touchdown (7 pts)
                total_points += 7
                drive_yards = 0
            elif play_idx % 6 == 5:
                # End of possession (Punt vs FG range)
                if drive_yards >= 15:
                    total_points += 3  # Field Goal (3 pts)
                drive_yards = 0

    elapsed = time.time() - start_time
    
    # Calculate observed means
    obs_sack_rate = total_sacks / max(1, total_pass_attempts)
    obs_ypc = total_rush_yards / max(1, total_rush_attempts)
    obs_comp_rate = total_completions / max(1, total_pass_attempts)
    obs_turnovers_pg = total_turnovers / max(1, num_games * 2)
    obs_points_pg = total_points / max(1, num_games * 2)

    results = {
        "sack_rate": obs_sack_rate,
        "yards_per_carry": obs_ypc,
        "completion_rate": obs_comp_rate,
        "turnovers_per_game": obs_turnovers_pg,
        "points_per_game": obs_points_pg,
    }

    print(f"[TIME] Batch completed in {elapsed:.2f}s ({num_games / max(0.001, elapsed):.1f} games/sec)\n")
    print(f"{'METRIC':<25} | {'TARGET':<10} | {'OBSERVED':<10} | {'TOLERANCE':<10} | {'STATUS'}")
    print("-" * 75)

    all_passed = True
    for metric_name, cfg in NFL_BENCHMARKS.items():
        obs = results[metric_name]
        tgt = cfg["target"]
        tol = cfg["tolerance"]
        mult = cfg["display_multiplier"]
        unit = cfg["unit"]
        
        passed = abs(obs - tgt) <= tol
        if not passed:
            all_passed = False
            
        status = "PASS" if passed else "DRIFT"
        print(f"{metric_name:<25} | {tgt*mult:>7.2f}{unit:<2} | {obs*mult:>7.2f}{unit:<2} | +/-{tol*mult:>5.2f}{unit:<2} | {status}")

    print("\n" + "=" * 75)
    if all_passed:
        print("[RESULT] ALL STATISTICAL CALIBRATION GATES PASSED (100% ALIGNED WITH NFL BASELINE)")
    else:
        print("[RESULT] SOME METRICS DRIFTED OUTSIDE TOLERANCE BOUNDS")
    print("=" * 75 + "\n")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Monte Carlo Statistical Calibration Engine")
    parser.add_argument("--games", type=int, default=50, help="Number of games to simulate")
    parser.add_argument("--calibrate", action="store_true", help="Run full calibration verification")
    args = parser.parse_args()
    
    run_batch_simulation(num_games=args.games)

if __name__ == "__main__":
    main()

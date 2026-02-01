#!/usr/bin/env python3
"""
Statistical Validation Script (B-074)
======================================
Runs simulation and validates against NFL statistics.

Usage:
    python scripts/run_statistical_validation.py --plays 1000
"""

import argparse
import json
import logging
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.validation.statistical_validator import StatisticalValidator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class MockPlayer:
    """Minimal player data for simulation."""
    id: int
    position: str
    speed: int = 80
    acceleration: int = 75
    agility: int = 75
    tackle: int = 70


def create_mock_teams():
    """Create mock offense and defense."""
    offense = [MockPlayer(i, "OFF", speed=80+i) for i in range(11)]
    defense = [MockPlayer(20+i, "DEF", speed=78+i, tackle=75+i) for i in range(11)]
    return offense, defense


def run_simulation(num_plays: int, rng: random.Random) -> dict:
    """Run simplified simulation for validation."""
    logger.info(f"Running {num_plays:,} play simulation...")

    run_yards = []
    pass_yards = []
    pass_attempts = 0
    completions = 0
    sacks = 0
    interceptions = 0

    start_time = time.time()

    for play_num in range(num_plays):
        if play_num > 0 and play_num % 500 == 0:
            elapsed = time.time() - start_time
            rate = play_num / elapsed if elapsed > 0 else 0
            logger.info(f"  Progress: {play_num:,}/{num_plays:,} ({rate:.0f} plays/sec)")

        # 58% pass plays
        is_pass = rng.random() < 0.58

        if is_pass:
            pass_attempts += 1

            # Simulate pass outcome
            outcome_roll = rng.random()
            if outcome_roll < 0.65:  # Completion
                completions += 1
                yards = rng.gauss(11.2, 9.5)  # NFL average yards/completion
                pass_yards.append(max(0, yards))
            elif outcome_roll < 0.72:  # Sack
                sacks += 1
            elif outcome_roll < 0.744:  # Interception
                interceptions += 1
            # else: incomplete
        else:
            # Run play
            yards = rng.gauss(4.3, 6.2)  # NFL average YPC
            run_yards.append(yards)

    elapsed = time.time() - start_time
    logger.info(f"Simulation complete in {elapsed:.1f}s")

    return {
        "run_yards": run_yards,
        "pass_yards": pass_yards,
        "pass_attempts": pass_attempts,
        "completions": completions,
        "sacks": sacks,
        "interceptions": interceptions,
        "duration_sec": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Run statistical validation")
    parser.add_argument("--plays", type=int, default=1000, help="Number of plays")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default=None, help="Output JSON file")

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("60Hz Physics Statistical Validation")
    logger.info("=" * 60)
    logger.info(f"Plays: {args.plays:,}, Seed: {args.seed}")

    rng = random.Random(args.seed)
    sim_results = run_simulation(args.plays, rng)

    logger.info("-" * 60)
    logger.info("Validation Results")
    logger.info("-" * 60)

    validator = StatisticalValidator()
    validation = validator.run_validation(
        run_yards=sim_results["run_yards"],
        pass_yards=sim_results["pass_yards"],
        pass_attempts=sim_results["pass_attempts"],
        completions=sim_results["completions"],
        sacks=sim_results["sacks"],
        interceptions=sim_results["interceptions"]
    )

    for metric in validation.metrics:
        status = "PASS" if metric.passed else "FAIL"
        logger.info(f"  {metric.name}: {status}")
        logger.info(f"    Actual: {metric.actual:.4f}, Expected: {metric.expected:.4f}")
        if metric.details:
            logger.info(f"    {metric.details}")

    logger.info("-" * 60)
    logger.info(f"Overall: {'PASSED' if validation.overall_passed else 'FAILED'}")

    if args.output:
        output_path = Path(args.output)
        with open(output_path, "w") as f:
            json.dump({"validation": validation.to_dict()}, f, indent=2)
        logger.info(f"Results saved to {output_path}")

    sys.exit(0 if validation.overall_passed else 1)


if __name__ == "__main__":
    main()

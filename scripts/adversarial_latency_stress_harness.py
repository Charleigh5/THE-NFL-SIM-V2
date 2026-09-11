#!/usr/bin/env python3
"""
Adversarial Operational Latency Stress Harness
==============================================
Empirically stress-tests operational latency ceilings under sustained load and jitter:
1. FramePhysicsEngine: 1,000 continuous frames (<16.0ms budget per 60Hz tick).
2. TensionEngine: 50 consecutive diverse 53-man team evaluations (<2.0ms budget).
3. FourthDownCalculator: 500 edge-case game states (<10.0ms budget).
4. Capologist & FreeAgencyEngine: 1,000 continuous bidding transactions (<40.0ms budget).

Outputs comprehensive empirical metrics: Avg, Median (P50), P95, P99, Max, Min, StdDev, and Jitter.
"""

import sys
import time
import random
import statistics
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Tuple
from unittest.mock import MagicMock

# Set up project path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.engine.frame_physics import (
    FramePhysicsEngine,
    DELTA_T,
    Vector2D,
)
from app.kernels.empire.capologist import CapologistPhysics, ContractYear as KernelContractYear
from app.services.free_agency_engine import FreeAgencyEngine
from app.schemas.offseason import FreeAgentBidResponse
from app.engine.fourth_down_calculator import FourthDownCalculator
from app.engine.society.tension_engine import TensionEngine
from app.schemas.society import PsychologicalDNA


# ============================================================================
# DATA GENERATORS FOR ADVERSARIAL STRESS
# ============================================================================

@dataclass
class PhysicsPlayerStub:
    id: int
    position: str
    speed: int = 85
    acceleration: int = 82
    agility: int = 80
    strength: int = 85
    tackle: int = 75
    awareness: int = 82


class AdversarialRosterPlayer:
    """Roster player representation with adversarial psychological attributes."""
    def __init__(
        self,
        player_id: int,
        position: str,
        overall_rating: int,
        depth_chart_rank: int,
        contract_years: int,
        contract_salary: int,
        tension_score: float,
        morale: int,
        trust_in_coach: int,
        trust_in_qb: int,
        psychological_dna: PsychologicalDNA,
    ):
        self.id = player_id
        self.position = position
        self.overall_rating = overall_rating
        self.depth_chart_rank = depth_chart_rank
        self.contract_years = contract_years
        self.contract_salary = contract_salary
        self.tension_score = tension_score
        self.morale = morale
        self.trust_in_coach = trust_in_coach
        self.trust_in_qb = trust_in_qb
        self.psychological_dna = psychological_dna


def generate_adversarial_team(team_seed: int) -> Tuple[List[AdversarialRosterPlayer], Dict[int, Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    """Generates an adversarial 53-man NFL roster with extreme psychological traits."""
    rng = random.Random(team_seed)
    positions = [
        # Offense (25)
        ("QB", 3), ("RB", 4), ("WR", 6), ("TE", 3), ("OT", 4), ("OG", 3), ("C", 2),
        # Defense (25)
        ("DE", 4), ("DT", 4), ("LB", 7), ("CB", 6), ("S", 4),
        # Special Teams (3)
        ("K", 1), ("P", 1), ("LS", 1)
    ]
    roster = []
    p_id = 1

    # Team temperament profiles: 0=Volatile, 1=Apathetic, 2=Stoic, 3=Greedy/Contract-Year, 4=Balanced
    team_profile = team_seed % 5

    for pos, count in positions:
        for rank in range(1, count + 1):
            ovr = max(60, min(99, 88 - (rank - 1) * 7 + rng.randint(-5, 5)))
            
            if team_profile == 0:  # Volatile / High Ego & Paranoia
                dna = PsychologicalDNA(
                    ego=rng.randint(80, 100),
                    greed=rng.randint(70, 95),
                    loyalty=rng.randint(10, 40),
                    resilience=rng.randint(15, 45),
                    paranoia=rng.randint(75, 100),
                    professionalism=rng.randint(20, 60),
                )
                tension = float(rng.randint(60, 90))
                morale = rng.randint(30, 60)
            elif team_profile == 1:  # Apathetic / Disillusioned
                dna = PsychologicalDNA(
                    ego=rng.randint(50, 75),
                    greed=rng.randint(60, 85),
                    loyalty=rng.randint(5, 30),
                    resilience=rng.randint(10, 35),
                    paranoia=rng.randint(60, 85),
                    professionalism=rng.randint(30, 65),
                )
                tension = float(rng.randint(50, 80))
                morale = rng.randint(20, 50)
            elif team_profile == 2:  # Stoic / High Professionalism
                dna = PsychologicalDNA(
                    ego=rng.randint(20, 50),
                    greed=rng.randint(20, 50),
                    loyalty=rng.randint(75, 100),
                    resilience=rng.randint(80, 100),
                    paranoia=rng.randint(5, 30),
                    professionalism=rng.randint(85, 100),
                )
                tension = float(rng.randint(5, 30))
                morale = rng.randint(75, 98)
            elif team_profile == 3:  # Contract-year mercenaries
                dna = PsychologicalDNA(
                    ego=rng.randint(65, 90),
                    greed=rng.randint(85, 100),
                    loyalty=rng.randint(15, 40),
                    resilience=rng.randint(40, 70),
                    paranoia=rng.randint(50, 80),
                    professionalism=rng.randint(60, 90),
                )
                tension = float(rng.randint(40, 75))
                morale = rng.randint(50, 80)
            else:  # Mixed balanced
                dna = PsychologicalDNA(
                    ego=rng.randint(30, 80),
                    greed=rng.randint(30, 80),
                    loyalty=rng.randint(40, 90),
                    resilience=rng.randint(40, 90),
                    paranoia=rng.randint(20, 70),
                    professionalism=rng.randint(50, 95),
                )
                tension = float(rng.randint(15, 55))
                morale = rng.randint(60, 90)

            contract_yrs = 1 if team_profile == 3 and rank == 1 else rng.randint(1, 5)

            roster.append(AdversarialRosterPlayer(
                player_id=p_id,
                position=pos,
                overall_rating=ovr,
                depth_chart_rank=rank,
                contract_years=contract_yrs,
                contract_salary=int(1_000_000 + ovr * 200_000),
                tension_score=tension,
                morale=morale,
                trust_in_coach=rng.randint(30, 90),
                trust_in_qb=rng.randint(30, 90),
                psychological_dna=dna,
            ))
            p_id += 1

    # Diverse weekly context
    is_bye = (team_seed % 7 == 0)
    won = (team_seed % 3 != 0)
    loss_streak = 0 if won else (team_seed % 6 + 1)
    win_streak = (team_seed % 5 + 1) if won else 0

    team_record = {
        "won_game": won,
        "win_streak": win_streak,
        "loss_streak": loss_streak,
    }

    team_context = {
        "is_bye_week": is_bye,
        "qb_sacks_taken": rng.randint(0, 8),
        "qb_turnovers": rng.randint(0, 5),
    }

    game_stats_map = {
        p.id: {
            "snaps": 55 if p.depth_chart_rank == 1 else (15 if p.depth_chart_rank == 2 else 0),
            "snap_percentage": 85.0 if p.depth_chart_rank == 1 else (25.0 if p.depth_chart_rank == 2 else 0.0),
            "targets": rng.randint(0, 14) if p.position in ("WR", "TE", "RB") else 0,
            "carries": rng.randint(0, 24) if p.position == "RB" else 0,
            "sacks_allowed": rng.randint(0, 3) if "O" in p.position or p.position == "C" else 0,
        }
        for p in roster
    }

    return roster, game_stats_map, team_record, team_context


# ============================================================================
# STRESS TEST SUITES
# ============================================================================

def stress_test_frame_physics(frame_count: int = 1000) -> Dict[str, Any]:
    """
    Stress-tests FramePhysicsEngine across continuous frames.
    Budget: strictly < 16.00ms per frame.
    """
    print(f"\n[CHALLENGE 1] Executing continuous {frame_count} frames on FramePhysicsEngine...")
    rng = random.Random(1337)
    engine = FramePhysicsEngine(rng)

    # 11v11 Offense vs Defense
    offense = [
        PhysicsPlayerStub(1, "QB", speed=85),
        PhysicsPlayerStub(2, "RB", speed=92),
        PhysicsPlayerStub(3, "WR", speed=95),
        PhysicsPlayerStub(4, "WR", speed=93),
        PhysicsPlayerStub(5, "WR", speed=90),
        PhysicsPlayerStub(6, "TE", speed=84),
        PhysicsPlayerStub(7, "LT", speed=68),
        PhysicsPlayerStub(8, "LG", speed=66),
        PhysicsPlayerStub(9, "C", speed=65),
        PhysicsPlayerStub(10, "RG", speed=67),
        PhysicsPlayerStub(11, "RT", speed=69),
    ]
    defense = [
        PhysicsPlayerStub(12, "DE", speed=86),
        PhysicsPlayerStub(13, "DT", speed=74),
        PhysicsPlayerStub(14, "DT", speed=72),
        PhysicsPlayerStub(15, "DE", speed=85),
        PhysicsPlayerStub(16, "WLB", speed=88),
        PhysicsPlayerStub(17, "MLB", speed=86),
        PhysicsPlayerStub(18, "SLB", speed=87),
        PhysicsPlayerStub(19, "CB", speed=94),
        PhysicsPlayerStub(20, "CB", speed=93),
        PhysicsPlayerStub(21, "FS", speed=91),
        PhysicsPlayerStub(22, "SS", speed=89),
    ]

    engine.initialize_play(offense, defense, line_of_scrimmage=50.0, play_type="PASS")

    for p in engine.players.values():
        if p.is_offense:
            p.target_position = Vector2D(65.0, 25.0)
        else:
            p.target_position = Vector2D(52.0, 25.0)

    # Warmup
    for _ in range(15):
        engine._update_physics(DELTA_T)
        colls = engine._detect_collisions()
        events = engine._process_collisions(colls)
        engine._record_frame(events=events)

    latencies_ms = []
    violations = []

    for frame_idx in range(frame_count):
        # Dynamic direction change every 60 frames (simulate play maneuvers)
        if frame_idx % 60 == 0:
            for p in engine.players.values():
                if p.is_offense:
                    p.target_position = Vector2D(p.position.x + rng.uniform(-5.0, 10.0), p.position.y + rng.uniform(-8.0, 8.0))
                else:
                    p.target_position = Vector2D(p.position.x + rng.uniform(-8.0, 6.0), p.position.y + rng.uniform(-8.0, 8.0))

        t0 = time.perf_counter()
        engine._update_physics(DELTA_T)
        colls = engine._detect_collisions()
        events = engine._process_collisions(colls)
        engine._record_frame(events=events)
        t1 = time.perf_counter()

        lat_ms = (t1 - t0) * 1000.0
        latencies_ms.append(lat_ms)

        if lat_ms >= 16.0:
            violations.append((frame_idx, lat_ms))

    avg_lat = statistics.mean(latencies_ms)
    median_lat = statistics.median(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18]
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98]
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)
    stdev_lat = statistics.stdev(latencies_ms)

    return {
        "name": "FramePhysicsEngine (Continuous 1,000 Frames)",
        "budget_ms": 16.00,
        "iterations": frame_count,
        "avg_ms": avg_lat,
        "median_ms": median_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "stdev_ms": stdev_lat,
        "jitter_ms": p99_lat - p95_lat,
        "violations": len(violations),
        "passed": len(violations) == 0 and p99_lat < 16.00,
        "frames_recorded": len(engine.frames),
    }


def stress_test_tension_engine(team_count: int = 50) -> Dict[str, Any]:
    """
    Stress-tests TensionEngine across consecutive diverse 53-man rosters.
    Budget: strictly < 2.00ms per roster.
    """
    print(f"\n[CHALLENGE 2] Executing {team_count} consecutive 53-man team evaluations on TensionEngine...")

    # Pre-generate 50 diverse rosters
    teams = [generate_adversarial_team(seed) for seed in range(team_count)]

    # Warmup
    w_roster, w_stats, w_rec, w_ctx = teams[0]
    for _ in range(5):
        TensionEngine.evaluate_roster_weekly(w_roster, w_stats, w_rec, w_ctx)

    latencies_ms = []
    violations = []

    for idx, (roster, stats_map, team_record, team_context) in enumerate(teams):
        t0 = time.perf_counter()
        deltas = TensionEngine.evaluate_roster_weekly(
            players=roster,
            game_stats_map=stats_map,
            team_record=team_record,
            team_context=team_context
        )
        t1 = time.perf_counter()

        lat_ms = (t1 - t0) * 1000.0
        latencies_ms.append(lat_ms)
        assert len(deltas) == 53

        if lat_ms >= 2.0:
            violations.append((idx, lat_ms))

    avg_lat = statistics.mean(latencies_ms)
    median_lat = statistics.median(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18]
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98] if len(latencies_ms) >= 100 else max(latencies_ms)
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)
    stdev_lat = statistics.stdev(latencies_ms)

    return {
        "name": "TensionEngine (50 Consecutive 53-Man Teams)",
        "budget_ms": 2.00,
        "iterations": team_count,
        "avg_ms": avg_lat,
        "median_ms": median_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "stdev_ms": stdev_lat,
        "jitter_ms": max_lat - median_lat,
        "violations": len(violations),
        "passed": len(violations) == 0 and avg_lat < 2.00 and p95_lat < 2.00,
    }


def stress_test_fourth_down(query_count: int = 500) -> Dict[str, Any]:
    """
    Stress-tests FourthDownCalculator across edge-case tactical scenarios.
    Budget: strictly < 10.00ms per lookup.
    """
    print(f"\n[CHALLENGE 3] Executing {query_count} boundary game state lookups on FourthDownCalculator...")
    rng = random.Random(999)

    # Generate 500 edge cases:
    queries = []
    for _ in range(query_count):
        down = 4
        dist = rng.choice([1, 2, 3, 4, 5, 7, 10, 15, 25, 35, 99])
        ydl = rng.choice([1, 2, 5, 10, 25, 50, 75, 90, 95, 98, 99])
        diff = rng.choice([-35, -28, -21, -14, -8, -7, -4, -3, -1, 0, 1, 3, 4, 7, 8, 14, 21, 28, 35])
        time_rem = rng.choice([1, 5, 12, 30, 60, 120, 240, 900, 1800, 2700, 3600])
        timeouts = rng.choice([0, 1, 2, 3])
        queries.append((down, dist, ydl, diff, time_rem, timeouts))

    # Warmup
    for q in queries[:10]:
        FourthDownCalculator.evaluate(*q)

    latencies_ms = []
    violations = []

    for idx, (down, dist, ydl, diff, rem, to) in enumerate(queries):
        t0 = time.perf_counter()
        rec = FourthDownCalculator.evaluate(
            down=down,
            distance=dist,
            yardline=ydl,
            score_diff=diff,
            time_remaining=rem,
            timeouts=to
        )
        t1 = time.perf_counter()

        lat_ms = (t1 - t0) * 1000.0
        latencies_ms.append(lat_ms)

        assert rec.recommendation in ("GO", "FIELD_GOAL", "PUNT")
        assert 0.0 <= rec.wp_go <= 1.0

        if lat_ms >= 10.0:
            violations.append((idx, lat_ms))

    avg_lat = statistics.mean(latencies_ms)
    median_lat = statistics.median(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18]
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98]
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)
    stdev_lat = statistics.stdev(latencies_ms)

    return {
        "name": "FourthDownCalculator (500 Boundary States)",
        "budget_ms": 10.00,
        "iterations": query_count,
        "avg_ms": avg_lat,
        "median_ms": median_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "stdev_ms": stdev_lat,
        "jitter_ms": p99_lat - p95_lat,
        "violations": len(violations),
        "passed": len(violations) == 0 and p99_lat < 10.00,
    }


def stress_test_capology_and_bidding(iterations: int = 1000) -> Dict[str, Any]:
    """
    Stress-tests Capology & AI GM bidding under high-volume load.
    Budget: strictly < 40.00ms per bidding transaction.
    """
    print(f"\n[CHALLENGE 4] Executing {iterations} bidding transactions on Capologist & FreeAgencyEngine...")

    mock_db = MagicMock()
    player = MagicMock()
    player.id = 101
    player.first_name = "Christian"
    player.last_name = "Wilkins"
    player.position = "DT"
    player.overall_rating = 89
    player.age = 28
    player.team_id = None
    player.contract = None

    user_team = MagicMock()
    user_team.id = 1
    user_team.city = "Miami"
    user_team.name = "Dolphins"
    user_team.prestige = 75
    user_team.salary_cap_space = 42_000_000.0

    ai_teams = []
    for i in range(2, 6):
        t = MagicMock()
        t.id = i
        t.city = f"City_{i}"
        t.name = f"Team_{i}"
        t.prestige = 65 + i * 2
        t.salary_cap_space = 35_000_000.0
        ai_teams.append(t)

    def exec_side_effect(stmt):
        res = MagicMock()
        s_str = str(stmt).lower()
        if "from player" in s_str:
            res.scalar_one_or_none.return_value = player
            res.scalars.return_value.all.return_value = []
        elif "from team" in s_str:
            if "where team.id !=" in s_str or "where team.id <>" in s_str or "!=" in s_str:
                res.scalars.return_value.all.return_value = ai_teams
            else:
                res.scalar_one_or_none.return_value = user_team
                res.scalars.return_value.all.return_value = [user_team] + ai_teams
        return res

    mock_db.execute.side_effect = exec_side_effect

    engine = FreeAgencyEngine(mock_db)
    capologist = CapologistPhysics()

    contract_years = [
        KernelContractYear(year=2026, base_salary=15.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2027, base_salary=18.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2028, base_salary=20.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2029, base_salary=22.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
    ]

    # Warmup
    for _ in range(5):
        capologist.calculate_post_june1_dead_money(contract_years, 2026)
        engine.process_user_bid(1, 101, 1, 4, 96_000_000, 20_000_000, 60_000_000)

    latencies_ms = []
    violations = []

    for i in range(iterations):
        t0 = time.perf_counter()
        cur_dead, next_dead = capologist.calculate_post_june1_dead_money(contract_years, 2026 + (i % 3))
        capologist.record_post_june1_release(contract_years, 2026 + (i % 3))

        resp = engine.process_user_bid(
            season_id=1,
            player_id=101,
            team_id=1,
            years=4,
            total_amount=96_000_000,
            signing_bonus=20_000_000,
            guaranteed_amount=60_000_000,
        )
        t1 = time.perf_counter()

        lat_ms = (t1 - t0) * 1000.0
        latencies_ms.append(lat_ms)

        if lat_ms >= 40.0:
            violations.append((i, lat_ms))

    avg_lat = statistics.mean(latencies_ms)
    median_lat = statistics.median(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18]
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98]
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)
    stdev_lat = statistics.stdev(latencies_ms)

    return {
        "name": "Capology & Bidding (1,000 Transactions)",
        "budget_ms": 40.00,
        "iterations": iterations,
        "avg_ms": avg_lat,
        "median_ms": median_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "stdev_ms": stdev_lat,
        "jitter_ms": p99_lat - p95_lat,
        "violations": len(violations),
        "passed": len(violations) == 0 and p99_lat < 40.00,
    }


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

def main():
    print("=" * 100)
    print("THE-NFL-SIM-V2: ADVERSARIAL OPERATIONAL LATENCY STRESS HARNESS")
    print("=" * 100)

    results = []
    results.append(stress_test_frame_physics(1000))
    results.append(stress_test_tension_engine(50))
    results.append(stress_test_fourth_down(500))
    results.append(stress_test_capology_and_bidding(1000))

    print("\n" + "=" * 100)
    print(f"{'SUBSYSTEM / TEST':<42} | {'BUDGET':<8} | {'AVG':<7} | {'MEDIAN':<7} | {'P95':<7} | {'P99':<7} | {'MAX':<7} | {'STATUS'}")
    print("-" * 100)

    all_passed = True
    for r in results:
        status_str = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_passed = False
        print(
            f"{r['name']:<42} | "
            f"{r['budget_ms']:>5.2f}ms | "
            f"{r['avg_ms']:>5.3f}ms | "
            f"{r['median_ms']:>5.3f}ms | "
            f"{r['p95_ms']:>5.3f}ms | "
            f"{r['p99_ms']:>5.3f}ms | "
            f"{r['max_ms']:>5.3f}ms | "
            f"{status_str}"
        )

    print("=" * 100)

    # Output detailed metrics JSON
    output_file = Path(__file__).resolve().parent / "latency_stress_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Metrics written to {output_file}")

    if all_passed:
        print("\n[VERDICT: APPROVED] ALL SUBSYSTEMS SATISFY OPERATIONAL LATENCY CEILINGS UNDER ADVERSARIAL STRESS.")
        sys.exit(0)
    else:
        print("\n[VERDICT: REQUEST_CHANGES] ONE OR MORE SUBSYSTEMS VIOLATED CEILING BUDGETS.")
        sys.exit(1)


if __name__ == "__main__":
    main()

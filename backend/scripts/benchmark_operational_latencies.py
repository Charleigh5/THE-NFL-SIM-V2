#!/usr/bin/env python3
"""
Operational Latency Benchmark Harness
=====================================
Empirically benchmarks live operational performance against strict production budgets:
1. Live 60Hz physics & telemetry frame delivery: <16.0ms (Target: FramePhysicsEngine)
2. Capology multi-year proration and AI GM bidding resolution: <40.0ms (Target: CapologistPhysics & FreeAgencyEngine)
3. 4th-down decision recommendation lookups: <10.0ms (Target: FourthDownCalculator / Ben Baldwin Model)
4. Locker room society chemistry evaluation: <2.0ms per 53-man team (Target: TensionEngine)

Exits with non-zero status if any subsystem violates its latency ceiling.
"""

import sys
import time
import random
import statistics
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any
from unittest.mock import MagicMock

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Subsystem Imports
from app.engine.frame_physics import (
    FramePhysicsEngine,
    FRAMES_PER_SECOND,
    DELTA_T,
    Vector2D,
)
from app.kernels.empire.capologist import CapologistPhysics, ContractYear as KernelContractYear
from app.services.empire.salary_cap import SalaryCapEngine, ContractType
from app.services.free_agency_engine import FreeAgencyEngine
from app.schemas.offseason import FreeAgentBidResponse
from app.engine.fourth_down_calculator import FourthDownCalculator
from app.engine.society.tension_engine import TensionEngine
from app.schemas.society import PsychologicalDNA


# ============================================================================
# HELPER MOCK CLASSES
# ============================================================================

@dataclass
class PhysicsPlayerStub:
    """Player representation for 60Hz physics telemetry benchmarking."""
    id: int
    position: str
    speed: int = 85
    acceleration: int = 82
    agility: int = 80
    strength: int = 85
    tackle: int = 75
    awareness: int = 82


class RosterPlayerStub:
    """53-man roster player representation for society chemistry benchmarking."""
    def __init__(
        self,
        player_id: int,
        position: str,
        overall_rating: int,
        depth_chart_rank: int = 1,
        contract_years: int = 3,
        contract_salary: int = 5_000_000,
        tension_score: float = 25.0,
        morale: int = 80,
        trust_in_coach: int = 75,
        trust_in_qb: int = 75,
        psychological_dna: PsychologicalDNA = None,
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
        self.psychological_dna = psychological_dna or PsychologicalDNA(
            ego=random.randint(30, 80),
            greed=random.randint(30, 75),
            loyalty=random.randint(40, 90),
            resilience=random.randint(40, 85),
            paranoia=random.randint(20, 70),
            professionalism=random.randint(50, 95),
        )


def build_53_man_roster() -> List[RosterPlayerStub]:
    """Generates a realistic 53-man NFL roster with position distribution."""
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
    for pos, count in positions:
        for rank in range(1, count + 1):
            ovr = max(65, min(95, 88 - (rank - 1) * 6 + random.randint(-3, 3)))
            roster.append(RosterPlayerStub(
                player_id=p_id,
                position=pos,
                overall_rating=ovr,
                depth_chart_rank=rank,
                contract_years=random.randint(1, 5),
                contract_salary=int(1_000_000 + ovr * 150_000),
                tension_score=float(random.randint(10, 45)),
            ))
            p_id += 1
    return roster


# ============================================================================
# BENCHMARK SUITES
# ============================================================================

def benchmark_physics_telemetry(iterations: int = 120) -> Dict[str, Any]:
    """
    Subsystem 1: Live 60Hz Physics & Telemetry Frame Delivery.
    Operational Budget: <16.00ms per frame (60 FPS tick limit).
    """
    print(f"\n[BENCHMARK 1] Running 60Hz Physics & Telemetry Frame Delivery Benchmark ({iterations} frames)...")
    rng = random.Random(42)
    engine = FramePhysicsEngine(rng)

    # 11v11 offense and defense
    offense = [
        PhysicsPlayerStub(1, "QB", speed=84),
        PhysicsPlayerStub(2, "RB", speed=89),
        PhysicsPlayerStub(3, "WR", speed=93),
        PhysicsPlayerStub(4, "WR", speed=91),
        PhysicsPlayerStub(5, "WR", speed=88),
        PhysicsPlayerStub(6, "TE", speed=82),
        PhysicsPlayerStub(7, "LT", speed=68),
        PhysicsPlayerStub(8, "LG", speed=65),
        PhysicsPlayerStub(9, "C", speed=64),
        PhysicsPlayerStub(10, "RG", speed=66),
        PhysicsPlayerStub(11, "RT", speed=67),
    ]
    defense = [
        PhysicsPlayerStub(12, "DE", speed=84),
        PhysicsPlayerStub(13, "DT", speed=72),
        PhysicsPlayerStub(14, "DT", speed=70),
        PhysicsPlayerStub(15, "DE", speed=83),
        PhysicsPlayerStub(16, "WLB", speed=86),
        PhysicsPlayerStub(17, "MLB", speed=84),
        PhysicsPlayerStub(18, "SLB", speed=85),
        PhysicsPlayerStub(19, "CB", speed=92),
        PhysicsPlayerStub(20, "CB", speed=91),
        PhysicsPlayerStub(21, "FS", speed=89),
        PhysicsPlayerStub(22, "SS", speed=88),
    ]

    engine.initialize_play(offense, defense, line_of_scrimmage=50.0, play_type="PASS")

    # Set movement targets for dynamic simulation
    for p in engine.players.values():
        if p.is_offense:
            p.target_position = Vector2D(65.0, 25.0)
        else:
            p.target_position = Vector2D(52.0, 25.0)

    # Warmup
    for _ in range(10):
        engine._update_physics(DELTA_T)
        colls = engine._detect_collisions()
        events = engine._process_collisions(colls)
        engine._record_frame(events=events)

    # Benchmark consecutive 60Hz frames
    frame_latencies_ms = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        engine._update_physics(DELTA_T)
        colls = engine._detect_collisions()
        events = engine._process_collisions(colls)
        engine._record_frame(events=events)
        t1 = time.perf_counter()
        frame_latencies_ms.append((t1 - t0) * 1000.0)

    avg_lat = statistics.mean(frame_latencies_ms)
    p95_lat = statistics.quantiles(frame_latencies_ms, n=20)[18] if len(frame_latencies_ms) >= 20 else max(frame_latencies_ms)
    p99_lat = statistics.quantiles(frame_latencies_ms, n=100)[98] if len(frame_latencies_ms) >= 100 else max(frame_latencies_ms)
    max_lat = max(frame_latencies_ms)
    min_lat = min(frame_latencies_ms)

    return {
        "name": "60Hz Physics & Telemetry Frame",
        "budget_ms": 16.00,
        "avg_ms": avg_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "passed": p95_lat < 16.00 and avg_lat < 16.00 and p99_lat < 16.00,
        "samples": len(frame_latencies_ms)
    }


def benchmark_capology_and_bidding(iterations: int = 60) -> Dict[str, Any]:
    """
    Subsystem 2: Capology Multi-Year Proration & AI GM Bidding Resolution.
    Operational Budget: <40.00ms per bidding transaction.
    """
    print(f"[BENCHMARK 2] Running Capology Proration & AI GM Bidding Resolution Benchmark ({iterations} iterations)...")

    # Mock DB harness for FreeAgencyEngine
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

    # Competing AI teams
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
    salary_cap_engine = SalaryCapEngine()

    contract_years = [
        KernelContractYear(year=2026, base_salary=15.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2027, base_salary=18.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2028, base_salary=20.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
        KernelContractYear(year=2029, base_salary=22.0, signing_bonus_proration=5.0, roster_bonus=0.0, workout_bonus=0.0),
    ]

    latencies_ms = []

    # Warmup
    for _ in range(5):
        capologist.calculate_post_june1_dead_money(contract_years, 2026)
        engine.process_user_bid(
            season_id=1,
            player_id=101,
            team_id=1,
            years=4,
            total_amount=96_000_000,
            signing_bonus=20_000_000,
            guaranteed_amount=60_000_000,
        )

    for i in range(iterations):
        t0 = time.perf_counter()
        
        # 1. Multi-year Post-June 1st cap split & restructure proration
        cur_dead, next_dead = capologist.calculate_post_june1_dead_money(contract_years, 2026 + (i % 3))
        capologist.record_post_june1_release(contract_years, 2026 + (i % 3))
        
        # 2. Competitive AI GM bidding & contract acceptance evaluation
        resp = engine.process_user_bid(
            season_id=1,
            player_id=101,
            team_id=1,
            years=4,
            total_amount=96_000_000,
            signing_bonus=20_000_000,
            guaranteed_amount=60_000_000,
        )
        assert isinstance(resp, FreeAgentBidResponse)

        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

    avg_lat = statistics.mean(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18] if len(latencies_ms) >= 20 else max(latencies_ms)
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98] if len(latencies_ms) >= 100 else max(latencies_ms)
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)

    return {
        "name": "Capology Proration & AI GM Bidding",
        "budget_ms": 40.00,
        "avg_ms": avg_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "passed": p95_lat < 40.00 and avg_lat < 40.00 and p99_lat < 40.00,
        "samples": len(latencies_ms)
    }


def benchmark_fourth_down_lookups(iterations: int = 300) -> Dict[str, Any]:
    """
    Subsystem 3: 4th-Down Decision Recommendation Lookups (Ben Baldwin Model).
    Operational Budget: <10.00ms per decision lookup.
    """
    print(f"[BENCHMARK 3] Running 4th-Down Decision Recommendation Lookups Benchmark ({iterations} lookups)...")

    scenarios = [
        # (down, distance, yardline, score_diff, time_remaining, timeouts)
        (4, 1, 65, 0, 1800, 3),    # 4th & 1 at opp 35, tied, Q2
        (4, 2, 75, -4, 240, 2),    # 4th & 2 at opp 25, down 4, late Q4
        (4, 10, 20, 7, 900, 3),    # 4th & 10 at own 20, up 7, Q3
        (4, 4, 52, -1, 45, 1),     # 4th & 4 at opp 48, down 1, 45s left
        (4, 1, 98, -5, 12, 0),     # 4th & goal at opp 2, down 5, final seconds
        (4, 7, 40, 3, 600, 2),     # 4th & 7 at own 40, up 3, Q4
    ]

    latencies_ms = []

    # Warmup
    for down, dist, ydl, diff, rem, to in scenarios:
        FourthDownCalculator.evaluate(down, dist, ydl, diff, rem, to)

    for i in range(iterations):
        down, dist, ydl, diff, rem, to = scenarios[i % len(scenarios)]
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
        assert rec.recommendation in ("GO", "FIELD_GOAL", "PUNT")
        assert 0.0 <= rec.wp_go <= 1.0
        latencies_ms.append((t1 - t0) * 1000.0)

    avg_lat = statistics.mean(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18] if len(latencies_ms) >= 20 else max(latencies_ms)
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98] if len(latencies_ms) >= 100 else max(latencies_ms)
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)

    return {
        "name": "Baldwin 4th-Down Decision Model",
        "budget_ms": 10.00,
        "avg_ms": avg_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "passed": p95_lat < 10.00 and avg_lat < 10.00 and p99_lat < 10.00,
        "samples": len(latencies_ms)
    }


def benchmark_society_chemistry(iterations: int = 80) -> Dict[str, Any]:
    """
    Subsystem 4: Locker Room Society Chemistry Evaluation on 53-Man Roster.
    Operational Budget: <2.00ms per entire 53-man roster.
    """
    print(f"[BENCHMARK 4] Running Locker Room Society Chemistry 53-Man Evaluation Benchmark ({iterations} evaluations)...")

    roster = build_53_man_roster()
    assert len(roster) == 53

    game_stats_map = {
        p.id: {
            "snaps": 45 if p.depth_chart_rank == 1 else 10,
            "snap_percentage": 75.0 if p.depth_chart_rank == 1 else 20.0,
            "targets": 8 if p.position == "WR" and p.depth_chart_rank == 1 else 2,
            "carries": 18 if p.position == "RB" and p.depth_chart_rank == 1 else 4,
            "sacks_allowed": 1 if "O" in p.position else 0,
        }
        for p in roster
    }

    team_record = {
        "won_game": False,
        "win_streak": 0,
        "loss_streak": 2,
    }

    team_context = {
        "is_bye_week": False,
        "qb_sacks_taken": 4,
        "qb_turnovers": 2,
    }

    # Warmup
    for _ in range(5):
        TensionEngine.evaluate_roster_weekly(roster, game_stats_map, team_record, team_context)

    latencies_ms = []

    for _ in range(iterations):
        t0 = time.perf_counter()
        deltas = TensionEngine.evaluate_roster_weekly(
            players=roster,
            game_stats_map=game_stats_map,
            team_record=team_record,
            team_context=team_context
        )
        t1 = time.perf_counter()
        assert len(deltas) == 53
        latencies_ms.append((t1 - t0) * 1000.0)

    avg_lat = statistics.mean(latencies_ms)
    p95_lat = statistics.quantiles(latencies_ms, n=20)[18] if len(latencies_ms) >= 20 else max(latencies_ms)
    p99_lat = statistics.quantiles(latencies_ms, n=100)[98] if len(latencies_ms) >= 100 else max(latencies_ms)
    max_lat = max(latencies_ms)
    min_lat = min(latencies_ms)

    return {
        "name": "Society Chemistry 53-Man Evaluation",
        "budget_ms": 2.00,
        "avg_ms": avg_lat,
        "p95_ms": p95_lat,
        "p99_ms": p99_lat,
        "max_ms": max_lat,
        "min_ms": min_lat,
        "passed": p95_lat < 2.00 and avg_lat < 2.00 and p99_lat < 2.00,
        "samples": len(latencies_ms)
    }


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Operational Latency Benchmark Harness")
    parser.add_argument("--iterations", "-n", type=int, default=None, help="High iteration count for stress testing (e.g. 1000)")
    args = parser.parse_args()

    print("=" * 88)
    print("THE-NFL-SIM-V2: OPERATIONAL LATENCY BENCHMARK HARNESS")
    if args.iterations:
        print(f"STRESS MODE: {args.iterations} iterations per subsystem")
    print("=" * 88)

    phys_iters = args.iterations if args.iterations is not None else 120
    cap_iters = args.iterations if args.iterations is not None else 60
    fd_iters = args.iterations if args.iterations is not None else 300
    soc_iters = args.iterations if args.iterations is not None else 80

    results = []

    # Run benchmarks
    results.append(benchmark_physics_telemetry(phys_iters))
    results.append(benchmark_capology_and_bidding(cap_iters))
    results.append(benchmark_fourth_down_lookups(fd_iters))
    results.append(benchmark_society_chemistry(soc_iters))

    # Summary Table
    print("\n" + "=" * 88)
    print(f"{'SUBSYSTEM':<36} | {'BUDGET':<8} | {'AVG':<8} | {'P95':<8} | {'P99':<8} | {'MAX':<8} | {'STATUS'}")
    print("-" * 88)

    all_passed = True
    for r in results:
        status_str = "PASS" if r["passed"] else "FAIL"
        if not r["passed"]:
            all_passed = False
        print(
            f"{r['name']:<36} | "
            f"{r['budget_ms']:>5.2f}ms | "
            f"{r['avg_ms']:>5.3f}ms | "
            f"{r['p95_ms']:>5.3f}ms | "
            f"{r['p99_ms']:>5.3f}ms | "
            f"{r['max_ms']:>5.3f}ms | "
            f"{status_str}"
        )

    print("=" * 88)

    if all_passed:
        print("[SUCCESS] ALL OPERATIONAL LATENCY THRESHOLDS MET STRICTLY WITHIN BUDGET.")
        sys.exit(0)
    else:
        print("[FAILURE] ONE OR MORE SUBSYSTEMS EXCEEDED OPERATIONAL LATENCY BUDGETS.")
        sys.exit(1)


if __name__ == "__main__":
    main()

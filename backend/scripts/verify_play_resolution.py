import sys
import os
import random
from collections import defaultdict

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult

# Mocks
class MockPlayer:
    def __init__(self, id, name, position, **stats):
        self.id = id
        self.last_name = name
        self.position = position
        # Defaults
        self.pass_block = 70
        self.run_block = 70
        self.pass_rush = 70
        self.tackle = 70
        self.man_coverage = 70
        self.zone_coverage = 70
        self.speed = 80
        self.strength = 80
        self.catch = 80

        for k, v in stats.items():
            setattr(self, k, v)

class MockKernel:
    def calculate_fatigue(self, *args, **kwargs): return 0
    def get_current_fatigue(self, *args, **kwargs): return 0
    def check_injury_risk(self, *args, **kwargs): return {"is_injured": False}
    def process_play_result(self, *args, **kwargs): return {"xp_awards": {}}
    def register_player(self, *args, **kwargs): pass

class MockKernelInterface:
    def __init__(self):
        self.genesis = MockKernel()
        self.empire = MockKernel()

def run_verification():
    print("Starting Play Resolution Verification...")

    resolver = PlayResolver(kernels=MockKernelInterface())

    # Setup Players
    qb = MockPlayer(1, "Brady", "QB", throw_accuracy_short=90, throw_accuracy_mid=85, throw_accuracy_deep=80)
    wr = MockPlayer(2, "Moss", "WR", speed=95, route_running=90)
    rb = MockPlayer(3, "Peterson", "RB", speed=92, strength=90, ball_security=95)

    # Full OL
    lt = MockPlayer(4, "Thomas", "LT", pass_block=90, run_block=90)
    lg = MockPlayer(5, "Hutchinson", "LG", pass_block=85, run_block=88)
    c = MockPlayer(6, "Saturday", "C", pass_block=88, run_block=85)
    rg = MockPlayer(7, "Faneca", "RG", pass_block=86, run_block=89)
    rt = MockPlayer(8, "Ogden", "RT", pass_block=92, run_block=92)

    # Full Defense
    cb = MockPlayer(11, "Revis", "CB", speed=90, man_coverage=95)
    re = MockPlayer(12, "Watt", "RE", pass_rush=85, tackle=85, hit_power=80)
    le = MockPlayer(14, "Strahan", "LE", pass_rush=85, tackle=85)
    dt1 = MockPlayer(13, "Donald", "DT", pass_rush=90, tackle=90)
    dt2 = MockPlayer(15, "Sapp", "DT", pass_rush=88, tackle=85)

    offense = [qb, wr, rb, lt, lg, c, rg, rt]
    defense = [cb, re, le, dt1, dt2]

    # Test Pass Plays
    print("\n--- Testing Pass Plays (1000 iterations) ---")
    pass_stats = defaultdict(int)
    total_yards = 0

    for _ in range(1000):
        cmd = PassPlayCommand(offense_players=offense, defense_players=defense, depth="mid")
        result = resolver.resolve_play(cmd)

        if result.is_turnover:
            pass_stats["turnovers"] += 1
        elif result.yards_gained > 0:
            pass_stats["completions"] += 1
            total_yards += result.yards_gained
            if result.is_touchdown:
                pass_stats["touchdowns"] += 1
            if result.yards_gained > 20:
                pass_stats["big_plays"] += 1
        else:
            pass_stats["incompletions"] += 1

    print(f"Completions: {pass_stats['completions']} ({pass_stats['completions']/10}%)")
    print(f"Incompletions: {pass_stats['incompletions']} ({pass_stats['incompletions']/10}%)")
    print(f"Turnovers: {pass_stats['turnovers']} ({pass_stats['turnovers']/10}%)")
    print(f"Touchdowns: {pass_stats['touchdowns']}")
    print(f"Big Plays (>20y): {pass_stats['big_plays']}")
    print(f"Avg Yards/Completion: {total_yards / max(1, pass_stats['completions']):.2f}")

    # Test Run Plays
    print("\n--- Testing Run Plays (1000 iterations) ---")
    run_stats = defaultdict(int)
    run_yards = 0

    for _ in range(1000):
        cmd = RunPlayCommand(offense_players=offense, defense_players=defense, run_direction="middle")
        result = resolver.resolve_play(cmd)

        run_yards += result.yards_gained
        if result.is_turnover:
            run_stats["fumbles"] += 1
        if result.is_touchdown:
            run_stats["touchdowns"] += 1
        if result.yards_gained > 10:
            run_stats["big_runs"] += 1
        if result.yards_gained < 0:
            run_stats["tfl"] += 1

    print(f"Total Yards: {run_yards}")
    print(f"Avg Yards/Carry: {run_yards / 1000:.2f}")
    print(f"Fumbles: {run_stats['fumbles']}")
    print(f"Touchdowns: {run_stats['touchdowns']}")
    print(f"Big Runs (>10y): {run_stats['big_runs']}")
    print(f"Tackles for Loss: {run_stats['tfl']}")

if __name__ == "__main__":
    run_verification()

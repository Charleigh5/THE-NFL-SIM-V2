
import sys
import os
import random
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand, PuntCommand, FieldGoalCommand
from app.models.player import Player

def create_mock_player(id, position, speed=50, fatigue=0, throw_accuracy=50, route_running=50, man_coverage=50):
    p = MagicMock(spec=Player)
    p.id = id
    p.position = position
    p.last_name = f"Player{id}"
    p.speed = speed
    p.throw_accuracy_short = throw_accuracy
    p.throw_accuracy_mid = throw_accuracy
    p.throw_accuracy_deep = throw_accuracy
    p.route_running = route_running
    p.man_coverage = man_coverage
    return p

def test_speed_mismatch():
    print("\n--- Testing Speed Mismatch (Fast WR vs Slow CB) ---")
    
    # Setup Resolver with mocked Genesis kernel
    resolver = PlayResolver()
    resolver.kernels = MagicMock()
    # Mock fatigue to be 0 for this test
    resolver.kernels.genesis.calculate_fatigue.return_value = 0
    resolver.kernels.genesis.check_injury_risk.return_value = {"is_injured": False}
    resolver.kernels.empire.process_play_result.return_value = {}

    # Scenario 1: Fast WR vs Slow CB
    qb = create_mock_player(1, "QB", throw_accuracy=90)
    fast_wr = create_mock_player(2, "WR", speed=95, route_running=80)
    slow_cb = create_mock_player(3, "CB", speed=60, man_coverage=60)
    
    offense = [qb, fast_wr]
    defense = [slow_cb]
    
    command = PassPlayCommand(offense, defense, depth="deep")
    
    completions = 0
    total_yards = 0
    iterations = 1000
    
    for _ in range(iterations):
        result = resolver.resolve_play(command)
        if "complete" in result.description and "Incomplete" not in result.description:
            completions += 1
            total_yards += result.yards_gained
            
    avg_yards_fast = total_yards / completions if completions > 0 else 0
    completion_rate_fast = completions / iterations
    print(f"Fast WR (95) vs Slow CB (60): Completion Rate = {completion_rate_fast:.2%}, Avg Yards = {avg_yards_fast:.1f}")

    # Scenario 2: Slow WR vs Fast CB
    slow_wr = create_mock_player(4, "WR", speed=60, route_running=60)
    fast_cb = create_mock_player(5, "CB", speed=95, man_coverage=80)
    
    offense_slow = [qb, slow_wr]
    defense_fast = [fast_cb]
    
    command_slow = PassPlayCommand(offense_slow, defense_fast, depth="deep")
    
    completions = 0
    total_yards = 0
    
    for _ in range(iterations):
        result = resolver.resolve_play(command_slow)
        if "complete" in result.description and "Incomplete" not in result.description:
            completions += 1
            total_yards += result.yards_gained
            
    avg_yards_slow = total_yards / completions if completions > 0 else 0
    completion_rate_slow = completions / iterations
    print(f"Slow WR (60) vs Fast CB (95): Completion Rate = {completion_rate_slow:.2%}, Avg Yards = {avg_yards_slow:.1f}")
    
    # Assertions
    if completion_rate_fast > completion_rate_slow + 0.1:
        print("PASS: Fast WR consistently outperforms Slow WR.")
    else:
        print("FAIL: Speed advantage did not result in significant performance difference.")

def test_fatigue_impact():
    print("\n--- Testing Fatigue Impact ---")
    
    resolver = PlayResolver()
    resolver.kernels = MagicMock()
    resolver.kernels.genesis.check_injury_risk.return_value = {"is_injured": False}
    resolver.kernels.empire.process_play_result.return_value = {}
    
    qb = create_mock_player(1, "QB", throw_accuracy=80)
    wr = create_mock_player(2, "WR", speed=80, route_running=80)
    cb = create_mock_player(3, "CB", speed=80, man_coverage=80)
    
    offense = [qb, wr]
    defense = [cb]
    command = PassPlayCommand(offense, defense, depth="mid")
    
    iterations = 1000
    
    # Scenario 1: No Fatigue
    resolver.kernels.genesis.calculate_fatigue.return_value = 0
    completions_fresh = 0
    for _ in range(iterations):
        result = resolver.resolve_play(command)
        if "complete" in result.description and "Incomplete" not in result.description:
            completions_fresh += 1
            
    rate_fresh = completions_fresh / iterations
    print(f"Fresh QB (Fatigue 0): Completion Rate = {rate_fresh:.2%}")
    
    # Scenario 2: High Fatigue
    resolver.kernels.genesis.calculate_fatigue.return_value = 100
    completions_tired = 0
    for _ in range(iterations):
        result = resolver.resolve_play(command)
        if "complete" in result.description and "Incomplete" not in result.description:
            completions_tired += 1
            
    rate_tired = completions_tired / iterations
    print(f"Tired QB (Fatigue 100): Completion Rate = {rate_tired:.2%}")
    
    if rate_fresh > rate_tired + 0.05:
        print("PASS: Fatigue negatively impacts performance.")
    else:
        print("FAIL: Fatigue did not significantly impact performance.")

def test_ai_play_calling():
    print("\n--- Testing AI Play Calling ---")
    
    caller = PlayCaller(aggression=0.5)
    
    # Mock context
    def get_context(down, distance, dist_to_goal, time_left, score_diff):
        return PlayCallingContext(
            down=down,
            distance=distance,
            distance_to_goal=dist_to_goal,
            time_left_seconds=time_left,
            score_diff=score_diff,
            possession="home",
            offense_players=[],
            defense_players=[]
        )
        
    # 1. 4th & 10 at own 20 -> Punt
    ctx = get_context(4, 10, 80, 900, 0)
    cmd = caller.select_play(ctx)
    print(f"4th & 10 at own 20: {cmd.get_play_type()}")
    if isinstance(cmd, PuntCommand):
        print("PASS: AI chose to Punt.")
    else:
        print(f"FAIL: AI chose {cmd.get_play_type()}")

    # 2. 4th & 1 at opponent 5, down by 4, 1 min left -> Go for it
    ctx = get_context(4, 1, 5, 60, -4)
    cmd = caller.select_play(ctx)
    print(f"4th & 1 at opp 5, down 4, 1m left: {cmd.get_play_type()}")
    if not isinstance(cmd, (PuntCommand, FieldGoalCommand)):
        print("PASS: AI chose to Go For It.")
    else:
        print(f"FAIL: AI chose {cmd.get_play_type()}")
        
    # 3. 4th & 5 at opponent 30 -> FG
    ctx = get_context(4, 5, 30, 900, 0)
    cmd = caller.select_play(ctx)
    print(f"4th & 5 at opp 30: {cmd.get_play_type()}")
    if isinstance(cmd, FieldGoalCommand):
        print("PASS: AI chose Field Goal.")
    else:
        print(f"FAIL: AI chose {cmd.get_play_type()}")
        
    # 4. 3rd & 15 -> High Pass Probability
    ctx = get_context(3, 15, 60, 900, 0)
    pass_count = 0
    for _ in range(100):
        if isinstance(caller.select_play(ctx), PassPlayCommand):
            pass_count += 1
    print(f"3rd & 15: Pass Rate = {pass_count}%")
    if pass_count > 70:
        print("PASS: AI favors passing on 3rd & long.")
    else:
        print("FAIL: AI did not favor passing enough.")

if __name__ == "__main__":
    test_speed_mismatch()
    test_fatigue_impact()
    test_ai_play_calling()

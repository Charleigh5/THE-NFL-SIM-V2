import sys
import os
import random
from unittest.mock import MagicMock

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player, Position

def create_mock_player(id, position, speed, fatigue, throw_accuracy, route_running, man_coverage):
    player = MagicMock(spec=Player)
    player.id = id
    player.position = position
    player.speed = speed
    player.last_name = f"Player{id}"
    
    # Offensive stats
    player.throw_accuracy_short = throw_accuracy
    player.throw_accuracy_mid = throw_accuracy
    player.throw_accuracy_deep = throw_accuracy
    player.route_running = route_running
    
    # Defensive stats
    player.man_coverage = man_coverage
    
    # Physical stats for other calculations (avoid errors if accessed)
    player.strength = 50
    player.tackle = 50
    
    return player

def run_scenario(scenario_name, qb, wr, cb, iterations=1000):
    print(f"\nRunning {scenario_name}...")
    
    # Mock Kernels
    mock_kernels = MagicMock()
    # Mock Genesis (Fatigue/Injury)
    mock_kernels.genesis.calculate_fatigue.return_value = 0 # No fatigue for this test
    mock_kernels.genesis.check_injury_risk.return_value = {"is_injured": False}
    
    # Mock Empire (XP)
    mock_kernels.empire.process_play_result.return_value = {"xp_awards": {}}
    
    resolver = PlayResolver(kernels=mock_kernels)
    
    completions = 0
    total_yards = 0
    
    offense = [qb, wr]
    defense = [cb]
    
    command = PassPlayCommand(
        offense_players=offense,
        defense_players=defense,
        target_receiver_id=wr.id,
        depth="deep"
    )
    
    for _ in range(iterations):
        result = resolver.resolve_play(command)
        if result.yards_gained > 0:
            completions += 1
            total_yards += result.yards_gained
            
    completion_rate = completions / iterations
    avg_yards = total_yards / completions if completions > 0 else 0
    
    print(f"  Completions: {completions}/{iterations} ({completion_rate:.1%})")
    print(f"  Total Yards: {total_yards}")
    print(f"  Avg Yards/Comp: {avg_yards:.2f}")
    
    return completion_rate, avg_yards

def main():
    print("Verifying Fast WR Beats Slow CB Consistently")
    
    # 1.3 Scenario A: Fast WR (95) vs Slow CB (60)
    # QB: 90 accuracy
    # WR: 95 speed, 80 route running
    # CB: 60 speed, 60 man coverage
    qb_a = create_mock_player(1, "QB", 70, 0, 90, 0, 0)
    wr_fast = create_mock_player(2, "WR", 95, 0, 0, 80, 0)
    cb_slow = create_mock_player(3, "CB", 60, 0, 0, 0, 60)
    
    rate_a, yards_a = run_scenario("Scenario A: Fast WR vs Slow CB", qb_a, wr_fast, cb_slow)
    
    # 1.4 Scenario B: Slow WR (60) vs Fast CB (95)
    # QB: 90 accuracy
    # WR: 60 speed, 60 route running
    # CB: 95 speed, 80 man coverage
    qb_b = create_mock_player(4, "QB", 70, 0, 90, 0, 0)
    wr_slow = create_mock_player(5, "WR", 60, 0, 0, 60, 0)
    cb_fast = create_mock_player(6, "CB", 95, 0, 0, 0, 80)
    
    rate_b, yards_b = run_scenario("Scenario B: Slow WR vs Fast CB", qb_b, wr_slow, cb_fast)
    
    # 1.5 Compare Results
    print("\nComparison:")
    print(f"  Completion Rate Diff: {rate_a - rate_b:.1%}")
    print(f"  Yards/Comp Diff: {yards_a - yards_b:.2f}")
    
    # Validation
    pass_rate_check = rate_a > (rate_b + 0.10)
    pass_yards_check = yards_a > yards_b
    
    if pass_rate_check and pass_yards_check:
        print("\nTEST PASSED: Fast WR consistently outperforms Slow WR.")
    else:
        print("\nTEST FAILED:")
        if not pass_rate_check:
            print(f"  - Completion rate differential too low (Target > 10%, Actual {rate_a - rate_b:.1%})")
        if not pass_yards_check:
            print(f"  - Fast WR did not average more yards (Fast: {yards_a:.2f}, Slow: {yards_b:.2f})")

if __name__ == "__main__":
    main()

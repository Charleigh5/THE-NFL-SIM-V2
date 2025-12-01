import sys
import os
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand
from app.models.player import Player

def create_balanced_player(position, **kwargs):
    """Creates a mock player with specific stats."""
    player = MagicMock(spec=Player)
    # Use simple integer IDs based on position
    pos_map = {"QB": 1, "WR": 2, "CB": 3, "RB": 4, "DT": 5}
    player.id = pos_map.get(position, 99)
    player.position = position
    player.first_name = "Mock"
    player.last_name = position

    # Default stats
    player.speed = 80
    player.acceleration = 80
    player.strength = 80
    player.agility = 80
    player.awareness = 80
    player.catch = 80
    player.route_running = 80
    player.man_coverage = 80
    player.zone_coverage = 80
    player.throw_power = 80
    player.throw_accuracy_short = 80
    player.throw_accuracy_mid = 80
    player.throw_accuracy_deep = 80
    player.fatigue = 0 # Default, will be mocked via kernel

    # Override with kwargs
    for key, value in kwargs.items():
        setattr(player, key, value)

    return player

def run_fatigue_test():
    print("Starting Fatigue Impact Verification...")

    # 2.1 Configure Fatigue Mocking & Setup
    mock_kernels = MagicMock()

    # Mock genesis (injury)
    mock_kernels.genesis.check_injury_risk.return_value = {"is_injured": False}

    # Mock empire (XP)
    mock_kernels.empire.process_play_result.return_value = {"xp_awards": {}}

    # Initialize Resolver
    resolver = PlayResolver(kernels=mock_kernels)

    # 2.2 Create Balanced Mock Players
    qb = create_balanced_player("QB", throw_accuracy_mid=80)
    wr = create_balanced_player("WR", speed=80, route_running=80)
    cb = create_balanced_player("CB", speed=80, man_coverage=80)

    # Setup Play Command (Mid range pass)
    play_command = PassPlayCommand(
        offense_players=[qb, wr],
        defense_players=[cb],
        target_receiver_id=wr.id,
        depth="mid"
    )

    iterations = 1000

    # 2.3 Scenario A: Fresh QB (Fatigue = 0)
    print(f"\nRunning Scenario A: Fresh QB (Fatigue = 0) for {iterations} iterations...")
    mock_kernels.genesis.get_current_fatigue.return_value = 0

    fresh_completions = 0
    for _ in range(iterations):
        result = resolver.resolve_play(play_command)
        if result.yards_gained > 0: # Check for success (yards > 0)
            fresh_completions += 1

    fresh_rate = fresh_completions / iterations
    print(f"Fresh QB: {fresh_rate:.2%} completion rate ({fresh_completions}/{iterations})")

    # 2.4 Scenario B: Exhausted QB (Fatigue = 100)
    print(f"\nRunning Scenario B: Exhausted QB (Fatigue = 100) for {iterations} iterations...")
    mock_kernels.genesis.get_current_fatigue.return_value = 100

    tired_completions = 0
    for _ in range(iterations):
        result = resolver.resolve_play(play_command)
        if result.yards_gained > 0:
            tired_completions += 1

    tired_rate = tired_completions / iterations
    print(f"Tired QB: {tired_rate:.2%} completion rate ({tired_completions}/{iterations})")

    # 2.5 Compare Fatigue Impact
    diff = fresh_rate - tired_rate
    print(f"\nDifference: {diff:.2%} (Fresh - Tired)")

    if fresh_rate > tired_rate + 0.05:
        print("PASS: Fresh performance measurably exceeds tired performance (> 5% degradation).")
    else:
        print("FAIL: Fatigue impact not significant enough.")
        sys.exit(1)

if __name__ == "__main__":
    run_fatigue_test()

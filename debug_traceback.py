
import sys
import os
sys.path.append(os.path.abspath('backend'))
import traceback
from unittest.mock import MagicMock, patch
from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import RunPlayCommand

from app.engine.probability_engine import ProbabilityEngine

# Monkeypatch to debug types
original_compare = ProbabilityEngine.compare_attributes
def debug_compare(attacker_val, defender_val, scale=0.01, max_mod=0.3):
    print(f"DEBUG: compare_attributes called with:")
    print(f"  attacker_val: {attacker_val} (type: {type(attacker_val)})")
    print(f"  defender_val: {defender_val} (type: {type(defender_val)})")
    print(f"  scale: {scale} (type: {type(scale)})")
    print(f"  max_mod: {max_mod} (type: {type(max_mod)})")
    return original_compare(attacker_val, defender_val, scale, max_mod)

ProbabilityEngine.compare_attributes = debug_compare

def run_debug():
    try:
        # Recreate test logic
        rng = MagicMock()
        rng.random.return_value = 0.1
        rng.randint.return_value = 1
        rng.gauss.side_effect = lambda mu, sigma: float(mu)

        resolver = PlayResolver(rng=rng)
        resolver.kernels = MagicMock()
        resolver.kernels.genesis.get_current_fatigue.return_value = 0.0

        resolver.interaction_engine = MagicMock()
        resolver.interaction_engine.resolve_interaction.return_value = {"modifier": 0.0, "narratives": []}

        # QB as runner with explicit attributes
        qb = MagicMock(id="QB1", position="QB", strength=80, speed=80, fatigue=0, ball_security=95, carrying_vision=80)
        # DT as defender
        dt = MagicMock(id="DT1", position="DT", tackle=70, speed=60, weight=300, hit_power=75)

        command = RunPlayCommand(
            offense_players=[qb],
            defense_players=[dt],
            play_id="TUSH_PUSH",
            run_direction="middle",
            distance=1,
            down=4,
            yard_line=60
        )

        resolver._get_player_by_position = MagicMock(return_value=qb)
        resolver._get_familiarity_penalty = MagicMock(return_value=1.0)

        # Mock tribe modifiers
        with patch('app.orchestrator.play_resolver.get_tribe_modifiers') as mock_tribe:
            mock_tribe.return_value = {
                "tribe": "Balanced",
                "base_yards": 2.5,
                "std_dev": 1.0,
                "breakaway_mult": 1.0,
                "fumble_mult": 1.0
            }

            # Mock physics state
            resolver._create_rb_physics = MagicMock()
            mock_physics_state = MagicMock()
            mock_physics_state.yards_after_contact = 0.0
            mock_physics_state.balance = 50.0
            resolver._create_rb_physics.return_value = mock_physics_state

            print("Running _resolve_run_play...")
            result = resolver._resolve_run_play(command)
            print("Result:", result)

    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    run_debug()

import math
from app.engine.physics import BallPhysics

from typing import Any, Optional
from app.core.random_utils import DeterministicRNG

class SpecialTeamsEngine:
    @staticmethod
    def calculate_kick(
        rng_or_power: Any = None,
        power: Optional[int] = None,
        accuracy: Optional[int] = None,
        kick_type: str = "FieldGoal",
        rng: Optional[Any] = None,
    ) -> dict:
        """
        Calculate kick trajectory and result with deterministic RNG.
        Supports both (rng, power, accuracy) and (power=90, accuracy=95).
        """
        if isinstance(rng_or_power, (int, float)):
            actual_power = int(rng_or_power)
            actual_accuracy = accuracy if accuracy is not None else 80
            actual_rng = rng or DeterministicRNG(f"kick_{actual_power}_{actual_accuracy}_{kick_type}")
        elif rng_or_power is not None and not isinstance(rng_or_power, (int, float)):
            actual_rng = rng_or_power
            actual_power = power if power is not None else 80
            actual_accuracy = accuracy if accuracy is not None else 80
        else:
            actual_power = power if power is not None else 80
            actual_accuracy = accuracy if accuracy is not None else 80
            actual_rng = rng or DeterministicRNG(f"kick_{actual_power}_{actual_accuracy}_{kick_type}")

        # Base Velocity from Power (0-100) -> 20-35 m/s
        v0 = 20 + (actual_power / 100.0) * 15

        # Angle
        angle = 45.0
        if kick_type == "Punt":
            angle = 55.0  # Higher angle for hangtime

        # Accuracy affects lateral deviation (wind/hook)
        accuracy_error = (100 - actual_accuracy) * 0.5  # Degrees off center
        deviation = actual_rng.uniform(-accuracy_error, accuracy_error)

        # Spiral Efficiency
        spiral = 0.1 if kick_type == "FieldGoal" else 0.9  # FG is end-over-end (wobbly aerodynamics), Punt is spiral

        trajectory = BallPhysics.calculate_trajectory(v0, angle, spiral_efficiency=spiral)

        return {
            "trajectory": trajectory,
            "distance": trajectory[-1]['x'],
            "hang_time": trajectory[-1]['t'],
            "deviation": deviation
        }

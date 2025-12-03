import math
from app.engine.physics import BallPhysics

class SpecialTeamsEngine:
    @staticmethod
    def calculate_kick(rng, power: int, accuracy: int, kick_type: str = "FieldGoal") -> dict:
        """
        Calculate kick trajectory and result.
        """
        # Base Velocity from Power (0-100) -> 20-35 m/s
        v0 = 20 + (power / 100.0) * 15

        # Angle
        angle = 45.0
        if kick_type == "Punt":
            angle = 55.0 # Higher angle for hangtime

        # Accuracy affects lateral deviation (wind/hook)
        accuracy_error = (100 - accuracy) * 0.5 # Degrees off center
        deviation = rng.uniform(-accuracy_error, accuracy_error)

        # Spiral Efficiency
        spiral = 0.1 if kick_type == "FieldGoal" else 0.9 # FG is end-over-end (wobbly aerodynamics), Punt is spiral

        trajectory = BallPhysics.calculate_trajectory(v0, angle, spiral_efficiency=spiral)

        return {
            "trajectory": trajectory,
            "distance": trajectory[-1]['x'],
            "hang_time": trajectory[-1]['t'],
            "deviation": deviation
        }

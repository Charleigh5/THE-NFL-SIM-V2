import enum
from pydantic import BaseModel
from typing import List

class PassRushMove(str, enum.Enum):
    BULL_RUSH = "Bull Rush"
    SWIM = "Swim"
    SPIN = "Spin"
    RIP = "Rip"

class CoverageType(str, enum.Enum):
    MAN = "Man"
    ZONE = "Zone"

class PassRushEngine:
    @staticmethod
    def resolve_move(move: PassRushMove, rusher_rating: int, blocker_rating: int, blocker_weight: int, rusher_strength: int) -> dict:
        """
        Resolve a pass rush move based on physics and ratings.
        """
        success = False
        momentum = 0.0

        if move == PassRushMove.BULL_RUSH:
            # F = ma logic. Heavier/Stronger rusher has advantage.
            force = rusher_strength * 1.5
            anchor = blocker_weight * 0.8 + blocker_rating
            if force > anchor:
                success = True
                momentum = (force - anchor) / 10.0

        elif move == PassRushMove.SWIM:
            # Finesse vs Agility
            agility_diff = rusher_rating - blocker_rating
            if agility_diff > 5:
                success = True

        elif move == PassRushMove.SPIN:
            # Counter move
            if rusher_rating > blocker_rating:
                success = True

        return {"success": success, "momentum": momentum}

class DefenseEngine:
    @staticmethod
    def calculate_pursuit_angle(defender_pos: dict, ball_carrier_pos: dict, ball_carrier_velocity: dict) -> float:
        """
        Calculate the optimal interception angle (Inside-Out).
        """
        import math
        dx = ball_carrier_pos['x'] - defender_pos['x']
        dy = ball_carrier_pos['y'] - defender_pos['y']

        # Simple pursuit vector
        angle = math.atan2(dy, dx)
        return math.degrees(angle)

    @staticmethod
    def resolve_zone_coverage(rng, defender_zone: dict, ball_pos: dict, awareness: int) -> bool:
        """
        Check if defender reacts to ball entering zone.
        """
        # Check if ball is in zone
        in_zone = (defender_zone['x_min'] <= ball_pos['x'] <= defender_zone['x_max'] and
                   defender_zone['y_min'] <= ball_pos['y'] <= defender_zone['y_max'])

        if in_zone:
            # Reaction check
            return rng.randint(0, 100) < awareness
        return False

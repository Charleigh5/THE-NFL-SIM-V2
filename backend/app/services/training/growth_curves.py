from enum import Enum
from typing import Dict, Tuple

class GrowthCurveType(Enum):
    RB_SPEED = "RB_SPEED"        # Early Peak (26), Sharp Decline (28)
    SKILL_POS = "SKILL_POS"      # Prime (26-29), Moderate Decline
    TRENCHES = "TRENCHES"        # Late Peak (27-31), Slow Decline
    QB_KICKER = "QB_KICKER"      # Longevity (35+), Very Slow Decline

# Map positions to curve archetypes
POSITION_CURVE_MAP = {
    "RB": GrowthCurveType.RB_SPEED,
    "CB": GrowthCurveType.RB_SPEED,  # Cornerbacks also rely heavily on speed
    "WR": GrowthCurveType.SKILL_POS,
    "TE": GrowthCurveType.SKILL_POS,
    "LB": GrowthCurveType.SKILL_POS,
    "FS": GrowthCurveType.SKILL_POS,
    "SS": GrowthCurveType.SKILL_POS,
    "OT": GrowthCurveType.TRENCHES,
    "OG": GrowthCurveType.TRENCHES,
    "C": GrowthCurveType.TRENCHES,
    "DE": GrowthCurveType.TRENCHES,
    "DT": GrowthCurveType.TRENCHES,
    "QB": GrowthCurveType.QB_KICKER,
    "K": GrowthCurveType.QB_KICKER,
    "P": GrowthCurveType.QB_KICKER,
}

class GrowthCurveEngine:
    """
    Manages age-based progression and regression logic.
    Based on PFF research on positional aging curves.
    """

    @staticmethod
    def get_xp_multiplier(age: int, position: str) -> float:
        """
        Returns XP multiplier based on age and position.
        Young players learn faster (neuroplasticity/physical dev).
        """
        # Rookie Bump (21-22)
        if age <= 22:
            return 1.5

        # Development Phase (23-24)
        if age <= 24:
            return 1.2

        # Prime & Post-Prime Logic by Position
        curve = POSITION_CURVE_MAP.get(position, GrowthCurveType.SKILL_POS)

        if curve == GrowthCurveType.RB_SPEED:
            if age <= 26: return 1.0  # Prime
            if age <= 28: return 0.8  # Slight decline
            return 0.5                # Wall hit

        elif curve == GrowthCurveType.SKILL_POS:
            if age <= 29: return 1.0  # Prime
            if age <= 31: return 0.8  # Vet
            return 0.5

        elif curve == GrowthCurveType.TRENCHES:
            if age <= 30: return 1.0  # Long Prime
            if age <= 33: return 0.9  # Graceful aging
            return 0.6

        elif curve == GrowthCurveType.QB_KICKER:
            if age <= 33: return 1.0  # Extended Prime
            if age <= 37: return 0.9  # Tom Brady zone
            return 0.7

        return 1.0

    @staticmethod
    def get_regression_score(age: int, position: str) -> int:
        """
        Returns a 'Regression Score' (0-100 scale) indicating severity of attribute loss.
        0 = No Regression
        10 = Minor (lose 1 point in a secondary stat)
        50 = Major (lose 2-3 points in primary stats)
        """
        curve = POSITION_CURVE_MAP.get(position, GrowthCurveType.SKILL_POS)
        score = 0

        if curve == GrowthCurveType.RB_SPEED:
            # RB Wall logic: Hard hits after 27/28
            decline_start = 27
            severity = 12 # Steep penalty
            if age > decline_start:
                score = (age - decline_start) * severity

        elif curve == GrowthCurveType.SKILL_POS:
            decline_start = 29
            severity = 6
            if age > decline_start:
                score = (age - decline_start) * severity

        elif curve == GrowthCurveType.TRENCHES:
            decline_start = 31
            severity = 4 # Slow decline
            if age > decline_start:
                score = (age - decline_start) * severity

        elif curve == GrowthCurveType.QB_KICKER:
            decline_start = 35
            severity = 3 # Very slow
            if age > decline_start:
                score = (age - decline_start) * severity

        # Cap regression score
        return min(max(int(score), 0), 100)

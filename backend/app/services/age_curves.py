
from typing import Dict, Tuple

# Format: (peak_start, peak_end, decline_rate_per_year)
POSITION_CURVES: Dict[str, Tuple[int, int, float]] = {
    "QB":  (26, 30, 0.02),   # Slow decline, mental peak late
    "RB":  (23, 27, 0.06),   # Steep decline, early peak
    "WR":  (25, 29, 0.04),   # Moderate decline
    "TE":  (26, 30, 0.03),   # Technique helps longevity
    "OT":  (26, 32, 0.03),   # Long prime, technique reliant
    "OG":  (26, 32, 0.03),
    "C":   (26, 32, 0.02),   # Mental aspect extends career
    "DE":  (25, 29, 0.04),
    "DT":  (25, 30, 0.035),
    "LB":  (25, 29, 0.04),   # Athleticism dependent
    "EDGE": (25, 29, 0.045), # Burst dependent
    "CB":  (24, 28, 0.05),   # Speed dependent, sharp falloff
    "S":   (25, 30, 0.035),
    "K":   (28, 38, 0.015),  # Very long prime
    "P":   (28, 38, 0.015),
    # Default for unknown positions
    "DEFAULT": (25, 29, 0.04)
}

def get_age_modifier(age: int, position: str) -> float:
    """
    Calculate the age-based performance modifier (0.0 - 1.0).
    Returns 1.0 if player is in their prime.
    """
    curve = POSITION_CURVES.get(position, POSITION_CURVES["DEFAULT"])
    peak_start, peak_end, decline_rate = curve

    if age < peak_start:
        # Rising phase: Rookie -> Prime
        # e.g., Age 21 = 0.85, Age 25 = 0.97
        growth_per_year = 0.15 / (peak_start - 20)
        return min(1.0, 0.85 + (age - 21) * growth_per_year)

    elif age <= peak_end:
        # Peak phase
        return 1.0

    else:
        # Decline phase
        # Linear decline from 1.0
        decline = (age - peak_end) * decline_rate
        # Floor value to prevent elite vets from becoming useless too fast
        # Minimum physical floor is 70% of peak
        return max(0.70, 1.0 - decline)

def get_experience_bonus(years_experience: int, position: str) -> float:
    """
    Calculate bonus multiplier for experience (mental attributes).
    Returns 1.0 - 1.15 multiplier.
    """
    if position == "QB":
        # QBs gain significant mental advantage with experience
        return min(1.15, 1.0 + years_experience * 0.015)
    elif position in ("OL", "TE", "C", "OG", "OT"):
        # Technique positions benefit more from experience
        return min(1.10, 1.0 + years_experience * 0.012)
    elif position in ("S", "LB"):
        # Defensive playcallers/readers
        return min(1.08, 1.0 + years_experience * 0.010)
    else:
        # Purely physical positions benefit less
        return min(1.05, 1.0 + years_experience * 0.008)

def get_physical_regression(age: int, position: str) -> float:
    """
    Specific modifier for physical stats (Speed, Acceleration)
    Declines faster than overall ability for most positions.
    """
    if age < 29:
        return 1.0

    # After 29, physicals drop
    years_over = age - 29

    if position in ("RB", "CB", "WR", "EDGE"):
        # Relies on speed/burst -> faster regression
        return max(0.80, 1.0 - (years_over * 0.015))
    else:
        # Slower regression for linemen/QBs
        return max(0.85, 1.0 - (years_over * 0.008))

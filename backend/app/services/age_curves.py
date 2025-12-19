
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

# Age-based LEARNING rate modifiers (how fast players improve)
# Different from performance curves - this is about skill acquisition
AGE_DEVELOPMENT_MODIFIERS: Dict[Tuple[int, int], float] = {
    (21, 24): 1.2,   # Peak learning years - young brain, high neural plasticity
    (25, 27): 1.0,   # Steady state - established patterns
    (28, 30): 0.8,   # Slower gains - harder to learn new skills
    (31, 99): 0.5,   # Veteran maintenance - mostly pattern recognition
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


def get_development_rate_modifier(age: int, development_trait: str = "NORMAL") -> float:
    """
    Calculate XP/skill learning rate modifier based on age.

    Young players (21-24) learn faster, veterans (31+) struggle to develop new skills.
    This affects how quickly training drills improve player ratings.

    Args:
        age: Player's current age
        development_trait: Player's development trait (NORMAL, STAR, SUPERSTAR, XFACTOR)

    Returns:
        Multiplier for XP gains (0.5 - 1.5)
    """
    # Find the age bracket
    base_modifier = 1.0
    for (min_age, max_age), modifier in AGE_DEVELOPMENT_MODIFIERS.items():
        if min_age <= age <= max_age:
            base_modifier = modifier
            break

    # Development trait bonus stacks with age
    trait_bonus = {
        "NORMAL": 1.0,
        "STAR": 1.25,
        "SUPERSTAR": 1.5,
        "XFACTOR": 2.0,
    }.get(development_trait, 1.0)

    return base_modifier * trait_bonus


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


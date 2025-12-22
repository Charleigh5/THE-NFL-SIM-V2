
from typing import Dict, Tuple, Optional, Any
from enum import Enum

class PlayerArchetype(Enum):
    """Player archetype enum used for curve determination."""
    SCRAMBLER = "SCRAMBLER"         # QB with high speed
    POCKET = "POCKET"               # QB with low speed
    SPEED_BACK = "SPEED_BACK"       # RB with high speed
    POWER_BACK = "POWER_BACK"       # RB with high trucking
    DEEP_THREAT = "DEEP_THREAT"     # WR with high speed
    POSSESSION = "POSSESSION"       # WR with high route running
    SPEED_RUSHER = "SPEED_RUSHER"   # DL/Edge with high speed
    POWER_RUSHER = "POWER_RUSHER"   # DL with high strength
    COVERAGE_LB = "COVERAGE_LB"     # LB with high speed/zone
    THUMPER_LB = "THUMPER_LB"       # LB with high hit power
    MAN_CORNER = "MAN_CORNER"       # CB relying on speed
    ZONE_SAFETY = "ZONE_SAFETY"     # S relying on zone coverage
    DEFAULT = "DEFAULT"

# =============================================================================
# ARCHETYPE-AWARE POSITION CURVES
# Format: (peak_start, peak_end, decline_rate_per_year)
# =============================================================================
POSITION_CURVES: Dict[str, Tuple[int, int, float]] = {
    # Default fallbacks (used if no archetype match)
    "QB":  (27, 32, 0.02),
    "RB":  (24, 27, 0.05),
    "WR":  (25, 29, 0.04),
    "TE":  (26, 30, 0.03),
    "OT":  (26, 32, 0.03),
    "OG":  (26, 32, 0.03),
    "C":   (26, 32, 0.02),
    "DE":  (25, 29, 0.04),
    "DT":  (25, 30, 0.035),
    "LB":  (25, 29, 0.04),
    "EDGE": (25, 29, 0.045),
    "CB":  (24, 28, 0.05),
    "S":   (25, 30, 0.035),
    "K":   (28, 38, 0.015),
    "P":   (28, 38, 0.015),
    "DEFAULT": (25, 29, 0.04)
}

# Archetype-specific overrides (key = archetype name, value = curve)
ARCHETYPE_CURVES: Dict[str, Tuple[int, int, float]] = {
    # QB Archetypes
    "SCRAMBLER": (25, 29, 0.04),     # Mobile QBs decline faster
    "POCKET": (28, 34, 0.015),       # Pocket passers peak later

    # RB Archetypes
    "SPEED_BACK": (23, 26, 0.06),    # Speed backs fall off cliff
    "POWER_BACK": (25, 29, 0.035),   # Power backs can grind longer

    # WR Archetypes
    "DEEP_THREAT": (24, 28, 0.05),   # Needs separation to be effective
    "POSSESSION": (27, 32, 0.025),   # Route-runners age gracefully

    # DL/Edge Archetypes
    "SPEED_RUSHER": (24, 28, 0.05),  # Burst-dependent
    "POWER_RUSHER": (27, 32, 0.025), # Power endures

    # LB Archetypes
    "COVERAGE_LB": (24, 28, 0.04),
    "THUMPER_LB": (26, 30, 0.03),

    # DB Archetypes
    "MAN_CORNER": (24, 28, 0.055),   # Speed is everything
    "ZONE_SAFETY": (28, 33, 0.02),   # Mental/positioning peaks late
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


def calculate_attribute_regression(
    player_age: int,
    position: str,
    current_attributes: Dict[str, int],
    rng_value: float = 0.5
) -> Dict[str, int]:
    """
    Calculate attribute regression for an aging player.

    Returns a dictionary of {attribute_name: points_to_decrease}.
    Called during offseason/year transition.

    Args:
        player_age: Player's age after the season
        position: Player's position (e.g., "RB", "QB")
        current_attributes: Dict of current attribute ratings
        rng_value: Random value 0-1 for probabilistic regression

    Returns:
        Dict mapping attribute names to point decreases (all positive values)
    """
    from app.core.constants import REGRESSION_WEIGHTS

    regression_results: Dict[str, int] = {}

    # Get position curve info
    curve = POSITION_CURVES.get(position, POSITION_CURVES["DEFAULT"])
    peak_start, peak_end, base_decline_rate = curve

    # No regression if still in prime or rising
    if player_age <= peak_end:
        return regression_results

    # Years past prime determines severity
    years_past_prime = player_age - peak_end

    # Base regression points available per year (increases with age)
    # Year 1 past prime: 1-2 pts, Year 5+: 3-5 pts
    base_regression_points = min(5, 1 + (years_past_prime * 0.75))

    # Position modifier (RBs regress harder than QBs)
    position_modifier = base_decline_rate / 0.04  # Normalize to 1.0 for average

    # Calculate regression per attribute
    for attr_name, weight in REGRESSION_WEIGHTS.items():
        if attr_name not in current_attributes:
            continue

        current_value = current_attributes[attr_name]

        # Don't regress attributes below 40 (floor)
        if current_value <= 40:
            continue

        # Regression probability based on weight and age
        regression_chance = weight * position_modifier * (0.3 + years_past_prime * 0.15)

        if rng_value < regression_chance:
            # Calculate points to lose (1-3 typically)
            points_lost = max(1, int(base_regression_points * weight))

            # Higher rated attributes regress more noticeably
            if current_value >= 90:
                points_lost += 1
            elif current_value >= 80:
                points_lost = max(points_lost, 1)

            regression_results[attr_name] = points_lost

    return regression_results


def get_player_archetype(
    position: str,
    attributes: Optional[Dict[str, Any]] = None
) -> PlayerArchetype:
    """
    Determine a player's archetype based on their position and key attributes.

    This function analyzes attribute thresholds to classify players into archetypes
    that determine their aging curve. Speed-dependent players decline faster.

    Args:
        position: Player's position (e.g., "QB", "RB", "WR")
        attributes: Dict of player attributes (speed, trucking, route_running, etc.)

    Returns:
        PlayerArchetype enum value
    """
    if attributes is None:
        attributes = {}

    speed = attributes.get("speed", 70)
    trucking = attributes.get("trucking", 70)
    route_running = attributes.get("route_running", 70)
    strength = attributes.get("strength", 70)
    hit_power = attributes.get("hit_power", 70)
    zone_coverage = attributes.get("zone_coverage", 70)

    if position == "QB":
        return PlayerArchetype.SCRAMBLER if speed > 80 else PlayerArchetype.POCKET

    elif position == "RB":
        if speed > 90:
            return PlayerArchetype.SPEED_BACK
        elif trucking > 85:
            return PlayerArchetype.POWER_BACK
        return PlayerArchetype.SPEED_BACK  # Default RBs lean speed

    elif position == "WR":
        if speed > 93:
            return PlayerArchetype.DEEP_THREAT
        elif route_running > 85:
            return PlayerArchetype.POSSESSION
        return PlayerArchetype.DEEP_THREAT  # Default WRs lean speed

    elif position in ("DE", "EDGE"):
        return PlayerArchetype.SPEED_RUSHER if speed > 80 else PlayerArchetype.POWER_RUSHER

    elif position == "DT":
        return PlayerArchetype.POWER_RUSHER  # DTs are almost always power

    elif position == "LB":
        if speed > 85 or zone_coverage > 75:
            return PlayerArchetype.COVERAGE_LB
        elif hit_power > 85:
            return PlayerArchetype.THUMPER_LB
        return PlayerArchetype.THUMPER_LB  # Default LBs are thumpers

    elif position == "CB":
        return PlayerArchetype.MAN_CORNER  # CBs are almost always speed-dependent

    elif position == "S":
        return PlayerArchetype.ZONE_SAFETY if zone_coverage > 85 else PlayerArchetype.MAN_CORNER

    return PlayerArchetype.DEFAULT


def get_player_phase(
    position: str,
    age: int,
    archetype: Optional[PlayerArchetype] = None
) -> str:
    """
    Determine player's career phase using archetype-aware curves.

    Args:
        position: Player's position
        age: Player's current age
        archetype: Optional PlayerArchetype (if None, uses position default)

    Returns:
        "ASCENSION" (pre-prime), "PRIME", or "DECLINE" (post-prime)
    """
    # Determine which curve to use
    if archetype and archetype.value in ARCHETYPE_CURVES:
        curve = ARCHETYPE_CURVES[archetype.value]
    else:
        curve = POSITION_CURVES.get(position, POSITION_CURVES["DEFAULT"])

    peak_start, peak_end, _ = curve

    if age < peak_start:
        return "ASCENSION"
    elif age <= peak_end:
        return "PRIME"
    else:
        return "DECLINE"


def get_phase_xp_multiplier(
    position: str,
    age: int,
    archetype: Optional[PlayerArchetype] = None
) -> float:
    """
    Get XP multiplier based on career phase (archetype-aware).

    Returns:
        Multiplier (0.5 - 1.2 typically)
    """
    from app.core.constants import AGE_PHASE_MULTIPLIERS

    phase = get_player_phase(position, age, archetype)
    return AGE_PHASE_MULTIPLIERS.get(phase, 1.0)


def get_archetype_curve(
    position: str,
    archetype: Optional[PlayerArchetype] = None
) -> Tuple[int, int, float]:
    """
    Get the (peak_start, peak_end, decline_rate) curve for an archetype.

    Returns:
        Tuple of (peak_start, peak_end, decline_rate)
    """
    if archetype and archetype.value in ARCHETYPE_CURVES:
        return ARCHETYPE_CURVES[archetype.value]
    return POSITION_CURVES.get(position, POSITION_CURVES["DEFAULT"])

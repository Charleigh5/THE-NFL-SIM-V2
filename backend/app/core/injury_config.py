"""
Injury System Configuration
============================
Centralized tunable parameters for the per-play injury probability model.

Based on INJURY_SYSTEM_RESEARCH document and NFL/AWS Digital Athlete data.
All values are tunable for simulation balancing without code changes.

Formula: Injury Probability = Base × PlayType × Position × (Age × Durability × Fatigue)
"""


# ============================================================================
# BASE PROBABILITY
# ============================================================================

# Base injury probability per snap (~0.15% aligns with ~1-2 injuries per game)
BASE_PLAY_INJURY_PROBABILITY = 0.0015


# ============================================================================
# PLAY TYPE MULTIPLIERS
# ============================================================================

PLAY_TYPE_MULTIPLIERS: dict[str, float] = {
    "STANDARD": 1.0,
    "PASS_PLAY": 1.0,
    "RUN_PLAY": 1.1,
    "QB_KNOCKDOWN": 1.2,  # QB hit while releasing ball (pressure throw)
    "SACK": 1.5,  # High-velocity collision
    "HIP_DROP_TACKLE": 20.0,  # NFL/AWS Digital Athlete finding
    "NON_CONTACT_CUT": 0.4,  # Lower extremity baseline
    "SCRAMBLE": 1.2,  # QB exposed to hits
    "DESIGNED_QB_RUN": 1.3,  # QB taking designed contact
    "KICKOFF": 1.4,  # High-speed special teams
    "PUNT_RETURN": 1.3,
    "KICK_RETURN": 1.3,
    "FIELD_GOAL": 0.5,  # Limited contact
}


# ============================================================================
# POSITIONAL MULTIPLIERS
# ============================================================================
# Derived from 'Decoding NFL Injuries' and 'Epidemiology of Injuries at Combine'

POSITION_MULTIPLIERS: dict[str, float] = {
    # High-collision / high-velocity positions (1.3x)
    "RB": 1.3,
    "CB": 1.3,
    "S": 1.3,
    "FS": 1.3,
    "SS": 1.3,
    # Medium-contact positions (1.2x)
    "WR": 1.2,
    "TE": 1.2,
    "LB": 1.2,
    "MLB": 1.2,
    "OLB": 1.2,
    "ILB": 1.2,
    # Line positions (1.1-1.15x)
    "OT": 1.15,
    "OG": 1.15,
    "C": 1.15,
    "OL": 1.15,
    "DT": 1.1,
    "DE": 1.1,
    "DL": 1.1,
    "EDGE": 1.1,
    # Protected positions (0.7-0.8x)
    "QB": 0.8,
    "K": 0.7,
    "P": 0.7,
}

# Default multiplier for unknown positions
DEFAULT_POSITION_MULTIPLIER = 1.0


# ============================================================================
# PLAYER-SPECIFIC RISK MULTIPLIERS
# ============================================================================

# Age bands: (min_age, max_age): multiplier
AGE_RISK_MULTIPLIERS: dict[tuple[int, int], float] = {
    (0, 29): 1.0,  # Prime years
    (30, 32): 1.05,  # Early decline
    (33, 99): 1.15,  # Veteran wear
}

# Durability rating bands (injury_resistance attribute)
DURABILITY_RISK_MULTIPLIERS: dict[tuple[int, int], float] = {
    (90, 100): 0.90,  # Elite durability
    (80, 89): 0.95,  # Above average
    (70, 79): 1.00,  # Average
    (0, 69): 1.10,  # Below average
}

# Medical staff rating bands
MEDICAL_STAFF_RISK_MULTIPLIERS: dict[tuple[int, int], float] = {
    (90, 100): 0.95,
    (80, 89): 0.98,
    (0, 79): 1.00,
}


# ============================================================================
# FATIGUE MULTIPLIER
# ============================================================================

# Fatigue impact starts at this level (0-100 scale)
FATIGUE_IMPACT_THRESHOLD = 50

# Maximum additional risk from fatigue (at 100 fatigue)
# Formula: 1.0 + ((fatigue - threshold) / (100 - threshold)) * MAX_FATIGUE_MULTIPLIER
MAX_FATIGUE_RISK_MULTIPLIER = 0.50  # +50% max risk at 100 fatigue


# ============================================================================
# TOUGHNESS-BASED PLAY-THROUGH SYSTEM
# ============================================================================

# Base toughness thresholds for playing through injuries
# Players with toughness >= threshold can play through that severity
# Format: severity_level: required_toughness (0-100)
TOUGHNESS_PLAY_THROUGH_THRESHOLDS: dict[int, int] = {
    1: 30,  # Minor injuries - most players can play through
    2: 45,
    3: 60,
    4: 75,
    5: 85,  # Moderate injuries - only tough players
    6: 92,
    7: 98,  # Near-elite toughness required (Ragknow bypasses)
}

# Performance penalty multiplier based on toughness
# Higher toughness = reduced penalty when playing through injury
# Formula: base_penalty * (1.0 - (toughness / 100) * TOUGHNESS_PENALTY_REDUCTION)
TOUGHNESS_PENALTY_REDUCTION_FACTOR = 0.3  # Up to 30% penalty reduction at 100 toughness


# ============================================================================
# INJURY PERFORMANCE PENALTIES
# ============================================================================

# Attribute penalties when playing through an injury (by severity)
# These are BASE penalties, reduced by toughness
INJURY_PERFORMANCE_PENALTIES: dict[int, dict[str, int]] = {
    1: {"speed": -2, "agility": -2, "acceleration": -1},
    2: {"speed": -3, "agility": -3, "acceleration": -2},
    3: {"speed": -5, "agility": -4, "acceleration": -3},
    4: {"speed": -7, "agility": -6, "acceleration": -5, "strength": -3},
    5: {"speed": -10, "agility": -8, "acceleration": -6, "strength": -5},
    6: {"speed": -12, "agility": -10, "acceleration": -8, "strength": -6},
    7: {"speed": -15, "agility": -12, "acceleration": -10, "strength": -8},
}


# ============================================================================
# SEVERITY ESCALATION (Playing Injured Risk)
# ============================================================================

# Base escalation chance per play when playing through injury
# Formula: BASE_CHANCE * severity
INJURY_ESCALATION_BASE_CHANCE = 0.02  # 2% per severity level per play

# Maximum severity increase when escalation occurs
INJURY_ESCALATION_MAX_INCREASE = 2


# ============================================================================
# RAGKNOW TRAIT SPECIAL BONUSES
# ============================================================================

RAGKNOW_RECOVERY_MULTIPLIER = 0.90  # 10% faster recovery
RAGKNOW_MAX_PLAYABLE_SEVERITY = 7  # Can play through up to Moderate
RAGKNOW_IGNORE_PENALTIES = True  # No performance penalties when injured
RAGKNOW_BLOCK_DEGRADATION = True  # No permanent attribute loss


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_play_type_multiplier(play_type: str) -> float:
    """Get the injury risk multiplier for a play type."""
    return PLAY_TYPE_MULTIPLIERS.get(play_type.upper(), 1.0)


def get_position_multiplier(position: str) -> float:
    """Get the injury risk multiplier for a position."""
    if not position:
        return DEFAULT_POSITION_MULTIPLIER
    return POSITION_MULTIPLIERS.get(position.upper(), DEFAULT_POSITION_MULTIPLIER)


def get_age_multiplier(age: int) -> float:
    """Get the injury risk multiplier based on player age."""
    for (min_age, max_age), multiplier in AGE_RISK_MULTIPLIERS.items():
        if min_age <= age <= max_age:
            return multiplier
    return 1.0


def get_durability_multiplier(injury_resistance: int) -> float:
    """Get the injury risk multiplier based on durability rating."""
    for (min_rat, max_rat), multiplier in DURABILITY_RISK_MULTIPLIERS.items():
        if min_rat <= injury_resistance <= max_rat:
            return multiplier
    return 1.0


def get_medical_staff_multiplier(medical_rating: int) -> float:
    """Get the injury risk multiplier based on medical staff quality."""
    for (min_rat, max_rat), multiplier in MEDICAL_STAFF_RISK_MULTIPLIERS.items():
        if min_rat <= medical_rating <= max_rat:
            return multiplier
    return 1.0


def get_fatigue_multiplier(fatigue: float) -> float:
    """
    Calculate injury risk multiplier from fatigue.

    Fatigue below FATIGUE_IMPACT_THRESHOLD has no effect.
    Above threshold, risk increases linearly up to MAX_FATIGUE_RISK_MULTIPLIER.
    """
    if fatigue <= FATIGUE_IMPACT_THRESHOLD:
        return 1.0

    # Calculate how far past threshold (0.0 to 1.0)
    fatigue_factor = (fatigue - FATIGUE_IMPACT_THRESHOLD) / (100 - FATIGUE_IMPACT_THRESHOLD)
    return 1.0 + (fatigue_factor * MAX_FATIGUE_RISK_MULTIPLIER)


def can_play_through_injury(severity: int, toughness: int, has_ragknow: bool = False) -> bool:
    """
    Determine if a player can play through an injury based on toughness.

    Args:
        severity: Injury severity (1-10)
        toughness: Player's toughness rating (0-100)
        has_ragknow: Whether player has the Ragknow trait

    Returns:
        True if player can play through this injury
    """
    # Ragknow bypasses normal toughness checks up to severity 7
    if has_ragknow and severity <= RAGKNOW_MAX_PLAYABLE_SEVERITY:
        return True

    # Severity 8+ cannot be played through by anyone
    if severity > 7:
        return False

    # Check toughness threshold
    required_toughness = TOUGHNESS_PLAY_THROUGH_THRESHOLDS.get(severity, 100)
    return toughness >= required_toughness


def calculate_toughness_penalty_reduction(toughness: int) -> float:
    """
    Calculate how much injury penalties are reduced by toughness.

    Returns a multiplier (0.7 to 1.0) to apply to base penalties.
    """
    reduction = (toughness / 100.0) * TOUGHNESS_PENALTY_REDUCTION_FACTOR
    return 1.0 - reduction

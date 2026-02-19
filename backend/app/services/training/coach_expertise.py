#!/usr/bin/env python3
"""
Coach Expertise System
======================
Calculates development bonuses based on coach tier, scheme expertise,
and archetypes. Higher-tier coaches significantly impact player growth.

Tier Multipliers:
- LEGEND: 1.50x development
- ELITE: 1.30x development
- VETERAN: 1.10x development
- DEVELOPING: 1.00x (baseline)
- ROOKIE: 0.90x development
"""

from enum import Enum

from app.models.coach import CoachTier

# ============================================================================
# TIER DEVELOPMENT MULTIPLIERS
# ============================================================================

TIER_MULTIPLIERS: dict[CoachTier, float] = {
    CoachTier.LEGEND: 1.50,
    CoachTier.ELITE: 1.30,
    CoachTier.VETERAN: 1.10,
    CoachTier.DEVELOPING: 1.00,
    CoachTier.ROOKIE: 0.90,
}

# Combined rating thresholds for tier calculation
TIER_THRESHOLDS = [
    (270, CoachTier.LEGEND),
    (230, CoachTier.ELITE),
    (180, CoachTier.VETERAN),
    (140, CoachTier.DEVELOPING),
    (0, CoachTier.ROOKIE),
]

# ============================================================================
# SCHEME-BASED EXPERTISE
# ============================================================================

# Maps offensive/defensive schemes to position bonuses
SCHEME_EXPERTISE: dict[str, dict[str, float]] = {
    # Offensive Schemes
    "West Coast": {"QB": 0.15, "WR": 0.15, "TE": 0.12, "RB": 0.08},
    "Air Raid": {"QB": 0.20, "WR": 0.18, "TE": 0.10},
    "Spread": {"QB": 0.15, "WR": 0.15, "RB": 0.10},
    "Power Run": {"RB": 0.18, "OL": 0.15, "FB": 0.15, "TE": 0.10},
    "Zone Run": {"RB": 0.15, "OL": 0.12, "TE": 0.08},
    "RPO": {"QB": 0.12, "RB": 0.12, "WR": 0.10, "OL": 0.08},
    "Pro Style": {"QB": 0.10, "RB": 0.10, "WR": 0.10, "TE": 0.10, "OL": 0.10},

    # Defensive Schemes
    "4-3": {"DE": 0.15, "DT": 0.15, "LB": 0.10, "CB": 0.08},
    "3-4": {"NT": 0.18, "OLB": 0.15, "ILB": 0.12, "DE": 0.10},
    "Zone Blitz": {"LB": 0.18, "S": 0.15, "CB": 0.10},
    "Cover-2": {"S": 0.15, "CB": 0.12, "LB": 0.08},
    "Cover-3": {"FS": 0.15, "CB": 0.12, "SS": 0.10},
    "Man Coverage": {"CB": 0.18, "S": 0.12, "LB": 0.08},
    "Tampa 2": {"MLB": 0.15, "S": 0.12, "CB": 0.12},
}

# ============================================================================
# COACH ARCHETYPES
# ============================================================================

class CoachArchetype(str, Enum):
    """Coach specialization archetypes."""
    GENERALIST = "GENERALIST"
    QB_GURU = "QB_GURU"
    OL_MASTER = "OL_MASTER"
    RUN_GAME_SPECIALIST = "RUN_GAME_SPECIALIST"
    RECEIVING_COACH = "RECEIVING_COACH"
    DB_WHISPERER = "DB_WHISPERER"
    PASS_RUSH_SPECIALIST = "PASS_RUSH_SPECIALIST"
    LB_GURU = "LB_GURU"
    SPECIAL_TEAMS_ACE = "SPECIAL_TEAMS_ACE"

# Archetype bonuses: (primary positions, primary bonus, secondary positions, secondary bonus)
ARCHETYPE_BONUSES: dict[CoachArchetype, dict[str, float]] = {
    CoachArchetype.GENERALIST: {},  # No specific bonuses, balanced
    CoachArchetype.QB_GURU: {"QB": 0.25, "WR": 0.10, "TE": 0.08},
    CoachArchetype.OL_MASTER: {"OL": 0.25, "C": 0.25, "G": 0.25, "T": 0.25, "RB": 0.10},
    CoachArchetype.RUN_GAME_SPECIALIST: {"RB": 0.25, "FB": 0.20, "OL": 0.12},
    CoachArchetype.RECEIVING_COACH: {"WR": 0.25, "TE": 0.20, "RB": 0.08},
    CoachArchetype.DB_WHISPERER: {"CB": 0.25, "S": 0.22, "FS": 0.22, "SS": 0.22},
    CoachArchetype.PASS_RUSH_SPECIALIST: {"DE": 0.25, "EDGE": 0.25, "DT": 0.15, "OLB": 0.12},
    CoachArchetype.LB_GURU: {"LB": 0.25, "ILB": 0.25, "OLB": 0.22, "MLB": 0.25},
    CoachArchetype.SPECIAL_TEAMS_ACE: {"K": 0.30, "P": 0.30, "LS": 0.25},
}

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_tier_from_ratings(offense: int, defense: int, development: int) -> CoachTier:
    """
    Calculate coach tier based on combined ratings.

    Args:
        offense: Offensive rating (0-100)
        defense: Defensive rating (0-100)
        development: Development rating (0-100)

    Returns:
        CoachTier based on combined score
    """
    combined = offense + defense + development

    for threshold, tier in TIER_THRESHOLDS:
        if combined >= threshold:
            return tier

    return CoachTier.ROOKIE


def get_tier_multiplier(tier: CoachTier) -> float:
    """Get the development multiplier for a coach tier."""
    return TIER_MULTIPLIERS.get(tier, 1.0)


def get_scheme_bonus(scheme: str, position: str) -> float:
    """
    Get the development bonus for a position under a specific scheme.

    Args:
        scheme: Offensive or defensive scheme name
        position: Player position (e.g., "QB", "WR", "CB")

    Returns:
        Bonus multiplier (e.g., 0.15 for 15% bonus)
    """
    if scheme not in SCHEME_EXPERTISE:
        return 0.0

    return SCHEME_EXPERTISE[scheme].get(position, 0.0)


def get_archetype_bonus(archetype: CoachArchetype, position: str) -> float:
    """
    Get the development bonus for a position from coach archetype.

    Args:
        archetype: Coach's archetype
        position: Player position

    Returns:
        Bonus multiplier (e.g., 0.25 for 25% bonus)
    """
    if archetype not in ARCHETYPE_BONUSES:
        return 0.0

    return ARCHETYPE_BONUSES[archetype].get(position, 0.0)


def calculate_development_bonus(
    coach_tier: CoachTier,
    offensive_scheme: str | None,
    defensive_scheme: str | None,
    archetype: CoachArchetype,
    player_position: str,
    cap_total: float = 2.0
) -> float:
    """
    Calculate the total development bonus for a player under a coach.

    Formula: tier_multiplier * (1.0 + scheme_bonus + archetype_bonus)

    Args:
        coach_tier: Coach's tier level
        offensive_scheme: Coach's offensive playbook
        defensive_scheme: Coach's defensive playbook
        archetype: Coach's archetype specialty
        player_position: Player's position
        cap_total: Maximum total multiplier (default 2.0 = 100% max bonus)

    Returns:
        Total development multiplier (e.g., 1.65 = 65% bonus)
    """
    # Base tier multiplier
    tier_mult = get_tier_multiplier(coach_tier)

    # Scheme bonuses (pick higher of offensive/defensive)
    off_bonus = get_scheme_bonus(offensive_scheme or "", player_position)
    def_bonus = get_scheme_bonus(defensive_scheme or "", player_position)
    scheme_bonus = max(off_bonus, def_bonus)

    # Archetype bonus
    arch_bonus = get_archetype_bonus(archetype, player_position)

    # Combine: tier * (1 + bonuses)
    total = tier_mult * (1.0 + scheme_bonus + arch_bonus)

    # Cap at maximum
    return min(total, cap_total)


def get_position_development_summary(
    coach_tier: CoachTier,
    offensive_scheme: str | None,
    defensive_scheme: str | None,
    archetype: CoachArchetype
) -> dict[str, float]:
    """
    Get development bonuses for all positions under this coach.

    Returns:
        Dict mapping position to development multiplier
    """
    positions = [
        "QB", "RB", "FB", "WR", "TE", "OL", "C", "G", "T",
        "DL", "DE", "DT", "NT", "EDGE",
        "LB", "ILB", "OLB", "MLB",
        "CB", "S", "FS", "SS",
        "K", "P", "LS"
    ]

    return {
        pos: calculate_development_bonus(
            coach_tier, offensive_scheme, defensive_scheme, archetype, pos
        )
        for pos in positions
    }


# ============================================================================
# NOTABLE COACH PROFILES (Examples)
# ============================================================================

NOTABLE_COACHES = {
    "Andy Reid": {
        "tier": CoachTier.LEGEND,
        "archetype": CoachArchetype.QB_GURU,
        "offensive_scheme": "West Coast",
        "notes": "Developed Mahomes, McNabb, Vick"
    },
    "Bill Belichick": {
        "tier": CoachTier.LEGEND,
        "archetype": CoachArchetype.GENERALIST,
        "defensive_scheme": "Multiple",
        "notes": "GOAT defensive mind, develops all positions"
    },
    "Sean McVay": {
        "tier": CoachTier.ELITE,
        "archetype": CoachArchetype.RECEIVING_COACH,
        "offensive_scheme": "West Coast",
        "notes": "Innovative play-caller, WR development"
    },
    "Kyle Shanahan": {
        "tier": CoachTier.ELITE,
        "archetype": CoachArchetype.RUN_GAME_SPECIALIST,
        "offensive_scheme": "Zone Run",
        "notes": "Zone running scheme master"
    },
}

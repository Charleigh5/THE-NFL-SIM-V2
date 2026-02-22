"""
RPG Abilities System - Phase 11: True-to-Life RPG

Abilities are distinct from Traits:
- Traits: Earned through stats/progression, always passive
- Abilities: Purchased with XP at level thresholds, active mechanics

This module defines the Ability catalog and status tracking.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AbilityStatus(str, Enum):
    """Status of an ability for a player."""

    LOCKED = "LOCKED"  # Requirements not met
    AVAILABLE = "AVAILABLE"  # Requirements met, not purchased
    UNLOCKED = "UNLOCKED"  # Purchased and active


@dataclass
class AbilityDefinition:
    """
    Defines an unlockable ability's properties, requirements, and effects.
    """

    name: str
    description: str
    position_requirements: list[str]
    level_requirement: int
    xp_cost: int
    effects: dict[str, float]

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "name": self.name,
            "description": self.description,
            "position_requirements": self.position_requirements,
            "level_requirement": self.level_requirement,
            "xp_cost": self.xp_cost,
            "effects": self.effects,
        }


# =============================================================================
# ABILITY CATALOG
# =============================================================================

ABILITY_CATALOG: dict[str, AbilityDefinition] = {
    # -------------------------------------------------------------------------
    # QB ABILITIES
    # -------------------------------------------------------------------------
    "pre_snap_diagnostician": AbilityDefinition(
        name="Pre-Snap Diagnostician",
        description="Reveals defensive coverage shell (Man/Zone) pre-snap with confidence based on QB Awareness vs DC Disguise rating. Higher awareness = more accurate reads.",
        position_requirements=["QB"],
        level_requirement=10,
        xp_cost=5000,
        effects={
            "awareness_boost": 15,  # Bonus awareness for read calculation
            "pre_snap_read_accuracy": 0.90,  # Base 90% accuracy (modified by matchup)
            "audible_time_reduction": 2.0,  # Seconds saved on audibles
        },
    ),
    "audible_master": AbilityDefinition(
        name="Audible Master",
        description="Reduces audible time from 8 seconds to 2 seconds. Eliminates False Start risk when audibling. Can hot-route 2 receivers instead of 1.",
        position_requirements=["QB"],
        level_requirement=8,
        xp_cost=3000,
        effects={
            "audible_time": 2.0,  # Seconds (vs normal 8s)
            "false_start_immunity": 1.0,  # Boolean: OL won't false start on audibles
            "hot_route_count": 2,  # Can hot route 2 receivers
        },
    ),
    "red_zone_assassin": AbilityDefinition(
        name="Red Zone Assassin",
        description="Elite performance inside the 20 yard line. TD rate increases, interception risk decreases.",
        position_requirements=["QB"],
        level_requirement=12,
        xp_cost=6000,
        effects={
            "red_zone_accuracy_boost": 10,
            "red_zone_td_chance_boost": 0.15,
            "red_zone_int_reduction": 0.20,
        },
    ),
    # -------------------------------------------------------------------------
    # RB ABILITIES
    # -------------------------------------------------------------------------
    "vision_master": AbilityDefinition(
        name="Vision Master",
        description="See the hole before it opens. Enhanced ability to find running lanes and avoid tacklers in the backfield.",
        position_requirements=["RB"],
        level_requirement=8,
        xp_cost=3500,
        effects={
            "vision_boost": 15,
            "pre_snap_hole_detection": 1.0,  # Boolean: Can see blocking assignments
            "backfield_evasion_boost": 0.20,
        },
    ),
    # -------------------------------------------------------------------------
    # WR ABILITIES
    # -------------------------------------------------------------------------
    "route_tree_genius": AbilityDefinition(
        name="Route Tree Genius",
        description="Mastery of the entire route tree. Can adjust routes on the fly based on coverage.",
        position_requirements=["WR", "TE"],
        level_requirement=10,
        xp_cost=4500,
        effects={
            "route_running_boost": 10,
            "route_adjustment": 1.0,  # Boolean: Can adjust mid-route
            "option_route_success": 0.25,  # 25% better on option routes
        },
    ),
    # -------------------------------------------------------------------------
    # DEFENSIVE ABILITIES
    # -------------------------------------------------------------------------
    "film_junkie": AbilityDefinition(
        name="Film Junkie",
        description="Study pays off. Can predict play type (run/pass) pre-snap based on formation.",
        position_requirements=["LB", "S", "CB"],
        level_requirement=8,
        xp_cost=3000,
        effects={
            "play_prediction_accuracy": 0.75,  # 75% accurate run/pass prediction
            "play_recognition_boost": 10,
            "reaction_time_boost": 0.10,
        },
    ),
    "coverage_chameleon": AbilityDefinition(
        name="Coverage Chameleon",
        description="Master of disguise. Can effectively play both man and zone coverage.",
        position_requirements=["CB", "S"],
        level_requirement=10,
        xp_cost=5000,
        effects={
            "man_coverage_boost": 8,
            "zone_coverage_boost": 8,
            "coverage_switch_reaction": 0.15,  # Faster transition between coverages
        },
    ),
}


# =============================================================================
# ABILITY HELPER FUNCTIONS
# =============================================================================


def get_ability_definition(ability_key: str) -> AbilityDefinition | None:
    """Get an ability definition by its key."""
    return ABILITY_CATALOG.get(ability_key)


def get_ability_by_name(name: str) -> AbilityDefinition | None:
    """Get an ability definition by its display name."""
    for ability_def in ABILITY_CATALOG.values():
        if ability_def.name == name:
            return ability_def
    return None


def get_abilities_for_position(position: str) -> list[AbilityDefinition]:
    """Get all abilities available for a specific position."""
    return [
        ability
        for ability in ABILITY_CATALOG.values()
        if position in ability.position_requirements or "ALL" in ability.position_requirements
    ]


def check_ability_eligibility(
    player_level: int, player_xp: int, player_position: str, ability_key: str
) -> tuple[bool, str, AbilityStatus]:
    """
    Check if a player is eligible to unlock a specific ability.

    Returns:
        (is_eligible, reason, status)
    """
    ability_def = get_ability_definition(ability_key)

    if not ability_def:
        return False, f"Unknown ability: {ability_key}", AbilityStatus.LOCKED

    # Check position requirement
    if "ALL" not in ability_def.position_requirements:
        if player_position not in ability_def.position_requirements:
            return (
                False,
                f"Position {player_position} cannot unlock {ability_def.name}",
                AbilityStatus.LOCKED,
            )

    # Check level requirement
    if player_level < ability_def.level_requirement:
        return (
            False,
            f"Requires Level {ability_def.level_requirement} (currently {player_level})",
            AbilityStatus.LOCKED,
        )

    # Check XP cost
    if player_xp < ability_def.xp_cost:
        return (
            False,
            f"Requires {ability_def.xp_cost} XP (currently {player_xp})",
            AbilityStatus.AVAILABLE,
        )

    return True, "Eligible to unlock", AbilityStatus.AVAILABLE

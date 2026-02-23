#!/usr/bin/env python3
"""
Position-Specific Drill Catalog (B-011)
=======================================
Defines 50+ position-specific drills with detailed attributes.

Phase 7: Advanced Training System
- Position-specific drill definitions
- Target stat mappings
- Injury risk and XP multipliers
- Seasonal availability
"""

from enum import Enum

from pydantic import BaseModel, Field

# ============================================================================
# ENUMS
# ============================================================================


class SeasonPhase(str, Enum):
    """When a drill is available."""

    OFFSEASON = "offseason"
    PRESEASON = "preseason"
    REGULAR = "regular"


class DrillCategory(str, Enum):
    """Categories of drills."""

    STRENGTH = "STRENGTH"
    SPEED = "SPEED"
    TECHNIQUE = "TECHNIQUE"
    MENTAL = "MENTAL"
    ENDURANCE = "ENDURANCE"
    RECOVERY = "RECOVERY"


# ============================================================================
# PYDANTIC MODELS (B-012)
# ============================================================================


class Drill(BaseModel):
    """
    Definition of a training drill (B-012).

    Follows UMAP principles: each drill has clear inputs and outputs.
    """

    name: str = Field(..., description="Display name of the drill")
    target_stat: str = Field(..., description="Primary stat improved by this drill")
    secondary_stats: list[str] = Field(
        default_factory=list, description="Additional stats affected"
    )
    injury_risk: float = Field(ge=0.0, le=1.0, default=0.05, description="Base injury risk (0-1)")
    season_filter: list[SeasonPhase] = Field(
        default_factory=lambda: [SeasonPhase.OFFSEASON, SeasonPhase.PRESEASON, SeasonPhase.REGULAR]
    )
    xp_multiplier: float = Field(default=1.0, ge=0.1, le=3.0, description="XP gain multiplier")
    fatigue_cost: float = Field(
        default=10.0, ge=0.0, le=50.0, description="Fatigue added per session"
    )
    category: DrillCategory = Field(default=DrillCategory.TECHNIQUE)
    description: str = Field(default="", description="Detailed description for UI")

    class Config:
        use_enum_values = True


# ============================================================================
# QB DRILLS (B-013)
# ============================================================================

QB_DRILLS = [
    Drill(
        name="Footwork Mechanics",
        target_stat="throw_on_run",
        secondary_stats=["throw_accuracy_short"],
        injury_risk=0.02,
        xp_multiplier=1.2,
        fatigue_cost=8.0,
        category=DrillCategory.TECHNIQUE,
        season_filter=[SeasonPhase.OFFSEASON, SeasonPhase.PRESEASON],
        description="Ladder drills and drop-back mechanics to improve throwing platform.",
    ),
    Drill(
        name="Weighted Ball Throws",
        target_stat="throw_power",
        secondary_stats=["throw_accuracy_deep"],
        injury_risk=0.15,
        xp_multiplier=1.5,
        fatigue_cost=15.0,
        category=DrillCategory.STRENGTH,
        season_filter=[SeasonPhase.OFFSEASON],
        description="Overweighted football throws to build arm strength. High injury risk.",
    ),
    Drill(
        name="7-on-7 Passing",
        target_stat="throw_accuracy_mid",
        secondary_stats=["throw_accuracy_short", "play_action"],
        injury_risk=0.03,
        xp_multiplier=1.3,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Live passing drills against coverage without pass rush.",
    ),
    Drill(
        name="Film Study - Defenses",
        target_stat="play_recognition",
        secondary_stats=["awareness"],
        injury_risk=0.0,
        xp_multiplier=0.8,
        fatigue_cost=0.0,
        category=DrillCategory.MENTAL,
        description="Study opponent defensive schemes and tendencies.",
    ),
    Drill(
        name="Arm Care Program",
        target_stat="injury_resistance",
        secondary_stats=["stamina"],
        injury_risk=0.01,
        xp_multiplier=0.5,
        fatigue_cost=5.0,
        category=DrillCategory.RECOVERY,
        description="Low-intensity arm maintenance and stretching routine.",
    ),
    Drill(
        name="Pocket Presence Drill",
        target_stat="pocket_presence",
        secondary_stats=["break_sack"],
        injury_risk=0.04,
        xp_multiplier=1.4,
        fatigue_cost=15.0,
        category=DrillCategory.TECHNIQUE,
        description="Simulated pressure to improve pocket movement and awareness.",
    ),
    Drill(
        name="Two-Minute Drill",
        target_stat="clutch",
        secondary_stats=["throw_accuracy_short", "awareness"],
        injury_risk=0.05,
        xp_multiplier=1.6,
        fatigue_cost=20.0,
        category=DrillCategory.MENTAL,
        description="High-pressure clock management and quick decision making.",
    ),
]


# ============================================================================
# RB DRILLS (B-014)
# ============================================================================

RB_DRILLS = [
    Drill(
        name="Cone Agility",
        target_stat="agility",
        secondary_stats=["change_of_direction", "acceleration"],
        injury_risk=0.03,
        xp_multiplier=1.2,
        fatigue_cost=12.0,
        category=DrillCategory.SPEED,
        description="5-10-5 shuttle and cone drills for lateral quickness.",
    ),
    Drill(
        name="Sled Push",
        target_stat="trucking",
        secondary_stats=["strength", "break_tackle"],
        injury_risk=0.08,
        xp_multiplier=1.4,
        fatigue_cost=18.0,
        category=DrillCategory.STRENGTH,
        season_filter=[SeasonPhase.OFFSEASON, SeasonPhase.PRESEASON],
        description="Heavy sled work to build power at contact.",
    ),
    Drill(
        name="Ball Security Gauntlet",
        target_stat="ball_carrier_vision",
        secondary_stats=["carrying"],
        injury_risk=0.02,
        xp_multiplier=1.1,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Multiple defenders attempting to strip the ball while running.",
    ),
    Drill(
        name="Vision Drills",
        target_stat="ball_carrier_vision",
        secondary_stats=["awareness"],
        injury_risk=0.01,
        xp_multiplier=1.0,
        fatigue_cost=8.0,
        category=DrillCategory.MENTAL,
        description="Read holes and make cuts based on blocking alignments.",
    ),
    Drill(
        name="Zone Blocking Reads",
        target_stat="awareness",
        secondary_stats=["ball_carrier_vision", "acceleration"],
        injury_risk=0.04,
        xp_multiplier=1.3,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Reading zone blocks and making appropriate cuts.",
    ),
    Drill(
        name="Pass Protection",
        target_stat="pass_block",
        secondary_stats=["awareness"],
        injury_risk=0.06,
        xp_multiplier=1.2,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Blocking blitzing linebackers and picking up assignments.",
    ),
    Drill(
        name="Route Running - RB",
        target_stat="route_running",
        secondary_stats=["catching", "release"],
        injury_risk=0.02,
        xp_multiplier=1.1,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Swing routes, wheel routes, and option routes from backfield.",
    ),
]


# ============================================================================
# WR DRILLS (B-015)
# ============================================================================

WR_DRILLS = [
    Drill(
        name="Route Tree Mastery",
        target_stat="route_running",
        secondary_stats=["release", "short_route_running"],
        injury_risk=0.02,
        xp_multiplier=1.3,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Full route tree execution against air and coverage.",
    ),
    Drill(
        name="Contested Catch Drills",
        target_stat="spectacular_catch",
        secondary_stats=["catching", "catch_in_traffic"],
        injury_risk=0.05,
        xp_multiplier=1.4,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Jump ball and contested situations against DBs.",
    ),
    Drill(
        name="Timing Routes",
        target_stat="medium_route_running",
        secondary_stats=["catching", "awareness"],
        injury_risk=0.03,
        xp_multiplier=1.2,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Timing-based routes: slants, hitches, comebacks.",
    ),
    Drill(
        name="Release vs Press",
        target_stat="release",
        secondary_stats=["route_running"],
        injury_risk=0.04,
        xp_multiplier=1.3,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Getting off the line against press coverage.",
    ),
    Drill(
        name="Deep Ball Tracking",
        target_stat="deep_route_running",
        secondary_stats=["speed", "catching"],
        injury_risk=0.03,
        xp_multiplier=1.5,
        fatigue_cost=15.0,
        category=DrillCategory.TECHNIQUE,
        description="Tracking deep balls over the shoulder.",
    ),
    Drill(
        name="YAC Drills",
        target_stat="juke_move",
        secondary_stats=["spin_move", "stiff_arm"],
        injury_risk=0.04,
        xp_multiplier=1.2,
        fatigue_cost=14.0,
        category=DrillCategory.SPEED,
        description="Making defenders miss after the catch.",
    ),
    Drill(
        name="Hand Fighting",
        target_stat="release",
        secondary_stats=["strength"],
        injury_risk=0.06,
        xp_multiplier=1.1,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Using hands to create separation at the line and in routes.",
    ),
]


# ============================================================================
# OL DRILLS (B-016)
# ============================================================================

OL_DRILLS = [
    Drill(
        name="Pass Protection Sets",
        target_stat="pass_block",
        secondary_stats=["pass_block_power", "pass_block_finesse"],
        injury_risk=0.04,
        xp_multiplier=1.3,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Kick slides and anchor drills against rushers.",
    ),
    Drill(
        name="Run Blocking - Drive",
        target_stat="run_block",
        secondary_stats=["run_block_power"],
        injury_risk=0.06,
        xp_multiplier=1.4,
        fatigue_cost=18.0,
        category=DrillCategory.STRENGTH,
        description="Driving defenders off the line with power.",
    ),
    Drill(
        name="Pull and Lead",
        target_stat="run_block_finesse",
        secondary_stats=["agility", "acceleration"],
        injury_risk=0.05,
        xp_multiplier=1.2,
        fatigue_cost=15.0,
        category=DrillCategory.TECHNIQUE,
        description="Pulling across the formation and leading through holes.",
    ),
    Drill(
        name="Combo Blocks",
        target_stat="awareness",
        secondary_stats=["run_block", "pass_block"],
        injury_risk=0.04,
        xp_multiplier=1.3,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Double teams transitioning to linebacker blocks.",
    ),
    Drill(
        name="Anchor Drill",
        target_stat="pass_block_power",
        secondary_stats=["strength"],
        injury_risk=0.08,
        xp_multiplier=1.5,
        fatigue_cost=20.0,
        category=DrillCategory.STRENGTH,
        season_filter=[SeasonPhase.OFFSEASON, SeasonPhase.PRESEASON],
        description="Absorbing bull rushes without giving ground.",
    ),
    Drill(
        name="Hand Placement",
        target_stat="pass_block_finesse",
        secondary_stats=["technique"],
        injury_risk=0.02,
        xp_multiplier=1.1,
        fatigue_cost=8.0,
        category=DrillCategory.TECHNIQUE,
        description="Proper strike timing and placement in pass sets.",
    ),
    Drill(
        name="Communication Drills",
        target_stat="awareness",
        secondary_stats=["play_recognition"],
        injury_risk=0.0,
        xp_multiplier=0.8,
        fatigue_cost=5.0,
        category=DrillCategory.MENTAL,
        description="Calling out protections and reading blitz packages.",
    ),
]


# ============================================================================
# DL DRILLS (B-017)
# ============================================================================

DL_DRILLS = [
    Drill(
        name="Pass Rush Moves",
        target_stat="finesse_moves",
        secondary_stats=["power_moves", "acceleration"],
        injury_risk=0.05,
        xp_multiplier=1.4,
        fatigue_cost=16.0,
        category=DrillCategory.TECHNIQUE,
        description="Speed rush, bull rush, and counter moves.",
    ),
    Drill(
        name="Gap Control",
        target_stat="block_shedding",
        secondary_stats=["tackling", "strength"],
        injury_risk=0.06,
        xp_multiplier=1.3,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Maintaining gap integrity in run defense.",
    ),
    Drill(
        name="Get-Off Drills",
        target_stat="acceleration",
        secondary_stats=["speed"],
        injury_risk=0.03,
        xp_multiplier=1.2,
        fatigue_cost=12.0,
        category=DrillCategory.SPEED,
        description="First step explosiveness off the snap.",
    ),
    Drill(
        name="Hand Combat",
        target_stat="power_moves",
        secondary_stats=["finesse_moves", "strength"],
        injury_risk=0.07,
        xp_multiplier=1.4,
        fatigue_cost=15.0,
        category=DrillCategory.TECHNIQUE,
        description="Hand fighting and disengaging from blocks.",
    ),
    Drill(
        name="Pursuit Angles",
        target_stat="pursuit",
        secondary_stats=["speed", "awareness"],
        injury_risk=0.02,
        xp_multiplier=1.0,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Taking proper angles in run pursuit.",
    ),
    Drill(
        name="Bull Rush Power",
        target_stat="power_moves",
        secondary_stats=["strength", "trucking"],
        injury_risk=0.10,
        xp_multiplier=1.6,
        fatigue_cost=22.0,
        category=DrillCategory.STRENGTH,
        season_filter=[SeasonPhase.OFFSEASON],
        description="High-intensity power rushing. Very high injury risk.",
    ),
]


# ============================================================================
# DB DRILLS (B-018)
# ============================================================================

DB_DRILLS = [
    Drill(
        name="Backpedal Technique",
        target_stat="man_coverage",
        secondary_stats=["speed", "agility"],
        injury_risk=0.03,
        xp_multiplier=1.2,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Smooth backpedaling while reading receiver routes.",
    ),
    Drill(
        name="Ball Tracking",
        target_stat="play_ball",
        secondary_stats=["catching", "awareness"],
        injury_risk=0.02,
        xp_multiplier=1.3,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Locating and high-pointing the ball.",
    ),
    Drill(
        name="Press Coverage",
        target_stat="press",
        secondary_stats=["man_coverage", "strength"],
        injury_risk=0.05,
        xp_multiplier=1.4,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Jamming receivers at the line of scrimmage.",
    ),
    Drill(
        name="Zone Coverage Drops",
        target_stat="zone_coverage",
        secondary_stats=["awareness", "play_recognition"],
        injury_risk=0.01,
        xp_multiplier=1.1,
        fatigue_cost=8.0,
        category=DrillCategory.TECHNIQUE,
        description="Zone drops and reading quarterback eyes.",
    ),
    Drill(
        name="Tackling - Open Field",
        target_stat="tackling",
        secondary_stats=["pursuit"],
        injury_risk=0.08,
        xp_multiplier=1.3,
        fatigue_cost=16.0,
        category=DrillCategory.TECHNIQUE,
        description="Breaking down and tackling in space.",
    ),
    Drill(
        name="Hip Turn Drill",
        target_stat="agility",
        secondary_stats=["speed", "man_coverage"],
        injury_risk=0.04,
        xp_multiplier=1.2,
        fatigue_cost=10.0,
        category=DrillCategory.SPEED,
        description="Opening hips and flipping when receivers break.",
    ),
]


# ============================================================================
# LB DRILLS (B-019)
# ============================================================================

LB_DRILLS = [
    Drill(
        name="Coverage Drops",
        target_stat="zone_coverage",
        secondary_stats=["man_coverage", "speed"],
        injury_risk=0.02,
        xp_multiplier=1.2,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Hook, curl, and flat zone responsibilities.",
    ),
    Drill(
        name="Blitz Timing",
        target_stat="acceleration",
        secondary_stats=["finesse_moves", "pursuit"],
        injury_risk=0.05,
        xp_multiplier=1.4,
        fatigue_cost=15.0,
        category=DrillCategory.TECHNIQUE,
        description="Firing through gaps at the snap.",
    ),
    Drill(
        name="Shed and Tackle",
        target_stat="block_shedding",
        secondary_stats=["tackling", "strength"],
        injury_risk=0.06,
        xp_multiplier=1.3,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Getting off blocks and making tackles in the hole.",
    ),
    Drill(
        name="Read and React",
        target_stat="play_recognition",
        secondary_stats=["awareness", "pursuit"],
        injury_risk=0.01,
        xp_multiplier=1.0,
        fatigue_cost=8.0,
        category=DrillCategory.MENTAL,
        description="Reading keys and reacting to run vs pass.",
    ),
    Drill(
        name="Man Coverage - RB/TE",
        target_stat="man_coverage",
        secondary_stats=["speed", "zone_coverage"],
        injury_risk=0.03,
        xp_multiplier=1.3,
        fatigue_cost=12.0,
        category=DrillCategory.TECHNIQUE,
        description="Covering backs and tight ends in isolation.",
    ),
    Drill(
        name="Downhill Run Fits",
        target_stat="tackling",
        secondary_stats=["block_shedding", "strength"],
        injury_risk=0.08,
        xp_multiplier=1.5,
        fatigue_cost=18.0,
        category=DrillCategory.STRENGTH,
        description="Filling gaps and making tackles at the line.",
    ),
]


# ============================================================================
# SPECIAL TEAMS DRILLS (B-020)
# ============================================================================

ST_DRILLS = [
    Drill(
        name="Kickoff Coverage",
        target_stat="speed",
        secondary_stats=["tackling", "pursuit"],
        injury_risk=0.10,
        xp_multiplier=1.2,
        fatigue_cost=18.0,
        category=DrillCategory.SPEED,
        description="Full-speed coverage drills. High injury risk.",
    ),
    Drill(
        name="Punt Protection",
        target_stat="awareness",
        secondary_stats=["pass_block"],
        injury_risk=0.04,
        xp_multiplier=1.0,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Blocking for punt protection.",
    ),
    Drill(
        name="Return Blocking",
        target_stat="run_block",
        secondary_stats=["awareness"],
        injury_risk=0.06,
        xp_multiplier=1.1,
        fatigue_cost=14.0,
        category=DrillCategory.TECHNIQUE,
        description="Setting up return lanes and blocking in space.",
    ),
    Drill(
        name="Field Goal Timing",
        target_stat="kick_accuracy",
        secondary_stats=["kick_power"],
        injury_risk=0.02,
        xp_multiplier=1.3,
        fatigue_cost=8.0,
        category=DrillCategory.TECHNIQUE,
        description="Snap-hold-kick timing and mechanics.",
    ),
    Drill(
        name="Leg Strength - Kickers",
        target_stat="kick_power",
        secondary_stats=["stamina"],
        injury_risk=0.08,
        xp_multiplier=1.4,
        fatigue_cost=15.0,
        category=DrillCategory.STRENGTH,
        season_filter=[SeasonPhase.OFFSEASON],
        description="Heavy leg work for kick distance.",
    ),
    Drill(
        name="Punt Hang Time",
        target_stat="kick_power",
        secondary_stats=["kick_accuracy"],
        injury_risk=0.03,
        xp_multiplier=1.2,
        fatigue_cost=10.0,
        category=DrillCategory.TECHNIQUE,
        description="Maximizing hang time for coverage.",
    ),
]


# ============================================================================
# MASTER CATALOG
# ============================================================================

POSITION_DRILL_MAP = {
    "QB": QB_DRILLS,
    "RB": RB_DRILLS,
    "FB": RB_DRILLS,  # Fullbacks use RB drills
    "WR": WR_DRILLS,
    "TE": WR_DRILLS + OL_DRILLS[:2],  # TEs do receiving and some blocking
    "LT": OL_DRILLS,
    "LG": OL_DRILLS,
    "C": OL_DRILLS,
    "RG": OL_DRILLS,
    "RT": OL_DRILLS,
    "LE": DL_DRILLS,
    "RE": DL_DRILLS,
    "DT": DL_DRILLS,
    "LOLB": LB_DRILLS,
    "MLB": LB_DRILLS,
    "ROLB": LB_DRILLS,
    "CB": DB_DRILLS,
    "FS": DB_DRILLS,
    "SS": DB_DRILLS,
    "K": ST_DRILLS[-3:],  # Kicker-specific
    "P": ST_DRILLS[-2:],  # Punter-specific
}

# All drills combined for catalog access
ALL_DRILLS = (
    QB_DRILLS + RB_DRILLS + WR_DRILLS + OL_DRILLS + DL_DRILLS + DB_DRILLS + LB_DRILLS + ST_DRILLS
)


def get_drills_for_position(position: str) -> list[Drill]:
    """
    Get available drills for a specific position.

    Args:
        position: Player position code (e.g., 'QB', 'WR', 'MLB')

    Returns:
        List of Drill objects available for that position
    """
    return POSITION_DRILL_MAP.get(position.upper(), [])


def get_drills_for_season(drills: list[Drill], phase: SeasonPhase) -> list[Drill]:
    """
    Filter drills available in a specific season phase.

    Args:
        drills: List of drills to filter
        phase: Current season phase

    Returns:
        Drills available in that phase
    """
    return [d for d in drills if phase in d.season_filter]


def get_drills_by_category(drills: list[Drill], category: DrillCategory) -> list[Drill]:
    """
    Filter drills by category.

    Args:
        drills: List of drills to filter
        category: Drill category to filter by

    Returns:
        Drills in that category
    """
    return [d for d in drills if d.category == category]


# Count validation
assert len(ALL_DRILLS) >= 50, f"Expected 50+ drills, got {len(ALL_DRILLS)}"

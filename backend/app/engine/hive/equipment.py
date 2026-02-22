#!/usr/bin/env python3
"""
Equipment Physics Module
========================
Player equipment effects on performance.

Phase 4: HIVE Environment Physics
- Cleat types and grip
- Glove effects on catching
- Equipment trade-offs
- Weather interaction
"""

from dataclasses import dataclass
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class CleatType(str, Enum):
    """Types of football cleats."""

    MOLDED = "MOLDED"  # Standard, all-around
    DETACHABLE = "DETACHABLE"  # Customizable studs
    TURF = "TURF"  # Short rubber studs
    LOW_CUT = "LOW_CUT"  # Speed focused
    MID_CUT = "MID_CUT"  # Balanced
    HIGH_CUT = "HIGH_CUT"  # Ankle support


class GloveType(str, Enum):
    """Types of receiver gloves."""

    STANDARD = "STANDARD"
    HIGH_GRIP = "HIGH_GRIP"
    ALL_WEATHER = "ALL_WEATHER"
    LINEMAN = "LINEMAN"
    NONE = "NONE"


class HelmetType(str, Enum):
    """Helmet protection levels."""

    STANDARD = "STANDARD"
    ENHANCED = "ENHANCED"
    REVOLUTION = "REVOLUTION"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass(frozen=True)
class EquipmentConfig:
    """Configuration for equipment physics."""

    # Cleat grip modifiers
    molded_grip: float = 1.0
    detachable_grip: float = 1.1
    turf_grip: float = 0.85

    # Cleat agility modifiers
    low_cut_agility: float = 1.05
    mid_cut_agility: float = 1.0
    high_cut_agility: float = 0.95

    # Glove catching modifiers
    standard_catch: float = 1.05
    high_grip_catch: float = 1.15
    all_weather_catch: float = 1.08
    no_glove_catch: float = 0.95

    # Helmet injury reduction
    standard_head_protection: float = 0.0
    enhanced_head_protection: float = 0.1
    revolution_head_protection: float = 0.15


@dataclass
class PlayerEquipment:
    """Equipment loadout for a player."""

    cleat_type: CleatType = CleatType.MOLDED
    cleat_cut: str = "MID"  # LOW, MID, HIGH
    glove_type: GloveType = GloveType.STANDARD
    helmet_type: HelmetType = HelmetType.STANDARD

    # Optional gear
    visor: bool = False
    arm_sleeve: bool = False
    hand_warmer: bool = False


# ============================================================================
# EQUIPMENT PHYSICS ENGINE
# ============================================================================


class EquipmentPhysics:
    """
    Calculate equipment effects on player performance.

    Trade-offs:
    - High grip cleats = better traction, higher injury risk
    - Low cut cleats = better agility, less ankle support
    - High grip gloves = better catching, worse in wet weather
    """

    def __init__(self, config: EquipmentConfig | None = None):
        self.config = config or EquipmentConfig()

    def get_grip_modifier(
        self,
        equipment: PlayerEquipment,
        turf_friction: float = 1.0,
        weather: str = "DRY",
    ) -> float:
        """
        Calculate total grip modifier from cleats.

        Returns modifier (1.0 = normal).
        """
        # Base from cleat type
        type_mods = {
            CleatType.MOLDED: self.config.molded_grip,
            CleatType.DETACHABLE: self.config.detachable_grip,
            CleatType.TURF: self.config.turf_grip,
            CleatType.LOW_CUT: self.config.molded_grip,
            CleatType.MID_CUT: self.config.molded_grip,
            CleatType.HIGH_CUT: self.config.molded_grip * 0.98,
        }
        base_grip = type_mods.get(equipment.cleat_type, 1.0)

        # Weather penalty
        weather_mods = {
            "DRY": 1.0,
            "WET": 0.85,
            "MUDDY": 0.7,
            "FROZEN": 0.6,
            "SNOW_COVERED": 0.65,
        }
        weather_mod = weather_mods.get(weather, 1.0)

        # Detachable cleats perform better in bad weather
        if equipment.cleat_type == CleatType.DETACHABLE and weather != "DRY":
            weather_mod += 0.1

        # Turf cleats struggle outdoors in weather
        if equipment.cleat_type == CleatType.TURF and weather != "DRY":
            weather_mod -= 0.1

        return base_grip * turf_friction * weather_mod

    def get_agility_modifier(self, equipment: PlayerEquipment) -> float:
        """
        Calculate agility modifier from cleat cut.

        Lower cut = more agility, less protection.
        """
        cut_mods = {
            "LOW": self.config.low_cut_agility,
            "MID": self.config.mid_cut_agility,
            "HIGH": self.config.high_cut_agility,
        }
        return cut_mods.get(equipment.cleat_cut, 1.0)

    def get_ankle_injury_modifier(self, equipment: PlayerEquipment) -> float:
        """
        Calculate ankle injury risk modifier.

        Higher cut = more protection = lower modifier.
        """
        cut_mods = {
            "LOW": 1.3,  # Higher ankle injury risk
            "MID": 1.0,  # Normal
            "HIGH": 0.75,  # Protected
        }
        return cut_mods.get(equipment.cleat_cut, 1.0)

    def get_catching_modifier(
        self,
        equipment: PlayerEquipment,
        weather: str = "DRY",
    ) -> float:
        """
        Calculate catching modifier from gloves.

        High grip gloves help in dry but hurt in wet.
        """
        # Base from glove type
        type_mods = {
            GloveType.STANDARD: self.config.standard_catch,
            GloveType.HIGH_GRIP: self.config.high_grip_catch,
            GloveType.ALL_WEATHER: self.config.all_weather_catch,
            GloveType.LINEMAN: 0.95,
            GloveType.NONE: self.config.no_glove_catch,
        }
        base = type_mods.get(equipment.glove_type, 1.0)

        # Weather interaction
        if weather in ["WET", "MUDDY", "SNOW_COVERED"]:
            if equipment.glove_type == GloveType.HIGH_GRIP:
                # High grip loses tackiness when wet
                base *= 0.85
            elif equipment.glove_type == GloveType.ALL_WEATHER:
                # All-weather performs better
                base *= 1.05

        # Cold weather
        if weather == "FROZEN":
            if equipment.hand_warmer:
                base *= 1.02  # Hand warmers help
            else:
                base *= 0.95  # Cold hands hurt catching

        return base

    def get_head_injury_reduction(self, equipment: PlayerEquipment) -> float:
        """
        Calculate head injury risk reduction from helmet.

        Returns reduction percentage (0.0 - 0.15).
        """
        reductions = {
            HelmetType.STANDARD: self.config.standard_head_protection,
            HelmetType.ENHANCED: self.config.enhanced_head_protection,
            HelmetType.REVOLUTION: self.config.revolution_head_protection,
        }
        return reductions.get(equipment.helmet_type, 0.0)

    def get_vision_modifier(self, equipment: PlayerEquipment) -> float:
        """
        Calculate vision modifier from visor.

        Visor can help or hurt depending on conditions.
        """
        if not equipment.visor:
            return 1.0

        # Visor provides slight advantage in sunny conditions
        # but can fog up or limit peripheral vision
        return 0.98

    def recommend_loadout(
        self,
        position_group: str,
        weather: str,
        turf_type: str,
    ) -> PlayerEquipment:
        """
        Recommend optimal equipment for conditions.

        Args:
            position_group: "skill" (WR/RB/DB) or "line" (OL/DL)
            weather: Current weather condition
            turf_type: NATURAL or ARTIFICIAL
        """
        equipment = PlayerEquipment()

        # Cleats
        if weather in ["WET", "MUDDY"]:
            equipment.cleat_type = CleatType.DETACHABLE
        elif turf_type == "ARTIFICIAL":
            equipment.cleat_type = CleatType.TURF
        else:
            equipment.cleat_type = CleatType.MOLDED

        # Cleat cut
        if position_group == "skill":
            equipment.cleat_cut = "LOW"
        else:
            equipment.cleat_cut = "MID"

        # Gloves
        if position_group == "skill":
            if weather in ["WET", "MUDDY", "SNOW_COVERED"]:
                equipment.glove_type = GloveType.ALL_WEATHER
            else:
                equipment.glove_type = GloveType.HIGH_GRIP
        else:
            equipment.glove_type = GloveType.LINEMAN

        # Accessories
        if weather == "FROZEN":
            equipment.hand_warmer = True

        return equipment

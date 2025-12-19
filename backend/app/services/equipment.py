"""
Equipment Physics System
========================
Models equipment (cleats, gloves, etc.) and their effects on player performance.

CITATION: ENHANCEMENT_REFERENCE.md - Equipment Physics Modifiers
"""

from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class CleatType(str, Enum):
    """Types of cleats with different trade-offs."""
    STANDARD = "STANDARD"           # Balanced
    HIGH_GRIP = "HIGH_GRIP"         # +Traction, -Speed
    SPEED = "SPEED"                 # +Speed, -Traction
    ANKLE_SUPPORT = "ANKLE_SUPPORT" # +Injury Prevention, -Agility


class GloveType(str, Enum):
    """Types of gloves with different trade-offs."""
    RECEIVER = "RECEIVER"      # +Catching, standard
    STICKY = "STICKY"          # +Catching in wet, -Durability
    LINEMAN = "LINEMAN"        # +Grip for blocking
    COLD_WEATHER = "COLD_WEATHER"  # Maintains grip in cold


class EquipmentModifiers(BaseModel):
    """
    Equipment configuration for a player with performance modifiers.

    All modifiers are additive percentages (-1.0 to +1.0 = -100% to +100%).
    """
    cleat_type: CleatType = CleatType.STANDARD
    glove_type: GloveType = GloveType.RECEIVER

    # Computed modifiers based on equipment choices
    speed_modifier: float = Field(default=0.0, ge=-0.15, le=0.10)
    traction_modifier: float = Field(default=0.0, ge=-0.15, le=0.15)
    catching_modifier: float = Field(default=0.0, ge=-0.10, le=0.15)
    agility_modifier: float = Field(default=0.0, ge=-0.10, le=0.10)
    injury_risk_modifier: float = Field(default=0.0, ge=-0.20, le=0.10)

    class Config:
        use_enum_values = True


# Equipment effect lookup tables
CLEAT_EFFECTS: Dict[CleatType, Dict[str, float]] = {
    CleatType.STANDARD: {
        "speed_modifier": 0.0,
        "traction_modifier": 0.0,
        "agility_modifier": 0.0,
        "injury_risk_modifier": 0.0,
    },
    CleatType.HIGH_GRIP: {
        "speed_modifier": -0.03,      # -3% speed
        "traction_modifier": 0.12,    # +12% traction
        "agility_modifier": 0.0,
        "injury_risk_modifier": -0.05,  # -5% injury risk (better footing)
    },
    CleatType.SPEED: {
        "speed_modifier": 0.05,       # +5% speed
        "traction_modifier": -0.08,   # -8% traction (slip risk)
        "agility_modifier": 0.02,     # +2% agility
        "injury_risk_modifier": 0.03,  # +3% injury risk
    },
    CleatType.ANKLE_SUPPORT: {
        "speed_modifier": -0.02,      # -2% speed
        "traction_modifier": 0.0,
        "agility_modifier": -0.05,    # -5% agility
        "injury_risk_modifier": -0.15,  # -15% injury risk (major benefit)
    },
}

GLOVE_EFFECTS: Dict[GloveType, Dict[str, float]] = {
    GloveType.RECEIVER: {
        "catching_modifier": 0.05,    # +5% catching (baseline)
    },
    GloveType.STICKY: {
        "catching_modifier": 0.10,    # +10% catching
        # Note: durability handled separately
    },
    GloveType.LINEMAN: {
        "catching_modifier": -0.05,   # -5% catching (not designed for it)
        # Blocking grip handled in OL physics
    },
    GloveType.COLD_WEATHER: {
        "catching_modifier": 0.03,    # +3% catching
        # Temperature modifier: maintains baseline in cold
    },
}


def calculate_equipment_modifiers(
    cleat_type: CleatType,
    glove_type: GloveType,
    weather_temp: Optional[float] = None,
    is_wet: bool = False,
) -> EquipmentModifiers:
    """
    Calculate combined equipment modifiers based on selections and conditions.

    Args:
        cleat_type: Type of cleats equipped
        glove_type: Type of gloves equipped
        weather_temp: Temperature in Fahrenheit (optional)
        is_wet: Whether field is wet (rain/snow)

    Returns:
        EquipmentModifiers with all calculated modifiers
    """
    modifiers = EquipmentModifiers(cleat_type=cleat_type, glove_type=glove_type)

    # Apply cleat effects
    cleat_effects = CLEAT_EFFECTS.get(cleat_type, CLEAT_EFFECTS[CleatType.STANDARD])
    modifiers.speed_modifier = cleat_effects.get("speed_modifier", 0.0)
    modifiers.traction_modifier = cleat_effects.get("traction_modifier", 0.0)
    modifiers.agility_modifier = cleat_effects.get("agility_modifier", 0.0)
    modifiers.injury_risk_modifier = cleat_effects.get("injury_risk_modifier", 0.0)

    # Apply glove effects
    glove_effects = GLOVE_EFFECTS.get(glove_type, GLOVE_EFFECTS[GloveType.RECEIVER])
    modifiers.catching_modifier = glove_effects.get("catching_modifier", 0.0)

    # Weather adjustments
    if is_wet:
        # Wet conditions reduce traction
        modifiers.traction_modifier -= 0.10

        # Sticky gloves help in wet
        if glove_type == GloveType.STICKY:
            modifiers.catching_modifier += 0.05  # Extra bonus in wet
        elif glove_type != GloveType.COLD_WEATHER:
            modifiers.catching_modifier -= 0.08  # Standard gloves suffer

    if weather_temp is not None and weather_temp < 40:
        # Cold weather penalties
        cold_severity = (40 - weather_temp) / 40  # 0.0 at 40°F, 1.0 at 0°F

        # Cold reduces catching unless using cold weather gloves
        if glove_type != GloveType.COLD_WEATHER:
            modifiers.catching_modifier -= cold_severity * 0.10

        # Cold affects traction slightly
        modifiers.traction_modifier -= cold_severity * 0.03

    return modifiers


def apply_equipment_to_player_stats(
    base_stats: Dict[str, float],
    equipment: EquipmentModifiers,
) -> Dict[str, float]:
    """
    Apply equipment modifiers to a player's base stats.

    Args:
        base_stats: Dictionary of stat name -> value
        equipment: Calculated equipment modifiers

    Returns:
        Modified stats dictionary
    """
    modified = base_stats.copy()

    # Apply modifiers to relevant stats
    stat_modifier_map = {
        "speed": equipment.speed_modifier,
        "acceleration": equipment.speed_modifier * 0.5,  # 50% effect on accel
        "agility": equipment.agility_modifier,
        "catching": equipment.catching_modifier,
        "catch_in_traffic": equipment.catching_modifier,
        "route_running": equipment.agility_modifier * 0.3,  # Minor effect
    }

    for stat_name, modifier in stat_modifier_map.items():
        if stat_name in modified:
            # Apply multiplicative modifier
            modified[stat_name] = modified[stat_name] * (1.0 + modifier)
            # Clamp to valid range
            modified[stat_name] = max(1, min(99, int(modified[stat_name])))

    return modified

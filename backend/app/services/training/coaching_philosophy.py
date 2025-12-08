#!/usr/bin/env python3
"""
Coaching Philosophy System (B-021)
==================================
Defines coaching styles and their effects on training.

Phase 7: Advanced Training System
- Coaching style definitions (B-022)
- Style trade-offs (B-023 to B-026)
- XP/Injury/Fatigue multipliers per style
"""

from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class CoachingStyleName(str, Enum):
    """Available coaching styles (B-022)."""
    VOLUME = "volume"          # B-023: High reps, moderate gains
    INTENSITY = "intensity"    # B-024: Max effort, high injury risk
    SMART = "smart"            # B-025: Analytics-driven, balanced
    OLD_SCHOOL = "old_school"  # B-026: Traditional, grit-focused


# ============================================================================
# PYDANTIC MODEL (B-022)
# ============================================================================

class CoachingStyle(BaseModel):
    """
    Coaching style configuration with trade-offs.

    Each style has multipliers that affect training outcomes.
    """
    name: CoachingStyleName = Field(..., description="Style identifier")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(default="", description="Detailed explanation")

    # Multipliers (1.0 = baseline)
    xp_multiplier: float = Field(
        default=1.0, ge=0.5, le=2.0,
        description="XP gain modifier"
    )
    injury_risk_multiplier: float = Field(
        default=1.0, ge=0.5, le=3.0,
        description="Injury risk modifier"
    )
    fatigue_multiplier: float = Field(
        default=1.0, ge=0.5, le=2.0,
        description="Fatigue accumulation modifier"
    )
    recovery_multiplier: float = Field(
        default=1.0, ge=0.5, le=2.0,
        description="Recovery rate modifier"
    )

    # Style-specific bonuses
    young_player_bonus: float = Field(
        default=0.0, ge=-0.5, le=0.5,
        description="Bonus XP for players under 26"
    )
    veteran_bonus: float = Field(
        default=0.0, ge=-0.5, le=0.5,
        description="Bonus XP for players over 30"
    )
    chemistry_effect: float = Field(
        default=0.0, ge=-0.3, le=0.3,
        description="Effect on team chemistry"
    )

    class Config:
        use_enum_values = True


# ============================================================================
# STYLE DEFINITIONS (B-023 to B-026)
# ============================================================================

VOLUME_STYLE = CoachingStyle(
    name=CoachingStyleName.VOLUME,
    display_name="Volume Training",
    description="High repetition approach. Moderate gains across the board with lower injury risk. Best for younger players who need fundamental development.",
    xp_multiplier=0.9,          # Slightly lower XP per drill
    injury_risk_multiplier=0.7,  # Much safer
    fatigue_multiplier=1.3,      # More tiring (high reps)
    recovery_multiplier=0.9,     # Slightly slower recovery
    young_player_bonus=0.15,     # Great for rookies
    veteran_bonus=-0.1,          # Veterans get less from reps
    chemistry_effect=0.05,       # Builds camaraderie
)

INTENSITY_STYLE = CoachingStyle(
    name=CoachingStyleName.INTENSITY,
    display_name="High Intensity",
    description="Maximum effort on every rep. Massive gains but significant injury risk. Best for teams with deep rosters and star players to push.",
    xp_multiplier=1.5,           # Huge XP gains
    injury_risk_multiplier=2.0,   # Double injury risk
    fatigue_multiplier=1.5,       # Very exhausting
    recovery_multiplier=0.8,      # Slower recovery
    young_player_bonus=0.0,       # Neutral for youth
    veteran_bonus=0.2,            # Pushes veterans to peak
    chemistry_effect=-0.1,        # Can cause tension
)

SMART_STYLE = CoachingStyle(
    name=CoachingStyleName.SMART,
    display_name="Smart Training",
    description="Analytics-driven approach. Targets weaknesses with optimal load management. Balanced gains with scientific injury prevention.",
    xp_multiplier=1.1,            # Slightly above baseline
    injury_risk_multiplier=0.8,   # Below average risk
    fatigue_multiplier=0.9,       # Efficient, less fatigue
    recovery_multiplier=1.2,      # Better recovery protocols
    young_player_bonus=0.1,       # Good for development
    veteran_bonus=0.1,            # Good for maintenance
    chemistry_effect=0.0,         # Neutral
)

OLD_SCHOOL_STYLE = CoachingStyle(
    name=CoachingStyleName.OLD_SCHOOL,
    display_name="Old School",
    description="Traditional, grit-focused approach. Builds mental toughness through adversity. High injury risk but develops clutch performers.",
    xp_multiplier=1.2,            # Good gains
    injury_risk_multiplier=1.5,   # Higher risk
    fatigue_multiplier=1.2,       # Moderate fatigue
    recovery_multiplier=0.85,     # 'Walk it off' mentality
    young_player_bonus=-0.1,      # Tough on rookies
    veteran_bonus=0.15,           # Vets thrive
    chemistry_effect=0.1,         # Builds brotherhood
)


# ============================================================================
# STYLE CATALOG
# ============================================================================

COACHING_STYLES = {
    CoachingStyleName.VOLUME: VOLUME_STYLE,
    CoachingStyleName.INTENSITY: INTENSITY_STYLE,
    CoachingStyleName.SMART: SMART_STYLE,
    CoachingStyleName.OLD_SCHOOL: OLD_SCHOOL_STYLE,
}


def get_coaching_style(name: str) -> CoachingStyle:
    """
    Get a coaching style by name.

    Args:
        name: Style name (case-insensitive)

    Returns:
        CoachingStyle object

    Raises:
        ValueError: If style not found
    """
    try:
        style_enum = CoachingStyleName(name.lower())
        return COACHING_STYLES[style_enum]
    except (ValueError, KeyError):
        raise ValueError(f"Unknown coaching style: {name}. Valid styles: {list(CoachingStyleName)}")


def calculate_training_modifiers(
    style: CoachingStyle,
    player_age: int,
    base_xp: float,
    base_injury_risk: float,
    base_fatigue: float
) -> dict:
    """
    Calculate final training modifiers based on coaching style and player.

    Args:
        style: Active coaching style
        player_age: Player's current age
        base_xp: Base XP from drill
        base_injury_risk: Base injury risk from drill
        base_fatigue: Base fatigue from drill

    Returns:
        Dict with modified values
    """
    # Determine age bonus
    age_bonus = 0.0
    if player_age < 26:
        age_bonus = style.young_player_bonus
    elif player_age > 30:
        age_bonus = style.veteran_bonus

    # Calculate modified values
    final_xp = base_xp * style.xp_multiplier * (1.0 + age_bonus)
    final_injury_risk = base_injury_risk * style.injury_risk_multiplier
    final_fatigue = base_fatigue * style.fatigue_multiplier

    return {
        "xp": final_xp,
        "injury_risk": min(final_injury_risk, 1.0),  # Cap at 100%
        "fatigue": final_fatigue,
        "age_bonus_applied": age_bonus,
        "style_name": style.name,
    }


# ============================================================================
# SEASONAL PERIODIZATION MODIFIERS
# ============================================================================

SEASONAL_INTENSITY_CAPS = {
    "offseason": 0.85,    # Offseason: Can go hard
    "preseason": 0.70,    # Preseason: Start managing load
    "regular": 0.50,      # Regular season: Recovery focus
    "playoffs": 0.30,     # Playoffs: Maintenance only
    "bye_week": 0.20,     # Bye: Recovery priority
}


def get_seasonal_intensity_cap(phase: str) -> float:
    """
    Get maximum recommended training intensity for a season phase.

    Args:
        phase: Current season phase

    Returns:
        Float multiplier (0.0 to 1.0) for max intensity
    """
    return SEASONAL_INTENSITY_CAPS.get(phase.lower(), 0.50)


# Export all styles for easy access
__all__ = [
    "CoachingStyle",
    "CoachingStyleName",
    "COACHING_STYLES",
    "VOLUME_STYLE",
    "INTENSITY_STYLE",
    "SMART_STYLE",
    "OLD_SCHOOL_STYLE",
    "get_coaching_style",
    "calculate_training_modifiers",
    "get_seasonal_intensity_cap",
    "SEASONAL_INTENSITY_CAPS",
]

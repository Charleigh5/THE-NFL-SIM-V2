"""
RB Tribes System - NFL Identity Blueprint Integration
======================================================
Implements the "Three Tribes" running back classification system from the
NFL Identity Blueprint. Each tribe has distinct variance profiles:

- FEAST_OR_FAMINE: High boom/bust (McCaffrey-type)
- BLUE_COLLAR: Low variance, consistent 4-yard gains (Jamaal Williams-type)
- CAUTIOUS_CARRIER: Ball security focus, late-career backs
- STANDARD: Default for players not meeting tribe thresholds
"""

from enum import Enum
from typing import Any, Optional, Dict
from dataclasses import dataclass


class RBTribe(Enum):
    """Running back archetype tribes with distinct play styles."""
    FEAST_OR_FAMINE = "Feast or Famine"
    BLUE_COLLAR = "Blue Collar"
    CAUTIOUS_CARRIER = "Cautious Carrier"
    STANDARD = "Standard"


@dataclass
class TribeProfile:
    """Variance profile for a tribe."""
    base_yards: float
    std_dev: float
    breakaway_multiplier: float
    fumble_multiplier: float
    description: str


# Tribe-specific variance profiles
TRIBE_PROFILES: Dict[RBTribe, TribeProfile] = {
    RBTribe.FEAST_OR_FAMINE: TribeProfile(
        base_yards=4.1,
        std_dev=6.0,  # High variance
        breakaway_multiplier=1.8,  # Double chance for big plays
        fumble_multiplier=1.1,  # Slightly higher fumble risk
        description="Explosive playmaker with boom-or-bust tendencies."
    ),
    RBTribe.BLUE_COLLAR: TribeProfile(
        base_yards=4.3,
        std_dev=2.0,  # Low variance, consistent
        breakaway_multiplier=0.6,  # Rare breakaways
        fumble_multiplier=0.8,  # Reliable ball carrier
        description="Consistent workhorse who moves the chains."
    ),
    RBTribe.CAUTIOUS_CARRIER: TribeProfile(
        base_yards=3.6,
        std_dev=2.5,  # Moderate variance
        breakaway_multiplier=0.4,  # Very few breakaways
        fumble_multiplier=0.6,  # Protects the ball
        description="Veteran who prioritizes ball security over explosiveness."
    ),
    RBTribe.STANDARD: TribeProfile(
        base_yards=4.2,
        std_dev=3.2,  # Default variance
        breakaway_multiplier=1.0,
        fumble_multiplier=1.0,
        description="Standard running back profile."
    ),
}


class RBTribeClassifier:
    """
    Classifies running backs into tribes based on their attributes.

    Thresholds from NFL Identity Blueprint:
    - FEAST_OR_FAMINE: Speed 90+, Elusiveness 85+
    - BLUE_COLLAR: Strength 85+, Speed 70-84 (power back)
    - CAUTIOUS_CARRIER: Age 30+, any decline in speed
    """

    # Threshold constants
    SPEED_ELITE = 90
    ELUSIVENESS_ELITE = 85
    STRENGTH_POWER = 85
    SPEED_POWER_MAX = 84
    SPEED_POWER_MIN = 70
    VETERAN_AGE = 30

    @classmethod
    def classify(cls, player: Any) -> RBTribe:
        """
        Classify a player into their RB tribe.

        Args:
            player: Player object with attributes (speed, elusiveness, strength, age)

        Returns:
            RBTribe enum value
        """
        speed = getattr(player, "speed", None) or 70
        elusiveness = getattr(player, "elusiveness", getattr(player, "agility", None)) or 70
        strength = getattr(player, "strength", None) or 70
        age = getattr(player, "age", None) or 25

        # Check for FEAST_OR_FAMINE (elite speed + elusiveness)
        if speed >= cls.SPEED_ELITE and elusiveness >= cls.ELUSIVENESS_ELITE:
            return RBTribe.FEAST_OR_FAMINE

        # Check for CAUTIOUS_CARRIER (veteran with declining athleticism)
        if age >= cls.VETERAN_AGE:
            return RBTribe.CAUTIOUS_CARRIER

        # Check for BLUE_COLLAR (power back, strong but not blazing fast)
        if strength >= cls.STRENGTH_POWER and cls.SPEED_POWER_MIN <= speed <= cls.SPEED_POWER_MAX:
            return RBTribe.BLUE_COLLAR

        # Default
        return RBTribe.STANDARD

    @classmethod
    def get_profile(cls, tribe: RBTribe) -> TribeProfile:
        """Get the variance profile for a tribe."""
        return TRIBE_PROFILES.get(tribe, TRIBE_PROFILES[RBTribe.STANDARD])

    @classmethod
    def classify_and_profile(cls, player: Any) -> tuple[RBTribe, TribeProfile]:
        """Convenience method to get both tribe and profile."""
        tribe = cls.classify(player)
        profile = cls.get_profile(tribe)
        return tribe, profile


def get_tribe_modifiers(player: Any) -> Dict[str, float]:
    """
    Get all tribe-based modifiers for a player.

    Returns:
        Dictionary with keys:
        - base_yards: Adjusted base yards for run plays
        - std_dev: Standard deviation for yards calculation
        - breakaway_mult: Multiplier for breakaway chance
        - fumble_mult: Multiplier for fumble chance
    """
    tribe, profile = RBTribeClassifier.classify_and_profile(player)

    return {
        "tribe": tribe.value,
        "base_yards": profile.base_yards,
        "std_dev": profile.std_dev,
        "breakaway_mult": profile.breakaway_multiplier,
        "fumble_mult": profile.fumble_multiplier,
        "description": profile.description
    }

"""
Archetype Effects System - NFL Identity Blueprint Integration
=============================================================
Implements game impact cascades for player archetypes from the
NFL Identity Blueprint. Each archetype has specific thresholds
and in-game effects.

Archetypes:
- FIELD_GENERAL: QB with 90+ accuracy unlocks audibles, +20% 3rd down
- TRAILER_PARK_TERMINATOR: Run Stopper + Blue Collar DNA
- SPEED_MERCHANT: WR/RB with 90+ speed, home run threat
- TRENCH_WARLORD: OL/DL with 85+ strength, dominance
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class PlayerArchetype(Enum):
    """Player archetypes with distinct game effects."""

    FIELD_GENERAL = "Field General"
    TRAILER_PARK_TERMINATOR = "Trailer Park Terminator"
    SPEED_MERCHANT = "Speed Merchant"
    TRENCH_WARLORD = "Trench Warlord"
    STANDARD = "Standard"


@dataclass
class ArchetypeThresholds:
    """Rating thresholds required to unlock an archetype."""

    required_ratings: dict[str, int]
    required_position: str | None = None
    required_dna: list[str] | None = None


@dataclass
class ArchetypeEffect:
    """Effects applied when archetype conditions are met."""

    conversion_boost: float = 0.0  # Multiplier for conversions
    breakaway_boost: float = 0.0  # Multiplier for big plays
    audible_unlock: bool = False  # Can change plays at line
    intimidation_factor: float = 1.0  # Affects opponent
    description: str = ""


# Archetype definitions with thresholds
ARCHETYPE_DEFINITIONS: dict[PlayerArchetype, ArchetypeThresholds] = {
    PlayerArchetype.FIELD_GENERAL: ArchetypeThresholds(
        required_ratings={"throw_accuracy_short": 90, "throw_accuracy_mid": 90},
        required_position="QB",
    ),
    PlayerArchetype.TRAILER_PARK_TERMINATOR: ArchetypeThresholds(
        required_ratings={"strength": 85, "tackle": 80},
        required_position="DT",
        required_dna=["Run Stopper", "Blue Collar"],
    ),
    PlayerArchetype.SPEED_MERCHANT: ArchetypeThresholds(
        required_ratings={"speed": 90, "acceleration": 88},
        required_position=None,  # WR, RB, CB
    ),
    PlayerArchetype.TRENCH_WARLORD: ArchetypeThresholds(
        required_ratings={"strength": 85, "awareness": 80},
        required_position=None,  # OL, DL positions
    ),
}

# Effects for each archetype
ARCHETYPE_EFFECTS: dict[PlayerArchetype, ArchetypeEffect] = {
    PlayerArchetype.FIELD_GENERAL: ArchetypeEffect(
        conversion_boost=0.20,  # +20% on 3rd down
        audible_unlock=True,
        description="Elite accuracy unlocks pre-snap reads and audibles.",
    ),
    PlayerArchetype.TRAILER_PARK_TERMINATOR: ArchetypeEffect(
        intimidation_factor=1.5,  # 50% more intimidating
        description="4th gen coal miner. Limited between-the-ears, unlimited motor.",
    ),
    PlayerArchetype.SPEED_MERCHANT: ArchetypeEffect(
        breakaway_boost=0.25,  # +25% breakaway chance
        description="Home run threat. Breaks free on any touch.",
    ),
    PlayerArchetype.TRENCH_WARLORD: ArchetypeEffect(
        intimidation_factor=1.3,
        conversion_boost=0.10,  # Run game boost
        description="Dominates the trenches. Pancakes for breakfast.",
    ),
    PlayerArchetype.STANDARD: ArchetypeEffect(
        description="Standard player without elite archetype traits."
    ),
}


class ArchetypeClassifier:
    """
    Classifies players into archetypes based on their attributes.
    """

    @classmethod
    def classify(cls, player: Any, dna_traits: list[str] | None = None) -> PlayerArchetype:
        """
        Classify a player into their archetype.

        Args:
            player: Player object with ratings
            dna_traits: Optional list of personality/DNA traits

        Returns:
            PlayerArchetype enum value
        """
        position = getattr(player, "position", "")
        dna = dna_traits or []

        # Check each archetype in priority order
        for archetype, thresholds in ARCHETYPE_DEFINITIONS.items():
            if cls._meets_thresholds(player, position, dna, thresholds):
                return archetype

        return PlayerArchetype.STANDARD

    @classmethod
    def _meets_thresholds(
        cls, player: Any, position: str, dna: list[str], thresholds: ArchetypeThresholds
    ) -> bool:
        """Check if player meets all thresholds for an archetype."""
        # Check position requirement
        if thresholds.required_position:
            if not position.startswith(thresholds.required_position):
                return False

        # Check rating requirements
        for rating_name, min_value in thresholds.required_ratings.items():
            player_rating = getattr(player, rating_name, 0) or 0
            if player_rating < min_value:
                return False

        # Check DNA requirements
        if thresholds.required_dna:
            for required_trait in thresholds.required_dna:
                if required_trait not in dna:
                    return False

        return True

    @classmethod
    def get_effects(cls, archetype: PlayerArchetype) -> ArchetypeEffect:
        """Get the effects for an archetype."""
        return ARCHETYPE_EFFECTS.get(archetype, ARCHETYPE_EFFECTS[PlayerArchetype.STANDARD])


class ArchetypeEffectApplicator:
    """
    Applies archetype effects during gameplay.
    """

    @classmethod
    def apply_modifiers(
        cls, player: Any, game_context: dict[str, Any], dna_traits: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Calculate and return all archetype-based modifiers for a play.

        Args:
            player: Player object
            game_context: Current game state (down, distance, etc.)
            dna_traits: Player's personality/DNA traits

        Returns:
            Dictionary with modifiers:
            - conversion_modifier: Float multiplier for conversions
            - breakaway_modifier: Float multiplier for big plays
            - has_audible: Boolean for audible capability
            - intimidation: Float factor for opponent debuff
            - narrative: String describing the effect
        """
        archetype = ArchetypeClassifier.classify(player, dna_traits)
        effects = ArchetypeClassifier.get_effects(archetype)

        result = {
            "archetype": archetype.value,
            "conversion_modifier": 1.0,
            "breakaway_modifier": 1.0,
            "has_audible": effects.audible_unlock,
            "intimidation": effects.intimidation_factor,
            "narrative": None,
        }

        # Apply 3rd down boost for Field General
        if archetype == PlayerArchetype.FIELD_GENERAL:
            if game_context.get("down") == 3:
                result["conversion_modifier"] = 1.0 + effects.conversion_boost
                result["narrative"] = (
                    f"{getattr(player, 'last_name', 'QB')} reads the defense pre-snap."
                )

        # Apply breakaway boost for Speed Merchant
        if archetype == PlayerArchetype.SPEED_MERCHANT:
            result["breakaway_modifier"] = 1.0 + effects.breakaway_boost
            if game_context.get("is_breakaway"):
                result["narrative"] = f"{getattr(player, 'last_name', 'Player')} has the jets!"

        # Apply trench boost for Trench Warlord
        if archetype == PlayerArchetype.TRENCH_WARLORD:
            if game_context.get("play_type") == "run":
                result["conversion_modifier"] = 1.0 + effects.conversion_boost

        return result


def get_archetype_modifiers(
    player: Any, game_context: dict[str, Any], dna_traits: list[str] | None = None
) -> dict[str, Any]:
    """
    Convenience function to get all archetype modifiers.

    Args:
        player: Player object
        game_context: Current game state
        dna_traits: Player's DNA/personality traits

    Returns:
        Dictionary with all modifiers and narrative
    """
    return ArchetypeEffectApplicator.apply_modifiers(player, game_context, dna_traits)

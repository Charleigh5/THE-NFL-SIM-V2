"""
Archetype Effects System - NFL Identity Blueprint Integration
=============================================================
Implements game impact cascades for player archetypes harmonized
with the 7 canonical RPG archetypes in app.rpg.player_archetypes.

Canonical 7 Archetypes:
1. FIELD_GENERAL: QB with 90+ accuracy unlocks audibles, +20% 3rd down
2. SORCERER: QB with elite arm talent and improvisation, +25% big plays
3. ALPHA_DOG: WR/CB with dominant press/coverage, +15% conversion, 1.4x intimidation
4. WEAPON: WR/RB with 90+ speed/accel, +25% breakaway chance
5. FREAK: EDGE/LB with 85+ strength/tackle, 1.5x intimidation
6. TECHNICIAN: OL/DL with 85+ strength and 80+ awareness, trench dominance
7. WORKHORSE: RB with 85+ stamina/carrying, 4th quarter wear-down dominance
"""

from enum import Enum
from typing import Any, Dict, Optional, List
from dataclasses import dataclass


class PlayerArchetype(str, Enum):
    """Player archetypes with distinct game effects harmonized with RPG archetypes."""
    FIELD_GENERAL = "Field General"
    SORCERER = "Sorcerer"
    ALPHA_DOG = "Alpha Dog"
    WEAPON = "Weapon"
    FREAK = "Freak"
    TECHNICIAN = "Technician"
    WORKHORSE = "Workhorse"
    STANDARD = "Standard"

    # Legacy aliases for backward compatibility
    TRAILER_PARK_TERMINATOR = "Freak"
    SPEED_MERCHANT = "Weapon"
    TRENCH_WARLORD = "Technician"


@dataclass
class ArchetypeThresholds:
    """Rating thresholds required to unlock an archetype."""
    required_ratings: Dict[str, int]
    allowed_positions: Optional[List[str]] = None
    required_dna: Optional[List[str]] = None


@dataclass
class ArchetypeEffect:
    """Effects applied when archetype conditions are met."""
    conversion_boost: float = 0.0  # Multiplier for conversions
    breakaway_boost: float = 0.0  # Multiplier for big plays
    audible_unlock: bool = False  # Can change plays at line
    intimidation_factor: float = 1.0  # Affects opponent
    description: str = ""


# Archetype definitions with thresholds
ARCHETYPE_DEFINITIONS: Dict[PlayerArchetype, ArchetypeThresholds] = {
    PlayerArchetype.FIELD_GENERAL: ArchetypeThresholds(
        required_ratings={"throw_accuracy_short": 90, "throw_accuracy_mid": 90},
        allowed_positions=["QB"]
    ),
    PlayerArchetype.SORCERER: ArchetypeThresholds(
        required_ratings={"throw_power": 90, "throw_accuracy_deep": 88},
        allowed_positions=["QB"]
    ),
    PlayerArchetype.ALPHA_DOG: ArchetypeThresholds(
        required_ratings={"press": 88, "man_coverage": 88},
        allowed_positions=["WR", "CB", "DB", "S"]
    ),
    PlayerArchetype.WEAPON: ArchetypeThresholds(
        required_ratings={"speed": 90, "acceleration": 88},
        allowed_positions=["WR", "RB", "TE", "CB"]
    ),
    PlayerArchetype.WORKHORSE: ArchetypeThresholds(
        required_ratings={"stamina": 85, "carrying": 85},
        allowed_positions=["RB", "FB"]
    ),
    PlayerArchetype.FREAK: ArchetypeThresholds(
        required_ratings={"strength": 85, "tackle": 80},
        allowed_positions=["EDGE", "LB", "DE", "DT", "DL"]
    ),
    PlayerArchetype.TECHNICIAN: ArchetypeThresholds(
        required_ratings={"strength": 85, "awareness": 80},
        allowed_positions=["OL", "OT", "OG", "C", "DL", "DT", "DE", "LT", "LG", "RG", "RT"]
    ),
}

# Effects for each archetype
ARCHETYPE_EFFECTS: Dict[PlayerArchetype, ArchetypeEffect] = {
    PlayerArchetype.FIELD_GENERAL: ArchetypeEffect(
        conversion_boost=0.20,  # +20% on 3rd down
        audible_unlock=True,
        description="Elite accuracy unlocks pre-snap reads and audibles."
    ),
    PlayerArchetype.SORCERER: ArchetypeEffect(
        breakaway_boost=0.25,
        audible_unlock=True,
        description="Improvisational magic and off-platform arm talent."
    ),
    PlayerArchetype.ALPHA_DOG: ArchetypeEffect(
        conversion_boost=0.15,
        intimidation_factor=1.4,
        description="Dominant competitor that demoralizes opposing coverage."
    ),
    PlayerArchetype.WEAPON: ArchetypeEffect(
        breakaway_boost=0.25,  # +25% breakaway chance
        description="Home run threat and versatile mismatch weapon."
    ),
    PlayerArchetype.FREAK: ArchetypeEffect(
        intimidation_factor=1.5,  # 50% more intimidating
        description="Physical specimen with unlimited motor and explosive disruption."
    ),
    PlayerArchetype.TECHNICIAN: ArchetypeEffect(
        intimidation_factor=1.3,
        conversion_boost=0.10,  # Run game / line boost
        description="Dominates the trenches with precise technique and zero mistakes."
    ),
    PlayerArchetype.WORKHORSE: ArchetypeEffect(
        conversion_boost=0.15,
        description="Iron man running back that punishes defenses in late-game situations."
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
    def classify(cls, player: Any, dna_traits: Optional[List[str]] = None) -> PlayerArchetype:
        """
        Classify a player into their archetype.

        Args:
            player: Player object with ratings
            dna_traits: Optional list of personality/DNA traits

        Returns:
            PlayerArchetype enum value
        """
        raw_pos = getattr(player, "position", "")
        position = str(raw_pos) if isinstance(raw_pos, str) else ""
        dna = dna_traits if isinstance(dna_traits, list) else []

        # Check each archetype in priority order
        for archetype, thresholds in ARCHETYPE_DEFINITIONS.items():
            if cls._meets_thresholds(player, position, dna, thresholds):
                return archetype

        return PlayerArchetype.STANDARD

    @classmethod
    def _meets_thresholds(
        cls,
        player: Any,
        position: str,
        dna: List[str],
        thresholds: ArchetypeThresholds
    ) -> bool:
        """Check if player meets all thresholds for an archetype."""
        # Check position requirement
        if thresholds.allowed_positions:
            if not position:
                return False
            # Check prefix / exact match
            matched_pos = any(
                position.upper().startswith(p.upper()) or p.upper().startswith(position.upper())
                for p in thresholds.allowed_positions
            )
            if not matched_pos:
                return False

        # Check rating requirements
        for rating_name, min_value in thresholds.required_ratings.items():
            val = getattr(player, rating_name, 0)
            player_rating = val if isinstance(val, (int, float)) else 0
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
        cls,
        player: Any,
        game_context: Dict[str, Any],
        dna_traits: Optional[List[str]] = None
    ) -> Dict[str, Any]:
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
            "narrative": None
        }

        # Apply 3rd down boost for Field General
        if archetype == PlayerArchetype.FIELD_GENERAL:
            if game_context.get("down") == 3:
                result["conversion_modifier"] = 1.0 + effects.conversion_boost
                result["narrative"] = f"{getattr(player, 'last_name', 'QB')} reads the defense pre-snap."

        # Apply breakaway boost for Weapon / Sorcerer
        if archetype in [PlayerArchetype.WEAPON, PlayerArchetype.SORCERER]:
            result["breakaway_modifier"] = 1.0 + effects.breakaway_boost
            if game_context.get("is_breakaway"):
                result["narrative"] = f"{getattr(player, 'last_name', 'Player')} has the jets!"

        # Apply trench boost for Technician
        if archetype == PlayerArchetype.TECHNICIAN:
            if game_context.get("play_type") == "run":
                result["conversion_modifier"] = 1.0 + effects.conversion_boost

        # Apply late-game / heavy load boost for Workhorse
        if archetype == PlayerArchetype.WORKHORSE:
            if game_context.get("quarter", 1) >= 4 or game_context.get("down") == 4:
                result["conversion_modifier"] = 1.0 + effects.conversion_boost

        return result


def get_archetype_modifiers(
    player: Any,
    game_context: Dict[str, Any],
    dna_traits: Optional[List[str]] = None
) -> Dict[str, Any]:
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

"""
Use-Based Skill Progression Service
====================================

Skyrim-style progression where player attributes improve through successful
in-game use. Supplements the existing weekly training XP system.

Key Mechanics:
- Successful actions award XP to specific attributes
- Higher difficulty actions = more XP (deep passes, goal line plays)
- Development trait and age multipliers
- Diminishing returns at higher attribute levels
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

class ActionType(str, Enum):
    """Types of in-game actions that award attribute XP."""
    # Passing Actions
    PASS_COMPLETION_SHORT = "PASS_COMPLETION_SHORT"
    PASS_COMPLETION_MID = "PASS_COMPLETION_MID"
    PASS_COMPLETION_DEEP = "PASS_COMPLETION_DEEP"
    PASS_UNDER_PRESSURE = "PASS_UNDER_PRESSURE"
    TOUCHDOWN_PASS = "TOUCHDOWN_PASS"

    # Rushing Actions
    RUSHING_GAIN = "RUSHING_GAIN"
    RUSHING_TD = "RUSHING_TD"
    BROKEN_TACKLE = "BROKEN_TACKLE"
    BIG_RUN = "BIG_RUN"  # 10+ yards

    # Receiving Actions
    RECEPTION = "RECEPTION"
    CONTESTED_CATCH = "CONTESTED_CATCH"
    YAC_GAIN = "YAC_GAIN"  # Yards after catch
    RECEIVING_TD = "RECEIVING_TD"

    # Blocking Actions
    PANCAKE_BLOCK = "PANCAKE_BLOCK"
    SUSTAINED_BLOCK = "SUSTAINED_BLOCK"
    PASS_PRO_WIN = "PASS_PRO_WIN"

    # Defensive Actions
    TACKLE = "TACKLE"
    TACKLE_FOR_LOSS = "TACKLE_FOR_LOSS"
    SACK = "SACK"
    QB_HIT = "QB_HIT"
    PASS_DEFENDED = "PASS_DEFENDED"
    INTERCEPTION = "INTERCEPTION"
    FORCED_FUMBLE = "FORCED_FUMBLE"
    FUMBLE_RECOVERY = "FUMBLE_RECOVERY"

    # Special Teams
    FIELD_GOAL_MADE = "FIELD_GOAL_MADE"
    LONG_FG_MADE = "LONG_FG_MADE"  # 50+ yards
    PUNT_INSIDE_20 = "PUNT_INSIDE_20"


# XP awards per action type -> {attribute_name: base_xp}
ACTION_XP_AWARDS: Dict[str, Dict[str, int]] = {
    # Passing
    ActionType.PASS_COMPLETION_SHORT: {
        "throw_accuracy_short": 3,
        "awareness": 1,
    },
    ActionType.PASS_COMPLETION_MID: {
        "throw_accuracy_mid": 4,
        "awareness": 1,
    },
    ActionType.PASS_COMPLETION_DEEP: {
        "throw_accuracy_deep": 5,
        "throw_power": 2,
        "awareness": 1,
    },
    ActionType.PASS_UNDER_PRESSURE: {
        "throw_on_the_run": 4,
        "pocket_presence": 3,
    },
    ActionType.TOUCHDOWN_PASS: {
        "awareness": 3,
        "throw_accuracy_mid": 2,
    },

    # Rushing
    ActionType.RUSHING_GAIN: {
        "agility": 1,
        "acceleration": 1,
    },
    ActionType.RUSHING_TD: {
        "agility": 3,
        "awareness": 2,
    },
    ActionType.BROKEN_TACKLE: {
        "break_tackle": 4,
        "trucking": 2,
        "strength": 1,
    },
    ActionType.BIG_RUN: {
        "speed": 3,
        "acceleration": 2,
        "agility": 2,
    },

    # Receiving
    ActionType.RECEPTION: {
        "catching": 2,
        "route_running": 2,
    },
    ActionType.CONTESTED_CATCH: {
        "catching": 4,
        "catch_in_traffic": 5,
        "awareness": 2,
    },
    ActionType.YAC_GAIN: {
        "speed": 2,
        "juke_move": 2,
        "stiff_arm": 1,
    },
    ActionType.RECEIVING_TD: {
        "catching": 3,
        "route_running": 2,
    },

    # Blocking
    ActionType.PANCAKE_BLOCK: {
        "run_block": 5,
        "strength": 3,
    },
    ActionType.SUSTAINED_BLOCK: {
        "run_block": 2,
        "pass_block": 2,
    },
    ActionType.PASS_PRO_WIN: {
        "pass_block": 4,
        "awareness": 1,
    },

    # Defensive
    ActionType.TACKLE: {
        "tackle": 2,
        "pursuit": 1,
    },
    ActionType.TACKLE_FOR_LOSS: {
        "tackle": 4,
        "pursuit": 3,
        "play_recognition": 2,
    },
    ActionType.SACK: {
        "tackle": 3,
        "pass_rush": 5,
        "power_moves": 2,
        "finesse_moves": 2,
    },
    ActionType.QB_HIT: {
        "pass_rush": 3,
        "pursuit": 2,
    },
    ActionType.PASS_DEFENDED: {
        "man_coverage": 3,
        "zone_coverage": 3,
        "awareness": 2,
    },
    ActionType.INTERCEPTION: {
        "catching": 4,
        "zone_coverage": 5,
        "man_coverage": 3,
        "awareness": 3,
    },
    ActionType.FORCED_FUMBLE: {
        "hit_power": 5,
        "tackle": 2,
    },
    ActionType.FUMBLE_RECOVERY: {
        "awareness": 4,
    },

    # Special Teams
    ActionType.FIELD_GOAL_MADE: {
        "kick_power": 2,
        "kick_accuracy": 3,
    },
    ActionType.LONG_FG_MADE: {
        "kick_power": 5,
        "kick_accuracy": 4,
    },
    ActionType.PUNT_INSIDE_20: {
        "kick_power": 2,
        "kick_accuracy": 3,
    },
}


# Development trait multipliers (matches DevelopmentTrait enum)
DEV_TRAIT_MULTIPLIERS = {
    "NORMAL": 1.0,
    "STAR": 1.2,
    "SUPERSTAR": 1.5,
    "XFACTOR": 2.0,
}

# Age-based learning rate multipliers
def get_age_multiplier(age: int, position: str = "DEFAULT") -> float:
    """
    Get XP learning multiplier based on age and position.
    Young players learn faster, veterans slower. Position affects prime window.

    Now delegates to age_curves.get_development_rate_modifier for consistency,
    but also incorporates phase-based multipliers.
    """
    from app.services.age_curves import get_phase_xp_multiplier, get_development_rate_modifier

    # Combine phase multiplier (ASCENSION/PRIME/DECLINE) with development rate
    phase_mult = get_phase_xp_multiplier(position, age)
    dev_mult = get_development_rate_modifier(age)

    # Average them to avoid over-penalizing
    return (phase_mult + dev_mult) / 2


# Difficulty/context multipliers
CONTEXT_MULTIPLIERS = {
    "red_zone": 1.5,      # Inside opponent's 20
    "goal_line": 2.0,     # Inside opponent's 5
    "clutch_moment": 1.3, # 4th quarter, close game
    "contested": 1.5,     # Contested catch/play
    "blitz": 1.3,         # Completed pass vs blitz
}


# XP required to gain +1 to an attribute (diminishing returns)
def get_xp_threshold(current_rating: int) -> int:
    """
    Higher ratings require more XP to improve.
    This creates natural diminishing returns.
    """
    if current_rating < 60:
        return 100
    elif current_rating < 70:
        return 150
    elif current_rating < 80:
        return 250
    elif current_rating < 85:
        return 400
    elif current_rating < 90:
        return 600
    elif current_rating < 95:
        return 1000
    else:
        return 2000  # Extremely hard to improve 95+


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class AttributeXPGain:
    """Record of XP gained for a specific attribute."""
    attribute_name: str
    base_xp: int
    final_xp: int
    multipliers_applied: Dict[str, float]


@dataclass
class ProgressionEvent:
    """Record of an attribute level-up."""
    player_id: int
    attribute_name: str
    old_value: int
    new_value: int
    total_xp_spent: int


# =============================================================================
# MAIN SERVICE
# =============================================================================

class UseBasedProgression:
    """
    Skyrim-style progression where attributes improve through use.

    Usage:
        progression = UseBasedProgression()
        gains = progression.award_action_xp(player, ActionType.SACK, context)
        levelups = progression.check_and_apply_levelups(player)
    """

    @staticmethod
    def award_action_xp(
        player: Any,
        action_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[AttributeXPGain]:
        """
        Award XP to player attributes based on a successful action.

        Args:
            player: Player object with id, age, development_trait, attribute_xp
            action_type: The type of action performed (from ActionType enum)
            context: Optional context for multipliers (red_zone, clutch, etc.)

        Returns:
            List of AttributeXPGain records showing XP awarded
        """
        context = context or {}
        gains = []

        # Get base XP awards for this action
        action_key = action_type if isinstance(action_type, str) else action_type.value
        base_awards = ACTION_XP_AWARDS.get(action_key, {})

        if not base_awards:
            logger.warning(f"Unknown action type: {action_type}")
            return gains

        # Calculate multipliers
        dev_trait = getattr(player, "development_trait", "NORMAL")
        dev_mult = DEV_TRAIT_MULTIPLIERS.get(str(dev_trait).upper(), 1.0)

        age = getattr(player, "age", 25)
        position = getattr(player, "position", "DEFAULT")
        # Convert Position enum to string if needed
        from enum import Enum
        position_str = position.value if isinstance(position, Enum) else str(position)
        age_mult = get_age_multiplier(age, position_str)

        # Context multipliers
        context_mult = 1.0
        multipliers_used = {"dev_trait": dev_mult, "age": age_mult}

        for ctx_key, ctx_mult in CONTEXT_MULTIPLIERS.items():
            if context.get(ctx_key):
                context_mult *= ctx_mult
                multipliers_used[ctx_key] = ctx_mult

        multipliers_used["context"] = context_mult
        total_mult = dev_mult * age_mult * context_mult

        # Award XP to each attribute
        attribute_xp = getattr(player, "attribute_xp", None)
        if attribute_xp is None:
            attribute_xp = {}
            player.attribute_xp = attribute_xp

        for attr_name, base_xp in base_awards.items():
            final_xp = int(base_xp * total_mult)

            # Accumulate XP
            current_attr_xp = attribute_xp.get(attr_name, 0)
            attribute_xp[attr_name] = current_attr_xp + final_xp

            gains.append(AttributeXPGain(
                attribute_name=attr_name,
                base_xp=base_xp,
                final_xp=final_xp,
                multipliers_applied=multipliers_used.copy()
            ))

            logger.debug(
                f"Player {getattr(player, 'id', 'unknown')} gained {final_xp} XP "
                f"in {attr_name} (base: {base_xp}, mult: {total_mult:.2f})"
            )

        return gains

    @staticmethod
    def check_and_apply_levelups(player: Any) -> List[ProgressionEvent]:
        """
        Check if any attributes have enough XP to level up, and apply if so.

        Args:
            player: Player object

        Returns:
            List of ProgressionEvent records for any attributes that leveled up
        """
        levelups = []
        attribute_xp = getattr(player, "attribute_xp", {})

        for attr_name, accumulated_xp in list(attribute_xp.items()):
            # Get current attribute value
            current_value = getattr(player, attr_name, None)
            if current_value is None:
                continue

            # Check if we have enough XP to level up
            threshold = get_xp_threshold(current_value)

            while accumulated_xp >= threshold and current_value < 99:
                # Level up!
                old_value = current_value
                current_value = min(99, current_value + 1)
                accumulated_xp -= threshold

                # Apply to player
                setattr(player, attr_name, current_value)

                levelups.append(ProgressionEvent(
                    player_id=getattr(player, "id", 0),
                    attribute_name=attr_name,
                    old_value=old_value,
                    new_value=current_value,
                    total_xp_spent=threshold
                ))

                logger.info(
                    f"🎯 LEVEL UP! Player {getattr(player, 'id', 'unknown')}: "
                    f"{attr_name} {old_value} → {current_value}"
                )

                # Recalculate threshold for next level
                threshold = get_xp_threshold(current_value)

            # Update remaining XP
            attribute_xp[attr_name] = accumulated_xp

        return levelups

    @staticmethod
    def get_progression_summary(player: Any) -> Dict[str, Dict]:
        """
        Get a summary of player's attribute XP progress.

        Returns:
            Dict mapping attribute name to progress info
        """
        attribute_xp = getattr(player, "attribute_xp", {})
        summary = {}

        for attr_name, xp in attribute_xp.items():
            current_value = getattr(player, attr_name, 50)
            threshold = get_xp_threshold(current_value)

            summary[attr_name] = {
                "current_xp": xp,
                "threshold": threshold,
                "progress_pct": min(100, int((xp / threshold) * 100)),
                "current_rating": current_value,
            }

        return summary

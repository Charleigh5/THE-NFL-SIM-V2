"""
Position-Weighted Rating Calculator
=====================================

Implements Madden-style position-weighted OVR calculation.

Based on industry research:
- Madden uses ~43 attributes with position-specific weights
- Key attributes for each position carry higher weights
- Speed/Awareness are important across positions but vary in weight
"""
from typing import Dict, Optional
from app.models.player import Player


# =============================================================================
# POSITION WEIGHT DEFINITIONS (Madden-inspired)
# =============================================================================
# Weights are normalized to sum to 1.0 for each position
# Based on research: https://dexalytics.com/madden-nfl-player-ratings-explained

POSITION_WEIGHTS: Dict[str, Dict[str, float]] = {
    # -------------------------------------------------------------------------
    # QUARTERBACK
    # -------------------------------------------------------------------------
    "QB": {
        "throw_power": 0.12,
        "throw_accuracy_short": 0.11,
        "throw_accuracy_mid": 0.11,
        "throw_accuracy_deep": 0.10,
        "awareness": 0.10,
        "pocket_presence": 0.08,
        "quick_release": 0.06,
        "throw_on_run": 0.06,
        "speed": 0.05,
        "agility": 0.05,
        "acceleration": 0.04,
        "scramble_willingness": 0.04,
        "strength": 0.03,
        "stamina": 0.03,
        "injury_resistance": 0.02,
    },

    # -------------------------------------------------------------------------
    # RUNNING BACK
    # -------------------------------------------------------------------------
    "RB": {
        "speed": 0.13,
        "acceleration": 0.11,
        "agility": 0.11,
        "awareness": 0.08,
        "catching": 0.08,
        "strength": 0.07,
        "patience": 0.06,
        "juke_efficiency": 0.06,
        "break_tackle_threshold": 0.05,
        "pass_pro_rating": 0.05,
        "vision_cone_angle": 0.04,
        "stamina": 0.04,
        "injury_resistance": 0.02,
    },

    # -------------------------------------------------------------------------
    # WIDE RECEIVER
    # -------------------------------------------------------------------------
    "WR": {
        "speed": 0.14,
        "catching": 0.13,
        "route_running": 0.12,
        "acceleration": 0.10,
        "agility": 0.09,
        "release": 0.08,
        "awareness": 0.07,
        "blocking_tenacity": 0.04,
        "strength": 0.04,
        "stamina": 0.03,
        "height": 0.04,  # Special: taller WRs have advantage
        "injury_resistance": 0.02,
    },

    # -------------------------------------------------------------------------
    # TIGHT END
    # -------------------------------------------------------------------------
    "TE": {
        "catching": 0.12,
        "route_running": 0.10,
        "run_block": 0.10,
        "pass_block": 0.08,
        "speed": 0.10,
        "strength": 0.10,
        "awareness": 0.08,
        "acceleration": 0.07,
        "agility": 0.06,
        "release": 0.05,
        "blocking_tenacity": 0.05,
        "stamina": 0.04,
        "injury_resistance": 0.03,
    },

    # -------------------------------------------------------------------------
    # OFFENSIVE LINE (OT, OG, C)
    # -------------------------------------------------------------------------
    "OT": {
        "pass_block": 0.20,
        "run_block": 0.15,
        "strength": 0.12,
        "awareness": 0.10,
        "anchor": 0.10,
        "agility": 0.06,
        "acceleration": 0.05,
        "pull_speed": 0.05,
        "discipline": 0.05,
        "stamina": 0.05,
        "speed": 0.04,
        "injury_resistance": 0.03,
    },
    "OG": {
        "run_block": 0.18,
        "pass_block": 0.16,
        "strength": 0.14,
        "awareness": 0.10,
        "anchor": 0.08,
        "pull_speed": 0.08,
        "agility": 0.06,
        "acceleration": 0.05,
        "discipline": 0.05,
        "stamina": 0.05,
        "speed": 0.03,
        "injury_resistance": 0.02,
    },
    "C": {
        "pass_block": 0.16,
        "run_block": 0.16,
        "awareness": 0.14,  # Higher for making calls
        "strength": 0.12,
        "anchor": 0.10,
        "agility": 0.06,
        "acceleration": 0.05,
        "discipline": 0.06,
        "stamina": 0.05,
        "pull_speed": 0.04,
        "speed": 0.03,
        "injury_resistance": 0.03,
    },

    # -------------------------------------------------------------------------
    # DEFENSIVE LINE
    # -------------------------------------------------------------------------
    "DE": {
        "speed": 0.12,
        "acceleration": 0.10,
        "pass_rush_power": 0.12,
        "pass_rush_finesse": 0.12,
        "block_shed": 0.10,
        "strength": 0.08,
        "first_step": 0.08,
        "awareness": 0.06,
        "tackle": 0.06,
        "agility": 0.06,
        "gap_integrity": 0.05,
        "stamina": 0.03,
        "injury_resistance": 0.02,
    },
    "DT": {
        "strength": 0.14,
        "block_shed": 0.14,
        "pass_rush_power": 0.12,
        "awareness": 0.10,
        "tackle": 0.08,
        "gap_integrity": 0.08,
        "pass_rush_finesse": 0.06,
        "acceleration": 0.06,
        "first_step": 0.06,
        "speed": 0.04,
        "agility": 0.04,
        "stamina": 0.04,
        "injury_resistance": 0.04,
    },

    # -------------------------------------------------------------------------
    # LINEBACKER
    # -------------------------------------------------------------------------
    "LB": {
        "tackle": 0.12,
        "awareness": 0.10,
        "play_recognition": 0.10,
        "speed": 0.10,
        "acceleration": 0.08,
        "zone_coverage": 0.08,
        "hit_power": 0.06,
        "block_shed": 0.06,
        "man_coverage": 0.06,
        "agility": 0.05,
        "strength": 0.05,
        "run_fit": 0.05,
        "blitz_timing": 0.04,
        "stamina": 0.03,
        "coverage_disguise": 0.02,
    },

    # -------------------------------------------------------------------------
    # DEFENSIVE BACKS
    # -------------------------------------------------------------------------
    "CB": {
        "man_coverage": 0.14,
        "zone_coverage": 0.12,
        "speed": 0.12,
        "acceleration": 0.10,
        "agility": 0.08,
        "press": 0.08,
        "ball_tracking": 0.07,
        "awareness": 0.06,
        "play_recognition": 0.05,
        "tackle": 0.04,
        "catching": 0.04,
        "run_support": 0.04,
        "stamina": 0.03,
        "injury_resistance": 0.03,
    },
    "S": {
        "zone_coverage": 0.12,
        "tackle": 0.10,
        "awareness": 0.10,
        "speed": 0.10,
        "hit_power": 0.08,
        "man_coverage": 0.08,
        "acceleration": 0.07,
        "play_recognition": 0.07,
        "run_support": 0.06,
        "ball_tracking": 0.06,
        "agility": 0.05,
        "catching": 0.04,
        "stamina": 0.04,
        "injury_resistance": 0.03,
    },

    # -------------------------------------------------------------------------
    # SPECIALISTS
    # -------------------------------------------------------------------------
    "K": {
        "kick_power": 0.35,
        "kick_accuracy": 0.35,
        "awareness": 0.10,
        "stamina": 0.10,
        "injury_resistance": 0.10,
    },
    "P": {
        "kick_power": 0.30,
        "kick_accuracy": 0.25,
        "hang_time": 0.15,
        "coffin_corner": 0.10,
        "awareness": 0.10,
        "stamina": 0.05,
        "injury_resistance": 0.05,
    },
}


class RatingCalculator:
    """
    Service for calculating position-weighted overall ratings.

    Implements Madden-style rating calculation using position-specific
    attribute weights to compute a single OVR number.
    """

    @staticmethod
    def calculate_overall_rating(player: Player) -> int:
        """
        Calculate position-weighted overall rating for a player.

        Args:
            player: Player model instance with attributes

        Returns:
            Integer OVR rating (40-99 scale)
        """
        position = player.position
        weights = POSITION_WEIGHTS.get(position)

        if not weights:
            # Unknown position: return simple average of key stats
            return RatingCalculator._calculate_fallback_rating(player)

        weighted_sum = 0.0
        total_weight = 0.0

        for attr_name, weight in weights.items():
            # Handle special cases
            if attr_name == "height":
                # Convert height to rating: 70" = 50, 76" = 80, etc.
                height_val = getattr(player, "height", 72)
                attr_value = max(40, min(99, 50 + (height_val - 70) * 5))
            elif attr_name == "break_tackle_threshold":
                # Normalize threshold (lower is better for breaking tackles)
                threshold = getattr(player, attr_name, 100)
                attr_value = max(40, min(99, 100 - (threshold / 2)))
            else:
                attr_value = getattr(player, attr_name, 50)

            weighted_sum += attr_value * weight
            total_weight += weight

        # Normalize just in case weights don't sum to 1
        if total_weight > 0:
            raw_rating = weighted_sum / total_weight
        else:
            raw_rating = 50

        # Clamp to valid range
        return int(max(40, min(99, round(raw_rating))))

    @staticmethod
    def _calculate_fallback_rating(player: Player) -> int:
        """
        Calculate a simple average rating for unknown positions.

        Uses core athletic attributes that apply to all positions.
        """
        core_attrs = [
            "speed", "acceleration", "strength", "agility",
            "awareness", "stamina", "injury_resistance"
        ]

        total = sum(getattr(player, attr, 50) for attr in core_attrs)
        return int(max(40, min(99, total / len(core_attrs))))

    @staticmethod
    def get_position_weights(position: str) -> Optional[Dict[str, float]]:
        """
        Get the weight configuration for a position.

        Useful for debugging or displaying to users.
        """
        return POSITION_WEIGHTS.get(position)

    @staticmethod
    def get_top_attributes(position: str, n: int = 5) -> list:
        """
        Get the top N most important attributes for a position.

        Returns list of (attribute_name, weight) tuples.
        """
        weights = POSITION_WEIGHTS.get(position, {})
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        return sorted_weights[:n]

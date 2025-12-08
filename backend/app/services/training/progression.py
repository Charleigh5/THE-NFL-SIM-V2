#!/usr/bin/env python3
"""
XP Progression Module
=====================
Handles player development, regression, and aging curves.

Phase 7: Training & Development
- XP thresholds and leveling
- Age-based regression physics
- Dev Trait (Star, Superstar) influence
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math
import random


# ============================================================================
# ENUMS
# ============================================================================

class DevTrait(str, Enum):
    """Development potential trait."""
    NORMAL = "NORMAL"
    STAR = "STAR"
    SUPERSTAR = "SUPERSTAR"
    X_FACTOR = "X_FACTOR"


class ProgressionPhase(str, Enum):
    """Career phase for progression logic."""
    ROOKIE = "ROOKIE"          # Rapid initial growth
    PRIME = "PRIME"            # Peak performance
    POST_PRIME = "POST_PRIME"  # Mental growth, physical plateau
    DECLINE = "DECLINE"        # Physical regression
    RETIREMENT = "RETIREMENT"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class PlayerProgressionState:
    """Current progression status."""
    player_id: str
    age: int
    current_xp: int
    level: int  # OVR approximation
    dev_trait: DevTrait
    xp_to_next_level: int
    career_phase: ProgressionPhase = ProgressionPhase.ROOKIE


# ============================================================================
# PROGRESSION ENGINE
# ============================================================================

class ProgressionEngine:
    """
    Calculates XP gains, leveling up, and regression.

    Physics:
    - Logistic growth curve for skill acquisition
    - Exponential decay for physical traits after peak age
    """

    # Peak ages by position group
    PEAK_AGES = {
        "QB": (26, 32),
        "RB": (23, 27),
        "WR": (25, 29),
        "TE": (26, 30),
        "OL": (26, 31),
        "DL": (25, 29),
        "LB": (24, 28),
        "DB": (24, 28),
        "K": (27, 35),
        "P": (27, 35),
    }

    def calculate_xp_threshold(self, current_level: int) -> int:
        """Calculate XP needed for next level."""
        # Nonlinear scaling: Harder to improve as you get better
        # Base 1000 + exponential factor
        return int(1000 * (1.1 ** (current_level - 70))) if current_level > 70 else 1000

    def get_dev_trait_multiplier(self, trait: DevTrait) -> float:
        """Get XP multiplier for dev trait."""
        return {
            DevTrait.NORMAL: 1.0,
            DevTrait.STAR: 1.25,
            DevTrait.SUPERSTAR: 1.5,
            DevTrait.X_FACTOR: 2.0,
        }[trait]

    def determine_phase(self, position: str, age: int) -> ProgressionPhase:
        """Determine career phase based on age."""
        start_peak, end_peak = self.PEAK_AGES.get(position, (25, 29))

        if age < start_peak:
            return ProgressionPhase.ROOKIE
        elif start_peak <= age <= end_peak:
            return ProgressionPhase.PRIME
        elif age <= end_peak + 2:
            return ProgressionPhase.POST_PRIME
        else:
            return ProgressionPhase.DECLINE

    def apply_xp(
        self,
        state: PlayerProgressionState,
        xp_gained: int,
    ) -> Tuple[PlayerProgressionState, int]:
        """
        Apply XP and handle leveling.

        Returns:
            (Updated State, Levels Gained)
        """
        multiplier = self.get_dev_trait_multiplier(state.dev_trait)
        adjusted_xp = int(xp_gained * multiplier)

        new_xp = state.current_xp + adjusted_xp
        levels_gained = 0

        # Level up loop
        while new_xp >= state.xp_to_next_level:
            new_xp -= state.xp_to_next_level
            state.level += 1 # In real system, this would trigger attribute upgrade point
            levels_gained += 1
            # Recalculate threshold for next level
            state.xp_to_next_level = self.calculate_xp_threshold(state.level)

        state.current_xp = new_xp
        return state, levels_gained

    def calculate_regression(
        self,
        position: str,
        age: int,
        attributes: Dict[str, int],
    ) -> Dict[str, int]:
        """
        Calculate attribute regression for declining players.

        Physics:
        - Speed/Agility decay fastest
        - Strength decays moderate
        - Awareness/skills stay or grow
        """
        phase = self.determine_phase(position, age)
        if phase != ProgressionPhase.DECLINE:
            return {} # No regression

        start_peak, end_peak = self.PEAK_AGES.get(position, (25, 29))
        years_past_prime = age - end_peak

        # Regression severity increases with age
        loss_chance = 0.5 + (years_past_prime * 0.1) # 50% base + 10% per year

        regressed_attrs = {}

        for attr, val in attributes.items():
            if attr in ["speed", "acceleration", "agility", "jumping"]:
                # Physical traits hit hardest
                if random.random() < loss_chance:
                    loss = random.randint(1, 1 + years_past_prime)
                    regressed_attrs[attr] = -loss
            elif attr in ["strength", "throw_power"]:
                # Power traits hit slower
                if random.random() < (loss_chance * 0.6):
                    loss = random.randint(1, 2)
                    regressed_attrs[attr] = -loss
            elif attr in ["awareness", "play_recognition"]:
                # Mental traits rarely regress, might even gain
                pass

        return regressed_attrs

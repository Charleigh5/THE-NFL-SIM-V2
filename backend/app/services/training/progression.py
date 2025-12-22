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
from app.services.training.growth_curves import GrowthCurveEngine


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
    position: str = "ATH"  # Needed for growth curves
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

    def get_age_curve_coefficient(self, position: str, age: int) -> float:
        """
        Get the efficiency multiplier for XP based on age curve.

        Spec: RPG-003
        """
        phase = self.determine_phase(position, age)

        if phase == ProgressionPhase.ROOKIE:
            # Young players learn faster (110-130%)
            return 1.25
        elif phase == ProgressionPhase.PRIME:
            # Peak learning efficiency (100%)
            return 1.0
        elif phase == ProgressionPhase.POST_PRIME:
            # Slowing down (80%)
            return 0.8
        else:
            # Decline phase - XP is very hard to earn (50%)
            return 0.5

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

        # Apply Age Curve Logic (RPG-003)
        # Uses GrowthCurveEngine to get position-specific multiplier
        age_multiplier = GrowthCurveEngine.get_xp_multiplier(state.age, state.position)

        adjusted_xp = int(xp_gained * multiplier * age_multiplier)

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

        Uses GrowthCurveEngine for regression severity scores.
        """
        # Get standardized regression score (0-100)
        regression_score = GrowthCurveEngine.get_regression_score(age, position)

        if regression_score == 0:
            return {} # No regression

        regressed_attrs = {}

        # Convert score to actual potential drops
        # Score 10 ~= 10% chance to lose 1
        # Score 50 ~= 50% chance to lose 1, maybe 2

        # Physical Attributes (Hit Hardest)
        physicals = ["speed", "acceleration", "agility", "jumping"]
        physical_loss_chance = regression_score / 100.0  # e.g., 0.50

        for attr in physicals:
             if attr in attributes:
                  if random.random() < physical_loss_chance:
                       # Major regression can lose multiple points
                       loss = 1
                       if regression_score > 40 and random.random() < 0.3: loss += 1
                       if regression_score > 70 and random.random() < 0.3: loss += 1
                       regressed_attrs[attr] = -loss

        # Skill Attributes (Hit Moderate)
        skills = ["carry", "catch", "throw_power", "throw_accuracy", "block", "tackle", "kick_power"]
        skill_loss_chance = regression_score / 200.0 # Half as likely

        for attr in skills:
             if attr in attributes:
                  if random.random() < skill_loss_chance:
                       loss = 1
                       if regression_score > 60 and random.random() < 0.2: loss += 1
                       regressed_attrs[attr] = -loss

        # Mental Attributes (Safe)
        # No regression applied here by default in this engine version

        return regressed_attrs

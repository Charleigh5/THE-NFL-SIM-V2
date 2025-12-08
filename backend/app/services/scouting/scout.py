#!/usr/bin/env python3
"""
Scouting Engine Module
======================
Manages "Fog of War" mechanics, scout assignments, and attribute unlocking.

Phase 8: Scouting & Draft
- True vs Perceived Ratings
- Scout efficiency and regional knowledge
- Fog of War tiers (Unknown, Range, Precise)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, NewType
from enum import Enum
import random
import math

# Using strings for IDs to keep it simple, but conceptually Typed
PlayerID = str
ScoutID = str


# ============================================================================
# ENUMS
# ============================================================================

class ScoutRegion(str, Enum):
    """Geographic regions for scouting assignment."""
    NATIONAL = "NATIONAL"
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"
    NORTH = "NORTH"


class KnowledgeTier(str, Enum):
    """Level of information revealed about an attribute."""
    UNKNOWN = "UNKNOWN"    # "???"
    VAGUE = "VAGUE"        # "C- to B+" (Wide range)
    SOLID = "SOLID"        # "B" (Narrow range)
    PARTIAL = "PARTIAL"    # "85" (Exact number, but maybe +/- error)
    EXACT = "EXACT"        # "85" (True value)


class ScoutSpecialty(str, Enum):
    """Scout proficiency areas."""
    GENERALIST = "GENERALIST"
    QB_GURU = "QB_GURU"
    TRENCHES = "TRENCHES" # OL/DL
    SKILL_POS = "SKILL_POS" # WR/RB/DB
    ATHLETICISM = "ATHLETICISM" # Better at physicals


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ScoutProfile:
    """A hired scout's attributes."""
    scout_id: ScoutID
    name: str
    region: ScoutRegion
    specialty: ScoutSpecialty
    efficiency: int  # 1-100: How fast they unlock info
    accuracy: int    # 1-100: How close their estimates are to reality


@dataclass
class ScoutingReport:
    """A generated report on a prospect."""
    player_id: PlayerID
    scout_id: ScoutID
    completion_percentage: float = 0.0

    # Map of Attribute Name -> (Perceived Value, Error Margin, Tier)
    # If Tier is VAGUE, user sees e.g. 70-80
    # If Tier is SOLID, user sees e.g. 74-76
    attributes: Dict[str, Tuple[int, int, KnowledgeTier]] = field(default_factory=dict)

    # Text notes
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


# ============================================================================
# SCOUTING ENGINE
# ============================================================================

class ScoutingEngine:
    """
    Manages the revelation of player info (Fog of War).
    """

    def generate_report(
        self,
        true_attributes: Dict[str, int],
        scout: ScoutProfile,
        visits: int = 1
    ) -> ScoutingReport:
        """
        Generate or update a scouting report based on visits.

        Physics of Info:
        - More visits = higher completion = better tiers.
        - Higher scout accuracy = lower error margin.
        - Scout specialty boosts specific attributes.
        """
        report = ScoutingReport(
            player_id="PROSPECT_X", # assigned by caller context usually
            scout_id=scout.scout_id
        )

        # Calculate functional efficiency
        # Base per visit + efficiency bonus
        scout_power = (10 + (scout.efficiency * 0.2)) * visits
        report.completion_percentage = min(100.0, scout_power)

        for attr, true_val in true_attributes.items():
            # Determine Tier based on completion
            tier = self._calculate_tier(report.completion_percentage, attr, scout)

            # Determine Error Margin based on scout accuracy and specialty
            specialty_bonus = self._is_specialty_match(attr, scout.specialty)
            accuracy_effective = scout.accuracy + (20 if specialty_bonus else 0)

            # Error decreases as accuracy increases
            # 50 accuracy -> +/- 10
            # 99 accuracy -> +/- 1
            max_error = max(1, int(20 * (1 - (accuracy_effective / 120.0))))

            # Apply error
            noise = random.randint(-max_error, max_error)
            perceived_val = max(0, min(99, true_val + noise))

            report.attributes[attr] = (perceived_val, max_error, tier)

        return report

    def _calculate_tier(self, completion: float, attribute: str, scout: ScoutProfile) -> KnowledgeTier:
        """Determine what level of detail is revealed."""
        # Athletic attributes are harder to see without Combine/Pro Day scounting (unless specialist)
        is_physical = attribute in ["speed", "strength", "agility"]

        threshold_mod = 20 if is_physical and scout.specialty != ScoutSpecialty.ATHLETICISM else 0

        if completion < (20 + threshold_mod):
            return KnowledgeTier.UNKNOWN
        elif completion < (45 + threshold_mod):
            return KnowledgeTier.VAGUE
        elif completion < (75 + threshold_mod):
            return KnowledgeTier.SOLID
        elif completion < (90 + threshold_mod):
            return KnowledgeTier.PARTIAL
        else:
            return KnowledgeTier.EXACT

    def _is_specialty_match(self, attribute: str, specialty: ScoutSpecialty) -> bool:
        """Check if attribute matches scout specialty."""
        if specialty == ScoutSpecialty.GENERALIST:
            return False # Reliable but no peaks
        if specialty == ScoutSpecialty.ATHLETICISM:
            return attribute in ["speed", "strength", "agility", "jumping"]
        if specialty == ScoutSpecialty.QB_GURU:
            return attribute in ["throw_power", "accuracy", "play_recognition"]
        # Simplified for example
        return False

    def format_for_display(self, report: ScoutingReport) -> Dict[str, str]:
        """
        Convert internal data to user-facing strings.
        E.g. (75, 5, SOLID) -> "B (70-80)"
        """
        display = {}
        for attr, (val, err, tier) in report.attributes.items():
            if tier == KnowledgeTier.UNKNOWN:
                display[attr] = "???"
            elif tier == KnowledgeTier.VAGUE:
                # Wide range
                display[attr] = f"{val-10}-{val+10}"
            elif tier == KnowledgeTier.SOLID:
                # Letter grade or narrow range
                display[attr] = self._val_to_grade(val)
            elif tier == KnowledgeTier.PARTIAL:
                display[attr] = f"~{val}"
            elif tier == KnowledgeTier.EXACT:
                display[attr] = str(val)
        return display

    def _val_to_grade(self, val: int) -> str:
        if val >= 90: return "A"
        if val >= 80: return "B"
        if val >= 70: return "C"
        if val >= 60: return "D"
        return "F"

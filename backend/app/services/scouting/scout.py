#!/usr/bin/env python3
"""
Scouting Engine Module
======================
Manages "Fog of War" mechanics, scout assignments, and attribute unlocking.

Hyper-Immersive Update:
- Added Scout Bias (Old School vs Analytics)
- Added Region (National vs Regional)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, NewType
from enum import Enum
import random
import math

PlayerID = str
ScoutID = str

# ============================================================================
# ENUMS
# ============================================================================

class ScoutRegion(str, Enum):
    NATIONAL = "NATIONAL"
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"
    MIDWEST = "MIDWEST"

class KnowledgeTier(str, Enum):
    UNKNOWN = "UNKNOWN"    # "???"
    VAGUE = "VAGUE"        # "C- to B+" (Wide range)
    SOLID = "SOLID"        # "B" (Narrow range)
    PARTIAL = "PARTIAL"    # "85" (Exact number, but maybe +/- error)
    EXACT = "EXACT"        # "85" (True value)

class ScoutSpecialty(str, Enum):
    GENERALIST = "GENERALIST"
    QB_GURU = "QB_GURU"
    TRENCHES = "TRENCHES"
    SKILL_POS = "SKILL_POS"
    ATHLETICISM = "ATHLETICISM"

class ScoutBias(str, Enum):
    NEUTRAL = "NEUTRAL"
    OLD_SCHOOL = "OLD_SCHOOL"     # Overvalues Size/Strength, underrates Spread QBs
    ANALYTICS = "ANALYTICS"       # Overvalues Efficiency, underrates "Eye Test"
    RAS_LOVER = "RAS_LOVER"       # Overvalues Athleticism regardless of skill
    CHARACTER = "CHARACTER"       # Overvalues Leadership/Intangibles

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
    bias: ScoutBias = ScoutBias.NEUTRAL

@dataclass
class ScoutingReport:
    """A generated report on a prospect."""
    player_id: PlayerID
    scout_id: ScoutID
    completion_percentage: float = 0.0

    # Map of Attribute Name -> (Perceived Value, Error Margin, Tier)
    attributes: Dict[str, Tuple[int, int, KnowledgeTier]] = field(default_factory=dict)

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
        Generate or update a scouting report.
        """
        report = ScoutingReport(
            player_id="PROSPECT_X",
            scout_id=scout.scout_id
        )

        # 1. Completion Calculation
        scout_power = (10 + (scout.efficiency * 0.2)) * visits
        report.completion_percentage = min(100.0, scout_power)

        for attr, true_val in true_attributes.items():
            # 2. Determine Tier
            tier = self._calculate_tier(report.completion_percentage, attr, scout)

            # 3. Determine Error Margin (Accuracy + Specialty)
            specialty_bonus = self._is_specialty_match(attr, scout.specialty)
            accuracy_effective = scout.accuracy + (20 if specialty_bonus else 0)

            # Base Error
            max_error = max(1, int(20 * (1 - (accuracy_effective / 120.0))))

            # 4. Apply Bias (The "Hyper-Immersive" Twist)
            bias_shift = self._calculate_bias_shift(attr, scout.bias, true_val)

            # Final Value Calculation
            # Noise is random error + systematic bias
            noise = random.randint(-max_error, max_error)
            perceived_val = max(0, min(99, true_val + noise + bias_shift))

            report.attributes[attr] = (perceived_val, max_error, tier)

        return report

    def _calculate_bias_shift(self, attr: str, bias: ScoutBias, val: int) -> int:
        """
        Returns a shift in perceived rating based on bias.
        e.g. Old School scout sees a 90 Str player as a 95 (loves him).
        """
        if bias == ScoutBias.NEUTRAL:
            return 0

        shift = 0

        if bias == ScoutBias.OLD_SCHOOL:
            if attr in ["strength", "tackle", "run_block", "hit_power"]:
                shift += 3 # Loves physicality
            if attr in ["speed", "agility"]:
                shift -= 2 # Undervalues pure speed

        elif bias == ScoutBias.ANALYTICS:
            if attr in ["awareness", "route_running", "accuracy"]:
                shift += 3 # Loves technical efficiency
            if attr in ["strength", "size"]:
                shift -= 2 # Doesn't care about "looking the part"

        elif bias == ScoutBias.RAS_LOVER:
            if attr in ["speed", "jump", "agility", "strength"]:
                shift += 5 # HUGE boost for athletes
            else:
                shift -= 3 # Penalties for technical skills ("he's raw")

        elif bias == ScoutBias.TECHNICIAN:
            if attr in ["route_running", "awareness", "man_coverage", "zone_coverage", "throw_accuracy_mid", "throw_accuracy_short", "throw_accuracy_deep"]:
                shift += 4 # Loves technique and precision
            if attr in ["speed", "strength"]:
                shift -= 2 # Doesn't prioritize raw tools

        elif bias == ScoutBias.CHARACTER:
            if attr in ["awareness", "stamina"]:
                shift += 3 # Values mental/leadership proxies
            # No penalties - CHARACTER scouts are positive overall

        return shift

    def _calculate_tier(self, completion: float, attribute: str, scout: ScoutProfile) -> KnowledgeTier:
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
        if specialty == ScoutSpecialty.GENERALIST: return False
        if specialty == ScoutSpecialty.ATHLETICISM: return attribute in ["speed", "strength", "agility"]
        if specialty == ScoutSpecialty.QB_GURU: return attribute in ["throw_power", "throw_accuracy_mid"]
        if specialty == ScoutSpecialty.TRENCHES: return attribute in ["run_block", "pass_block", "power_moves"]
        if specialty == ScoutSpecialty.SKILL_POS: return attribute in ["catching", "route_running", "man_coverage"]
        return False

    def format_for_display(self, report: ScoutingReport) -> Dict[str, str]:
        display = {}
        for attr, (val, err, tier) in report.attributes.items():
            if tier == KnowledgeTier.UNKNOWN:
                display[attr] = "???"
            elif tier == KnowledgeTier.VAGUE:
                display[attr] = f"{val-10}-{val+10}"
            elif tier == KnowledgeTier.SOLID:
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

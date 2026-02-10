#!/usr/bin/env python3
"""
Enhanced Injury System - GENESIS Biological
============================================
Hierarchical injury modeling with chronic wear and physics-based calculations.

Phase 2: GENESIS Biological Player Modeling
- Body part hierarchy (Head → Neck → Shoulder → ...)
- Chronic wear tracking
- G-force injury calculations
- Re-injury probability

Context7 Best Practices:
- Dataclasses for injury records
- Enum-based body part taxonomy
- Physics integration for injury probability
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ============================================================================
# BODY PART HIERARCHY
# ============================================================================

class BodyRegion(str, Enum):
    """Top-level body regions."""
    HEAD = "HEAD"
    TORSO = "TORSO"
    UPPER_EXTREMITY = "UPPER_EXTREMITY"
    LOWER_EXTREMITY = "LOWER_EXTREMITY"


class BodyPart(str, Enum):
    """Specific body parts for injury tracking."""
    # Head Region
    HEAD = "HEAD"
    NECK = "NECK"

    # Torso Region
    CHEST = "CHEST"
    RIBS = "RIBS"
    BACK_UPPER = "BACK_UPPER"
    BACK_LOWER = "BACK_LOWER"
    SPINE = "SPINE"
    ABDOMEN = "ABDOMEN"

    # Upper Extremity
    SHOULDER_LEFT = "SHOULDER_LEFT"
    SHOULDER_RIGHT = "SHOULDER_RIGHT"
    ARM_UPPER_LEFT = "ARM_UPPER_LEFT"
    ARM_UPPER_RIGHT = "ARM_UPPER_RIGHT"
    ELBOW_LEFT = "ELBOW_LEFT"
    ELBOW_RIGHT = "ELBOW_RIGHT"
    ARM_LOWER_LEFT = "ARM_LOWER_LEFT"
    ARM_LOWER_RIGHT = "ARM_LOWER_RIGHT"
    WRIST_LEFT = "WRIST_LEFT"
    WRIST_RIGHT = "WRIST_RIGHT"
    HAND_LEFT = "HAND_LEFT"
    HAND_RIGHT = "HAND_RIGHT"
    FINGER_LEFT = "FINGER_LEFT"
    FINGER_RIGHT = "FINGER_RIGHT"

    # Lower Extremity
    HIP_LEFT = "HIP_LEFT"
    HIP_RIGHT = "HIP_RIGHT"
    THIGH_LEFT = "THIGH_LEFT"
    THIGH_RIGHT = "THIGH_RIGHT"
    KNEE_LEFT = "KNEE_LEFT"
    KNEE_RIGHT = "KNEE_RIGHT"
    CALF_LEFT = "CALF_LEFT"
    CALF_RIGHT = "CALF_RIGHT"
    ANKLE_LEFT = "ANKLE_LEFT"
    ANKLE_RIGHT = "ANKLE_RIGHT"
    FOOT_LEFT = "FOOT_LEFT"
    FOOT_RIGHT = "FOOT_RIGHT"
    TOE_LEFT = "TOE_LEFT"
    TOE_RIGHT = "TOE_RIGHT"


class InjuryType(str, Enum):
    """Types of injuries."""
    # Muscle/Soft Tissue
    STRAIN = "STRAIN"
    SPRAIN = "SPRAIN"
    CONTUSION = "CONTUSION"
    TEAR_PARTIAL = "TEAR_PARTIAL"
    TEAR_COMPLETE = "TEAR_COMPLETE"
    TENDINITIS = "TENDINITIS"

    # Bone
    FRACTURE = "FRACTURE"
    STRESS_FRACTURE = "STRESS_FRACTURE"
    DISLOCATION = "DISLOCATION"

    # Ligament (knee-specific)
    ACL_TEAR = "ACL_TEAR"
    MCL_TEAR = "MCL_TEAR"
    PCL_TEAR = "PCL_TEAR"
    LCL_TEAR = "LCL_TEAR"
    MENISCUS_TEAR = "MENISCUS_TEAR"

    # Head/Neurological
    CONCUSSION = "CONCUSSION"
    STINGER = "STINGER"

    # Other
    LACERATION = "LACERATION"
    CRAMP = "CRAMP"


class InjurySeverity(int, Enum):
    """Severity levels."""
    MINOR = 1       # 0-1 weeks
    MODERATE = 3    # 2-4 weeks
    SERIOUS = 5     # 5-8 weeks
    SEVERE = 7      # 9-12 weeks
    MAJOR = 9       # Season-ending
    CAREER = 10     # Career-threatening


# ============================================================================
# BODY PART HIERARCHY MAPPING
# ============================================================================

BODY_PART_REGIONS: dict[BodyPart, BodyRegion] = {
    BodyPart.HEAD: BodyRegion.HEAD,
    BodyPart.NECK: BodyRegion.HEAD,
    BodyPart.CHEST: BodyRegion.TORSO,
    BodyPart.RIBS: BodyRegion.TORSO,
    BodyPart.BACK_UPPER: BodyRegion.TORSO,
    BodyPart.BACK_LOWER: BodyRegion.TORSO,
    BodyPart.SPINE: BodyRegion.TORSO,
    BodyPart.ABDOMEN: BodyRegion.TORSO,
    # Upper extremity
    BodyPart.SHOULDER_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.SHOULDER_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ARM_UPPER_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ARM_UPPER_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ELBOW_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ELBOW_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ARM_LOWER_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.ARM_LOWER_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.WRIST_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.WRIST_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.HAND_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.HAND_RIGHT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.FINGER_LEFT: BodyRegion.UPPER_EXTREMITY,
    BodyPart.FINGER_RIGHT: BodyRegion.UPPER_EXTREMITY,
    # Lower extremity
    BodyPart.HIP_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.HIP_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.THIGH_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.THIGH_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.KNEE_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.KNEE_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.CALF_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.CALF_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.ANKLE_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.ANKLE_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.FOOT_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.FOOT_RIGHT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.TOE_LEFT: BodyRegion.LOWER_EXTREMITY,
    BodyPart.TOE_RIGHT: BodyRegion.LOWER_EXTREMITY,
}

# Recovery times in weeks by injury type
BASE_RECOVERY_WEEKS: dict[InjuryType, tuple[int, int]] = {
    InjuryType.CRAMP: (0, 0),
    InjuryType.CONTUSION: (0, 1),
    InjuryType.STRAIN: (1, 4),
    InjuryType.SPRAIN: (1, 6),
    InjuryType.TENDINITIS: (2, 6),
    InjuryType.STINGER: (0, 2),
    InjuryType.LACERATION: (0, 1),
    InjuryType.TEAR_PARTIAL: (4, 8),
    InjuryType.TEAR_COMPLETE: (12, 52),
    InjuryType.STRESS_FRACTURE: (4, 12),
    InjuryType.FRACTURE: (6, 16),
    InjuryType.DISLOCATION: (2, 8),
    InjuryType.CONCUSSION: (1, 4),
    InjuryType.MENISCUS_TEAR: (4, 16),
    InjuryType.MCL_TEAR: (4, 8),
    InjuryType.LCL_TEAR: (4, 8),
    InjuryType.PCL_TEAR: (8, 40),
    InjuryType.ACL_TEAR: (36, 52),
}


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Injury:
    """Individual injury record."""
    body_part: BodyPart
    injury_type: InjuryType
    severity: InjurySeverity
    weeks_to_recovery: int
    weeks_elapsed: int = 0
    season: int = 0
    week: int = 0
    play_id: str | None = None
    g_force: float = 0.0  # Impact force that caused injury

    @property
    def is_healed(self) -> bool:
        """Check if injury has healed."""
        return self.weeks_elapsed >= self.weeks_to_recovery

    @property
    def healing_progress(self) -> float:
        """Progress toward healing (0-1)."""
        if self.weeks_to_recovery == 0:
            return 1.0
        return min(1.0, self.weeks_elapsed / self.weeks_to_recovery)

    @property
    def region(self) -> BodyRegion:
        """Get body region for this injury."""
        return BODY_PART_REGIONS.get(self.body_part, BodyRegion.TORSO)

    def heal_week(self) -> None:
        """Process one week of healing."""
        self.weeks_elapsed += 1


@dataclass
class ChronicWear:
    """Chronic wear/damage to a body part."""
    body_part: BodyPart
    wear_level: float = 0.0  # 0-100
    injury_history: list[Injury] = field(default_factory=list)

    @property
    def re_injury_risk_modifier(self) -> float:
        """
        Modifier for re-injury probability.
        Higher wear = higher risk of new injury.
        """
        base_risk = 1.0 + (self.wear_level / 50.0)
        history_factor = 1.0 + (len(self.injury_history) * 0.1)
        return base_risk * history_factor

    @property
    def performance_modifier(self) -> float:
        """
        Performance reduction due to chronic wear.
        1.0 = no reduction, lower = impaired.
        """
        return max(0.7, 1.0 - (self.wear_level / 200.0))

    def add_wear(self, amount: float) -> None:
        """Add chronic wear."""
        self.wear_level = min(100.0, self.wear_level + amount)

    def recover_wear(self, amount: float) -> None:
        """Recover some chronic wear (offseason rest)."""
        self.wear_level = max(0.0, self.wear_level - amount)


@dataclass
class InjuryProfile:
    """Complete injury profile for a player."""
    # Current injuries
    active_injuries: list[Injury] = field(default_factory=list)

    # Injury history
    injury_history: list[Injury] = field(default_factory=list)

    # Chronic wear by body part
    chronic_wear: dict[BodyPart, ChronicWear] = field(default_factory=dict)

    # CTE risk tracking (head impacts)
    head_impact_count: int = 0
    cumulative_head_g_force: float = 0.0

    # Player's natural resistance
    injury_resistance: int = 80  # 0-100 rating

    @property
    def is_injured(self) -> bool:
        """Check if player has any active injuries."""
        return len(self.active_injuries) > 0

    @property
    def can_play(self) -> bool:
        """Check if player is healthy enough to play."""
        if not self.active_injuries:
            return True

        # Can play through minor injuries
        for injury in self.active_injuries:
            if injury.severity >= InjurySeverity.SERIOUS:
                return False
        return True

    @property
    def cte_risk_score(self) -> float:
        """
        CTE risk score based on cumulative head trauma.
        Higher = more concerning.
        """
        # Based on impact count and cumulative force
        impact_factor = min(100, self.head_impact_count * 0.5)
        force_factor = min(100, self.cumulative_head_g_force / 100)
        return (impact_factor + force_factor) / 2

    def get_worst_injury(self) -> Injury | None:
        """Get the most severe active injury."""
        if not self.active_injuries:
            return None
        return max(self.active_injuries, key=lambda i: i.severity.value)

    def get_wear(self, body_part: BodyPart) -> ChronicWear:
        """Get or create chronic wear record for body part."""
        if body_part not in self.chronic_wear:
            self.chronic_wear[body_part] = ChronicWear(body_part=body_part)
        return self.chronic_wear[body_part]


# ============================================================================
# INJURY ENGINE
# ============================================================================

class InjuryEngine:
    """
    Engine for processing injuries and calculating injury probabilities.
    """

    def __init__(
        self,
        profile: InjuryProfile | None = None,
        rng: Any = None,
    ):
        self.profile = profile or InjuryProfile()
        self.rng = rng

    def calculate_injury_probability(
        self,
        body_part: BodyPart,
        g_force: float,
        fatigue_modifier: float = 1.0,
        is_contact: bool = True,
    ) -> float:
        """
        Calculate probability of injury from an impact.

        Args:
            body_part: Body part receiving impact
            g_force: Impact force in G's
            fatigue_modifier: Modifier from fatigue system (1.0 = normal)
            is_contact: Whether this is a contact play

        Returns:
            Probability of injury (0.0-1.0)
        """
        # Base probability from G-force
        # Injuries become likely above 10G, almost certain above 25G
        if g_force < 5:
            base_prob = 0.001
        elif g_force < 10:
            base_prob = 0.01 * (g_force - 5)
        elif g_force < 20:
            base_prob = 0.05 + 0.02 * (g_force - 10)
        else:
            base_prob = 0.25 + 0.03 * (g_force - 20)

        # Resistance modifier (higher rating = lower probability)
        resistance_mod = (100 - self.profile.injury_resistance) / 100 + 0.5

        # Chronic wear modifier
        wear = self.profile.get_wear(body_part)
        wear_mod = wear.re_injury_risk_modifier

        # Contact vs non-contact
        contact_mod = 1.5 if is_contact else 1.0

        # Combine all modifiers
        final_prob = base_prob * resistance_mod * wear_mod * fatigue_modifier * contact_mod

        return min(0.95, max(0.0, final_prob))

    def check_for_injury(
        self,
        body_part: BodyPart,
        g_force: float,
        fatigue_modifier: float = 1.0,
        is_contact: bool = True,
        season: int = 0,
        week: int = 0,
    ) -> Injury | None:
        """
        Check if an impact causes an injury.

        Returns:
            Injury if one occurred, None otherwise
        """
        probability = self.calculate_injury_probability(
            body_part, g_force, fatigue_modifier, is_contact
        )

        # Roll for injury
        if self.rng:
            roll = self.rng.next_float()
        else:
            import random
            roll = random.random()

        if roll >= probability:
            return None

        # Injury occurred - determine type and severity
        injury = self._generate_injury(body_part, g_force, season, week)

        # Add to profile
        self.profile.active_injuries.append(injury)
        self.profile.injury_history.append(injury)

        # Add chronic wear
        wear = self.profile.get_wear(body_part)
        wear.add_wear(injury.severity.value * 2)
        wear.injury_history.append(injury)

        return injury

    def _generate_injury(
        self,
        body_part: BodyPart,
        g_force: float,
        season: int,
        week: int,
    ) -> Injury:
        """Generate an injury based on body part and force."""
        # Determine injury type based on body part and force
        if body_part in [BodyPart.HEAD, BodyPart.NECK]:
            if g_force > 20:
                injury_type = InjuryType.CONCUSSION
            else:
                injury_type = InjuryType.STINGER
        elif body_part in [BodyPart.KNEE_LEFT, BodyPart.KNEE_RIGHT]:
            if g_force > 25:
                injury_type = InjuryType.ACL_TEAR
            elif g_force > 15:
                injury_type = InjuryType.MCL_TEAR
            else:
                injury_type = InjuryType.SPRAIN
        elif body_part in [BodyPart.ANKLE_LEFT, BodyPart.ANKLE_RIGHT]:
            injury_type = InjuryType.SPRAIN
        elif body_part in [BodyPart.THIGH_LEFT, BodyPart.THIGH_RIGHT,
                          BodyPart.CALF_LEFT, BodyPart.CALF_RIGHT]:
            injury_type = InjuryType.STRAIN
        elif body_part in [BodyPart.SHOULDER_LEFT, BodyPart.SHOULDER_RIGHT]:
            injury_type = InjuryType.DISLOCATION if g_force > 20 else InjuryType.CONTUSION
        else:
            injury_type = InjuryType.CONTUSION

        # Determine severity based on G-force
        if g_force < 10:
            severity = InjurySeverity.MINOR
        elif g_force < 15:
            severity = InjurySeverity.MODERATE
        elif g_force < 20:
            severity = InjurySeverity.SERIOUS
        elif g_force < 25:
            severity = InjurySeverity.SEVERE
        else:
            severity = InjurySeverity.MAJOR

        # Get recovery time
        min_weeks, max_weeks = BASE_RECOVERY_WEEKS.get(injury_type, (1, 4))
        if self.rng:
            recovery = self.rng.next_int(min_weeks, max_weeks)
        else:
            import random
            recovery = random.randint(min_weeks, max_weeks)

        return Injury(
            body_part=body_part,
            injury_type=injury_type,
            severity=severity,
            weeks_to_recovery=recovery,
            season=season,
            week=week,
            g_force=g_force,
        )

    def process_head_impact(self, g_force: float) -> None:
        """Track head impact for CTE risk."""
        self.profile.head_impact_count += 1
        self.profile.cumulative_head_g_force += g_force

    def process_week(self) -> list[Injury]:
        """
        Process healing for one week.

        Returns:
            List of injuries that healed this week
        """
        healed = []
        still_active = []

        for injury in self.profile.active_injuries:
            injury.heal_week()
            if injury.is_healed:
                healed.append(injury)
            else:
                still_active.append(injury)

        self.profile.active_injuries = still_active
        return healed

    def process_offseason_recovery(self, weeks: int = 12) -> None:
        """
        Process offseason recovery.

        Args:
            weeks: Weeks of offseason rest
        """
        # Heal all injuries
        for _ in range(weeks):
            self.process_week()

        # Recover some chronic wear
        for wear in self.profile.chronic_wear.values():
            wear.recover_wear(5.0)  # 5% recovery per offseason

#!/usr/bin/env python3
"""
GENESIS Biometrics Module
=========================
Extended biological attributes for players.

Phase 2: GENESIS Biological Player Modeling
- Hand size, wingspan, fast-twitch percentages
- S2 Cognition score (hidden cognitive ability)
- Sweat rate, body fat percentage
- Biological age factors

Context7 Best Practices:
- SQLAlchemy Mapped columns with type hints
- Pydantic validators for constraints
- Dataclasses for computed properties
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

# ============================================================================
# ENUMS
# ============================================================================


class BodyType(str, Enum):
    """Player body type classification."""

    LEAN = "LEAN"  # Low body fat, explosive
    ATHLETIC = "ATHLETIC"  # Balanced build
    STOCKY = "STOCKY"  # Lower center of gravity
    POWER = "POWER"  # High muscle mass
    LANKY = "LANKY"  # Long limbs, tall


class FiberType(str, Enum):
    """Muscle fiber dominance."""

    FAST_TWITCH = "FAST_TWITCH"  # Explosive, quick fatigue
    BALANCED = "BALANCED"  # Mixed fiber type
    SLOW_TWITCH = "SLOW_TWITCH"  # Endurance, slow fatigue


# ============================================================================
# BIOMETRIC DATA
# ============================================================================


@dataclass
class BiometricProfile:
    """
    Extended biological attributes for a player.

    These attributes affect physics calculations and fatigue modeling.
    """

    # Physical Measurements (additional to height/weight)
    hand_size: float = 9.5  # inches (NFL average: 9.5")
    wingspan: float = 76.0  # inches (fingertip to fingertip)
    arm_length: float = 32.0  # inches (shoulder to wrist)
    vertical_jump: float = 32.0  # inches
    broad_jump: float = 108.0  # inches
    three_cone: float = 7.2  # seconds
    twenty_yard_shuttle: float = 4.3  # seconds

    # Body Composition
    body_fat_percentage: float = 12.0  # percent (NFL range: 5-25%)
    lean_mass_lbs: float = 200.0  # calculated from weight - fat
    body_type: BodyType = BodyType.ATHLETIC

    # Muscle Fiber Composition (affects explosiveness vs endurance)
    fast_twitch_percentage: float = 50.0  # 0-100 (higher = more explosive)
    fiber_type: FiberType = FiberType.BALANCED

    # Cognitive Attributes (hidden from UI, affects decision making)
    s2_cognition_score: float = 100.0  # Standard score (mean=100, std=15)
    reaction_time_ms: float = 250.0  # milliseconds
    processing_speed: float = 100.0  # percentile

    # Thermoregulation
    sweat_rate: float = 1.5  # liters per hour
    heat_tolerance: float = 50.0  # 0-100 scale
    cold_tolerance: float = 50.0  # 0-100 scale

    # Recovery Factors
    vo2_max: float = 50.0  # ml/kg/min (NFL range: 40-60)
    resting_heart_rate: float = 60.0  # bpm
    hrv_score: float = 70.0  # Heart rate variability (higher = better recovery)

    @property
    def relative_wingspan(self) -> float:
        """Wingspan relative to height (ape index)."""
        # Assuming height in inches stored elsewhere
        return self.wingspan / 72.0  # Normalized to 6' player

    @property
    def catch_radius(self) -> float:
        """
        Effective catch radius considering arm length and hand size.
        Used in WR/TE physics for contested catch calculations.
        """
        base_radius = (self.arm_length + self.hand_size) / 12.0  # feet
        return base_radius * 1.1  # Additional reach factor

    @property
    def explosion_factor(self) -> float:
        """
        Explosiveness rating based on muscle fiber composition.
        Higher values = better for short bursts.
        """
        # Fast-twitch dominant players are more explosive
        return 0.5 + (self.fast_twitch_percentage / 200.0)

    @property
    def endurance_factor(self) -> float:
        """
        Endurance rating based on muscle fiber composition.
        Higher values = better sustained performance.
        """
        # Slow-twitch (100 - fast_twitch) is better for endurance
        slow_twitch = 100.0 - self.fast_twitch_percentage
        return 0.5 + (slow_twitch / 200.0)

    @property
    def cognitive_modifier(self) -> float:
        """
        Decision-making speed modifier based on S2 cognition.
        Values > 1.0 = faster decisions, < 1.0 = slower.
        """
        # S2 score of 100 = 1.0x modifier
        # S2 score of 130 = ~1.3x modifier (30% faster)
        return self.s2_cognition_score / 100.0

    @property
    def heat_impact_modifier(self) -> float:
        """
        How much hot weather affects this player.
        Lower = less affected by heat.
        """
        # High sweat rate and low heat tolerance = more affected
        base_impact = 100.0 - self.heat_tolerance
        sweat_factor = self.sweat_rate / 2.0  # Normalize to ~0.75-1.25
        return (base_impact / 100.0) * sweat_factor

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for database storage."""
        return {
            "hand_size": self.hand_size,
            "wingspan": self.wingspan,
            "arm_length": self.arm_length,
            "vertical_jump": self.vertical_jump,
            "broad_jump": self.broad_jump,
            "three_cone": self.three_cone,
            "twenty_yard_shuttle": self.twenty_yard_shuttle,
            "body_fat_percentage": self.body_fat_percentage,
            "lean_mass_lbs": self.lean_mass_lbs,
            "body_type": self.body_type.value,
            "fast_twitch_percentage": self.fast_twitch_percentage,
            "fiber_type": self.fiber_type.value,
            "s2_cognition_score": self.s2_cognition_score,
            "reaction_time_ms": self.reaction_time_ms,
            "processing_speed": self.processing_speed,
            "sweat_rate": self.sweat_rate,
            "heat_tolerance": self.heat_tolerance,
            "cold_tolerance": self.cold_tolerance,
            "vo2_max": self.vo2_max,
            "resting_heart_rate": self.resting_heart_rate,
            "hrv_score": self.hrv_score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BiometricProfile":
        """Deserialize from dictionary."""
        return cls(
            hand_size=data.get("hand_size", 9.5),
            wingspan=data.get("wingspan", 76.0),
            arm_length=data.get("arm_length", 32.0),
            vertical_jump=data.get("vertical_jump", 32.0),
            broad_jump=data.get("broad_jump", 108.0),
            three_cone=data.get("three_cone", 7.2),
            twenty_yard_shuttle=data.get("twenty_yard_shuttle", 4.3),
            body_fat_percentage=data.get("body_fat_percentage", 12.0),
            lean_mass_lbs=data.get("lean_mass_lbs", 200.0),
            body_type=BodyType(data.get("body_type", "ATHLETIC")),
            fast_twitch_percentage=data.get("fast_twitch_percentage", 50.0),
            fiber_type=FiberType(data.get("fiber_type", "BALANCED")),
            s2_cognition_score=data.get("s2_cognition_score", 100.0),
            reaction_time_ms=data.get("reaction_time_ms", 250.0),
            processing_speed=data.get("processing_speed", 100.0),
            sweat_rate=data.get("sweat_rate", 1.5),
            heat_tolerance=data.get("heat_tolerance", 50.0),
            cold_tolerance=data.get("cold_tolerance", 50.0),
            vo2_max=data.get("vo2_max", 50.0),
            resting_heart_rate=data.get("resting_heart_rate", 60.0),
            hrv_score=data.get("hrv_score", 70.0),
        )


# ============================================================================
# POSITION-SPECIFIC BIOMETRIC RANGES
# ============================================================================

POSITION_BIOMETRIC_RANGES = {
    "QB": {
        "hand_size": (9.0, 10.5),
        "wingspan": (74, 82),
        "fast_twitch_percentage": (40, 60),
        "s2_cognition_score": (95, 140),  # QBs tend to score higher
    },
    "RB": {
        "hand_size": (8.5, 10.0),
        "wingspan": (70, 78),
        "fast_twitch_percentage": (60, 85),
        "s2_cognition_score": (85, 120),
    },
    "WR": {
        "hand_size": (8.5, 11.0),
        "wingspan": (72, 84),
        "fast_twitch_percentage": (65, 90),
        "s2_cognition_score": (90, 125),
    },
    "TE": {
        "hand_size": (9.0, 11.0),
        "wingspan": (78, 86),
        "fast_twitch_percentage": (50, 75),
        "s2_cognition_score": (90, 120),
    },
    "OT": {
        "hand_size": (9.5, 11.5),
        "wingspan": (80, 88),
        "fast_twitch_percentage": (35, 55),
        "s2_cognition_score": (90, 115),
    },
    "OG": {
        "hand_size": (9.0, 11.0),
        "wingspan": (78, 84),
        "fast_twitch_percentage": (40, 60),
        "s2_cognition_score": (85, 110),
    },
    "C": {
        "hand_size": (9.0, 10.5),
        "wingspan": (76, 82),
        "fast_twitch_percentage": (35, 55),
        "s2_cognition_score": (95, 120),  # Centers read defenses
    },
    "DE": {
        "hand_size": (9.5, 11.5),
        "wingspan": (80, 88),
        "fast_twitch_percentage": (60, 85),
        "s2_cognition_score": (85, 115),
    },
    "DT": {
        "hand_size": (9.5, 11.0),
        "wingspan": (78, 84),
        "fast_twitch_percentage": (50, 70),
        "s2_cognition_score": (80, 110),
    },
    "LB": {
        "hand_size": (9.0, 10.5),
        "wingspan": (76, 84),
        "fast_twitch_percentage": (55, 80),
        "s2_cognition_score": (90, 125),
    },
    "CB": {
        "hand_size": (8.5, 10.0),
        "wingspan": (74, 82),
        "fast_twitch_percentage": (70, 95),
        "s2_cognition_score": (95, 130),
    },
    "S": {
        "hand_size": (8.5, 10.0),
        "wingspan": (74, 82),
        "fast_twitch_percentage": (60, 85),
        "s2_cognition_score": (95, 130),
    },
    "K": {
        "hand_size": (8.5, 10.0),
        "wingspan": (72, 78),
        "fast_twitch_percentage": (40, 60),
        "s2_cognition_score": (85, 110),
    },
    "P": {
        "hand_size": (8.5, 10.0),
        "wingspan": (74, 80),
        "fast_twitch_percentage": (40, 60),
        "s2_cognition_score": (85, 110),
    },
}


def generate_biometrics_for_position(
    position: str,
    rng: Any,
    talent_level: float = 0.5,
) -> BiometricProfile:
    """
    Generate realistic biometrics for a player based on position.

    Args:
        position: Player position (QB, RB, WR, etc.)
        rng: Random number generator (DeterministicRNG)
        talent_level: 0.0 (low talent) to 1.0 (elite talent)

    Returns:
        BiometricProfile with position-appropriate values
    """
    ranges = POSITION_BIOMETRIC_RANGES.get(position, POSITION_BIOMETRIC_RANGES["LB"])

    def sample_range(key: str, default: tuple[float, float]) -> float:
        """Sample from range, biased by talent level."""
        low, high = ranges.get(key, default)
        # Higher talent = closer to high end
        base = rng.next_float()
        biased = base * (1 - talent_level * 0.5) + talent_level * 0.5
        return low + (high - low) * biased

    # Generate base biometrics
    hand_size = sample_range("hand_size", (8.5, 11.0))
    wingspan = sample_range("wingspan", (72, 86))
    fast_twitch = sample_range("fast_twitch_percentage", (40, 80))
    s2_cognition = sample_range("s2_cognition_score", (85, 130))

    # Fiber type based on fast-twitch percentage
    if fast_twitch > 65:
        fiber_type = FiberType.FAST_TWITCH
    elif fast_twitch < 45:
        fiber_type = FiberType.SLOW_TWITCH
    else:
        fiber_type = FiberType.BALANCED

    return BiometricProfile(
        hand_size=round(hand_size, 2),
        wingspan=round(wingspan, 1),
        arm_length=round(wingspan * 0.42, 1),  # Arm is ~42% of wingspan
        vertical_jump=round(28 + rng.next_float() * 16, 1),  # 28-44"
        broad_jump=round(100 + rng.next_float() * 30, 0),  # 100-130"
        three_cone=round(7.5 - rng.next_float() * 0.8, 2),  # 6.7-7.5s
        twenty_yard_shuttle=round(4.5 - rng.next_float() * 0.5, 2),  # 4.0-4.5s
        body_fat_percentage=round(8 + rng.next_float() * 15, 1),  # 8-23%
        fast_twitch_percentage=round(fast_twitch, 1),
        fiber_type=fiber_type,
        s2_cognition_score=round(s2_cognition, 0),
        reaction_time_ms=round(200 + rng.next_float() * 100, 0),  # 200-300ms
        processing_speed=round(50 + rng.next_float() * 50, 0),  # 50-100 percentile
        sweat_rate=round(1.0 + rng.next_float() * 1.5, 2),  # 1.0-2.5 L/hr
        heat_tolerance=round(30 + rng.next_float() * 50, 0),  # 30-80
        cold_tolerance=round(30 + rng.next_float() * 50, 0),  # 30-80
        vo2_max=round(40 + rng.next_float() * 20, 1),  # 40-60 ml/kg/min
        resting_heart_rate=round(50 + rng.next_float() * 20, 0),  # 50-70 bpm
        hrv_score=round(50 + rng.next_float() * 40, 0),  # 50-90
    )

"""
Gameplay Constants Configuration.

Central location for all gameplay tuning parameters.
Modify this file to balance game mechanics without searching through code.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PassingConstants:
    """Constants for passing-related calculations."""

    # Base probabilities
    COMPLETION_BASE: float = 0.65
    DEEP_PASS_BASE: float = 0.45

    # Modifiers
    DEEP_PASS_PENALTY: float = -0.20
    PRESSURE_COMPLETION_PENALTY: float = 0.15
    SHORT_PASS_BONUS: float = 0.10

    # Trait stat boost to probability conversion
    STAT_BOOST_TO_PROB_SCALE: float = 0.005  # +10 rating = +5% probability

    # Pressure immunity bonus
    PRESSURE_IMMUNITY_BONUS: float = 0.10


@dataclass(frozen=True)
class RushingConstants:
    """Constants for rushing-related calculations."""

    # Base values
    RUN_YARDS_BASE: float = 4.0
    RUN_YARDS_VARIANCE: float = 3.0

    # Modifiers
    INSIDE_RUN_BONUS: float = 0.0
    OUTSIDE_RUN_BONUS: float = 0.0


@dataclass(frozen=True)
class AttributeComparisonConstants:
    """Constants for attribute comparison calculations."""

    # Generic comparison
    DEFAULT_SCALE: float = 0.01
    DEFAULT_MAX_MOD: float = 0.30

    # Speed comparison
    SPEED_MIN_MOD: float = -0.10  # Speed disadvantage cap
    SPEED_MAX_MOD: float = 0.20  # Speed advantage cap (higher because "speed kills")
    SPEED_SCALE: float = 0.01  # 1 point = 1%

    # Strength comparison
    STRENGTH_SCALE: float = 0.01
    STRENGTH_MAX_MOD: float = 0.20

    # Skill comparison (route running vs coverage, etc.)
    SKILL_SCALE: float = 0.01
    SKILL_MAX_MOD: float = 0.25


@dataclass(frozen=True)
class ProbabilityThresholds:
    """Constants for probability bounds and thresholds."""

    # Floor and ceiling for all probabilities
    MIN_CHANCE: float = 0.05
    MAX_CHANCE: float = 0.95

    # Critical outcomes
    CRITICAL_THRESHOLD: float = 0.10  # Top/bottom 10% of rolls

    # Trait effect caps
    TRAIT_BONUS_CAP: float = 0.30


@dataclass(frozen=True)
class FatigueConstants:
    """Constants for fatigue-related calculations."""

    # Fatigue per play
    BASE_FATIGUE_PER_PLAY: float = 0.02
    STAMINA_FATIGUE_SCALE: float = 0.01

    # Recovery
    REST_RECOVERY_RATE: float = 0.05

    # Performance impact
    MAX_FATIGUE_PENALTY: float = 0.20


@dataclass(frozen=True)
class GameplayConstants:
    """
    Central configuration for all gameplay tuning.

    Usage:
        from app.core.gameplay_constants import GAMEPLAY

        speed_mod = max(
            GAMEPLAY.attributes.SPEED_MIN_MOD,
            min(GAMEPLAY.attributes.SPEED_MAX_MOD, diff * GAMEPLAY.attributes.SPEED_SCALE)
        )
    """

    passing: PassingConstants = PassingConstants()
    rushing: RushingConstants = RushingConstants()
    attributes: AttributeComparisonConstants = AttributeComparisonConstants()
    thresholds: ProbabilityThresholds = ProbabilityThresholds()
    fatigue: FatigueConstants = FatigueConstants()


# Singleton instance for easy import
GAMEPLAY = GameplayConstants()

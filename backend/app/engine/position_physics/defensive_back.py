#!/usr/bin/env python3
"""
Defensive Back Physics Module
=============================
Physics for Cornerbacks and Safeties.

Phase 3: Position-Specific Physics
- Press coverage jam mechanics
- Hip-flip change of direction
- Break point recognition
- Interception physics
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .base import (
    PhysicsState,
    Vector2,
    forty_to_yards_per_second,
    speed_rating_to_forty,
)

# ============================================================================
# ENUMS
# ============================================================================


class CoverageType(str, Enum):
    """Types of coverage."""

    MAN_PRESS = "MAN_PRESS"
    MAN_OFF = "MAN_OFF"
    ZONE_DEEP = "ZONE_DEEP"
    ZONE_FLAT = "ZONE_FLAT"
    ZONE_HOOK = "ZONE_HOOK"
    SPY = "SPY"


class BreakType(str, Enum):
    """Route break recognition."""

    SLANT = "SLANT"  # 45° inside
    OUT = "OUT"  # 90° outside
    IN = "IN"  # 90° inside
    CORNER = "CORNER"  # 45° up and out
    POST = "POST"  # 45° up and in
    CURL = "CURL"  # Stop and turn
    COMEBACK = "COMEBACK"  # Stop and come back


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class DBState:
    """Current DB state during play."""

    physics: PhysicsState = field(default_factory=PhysicsState)

    # Coverage
    coverage_type: CoverageType = CoverageType.MAN_OFF
    assigned_receiver_id: str | None = None
    zone_position: Vector2 | None = None

    # Tracking
    receiver_distance: float = 5.0
    facing_receiver: bool = True
    hip_turned: bool = False  # Has flipped hips for deep coverage

    # Recognition
    break_recognized: bool = False
    break_recognition_time_ms: float = 0.0


@dataclass(frozen=True)
class DBPhysicsConfig:
    """Configuration for DB physics."""

    # Press coverage
    jam_window_yards: float = 5.0
    jam_success_base: float = 0.5

    # Break recognition
    break_recognition_min_ms: float = 50.0
    break_recognition_max_ms: float = 300.0

    # Interception
    int_window_ms: float = 200.0


# ============================================================================
# DEFENSIVE BACK PHYSICS
# ============================================================================


class DefensiveBackPhysics:
    """
    Physics engine for cornerbacks and safeties.

    Handles:
    - Press coverage and jam
    - Hip-flip for deep routes
    - Break recognition timing
    - Interception attempts
    """

    def __init__(
        self,
        config: DBPhysicsConfig | None = None,
        speed_rating: int = 90,
        acceleration_rating: int = 88,
        agility_rating: int = 88,
        man_coverage_rating: int = 85,
        zone_coverage_rating: int = 80,
        press_rating: int = 80,
        play_recognition_rating: int = 78,
        pursuit_rating: int = 85,
        height_inches: int = 71,
        vertical_jump_inches: int = 38,
    ):
        self.config = config or DBPhysicsConfig()
        self.speed = speed_rating
        self.acceleration = acceleration_rating
        self.agility = agility_rating
        self.man_coverage = man_coverage_rating
        self.zone_coverage = zone_coverage_rating
        self.press = press_rating
        self.play_recognition = play_recognition_rating
        self.pursuit = pursuit_rating
        self.height = height_inches
        self.vertical = vertical_jump_inches

    def execute_press_coverage(
        self,
        state: DBState,
        receiver_release_rating: int,
        receiver_strength: int,
        rng: Any = None,
    ) -> tuple[bool, float]:
        """
        Execute press jam at line of scrimmage.

        Returns:
            Tuple of (jam_successful, delay_yards)
        """
        # Base success from press rating
        base_success = self.config.jam_success_base + (self.press / 200.0)

        # Receiver release counters press
        release_counter = receiver_release_rating / 100.0

        # Strength advantage
        strength_diff = (self.press - receiver_strength) / 100.0 * 0.2

        success_prob = base_success - release_counter * 0.3 + strength_diff
        success_prob = min(0.9, max(0.1, success_prob))

        roll = rng.next_float() if rng else __import__("random").random()
        success = roll < success_prob

        # Calculate delay yards (how far WR got before jam ended)
        if success:
            delay_yards = 1.0 + (1.0 - self.press / 100.0) * 2.0
        else:
            delay_yards = 3.0 + receiver_release_rating / 100.0 * 2.0

        return success, delay_yards

    def calculate_break_recognition_time(
        self,
        break_type: BreakType,
        receiver_route_running: int,
    ) -> float:
        """
        Calculate time to recognize route break.
        Higher play recognition = faster recognition.
        """
        # Base time from play rec rating
        base_time = self.config.break_recognition_max_ms - (self.play_recognition / 100.0) * (
            self.config.break_recognition_max_ms - self.config.break_recognition_min_ms
        )

        # Route sharpness affects recognition
        break_difficulty = {
            BreakType.SLANT: 1.0,
            BreakType.OUT: 0.9,
            BreakType.IN: 0.95,
            BreakType.CORNER: 1.1,
            BreakType.POST: 1.05,
            BreakType.CURL: 0.8,
            BreakType.COMEBACK: 0.85,
        }
        difficulty = break_difficulty.get(break_type, 1.0)

        # Good route runners are harder to read
        rr_penalty = receiver_route_running / 100.0 * 0.3

        return base_time * difficulty * (1.0 + rr_penalty)

    def flip_hips(
        self,
        state: DBState,
        receiver_direction: float,  # Degrees relative to DB
    ) -> tuple[float, float]:
        """
        Execute hip-flip to turn and run with receiver.

        Returns:
            Tuple of (time_to_flip_ms, speed_loss_factor)
        """
        # Time based on agility
        base_flip_time = 200.0
        agility_factor = 100.0 / self.agility
        flip_time = base_flip_time * agility_factor

        # Sharper turns take longer
        angle_factor = abs(receiver_direction) / 180.0
        flip_time *= 1.0 + angle_factor * 0.5

        # Speed loss during flip
        speed_loss = 0.3 + angle_factor * 0.2

        state.hip_turned = True

        return flip_time, 1.0 - speed_loss

    def calculate_interception_probability(
        self,
        ball_position: Vector2,
        db_position: Vector2,
        ball_flight_time_remaining_ms: float,
        receiver_distance: float,
        rng: Any = None,
    ) -> float:
        """
        Calculate probability of interception.

        Requires:
        - Being in position (closer than receiver)
        - Timing the jump correctly
        - Athletic ability to make the play
        """
        distance_to_ball = db_position.distance_to(ball_position)

        # Position advantage
        if distance_to_ball > receiver_distance:
            # Receiver has position - INT unlikely
            position_factor = 0.2
        else:
            position_factor = 1.0 - (distance_to_ball / max(receiver_distance, 0.1))

        # Timing (need enough time to get there)
        time_factor = min(1.0, ball_flight_time_remaining_ms / self.config.int_window_ms)

        # Athletic ability
        athletic_factor = (self.speed + self.agility + self.vertical / 4) / 200.0

        # Coverage rating
        coverage_factor = self.man_coverage / 100.0

        prob = position_factor * time_factor * athletic_factor * coverage_factor * 0.5
        return min(0.5, max(0.01, prob))  # Max 50% INT chance

    def calculate_max_speed(self, fatigue: float = 0.0) -> float:
        """Calculate DB max speed in yards/second."""
        forty = speed_rating_to_forty(self.speed)
        base_speed = forty_to_yards_per_second(forty)
        fatigue_modifier = 1.0 - (fatigue / 200.0)
        return base_speed * fatigue_modifier

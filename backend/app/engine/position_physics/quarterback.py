#!/usr/bin/env python3
"""
Quarterback Physics Module
==========================
Physics-based quarterback mechanics.

Phase 3: Position-Specific Physics
- Throw trajectory with projectile motion
- Pressure timer and accuracy degradation
- Read progression with vision cone
- Scramble decision logic

Context7 Best Practices:
- Dataclasses for state
- Pure functions for calculations
- No magic numbers (all configurable)
"""

import math
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

class ThrowType(str, Enum):
    """Types of throws."""
    SCREEN = "SCREEN"
    SLANT = "SLANT"
    BULLET = "BULLET"
    TOUCH = "TOUCH"
    DEEP = "DEEP"
    LOB = "LOB"
    THROW_AWAY = "THROW_AWAY"


class PocketState(str, Enum):
    """Current state of the pocket."""
    CLEAN = "CLEAN"
    CLOSING = "CLOSING"
    COLLAPSED = "COLLAPSED"
    SCRAMBLING = "SCRAMBLING"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class QBPhysicsConfig:
    """Configuration for QB physics."""
    # Pocket timing
    clean_pocket_threshold_ms: float = 2500.0  # Time before pocket closes
    collapse_threshold_ms: float = 3500.0      # Time to full collapse

    # Throw mechanics
    min_throw_power: float = 25.0   # yards (dump-off)
    max_throw_power: float = 70.0   # yards (elite arm)
    release_time_ms: float = 300.0  # Time from decision to release

    # Accuracy
    base_accuracy_radius: float = 0.5  # yards at optimal
    pressure_accuracy_penalty: float = 0.1  # additional yards per 100ms pressure
    fatigue_accuracy_penalty: float = 0.05  # additional yards per 10% fatigue

    # Vision
    fov_degrees: float = 120.0
    read_time_ms: float = 250.0  # Time per read progression


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ThrowResult:
    """Result of a throw calculation."""
    target_position: Vector2
    actual_position: Vector2  # Where ball actually lands
    velocity: float           # yards/second
    flight_time_ms: float
    accuracy_deviation: float  # yards from target
    is_catchable: bool
    throw_type: ThrowType


@dataclass
class QBState:
    """Current QB state during play."""
    # Position and movement
    physics: PhysicsState = field(default_factory=PhysicsState)

    # Pocket state
    pocket_state: PocketState = PocketState.CLEAN
    time_in_pocket_ms: float = 0.0
    pressure_level: float = 0.0  # 0-100

    # Read progression
    current_read: int = 0
    read_timer_ms: float = 0.0
    reads_available: int = 4  # Primary + 3 progressions

    # Throw preparation
    is_throwing: bool = False
    throw_windup_ms: float = 0.0
    target_receiver_id: str | None = None

    # Scramble
    has_left_pocket: bool = False


# ============================================================================
# QUARTERBACK PHYSICS
# ============================================================================

class QuarterbackPhysics:
    """
    Physics engine for quarterback actions.

    Handles:
    - Throw trajectory and power
    - Accuracy under pressure
    - Pocket movement and scramble
    - Read progression timing
    """

    def __init__(
        self,
        config: QBPhysicsConfig | None = None,
        throw_power_rating: int = 80,
        throw_accuracy_rating: int = 80,
        awareness_rating: int = 80,
        speed_rating: int = 70,
        agility_rating: int = 70,
        poise_rating: int = 75,
    ):
        self.config = config or QBPhysicsConfig()
        self.throw_power = throw_power_rating
        self.throw_accuracy = throw_accuracy_rating
        self.awareness = awareness_rating
        self.speed = speed_rating
        self.agility = agility_rating
        self.poise = poise_rating

        # Derive max throw distance from arm strength
        self._max_throw_yards = self._calculate_max_throw()

    def _calculate_max_throw(self) -> float:
        """Calculate maximum throw distance from rating."""
        # 99 arm = 70 yards, 60 arm = 45 yards
        return 35.0 + (self.throw_power / 100.0) * 35.0

    def update_pocket_state(
        self,
        state: QBState,
        elapsed_ms: float,
        defenders_in_pocket: int = 0,
        closest_defender_distance: float = 10.0,
    ) -> QBState:
        """Update pocket state based on time and pressure."""
        state.time_in_pocket_ms += elapsed_ms

        # Calculate pressure level (0-100)
        distance_pressure = max(0, (5.0 - closest_defender_distance) / 5.0) * 50
        time_pressure = min(50, (state.time_in_pocket_ms / self.config.collapse_threshold_ms) * 50)
        state.pressure_level = min(100, distance_pressure + time_pressure + defenders_in_pocket * 10)

        # Update pocket state
        if state.has_left_pocket:
            state.pocket_state = PocketState.SCRAMBLING
        elif state.time_in_pocket_ms > self.config.collapse_threshold_ms:
            state.pocket_state = PocketState.COLLAPSED
        elif state.time_in_pocket_ms > self.config.clean_pocket_threshold_ms:
            state.pocket_state = PocketState.CLOSING
        else:
            state.pocket_state = PocketState.CLEAN

        return state

    def calculate_throw_trajectory(
        self,
        start_pos: Vector2,
        target_pos: Vector2,
        throw_type: ThrowType,
        pressure_level: float = 0.0,
        fatigue_level: float = 0.0,
        rng: Any = None,
    ) -> ThrowResult:
        """
        Calculate throw trajectory with physics.

        Args:
            start_pos: QB position
            target_pos: Target receiver position
            throw_type: Type of throw
            pressure_level: Current pressure (0-100)
            fatigue_level: Current fatigue (0-100)
            rng: Deterministic RNG for accuracy deviation

        Returns:
            ThrowResult with actual landing position
        """
        distance = start_pos.distance_to(target_pos)

        # Check if throw is possible
        if distance > self._max_throw_yards:
            # Underthrow
            direction = (target_pos - start_pos).normalized
            actual = start_pos + direction * self._max_throw_yards
            return ThrowResult(
                target_position=target_pos,
                actual_position=actual,
                velocity=self._calculate_velocity(distance),
                flight_time_ms=self._calculate_flight_time(distance, throw_type),
                accuracy_deviation=distance - self._max_throw_yards,
                is_catchable=False,
                throw_type=throw_type,
            )

        # Calculate accuracy deviation
        accuracy_radius = self._calculate_accuracy_radius(
            distance, pressure_level, fatigue_level, throw_type
        )

        # Apply random deviation within accuracy radius
        if rng:
            angle = rng.next_float() * 360.0
            deviation = rng.next_float() * accuracy_radius
        else:
            import random
            angle = random.random() * 360.0
            deviation = random.random() * accuracy_radius

        # Calculate actual landing position
        offset = Vector2(
            math.cos(math.radians(angle)) * deviation,
            math.sin(math.radians(angle)) * deviation,
        )
        actual_pos = target_pos + offset

        # Determine if catchable (within receiver's catch radius)
        is_catchable = deviation < 2.0  # 2 yards catch radius

        return ThrowResult(
            target_position=target_pos,
            actual_position=actual_pos,
            velocity=self._calculate_velocity(distance),
            flight_time_ms=self._calculate_flight_time(distance, throw_type),
            accuracy_deviation=deviation,
            is_catchable=is_catchable,
            throw_type=throw_type,
        )

    def _calculate_accuracy_radius(
        self,
        distance: float,
        pressure: float,
        fatigue: float,
        throw_type: ThrowType,
    ) -> float:
        """Calculate accuracy radius (yards from target)."""
        # Base accuracy from rating
        base = self.config.base_accuracy_radius * (100.0 / self.throw_accuracy)

        # Distance penalty (longer throws less accurate)
        distance_factor = 1.0 + (distance / 40.0)

        # Pressure penalty
        pressure_factor = 1.0 + (pressure / 100.0) * self.config.pressure_accuracy_penalty

        # Fatigue penalty
        fatigue_factor = 1.0 + (fatigue / 100.0) * self.config.fatigue_accuracy_penalty

        # Throw type modifiers
        type_mods = {
            ThrowType.SCREEN: 0.5,
            ThrowType.SLANT: 0.8,
            ThrowType.BULLET: 1.0,
            ThrowType.TOUCH: 1.2,
            ThrowType.DEEP: 1.5,
            ThrowType.LOB: 1.8,
            ThrowType.THROW_AWAY: 3.0,
        }
        type_factor = type_mods.get(throw_type, 1.0)

        # Poise reduces pressure impact
        poise_reduction = self.poise / 100.0
        adjusted_pressure_factor = 1.0 + (pressure_factor - 1.0) * (1.0 - poise_reduction * 0.5)

        return base * distance_factor * adjusted_pressure_factor * fatigue_factor * type_factor

    def _calculate_velocity(self, distance: float) -> float:
        """Calculate throw velocity in yards/second."""
        # Longer throws require more velocity
        base_velocity = 20.0 + (self.throw_power / 100.0) * 15.0
        distance_factor = 1.0 + (distance / 50.0) * 0.5
        return base_velocity * distance_factor

    def _calculate_flight_time(self, distance: float, throw_type: ThrowType) -> float:
        """Calculate ball flight time in milliseconds."""
        # Base on velocity and throw type
        velocity = self._calculate_velocity(distance)

        # Air time modifiers
        type_mods = {
            ThrowType.SCREEN: 0.7,
            ThrowType.SLANT: 0.8,
            ThrowType.BULLET: 0.9,
            ThrowType.TOUCH: 1.1,
            ThrowType.DEEP: 1.0,
            ThrowType.LOB: 1.4,
            ThrowType.THROW_AWAY: 1.0,
        }

        base_time = (distance / velocity) * 1000.0  # Convert to ms
        return base_time * type_mods.get(throw_type, 1.0)

    def process_read_progression(
        self,
        state: QBState,
        elapsed_ms: float,
        receiver_openness: list[float],
    ) -> tuple[int, bool]:
        """
        Process read progression.

        Args:
            state: Current QB state
            elapsed_ms: Time elapsed
            receiver_openness: Openness score for each receiver (0-1)

        Returns:
            Tuple of (current_read_index, should_throw)
        """
        state.read_timer_ms += elapsed_ms

        # Time per read adjusted by awareness
        time_per_read = self.config.read_time_ms * (100.0 / self.awareness)

        # Check if advanced to next read
        reads_completed = int(state.read_timer_ms / time_per_read)
        if reads_completed > state.current_read:
            state.current_read = min(reads_completed, len(receiver_openness) - 1)

        # Determine if should throw
        should_throw = False
        if state.current_read < len(receiver_openness):
            openness = receiver_openness[state.current_read]

            # Threshold based on situation
            threshold = 0.6 - (state.pressure_level / 200.0)  # Lower threshold under pressure
            should_throw = openness >= threshold

        return state.current_read, should_throw

    def calculate_scramble_decision(
        self,
        state: QBState,
        run_lanes: list[float],  # Openness of run lanes
    ) -> tuple[bool, int | None]:
        """
        Determine if QB should scramble.

        Returns:
            Tuple of (should_scramble, best_lane_index)
        """
        # Consider scramble if pocket collapsed or high pressure
        pressure_threshold = 70 - (self.poise * 0.2)  # Poised QBs wait longer

        if state.pocket_state == PocketState.COLLAPSED:
            should_scramble = True
        elif state.pressure_level > pressure_threshold:
            should_scramble = True
        elif state.current_read >= state.reads_available - 1:
            # Exhausted reads
            should_scramble = True
        else:
            should_scramble = False

        # Find best lane
        best_lane = None
        if run_lanes and should_scramble:
            best_lane = max(range(len(run_lanes)), key=lambda i: run_lanes[i])

        return should_scramble, best_lane

    def calculate_max_speed(self, fatigue: float = 0.0) -> float:
        """Calculate QB max speed in yards/second."""
        forty = speed_rating_to_forty(self.speed)
        base_speed = forty_to_yards_per_second(forty)
        fatigue_modifier = 1.0 - (fatigue / 200.0)  # 50% fatigue = 75% speed
        return base_speed * fatigue_modifier

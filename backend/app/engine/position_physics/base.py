#!/usr/bin/env python3
"""
Position Physics Base Module
============================
Abstract base and Protocol definitions for position-specific physics.

Phase 3: Position-Specific Physics
- Protocol for consistent physics interface
- Common calculations shared across positions
- Vector math utilities

Context7 Best Practices:
- Protocol for interfaces (not ABC)
- Dataclasses for physics state
- Pure functions for calculations
"""

import math
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

# ============================================================================
# VECTOR UTILITIES
# ============================================================================

@dataclass(frozen=True, slots=True)
class Vector2:
    """Immutable 2D vector for field positions."""
    x: float
    y: float

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def normalized(self) -> 'Vector2':
        mag = self.magnitude
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

    def distance_to(self, other: 'Vector2') -> float:
        return (self - other).magnitude

    def dot(self, other: 'Vector2') -> float:
        return self.x * other.x + self.y * other.y

    def angle_to(self, other: 'Vector2') -> float:
        """Angle to other vector in degrees."""
        delta = other - self
        return math.degrees(math.atan2(delta.y, delta.x))


@dataclass(frozen=True, slots=True)
class Vector3:
    """Immutable 3D vector for trajectory calculations."""
    x: float
    y: float
    z: float

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )


# ============================================================================
# PHYSICS STATE
# ============================================================================

@dataclass
class PhysicsState:
    """Current physics state for a player."""
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    acceleration: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    facing_angle: float = 0.0  # Degrees, 0 = upfield
    speed: float = 0.0  # yards/second

    @property
    def momentum(self) -> float:
        """Momentum magnitude (mass assumed from player weight)."""
        return self.speed


@dataclass
class CollisionResult:
    """Result of a collision/tackle attempt."""
    success: bool
    winner_id: str
    loser_id: str
    yards_after_contact: float = 0.0
    fumble: bool = False
    injury_g_force: float = 0.0


# ============================================================================
# PHYSICS PROTOCOL
# ============================================================================

@runtime_checkable
class PositionPhysics(Protocol):
    """Protocol for position-specific physics implementations."""

    def update(self, delta_time: float, state: PhysicsState) -> PhysicsState:
        """Update physics state for one tick."""
        ...

    def calculate_max_speed(self, player_speed: int, fatigue: float) -> float:
        """Calculate maximum speed in yards/second."""
        ...


# ============================================================================
# COMMON PHYSICS CALCULATIONS
# ============================================================================

# NFL field constants
YARDS_PER_METER = 1.0936
FIELD_LENGTH_YARDS = 100
FIELD_WIDTH_YARDS = 53.33

# Speed conversion: 40-yard dash to yards/second
def forty_to_yards_per_second(forty_time: float) -> float:
    """Convert 40-yard dash time to yards/second."""
    if forty_time <= 0:
        return 0
    return 40.0 / forty_time


def speed_rating_to_forty(speed_rating: int) -> float:
    """Convert 0-100 speed rating to 40-yard time."""
    # 99 speed ≈ 4.25s, 80 speed ≈ 4.55s, 60 speed ≈ 4.85s
    return 5.10 - (speed_rating * 0.0085)


def calculate_acceleration(
    accel_rating: int,
    current_speed: float,
    max_speed: float,
) -> float:
    """
    Calculate acceleration in yards/second².
    Higher rating = faster acceleration.
    """
    if current_speed >= max_speed:
        return 0.0

    # Base acceleration: 0-100 → 3-8 yards/s²
    base_accel = 3.0 + (accel_rating / 100.0) * 5.0

    # Reduce acceleration as approaching max speed
    speed_ratio = current_speed / max_speed if max_speed > 0 else 0
    return base_accel * (1.0 - speed_ratio ** 2)


def calculate_deceleration(
    agility_rating: int,
    current_speed: float,
) -> float:
    """
    Calculate stopping/cutting deceleration.
    Higher agility = faster stops.
    """
    # Base decel: 5-12 yards/s² based on agility
    base_decel = 5.0 + (agility_rating / 100.0) * 7.0
    return base_decel


def calculate_change_of_direction_time(
    agility_rating: int,
    cut_angle: float,
) -> float:
    """
    Time required to change direction.
    Sharper cuts take longer.
    """
    # Base time: 0.1-0.4s depending on angle
    angle_factor = abs(cut_angle) / 180.0
    base_time = 0.1 + (angle_factor * 0.3)

    # Agility reduces this
    agility_factor = 1.0 - (agility_rating / 200.0)
    return base_time * agility_factor


def resolve_momentum_collision(
    player1_weight: int,
    player1_speed: float,
    player2_weight: int,
    player2_speed: float,
    angle_degrees: float,
) -> tuple[float, float]:
    """
    Resolve collision using momentum conservation.
    Returns (player1_final_speed, player2_final_speed).
    """
    angle_rad = math.radians(angle_degrees)

    # Momentum: p = mv
    m1, v1 = player1_weight, player1_speed
    m2, v2 = player2_weight, player2_speed

    # Inelastic collision (players don't bounce)
    # Final velocity weighted by mass
    total_mass = m1 + m2
    if total_mass == 0:
        return 0, 0

    # Project velocities onto collision axis
    v1_component = v1 * math.cos(angle_rad)
    v2_component = v2 * math.cos(angle_rad)

    # Conservation of momentum
    final_v = (m1 * v1_component + m2 * v2_component) / total_mass

    # Distribute based on mass ratio
    return final_v * (m2 / total_mass), final_v * (m1 / total_mass)


def calculate_g_force(
    speed_change: float,
    time_delta: float,
) -> float:
    """
    Calculate G-force from speed change.
    Used for injury probability.
    """
    if time_delta <= 0:
        return 0

    # Acceleration in yards/s²
    accel = abs(speed_change) / time_delta

    # Convert to G's (1G ≈ 10.9 yards/s² on Earth)
    return accel / 10.9

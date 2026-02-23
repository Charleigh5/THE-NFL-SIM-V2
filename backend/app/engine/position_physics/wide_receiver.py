#!/usr/bin/env python3
"""
Wide Receiver Physics Module
============================
Physics-based receiver mechanics.

Phase 3: Position-Specific Physics
- Route running and separation
- Catch physics with radius/hands
- Contested catch calculations
- YAC (reuses RB physics)
"""

from dataclasses import dataclass, field
from enum import Enum

from .base import (
    PhysicsState,
    Vector2,
    forty_to_yards_per_second,
    speed_rating_to_forty,
)

# ============================================================================
# ENUMS
# ============================================================================


class RouteType(str, Enum):
    """Types of routes."""

    SLANT = "SLANT"
    OUT = "OUT"
    IN = "IN"
    CORNER = "CORNER"
    POST = "POST"
    GO = "GO"
    CURL = "CURL"
    COMEBACK = "COMEBACK"
    SCREEN = "SCREEN"
    WHEEL = "WHEEL"


class CatchType(str, Enum):
    """Types of catch situations."""

    WIDE_OPEN = "WIDE_OPEN"
    CONTESTED = "CONTESTED"
    IN_TRAFFIC = "IN_TRAFFIC"
    DIVING = "DIVING"
    JUMPING = "JUMPING"
    SIDELINE = "SIDELINE"
    RAC = "RAC"  # Run after catch


# ============================================================================
# CONFIGURATION
# ============================================================================


@dataclass(frozen=True)
class WRPhysicsConfig:
    """Configuration for WR physics."""

    # Separation thresholds
    open_separation_yards: float = 3.0  # Considered wide open
    contested_threshold_yards: float = 1.5

    # Catch timing
    optimal_timing_window_ms: float = 250.0
    min_catchable_window_ms: float = 500.0

    # Route breaks
    break_speed_retention: float = 0.7


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class CatchAttempt:
    """Data for a catch attempt."""

    ball_position: Vector2
    ball_velocity: float  # yards/second
    timing_offset_ms: float  # + = early, - = late
    defender_distance: float
    catch_type: CatchType


@dataclass
class WRState:
    """Current WR state during play."""

    physics: PhysicsState = field(default_factory=PhysicsState)

    # Route progress
    route_type: RouteType | None = None
    route_depth: float = 0.0  # Yards from LOS
    route_phase: int = 0  # 0=stem, 1=break, 2=separation

    # Separation tracking
    separation: float = 0.0
    defender_id: str | None = None

    # Catch readiness
    hands_ready: bool = False


# ============================================================================
# WIDE RECEIVER PHYSICS
# ============================================================================


class WideReceiverPhysics:
    """
    Physics engine for wide receiver actions.

    Handles:
    - Route running and separation
    - Catch probability calculations
    - Contested catch physics
    - RAC preparation
    """

    def __init__(
        self,
        config: WRPhysicsConfig | None = None,
        speed_rating: int = 90,
        acceleration_rating: int = 88,
        agility_rating: int = 85,
        route_running_rating: int = 85,
        catching_rating: int = 85,
        catch_in_traffic_rating: int = 80,
        spectacular_catch_rating: int = 75,
        release_rating: int = 80,
        height_inches: int = 72,
        vertical_jump_inches: int = 36,
        hand_size_inches: float = 9.5,
    ):
        self.config = config or WRPhysicsConfig()
        self.speed = speed_rating
        self.acceleration = acceleration_rating
        self.agility = agility_rating
        self.route_running = route_running_rating
        self.catching = catching_rating
        self.cit = catch_in_traffic_rating
        self.spectacular = spectacular_catch_rating
        self.release = release_rating
        self.height = height_inches
        self.vertical = vertical_jump_inches
        self.hand_size = hand_size_inches

        # Derived: catch radius in yards
        self._catch_radius = self._calculate_catch_radius()

    def _calculate_catch_radius(self) -> float:
        """Calculate catch radius from physical attributes."""
        # Base from arm span (roughly height * 1.0)
        arm_span_yards = (self.height * 1.0) / 36.0  # inches to yards

        # Add vertical jump reach
        vertical_reach = (self.vertical / 2.0) / 36.0

        # Hand size adds slight bonus
        hand_bonus = (self.hand_size - 9.0) / 36.0

        return arm_span_yards + vertical_reach + hand_bonus

    def calculate_separation(
        self,
        state: WRState,
        route_type: RouteType,
        yards_into_route: float,
        defender_speed: int,
        defender_coverage_rating: int,
        press_coverage: bool = False,
    ) -> float:
        """
        Calculate separation from defender.

        4 phases: release, stem, break, separation
        """
        # Phase 1: Release (0-3 yards)
        if yards_into_route < 3:
            if press_coverage:
                release_factor = self.release / 100.0
                return yards_into_route * release_factor * 0.5
            return yards_into_route * 0.3

        # Phase 2: Stem (3-8 yards)
        elif yards_into_route < 8:
            speed_diff = (self.speed - defender_speed) / 100.0
            return 1.0 + speed_diff * (yards_into_route - 3)

        # Phase 3: Break (at route depth)
        elif state.route_phase == 1:
            # Route running affects break separation
            rr_factor = self.route_running / 100.0
            coverage_factor = (100 - defender_coverage_rating) / 100.0

            # Sharper routes create more separation
            route_sharpness = {
                RouteType.SLANT: 0.8,
                RouteType.OUT: 1.0,
                RouteType.IN: 0.9,
                RouteType.CORNER: 1.1,
                RouteType.POST: 1.0,
                RouteType.GO: 0.3,  # No break
                RouteType.CURL: 1.2,
                RouteType.COMEBACK: 1.3,
                RouteType.SCREEN: 0.5,
                RouteType.WHEEL: 0.9,
            }
            sharpness = route_sharpness.get(route_type, 0.8)

            return 1.5 + rr_factor * coverage_factor * sharpness * 2.0

        # Phase 4: Post-break separation
        else:
            speed_diff = (self.speed - defender_speed) / 100.0
            distance_from_break = yards_into_route - 10  # Assume 10-yard break
            return state.separation + (speed_diff * distance_from_break * 0.3)

    def calculate_catch_probability(
        self,
        catch_attempt: CatchAttempt,
        fatigue: float = 0.0,
    ) -> float:
        """
        Calculate probability of successful catch.

        Based on:
        - Catch type situation
        - Ball timing
        - Defender proximity
        - Catch ratings
        """
        # Base probability from catch rating
        base_prob = 0.5 + (self.catching / 200.0)

        # Timing penalty
        timing_optimal = self.config.optimal_timing_window_ms
        timing_factor = 1.0 - min(1.0, abs(catch_attempt.timing_offset_ms) / timing_optimal * 0.3)

        # Defender proximity penalty
        if catch_attempt.defender_distance < self.config.contested_threshold_yards:
            # Contested catch uses CIT rating
            coverage_penalty = (
                self.config.contested_threshold_yards - catch_attempt.defender_distance
            )
            coverage_factor = 0.7 * (self.cit / 100.0)
        else:
            coverage_factor = 1.0

        # Catch type modifiers
        type_mods = {
            CatchType.WIDE_OPEN: 1.1,
            CatchType.CONTESTED: 0.75,
            CatchType.IN_TRAFFIC: 0.65,
            CatchType.DIVING: 0.5,
            CatchType.JUMPING: 0.7,
            CatchType.SIDELINE: 0.6,
            CatchType.RAC: 0.9,
        }
        type_factor = type_mods.get(catch_attempt.catch_type, 0.8)

        # Spectacular catch for difficult catches
        if catch_attempt.catch_type in [CatchType.DIVING, CatchType.JUMPING]:
            type_factor *= 0.5 + self.spectacular / 200.0

        # Fatigue penalty
        fatigue_factor = 1.0 - (fatigue / 200.0)

        prob = base_prob * timing_factor * coverage_factor * type_factor * fatigue_factor
        return min(0.98, max(0.02, prob))

    def can_reach_ball(
        self,
        player_position: Vector2,
        ball_position: Vector2,
        jumping: bool = False,
    ) -> tuple[bool, float]:
        """
        Check if ball is within catch radius.

        Returns:
            Tuple of (can_reach, reach_difficulty 0-1)
        """
        distance = player_position.distance_to(ball_position)

        effective_radius = self._catch_radius
        if jumping:
            effective_radius += (self.vertical / 36.0) * 0.5  # Extra vertical reach

        can_reach = distance <= effective_radius
        difficulty = min(1.0, distance / effective_radius) if effective_radius > 0 else 1.0

        return can_reach, difficulty

    def calculate_max_speed(self, fatigue: float = 0.0) -> float:
        """Calculate WR max speed in yards/second."""
        forty = speed_rating_to_forty(self.speed)
        base_speed = forty_to_yards_per_second(forty)
        fatigue_modifier = 1.0 - (fatigue / 200.0)
        return base_speed * fatigue_modifier

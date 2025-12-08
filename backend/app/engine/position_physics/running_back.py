#!/usr/bin/env python3
"""
Running Back Physics Module
============================
Physics-based running back mechanics.

Phase 3: Position-Specific Physics
- Momentum-based tackle resolution
- Cut move physics with traction
- Balance and center of gravity
- Yards after contact simulation

Context7 Best Practices:
- Dataclasses for state
- Pure functions for calculations
- Physics-based outcomes
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math

from .base import (
    Vector2, PhysicsState, CollisionResult,
    forty_to_yards_per_second,
    speed_rating_to_forty,
    calculate_acceleration,
    calculate_deceleration,
    calculate_change_of_direction_time,
    resolve_momentum_collision,
    calculate_g_force,
)


# ============================================================================
# ENUMS
# ============================================================================

class CutType(str, Enum):
    """Types of cut moves."""
    JUKE = "JUKE"           # Quick lateral movement
    SPIN = "SPIN"           # 360 rotation
    HURDLE = "HURDLE"       # Jump over tackler
    STIFF_ARM = "STIFF_ARM" # Push off tackler
    TRUCK = "TRUCK"         # Run through tackler
    DEAD_LEG = "DEAD_LEG"   # Plant and acceleration


class ContactType(str, Enum):
    """Type of tackle contact."""
    WRAP_UP = "WRAP_UP"         # Arms around waist
    DIVING = "DIVING"           # Dive at legs
    SHOULDER = "SHOULDER"       # Shoulder hit
    HEAD_ON = "HEAD_ON"         # Direct collision
    ARM_TACKLE = "ARM_TACKLE"   # One arm tackle
    PURSUIT = "PURSUIT"         # Angle pursuit


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class RBPhysicsConfig:
    """Configuration for RB physics."""
    # Balance
    base_balance: float = 50.0    # Center of gravity score
    contact_balance_loss: float = 20.0  # Balance lost per contact

    # Cut moves
    juke_speed_retention: float = 0.8   # Speed kept after juke
    spin_speed_retention: float = 0.6   # Speed kept after spin
    hurdle_success_threshold: float = 0.7

    # Yards after contact
    max_yac_yards: float = 15.0   # Maximum YAC possible
    min_yac_speed: float = 3.0    # Minimum speed to gain YAC


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class TackleAttempt:
    """Data for a tackle attempt."""
    tackler_id: str
    tackler_weight: int
    tackler_speed: float
    tackle_rating: int
    contact_type: ContactType
    approach_angle: float  # Degrees relative to runner direction


@dataclass
class CutMove:
    """Data for an attempted cut move."""
    cut_type: CutType
    direction_change: float  # Degrees
    target_position: Vector2


@dataclass
class RBState:
    """Current RB state during play."""
    physics: PhysicsState = field(default_factory=PhysicsState)

    # Balance (0 = falling, 100 = stable)
    balance: float = 100.0

    # Contact tracking
    contacts_absorbed: int = 0
    yards_after_contact: float = 0.0
    first_contact_position: Optional[Vector2] = None

    # Move cooldowns
    last_cut_time_ms: float = 0.0
    cut_cooldown_ms: float = 500.0

    # Ball security
    ball_security: float = 100.0  # Decreases with fatigue/contact


# ============================================================================
# RUNNING BACK PHYSICS
# ============================================================================

class RunningBackPhysics:
    """
    Physics engine for running back actions.

    Handles:
    - Tackle resolution with momentum
    - Cut moves with traction physics
    - Balance and stumble mechanics
    - Yards after contact simulation
    """

    def __init__(
        self,
        config: Optional[RBPhysicsConfig] = None,
        speed_rating: int = 85,
        acceleration_rating: int = 85,
        agility_rating: int = 85,
        strength_rating: int = 70,
        elusiveness_rating: int = 80,
        trucking_rating: int = 70,
        ball_carrier_vision_rating: int = 80,
        weight: int = 210,
    ):
        self.config = config or RBPhysicsConfig()
        self.speed = speed_rating
        self.acceleration = acceleration_rating
        self.agility = agility_rating
        self.strength = strength_rating
        self.elusiveness = elusiveness_rating
        self.trucking = trucking_rating
        self.vision = ball_carrier_vision_rating
        self.weight = weight

    def resolve_tackle_attempt(
        self,
        state: RBState,
        tackle: TackleAttempt,
        fatigue: float = 0.0,
        rng: Any = None,
    ) -> CollisionResult:
        """
        Resolve a tackle attempt using momentum physics.

        Returns:
            CollisionResult with outcome
        """
        # Calculate momentum for both players
        runner_momentum = self.weight * state.physics.speed
        tackler_momentum = tackle.tackler_weight * tackle.tackler_speed

        # Angle modifier (direct tackles more effective)
        angle_effectiveness = abs(math.cos(math.radians(tackle.approach_angle)))
        adjusted_tackler_momentum = tackler_momentum * (0.5 + 0.5 * angle_effectiveness)

        # Calculate tackle probability
        base_prob = self._calculate_tackle_probability(
            runner_momentum,
            adjusted_tackler_momentum,
            tackle.tackle_rating,
            tackle.contact_type,
        )

        # Modify by ratings
        elusiveness_mod = (100 - self.elusiveness) / 100.0  # Lower elusiveness = easier to tackle
        trucking_mod = self.trucking / 100.0
        fatigue_mod = 1.0 + (fatigue / 200.0)  # Fatigue increases tackle chance

        tackle_prob = base_prob * elusiveness_mod * fatigue_mod

        # Roll for tackle
        roll = rng.next_float() if rng else __import__('random').random()

        # Calculate G-force for injury check
        speed_change = abs(state.physics.speed - tackle.tackler_speed * 0.5)
        g_force = calculate_g_force(speed_change, 0.1)  # 100ms impact

        if roll < tackle_prob:
            # Tackle successful
            return CollisionResult(
                success=True,
                winner_id=tackle.tackler_id,
                loser_id="runner",
                yards_after_contact=0.0,
                fumble=self._check_fumble(state, g_force, rng),
                injury_g_force=g_force,
            )
        else:
            # Broken tackle - calculate YAC
            new_speed = self._calculate_post_contact_speed(
                state.physics.speed,
                tackle.tackler_speed,
                tackle.contact_type,
            )

            # Update state
            state.contacts_absorbed += 1
            state.balance -= self.config.contact_balance_loss
            state.physics.speed = new_speed

            if state.first_contact_position is None:
                state.first_contact_position = state.physics.position

            return CollisionResult(
                success=False,
                winner_id="runner",
                loser_id=tackle.tackler_id,
                yards_after_contact=self._estimate_yac(new_speed, state.balance),
                fumble=self._check_fumble(state, g_force * 0.5, rng),
                injury_g_force=g_force * 0.7,  # Reduced for broken tackle
            )

    def _calculate_tackle_probability(
        self,
        runner_momentum: float,
        tackler_momentum: float,
        tackle_rating: int,
        contact_type: ContactType,
    ) -> float:
        """Calculate base tackle success probability."""
        # Momentum ratio
        if runner_momentum == 0:
            momentum_factor = 1.0
        else:
            momentum_factor = tackler_momentum / (runner_momentum + tackler_momentum)

        # Tackle rating contribution
        rating_factor = tackle_rating / 100.0

        # Contact type modifiers
        type_mods = {
            ContactType.WRAP_UP: 1.2,      # Best tackle technique
            ContactType.DIVING: 0.7,        # Risky
            ContactType.SHOULDER: 0.9,
            ContactType.HEAD_ON: 1.0,
            ContactType.ARM_TACKLE: 0.5,    # Worst
            ContactType.PURSUIT: 0.85,
        }
        type_factor = type_mods.get(contact_type, 1.0)

        # Combine factors
        base_prob = 0.4 + (momentum_factor * 0.3) + (rating_factor * 0.3)
        return min(0.95, max(0.1, base_prob * type_factor))

    def _calculate_post_contact_speed(
        self,
        runner_speed: float,
        tackler_speed: float,
        contact_type: ContactType,
    ) -> float:
        """Calculate runner speed after breaking tackle."""
        # Momentum loss factors by contact type
        loss_factors = {
            ContactType.WRAP_UP: 0.5,
            ContactType.DIVING: 0.7,
            ContactType.SHOULDER: 0.6,
            ContactType.HEAD_ON: 0.4,
            ContactType.ARM_TACKLE: 0.8,
            ContactType.PURSUIT: 0.65,
        }

        retention = loss_factors.get(contact_type, 0.6)
        return runner_speed * retention

    def _estimate_yac(self, speed: float, balance: float) -> float:
        """Estimate yards after contact based on current state."""
        if speed < self.config.min_yac_speed:
            return 0

        # YAC based on speed and balance
        speed_factor = speed / 10.0  # Normalize
        balance_factor = balance / 100.0

        return min(self.config.max_yac_yards, speed_factor * balance_factor * 5)

    def _check_fumble(
        self,
        state: RBState,
        g_force: float,
        rng: Any = None,
    ) -> bool:
        """Check for fumble on contact."""
        # Base fumble rate: 1-2% per carry
        base_rate = 0.015

        # G-force increases fumble risk
        g_force_mod = 1.0 + (g_force / 20.0)

        # Ball security rating reduces risk
        security_mod = (100 - state.ball_security) / 100.0 * 0.5 + 0.5

        # Multiple contacts increase risk
        contact_mod = 1.0 + (state.contacts_absorbed * 0.1)

        fumble_prob = base_rate * g_force_mod * security_mod * contact_mod

        roll = rng.next_float() if rng else __import__('random').random()
        return roll < fumble_prob

    def execute_cut_move(
        self,
        state: RBState,
        cut: CutMove,
        surface_traction: float = 1.0,  # 1.0 = normal, <1 = slippery
        fatigue: float = 0.0,
        rng: Any = None,
    ) -> Tuple[bool, float, float]:
        """
        Execute a cut move.

        Args:
            state: Current RB state
            cut: Cut move to attempt
            surface_traction: Surface friction (weather/turf)
            fatigue: Current fatigue level
            rng: Deterministic RNG

        Returns:
            Tuple of (success, new_speed, g_force)
        """
        # Check cooldown
        if state.last_cut_time_ms < state.cut_cooldown_ms:
            return False, state.physics.speed, 0

        # Calculate success probability
        success_prob = self._calculate_cut_success(
            cut.cut_type,
            cut.direction_change,
            state.physics.speed,
            surface_traction,
            fatigue,
        )

        roll = rng.next_float() if rng else __import__('random').random()
        success = roll < success_prob

        # Calculate G-force from direction change
        g_force = calculate_g_force(
            state.physics.speed * math.sin(math.radians(cut.direction_change)),
            calculate_change_of_direction_time(self.agility, cut.direction_change),
        )

        if success:
            # Apply speed retention based on cut type
            retentions = {
                CutType.JUKE: self.config.juke_speed_retention,
                CutType.SPIN: self.config.spin_speed_retention,
                CutType.HURDLE: 0.7,
                CutType.STIFF_ARM: 0.9,
                CutType.TRUCK: 0.85,
                CutType.DEAD_LEG: 0.75,
            }
            new_speed = state.physics.speed * retentions.get(cut.cut_type, 0.8)
        else:
            # Failed cut = stumble
            new_speed = state.physics.speed * 0.4
            state.balance -= 30

        state.last_cut_time_ms = 0  # Reset cooldown
        return success, new_speed, g_force

    def _calculate_cut_success(
        self,
        cut_type: CutType,
        direction_change: float,
        current_speed: float,
        traction: float,
        fatigue: float,
    ) -> float:
        """Calculate probability of successful cut."""
        # Base success from agility
        base = 0.5 + (self.agility / 200.0)

        # Sharper cuts are harder
        angle_penalty = abs(direction_change) / 180.0 * 0.3

        # Speed penalty (harder to cut at full speed)
        max_speed = forty_to_yards_per_second(speed_rating_to_forty(self.speed))
        speed_penalty = (current_speed / max_speed) * 0.2

        # Surface traction
        traction_mod = 0.5 + (traction * 0.5)

        # Fatigue penalty
        fatigue_penalty = fatigue / 200.0

        # Cut type difficulty
        type_mods = {
            CutType.JUKE: 1.0,
            CutType.SPIN: 0.85,
            CutType.HURDLE: 0.7,
            CutType.STIFF_ARM: 0.9,
            CutType.TRUCK: 0.8,
            CutType.DEAD_LEG: 0.95,
        }

        prob = (base - angle_penalty - speed_penalty - fatigue_penalty) * traction_mod
        return min(0.95, max(0.1, prob * type_mods.get(cut_type, 1.0)))

    def calculate_max_speed(self, fatigue: float = 0.0) -> float:
        """Calculate RB max speed in yards/second."""
        forty = speed_rating_to_forty(self.speed)
        base_speed = forty_to_yards_per_second(forty)
        fatigue_modifier = 1.0 - (fatigue / 200.0)
        return base_speed * fatigue_modifier

#!/usr/bin/env python3
"""
Pass Rush Physics Module
========================
Physics for Defensive Ends and Edge Rushers.

Phase 3: Position-Specific Physics
- Pass rush simulation at 60Hz
- Power vs finesse move selection
- First-step explosion
- Sack/TFL physics
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math

from .base import (
    Vector2, PhysicsState, CollisionResult,
    forty_to_yards_per_second,
    speed_rating_to_forty,
    calculate_g_force,
)


# ============================================================================
# ENUMS
# ============================================================================

class RushMove(str, Enum):
    """Types of pass rush moves."""
    BULL_RUSH = "BULL_RUSH"       # Power move straight ahead
    SPEED_RUSH = "SPEED_RUSH"     # Speed around the edge
    SPIN_MOVE = "SPIN_MOVE"       # Inside spin
    RIP_MOVE = "RIP_MOVE"         # Rip under arm
    SWIM_MOVE = "SWIM_MOVE"       # Swim over arm
    CLUB_SWIPE = "CLUB_SWIPE"     # Club arm, swipe by
    STUNT = "STUNT"               # Cross with another DL


class BlockerStance(str, Enum):
    """Blocker's current stance."""
    SET = "SET"           # Ready position
    LUNGING = "LUNGING"   # Overcommitted
    RECOVERING = "RECOVERING"  # Off balance


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class PassRushRep:
    """Single pass rush rep state."""
    rusher_position: Vector2
    blocker_position: Vector2
    qb_position: Vector2

    # Battle state
    rush_move: Optional[RushMove] = None
    blocker_stance: BlockerStance = BlockerStance.SET
    leverage_score: float = 0.0  # -1 to 1- = blocker winning, + = rusher winning

    # Timing
    elapsed_ms: float = 0.0
    move_started_ms: float = 0.0

    # Outcome tracking
    pressure_generated: bool = False
    sack_achieved: bool = False


@dataclass(frozen=True)
class PassRushConfig:
    """Configuration for pass rush physics."""
    # Timing
    typical_pass_time_ms: float = 2500.0
    first_step_window_ms: float = 200.0

    # Movement
    speed_rush_angle: float = 45.0  # Degrees from LOS
    bull_rush_threshold: float = 0.3  # Leverage to start pushing


# ============================================================================
# PASS RUSH PHYSICS
# ============================================================================

class PassRushPhysics:
    """
    Physics engine for pass rushers.

    Handles:
    - Frame-by-frame rush simulation
    - Move selection AI
    - Leverage calculations
    - Sack/pressure outcomes
    """

    def __init__(
        self,
        config: Optional[PassRushConfig] = None,
        speed_rating: int = 80,
        acceleration_rating: int = 85,
        strength_rating: int = 85,
        power_move_rating: int = 80,
        finesse_move_rating: int = 75,
        block_shedding_rating: int = 80,
        pursuit_rating: int = 82,
        weight: int = 265,
    ):
        self.config = config or PassRushConfig()
        self.speed = speed_rating
        self.acceleration = acceleration_rating
        self.strength = strength_rating
        self.power_move = power_move_rating
        self.finesse_move = finesse_move_rating
        self.block_shedding = block_shedding_rating
        self.pursuit = pursuit_rating
        self.weight = weight

    def select_rush_move(
        self,
        blocker_strength: int,
        blocker_agility: int,
        distance_to_qb: float,
        rng: Any = None,
    ) -> RushMove:
        """
        AI-driven rush move selection.

        Considers:
        - Strength matchup for power moves
        - Agility matchup for finesse moves
        - Distance (speed rush needs room)
        """
        # Calculate matchup scores
        power_advantage = (self.strength + self.power_move) / 2 - blocker_strength
        finesse_advantage = (self.finesse_move + self.speed) / 2 - blocker_agility

        # Distance affects speed rush viability
        if distance_to_qb > 7:
            finesse_advantage += 10  # More room for speed
        else:
            power_advantage += 5  # Closer = bull rush viable

        # Build weighted options
        options = []

        if power_advantage > 0:
            options.extend([
                (RushMove.BULL_RUSH, 30 + power_advantage),
                (RushMove.CLUB_SWIPE, 15 + power_advantage * 0.5),
            ])

        if finesse_advantage > 0:
            options.extend([
                (RushMove.SPEED_RUSH, 25 + finesse_advantage),
                (RushMove.SPIN_MOVE, 15 + finesse_advantage * 0.8),
                (RushMove.RIP_MOVE, 20 + finesse_advantage * 0.5),
                (RushMove.SWIM_MOVE, 15 + finesse_advantage * 0.7),
            ])

        if not options:
            options = [(RushMove.BULL_RUSH, 50), (RushMove.SPEED_RUSH, 50)]

        # Weighted random selection
        total = sum(w for _, w in options)
        roll = (rng.next_float() if rng else __import__('random').random()) * total

        cumulative = 0
        for move, weight in options:
            cumulative += weight
            if roll <= cumulative:
                return move

        return options[0][0]

    def simulate_rush_tick(
        self,
        rep: PassRushRep,
        blocker_pass_block: int,
        blocker_strength: int,
        tick_ms: float = 16.67,  # 60Hz
        rng: Any = None,
    ) -> PassRushRep:
        """
        Simulate one tick of pass rush.

        Returns updated rep state.
        """
        rep.elapsed_ms += tick_ms

        # First step advantage (first 200ms)
        if rep.elapsed_ms < self.config.first_step_window_ms:
            first_step_bonus = self._calculate_first_step_advantage(
                rep.rush_move, tick_ms
            )
            rep.leverage_score += first_step_bonus

        # Move execution
        if rep.rush_move:
            move_result = self._execute_move_tick(
                rep, blocker_pass_block, blocker_strength, tick_ms, rng
            )
            rep.leverage_score += move_result

        # Check if pressure/sack achieved
        distance_to_qb = rep.rusher_position.distance_to(rep.qb_position)

        if rep.leverage_score > 0.5 and distance_to_qb < 2:
            rep.pressure_generated = True
            if rep.leverage_score > 0.8 and distance_to_qb < 1:
                rep.sack_achieved = True

        # Clamp leverage
        rep.leverage_score = max(-1.0, min(1.0, rep.leverage_score))

        return rep

    def _calculate_first_step_advantage(
        self,
        rush_move: Optional[RushMove],
        tick_ms: float,
    ) -> float:
        """Calculate first-step explosion advantage."""
        # Acceleration rating drives first step
        base_advantage = (self.acceleration / 100.0) * 0.02 * (tick_ms / 16.67)

        # Speed rush gets more from first step
        if rush_move == RushMove.SPEED_RUSH:
            base_advantage *= 1.3

        return base_advantage

    def _execute_move_tick(
        self,
        rep: PassRushRep,
        blocker_pass_block: int,
        blocker_strength: int,
        tick_ms: float,
        rng: Any = None,
    ) -> float:
        """Execute one tick of the current rush move."""
        move = rep.rush_move

        # Power moves: strength vs strength
        if move in [RushMove.BULL_RUSH, RushMove.CLUB_SWIPE]:
            strength_diff = (self.strength + self.power_move - blocker_strength - blocker_pass_block) / 200.0
            return strength_diff * 0.01 * (tick_ms / 16.67)

        # Finesse moves: agility/finesse vs pass block technique
        elif move in [RushMove.SPEED_RUSH, RushMove.SPIN_MOVE, RushMove.RIP_MOVE, RushMove.SWIM_MOVE]:
            finesse_diff = (self.finesse_move + self.speed - blocker_pass_block) / 200.0

            # Spin/swim have higher variance
            if move in [RushMove.SPIN_MOVE, RushMove.SWIM_MOVE]:
                roll = rng.next_float() if rng else __import__('random').random()
                if roll > 0.7:
                    finesse_diff *= 2.0  # Big win
                elif roll < 0.2:
                    finesse_diff *= -0.5  # Blocked

            return finesse_diff * 0.015 * (tick_ms / 16.67)

        return 0

    def calculate_sack_momentum(
        self,
        rusher_speed: float,
        qb_weight: int,
    ) -> Tuple[float, float]:
        """
        Calculate sack outcome using momentum.

        Returns:
            Tuple of (yards_lost, g_force)
        """
        # Momentum: p = mv
        rusher_momentum = self.weight * rusher_speed
        qb_momentum = qb_weight * 2.0  # QB assumed ~2 yards/s

        # Net momentum determines yards lost
        net_momentum = rusher_momentum - qb_momentum
        yards_lost = max(0, net_momentum / (self.weight + qb_weight) * 0.5)

        # G-force for injury check
        g_force = calculate_g_force(rusher_speed, 0.15)

        return yards_lost, g_force

    def calculate_strip_sack_probability(
        self,
        rep: PassRushRep,
        qb_ball_security: int,
    ) -> float:
        """
        Calculate probability of strip sack.

        Higher with finesse moves (more control).
        """
        base_prob = 0.1 * (rep.leverage_score + 1.0) / 2.0

        # Finesse moves better for strip
        if rep.rush_move in [RushMove.RIP_MOVE, RushMove.SWIM_MOVE, RushMove.CLUB_SWIPE]:
            base_prob *= 1.5

        # Ball security reduces chance
        security_mod = (100 - qb_ball_security) / 100.0

        return min(0.25, base_prob * security_mod)

    def calculate_max_speed(self, fatigue: float = 0.0) -> float:
        """Calculate edge rusher max speed."""
        forty = speed_rating_to_forty(self.speed)
        base_speed = forty_to_yards_per_second(forty)
        fatigue_modifier = 1.0 - (fatigue / 200.0)
        return base_speed * fatigue_modifier

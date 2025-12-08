#!/usr/bin/env python3
"""
Offensive Line Physics Module
=============================
Physics for pass and run blocking.

Phase 3: Position-Specific Physics
- Zero-suction blocking
- Deterministic assignments
- Sustain/counter battle loops
- Pocket contour calculation
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import math

from .base import Vector2, PhysicsState


# ============================================================================
# ENUMS
# ============================================================================

class BlockType(str, Enum):
    """Types of blocks."""
    PASS_SET = "PASS_SET"
    DRIVE_BLOCK = "DRIVE_BLOCK"
    REACH_BLOCK = "REACH_BLOCK"
    DOUBLE_TEAM = "DOUBLE_TEAM"
    PULL = "PULL"
    CUT_BLOCK = "CUT_BLOCK"
    CHIP = "CHIP"


class GapResponsibility(str, Enum):
    """Gap assignments."""
    A_GAP_LEFT = "A_GAP_LEFT"
    A_GAP_RIGHT = "A_GAP_RIGHT"
    B_GAP_LEFT = "B_GAP_LEFT"
    B_GAP_RIGHT = "B_GAP_RIGHT"
    C_GAP_LEFT = "C_GAP_LEFT"
    C_GAP_RIGHT = "C_GAP_RIGHT"
    EDGE = "EDGE"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class BlockerState:
    """Current blocker state."""
    physics: PhysicsState = field(default_factory=PhysicsState)

    # Assignment
    block_type: BlockType = BlockType.PASS_SET
    assigned_defender_id: Optional[str] = None
    gap: Optional[GapResponsibility] = None

    # Battle state
    win_score: float = 0.0  # -1 to 1 (-1 = lost, 1 = won)
    is_engaged: bool = False
    hand_placement: str = "inside"  # inside = good, outside = bad

    # Penalties
    holding_risk: float = 0.0  # 0-1, >0.9 = holding called


@dataclass(frozen=True)
class OLPhysicsConfig:
    """Configuration for OL physics."""
    # Engagement
    engagement_range_yards: float = 1.5

    # Battle thresholds
    win_threshold: float = 0.5
    loss_threshold: float = -0.5
    holding_threshold: float = -0.9

    # Pocket dimensions
    ideal_pocket_width_yards: float = 4.0
    ideal_pocket_depth_yards: float = 5.0


# ============================================================================
# OFFENSIVE LINE PHYSICS
# ============================================================================

class OffensiveLinePhysics:
    """
    Physics engine for offensive linemen.

    Handles:
    - Pass protection battles
    - Run blocking assignments
    - Pocket shape calculation
    - Holding/penalty emergence
    """

    def __init__(
        self,
        config: Optional[OLPhysicsConfig] = None,
        strength_rating: int = 85,
        pass_block_rating: int = 80,
        run_block_rating: int = 82,
        pass_block_power_rating: int = 78,
        pass_block_finesse_rating: int = 75,
        awareness_rating: int = 75,
        weight: int = 310,
    ):
        self.config = config or OLPhysicsConfig()
        self.strength = strength_rating
        self.pass_block = pass_block_rating
        self.run_block = run_block_rating
        self.pass_block_power = pass_block_power_rating
        self.pass_block_finesse = pass_block_finesse_rating
        self.awareness = awareness_rating
        self.weight = weight

    def process_pass_block_tick(
        self,
        state: BlockerState,
        rusher_power_move: int,
        rusher_finesse_move: int,
        rush_move_type: str,
        tick_ms: float = 16.67,
        rng: Any = None,
    ) -> BlockerState:
        """
        Process one tick of pass blocking.
        Uses zero-suction (blocker can miss).
        """
        if not state.is_engaged:
            return state

        # Determine battle type
        is_power = rush_move_type in ["BULL_RUSH", "CLUB_SWIPE"]

        if is_power:
            # Power vs power
            diff = (self.pass_block_power + self.strength - rusher_power_move) / 200.0
        else:
            # Finesse vs finesse
            diff = (self.pass_block_finesse - rusher_finesse_move) / 100.0

        # Add variance
        roll = rng.next_float() if rng else __import__('random').random()
        variance = (roll - 0.5) * 0.1

        # Update win score
        state.win_score += (diff * 0.01 + variance * 0.02) * (tick_ms / 16.67)

        # Check for holding (losing badly)
        if state.win_score < self.config.holding_threshold:
            # Lineman grabs to avoid giving up sack
            state.holding_risk = min(1.0, state.holding_risk + 0.1)

        # Clamp
        state.win_score = max(-1.0, min(1.0, state.win_score))

        return state

    def assign_blockers(
        self,
        blockers: List[Tuple[str, Vector2]],
        rushers: List[Tuple[str, Vector2]],
    ) -> Dict[str, Optional[str]]:
        """
        Deterministic blocker assignment.
        No double-targeting allowed.

        Returns:
            Dict of blocker_id -> rusher_id assignments
        """
        assignments = {}
        available_rushers = set(r[0] for r in rushers)

        # Sort blockers by x position (left to right)
        sorted_blockers = sorted(blockers, key=lambda b: b[1].x)

        for blocker_id, blocker_pos in sorted_blockers:
            if not available_rushers:
                assignments[blocker_id] = None
                continue

            # Find closest available rusher
            best_rusher = None
            best_distance = float('inf')

            for rusher_id, rusher_pos in rushers:
                if rusher_id not in available_rushers:
                    continue

                dist = blocker_pos.distance_to(rusher_pos)
                if dist < best_distance:
                    best_distance = dist
                    best_rusher = rusher_id

            if best_rusher:
                assignments[blocker_id] = best_rusher
                available_rushers.remove(best_rusher)
            else:
                assignments[blocker_id] = None

        return assignments

    def calculate_pocket_contour(
        self,
        blocker_positions: List[Vector2],
        qb_position: Vector2,
    ) -> Dict[str, float]:
        """
        Calculate pocket shape from blocker positions.

        Returns:
            Dict with pocket metrics
        """
        if not blocker_positions:
            return {
                "width": 0,
                "depth": 0,
                "shape_score": 0,
                "left_edge": 0,
                "right_edge": 0,
            }

        # Calculate pocket bounds
        xs = [p.x for p in blocker_positions]
        ys = [p.y for p in blocker_positions]

        width = max(xs) - min(xs)

        # Depth is distance from QB to closest blocker
        depths = [p.distance_to(qb_position) for p in blocker_positions]
        depth = min(depths) if depths else 0

        # Shape score (how close to ideal)
        width_score = min(1.0, width / self.config.ideal_pocket_width_yards)
        depth_score = min(1.0, depth / self.config.ideal_pocket_depth_yards)
        shape_score = (width_score + depth_score) / 2

        return {
            "width": width,
            "depth": depth,
            "shape_score": shape_score,
            "left_edge": min(xs),
            "right_edge": max(xs),
        }

    def check_holding_penalty(
        self,
        state: BlockerState,
        rng: Any = None,
    ) -> bool:
        """
        Check if holding penalty occurs.
        """
        if state.holding_risk < 0.7:
            return False

        # Base probability from holding risk
        prob = (state.holding_risk - 0.7) / 0.3 * 0.5  # Max 50% at full risk

        roll = rng.next_float() if rng else __import__('random').random()
        return roll < prob

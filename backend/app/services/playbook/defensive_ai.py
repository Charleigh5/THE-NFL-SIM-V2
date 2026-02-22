#!/usr/bin/env python3
"""
Defensive AI Module
===================
Defensive coordinator decision-making.

Phase 9: Playbook & AI
- Coverage shell selection
- Blitz packages
- Situational adjustments
"""

import random
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================


class CoverageType(str, Enum):
    """Pass coverage schemes."""

    COVER_0 = "COVER_0"  # All-out blitz, man
    COVER_1 = "COVER_1"  # Single high safety, man
    COVER_2 = "COVER_2"  # Two deep safeties, zone
    COVER_3 = "COVER_3"  # Three deep, zone
    COVER_4 = "COVER_4"  # Quarters, zone
    COVER_6 = "COVER_6"  # Quarter-quarter-half


class BlitzPackage(str, Enum):
    """Pressure types."""

    NONE = "NONE"
    LB_BLITZ = "LB_BLITZ"
    CB_BLITZ = "CB_BLITZ"
    SAFETY_BLITZ = "SAFETY_BLITZ"
    ALL_OUT = "ALL_OUT"


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class DefensiveCall:
    """A defensive playcall."""

    coverage: CoverageType
    blitz: BlitzPackage
    description: str


@dataclass
class DefensiveGameplan:
    """DC's strategy settings."""

    base_coverage: CoverageType = CoverageType.COVER_3
    blitz_frequency: float = 0.20  # 20% of plays
    man_coverage_pct: float = 0.30


# ============================================================================
# DEFENSIVE COORDINATOR AI
# ============================================================================


class DefensiveCoordinatorAI:
    """
    Defensive play caller.
    """

    def __init__(self, gameplan: DefensiveGameplan):
        self.gameplan = gameplan

    def call_defense(
        self, down: int, distance: int, predicted_pass_pct: float = 0.5
    ) -> DefensiveCall:
        """
        Select defensive coverage and pressure.
        """
        # 1. Determine if blitzing
        should_blitz = self._should_blitz(down, distance, predicted_pass_pct)

        # 2. Select coverage
        coverage = self._select_coverage(down, distance, predicted_pass_pct, should_blitz)

        # 3. Build call
        if should_blitz:
            blitz = self._pick_blitz_package(down, distance)
        else:
            blitz = BlitzPackage.NONE

        return DefensiveCall(
            coverage=coverage, blitz=blitz, description=f"{coverage.value} with {blitz.value}"
        )

    def _should_blitz(self, down: int, distance: int, pass_pct: float) -> bool:
        """Decide whether to send pressure."""
        # Base rate
        roll = random.random()

        # Increase blitz on obvious passing downs
        if down == 3 and distance > 7:
            threshold = self.gameplan.blitz_frequency * 1.5
        else:
            threshold = self.gameplan.blitz_frequency

        return roll < threshold

    def _select_coverage(
        self, down: int, distance: int, pass_pct: float, blitzing: bool
    ) -> CoverageType:
        """Choose coverage shell."""

        # If blitzing, lock to man
        if blitzing:
            return CoverageType.COVER_1

        # Long yardage: Prevent deep balls
        if distance >= 15:
            return CoverageType.COVER_2  # Two deep safeties

        # Short yardage: Press, aggressive
        if distance <= 3:
            return CoverageType.COVER_1  # Man coverage

        # Default to base
        return self.gameplan.base_coverage

    def _pick_blitz_package(self, down: int, distance: int) -> BlitzPackage:
        """Select which players to send."""
        packages = [BlitzPackage.LB_BLITZ, BlitzPackage.CB_BLITZ, BlitzPackage.SAFETY_BLITZ]

        # Critical down: All out
        if down == 3 and distance > 10:
            return BlitzPackage.ALL_OUT

        return random.choice(packages)

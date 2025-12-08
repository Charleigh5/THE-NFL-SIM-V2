#!/usr/bin/env python3
"""
Momentum Engine Module
======================
Dynamic momentum and morale tracking.

Phase 6: SOCIETY Locker Room Dynamics
- In-game momentum swings
- Season morale trends
- "Flow State" mechanics
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class MomentumState(str, Enum):
    """Overall momentum state."""
    COLD = "COLD"             # Struggling
    NEUTRAL = "NEUTRAL"
    HEATING_UP = "HEATING_UP" # Stringing plays together
    ON_FIRE = "ON_FIRE"       # Unstoppable (Flow State)
    ICE_COLD = "ICE_COLD"     # Demoralized


class MomentumEvent(str, Enum):
    """Events that shift momentum."""
    TOUCHDOWN = "TOUCHDOWN"
    TURNOVER = "TURNOVER"
    SACK = "SACK"
    BIG_PLAY_OFFENSE = "BIG_PLAY_OFFENSE" # 20+ yards
    THRD_DOWN_STOP = "THRD_DOWN_STOP"
    MISSED_FG = "MISSED_FG"
    TIMEOUT = "TIMEOUT" # Can freeze momentum


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class TeamMomentum:
    """Momentum state for a team."""
    team_id: str
    score: float = 50.0  # 0-100 scale, 50 neutral
    consecutive_successes: int = 0
    state: MomentumState = MomentumState.NEUTRAL

    def update(self, delta: float) -> None:
        """Adjust momentum score."""
        self.score = max(0.0, min(100.0, self.score + delta))
        self._update_state()

    def _update_state(self) -> None:
        if self.score >= 90:
            self.state = MomentumState.ON_FIRE
        elif self.score >= 70:
            self.state = MomentumState.HEATING_UP
        elif self.score <= 10:
            self.state = MomentumState.ICE_COLD
        elif self.score <= 30:
            self.state = MomentumState.COLD
        else:
            self.state = MomentumState.NEUTRAL


# ============================================================================
# MOMENTUM ENGINE
# ============================================================================

class MomentumEngine:
    """
    Tracks and applies momentum effects.

    "Big Mo" creates streaks and slumps.
    """

    def __init__(self):
        self.teams: Dict[str, TeamMomentum] = {}

    def get_team_momentum(self, team_id: str) -> TeamMomentum:
        """Get or create team momentum state."""
        if team_id not in self.teams:
            self.teams[team_id] = TeamMomentum(team_id=team_id)
        return self.teams[team_id]

    def process_event(self, team_id: str, event: MomentumEvent) -> None:
        """
        Process a momentum-shifting event.
        """
        momentum = self.get_team_momentum(team_id)

        # Base modifiers
        shifts = {
            MomentumEvent.TOUCHDOWN: 15.0,
            MomentumEvent.TURNOVER: -20.0, # Huge swing
            MomentumEvent.SACK: -5.0,
            MomentumEvent.BIG_PLAY_OFFENSE: 8.0,
            MomentumEvent.THRD_DOWN_STOP: 5.0,
            MomentumEvent.MISSED_FG: -10.0,
            MomentumEvent.TIMEOUT: 0.0, # Special logic
        }

        shift = shifts.get(event, 0.0)

        # Context modifiers (simplified)
        # Momentum begets momentum (easier to stay hot)
        if momentum.state == MomentumState.ON_FIRE and shift > 0:
            shift *= 1.2
        elif momentum.state == MomentumState.ICE_COLD and shift < 0:
            shift *= 1.2

        # Timeout "Icing" logic
        if event == MomentumEvent.TIMEOUT:
            # Brings scores closer to neutral
            if momentum.score > 50:
                momentum.update(-(momentum.score - 50) * 0.3)
            elif momentum.score < 50:
                momentum.update((50 - momentum.score) * 0.3)
        else:
            momentum.update(shift)

            # Update streaks
            if shift > 0:
                momentum.consecutive_successes += 1
            elif shift < 0:
                momentum.consecutive_successes = 0

    def get_performance_modifier(self, team_id: str) -> float:
        """
        Get attribute modifier based on momentum.

        ON_FIRE = ~1.10x
        ICE_COLD = ~0.90x
        """
        momentum = self.get_team_momentum(team_id)

        # Map 0-100 score to 0.90-1.10 multiplier
        # (Score - 50) / 50 * 0.1 + 1.0
        # 100 -> 50/50 * 0.1 + 1 = 1.1
        # 0 -> -50/50 * 0.1 + 1 = 0.9

        modifier = ((momentum.score - 50.0) / 50.0) * 0.1 + 1.0
        return modifier

    def reset_momentum(self, team_id: str) -> None:
        """Reset momentum to neutral (e.g. halftime)."""
        if team_id in self.teams:
            self.teams[team_id] = TeamMomentum(team_id=team_id)


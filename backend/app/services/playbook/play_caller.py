#!/usr/bin/env python3
"""
Play Calling AI Module
=======================
Intelligent play selection based on game state.

Phase 9: Playbook & AI
- Situational awareness (down, distance, score)
- Tendency tracking
- Aggression settings
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import random

from .playbook import Play, Playbook, PlayType, Concept


# ============================================================================
# ENUMS
# ============================================================================

class AggressionLevel(str, Enum):
    """Offensive coordinator aggression."""
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    AGGRESSIVE = "AGGRESSIVE"


class GameScript(str, Enum):
    """Game flow state."""
    TRAILING = "TRAILING"
    CLOSE = "CLOSE"
    LEADING = "LEADING"
    BLOWOUT = "BLOWOUT"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class GameSituation:
    """Current game context."""
    quarter: int
    time_remaining: int  # seconds
    down: int
    distance: int
    field_position: int  # 0-100 (own goal to opponent goal)
    score_diff: int     # Positive = winning


@dataclass
class PlayCallResult:
    """Output from AI decision."""
    selected_play: Play
    confidence: float  # 0.0-1.0
    reasoning: str


# ============================================================================
# PLAY CALLER AI
# ============================================================================

class PlayCallerAI:
    """
    Offensive Coordinator AI.
    """

    def __init__(self, playbook: Playbook, aggression: AggressionLevel = AggressionLevel.BALANCED):
        self.playbook = playbook
        self.aggression = aggression
        self.tendency_history: List[PlayType] = []

    def call_play(self, situation: GameSituation) -> PlayCallResult:
        """
        Select the optimal play based on situation.
        """
        # 1. Determine game script
        script = self._determine_script(situation)

        # 2. Get candidate plays
        candidates = self.playbook.get_plays_by_situation(
            situation.down, situation.distance, situation.field_position
        )

        if not candidates:
            # Fallback: grab any play
            candidates = list(self.playbook.plays.values())[:5]

        # 3. Score each play
        scored_plays = []
        for play in candidates:
            score = self._score_play(play, situation, script)
            scored_plays.append((score, play))

        # Sort by score
        scored_plays.sort(key=lambda x: x[0], reverse=True)

        # 4. Select with some randomness (not always top choice)
        # Top 3 plays: 60%, 30%, 10% chance
        roll = random.random()
        if roll < 0.6 and len(scored_plays) > 0:
            selected = scored_plays[0][1]
        elif roll < 0.9 and len(scored_plays) > 1:
            selected = scored_plays[1][1]
        elif len(scored_plays) > 2:
            selected = scored_plays[2][1]
        else:
            selected = scored_plays[0][1]

        # Track tendency
        self.tendency_history.append(selected.play_type)
        if len(self.tendency_history) > 20:
            self.tendency_history.pop(0)

        return PlayCallResult(
            selected_play=selected,
            confidence=0.8,
            reasoning=f"Selected {selected.name} for {situation.down} and {situation.distance}"
        )

    def _determine_script(self, situation: GameSituation) -> GameScript:
        """Classify game flow."""
        if abs(situation.score_diff) <= 7:
            return GameScript.CLOSE
        elif situation.score_diff < -14:
            return GameScript.TRAILING
        elif situation.score_diff > 14:
            return GameScript.LEADING
        else:
            return GameScript.CLOSE

    def _score_play(self, play: Play, situation: GameSituation, script: GameScript) -> float:
        """
        Rate a play's suitability (0-100).
        """
        score = 50.0

        # Down & Distance
        if situation.down == 3:
            # 3rd down: Prioritize plays that gain yards needed
            if play.avg_yards >= situation.distance:
                score += 20

        # Game Script
        if script == GameScript.TRAILING:
            # Need points fast
            if play.play_type == PlayType.PASS:
                score += 15
        elif script == GameScript.LEADING:
            # Run clock
            if play.play_type == PlayType.RUN:
                score += 15

        # Aggression
        if self.aggression == AggressionLevel.AGGRESSIVE:
            score += play.risk_level * 2
        elif self.aggression == AggressionLevel.CONSERVATIVE:
            score -= play.risk_level * 2

        # Tendency balance: Avoid being too predictable
        recent_passes = sum(1 for t in self.tendency_history[-5:] if t == PlayType.PASS)
        if recent_passes >= 4 and play.play_type == PlayType.RUN:
            score += 10 # Mix it up

        return score

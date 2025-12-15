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


from app.data.coaches import CoachingPhilosophy
from app.services.playbook.coaching_ai import CoachingAIService

# ============================================================================
# ENUMS
# ============================================================================

from .types import AggressionLevel, GameScript, GameSituation, PlayCallResult

# ============================================================================
# PLAY CALLER AI
# ============================================================================

class PlayCallerAI:
    """
    Offensive Coordinator AI.
    """

    def __init__(self, playbook: Playbook, philosophy: Optional[CoachingPhilosophy] = None, aggression: AggressionLevel = AggressionLevel.BALANCED):
        self.playbook = playbook
        self.tendency_history: List[PlayType] = []

        if philosophy:
            self.philosophy = philosophy
        else:
            # Backward compatibility
            val = 50
            if aggression == AggressionLevel.AGGRESSIVE: val = 75
            elif aggression == AggressionLevel.CONSERVATIVE: val = 25
            self.philosophy = CoachingPhilosophy(aggressiveness=val)

        self.coaching_service = CoachingAIService(self.philosophy)

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

        # Aggression (Dynamic)
        aggression_val = self.coaching_service.get_adjusted_aggression(situation)
        # 0 to 100. 50 is neutral.
        # Risk level typically 1-10.
        # If agg=80 (+30), risk_mod = 6. Score += play.risk * 6.
        # If agg=20 (-30), risk_mod = -6. Score -= play.risk * 6.
        risk_modifier = (aggression_val - 50) / 5.0
        score += play.risk_level * risk_modifier

        # Philosophy: Run/Pass Ratio
        # 0 = All Pass, 100 = All Run
        skew = self.philosophy.run_pass_ratio
        if play.play_type == PlayType.RUN:
            if skew > 50:
                score += (skew - 50) * 0.5  # Boost up to +25
            else:
                score -= (50 - skew) * 0.5  # Penalize up to -25
        elif play.play_type == PlayType.PASS:
             if skew < 50:
                 score += (50 - skew) * 0.5 # Boost up to +25
             else:
                 score -= (skew - 50) * 0.5 # Penalize up to -25

        # Tendency balance: Avoid being too predictable
        recent_passes = sum(1 for t in self.tendency_history[-5:] if t == PlayType.PASS)
        if recent_passes >= 4 and play.play_type == PlayType.RUN:
            score += 10 # Mix it up

        return score

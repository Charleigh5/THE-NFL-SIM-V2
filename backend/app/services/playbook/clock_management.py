from enum import Enum
from app.services.playbook.types import GameSituation
from app.services.playbook.coaching_ai import CoachingAIService

class ClockStrategy(str, Enum):
    NORMAL = "NORMAL"
    CHEW_CLOCK = "CHEW_CLOCK"
    HURRY_UP = "HURRY_UP"
    SPIKE = "SPIKE"
    KNEEL = "KNEEL"

class ClockManagementAI:
    """
    Manages game clock strategy: Hurry-up, Chew Clock, Spikes, Kneels.
    """
    def __init__(self, coaching_service: CoachingAIService):
        self.coaching_service = coaching_service

    def get_clock_strategy(self, situation: GameSituation, timeouts_remaining: int) -> ClockStrategy:
        """Determines the current clock strategy."""

        # Victory Formation (Kneel)
        # Winning, Ball over control, Opponent has no timeouts (simplified)
        # For now, just check time/score roughly
        if situation.quarter == 4 and situation.score_diff > 0:
            if situation.time_remaining < 120:
                # If opponent can stop clock, we can't kneel freely yet, but let's assume safely for now
                # In real sim, we check opponent timeouts.
                return ClockStrategy.KNEEL

        # Hurry Up Logic
        if self.is_hurry_up_situation(situation):
            # Check for spike
            if self.should_spike_ball(situation, timeouts_remaining):
                return ClockStrategy.SPIKE
            return ClockStrategy.HURRY_UP

        # Chew Clock Logic (Leading in 4th)
        if situation.score_diff > 0 and situation.quarter == 4:
            return ClockStrategy.CHEW_CLOCK

        return ClockStrategy.NORMAL

    def is_hurry_up_situation(self, situation: GameSituation) -> bool:
        """Is the offense trying to hurry?"""
        if situation.quarter not in [2, 4]:
            return False
        if situation.time_remaining > 240: # 4 mins
            return False

        # Trailing in 4th
        if situation.quarter == 4 and situation.score_diff < 0:
            return True

        # Trying to score before half
        if situation.quarter == 2 and situation.score_diff <= 7:
            return True

        # Tie game late
        if situation.quarter == 4 and situation.score_diff == 0:
            return True

        return False

    def should_spike_ball(self, situation: GameSituation, timeouts_remaining: int) -> bool:
        """
        Decide to spike to stop clock.
        Assumes clock is running.
        """
        if not self.is_hurry_up_situation(situation):
            return False

        # If we have timeouts, usually better to use timeout to save the down
        # Unless we want to save timeouts for FG icing or specific strategy?
        if timeouts_remaining > 0:
            return False

        # No timeouts, time running critical < 30s?
        # Only spike on 1st down usually? Or maybe 2nd if desperate?
        # Standard: 1st down, < 30s, clock running.
        if situation.time_remaining < 45 and situation.down == 1:
            return True

        return False

    def should_use_timeout(self, situation: GameSituation, timeouts_remaining: int, is_offense: bool) -> bool:
        """Wrapper for timeout decision with resource check."""
        if timeouts_remaining <= 0:
            return False

        if is_offense:
            return self.coaching_service.should_call_timeout(situation, is_offense)
        else:
            return self.should_defense_call_timeout(situation, timeouts_remaining)

    def should_defense_call_timeout(self, situation: GameSituation, timeouts_remaining: int) -> bool:
        """Determines if defense should call a timeout to preserve time."""
        if timeouts_remaining <= 0:
            return False

        # Only call if losing or tied
        if situation.score_diff > 0: # Defense team is winning (score_diff is relative to team evaluating)
            return False

        # 4th Quarter specific
        if situation.quarter == 4:
            # Under 2:30 generally means we need to stop clock
            if situation.time_remaining < 160:
                # If tied or losing by one score (<= 8)
                if abs(situation.score_diff) <= 8:
                    return True
                # Or losing by two scores but enough time to recover?
                if abs(situation.score_diff) <= 16 and situation.time_remaining > 90:
                    return True

        return False

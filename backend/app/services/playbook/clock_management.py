from dataclasses import dataclass
from enum import Enum

from app.services.playbook.coaching_ai import CoachingAIService
from app.services.playbook.types import GameSituation


class ClockStrategy(str, Enum):
    NORMAL = "NORMAL"
    CHEW_CLOCK = "CHEW_CLOCK"
    HURRY_UP = "HURRY_UP"
    SPIKE = "SPIKE"
    KNEEL = "KNEEL"


class UrgencyLevel(str, Enum):
    """Granular urgency levels for 2-minute drill scenarios."""
    LOW = "LOW"          # >4 min, normal play
    MEDIUM = "MEDIUM"    # 2-4 min, need to move efficiently
    HIGH = "HIGH"        # 1-2 min, hurry-up offense
    CRITICAL = "CRITICAL"  # <1 min, desperation mode


@dataclass
class TwoMinuteDrillContext:
    """Context for 2-minute drill decision making."""
    urgency_level: UrgencyLevel
    clock_strategy: ClockStrategy
    timeouts_remaining: int
    score_deficit: int  # Positive = trailing, negative = leading
    time_remaining: int  # Seconds
    field_position: int  # Yards to goal
    down: int
    distance: int

    # Derived recommendations
    favor_sideline_routes: bool = False
    avoid_middle_field: bool = False
    max_pass_depth: str = "deep"  # "short", "mid", "deep"
    spike_recommended: bool = False
    timeout_recommended: bool = False

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

    # =========================================================================
    # 2-MINUTE DRILL AI (AI-005)
    # =========================================================================

    def get_urgency_level(self, situation: GameSituation, timeouts_remaining: int) -> UrgencyLevel:
        """
        Determine the urgency level based on time, score, and resources.

        This provides more granular control than binary hurry-up detection.
        """
        time_remaining = situation.time_remaining
        score_diff = situation.score_diff
        quarter = situation.quarter

        # Not a late-game situation
        if quarter not in [2, 4]:
            return UrgencyLevel.LOW

        # Leading comfortably
        if score_diff > 16:
            return UrgencyLevel.LOW

        # Calculate effective time (accounting for timeouts)
        # Each timeout is worth ~40 seconds of clock stoppage
        effective_time = time_remaining + (timeouts_remaining * 40)

        # Trailing or tied in 4th quarter
        if quarter == 4 and score_diff <= 0:
            if effective_time < 60:
                return UrgencyLevel.CRITICAL
            elif effective_time < 120:
                return UrgencyLevel.HIGH
            elif effective_time < 240:
                return UrgencyLevel.MEDIUM

        # End of half (2nd quarter)
        if quarter == 2:
            if time_remaining < 60:
                return UrgencyLevel.HIGH
            elif time_remaining < 120:
                return UrgencyLevel.MEDIUM

        return UrgencyLevel.LOW

    def get_two_minute_drill_context(
        self,
        situation: GameSituation,
        timeouts_remaining: int
    ) -> TwoMinuteDrillContext:
        """
        Build a comprehensive context for 2-minute drill decision making.

        Returns a TwoMinuteDrillContext with all relevant factors and recommendations.
        """
        urgency = self.get_urgency_level(situation, timeouts_remaining)
        strategy = self.get_clock_strategy(situation, timeouts_remaining)

        # Base context
        context = TwoMinuteDrillContext(
            urgency_level=urgency,
            clock_strategy=strategy,
            timeouts_remaining=timeouts_remaining,
            score_deficit=-situation.score_diff,  # Invert: positive = trailing
            time_remaining=situation.time_remaining,
            field_position=situation.field_position,
            down=situation.down,
            distance=situation.distance
        )

        # Calculate recommendations based on urgency
        if urgency == UrgencyLevel.CRITICAL:
            context.favor_sideline_routes = True
            context.avoid_middle_field = True
            context.max_pass_depth = "mid"  # No time for deep developing routes
            context.spike_recommended = (
                situation.down == 1 and
                timeouts_remaining == 0 and
                situation.time_remaining < 30
            )
        elif urgency == UrgencyLevel.HIGH:
            context.favor_sideline_routes = True
            context.avoid_middle_field = False
            context.max_pass_depth = "deep"
        elif urgency == UrgencyLevel.MEDIUM:
            context.favor_sideline_routes = False
            context.avoid_middle_field = False
            context.max_pass_depth = "deep"

        # Timeout recommendation
        if timeouts_remaining > 0 and urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
            # In FG range with ~20 seconds, save for potential ice or FG setup
            if situation.yards_to_goal <= 35 and situation.time_remaining < 25:
                context.timeout_recommended = False  # Save for FG
            elif situation.time_remaining < 40 and situation.down >= 2:
                context.timeout_recommended = True  # Use it or lose it

        return context

    def get_play_adjustments(self, situation: GameSituation, timeouts_remaining: int) -> dict:
        """
        Get play selection adjustments for 2-minute drill situations.

        Returns a dictionary of adjustments to apply to play selection.
        """
        context = self.get_two_minute_drill_context(situation, timeouts_remaining)

        adjustments = {
            "urgency_level": context.urgency_level.value,
            "filter_hurry_up_compatible": context.urgency_level in [
                UrgencyLevel.HIGH, UrgencyLevel.CRITICAL
            ],
            "pass_probability_boost": 0.0,
            "sideline_route_boost": 0.0,
            "deep_pass_penalty": 0.0,
            "run_penalty": 0.0,
            "max_play_clock_usage": 40,  # Default full play clock
        }

        if context.urgency_level == UrgencyLevel.CRITICAL:
            adjustments["pass_probability_boost"] = 0.35
            adjustments["sideline_route_boost"] = 0.25
            adjustments["deep_pass_penalty"] = 0.3
            adjustments["run_penalty"] = 0.4
            adjustments["max_play_clock_usage"] = 8  # Snap quickly
        elif context.urgency_level == UrgencyLevel.HIGH:
            adjustments["pass_probability_boost"] = 0.25
            adjustments["sideline_route_boost"] = 0.15
            adjustments["deep_pass_penalty"] = 0.1
            adjustments["run_penalty"] = 0.2
            adjustments["max_play_clock_usage"] = 15
        elif context.urgency_level == UrgencyLevel.MEDIUM:
            adjustments["pass_probability_boost"] = 0.1
            adjustments["max_play_clock_usage"] = 25

        return adjustments


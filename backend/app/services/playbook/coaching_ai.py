from app.data.coaches import CoachingPhilosophy
from app.services.playbook.types import GameSituation
import random

class CoachingAIService:
    """
    Service to interpret CoachingPhilosophy into specific game decisions.
    Acts as the 'brain' of the coach, making high-level strategic choices.
    """

    def __init__(self, philosophy: CoachingPhilosophy):
        self.philosophy = philosophy

    def get_adjusted_aggression(self, situation: GameSituation) -> int:
        """
        Calculate effective aggression based on game state and personality.
        Returns 0-100 score.
        """
        base_aggression = self.philosophy.aggressiveness

        # Adjust for score diff
        if situation.score_diff < -7:
            # Trailing -> more aggressive
            base_aggression += 10
        elif situation.score_diff > 7:
            # Leading -> more conservative
            base_aggression -= 10

        # Adjust for urgency (4th quarter)
        if situation.quarter == 4:
            if situation.score_diff < 0:
                base_aggression += 15 # Desperation
            elif situation.score_diff > 0:
                base_aggression -= 15 # Protect lead

        return max(0, min(100, base_aggression))

    def should_go_for_it_4th_down(self, situation: GameSituation) -> bool:
        """
        Decide whether to go for it on 4th down.
        """
        if situation.down != 4:
            return False

        # Distance factor
        distance_penalty = situation.distance * 10 # 10% penalty per yard

        # Field position factor (0=own end, 100=opp end)
        # Sweet spot is 40-yard line (60) to 20-yard line (80)
        position_bonus = 0
        if 40 <= situation.field_position <= 80:
            position_bonus = 20
        elif situation.field_position > 90:
             # Too close, maybe kick FG unless aggressive
             position_bonus = -10

        # Aggression factor (use the specific 4th down trait if available)
        # Fallback to general aggression if model hasn't been reloaded yet,
        # but since we updated code, it should be there.
        aggression_score = getattr(self.philosophy, 'fourth_down_aggression', self.philosophy.aggressiveness)

        # Situational overrides
        if situation.quarter == 4 and situation.score_diff < -8 and situation.time_remaining < 300:
            # Down by 2 scores, late -> almost always go
            return True

        probability = aggression_score - distance_penalty + position_bonus

        # Random roll
        roll = random.uniform(0, 100)
        return roll < probability

    def get_2pt_decision(self, situation: GameSituation) -> bool:
        """
        Decide whether to go for 2 points after a touchdown.
        """
        threshold = getattr(self.philosophy, 'two_pt_conversion_threshold', 50)

        # Standard chart logic approximation
        # Down by 2, 5, 16, 19 usually calls for 2
        # Up by 1, 4, 5, 12, 19 usually calls for 2
        # Implementation of "The Chart" is complex, we'll use a simplified version
        # influenced by the threshold.

        score_diff = situation.score_diff # This is AFTER the TD code triggers this logic presumably?
        # Usually this decision is made when score_diff is e.g. -2.

        # If the 'chart' suggests it, we check if personality allows it
        chart_says_go = False
        if score_diff in [-2, -5, -16, -19, 1, 4, 5, 12, 19]:
            chart_says_go = True

        if chart_says_go:
            # Conservative coaches might still kick
            if threshold > 70: # High threshold = conservative about 2pt (confusing naming?)
                # Wait, 'threshold' usually means 'minimum value to trigger'.
                # If we name it 'aggressiveness', high = go more.
                # If we name it 'threshold', it might mean probability?
                # Let's assume the field 'two_pt_conversion_threshold' acts as a
                # "tendency to follow the analytics chart".
                # For this MVP, let's treat it as "Probablity to go for it in marginal situations"
                pass
            return True # Simplified: Always follow chart for now

        # Random aggression override
        if self.philosophy.aggressiveness > 80:
             if random.random() < 0.1: # 10% chance to go for it just because
                 return True

        return False

    def should_call_timeout(self, situation: GameSituation, is_offense: bool) -> bool:
        """
        Decide whether to call a timeout.
        """
        # Only relevant in 2nd and 4th quarters usually
        if situation.quarter not in [2, 4]:
            return False

        # Only if time is running out
        if situation.time_remaining > 180: # 3 minutes
            return False

        aggression = getattr(self.philosophy, 'timeout_aggressiveness', 50)

        if is_offense:
            # Offense calls TO to save time when trailing or trying to score before half
            if situation.score_diff <= 0 or situation.quarter == 2:
                # If clock is running (implied)
                # This logic is simplified; sim engine handles clock stopping.
                # This returns "Do I WANT to stop the clock?"
                return True
        else:
            # Defense calls TO to get ball back
            if situation.score_diff < 0 and situation.score_diff > -9: # One score game
                 if situation.quarter == 4:
                     return True

        return False

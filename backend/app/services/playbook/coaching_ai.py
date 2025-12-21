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

        Uses real NFL analytics data from FOURTH_DOWN_ANALYTICS.
        """
        from app.core.nfl_reference_data import FOURTH_DOWN_ANALYTICS

        if situation.down != 4:
            return False

        analytics = FOURTH_DOWN_ANALYTICS

        # === SHORT YARDAGE: ALWAYS GO ===
        # Real data: 95.2% optimal on 4th & 1
        if situation.distance <= analytics.always_go_distance:
            # Almost always go for it on 4th & 1 (unless very conservative)
            if self.philosophy.aggressiveness >= 30:  # Even moderately aggressive
                return True

        # === FIELD POSITION BONUS ===
        # Go-for-it zone: Opponent's 40 to midfield (4th-60 zone)
        position_bonus = 0
        if analytics.go_for_it_zone_start <= situation.field_position <= analytics.go_for_it_zone_end:
            position_bonus = 30  # Strong bonus in optimal zone
        elif situation.field_position > 80:  # Deep in opponent territory
            position_bonus = 10  # Consider FG range
        elif situation.field_position > 95:
            position_bonus = -20  # Inside the 5 - chip shot FG territory

        # === DISTANCE PENALTY ===
        # Higher penalty for longer distance
        distance_penalty = situation.distance * 8

        # === COACH AGGRESSION ===
        aggression_score = getattr(
            self.philosophy,
            'fourth_down_aggression',
            self.philosophy.aggressiveness
        )

        # === SITUATIONAL OVERRIDES ===
        # Late game, trailing -> desperate times
        if analytics.late_game_trailing_2scores_override:
            if (situation.quarter == 4 and
                situation.score_diff < -8 and
                situation.time_remaining < 300):
                return True

        # === MEDIUM YARDAGE: CONSIDER ANALYTICS ===
        if situation.distance <= analytics.consider_go_distance:
            # Real data: kicking on 4th & 5 forfeits ~3% WP
            # We'll give a slight nudge to go for it on 4th & 2-5
            position_bonus += 15

        # Calculate final probability
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

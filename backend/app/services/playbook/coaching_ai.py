from app.data.coaches import CoachingPhilosophy
from app.services.playbook.types import GameSituation
from typing import Optional
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

        Uses real NFL analytics data and coach personality matrices.
        """
        from app.core.nfl_reference_data import FOURTH_DOWN_ANALYTICS

        if situation.down != 4:
            return False

        analytics = FOURTH_DOWN_ANALYTICS

        # Get coach's specific 4th down trait
        fourth_down_agg = getattr(
            self.philosophy, 'fourth_down_aggression', self.philosophy.aggressiveness
        )

        # === ARCHETYPE LOGIC ===
        # THE GAMBLER (aggression >= 75): Goes for it on 4th & Short anywhere past own 30
        # ANALYTICS DISCIPLE (60-74): Follows the chart strictly
        # BALANCED (40-59): Standard logic
        # CONSERVATIVE (< 40): Rarely goes for it unless desperate

        # --- Phase 1: Desperation Overrides (ALL archetypes) ---
        if situation.quarter == 4 and situation.score_diff < -8 and situation.time_remaining < 300:
            # Trailing by 2+ scores in final 5 mins -> GO FOR IT
            return True

        if situation.time_remaining < 60 and situation.score_diff < 0:
            # Final minute, losing -> GO FOR IT
            return True

        # --- Phase 2: Archetype-based Matrix ---

        # THE GAMBLER
        if fourth_down_agg >= 75:
            if situation.distance <= 2 and situation.field_position > 30:
                return True  # 4th & 1-2 past own 30
            if situation.distance <= 5 and situation.field_position > 50:
                return True  # 4th & 3-5 in opponent territory
            if situation.distance <= 10 and situation.field_position > 65:
                return True  # 4th & 6-10 in opponent red zone

        # ANALYTICS DISCIPLE
        elif fourth_down_agg >= 60:
            if situation.distance <= analytics.always_go_distance:
                return True  # Always go on 4th & 1
            if situation.distance <= analytics.consider_go_distance and \
               analytics.go_for_it_zone_start <= situation.field_position <= analytics.go_for_it_zone_end:
                return True  # Go for it in the "go zone" on 4th & 2-5

        # BALANCED
        elif fourth_down_agg >= 40:
            if situation.distance <= 1 and situation.field_position > 50:
                return True  # 4th & 1 in opponent territory only
            if situation.distance <= 2 and situation.field_position > 70:
                return True  # 4th & 2 in red zone

        # CONSERVATIVE (< 40)
        else:
            # Only go for it on goal line stands
            if situation.distance <= 1 and situation.field_position > 97:
                return True  # 4th & Goal from the 1

        return False

    def get_2pt_decision(self, situation: GameSituation) -> bool:
        """
        Decide whether to go for 2 points after a touchdown.
        Uses "The Chart" logic with personality overrides.
        """
        # "The Chart" optimal situations for 2-point attempts
        # Score differential AFTER the TD (so if you were down 8, you're now down 2)
        optimal_2pt_diffs = [-2, -5, -9, -16, -19, 1, 4, 5, 12, 19]

        score_diff = situation.score_diff
        aggression = self.philosophy.aggressiveness
        two_pt_threshold = getattr(self.philosophy, 'two_pt_conversion_threshold', 50)

        # --- ARCHETYPE OVERRIDES ---

        # THE GAMBLER (aggression >= 75): Goes for 2 more often
        if aggression >= 75:
            # Go for 2 on any close game situation
            if abs(score_diff) <= 8:
                return True
            # Always follow chart
            if score_diff in optimal_2pt_diffs:
                return True

        # ANALYTICS DISCIPLE (60-74): Strictly follows the chart
        elif aggression >= 60:
            if score_diff in optimal_2pt_diffs:
                return True

        # BALANCED (40-59): Follows chart with some hesitation
        elif aggression >= 40:
            if score_diff in [-2, -5, 1, 4]:  # Only most obvious situations
                return True

        # CONSERVATIVE / OLD SCHOOL (< 40): Almost never goes for 2
        else:
            # Only go for 2 if down by 2 late in game (must tie)
            if score_diff == -2 and situation.quarter == 4 and situation.time_remaining < 300:
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

    def should_attempt_trick_play(self, situation: GameSituation) -> Optional[str]:
        """
        Determine if a trick play should be called and which one.
        Returns PlayCall ID (e.g. "FAKE_PUNT_RUN") or None.
        """
        # 1. Base Eligibility
        # rare check first to save compute
        rand_check = random.random()
        base_prob = 0.02 # 2% base chance per valid down? Low...

        # Adjust by Aggressiveness (0-100) -> 0.0 to 0.10
        aggression_factor = (self.philosophy.aggressiveness / 100.0) * 0.10

        threshold = base_prob + aggression_factor

        # Situational Bonuses
        if situation.score_diff < -3 and situation.score_diff > -17:
            # Trailing by 1-2 scores -> desperate/momentum needed
            threshold += 0.05

        if situation.quarter == 4 and situation.score_diff < 0:
            threshold += 0.05

        # Field Position Constraints
        # Don't do it inside own 30 unless desperate
        if situation.field_position < 30 and situation.score_diff > -10:
             return None

        if rand_check > threshold:
             return None

        # 2. Select Play Type based on Down/Distance
        if situation.down == 4:
            # PUNT or FG Formation Logic
            # If in FG Range (roughly Opp 38+)
            if situation.field_position >= 62: # Opp 38
                # Fake FG?
                if random.random() < 0.5:
                    return "FAKE_FG_PASS" if random.random() < 0.6 else "FAKE_FG_RUN"
            else:
                # Fake Punt
                if situation.distance < 10: # Reasonable fake distance
                     return "FAKE_PUNT_RUN" if situation.distance < 4 else "FAKE_PUNT_PASS"

        elif situation.down in [1, 2]:
             # Offensive Trickery (Flea Flicker, etc)
             # Best used on 1st & 10 or 2nd & Short
             if situation.field_position > 40 and situation.field_position < 80:
                  if random.random() < 0.3:
                       return "FLEA_FLICKER"
                  elif random.random() < 0.3:
                       return "PHILLY_SPECIAL"

        return None

from dataclasses import dataclass
from typing import Any

from app.kernels.cortex.strategy import StrategyEngine


@dataclass
class GameSituation:
    down: int
    distance: int
    field_position: int  # 0-100 (0 is own goal line, 100 is opponent goal line)
    time_remaining: int  # Seconds
    score_differential: int  # Positive = Leading, Negative = Trailing
    quarter: int
    timeouts_left: int = 3


class CoordinatorMultiplier:
    """
    NFL Identity Blueprint: Coordinator IQ Multiplier System.

    The OC/DC is a multiplier, making the unit better than sum of parts.
    Formula: 1.0 + (IQ - 75) / 200

    Examples:
    - IQ 75 -> 1.0x (neutral)
    - IQ 95 -> 1.1x (10% boost)
    - IQ 55 -> 0.9x (10% penalty)
    """

    BASE_IQ = 75
    DIVISOR = 200.0

    @classmethod
    def calculate_boost(cls, intelligence: int) -> float:
        """
        Calculate coordinator boost multiplier.

        Args:
            intelligence: Coach intelligence rating (0-100)

        Returns:
            Multiplier (0.625 to 1.125 range for 0-100 IQ)
        """
        return 1.0 + (intelligence - cls.BASE_IQ) / cls.DIVISOR

    @classmethod
    def apply_to_probability(cls, base_prob: float, intelligence: int) -> float:
        """
        Apply coordinator boost to a success probability.

        Args:
            base_prob: Base success probability (0.0 to 1.0)
            intelligence: Coach intelligence rating

        Returns:
            Modified probability (clamped to 0.0-1.0)
        """
        boost = cls.calculate_boost(intelligence)
        modified = base_prob * boost
        return max(0.0, min(1.0, modified))


class CortexKernel:
    """
    Facade for the Cortex (AI/Strategy) Engine.
    Manages decision making and play calling based on game situation and coach philosophy.
    """

    def __init__(self, seed: Any = None):
        from app.core.random_utils import DeterministicRNG

        self.strategy = StrategyEngine()
        self.rng = DeterministicRNG(seed if seed is not None else 0)
        self.coordinator_multiplier = CoordinatorMultiplier()

    def call_play(
        self, situation: GameSituation, coach_philosophy: dict[str, Any] | None = None
    ) -> str:
        """
        Decide on a play type based on the current game situation.

        Returns:
            str: Play type (e.g., "RUN", "PASS_SHORT", "PASS_DEEP", "PUNT", "FG")
        """
        coach = coach_philosophy or {}
        aggressiveness = coach.get("aggressiveness", 50)  # 0-100
        pass_tendency = coach.get("pass_tendency", 50)  # 0-100
        coordinator_iq = coach.get("intelligence", 70)  # NFL Identity Blueprint

        # Calculate coordinator boost
        coord_boost = self.coordinator_multiplier.calculate_boost(coordinator_iq)

        # 1. Special Teams Logic (4th Down)
        if situation.down == 4:
            return self._decide_4th_down(situation, aggressiveness)

        # 2. End of Game Logic (Hail Mary / Victory Formation)
        if situation.quarter == 4 and situation.time_remaining < 120:
            if situation.score_differential < 0 and situation.score_differential >= -8:
                # Trailing by one score
                if situation.time_remaining < 10 and situation.field_position < 60:
                    return "HAIL_MARY"
            elif situation.score_differential > 0:
                # Leading, burn clock
                return "RUN"

        # 3. Down & Distance Logic
        if situation.distance > 10:
            # Long yardage -> Pass likely
            if situation.down == 3:
                return "PASS_DEEP" if aggressiveness > 60 else "PASS_SHORT"  # Screen/Draw
            return "PASS_DEEP"

        elif situation.distance <= 3:
            # Short yardage -> Run likely
            if situation.down == 3:
                return "RUN" if pass_tendency < 60 else "PASS_SHORT"
            return "RUN"

        # 4. Standard Logic (Mixed)
        # Adjust base pass chance by tendency
        pass_chance = pass_tendency / 100.0

        # Adjust by score (Trailing -> Pass more)
        if situation.score_differential < -7:
            pass_chance += 0.15
        elif situation.score_differential > 7:
            pass_chance -= 0.15

        # Adjust by field position (Red Zone -> Run more usually, but varies)
        if situation.field_position > 80:
            pass_chance -= 0.10

        # Apply coordinator IQ boost to optimal play selection accuracy
        # Higher IQ = better situational awareness, less random deviation
        if coord_boost > 1.0:
            # Smart coordinators make fewer suboptimal calls
            # Reduce randomness slightly
            pass

        if self.rng.random() < pass_chance:
            return "PASS_DEEP" if self.rng.random() < 0.3 else "PASS_SHORT"
        else:
            return "RUN"

    def get_coordinator_boost(self, intelligence: int) -> float:
        """Get the coordinator multiplier for external use."""
        return self.coordinator_multiplier.calculate_boost(intelligence)

    def _decide_4th_down(self, situation: GameSituation, aggressiveness: int) -> str:
        """Decide what to do on 4th down."""
        # Field Goal Range (approx 35 yard line of opponent -> field_position 65+)
        in_fg_range = situation.field_position >= 65

        # Desperation Mode (Trailing late)
        desperate = (
            situation.quarter == 4
            and situation.time_remaining < 300
            and situation.score_differential < 0
        )

        if desperate:
            return "PASS_DEEP"  # Go for it

        if situation.distance <= 1:
            # 4th & 1
            # Aggressive coaches go for it past own 40
            if situation.field_position > 40:
                if aggressiveness > 60:
                    return "RUN"

        if in_fg_range:
            return "FG"

        return "PUNT"

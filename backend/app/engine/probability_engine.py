import random
from typing import Optional
from enum import Enum
import math

class OutcomeType(Enum):
    CRITICAL_FAILURE = "critical_failure"
    FAILURE = "failure"
    SUCCESS = "success"
    CRITICAL_SUCCESS = "critical_success"

class ProbabilityEngine:
    """
    Engine for calculating success probabilities based on player attributes and context.
    Replaces legacy random logic with attribute-driven outcomes.
    """

    @staticmethod
    def compare_attributes(attacker_val: int, defender_val: int, scale: float = 0.01, max_mod: float = 0.3) -> float:
        """
        Generic attribute comparison.
        Returns a probability modifier (e.g., 0.10 for +10% chance).
        """
        diff = attacker_val - defender_val
        mod = diff * scale
        return max(-max_mod, min(max_mod, mod))

    @staticmethod
    def compare_speed(attacker_speed: int, defender_speed: int) -> float:
        """
        Compare speed attributes to determine a separation bonus.
        Returns a value between -0.10 and 0.20.
        """
        # Custom scaling for speed: 1 point = 1%
        # Asymmetric cap: Speed kills, so advantage is higher than disadvantage
        diff = attacker_speed - defender_speed
        return max(-0.10, min(0.20, diff / 100.0))

    @staticmethod
    def compare_strength(attacker_str: int, defender_str: int) -> float:
        """
        Compare strength attributes for blocking/tackling.
        Returns a value between -0.2 and 0.2.
        """
        return ProbabilityEngine.compare_attributes(attacker_str, defender_str, scale=0.01, max_mod=0.20)

    @staticmethod
    def compare_skill(attacker_skill: int, defender_skill: int) -> float:
        """
        Compare specific skills (e.g., Route Running vs Man Coverage).
        Returns a value between -0.25 and 0.25.
        """
        return ProbabilityEngine.compare_attributes(attacker_skill, defender_skill, scale=0.01, max_mod=0.25)

    @staticmethod
    def calculate_success_chance(
        base_probability: float,
        attribute_modifiers: float,
        context_modifiers: float = 0.0,
        fatigue_penalty: float = 0.0,
        min_chance: float = 0.05,
        max_chance: float = 0.95
    ) -> float:
        """
        Calculate final success probability.
        """
        total_chance = base_probability + attribute_modifiers + context_modifiers - fatigue_penalty
        return max(min_chance, min(max_chance, total_chance))

    @staticmethod
    def resolve_outcome(probability: float) -> bool:
        """
        Resolve a boolean outcome based on probability.
        """
        return random.random() < probability

    @staticmethod
    def resolve_tiered_outcome(probability: float, critical_threshold: float = 0.10) -> OutcomeType:
        """
        Resolve an outcome into 4 tiers:
        - Critical Failure: Roll > Probability + (1 - Probability) * (1 - Critical Threshold)? No.
        Let's define ranges:
        0.0 to Prob: Success
            0.0 to (Prob * CritThreshold): Critical Success
        Prob to 1.0: Failure
            (1.0 - (1-Prob)*CritThreshold) to 1.0: Critical Failure
        """
        roll = random.random()

        if roll < probability:
            # Success branch
            # If probability is 0.6, crit threshold 0.1 -> top 10% of success range?
            # Or absolute top 5% of all rolls?
            # Let's use absolute top/bottom of the range relative to the success/fail blocks.

            # Critical Success: if roll is in the top 10% of the success range?
            # Actually, usually low roll = success in some systems, high in others.
            # Here resolve_outcome(p) returns true if roll < p. So 0.0 is best.

            # Let's say Critical Success is the bottom 10% of the success range.
            if roll < (probability * critical_threshold):
                return OutcomeType.CRITICAL_SUCCESS
            return OutcomeType.SUCCESS
        else:
            # Failure branch
            # Critical Failure is the top 10% of the failure range.
            failure_range_start = probability
            failure_range_width = 1.0 - probability
            if roll > (1.0 - (failure_range_width * critical_threshold)):
                return OutcomeType.CRITICAL_FAILURE
            return OutcomeType.FAILURE

    @staticmethod
    def calculate_variable_outcome(
        base_value: float,
        variance: float,
        modifiers: float = 0.0
    ) -> float:
        """
        Calculate a scalar outcome (e.g., yards gained) with uniform variance.
        """
        random_factor = random.uniform(-variance, variance)
        return base_value + random_factor + modifiers

    @staticmethod
    def calculate_normal_outcome(
        mean: float,
        std_dev: float,
        min_val: float = 0.0,
        max_val: float = 100.0
    ) -> float:
        """
        Calculate a scalar outcome using a normal distribution (bell curve).
        More realistic for yards gained, etc.
        """
        val = random.gauss(mean, std_dev)
        return max(min_val, min(max_val, val))

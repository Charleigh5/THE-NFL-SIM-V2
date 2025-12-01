import random
from typing import Optional

class ProbabilityEngine:
    """
    Engine for calculating success probabilities based on player attributes and context.
    Replaces legacy random logic with attribute-driven outcomes.
    """

    @staticmethod
    def compare_speed(attacker_speed: int, defender_speed: int) -> float:
        """
        Compare speed attributes to determine a separation bonus.
        Returns a value between -0.2 and 0.5.
        Positive means attacker is faster.
        """
        diff = attacker_speed - defender_speed
        # Each point of speed difference is worth 1% separation
        # Cap at 20% advantage or 10% disadvantage
        return max(-0.10, min(0.20, diff / 100.0))

    @staticmethod
    def compare_strength(attacker_str: int, defender_str: int) -> float:
        """
        Compare strength attributes for blocking/tackling.
        Returns a value between -0.2 and 0.2.
        """
        diff = attacker_str - defender_str
        return max(-0.20, min(0.20, diff / 100.0))

    @staticmethod
    def compare_skill(attacker_skill: int, defender_skill: int) -> float:
        """
        Compare specific skills (e.g., Route Running vs Man Coverage).
        Returns a value between -0.25 and 0.25.
        """
        diff = attacker_skill - defender_skill
        return max(-0.25, min(0.25, diff / 100.0))

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

        Args:
            base_probability: The baseline chance of success (0.0 to 1.0)
            attribute_modifiers: Sum of attribute comparison bonuses/penalties
            context_modifiers: Sum of situational modifiers (weather, home field, etc.)
            fatigue_penalty: Penalty due to fatigue (should be positive value, subtracted)
            min_chance: Floor for probability
            max_chance: Ceiling for probability

        Returns:
            Float between min_chance and max_chance
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
    def calculate_variable_outcome(
        base_value: float,
        variance: float,
        modifiers: float = 0.0
    ) -> float:
        """
        Calculate a scalar outcome (e.g., yards gained) with variance.
        """
        # Random factor between -variance and +variance
        random_factor = random.uniform(-variance, variance)
        return base_value + random_factor + modifiers

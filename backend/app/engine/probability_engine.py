
from enum import Enum

from app.core.gameplay_constants import GAMEPLAY


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
        Returns a value between SPEED_MIN_MOD and SPEED_MAX_MOD.
        """
        # Custom scaling for speed: 1 point = 1%
        # Asymmetric cap: Speed kills, so advantage is higher than disadvantage
        diff = attacker_speed - defender_speed
        return max(
            GAMEPLAY.attributes.SPEED_MIN_MOD,
            min(GAMEPLAY.attributes.SPEED_MAX_MOD, diff * GAMEPLAY.attributes.SPEED_SCALE)
        )

    @staticmethod
    def compare_strength(attacker_str: int, defender_str: int) -> float:
        """
        Compare strength attributes for blocking/tackling.
        Returns a value between -STRENGTH_MAX_MOD and +STRENGTH_MAX_MOD.
        """
        return ProbabilityEngine.compare_attributes(
            attacker_str, defender_str,
            scale=GAMEPLAY.attributes.STRENGTH_SCALE,
            max_mod=GAMEPLAY.attributes.STRENGTH_MAX_MOD
        )

    @staticmethod
    def compare_skill(attacker_skill: int, defender_skill: int) -> float:
        """
        Compare specific skills (e.g., Route Running vs Man Coverage).
        Returns a value between -SKILL_MAX_MOD and +SKILL_MAX_MOD.
        """
        return ProbabilityEngine.compare_attributes(
            attacker_skill, defender_skill,
            scale=GAMEPLAY.attributes.SKILL_SCALE,
            max_mod=GAMEPLAY.attributes.SKILL_MAX_MOD
        )

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
    def calculate_success_chance_with_traits(
        base_probability: float,
        base_attribute_modifiers: float,
        player_traits: list,  # List of TraitDefinition objects
        context: dict,  # Game context for conditional trait activation
        fatigue_penalty: float = 0.0,
        min_chance: float = 0.05,
        max_chance: float = 0.95
    ) -> tuple[float, list]:
        """
        Calculate success probability with trait modifiers applied.

        Follows industry best practices:
        - Modular: Traits are treated as separate modifier components
        - Data-driven: Effects defined in trait catalog, not hardcoded
        - Additive first: Base + trait modifiers, then context

        Args:
            base_probability: Starting probability (0.0-1.0)
            base_attribute_modifiers: Sum of attribute comparison modifiers
            player_traits: List of TraitDefinition objects for the player
            context: Dict with keys like 'triggers', 'quarter', 'down', etc.
            fatigue_penalty: Reduction from fatigue (0.0-1.0)
            min_chance: Floor value for probability
            max_chance: Ceiling value for probability

        Returns:
            Tuple of (final_probability, list of active trait names)
        """
        # Import here to avoid circular dependency
        from app.services.trait_service import TraitService

        trait_bonus = 0.0
        active_traits = []
        context_bonus = 0.0

        # Apply trait modifiers
        for trait_def in player_traits:
            if TraitService.check_trait_activation(trait_def, context):
                active_traits.append(trait_def.name)

                # Extract relevant effects and convert to probability modifiers
                effects = trait_def.effects

                # Generic boost effects (scaled to probability)
                for key, value in effects.items():
                    if "_boost" in key:
                        # Stat boosts: +10 rating = +5% probability
                        trait_bonus += value * GAMEPLAY.passing.STAT_BOOST_TO_PROB_SCALE
                    elif "_chance" in key or "_rate" in key:
                        # Direct probability modifiers
                        trait_bonus += value
                    elif "_reduction" in key:
                        # Penalty reductions (add as positive)
                        trait_bonus += value
                    elif key == "pressure_immunity" and value:
                        # Boolean flags: nullify specific penalties
                        context_bonus += 0.10  # +10% for pressure immunity
                    elif key == "fatigue_override" and value:
                        fatigue_penalty = 0.0  # Override fatigue

        # Apply additively: base + attributes + traits + context - fatigue
        total_chance = (
            base_probability
            + base_attribute_modifiers
            + trait_bonus
            + context_bonus
            - fatigue_penalty
        )

        final_probability = max(min_chance, min(max_chance, total_chance))
        return final_probability, active_traits

    @staticmethod
    def resolve_outcome(rng, probability: float) -> bool:
        """
        Resolve a boolean outcome based on probability.
        """
        return rng.random() < probability

    @staticmethod
    def resolve_tiered_outcome(rng, probability: float, critical_threshold: float = 0.10) -> OutcomeType:
        """
        Resolve an outcome into 4 tiers:
        - Critical Failure: Roll > Probability + (1 - Probability) * (1 - Critical Threshold)? No.
        Let's define ranges:
        0.0 to Prob: Success
            0.0 to (Prob * CritThreshold): Critical Success
        Prob to 1.0: Failure
            (1.0 - (1-Prob)*CritThreshold) to 1.0: Critical Failure
        """
        roll = rng.random()

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
        rng,
        base_value: float,
        variance: float,
        modifiers: float = 0.0
    ) -> float:
        """
        Calculate a scalar outcome (e.g., yards gained) with uniform variance.
        """
        random_factor = rng.uniform(-variance, variance)
        return base_value + random_factor + modifiers

    @staticmethod
    def calculate_normal_outcome(
        rng,
        mean: float,
        std_dev: float,
        min_val: float = 0.0,
        max_val: float = 100.0
    ) -> float:
        """
        Calculate a scalar outcome using a normal distribution (bell curve).
        More realistic for yards gained, etc.
        """
        val = rng.gauss(mean, std_dev)
        return max(min_val, min(max_val, val))

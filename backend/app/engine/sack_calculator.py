from __future__ import annotations

import random
from typing import Optional

from app.core.logging_config import get_logger, ErrorCategory, log_error
from app.models.player import Player

logger = get_logger(__name__)

class SackCalculator:
    """
    Calculator for pocket pressure and sack outcomes.

    Factors in:
    - DL pass rush vs OL pass block
    - OL Chemistry (cohesion)
    - QB Pocket Presence (new attribute)
    - QB Mobility (scramble willingness, speed)
    """

    BASE_SACK_PROBABILITY = 0.07 # 7% base sack rate on pass plays

    @staticmethod
    def calculate_sack_probability(
        qb: Player,
        pressure_level: float, # 0.0 to 1.0 representing pass rush win rate
        ol_chemistry_bonus: int # 0 to 5
    ) -> float:
        """
        Calculate the refined probability of a sack occurring given the pressure.

        Formula:
        P(Sack) = Base * PressureFactor * (1 - PocketPresenceEffect) * (1 - ChemistryEffect)
        """
        try:
            # 1. Pocket Presence Effect (0.0 to 0.495 reduction)
            # Higher presence = lower sack chance
            pocket_presence = getattr(qb, 'pocket_presence', None) or 50
            presence_factor = pocket_presence * 0.005

            # 2. Chemistry Effect (0.0 to 0.1 reduction)
            # Each point of chemistry reduces sack chance by 2%
            chemistry_factor = ol_chemistry_bonus * 0.02

            # 3. Mobility Factor (Escape)
            # If pressure implies a sack, QB can scramble
            # Combine speed/agility/acceleration with safe defaults
            qb_speed = getattr(qb, 'speed', None) or 50
            qb_accel = getattr(qb, 'acceleration', None) or 50
            qb_agility = getattr(qb, 'agility', None) or 50
            mobility_score = (qb_speed + qb_accel + qb_agility) / 300.0 # 0.0-1.0
            escape_factor = mobility_score * 0.3 # Up to 30% reduction for elite mobility

            # Combine reduction factors (multiplicative for diminishing returns)
            # Total Reduction = 1 - ((1-p)(1-c)(1-e))
            # Just multiply the probability by (1 - factor)

            # Base probability scaled by pressure (pressure 0.5 = normal, 1.0 = instant jailbreak)
            # Let's say pressure_level scales the base prob.
            # If pressure_level is defined as "Probability DL wins rep", then:
            # P(Pressure) = pressure_level
            # P(Sack | Pressure) vs P(ThrowAway | Pressure) etc.

            # Simplified for Engine:
            # initial_prob is proportional to pressure_level
            initial_prob = SackCalculator.BASE_SACK_PROBABILITY * (1 + pressure_level)

            final_prob = initial_prob * (1 - presence_factor) * (1 - chemistry_factor) * (1 - escape_factor)

            # Clamp
            final_prob = max(0.0, min(0.95, final_prob))

            logger.debug(
                "sack_calc",
                qb=f"{qb.first_name} {qb.last_name}",
                pressure=pressure_level,
                presence_val=pocket_presence,
                presence_mod=presence_factor,
                chem_mod=chemistry_factor,
                escape_mod=escape_factor,
                result=final_prob
            )

            return final_prob

        except Exception as e:
            log_error(logger, ErrorCategory.SACK_CALC_ERROR, "Failed to calculate sack probability", exc_info=e)
            return SackCalculator.BASE_SACK_PROBABILITY # Fallback

    @staticmethod
    def resolve_sack_outcome(qb: Player, sack_prob: float) -> str:
        """
        Determine if a play results in a Sack, Throw Away, or Scramble based on probability.
        """
        roll = random.random()

        if roll < sack_prob:
            return "SACK"

        # If not sacked, check for Throw Away vs Forced Scramble
        # Driven by "Throw Away" trait or "Scramble Willingness"
        # For now, return "PRESSURE_AVOIDED"
        return "PRESSURE_AVOIDED"

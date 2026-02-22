from __future__ import annotations

import random

from app.core.logging_config import ErrorCategory, get_logger, log_error
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

    NFL Calibration (2020-2024):
    - League average sack rate: ~6.5% per pass play
    - Elite QB sack rate: ~4.5-5.0%
    - Poor QB sack rate: ~8.5-9.0%
    - Pressure-to-sack conversion: ~22%
    """

    BASE_SACK_PROBABILITY = 0.065  # 6.5% NFL average sack rate

    @staticmethod
    def calculate_sack_probability(
        qb: Player,
        pressure_level: float,  # 0.0 to 1.0 representing pass rush win rate
        ol_chemistry_bonus: int,  # 0 to 5
    ) -> float:
        """
        Calculate the refined probability of a sack occurring given the pressure.

        Formula:
        P(Sack) = Base * PressureFactor * (1 - PocketPresenceEffect) * (1 - ChemistryEffect)

        NFL Calibration:
        - 90+ pocket presence → ~4.5% sack rate (elite)
        - 50 pocket presence → ~6.5% sack rate (average)
        - <40 pocket presence → ~9% sack rate (poor)
        """
        try:
            # 1. Pocket Presence Effect (0.0 to 0.45 reduction)
            # Higher presence = lower sack chance
            # NFL: Elite QBs (90+ rating) have ~30-40% fewer sacks
            pocket_presence = getattr(qb, "pocket_presence", None) or 50
            presence_factor = pocket_presence * 0.005  # 90 rating = 45% reduction

            # 2. Chemistry Effect (0.0 to 0.1 reduction)
            # Each point of chemistry reduces sack chance by 2%
            chemistry_factor = ol_chemistry_bonus * 0.02

            # 3. Mobility Factor (Escape)
            # Combine speed/agility/acceleration with safe defaults
            # NFL: Mobile QBs like Jackson, Allen have lower sack rates
            qb_speed = getattr(qb, "speed", None) or 50
            qb_accel = getattr(qb, "acceleration", None) or 50
            qb_agility = getattr(qb, "agility", None) or 50
            mobility_score = (qb_speed + qb_accel + qb_agility) / 300.0  # 0.0-1.0
            escape_factor = mobility_score * 0.25  # Up to 25% reduction for elite mobility

            # Base probability scaled by pressure
            # pressure_level 0.5 = normal, 1.0 = instant pressure
            initial_prob = SackCalculator.BASE_SACK_PROBABILITY * (1 + pressure_level)

            final_prob = (
                initial_prob * (1 - presence_factor) * (1 - chemistry_factor) * (1 - escape_factor)
            )

            # Clamp to reasonable bounds
            final_prob = max(0.02, min(0.25, final_prob))

            logger.debug(
                "sack_calc",
                qb=f"{qb.first_name} {qb.last_name}",
                pressure=pressure_level,
                presence_val=pocket_presence,
                presence_mod=presence_factor,
                chem_mod=chemistry_factor,
                escape_mod=escape_factor,
                result=final_prob,
            )

            return final_prob

        except Exception as e:
            log_error(
                logger,
                ErrorCategory.SACK_CALC_ERROR,
                "Failed to calculate sack probability",
                exc_info=e,
            )
            return SackCalculator.BASE_SACK_PROBABILITY  # Fallback

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

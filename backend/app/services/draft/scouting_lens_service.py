"""
Scouting Lens & Draft AI Service
=================================
Models front office evaluation lenses (Consensus, Film, Analytics, Regional Scout)
and dynamic in-draft trade-up urgency algorithms.
"""

import math
import random
from typing import Dict, List, Optional
from app.schemas.deep_dive import (
    ScoutBiasLens,
    ProspectIntelligence,
    DraftTradeUrgency,
)


class ScoutingLensService:
    """Service evaluating prospects through distinct front-office scouting lenses."""

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)

    def evaluate_prospect(
        self,
        prospect_id: int,
        name: str,
        position: str,
        college: str,
        true_ovr: int,
        s2_score: int,
        gps_speed_max: float,
        burst_score: float,
        scheme_fit_pct: int = 80,
    ) -> ProspectIntelligence:
        """
        Synthesize multi-lens perceived ratings for a draft prospect.
        """
        # 1. Consensus Media Grade: Regressed toward median with slight variance
        consensus_noise = int(round(random.gauss(0, 2.0)))
        consensus_ovr = max(55, min(99, true_ovr + consensus_noise))

        # 2. Film Traditionalist: Heavily weights S2 cognition and college pedigree
        film_mod = (s2_score - 75) * 0.12 + (scheme_fit_pct - 75) * 0.08
        film_ovr = max(55, min(99, int(round(true_ovr + film_mod + random.gauss(0, 1.5)))))

        # 3. Analytics Department: Heavily weights GPS speed and burst score
        speed_delta = (gps_speed_max - 20.0) * 2.5
        burst_delta = (burst_score - 75.0) * 0.15
        analytics_mod = speed_delta + burst_delta
        analytics_ovr = max(55, min(99, int(round(true_ovr + analytics_mod + random.gauss(0, 1.0)))))

        # 4. Regional Scout: High variance, visceral subjective conviction
        regional_bias = random.gauss(0, 4.0)
        regional_ovr = max(55, min(99, int(round(true_ovr + regional_bias))))

        # Boom/Bust factor calculation
        variance_index = (
            abs(film_ovr - analytics_ovr) + abs(regional_ovr - consensus_ovr)
        ) / 20.0
        boom_bust_factor = max(0.05, min(0.95, round(variance_index, 2)))

        # Medical grade based on random risk model
        if boom_bust_factor > 0.75:
            medical_grade = "FAIL" if random.random() < 0.25 else "CONCERN"
        elif boom_bust_factor > 0.45 and random.random() < 0.20:
            medical_grade = "CONCERN"
        else:
            medical_grade = "PASS"

        # Projected Draft Round based on consensus OVR
        if consensus_ovr >= 85:
            projected_round = 1
        elif consensus_ovr >= 80:
            projected_round = 2
        elif consensus_ovr >= 76:
            projected_round = 3
        elif consensus_ovr >= 72:
            projected_round = 4
        elif consensus_ovr >= 68:
            projected_round = 5
        elif consensus_ovr >= 64:
            projected_round = 6
        else:
            projected_round = 7

        perceived_ovr = {
            ScoutBiasLens.CONSENSUS.value: consensus_ovr,
            ScoutBiasLens.FILM_TRADITIONALIST.value: film_ovr,
            ScoutBiasLens.ANALYTICS_METRICS.value: analytics_ovr,
            ScoutBiasLens.REGIONAL_SCOUT.value: regional_ovr,
        }

        return ProspectIntelligence(
            id=prospect_id,
            name=name,
            position=position,
            college=college,
            true_ovr=true_ovr,
            consensus_ovr=consensus_ovr,
            perceived_ovr=perceived_ovr,
            s2_cognition_score=s2_score,
            gps_speed_max=round(gps_speed_max, 1),
            burst_score=round(burst_score, 1),
            boom_bust_factor=boom_bust_factor,
            scheme_fit_percentage=scheme_fit_pct,
            medical_grade=medical_grade,
            draft_projection_round=projected_round,
        )

    def calculate_trade_urgency(
        self,
        team_id: str,
        target_position: str,
        roster_need_score: float, # 0.0 to 1.0
        remaining_in_tier: int,
        current_pick: int,
    ) -> DraftTradeUrgency:
        """
        Calculates how aggressively an AI GM will attempt to trade up to capture a falling tier prospect.
        Formula: Urgency = (Need^1.5) * (1 / max(1, remaining_in_tier)) * PositionalMultiplier
        """
        premium_positions = {"QB": 1.5, "OT": 1.3, "DE": 1.3, "CB": 1.2, "WR": 1.15}
        pos_mult = premium_positions.get(target_position, 1.0)

        # Scarcity factor
        scarcity = 1.0 / max(1, remaining_in_tier)
        base_urgency = (roster_need_score ** 1.5) * scarcity * pos_mult
        urgency_index = max(0.0, min(1.0, round(base_urgency, 3)))

        # Willingness to overpay above Jimmy Johnson chart value
        overpay_pct = round(urgency_index * 0.35, 3)

        # Base pick value on Jimmy Johnson draft chart approximation
        base_pick_value = int(round(3000 * math.exp(-0.065 * current_pick)))
        suggested_value = int(round(base_pick_value * (1.0 + overpay_pct)))

        return DraftTradeUrgency(
            team_id=team_id,
            target_position=target_position,
            urgency_index=urgency_index,
            willing_to_overpay_pct=overpay_pct,
            suggested_package_value=suggested_value,
        )


scouting_lens_service = ScoutingLensService()

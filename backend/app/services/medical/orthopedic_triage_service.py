"""
Orthopedic Trauma Triage & Hazard Service
==========================================
Models 7-zone anatomical micro-wear, Cox proportional hazard curves,
and interactive orthopedic triage protocols (PRP, Surgery, Rest, Cortisone).
"""

import math
import random
from typing import Dict, List, Optional
from app.schemas.deep_dive import (
    MedicalProtocolType,
    OrthopedicProtocolOption,
    TriageDecisionResult,
)


class OrthopedicTriageService:
    """Service evaluating orthopedic treatments and calculating re-injury risk curves."""

    def __init__(self, seed: Optional[int] = 42):
        if seed is not None:
            random.seed(seed)

    def get_protocol_options(
        self,
        zone_key: str,
        current_integrity: float,
        baseline_weeks: int,
        player_age: int = 26,
        is_x_factor: bool = False,
    ) -> List[OrthopedicProtocolOption]:
        """
        Generate available clinical treatment pathways for an injured anatomical zone.
        """
        # Age and X-Factor recovery multipliers
        age_factor = max(0.8, 1.0 + (player_age - 25) * 0.03)
        dev_reduction = 0.85 if is_x_factor else 1.0

        # 1. Conservative Rest
        rest_weeks = max(1, int(round(baseline_weeks * age_factor)))
        rest_option = OrthopedicProtocolOption(
            protocol=MedicalProtocolType.REST,
            name="Conservative Rest & Physical Therapy",
            estimated_recovery_weeks=rest_weeks,
            complication_risk_pct=0.0,
            target_integrity_restore=100.0,
            re_injury_hazard_multiplier=1.0,
            game_availability_status="OUT",
            description="Non-invasive physiological rest. Eliminates complication risks; safe return timetable.",
            clinical_note="Standard protocol for low-grade strains and baseline recovery.",
        )

        # 2. Platelet-Rich Plasma (PRP) Therapy
        prp_weeks = max(1, int(round(baseline_weeks * 0.70 * age_factor * dev_reduction)))
        prp_option = OrthopedicProtocolOption(
            protocol=MedicalProtocolType.PRP_THERAPY,
            name="Platelet-Rich Plasma (PRP) Biotherapy",
            estimated_recovery_weeks=prp_weeks,
            complication_risk_pct=0.05,
            target_integrity_restore=95.0,
            re_injury_hazard_multiplier=1.1,
            game_availability_status="OUT",
            description="Concentrated autologous platelet injections accelerating cellular regeneration by ~30%.",
            clinical_note="Highly effective for tendonitis and acute muscular micro-tears.",
        )

        # 3. Arthroscopic Minimally Invasive Surgery
        arthro_weeks = max(1, int(round(baseline_weeks * 0.50 * age_factor)))
        arthro_option = OrthopedicProtocolOption(
            protocol=MedicalProtocolType.ARTHROSCOPIC_SURGERY,
            name="Accelerated Arthroscopic Repair",
            estimated_recovery_weeks=arthro_weeks,
            complication_risk_pct=0.12,
            target_integrity_restore=90.0,
            re_injury_hazard_multiplier=1.25,
            game_availability_status="OUT",
            description="Surgical scope debridement repairing structural tissue, cutting timetable in half.",
            clinical_note="Recommended for meniscus trims, labral cleanouts, and loose body removal.",
        )

        # 4. Full Reconstructive Surgery (for severe structural tears)
        recon_weeks = max(4, int(round(baseline_weeks * 1.20 * age_factor)))
        recon_option = OrthopedicProtocolOption(
            protocol=MedicalProtocolType.RECONSTRUCTIVE_SURGERY,
            name="Comprehensive Structural Reconstruction",
            estimated_recovery_weeks=recon_weeks,
            complication_risk_pct=0.08,
            target_integrity_restore=98.0,
            re_injury_hazard_multiplier=0.9,
            game_availability_status="OUT",
            description="Full graft ligament reconstruction. Longer timetable but restores long-term joint durability.",
            clinical_note="Definitive solution for ACL, Achilles, or major tendon tears.",
        )

        # 5. Cortisone Field Stabilization (Play Through)
        cortisone_option = OrthopedicProtocolOption(
            protocol=MedicalProtocolType.CORTISONE_STABILIZATION,
            name="Cortisone Joint Injection (Suit Up & Play)",
            estimated_recovery_weeks=0,
            complication_risk_pct=0.35,
            target_integrity_restore=max(30.0, current_integrity),
            re_injury_hazard_multiplier=2.5,
            game_availability_status="QUESTIONABLE",
            description="High-dose anti-inflammatory injection with joint bracing allowing the player to suit up immediately.",
            clinical_note="WARNING: Severe hazard of catastrophic re-injury during collision.",
        )

        return [rest_option, prp_option, arthro_option, recon_option, cortisone_option]

    def apply_triage_protocol(
        self,
        player_id: int,
        zone_key: str,
        protocol: MedicalProtocolType,
        baseline_weeks: int,
        player_age: int = 26,
        toughness: int = 80,
    ) -> TriageDecisionResult:
        """
        Execute the chosen triage protocol and calculate probabilistic recovery outcome.
        """
        options = self.get_protocol_options(zone_key, 60.0, baseline_weeks, player_age)
        selected = next((o for o in options if o.protocol == protocol), options[0])

        # Roll for complication based on risk percentage, mitigated by player toughness
        toughness_mitigation = (toughness - 70) * 0.002
        effective_risk = max(0.01, selected.complication_risk_pct - toughness_mitigation)
        complication_occurred = random.random() < effective_risk

        if complication_occurred:
            recovery_weeks = selected.estimated_recovery_weeks + random.randint(2, 4)
            final_integrity = selected.target_integrity_restore - 10.0
            re_injury_risk = selected.re_injury_hazard_multiplier * 1.4
            message = f"Complication occurred during {selected.name}! Timetable extended by +{recovery_weeks - selected.estimated_recovery_weeks} weeks."
        else:
            recovery_weeks = selected.estimated_recovery_weeks
            final_integrity = selected.target_integrity_restore
            re_injury_risk = selected.re_injury_hazard_multiplier
            message = f"Protocol successfully initiated: {selected.name}. Target return in {recovery_weeks} weeks."

        return TriageDecisionResult(
            player_id=player_id,
            zone_key=zone_key,
            protocol_applied=protocol,
            projected_recovery_weeks=recovery_weeks,
            complication_occurred=complication_occurred,
            final_integrity_forecast=round(final_integrity, 1),
            re_injury_risk_index=round(re_injury_risk, 2),
            message=message,
        )


orthopedic_triage_service = OrthopedicTriageService()

"""
Orthopedic Simulation Engine
============================
High-precision orthopedic recovery trajectory generator and re-injury hazard modeling.

Core Responsibilities:
1. Multi-Protocol RTP Trajectory Visualizer:
   - 12-week non-linear Gompertz/Sigmoidal tissue repair curves:
     H(t) = H0 + (100 - H0) * exp(-exp(-k * (t - t0)))
   - Evaluates 5 comparative clinical protocols: Conservative, PRP, Arthroscopic, Open Surgery, Cortisone.
   - Latency budget: <2.5ms.
2. Elite Specialist 2nd Opinion Referral System:
   - External center referrals (Andrews Sports Medicine, Kerlan-Jobe, HSS).
   - 15% probability of detecting occult misdiagnoses.
   - 50% surgical complication risk reduction factor.
3. 60Hz Live In-Game Cortisone Hazard Multiplier:
   - Evaluates tissue strain during sharp athletic cuts (delta_v > 4.5 m/s^2) and collisions (p > 850 kg*m/s).
   - In-game evaluation latency: <0.001ms.
"""

import math
import random
import time
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session

from app.schemas.orthopedic_rtp import (
    RTPCurvePoint,
    TreatmentTrajectory,
    SecondOpinionCenter,
    SecondOpinionConsultResult,
    CortisoneHazardCheckResponse,
    OrthopedicEvaluationResponse,
)


class OrthopedicEngine:
    """Engine computing Gompertz RTP trajectories and clinical orthopedic triage decisions."""

    # Elite Outside Orthopedic Centers of Excellence
    SPECIALIST_CENTERS: Dict[str, SecondOpinionCenter] = {
        "andrews_sports_med": SecondOpinionCenter(
            center_id="andrews_sports_med",
            name="Andrews Sports Medicine & Orthopaedic Center",
            specialty_region="Knee, Ligament & UCL Reconstruction (Birmingham, AL)",
            chief_surgeon="Dr. James Andrews, MD",
            consultation_cost=45000,
            turnaround_days=3,
            diagnostic_accuracy_boost=0.25,
        ),
        "kerlan_jobe": SecondOpinionCenter(
            center_id="kerlan_jobe",
            name="Kerlan-Jobe Orthopaedic Clinic",
            specialty_region="Shoulder, Elbow, Rotator Cuff & Spine (Los Angeles, CA)",
            chief_surgeon="Dr. Neal ElAttrache, MD",
            consultation_cost=35000,
            turnaround_days=2,
            diagnostic_accuracy_boost=0.20,
        ),
        "hss_ny": SecondOpinionCenter(
            center_id="hss_ny",
            name="Hospital for Special Surgery (HSS)",
            specialty_region="Foot, Ankle, Hip, Turf Toe & Complex Joint (New York, NY)",
            chief_surgeon="Dr. Bryan Kelly, MD",
            consultation_cost=50000,
            turnaround_days=2,
            diagnostic_accuracy_boost=0.25,
        ),
    }

    def get_specialist_centers(self) -> List[SecondOpinionCenter]:
        """Return list of available elite outside orthopedic consultation centers."""
        return list(self.SPECIALIST_CENTERS.values())

    def compute_gompertz_point(
        self,
        t: float,
        h0: float,
        h_max: float,
        k: float,
        t0: float,
    ) -> float:
        """
        Compute non-linear Gompertz tissue repair percentage at week t.
        Formula: H(t) = H0 + (H_max - H0) * exp(-exp(-k * (t - t0)))
        Clamped strictly between 0.0 and 100.0.
        """
        exponent = -k * (t - t0)
        # Numerical protection against overflow/underflow
        if exponent > 50.0:
            double_exp = 0.0
        elif exponent < -50.0:
            double_exp = math.exp(50.0)
        else:
            double_exp = math.exp(exponent)

        growth_fraction = math.exp(-double_exp)
        calculated_health = h0 + (h_max - h0) * growth_fraction
        return max(0.0, min(100.0, round(calculated_health, 2)))

    def generate_rtp_evaluation(
        self,
        player_id: int,
        injury_type: str = "Joint Sprain",
        body_part: str = "right_leg",
        severity_grade: int = 3,
        baseline_health: float = 55.0,
        player_name: Optional[str] = None,
        player_age: int = 26,
        durability_rating: int = 80,
        is_cortisone_active: bool = False,
        has_specialist_clearance: bool = False,
        specialist_center_name: Optional[str] = None,
    ) -> OrthopedicEvaluationResponse:
        """
        Compute 12-week comparative trajectory curves across 5 protocols using Gompertz non-linear dynamics.
        Execution budget: <2.5ms.
        """
        # Durability and age modifiers
        durability_mod = 0.8 + (durability_rating / 100.0) * 0.4  # e.g., 80 -> 1.12
        age_mod = max(0.75, 1.0 - max(0, player_age - 28) * 0.03)  # older heals slower
        combined_rate_mod = durability_mod * age_mod

        # Initial tissue integrity based on severity
        clamped_h0 = max(20.0, min(80.0, baseline_health))
        h_target = 100.0

        # Specialist clearance cuts surgical complication risk in half
        complication_factor = 0.50 if has_specialist_clearance else 1.0

        trajectories: List[TreatmentTrajectory] = []

        # -------------------------------------------------------------
        # 1. Conservative Rest & Physical Therapy
        # -------------------------------------------------------------
        cons_k = 0.45 * combined_rate_mod
        cons_t0 = 4.0
        cons_est_weeks = max(3, int(round(severity_grade * 1.5 * (1.0 / combined_rate_mod))))
        cons_curve: List[RTPCurvePoint] = []
        for w in range(13):
            h_w = self.compute_gompertz_point(w, clamped_h0, h_target, cons_k, cons_t0)
            re_inj = max(2.0, min(95.0, (100.0 - h_w) * 0.70))
            eff = min(100.0, round(h_w * 1.02, 1)) if h_w >= 85.0 else min(80.0, round(h_w * 0.90, 1))
            cons_curve.append(
                RTPCurvePoint(
                    week=w,
                    health_percentage=h_w,
                    re_injury_risk_pct=round(re_inj, 1),
                    on_field_effectiveness_pct=round(eff, 1),
                )
            )

        trajectories.append(
            TreatmentTrajectory(
                protocol="CONSERVATIVE",
                label="Conservative Rest & Physical Therapy",
                est_recovery_weeks=cons_est_weeks,
                complication_risk_pct=0.0,
                total_medical_cost=0,
                curve=cons_curve,
            )
        )

        # -------------------------------------------------------------
        # 2. Platelet-Rich Plasma (PRP) Biotherapy
        # -------------------------------------------------------------
        prp_k = 0.65 * combined_rate_mod
        prp_t0 = 2.5
        prp_est_weeks = max(2, int(round(cons_est_weeks * 0.70)))
        prp_curve: List[RTPCurvePoint] = []
        for w in range(13):
            h_w = self.compute_gompertz_point(w, clamped_h0, 96.0, prp_k, prp_t0)
            re_inj = max(2.5, min(95.0, (100.0 - h_w) * 0.65 * 1.10))
            eff = min(100.0, round(h_w * 1.04, 1)) if h_w >= 85.0 else min(80.0, round(h_w * 0.92, 1))
            prp_curve.append(
                RTPCurvePoint(
                    week=w,
                    health_percentage=h_w,
                    re_injury_risk_pct=round(re_inj, 1),
                    on_field_effectiveness_pct=round(eff, 1),
                )
            )

        trajectories.append(
            TreatmentTrajectory(
                protocol="BIOLOGIC_PRP",
                label="Platelet-Rich Plasma (PRP) Biotherapy",
                est_recovery_weeks=prp_est_weeks,
                complication_risk_pct=round(5.0 * complication_factor, 1),
                total_medical_cost=8500,
                curve=prp_curve,
            )
        )

        # -------------------------------------------------------------
        # 3. Accelerated Arthroscopic Repair (Scope)
        # -------------------------------------------------------------
        arthro_h0 = max(15.0, clamped_h0 - 8.0)  # acute post-op deficit
        arthro_k = 0.85 * combined_rate_mod
        arthro_t0 = 3.0
        arthro_est_weeks = max(2, int(round(cons_est_weeks * 0.50)))
        arthro_curve: List[RTPCurvePoint] = []
        for w in range(13):
            h_w = self.compute_gompertz_point(w, arthro_h0, 94.0, arthro_k, arthro_t0)
            re_inj = max(3.0, min(95.0, (100.0 - h_w) * 0.60 * 1.25))
            eff = min(100.0, round(h_w * 1.05, 1)) if h_w >= 85.0 else min(80.0, round(h_w * 0.88, 1))
            arthro_curve.append(
                RTPCurvePoint(
                    week=w,
                    health_percentage=h_w,
                    re_injury_risk_pct=round(re_inj, 1),
                    on_field_effectiveness_pct=round(eff, 1),
                )
            )

        trajectories.append(
            TreatmentTrajectory(
                protocol="ARTHROSCOPIC",
                label="Accelerated Arthroscopic Repair",
                est_recovery_weeks=arthro_est_weeks,
                complication_risk_pct=round(12.0 * complication_factor, 1),
                total_medical_cost=28000,
                curve=arthro_curve,
            )
        )

        # -------------------------------------------------------------
        # 4. Open Structural Reconstruction
        # -------------------------------------------------------------
        recon_h0 = max(10.0, clamped_h0 - 15.0)  # heavy surgical trauma
        recon_k = 0.70 * combined_rate_mod
        recon_t0 = 5.0
        recon_est_weeks = max(6, int(round(cons_est_weeks * 1.25)))
        recon_curve: List[RTPCurvePoint] = []
        for w in range(13):
            h_w = self.compute_gompertz_point(w, recon_h0, 99.0, recon_k, recon_t0)
            re_inj = max(1.5, min(95.0, (100.0 - h_w) * 0.50 * 0.90))
            eff = min(100.0, round(h_w * 1.05, 1)) if h_w >= 85.0 else min(75.0, round(h_w * 0.85, 1))
            recon_curve.append(
                RTPCurvePoint(
                    week=w,
                    health_percentage=h_w,
                    re_injury_risk_pct=round(re_inj, 1),
                    on_field_effectiveness_pct=round(eff, 1),
                )
            )

        trajectories.append(
            TreatmentTrajectory(
                protocol="OPEN_SURGERY",
                label="Full Structural Reconstruction",
                est_recovery_weeks=recon_est_weeks,
                complication_risk_pct=round(8.0 * complication_factor, 1),
                total_medical_cost=65000,
                curve=recon_curve,
            )
        )

        # -------------------------------------------------------------
        # 5. Cortisone Joint Injection (Suit Up & Play)
        # -------------------------------------------------------------
        cort_k = 0.18 * combined_rate_mod  # very slow structural repair
        cort_t0 = 7.0
        cort_curve: List[RTPCurvePoint] = []
        for w in range(13):
            h_w = self.compute_gompertz_point(w, clamped_h0, 85.0, cort_k, cort_t0)
            # 2.5x acute re-injury hazard multiplier
            re_inj = max(15.0, min(95.0, (100.0 - h_w) * 0.90 * 2.5))
            # Pain masked to 95% effectiveness while cortisone active (weeks 0-3)
            eff = 95.0 if w <= 3 else min(95.0, round(h_w * 1.02, 1))
            cort_curve.append(
                RTPCurvePoint(
                    week=w,
                    health_percentage=h_w,
                    re_injury_risk_pct=round(re_inj, 1),
                    on_field_effectiveness_pct=round(eff, 1),
                )
            )

        trajectories.append(
            TreatmentTrajectory(
                protocol="CORTISONE",
                label="Cortisone Joint Injection (Suit Up & Play)",
                est_recovery_weeks=0,
                complication_risk_pct=35.0,
                total_medical_cost=2500,
                curve=cort_curve,
            )
        )

        return OrthopedicEvaluationResponse(
            player_id=player_id,
            player_name=player_name,
            injury_type=injury_type,
            body_part=body_part,
            severity_grade=severity_grade,
            baseline_health=clamped_h0,
            is_cortisone_active=is_cortisone_active,
            has_specialist_clearance=has_specialist_clearance,
            specialist_center_name=specialist_center_name,
            trajectories=trajectories,
            specialist_centers=self.get_specialist_centers(),
            cortisone_in_game_hazard_multiplier=2.5,
        )

    def consult_outside_specialist(
        self,
        db: Session,
        player_id: int,
        center_id: str,
        seed: Optional[int] = None,
    ) -> SecondOpinionConsultResult:
        """
        Dispatch an injured player to an elite outside orthopedic clinic.
        - Deducts consultation fee from team medical budget / finances.
        - 15% probability of discovering occult pathology (upgrading diagnosis).
        - Applies 50% complication risk reduction factor to surgical procedures.
        """
        if center_id not in self.SPECIALIST_CENTERS:
            raise ValueError(f"Unknown specialist center: {center_id}")

        center = self.SPECIALIST_CENTERS[center_id]

        from app.models.player import Player
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise ValueError(f"Player {player_id} not found")

        orig_diag = player.injury_type or "Soft Tissue Trauma"
        severity = player.injury_severity or 3

        # Deterministic or controlled RNG for consult outcome
        rng = random.Random(seed if seed is not None else (player_id * 1000 + int(time.time())))
        occult_roll = rng.random()
        occult_detected = occult_roll < 0.15  # 15% probability of occult misdiagnosis

        if occult_detected:
            confirmed_diag = f"{orig_diag} with Occult Subchondral Avulsion & Labral Micro-Tear"
            findings_narrative = (
                f"High-resolution 3T MRI at {center.name} under {center.chief_surgeon} revealed occult "
                f"subchondral avulsion and micro-tears masked during primary team examination. "
                f"Surgical arthroscopy or biologic PRP is strongly recommended over conservative rest."
            )
            rec_protocol = "ARTHROSCOPIC"
        else:
            confirmed_diag = orig_diag
            findings_narrative = (
                f"{center.chief_surgeon} at {center.name} confirmed the primary team diagnosis of {orig_diag}. "
                f"Joint stability and neurovascular bundle remain intact. Biologic PRP or conservative rehab indicated."
            )
            rec_protocol = "BIOLOGIC_PRP" if severity >= 4 else "CONSERVATIVE"

        # Update player injury medical flags in database
        from app.models.player_injury import PlayerInjury
        injury_record = player.injury
        if not injury_record:
            injury_record = PlayerInjury(player_id=player.id)
            db.add(injury_record)
            player.injury = injury_record

        flags = dict(injury_record.medical_flags or {})
        flags["specialist_cleared"] = True
        flags["specialist_center_id"] = center_id
        flags["specialist_center_name"] = center.name
        flags["chief_surgeon"] = center.chief_surgeon
        flags["complication_reduction_factor"] = 0.50
        flags["confirmed_diagnosis"] = confirmed_diag
        flags["occult_pathology_detected"] = occult_detected

        injury_record.medical_flags = flags
        if occult_detected:
            injury_record.injury_type = confirmed_diag

        db.commit()
        db.refresh(player)

        return SecondOpinionConsultResult(
            player_id=player.id,
            center_id=center_id,
            center_name=center.name,
            chief_surgeon=center.chief_surgeon,
            original_diagnosis=orig_diag,
            confirmed_diagnosis=confirmed_diag,
            occult_pathology_detected=occult_detected,
            findings_narrative=findings_narrative,
            recommended_protocol=rec_protocol,
            complication_reduction_factor=0.50,
            consultation_cost=center.consultation_cost,
        )

    def evaluate_cortisone_in_game_hazard(
        self,
        runner_has_cortisone: bool,
        is_sharp_cut: bool = False,
        momentum: float = 0.0,
        g_force: float = 0.0,
        seed: Optional[int] = None,
    ) -> CortisoneHazardCheckResponse:
        """
        Evaluate in-game 60Hz physics hazard for runners playing under cortisone stabilization.
        - Hazard multiplier: 2.5x.
        - Evaluated on sharp cuts (delta_v > 4.5 m/s^2) and tackles (momentum > 850 kg*m/s).
        - Latency: <0.001ms.
        """
        if not runner_has_cortisone:
            return CortisoneHazardCheckResponse(
                catastrophic_rupture=False,
                hazard_multiplier=1.0,
                effective_risk_pct=0.5,
                event_message="Normal tissue integrity; standard baseline strain.",
            )

        hazard_mult = 2.5
        base_strain_risk = 0.012  # 1.2% base cut strain probability

        cut_multiplier = 2.2 if is_sharp_cut else 1.0
        momentum_multiplier = 1.0 + max(0.0, (momentum - 700.0) / 300.0) if momentum > 700.0 else 1.0
        g_force_multiplier = 1.0 + max(0.0, (g_force - 8.0) / 10.0) if g_force > 8.0 else 1.0

        effective_prob = base_strain_risk * hazard_mult * cut_multiplier * momentum_multiplier * g_force_multiplier
        effective_prob = max(0.01, min(0.75, effective_prob))

        rng = random.Random(seed if seed is not None else int(time.time() * 1000000) % 1000000)
        roll = rng.random()
        rupture_occurred = roll < effective_prob

        if rupture_occurred:
            msg = (
                f"CATASTROPHIC RE-RUPTURE! Player playing under Cortisone suffered severe Grade III tissue failure "
                f"during high-shear cut (Hazard 2.5x, Momentum {round(momentum, 1)} kg*m/s, G-Force {round(g_force, 1)}G)."
            )
        else:
            msg = (
                f"Cortisone stabilization held. High-G cut survived (Hazard 2.5x, Risk {round(effective_prob * 100, 1)}%)."
            )

        return CortisoneHazardCheckResponse(
            catastrophic_rupture=rupture_occurred,
            hazard_multiplier=hazard_mult,
            effective_risk_pct=round(effective_prob * 100.0, 2),
            event_message=msg,
        )


orthopedic_engine = OrthopedicEngine()

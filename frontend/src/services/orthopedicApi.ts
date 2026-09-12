/**
 * Orthopedic API Client & Offline Trajectory Fallback Engine
 * ==========================================================
 * Connects frontend to FastAPI /api/orthopedic endpoints with
 * mathematical fallback Gompertz trajectory modeling.
 */

import { apiClient } from "./api";
import type {
  OrthopedicEvaluationResponse,
  SecondOpinionCenter,
  SecondOpinionRequest,
  SecondOpinionConsultResult,
  CortisoneHazardCheckRequest,
  CortisoneHazardCheckResponse,
  TreatmentTrajectory,
  RTPCurvePoint,
} from "../types/orthopedicRtp";

// Raw backend response snake_case mapping helper
interface RawRTPCurvePoint {
  week: number;
  health_percentage: number;
  re_injury_risk_pct: number;
  on_field_effectiveness_pct: number;
}

interface RawTreatmentTrajectory {
  protocol: "CONSERVATIVE" | "BIOLOGIC_PRP" | "ARTHROSCOPIC" | "OPEN_SURGERY" | "CORTISONE";
  label: string;
  est_recovery_weeks: number;
  complication_risk_pct: number;
  total_medical_cost: number;
  curve: RawRTPCurvePoint[];
}

interface RawSecondOpinionCenter {
  center_id: string;
  name: string;
  specialty_region: string;
  chief_surgeon: string;
  consultation_cost: number;
  turnaround_days: number;
  diagnostic_accuracy_boost: number;
}

interface RawSecondOpinionConsultResult {
  player_id: number;
  center_id: string;
  center_name: string;
  chief_surgeon: string;
  original_diagnosis: string;
  confirmed_diagnosis: string;
  occult_pathology_detected: bool;
  findings_narrative: string;
  recommended_protocol: string;
  complication_reduction_factor: number;
  consultation_cost: number;
}

interface RawOrthopedicEvaluationResponse {
  player_id: number;
  player_name?: string;
  injury_type: string;
  body_part: string;
  severity_grade: number;
  baseline_health: number;
  is_cortisone_active: bool;
  has_specialist_clearance: bool;
  specialist_center_name?: string | null;
  trajectories: RawTreatmentTrajectory[];
  specialist_centers: RawSecondOpinionCenter[];
  cortisone_in_game_hazard_multiplier: number;
}

type bool = boolean;

function mapEvaluationResponse(raw: RawOrthopedicEvaluationResponse): OrthopedicEvaluationResponse {
  return {
    playerId: raw.player_id,
    playerName: raw.player_name,
    injuryType: raw.injury_type,
    bodyPart: raw.body_part,
    severityGrade: raw.severity_grade,
    baselineHealth: raw.baseline_health,
    isCortisoneActive: raw.is_cortisone_active,
    hasSpecialistClearance: raw.has_specialist_clearance,
    specialistCenterName: raw.specialist_center_name,
    cortisoneInGameHazardMultiplier: raw.cortisone_in_game_hazard_multiplier,
    trajectories: raw.trajectories.map((t) => ({
      protocol: t.protocol,
      label: t.label,
      estRecoveryWeeks: t.est_recovery_weeks,
      complicationRiskPct: t.complication_risk_pct,
      totalMedicalCost: t.total_medical_cost,
      curve: t.curve.map((p) => ({
        week: p.week,
        healthPercentage: p.health_percentage,
        reInjuryRiskPct: p.re_injury_risk_pct,
        onFieldEffectivenessPct: p.on_field_effectiveness_pct,
      })),
    })),
    specialistCenters: raw.specialist_centers.map((c) => ({
      centerId: c.center_id,
      name: c.name,
      specialtyRegion: c.specialty_region,
      chiefSurgeon: c.chief_surgeon,
      consultationCost: c.consultation_cost,
      turnaroundDays: c.turnaround_days,
      diagnosticAccuracyBoost: c.diagnostic_accuracy_boost,
    })),
  };
}

function computeGompertzPoint(t: number, h0: number, hMax: number, k: number, t0: number): number {
  const exponent = -k * (t - t0);
  const doubleExp = Math.exp(Math.max(-50, Math.min(50, exponent)));
  const growth = Math.exp(-doubleExp);
  const health = h0 + (hMax - h0) * growth;
  return Math.max(0, Math.min(100, Math.round(health * 10) / 10));
}

export function generateFallbackEvaluation(
  playerId: number,
  injuryType: string = "Meniscus Tear",
  bodyPart: string = "right_leg",
  severityGrade: number = 4,
  baselineHealth: number = 55
): OrthopedicEvaluationResponse {
  const h0 = Math.max(20, Math.min(80, baselineHealth));
  const protocols: Array<{
    protocol: TreatmentTrajectory["protocol"];
    label: string;
    weeks: number;
    compRisk: number;
    cost: number;
    k: number;
    t0: number;
    hTarget: number;
    initialOffset: number;
    hazardMult: number;
  }> = [
    {
      protocol: "CONSERVATIVE",
      label: "Conservative Rest & Physical Therapy",
      weeks: 6,
      compRisk: 0.0,
      cost: 0,
      k: 0.45,
      t0: 4.0,
      hTarget: 100.0,
      initialOffset: 0,
      hazardMult: 1.0,
    },
    {
      protocol: "BIOLOGIC_PRP",
      label: "Platelet-Rich Plasma (PRP) Biotherapy",
      weeks: 4,
      compRisk: 5.0,
      cost: 8500,
      k: 0.65,
      t0: 2.5,
      hTarget: 96.0,
      initialOffset: 0,
      hazardMult: 1.1,
    },
    {
      protocol: "ARTHROSCOPIC",
      label: "Accelerated Arthroscopic Scope",
      weeks: 3,
      compRisk: 12.0,
      cost: 28000,
      k: 0.85,
      t0: 3.0,
      hTarget: 94.0,
      initialOffset: -8,
      hazardMult: 1.25,
    },
    {
      protocol: "OPEN_SURGERY",
      label: "Full Structural Reconstruction",
      weeks: 8,
      compRisk: 8.0,
      cost: 65000,
      k: 0.7,
      t0: 5.0,
      hTarget: 99.0,
      initialOffset: -15,
      hazardMult: 0.9,
    },
    {
      protocol: "CORTISONE",
      label: "Cortisone Joint Injection (Suit Up & Play)",
      weeks: 0,
      compRisk: 35.0,
      cost: 2500,
      k: 0.18,
      t0: 7.0,
      hTarget: 85.0,
      initialOffset: 0,
      hazardMult: 2.5,
    },
  ];

  const trajectories: TreatmentTrajectory[] = protocols.map((p) => {
    const startH = Math.max(15, h0 + p.initialOffset);
    const curve: RTPCurvePoint[] = [];
    for (let w = 0; w <= 12; w++) {
      const health = computeGompertzPoint(w, startH, p.hTarget, p.k, p.t0);
      const reInj = Math.max(2, Math.min(95, (100 - health) * 0.7 * p.hazardMult));
      const eff =
        p.protocol === "CORTISONE" && w <= 3 ? 95 : Math.min(100, Math.round(health * 1.03));
      curve.push({
        week: w,
        healthPercentage: health,
        reInjuryRiskPct: Math.round(reInj * 10) / 10,
        onFieldEffectivenessPct: eff,
      });
    }
    return {
      protocol: p.protocol,
      label: p.label,
      estRecoveryWeeks: p.weeks,
      complicationRiskPct: p.compRisk,
      totalMedicalCost: p.cost,
      curve,
    };
  });

  return {
    playerId,
    injuryType,
    bodyPart,
    severityGrade,
    baselineHealth: h0,
    isCortisoneActive: false,
    hasSpecialistClearance: false,
    cortisoneInGameHazardMultiplier: 2.5,
    trajectories,
    specialistCenters: [
      {
        centerId: "andrews_sports_med",
        name: "Andrews Sports Medicine & Orthopaedic Center",
        specialtyRegion: "Knee, Ligament & UCL Reconstruction (Birmingham, AL)",
        chiefSurgeon: "Dr. James Andrews, MD",
        consultationCost: 45000,
        turnaroundDays: 3,
        diagnosticAccuracyBoost: 0.25,
      },
      {
        centerId: "kerlan_jobe",
        name: "Kerlan-Jobe Orthopaedic Clinic",
        specialtyRegion: "Shoulder, Elbow, Rotator Cuff & Spine (Los Angeles, CA)",
        chiefSurgeon: "Dr. Neal ElAttrache, MD",
        consultationCost: 35000,
        turnaroundDays: 2,
        diagnosticAccuracyBoost: 0.2,
      },
      {
        centerId: "hss_ny",
        name: "Hospital for Special Surgery (HSS)",
        specialtyRegion: "Foot, Ankle, Hip, Turf Toe & Complex Joint (New York, NY)",
        chiefSurgeon: "Dr. Bryan Kelly, MD",
        consultationCost: 50000,
        turnaroundDays: 2,
        diagnosticAccuracyBoost: 0.25,
      },
    ],
  };
}

export const orthopedicApi = {
  /**
   * Fetch 12-week Gompertz trajectory evaluation for an athlete.
   */
  async getOrthopedicEvaluation(playerId: number): Promise<OrthopedicEvaluationResponse> {
    try {
      const response = await apiClient.get<RawOrthopedicEvaluationResponse>(
        `/api/orthopedic/evaluation/${playerId}`
      );
      return mapEvaluationResponse(response.data);
    } catch (err) {
      console.warn(
        "Failed to fetch live evaluation, generating fallback Gompertz trajectories:",
        err
      );
      return generateFallbackEvaluation(playerId);
    }
  },

  /**
   * Fetch available outside orthopedic consultation centers.
   */
  async getSpecialistCenters(): Promise<SecondOpinionCenter[]> {
    try {
      const response = await apiClient.get<RawSecondOpinionCenter[]>("/api/orthopedic/specialists");
      return response.data.map((c) => ({
        centerId: c.center_id,
        name: c.name,
        specialtyRegion: c.specialty_region,
        chiefSurgeon: c.chief_surgeon,
        consultationCost: c.consultation_cost,
        turnaroundDays: c.turnaround_days,
        diagnosticAccuracyBoost: c.diagnostic_accuracy_boost,
      }));
    } catch {
      return generateFallbackEvaluation(1).specialistCenters;
    }
  },

  /**
   * Dispatch athlete to outside specialist clinic for second opinion.
   */
  async consultSpecialist(request: SecondOpinionRequest): Promise<SecondOpinionConsultResult> {
    const rawPayload = {
      player_id: request.playerId,
      center_id: request.centerId,
    };
    const response = await apiClient.post<RawSecondOpinionConsultResult>(
      "/api/orthopedic/specialists/consult",
      rawPayload
    );
    const raw = response.data;
    return {
      playerId: raw.player_id,
      centerId: raw.center_id,
      centerName: raw.center_name,
      chiefSurgeon: raw.chief_surgeon,
      originalDiagnosis: raw.original_diagnosis,
      confirmedDiagnosis: raw.confirmed_diagnosis,
      occultPathologyDetected: raw.occult_pathology_detected,
      findingsNarrative: raw.findings_narrative,
      recommendedProtocol: raw.recommended_protocol,
      complicationReductionFactor: raw.complication_reduction_factor,
      consultationCost: raw.consultation_cost,
    };
  },

  /**
   * Check in-game cortisone strain hazard under cut and tackle telemetry.
   */
  async checkCortisoneHazard(
    request: CortisoneHazardCheckRequest
  ): Promise<CortisoneHazardCheckResponse> {
    const rawPayload = {
      runner_has_cortisone: request.runnerHasCortisone,
      is_sharp_cut: request.isSharpCut ?? false,
      momentum: request.momentum ?? 0,
      g_force: request.gForce ?? 0,
    };
    const response = await apiClient.post<{
      catastrophic_rupture: bool;
      hazard_multiplier: number;
      effective_risk_pct: number;
      event_message: string;
    }>("/api/orthopedic/cortisone/check-hazard", rawPayload);

    return {
      catastrophicRupture: response.data.catastrophic_rupture,
      hazardMultiplier: response.data.hazard_multiplier,
      effectiveRiskPct: response.data.effective_risk_pct,
      eventMessage: response.data.event_message,
    };
  },
};

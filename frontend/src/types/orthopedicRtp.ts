/**
 * Orthopedic RTP Projection Trajectory & Re-Injury Hazard Types
 * =============================================================
 * Strict TypeScript contracts for:
 * 1. 12-week Gompertz tissue repair trajectory curves
 * 2. Elite outside specialist consultation centers & findings
 * 3. In-game Cortisone 2.5x hazard multipliers
 */

export type MedicalProtocol =
  | "CONSERVATIVE"
  | "BIOLOGIC_PRP"
  | "ARTHROSCOPIC"
  | "OPEN_SURGERY"
  | "CORTISONE";

export interface RTPCurvePoint {
  week: number;
  healthPercentage: number;
  reInjuryRiskPct: number;
  onFieldEffectivenessPct: number;
}

export interface TreatmentTrajectory {
  protocol: MedicalProtocol;
  label: string;
  estRecoveryWeeks: number;
  complicationRiskPct: number;
  totalMedicalCost: number;
  curve: RTPCurvePoint[];
}

export interface SecondOpinionCenter {
  centerId: string;
  name: string;
  specialtyRegion: string;
  chiefSurgeon: string;
  consultationCost: number;
  turnaroundDays: number;
  diagnosticAccuracyBoost: number;
}

export interface SecondOpinionRequest {
  playerId: number;
  centerId: string;
}

export interface SecondOpinionConsultResult {
  playerId: number;
  centerId: string;
  centerName: string;
  chiefSurgeon: string;
  originalDiagnosis: string;
  confirmedDiagnosis: string;
  occultPathologyDetected: boolean;
  findingsNarrative: string;
  recommendedProtocol: string;
  complicationReductionFactor: number;
  consultationCost: number;
}

export interface CortisoneHazardCheckRequest {
  runnerHasCortisone: boolean;
  isSharpCut?: boolean;
  momentum?: number;
  gForce?: number;
}

export interface CortisoneHazardCheckResponse {
  catastrophicRupture: boolean;
  hazardMultiplier: number;
  effectiveRiskPct: number;
  eventMessage: string;
}

export interface OrthopedicEvaluationResponse {
  playerId: number;
  playerName?: string;
  injuryType: string;
  bodyPart: string;
  severityGrade: number;
  baselineHealth: number;
  isCortisoneActive: boolean;
  hasSpecialistClearance: boolean;
  specialistCenterName?: string | null;
  trajectories: TreatmentTrajectory[];
  specialistCenters: SecondOpinionCenter[];
  cortisoneInGameHazardMultiplier: number;
}

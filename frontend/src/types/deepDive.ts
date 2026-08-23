/**
 * Deep Dive Simulation Subsystems Types
 * =====================================
 * Contract-synchronized with backend/app/schemas/deep_dive.py
 */

export type ScoutBiasLens =
  | "CONSENSUS"
  | "FILM_TRADITIONALIST"
  | "ANALYTICS_METRICS"
  | "REGIONAL_SCOUT";

export interface ProspectIntelligence {
  id: number;
  name: string;
  position: string;
  college: string;
  true_ovr: number;
  consensus_ovr: number;
  perceived_ovr: Record<ScoutBiasLens, number>;
  s2_cognition_score: number;
  gps_speed_max: number;
  burst_score: number;
  boom_bust_factor: number;
  scheme_fit_percentage: number;
  medical_grade: "PASS" | "CONCERN" | "FAIL";
  draft_projection_round: number;
}

export interface DraftTradeUrgency {
  team_id: string;
  target_position: string;
  urgency_index: number;
  willing_to_overpay_pct: number;
  suggested_package_value: number;
}

export type CoachingBranch = "SCHEME_TACTICS" | "DEVELOPMENT" | "PROGRAM_CULTURE";

export interface CoachingSkillNode {
  id: string;
  name: string;
  branch: CoachingBranch;
  tier: number;
  unlocked: boolean;
  sp_cost: number;
  bonus_description: string;
  prerequisites: string[];
  stat_multiplier: number;
}

export interface StaffSynergyBreakdown {
  head_coach_id: string;
  offensive_coord_id: string;
  defensive_coord_id: string;
  offensive_synergy_score: number;
  defensive_synergy_score: number;
  overall_chemistry_score: number;
  active_synergy_perks: string[];
  scheme_alignment_notes: string[];
}

export interface CoachDynastyProfile {
  coach_id: string;
  name: string;
  role: string;
  level: number;
  current_sp: number;
  total_sp_earned: number;
  archetype: string;
  tree_nodes: Record<string, CoachingSkillNode>;
}

export type MedicalProtocolType =
  | "REST"
  | "PRP_THERAPY"
  | "ARTHROSCOPIC_SURGERY"
  | "RECONSTRUCTIVE_SURGERY"
  | "CORTISONE_STABILIZATION";

export interface OrthopedicProtocolOption {
  protocol: MedicalProtocolType;
  name: string;
  estimated_recovery_weeks: number;
  complication_risk_pct: number;
  target_integrity_restore: number;
  re_injury_hazard_multiplier: number;
  game_availability_status: "OUT" | "DOUBTFUL" | "QUESTIONABLE" | "ACTIVE";
  description: string;
  clinical_note?: string;
}

export interface TriageDecisionResult {
  player_id: number;
  zone_key: string;
  protocol_applied: MedicalProtocolType;
  projected_recovery_weeks: number;
  complication_occurred: boolean;
  final_integrity_forecast: number;
  re_injury_risk_index: number;
  message: string;
}

export interface BodyHealth {
  player_id: number;
  head_health: number;
  neck_health: number;
  torso_health: number;
  right_arm_health: number;
  left_arm_health: number;
  right_leg_health: number;
  left_leg_health: number;
  general_wear: number;
  is_injured: boolean;
}

export interface BioMetrics {
  fast_twitch_ratio: number;
  max_acceleration_cap: number;
  hand_size_inches: number;
  wingspan_inches: number;
  interaction_radius: number;
  fumble_risk: number;
  power_clean_max?: number;
  gps_speed_max?: number;
  s2_cognition_score?: number;
  medical_flags?: string[];
  genesis_revealed?: boolean;
}

export interface FatigueState {
  hrv: number;
  lactic_acid: number;
  max_burst_capacity: number;
  home_climate: string;
  atp_pc?: number;
  glycolytic?: number;
  aerobic?: number;
  neural?: number;
}

export type TreatmentType = "REST" | "SURGERY" | "PLAY_THROUGH";

export interface TreatmentDecisionRequest {
  player_id: number;
  treatment: TreatmentType;
}

export interface TreatmentDecisionResponse {
  player_id: number;
  treatment: TreatmentType;
  recovery_weeks: number;
  surgery_risk?: number;
  performance_penalty?: Record<string, number>;
}

export interface InjuredPlayer {
  player_id: number;
  first_name: string;
  last_name: string;
  position: string;
  injury_type?: string;
  injury_status: string;
  severity: number;
  weeks_remaining: number;
  body_part?: string;
}

export interface SurgeryRisk {
  player_id: number;
  base_risk: number;
  age_risk: number;
  severity_risk: number;
  total_risk: number;
  estimated_recovery_reduction: number;
}

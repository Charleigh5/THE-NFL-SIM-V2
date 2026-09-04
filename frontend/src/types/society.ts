/**
 * Society Engine Contracts (2025/2026 Production Standard)
 * ========================================================
 * Synchronized with backend/app/schemas/society.py
 */

export interface PsychologicalDNA {
  ego: number;
  greed: number;
  loyalty: number;
  resilience: number;
  paranoia: number;
  professionalism: number;
}

export interface PlayerBackstory {
  origin?: string;
  financial_motive?: string;
  career_milestone?: string;
  draft_narrative?: string;
  mentor_id?: number | null;
  rival_id?: number | null;
}

export interface TensionDelta {
  player_id: number;
  prior_tension: number;
  new_tension: number;
  primary_driver: string;
  morale_delta: number;
  is_active_grievance: boolean;
}

export interface LockerRoomDialogueTurn {
  speaker_name: string;
  speaker_role: string;
  speaker_id?: number | null;
  text: string;
}

export interface LockerRoomConsequences {
  morale_deltas: Record<string, number>;
  trust_coach_deltas: Record<string, number>;
  trust_qb_deltas: Record<string, number>;
  trade_requested: boolean;
  team_chemistry_delta: number;
  drama_headline: string;
}

export interface LockerRoomActionOption {
  id: string;
  label: string;
  description: string;
  projected_impact: string;
}

export interface LockerRoomEventResponse {
  team_id: number;
  week: number;
  active_actors: number[];
  captain_id?: number | null;
  headline: string;
  dialogue: LockerRoomDialogueTurn[];
  consequences: LockerRoomConsequences;
  action_options: LockerRoomActionOption[];
  summary: string;
}

export interface LockerRoomResolutionRequest {
  team_id: number;
  action_id: string;
  week: number;
  active_actor_ids: number[];
}

export interface LockerRoomResolutionResponse {
  team_id: number;
  action_id: string;
  success: boolean;
  message: string;
  updated_chemistry: number;
}

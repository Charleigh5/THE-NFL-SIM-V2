export type AbilityStatusType = "LOCKED" | "AVAILABLE" | "UNLOCKED";

export interface AbilityDefinition {
  key: string;
  name: string;
  description: string;
  position_requirements: string[];
  level_requirement: number;
  xp_cost: number;
  effects: Record<string, number>;
}

export interface PlayerAbilityStatus {
  key: string;
  name: string;
  description: string;
  status: AbilityStatusType;
  level_required: number;
  xp_cost: number;
  reason: string;
  effects: Record<string, number>;
}

export interface UnlockAbilityResponse {
  success: boolean;
  message: string;
  remaining_xp?: number;
}

export interface PreSnapInsightRequest {
  qb_id: number;
  defensive_coordinator_id?: number;
}

export interface PreSnapInsightResponse {
  has_ability: boolean;
  predicted_coverage?: string;
  confidence?: "High" | "Medium" | "Low" | string;
  key_read?: string;
  is_correct?: boolean;
}

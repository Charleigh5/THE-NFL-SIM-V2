import type { InteractionResult } from "./interaction";

export interface PlayResult {
  play_id?: string | number;
  play_type?: string;
  quarter?: number;
  time_remaining?: number;
  yard_line?: number;
  down?: number;
  distance?: number;
  yards_gained: number;
  is_touchdown: boolean;
  is_turnover?: boolean;
  is_interception?: boolean;
  is_fumble?: boolean;
  is_incomplete?: boolean;
  is_sack: boolean;
  is_penalty: boolean;
  is_safety?: boolean;
  points_scored?: number;
  penalty_yards: number;
  time_elapsed: number;
  description: string;
  passer_id?: number;
  receiver_id?: number;
  rusher_id?: number;
  tackler_ids: number[];
  weather_impact: number;
  turf_impact: number;
  injuries: Record<string, unknown>[];
  fatigue_deltas: Record<number, number>;
  xp_awards: Record<number, number>;
  headline?: string;
  is_highlight_worthy: boolean;
  interaction_events: InteractionResult[];
}

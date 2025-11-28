export interface PlayResult {
  yards_gained: number;
  is_touchdown: boolean;
  is_turnover: boolean;
  is_sack: boolean;
  is_penalty: boolean;
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
}

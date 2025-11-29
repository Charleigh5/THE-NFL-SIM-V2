export interface TeamNeed {
  position: string;
  current_count: number;
  target_count: number;
  need_score: number;
}

export interface Prospect {
  id: number;
  name: string;
  position: string;
  overall_rating: number;
}

export interface DraftPickSummary {
  round: number;
  pick_number: number;
  team_id: number;
  player_name: string;
  player_position: string;
  player_overall: number;
}

export interface PlayerProgressionResult {
  player_id: number;
  name: string;
  position: string;
  change: number;
  old_rating: number;
  new_rating: number;
}

export interface TeamNeed {
  position: string;
  current_count: number;
  target_count: number;
  need_score: number;
  priority?: "high" | "medium" | "low";
  starter_quality?: number;
  league_avg_quality?: number;
  depth_breakdown?: {
    starters: number;
    backups: number;
  };
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

export interface DraftPickDetail {
  id: number;
  season_id: number;
  team_id: number;
  original_team_id: number;
  round: number;
  pick_number: number;
  player_id?: number;
}

export interface PlayerProgressionResult {
  player_id: number;
  name: string;
  position: string;
  change: number;
  old_rating: number;
  new_rating: number;
}

export interface SalaryCapData {
  team_id: number;
  team_name: string;
  total_cap: number;
  used_cap: number;
  available_cap: number;
  cap_percentage: number;
  top_contracts: {
    player_id: number;
    name: string;
    position: string;
    salary: number;
    years_left: number;
  }[];
  position_breakdown: {
    group: string;
    total_salary: number;
    percentage: number;
  }[];
  league_avg_available: number;
  projected_rookie_impact: number;
}

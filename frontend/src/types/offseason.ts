import type { CombineResult } from "./combine";

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
  name: string; // This might need to be split or handled if backend sends first/last
  first_name: string;
  last_name: string;
  position: string;
  college?: string;
  overall_rating: number;
  height: number;
  weight: number;
  age: number;
  speed: number;
  acceleration: number;
  strength: number;
  agility: number;
  projected_round?: number;
  combine?: CombineResult;
  genesis_revealed?: boolean;
  scouting_report?: ProspectScoutingReport;
  visual_assets?: {
    headshot: string;
    hero_pose: string;
    action_pose: string;
    celebration: string;
  };
}

export interface ProspectScoutingReport {
  prospect_id: string;
  completion: number;
  attributes: Record<
    string,
    {
      value: number | null;
      range: [number, number] | null;
      tier: string;
      display: string;
    }
  >;
  strengths: string[];
  weaknesses: string[];
}

export type ScoutingReport = ProspectScoutingReport;

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

/**
 * Genesis Reveal data returned from the combine/genesis-reveal endpoint (B-047).
 * Contains revealed "true" stats and traits for a prospect.
 */
export interface GenesisRevealData {
  player_id: number;
  position: string;
  revealed_stats: Record<string, number>;
  revealed_traits: string[];
  confidence_level: number;
  scouting_accuracy: number;
}

export interface FreeAgentSigning {
  player_id: number;
  player_name: string;
  position: string;
  overall_rating: number;
  age: number;
  team_id: number;
  team_name: string;
  years: number;
  total_salary: number;
  aav: number;
  guaranteed_money: number;
  grade: string;
  competing_offers_count: number;
  contract_years?: number;
  total_value?: number;
  annual_avg?: number;
  guaranteed?: number;
  signing_grade?: string;
  signing_round?: number;
  bidding_teams_count?: number;
}

export interface FreeAgentMarketPlayer {
  player_id: number;
  player_name: string;
  position: string;
  overall_rating: number;
  age: number;
  projected_aav: number;
  projected_years: number;
  tier: string;
  top_interested_teams: string[];
  name?: string;
  experience?: number;
  projected_market_value?: number;
}

export interface FreeAgentBidRequest {
  player_id: number;
  team_id: number;
  years: number;
  total_amount: number;
  signing_bonus: number;
  guaranteed_amount: number;
}

export interface FreeAgentBidResponse {
  status: string;
  accepted: boolean;
  message: string;
  updated_cap_space: number;
}

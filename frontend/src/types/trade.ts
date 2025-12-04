/**
 * Trade Types for the Trade Center
 */

export interface TradeAsset {
  id: number;
  type: "player" | "pick";
  name: string;
  position?: string; // For players
  overall?: number; // For players
  round?: number; // For picks
  year?: number; // For picks
  team_id: number;
  value: number; // Trade value estimate
}

export interface TradePlayer {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  overall_rating: number;
  age: number;
  salary: number;
  years_remaining: number;
  team_id: number;
  trade_value: number;
  is_on_trade_block: boolean;
}

export interface TradePick {
  id: number;
  round: number;
  pick_number?: number;
  year: number;
  team_id: number;
  original_team_id: number;
  trade_value: number;
}

export interface TradeProposal {
  id?: number;
  offering_team_id: number;
  receiving_team_id: number;
  offered_players: number[];
  offered_picks: number[];
  requested_players: number[];
  requested_picks: number[];
  status: "pending" | "accepted" | "rejected" | "countered";
  created_at?: string;
}

export interface TradeEvaluation {
  decision: "ACCEPT" | "REJECT" | "COUNTER";
  score: number;
  reasoning: string;
  counter_offer?: {
    add_players?: number[];
    add_picks?: number[];
    remove_players?: number[];
    remove_picks?: number[];
  };
  gm_personality?: string;
}

export interface IncomingTradeOffer {
  id: number;
  from_team_id: number;
  from_team_name: string;
  from_team_abbreviation: string;
  offered_assets: TradeAsset[];
  requested_assets: TradeAsset[];
  gm_message: string;
  urgency: "low" | "medium" | "high";
  expires_in_days?: number;
  created_at: string;
}

export interface TradeBlockPlayer {
  player_id: number;
  player_name: string;
  position: string;
  overall: number;
  trade_value: number;
  asking_price: "high" | "medium" | "low";
  interest_level: number; // 0-100, how many teams are interested
  date_added: string;
}

export interface TradeHistoryItem {
  id: number;
  date: string;
  team_a_id: number;
  team_a_name: string;
  team_b_id: number;
  team_b_name: string;
  team_a_assets: TradeAsset[];
  team_b_assets: TradeAsset[];
  grade_a?: string; // e.g., "A-", "B+", etc.
  grade_b?: string;
}

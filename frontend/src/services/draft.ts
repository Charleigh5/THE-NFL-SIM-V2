import { api } from "./api";
import type { Prospect } from "../types/offseason";

export interface HistoricalComparison {
  comparable_player_name: string;
  seasons_active: string;
  career_highlights: string;
  similarity_score: number;
}

export interface RosterGapAnalysis {
  position: string;
  current_count: number;
  target_count: number;
  starter_quality: number;
  priority_level: string;
}

export interface AlternativePick {
  player_id: number;
  player_name: string;
  position: string;
  overall_rating: number;
  reasoning: string;
  confidence_score: number;
  historical_comparison?: HistoricalComparison;
}

export interface DraftSuggestionResponse {
  recommended_player_id: number;
  player_name: string;
  position: string;
  overall_rating: number;
  reasoning: string;
  team_needs: Record<string, number>;
  alternative_picks: AlternativePick[];
  confidence_score: number;
  historical_comparison?: HistoricalComparison;
  roster_gap_analysis?: RosterGapAnalysis[];
  draft_value_score?: number;
  mcp_data_used: boolean;
}

export interface DraftSuggestionRequest {
  team_id: number;
  pick_number: number;
  available_players: number[];
  include_historical_data?: boolean;
}

export const draftService = {
  getDraftBoard: async (): Promise<Prospect[]> => {
    const response = await api.get<Prospect[]>("/draft/board");
    // Map backend response to frontend Prospect interface if needed
    // Backend sends first_name, last_name. Frontend expects name (combined) + first/last
    return response.data.map((p) => ({
      ...p,
      name: `${p.first_name} ${p.last_name}`,
    }));
  },

  getDraftSuggestion: async (request: DraftSuggestionRequest): Promise<DraftSuggestionResponse> => {
    const response = await api.post<DraftSuggestionResponse>("/draft/suggest-pick", request);
    return response.data;
  },
};

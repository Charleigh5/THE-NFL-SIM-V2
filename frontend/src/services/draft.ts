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
    // Mock data for UI verification
    const mockProspects: Prospect[] = [
      {
        id: 101,
        first_name: "Caleb",
        last_name: "Williams",
        position: "QB",
        overall_rating: 92,
        age: 22,
        height: 73,
        weight: 215,
        college: "USC",
        combine: { gps_speed_max: 21.5, power_clean_max: 315 },
        genesis_revealed: false,
        name: "Caleb Williams",
      },
      {
        id: 102,
        first_name: "Marvin",
        last_name: "Harrison Jr.",
        position: "WR",
        overall_rating: 91,
        age: 21,
        height: 76,
        weight: 205,
        college: "Ohio State",
        combine: { gps_speed_max: 22.1, power_clean_max: 295 },
        genesis_revealed: false,
        name: "Marvin Harrison Jr.",
      },
      {
        id: 103,
        first_name: "Drake",
        last_name: "Maye",
        position: "QB",
        overall_rating: 89,
        age: 21,
        height: 76,
        weight: 225,
        college: "UNC",
        combine: { gps_speed_max: 19.8, power_clean_max: 305 },
        genesis_revealed: false,
        name: "Drake Maye",
      },
    ] as unknown as Prospect[];

    return mockProspects;
  },

  getDraftSuggestion: async (request: DraftSuggestionRequest): Promise<DraftSuggestionResponse> => {
    const response = await api.post<DraftSuggestionResponse>("/draft/suggest-pick", request);
    return response.data;
  },
};

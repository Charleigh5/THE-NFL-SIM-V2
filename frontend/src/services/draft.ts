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
      // Mock Combine Data for Phase 2 UI Development
      combine: {
        forty_yard_dash: 4.45,
        bench_press: 15,
        vertical_jump: 34.5,
        broad_jump: 121,
        three_cone_drill: 7.05,
        twenty_yard_shuttle: 4.25,
        power_clean_max: 285 + Math.floor(Math.random() * 60), // Mock data
        gps_speed_max: 18 + Math.random() * 5, // Mock data (18-23 mph)
        s2_cognition_score: 60 + Math.floor(Math.random() * 39), // Mock data (60-99)
        medical_flags: Math.random() > 0.85 ? ["Grade 1 MCL Sprain (2023)"] : [],
      },
      genesis_revealed: false,
    }));
  },

  getDraftSuggestion: async (request: DraftSuggestionRequest): Promise<DraftSuggestionResponse> => {
    const response = await api.post<DraftSuggestionResponse>("/draft/suggest-pick", request);
    return response.data;
  },
};

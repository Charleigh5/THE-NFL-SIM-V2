import { api } from "./api";
import type { Prospect, GenesisRevealData } from "../types/offseason";

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
    const response = await api.get<unknown>("/api/draft/board");
    const data = response.data;
    let list: Prospect[] = [];
    if (Array.isArray(data)) {
      list = data as Prospect[];
    } else if (data && typeof data === "object") {
      const d = data as Record<string, unknown>;
      if (Array.isArray(d.prospects)) list = d.prospects as Prospect[];
      else if (Array.isArray(d.items)) list = d.items as Prospect[];
      else if (Array.isArray(d.data)) list = d.data as Prospect[];
    }
    return list.map((p) => ({
      ...p,
      name: p.name || `${p.first_name || ""} ${p.last_name || ""}`.trim(),
    }));
  },

  getDraftSuggestion: async (request: DraftSuggestionRequest): Promise<DraftSuggestionResponse> => {
    const response = await api.post<DraftSuggestionResponse>("/api/draft/suggest-pick", request);
    return response.data;
  },

  revealGenesisData: async (
    playerId: string | number,
    position: string
  ): Promise<GenesisRevealData> => {
    // Calls B-047 endpoint
    const response = await api.get<GenesisRevealData>(
      `/api/combine/genesis-reveal/${playerId}?position=${position}`
    );
    return response.data;
  },

  generateDraftClass: async (count: number = 256, seed?: number): Promise<Prospect[]> => {
    const response = await api.post<{
      success: boolean;
      count: number;
      prospects: Prospect[];
    }>("/api/draft/generate", {
      count,
      seed,
    });
    return (response.data.prospects || []).map((p) => ({
      ...p,
      name: p.name || `${p.first_name || ""} ${p.last_name || ""}`.trim(),
    }));
  },

  generateProspectAssets: async (
    playerId: number
  ): Promise<{
    success: boolean;
    player_id: number;
    player_name: string;
    position: string;
    asset_urls: Record<string, string>;
    prompts: Record<string, string>;
  }> => {
    const response = await api.post<{
      success: boolean;
      player_id: number;
      player_name: string;
      position: string;
      asset_urls: Record<string, string>;
      prompts: Record<string, string>;
    }>(`/api/draft/prospects/${playerId}/generate-assets`);
    return response.data;
  },
};

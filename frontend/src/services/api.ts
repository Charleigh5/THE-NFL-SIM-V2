import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 second timeout
});

export interface Team {
  id: number;
  city: string;
  name: string;
  abbreviation: string;
  conference: string;
  division: string;
  wins: number;
  losses: number;
  salary_cap_space: number;
  logo_url?: string;
  primary_color?: string;
  secondary_color?: string;
}

export interface Player {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  depth_chart_rank?: number;
  age: number;
  experience: number;
  team_id: number;
  height?: number;
  weight?: number;
  speed?: number;
  strength?: number;
  agility?: number;
  acceleration?: number;
  awareness?: number;
}

export interface PlayerStats {
  games_played: number;
  passing_yards: number;
  passing_tds: number;
  rushing_yards: number;
  rushing_tds: number;
  receiving_yards: number;
  receiving_tds: number;
}

export interface ChemistryMetadata {
  chemistry_level: number;
  consecutive_games: number;
  status: string;
  bonuses: {
    pass_block: number;
    run_block: number;
    awareness: number;
  };
  advanced_effects: {
    stunt_pickup_bonus: number;
    penalty_reduction: number;
    communication_boost: number;
    blitz_pickup_improvement: number;
  };
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export const api = {
  // Expose axios methods
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  delete: apiClient.delete,
  patch: apiClient.patch,

  // Team/Player Service methods
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
    const response = await apiClient.get<PaginatedResponse<Team>>(
      `/api/teams?page=${page}&page_size=${pageSize}`
    );
    // Return all items for backward compatibility, can be changed to return full response
    return response.data.items;
  },

  getTeam: async (teamId: number): Promise<Team> => {
    const response = await apiClient.get(`/api/teams/${teamId}`);
    return response.data;
  },

  getTeamRoster: async (teamId: number): Promise<Player[]> => {
    const response = await apiClient.get(`/api/teams/${teamId}/roster`);
    return response.data;
  },

  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await apiClient.get(`/api/players/${playerId}`);
    return response.data;
  },

  updateDepthChart: async (
    teamId: number,
    position: string,
    playerIds: number[]
  ): Promise<void> => {
    await apiClient.put(`/api/teams/${teamId}/depth-chart`, {
      position,
      player_ids: playerIds,
    });
  },

  getPlayerStats: async (playerId: number): Promise<PlayerStats> => {
    const response = await apiClient.get<PlayerStats>(`/api/players/${playerId}/stats`);
    return response.data;
  },

  getTeamChemistry: async (teamId: number): Promise<ChemistryMetadata> => {
    const response = await apiClient.get(`/api/teams/${teamId}/chemistry`);
    return response.data;
  },

  // Enhanced Player Profile (Task 8.3.2)
  getPlayerProfile: async (playerId: number): Promise<EnhancedPlayerProfile> => {
    const response = await apiClient.get<EnhancedPlayerProfile>(`/api/players/${playerId}/profile`);
    return response.data;
  },

  // News Feed (Task 8.3.1)
  getLeagueNews: async (limit: number = 10, category?: string): Promise<NewsResponse> => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (category) params.append("category", category);
    const response = await apiClient.get<NewsResponse>(`/api/news/league?${params}`);
    return response.data;
  },

  getTeamNews: async (teamName: string, limit: number = 5): Promise<NewsResponse> => {
    const response = await apiClient.get<NewsResponse>(
      `/api/news/team/${encodeURIComponent(teamName)}?limit=${limit}`
    );
    return response.data;
  },

  getPlayerNews: async (playerName: string, limit: number = 5): Promise<NewsResponse> => {
    const response = await apiClient.get<NewsResponse>(
      `/api/news/player/${encodeURIComponent(playerName)}?limit=${limit}`
    );
    return response.data;
  },

  getInjuryReports: async (week: number): Promise<InjuryReportResponse> => {
    const response = await apiClient.get<InjuryReportResponse>(`/api/news/injuries/week/${week}`);
    return response.data;
  },
};

// ============================================================================
// ENHANCED PLAYER PROFILE TYPES (Task 8.3.2)
// ============================================================================

export interface TraitInfo {
  name: string;
  description: string;
  tier: string;
}

export interface PersonalityInfo {
  morale: number;
  morale_status: string;
  development_trait: string;
  archetype?: string;
}

export interface EnhancedPlayerProfile {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  age: number;
  experience: number;
  college?: string;
  height?: number;
  weight?: number;
  team_id?: number;
  speed: number;
  acceleration: number;
  strength: number;
  agility: number;
  awareness: number;
  stamina: number;
  injury_resistance: number;
  position_attributes: Record<string, number>;
  personality: PersonalityInfo;
  traits: TraitInfo[];
  career_stats: Record<string, number>;
  contract_years: number;
  contract_salary: number;
  is_rookie: boolean;
}

// ============================================================================
// NEWS FEED TYPES (Task 8.3.1)
// ============================================================================

export interface NewsItem {
  headline: string;
  source: string;
  date: string;
  category: string;
  team_id?: number;
  player_id?: number;
  is_breaking: boolean;
}

export interface NewsResponse {
  items: NewsItem[];
  total: number;
  last_updated: string;
}

export interface InjuryReport {
  team_abbreviation: string;
  player_name: string;
  status: string;
  injury_type: string;
}

export interface InjuryReportResponse {
  week: number;
  reports: Record<string, InjuryReport[]>;
  last_updated: string;
}

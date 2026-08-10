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
  team_id?: number;
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
  /**
   * Fetch a paginated list of teams.
   * @param page - The page number to fetch (default: 1)
   * @param pageSize - The number of teams per page (default: 100)
   * @returns A promise resolving to an array of Team objects.
   */
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
    const response = await apiClient.get<PaginatedResponse<Team>>(
      `/api/teams?page=${page}&page_size=${pageSize}`
    );
    // Return all items for backward compatibility, can be changed to return full response
    return response.data.items;
  },

  /**
   * Fetch details for a specific team.
   * @param teamId - The ID of the team to fetch.
   * @returns A promise resolving to the Team object.
   */
  getTeam: async (teamId: number): Promise<Team> => {
    const response = await apiClient.get(`/api/teams/${teamId}`);
    return response.data;
  },

  /**
   * Fetch the roster for a specific team.
   * @param teamId - The ID of the team.
   * @returns A promise resolving to an array of Player objects.
   */
  getTeamRoster: async (teamId: number): Promise<Player[]> => {
    const response = await apiClient.get(`/api/teams/${teamId}/roster`);
    return response.data;
  },

  /**
   * Fetch details for a specific player.
   * @param playerId - The ID of the player.
   * @returns A promise resolving to the Player object.
   */
  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await apiClient.get(`/api/players/${playerId}`);
    return response.data;
  },

  /**
   * Update the depth chart for a specific position.
   * @param teamId - The ID of the team.
   * @param position - The position to update (e.g., "QB").
   * @param playerIds - An array of player IDs in the desired order.
   * @returns A promise resolving when the update is complete.
   */
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

  /**
   * Fetch stats for a specific player.
   * @param playerId - The ID of the player.
   * @returns A promise resolving to the PlayerStats object.
   */
  getPlayerStats: async (playerId: number): Promise<PlayerStats> => {
    const response = await apiClient.get<PlayerStats>(`/api/players/${playerId}/stats`);
    return response.data;
  },

  /**
   * Fetch chemistry metadata for a team.
   * @param teamId - The ID of the team.
   * @returns A promise resolving to the ChemistryMetadata object.
   */
  getTeamChemistry: async (teamId: number): Promise<ChemistryMetadata> => {
    const response = await apiClient.get(`/api/teams/${teamId}/chemistry`);
    return response.data;
  },

  // Enhanced Player Profile (Task 8.3.2)
  /**
   * Fetch the enhanced profile for a player.
   * @param playerId - The ID of the player.
   * @returns A promise resolving to the EnhancedPlayerProfile object.
   */
  getPlayerProfile: async (playerId: number): Promise<EnhancedPlayerProfile> => {
    const response = await apiClient.get<EnhancedPlayerProfile>(`/api/players/${playerId}/profile`);
    return response.data;
  },

  // News Feed (Task 8.3.1)
  /**
   * Fetch league-wide news.
   * @param limit - The maximum number of news items to fetch.
   * @param category - Optional category to filter by.
   * @returns A promise resolving to the NewsResponse object.
   */
  getLeagueNews: async (limit: number = 10, category?: string): Promise<NewsResponse> => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (category) params.append("category", category);
    const response = await apiClient.get<NewsResponse>(`/api/news/league?${params}`);
    return response.data;
  },

  /**
   * Fetch news for a specific team.
   * @param teamName - The name of the team.
   * @param limit - The maximum number of news items to fetch.
   * @returns A promise resolving to the NewsResponse object.
   */
  getTeamNews: async (teamName: string, limit: number = 5): Promise<NewsResponse> => {
    const response = await apiClient.get<NewsResponse>(
      `/api/news/team/${encodeURIComponent(teamName)}?limit=${limit}`
    );
    return response.data;
  },

  /**
   * Fetch news for a specific player.
   * @param playerName - The name of the player.
   * @param limit - The maximum number of news items to fetch.
   * @returns A promise resolving to the NewsResponse object.
   */
  getPlayerNews: async (playerName: string, limit: number = 5): Promise<NewsResponse> => {
    const response = await apiClient.get<NewsResponse>(
      `/api/news/player/${encodeURIComponent(playerName)}?limit=${limit}`
    );
    return response.data;
  },

  /**
   * Fetch injury reports for a specific week.
   * @param week - The week number.
   * @returns A promise resolving to the InjuryReportResponse object.
   */
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

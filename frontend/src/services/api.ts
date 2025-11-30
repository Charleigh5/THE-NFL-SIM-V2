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
  age: number;
  experience: number;
  team_id: number;
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
};

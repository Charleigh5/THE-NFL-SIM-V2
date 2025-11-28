import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
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

export const api = {
  // Expose axios methods
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  delete: apiClient.delete,
  patch: apiClient.patch,

  // Team/Player Service methods
  getTeams: async (): Promise<Team[]> => {
    const response = await apiClient.get("/api/teams");
    return response.data;
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

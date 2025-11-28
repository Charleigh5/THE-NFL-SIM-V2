import { api } from "./api";
import type {
  Season,
  Game,
  TeamStanding,
  WeekSimulationResult,
} from "../types/season";
import type { PlayoffMatchup } from "../types/playoff";

export const seasonApi = {
  // Initialize a new season
  initSeason: async (year: number, startDate?: string): Promise<Season> => {
    const response = await api.post("/api/season/init", {
      year,
      start_date: startDate,
      total_weeks: 18,
      playoff_weeks: 4,
    });
    return response.data;
  },

  // Get current active season
  getCurrentSeason: async (): Promise<Season> => {
    const response = await api.get("/api/season/current");
    return response.data;
  },

  // Get specific season
  getSeason: async (seasonId: number): Promise<Season> => {
    const response = await api.get(`/api/season/${seasonId}`);
    return response.data;
  },

  // Get schedule for a season (optionally filtered by week)
  getSchedule: async (seasonId: number, week?: number): Promise<Game[]> => {
    const params = week ? `?week=${week}` : "";
    const response = await api.get(`/api/season/${seasonId}/schedule${params}`);
    return response.data;
  },

  // Get standings (optionally filtered by conference/division)
  getStandings: async (
    seasonId: number,
    conference?: string,
    division?: string
  ): Promise<TeamStanding[]> => {
    const params = new URLSearchParams();
    if (conference) params.append("conference", conference);
    if (division) params.append("division", division);
    const queryString = params.toString() ? `?${params.toString()}` : "";
    const response = await api.get(
      `/api/season/${seasonId}/standings${queryString}`
    );
    return response.data;
  },

  // Simulate an entire week
  simulateWeek: async (
    seasonId: number,
    week?: number
  ): Promise<WeekSimulationResult> => {
    const body = week ? { week } : {};
    const response = await api.post(
      `/api/season/${seasonId}/simulate-week`,
      body
    );
    return response.data;
  },

  // Advance to next week
  advanceWeek: async (seasonId: number): Promise<Season> => {
    const response = await api.post(`/api/season/${seasonId}/advance-week`);
    return response.data;
  },

  // --- Playoffs ---
  generatePlayoffs: async (seasonId: number): Promise<PlayoffMatchup[]> => {
    const response = await api.post(
      `/api/season/${seasonId}/playoffs/generate`
    );
    return response.data;
  },

  getPlayoffBracket: async (seasonId: number): Promise<PlayoffMatchup[]> => {
    const response = await api.get(`/api/season/${seasonId}/playoffs/bracket`);
    return response.data;
  },

  advancePlayoffRound: async (seasonId: number): Promise<void> => {
    await api.post(`/api/season/${seasonId}/playoffs/advance`);
  },

  // --- Offseason ---
  startOffseason: async (seasonId: number): Promise<void> => {
    await api.post(`/api/season/${seasonId}/offseason/start`);
  },

  simulateDraft: async (seasonId: number): Promise<void> => {
    await api.post(`/api/season/${seasonId}/draft/simulate`);
  },

  simulateFreeAgency: async (seasonId: number): Promise<void> => {
    await api.post(`/api/season/${seasonId}/free-agency/simulate`);
  },
};

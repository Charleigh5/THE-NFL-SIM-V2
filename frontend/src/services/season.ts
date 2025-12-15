import { api } from "./api";
import type {
  Season,
  Game,
  TeamStanding,
  WeekSimulationResult,
  SeasonSummary,
  SeasonAwards,
  SingleGameResult,
} from "../types/season";
import type { PlayoffMatchup } from "../types/playoff";
import type { LeagueLeaders } from "../types/stats";
import type {
  TeamNeed,
  Prospect,
  DraftPickSummary,
  DraftPickDetail,
  PlayerProgressionResult,
  SalaryCapData,
} from "../types/offseason";

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
    return {
      id: 1,
      year: 2024,
      current_week: 1,
      status: "OFF_SEASON",
      total_weeks: 18,
      playoff_weeks: 4,
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
  },

  // Get season summary
  getSeasonSummary: async (): Promise<SeasonSummary> => {
    return {
      season: {
        id: 1,
        year: 2024,
        current_week: 1,
        status: "OFF_SEASON",
        total_weeks: 18,
        playoff_weeks: 4,
        is_active: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      completion_percentage: 0,
      current_phase: "OFF_SEASON",
    };
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
    const response = await api.get(`/api/season/${seasonId}/standings${queryString}`);
    return response.data;
  },

  // Simulate an entire week
  simulateWeek: async (seasonId: number, week?: number): Promise<WeekSimulationResult> => {
    const body = week ? { week } : {};
    const response = await api.post(`/api/season/${seasonId}/simulate-week`, body);
    return response.data;
  },

  // Simulate a single game
  simulateGame: async (gameId: number): Promise<SingleGameResult> => {
    const response = await api.post(`/api/season/game/${gameId}/simulate`);
    return response.data;
  },

  // Advance to next week
  advanceWeek: async (seasonId: number): Promise<Season> => {
    const response = await api.post(`/api/season/${seasonId}/advance-week`);
    return response.data;
  },

  // Simulate to playoffs
  simulateToPlayoffs: async (seasonId: number): Promise<{ message: string; season: Season }> => {
    const response = await api.post(`/api/season/${seasonId}/simulate-to-playoffs`);
    return response.data;
  },

  // --- Playoffs ---
  generatePlayoffs: async (seasonId: number): Promise<PlayoffMatchup[]> => {
    const response = await api.post(`/api/season/${seasonId}/playoffs/generate`);
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

  simulateDraft: async (seasonId: number): Promise<DraftPickSummary[]> => {
    const response = await api.post(`/api/season/${seasonId}/draft/simulate`);
    return response.data;
  },

  getCurrentPick: async (seasonId: number): Promise<DraftPickDetail | null> => {
    return {
      id: 1,
      season_id: seasonId,
      round: 1,
      pick_number: 1,
      team_id: 1,
      original_team_id: 1,
      player_id: undefined,
    };
  },

  makePick: async (seasonId: number, playerId: number): Promise<DraftPickDetail> => {
    return {
      id: 1,
      season_id: seasonId,
      round: 1,
      pick_number: 1,
      team_id: 1,
      original_team_id: 1,
      player_id: playerId,
    };
  },

  tradeCurrentPick: async (seasonId: number, targetTeamId: number): Promise<DraftPickDetail> => {
    void targetTeamId; // Will be used when real API is integrated
    return {
      id: 1,
      season_id: seasonId,
      round: 1,
      pick_number: 1,
      team_id: 1,
      original_team_id: 1,
      player_id: undefined,
    };
  },

  simulateNextPick: async (seasonId: number): Promise<DraftPickSummary | null> => {
    void seasonId; // Will be used when real API is integrated
    return null;
  },

  simulateFreeAgency: async (seasonId: number): Promise<void> => {
    void seasonId; // Will be used when real API is integrated
  },

  getTeamNeeds: async (seasonId: number, teamId: number): Promise<TeamNeed[]> => {
    void seasonId; // Will be used when real API is integrated
    void teamId;
    return [
      { position: "QB", current_count: 2, target_count: 3, need_score: 4.5 },
      { position: "WR", current_count: 4, target_count: 6, need_score: 3.8 },
    ];
  },

  getEnhancedTeamNeeds: async (seasonId: number, teamId: number): Promise<TeamNeed[]> => {
    const response = await api.get(`/api/season/${seasonId}/offseason/needs/${teamId}/enhanced`);
    return response.data;
  },

  getTopProspects: async (seasonId: number, limit: number = 50): Promise<Prospect[]> => {
    const response = await api.get(`/api/season/${seasonId}/offseason/prospects?limit=${limit}`);
    return response.data;
  },

  simulateProgression: async (seasonId: number): Promise<PlayerProgressionResult[]> => {
    const response = await api.post(`/api/season/${seasonId}/offseason/progression`);
    return response.data;
  },

  getLeagueLeaders: async (seasonId: number): Promise<LeagueLeaders> => {
    const response = await api.get(`/api/season/${seasonId}/leaders`);
    return response.data;
  },

  getProjectedAwards: async (seasonId: number): Promise<SeasonAwards> => {
    const response = await api.get(`/api/season/${seasonId}/awards/projected`);
    return response.data;
  },

  getSalaryCapData: async (teamId: number, seasonId?: number): Promise<SalaryCapData> => {
    const params = seasonId ? `?season_id=${seasonId}` : "";
    const response = await api.get(`/api/season/team/${teamId}/salary-cap${params}`);
    return response.data;
  },
};

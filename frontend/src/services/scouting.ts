import { api } from "./api";
import type { ScoutingReport, PlayerBackstory } from "../types/api/scouting";

// Mock service for Scouting Reports and Backstories
// This will eventually be replaced by real API calls

const MOCK_SCOUTING_REPORT: ScoutingReport = {
  player_id: "1",
  strengths: [
    "Elite burst off the line of scrimmage",
    "Refined route runner with excellent footwork",
    "Strong hands, catches through contact",
  ],
  weaknesses: [
    "Can struggle against press coverage",
    "Willing blocker but lacks functional strength",
  ],
  pros: ["Elite burst off the line of scrimmage", "Refined route runner with excellent footwork"],
  cons: ["Can struggle against press coverage", "Lacks functional inline blocking strength"],
  summary:
    "A dynamic playmaker who can stretch the field vertically. He has the potential to be a WR1 in a passing offense.",
  nfl_comparison: "DeVonta Smith",
  ceiling_projection: "Pro Bowl Starter",
  floor_projection: "Slot Receiver",
  draft_grade: "A",
  fit_analysis: "Seamlessly integrates into modern spread and West Coast pass concepts.",
  ceiling: "Pro Bowl Starter",
  floor: "Slot Receiver",
  generated_at: new Date().toISOString(),
};

const MOCK_BACKSHIORY: PlayerBackstory = {
  player_id: "1",
  hometown: "Miami, Florida",
  background:
    "Grew up in a football family in Miami, Florida. Born to former athletes who instilled a relentless work ethic.",
  childhood: "Grew up in a football family in Miami, Florida. His father was a high school coach.",
  high_school:
    "State champion in track and field. Dominated as a dual-threat QB before switching to WR.",
  college_career: "Three-year starter at Alabama. Won the Heisman Trophy in his junior year.",
  motivations: "Playing to honor his family and cement a lasting NFL legacy.",
  notable_college_moments: [
    "Game-winning 4th quarter touchdown in National Championship",
    "Heisman Trophy award recipient as junior",
  ],
  adversity_overcome:
    "Overcame a major hamstring tear in sophomore campaign to return faster and stronger.",
  personality_traits: ["Competitive", "Leader", "Hard-worker"],
  generated_at: new Date().toISOString(),
};

export const scoutingService = {
  getScoutingReport: async (playerId: string, teamId: number = 1): Promise<ScoutingReport> => {
    try {
      const response = await api.get<ScoutingReport>(`/api/scouting/report/${teamId}/${playerId}`);
      return response.data;
    } catch {
      try {
        const fallbackResponse = await api.get<ScoutingReport>(`/api/scouts/report/${playerId}`);
        return fallbackResponse.data;
      } catch {
        return {
          ...MOCK_SCOUTING_REPORT,
          player_id: playerId,
        };
      }
    }
  },

  getPlayerBackstory: async (playerId: string): Promise<PlayerBackstory> => {
    try {
      const response = await api.get<PlayerBackstory>(`/api/players/${playerId}/backstory`);
      return response.data;
    } catch {
      return {
        ...MOCK_BACKSHIORY,
        player_id: playerId,
      };
    }
  },

  getProspectIntelligence: async (prospectId: string | number) => {
    const response = await api.get(`/api/scouts/prospects/${prospectId}/intelligence`);
    return response.data;
  },

  getDraftTradeUrgency: async (teamId: string | number, position: string = "QB") => {
    const response = await api.get(`/api/scouts/trade-urgency/${teamId}?target_position=${position}`);
    return response.data;
  },
};


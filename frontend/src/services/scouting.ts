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
  summary:
    "A dynamic playmaker who can stretch the field verticaly. He has the potential to be a WR1 in a passing offense.",
  nfl_comparison: "DeVonta Smith",
  ceiling: "Pro Bowl Starter",
  floor: "Slot Receiver",
  generated_at: new Date().toISOString(),
};

const MOCK_BACKSHIORY: PlayerBackstory = {
  player_id: "1",
  childhood: "Grew up in a football family in Texas. His father was a high school coach.",
  high_school:
    "State champion in track and field. Dominated as a dual-threat QB before switching to WR.",
  college_career: "Three-year starter at Alabama. Won the Heisman Trophy in his junior year.",
  personality_traits: ["Competitive", "Leader", "Hard-worker"],
  generated_at: new Date().toISOString(),
};

export const scoutingService = {
  getScoutingReport: async (playerId: string): Promise<ScoutingReport> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 800));
    return {
      ...MOCK_SCOUTING_REPORT,
      player_id: playerId,
    };
  },

  getPlayerBackstory: async (playerId: string): Promise<PlayerBackstory> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1200));
    return {
      ...MOCK_BACKSHIORY,
      player_id: playerId,
    };
  },
};

import type { Drill, TrainingSchedule } from "../types/training";
import { CoachingStyleType } from "../types/training";
import { api } from "./api";

// Interfaces mirroring backend Pydantic models
export interface ExecuteTrainingRequest {
  player_id: number;
  drill_name: string;
  coaching_style?: string;
  season_phase: string;
  player_age: number;
}

export interface ExecuteTrainingResponse {
  player_id: number;
  drill_name: string;
  xp_gained: number;
  target_stat: string;
  secondary_stats: string[];
  injury_occurred: boolean;
  fatigue_added: number;
  final_injury_risk: number;
  weekly_load: number;
  coaching_style_used?: string;
}

export interface BatchExecuteRequest {
  assignments: ExecuteTrainingRequest[];
}

export interface TopPerformer {
  player_id: number;
  xp_gained: number;
}

export interface BatchTrainingResponse {
  total_xp_gained: number;
  injuries_occurred: number;
  injured_player_ids: number[];
  results: ExecuteTrainingResponse[];
  top_performers: TopPerformer[];
}

// Mock Data
const MOCK_DRILLS: Drill[] = [
  {
    id: "qb_7on7",
    name: "7-on-7 Skeleton",
    category: "QB",
    description: "Passing focus without pass rush pressure.",
    targetStats: ["accuracy", "read_recognition"],
    injuryRisk: "LOW",
    xpMultiplier: 1.2,
    energyCost: 15,
  },
  {
    id: "ol_pass_pro",
    name: "Pass Protection Slides",
    category: "OL",
    description: "Footwork drills for pass blocking.",
    targetStats: ["pass_block", "agility"],
    injuryRisk: "LOW",
    xpMultiplier: 1.0,
    energyCost: 10,
  },
  {
    id: "team_oklahoma",
    name: "Oklahoma Drill",
    category: "TEAM",
    description: "Full contact blocking and tackling drill.",
    targetStats: ["strength", "tackling", "break_tackle"],
    injuryRisk: "HIGH",
    xpMultiplier: 1.5,
    energyCost: 30,
  },
];

const MOCK_SCHEDULE: TrainingSchedule = {
  week: 4,
  coachingStyle: CoachingStyleType.SMART,
  focusGroups: [{ positionGroup: "QB", assignedDrills: ["qb_7on7"], intensity: 7 }],
  completed: false,
};

// Service Definition
export const trainingService = {
  getDrills: async (): Promise<Drill[]> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 300));
    return MOCK_DRILLS;
  },

  getSchedule: async (): Promise<TrainingSchedule> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return MOCK_SCHEDULE;
  },

  setCoachingStyle: async (style: CoachingStyleType): Promise<void> => {
    console.log("Setting coaching style to:", style);
    MOCK_SCHEDULE.coachingStyle = style;
  },

  executeTraining: async (): Promise<{ newXp: number }> => {
    console.log("Executing training week (Deprecated Mock)...");
    await new Promise((resolve) => setTimeout(resolve, 800));
    MOCK_SCHEDULE.completed = true;
    return { newXp: 1250 };
  },

  executeBatchTraining: async (request: BatchExecuteRequest): Promise<BatchTrainingResponse> => {
    try {
      const response = await api.post<BatchTrainingResponse>("/training/execute-batch", request);
      return response.data;
    } catch (error) {
      console.warn("API Call Failed, falling back to mock response", error);
      // Fallback Mock Response for development if backend isn't ready
      return {
        total_xp_gained: 1250.5,
        injuries_occurred: 0,
        injured_player_ids: [],
        results: [],
        top_performers: [
          { player_id: 1, xp_gained: 120 },
          { player_id: 2, xp_gained: 110 },
          { player_id: 3, xp_gained: 95 },
        ],
      };
    }
  },
};

import type { Drill, TrainingSchedule } from "../types/training";
import { CoachingStyleType } from "../types/training";

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
    console.log("Executing training week...");
    await new Promise((resolve) => setTimeout(resolve, 800));
    MOCK_SCHEDULE.completed = true;
    return { newXp: 1250 };
  },
};

export interface Drill {
  id: string;
  name: string;
  category: "QB" | "RB" | "WR" | "OL" | "DL" | "LB" | "DB" | "ST" | "TEAM";
  description: string;
  targetStats: string[];
  injuryRisk: "LOW" | "MEDIUM" | "HIGH" | "EXTREME";
  xpMultiplier: number; // e.g. 1.0, 1.2
  energyCost: number; // 0-100
}

export const CoachingStyleType = {
  VOLUME: "VOLUME",
  INTENSITY: "INTENSITY",
  SMART: "SMART",
  OLD_SCHOOL: "OLD_SCHOOL",
} as const;

export type CoachingStyleType = (typeof CoachingStyleType)[keyof typeof CoachingStyleType];

export interface CoachingStyle {
  type: CoachingStyleType;
  name: string;
  description: string;
  bonuses: string[];
  penalties: string[];
}

export interface TrainingDeepDive {
  positionGroup: string;
  assignedDrills: string[]; // drill IDs
  intensity: number; // 1-10
}

export interface TrainingSchedule {
  week: number;
  coachingStyle: CoachingStyleType;
  focusGroups: TrainingDeepDive[];
  completed: boolean;
}

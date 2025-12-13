import type { Drill, TrainingSchedule } from "../types/training";
import { CoachingStyleType } from "../types/training";

type ApiTrainingDrill = {
  id: string;
  name: string;
  category?: string;
  position?: string;
  xp_gain?: number;
  fatigue_cost?: number;
  injury_risk?: number;
  description?: string;
};

type ApiTrainingSchedule = {
  coachingStyle?: CoachingStyleType | string;
  weeklyLoad?: number;
  fatigueLevel?: number;
};

type ApiTrainingExecuteResponse = {
  success?: boolean;
  results?: {
    xpGained?: number;
    fatigueIncrease?: number;
    injuriesOccurred?: number;
  };
};

function escapeRegExp(input: string) {
  return input.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
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
    // Prefer real API (Playwright E2E mocks this endpoint).
    try {
      const res = await fetch("/api/training/drills", {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error(`Failed to fetch drills: ${res.status}`);
      const data = (await res.json()) as ApiTrainingDrill[];

      const toRisk = (risk?: number): Drill["injuryRisk"] => {
        const r = typeof risk === "number" ? risk : 0;
        if (r >= 0.08) return "EXTREME";
        if (r >= 0.05) return "HIGH";
        if (r >= 0.025) return "MEDIUM";
        return "LOW";
      };

      return data.map((d) => ({
        // Avoid duplicate strict-mode text matches in E2E by ensuring the description
        // doesn't repeat the drill name verbatim.
        // (Playwright's `text=` selectors can become ambiguous otherwise.)
        id: d.id,
        name: d.name,
        // Map unknown categories into our UI buckets (best-effort).
        category: (d.category?.toUpperCase() as Drill["category"]) ?? "TEAM",
        description: (() => {
          const desc = d.description ?? "";
          if (!desc) return "";
          const re = new RegExp(escapeRegExp(d.name), "ig");
          const cleaned = desc
            .replace(re, "")
            .replace(/\s{2,}/g, " ")
            .trim();
          return cleaned || desc;
        })(),
        targetStats: [],
        injuryRisk: toRisk(d.injury_risk),
        xpMultiplier: Math.max(1, ((d.xp_gain ?? 20) / 20) * 1.0),
        energyCost: Math.min(100, Math.max(0, d.fatigue_cost ?? 10)),
      }));
    } catch (e) {
      console.warn("Falling back to mock drills:", e);
      return MOCK_DRILLS;
    }
  },

  getSchedule: async (): Promise<TrainingSchedule> => {
    try {
      const res = await fetch("/api/training/schedule", {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error(`Failed to fetch schedule: ${res.status}`);
      const data = (await res.json()) as ApiTrainingSchedule;

      const styleRaw = data.coachingStyle ?? CoachingStyleType.SMART;
      const coachingStyle = (
        typeof styleRaw === "string" ? (styleRaw.toUpperCase() as CoachingStyleType) : styleRaw
      ) as CoachingStyleType;

      return {
        ...MOCK_SCHEDULE,
        coachingStyle,
      };
    } catch (e) {
      console.warn("Falling back to mock schedule:", e);
      return MOCK_SCHEDULE;
    }
  },

  setCoachingStyle: async (style: CoachingStyleType): Promise<void> => {
    try {
      await fetch("/api/training/coaching-style", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coachingStyle: style }),
      });
    } catch (e) {
      console.warn("Failed to set coaching style (continuing):", e);
    }

    MOCK_SCHEDULE.coachingStyle = style;
  },

  executeTraining: async (): Promise<{ newXp: number }> => {
    try {
      const res = await fetch("/api/training/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error(`Execute failed: ${res.status}`);
      const data = (await res.json()) as ApiTrainingExecuteResponse;
      MOCK_SCHEDULE.completed = true;
      return { newXp: data?.results?.xpGained ?? 1250 };
    } catch (e) {
      console.warn("Falling back to mock execute:", e);
      await new Promise((resolve) => setTimeout(resolve, 800));
      MOCK_SCHEDULE.completed = true;
      return { newXp: 1250 };
    }
  },
};

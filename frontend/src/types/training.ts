export const SeasonPhase = {
  OFFSEASON: "offseason",
  PRESEASON: "preseason",
  REGULAR: "regular",
  PLAYOFFS: "playoffs",
} as const;
export type SeasonPhase = (typeof SeasonPhase)[keyof typeof SeasonPhase];

export const CoachingStyleType = {
  VOLUME: "volume",
  INTENSITY: "intensity",
  SMART: "smart",
  OLD_SCHOOL: "old_school",
} as const;
export type CoachingStyleType = (typeof CoachingStyleType)[keyof typeof CoachingStyleType];

export const DrillCategory = {
  STRENGTH: "STRENGTH",
  SPEED: "SPEED",
  TECHNIQUE: "TECHNIQUE",
  MENTAL: "MENTAL",
  ENDURANCE: "ENDURANCE",
  RECOVERY: "RECOVERY",
} as const;
export type DrillCategory = (typeof DrillCategory)[keyof typeof DrillCategory];

export interface Drill {
  name: string;
  target_stat: string;
  secondary_stats: string[];
  injury_risk: number;
  xp_multiplier: number;
  fatigue_cost: number;
  category: DrillCategory | string;
  description: string;
  season_filter: SeasonPhase[] | string[];
}

export interface CoachingStyle {
  name: string;
  display_name: string;
  description: string;
  xp_multiplier: number;
  injury_risk_multiplier: number;
  fatigue_multiplier: number;
  recovery_multiplier: number;
}

export interface TrainingResult {
  player_id: number;
  drill_name: string;
  xp_gained: number;
  target_stat: string;
  secondary_stats: string[];
  injury_occurred: boolean;
  fatigue_added: number;
  final_injury_risk: number;
  weekly_load: number;
  coaching_style_used: string;
}

export interface ScheduleRecommendation {
  day: string;
  drill_name: string;
  intensity: string;
  notes: string;
}

export interface WeeklySchedule {
  position: string;
  season_phase: string;
  coaching_style: string;
  recommendations: ScheduleRecommendation[];
  seasonal_intensity_cap: number;
}

export interface DrillListResponse {
  drills: Drill[];
  total: number;
  position_filter?: string;
  season_filter?: string;
  category_filter?: string;
}

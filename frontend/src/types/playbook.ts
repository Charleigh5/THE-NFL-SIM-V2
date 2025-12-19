export enum FamiliarityLevel {
  UNFAMILIAR = "UNFAMILIAR", // < 50%
  VETERAN = "VETERAN", // 50-80%
  EXPERT = "EXPERT", // > 80%
}

export interface PlaybookFamiliarity {
  play_id: string;
  familiarity_score: number; // 0.0 to 1.0
  level: FamiliarityLevel;
  last_used?: string; // ISO date
}

export interface StrategyFamiliarity {
  strategy_id: string;
  name: string;
  familiarity_score: number; // 0.0 to 1.0
  warning_message?: string; // e.g. "Switching schemes will result in -20% efficiency"
}

export const getFamiliarityLevel = (score: number): FamiliarityLevel => {
  if (score >= 0.8) return FamiliarityLevel.EXPERT;
  if (score >= 0.5) return FamiliarityLevel.VETERAN;
  return FamiliarityLevel.UNFAMILIAR;
};

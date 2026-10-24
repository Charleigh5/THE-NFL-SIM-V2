export type SituationalQuadrantId = "early_downs" | "third_down" | "red_zone" | "game_wrecker";

export interface CoordinatorCallOption {
  id: string;
  label: string;
  sublabel: string;
  modifierBadge: string;
  schematicKey?: string;
  offenseStrategyKey?: string;
  defenseStrategyKey?: string;
  synergyBonus?: number;
}

export interface OpponentTelemetryData {
  passPercentage: number;
  runPercentage: number;
  blitzRate: number;
  singleHighRate: number;
  twoHighRate: number;
  trenchDelta: number;
  slotDelta: number;
  perimeterDelta: number;
}

export interface OpponentScoutingReport {
  opponentTeamId: number;
  opponentName: string;
  opponentAbbreviation: string;
  opponentRecord: string;
  opponentRank: string;
  isHomeGame: boolean;
  gameId: number;
  venue: string;
  offensiveTendency: string;
  defensiveTendency: string;
  gameWreckerName: string;
  gameWreckerPosition: string;
  gameWreckerRating: number;
  recommendedCounterSummary: string;
  telemetry: OpponentTelemetryData;
}

export interface LockedCoordinatorGameplan {
  seasonId: number;
  week: number;
  teamId: number;
  opponentId: number | null;
  selections: Record<SituationalQuadrantId, string>;
  lockedAtIso: string;
  synergyScore: number;
}

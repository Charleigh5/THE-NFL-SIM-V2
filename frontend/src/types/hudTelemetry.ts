/**
 * HUD Telemetry & In-Game Coaching Contracts
 * ==========================================
 * Strict TypeScript types for:
 * 1. Floating Ben Baldwin 4th-down decision pill
 * 2. Game momentum flow & Win Probability trajectories
 * 3. Tactile keyboard audibles engine
 */

export type DecisionStrength =
  | "STRONG_GO"
  | "LEAN_GO"
  | "TOSS_UP"
  | "LEAN_PUNT"
  | "STRONG_PUNT"
  | "STRONG_FG"
  | "LEAN_FG";

export interface FourthDownTelemetryPayload {
  yardLine: number;
  yardsToGo: number;
  scoreDifferential: number;
  quarter: number;
  timeRemainingSeconds: number;
  recommendation: "GO" | "FIELD_GOAL" | "PUNT";
  recommendationStrength: DecisionStrength;
  wpGo: number;
  wpFg: number;
  wpPunt: number;
  wpNetGain: number;
  conversionProb: number;
  fgMakeProb: number;
  fgDistance: number;
  summary: string;
  isGarbageTime: boolean;
}

export interface FourthDownTelemetryRequest {
  yardLine?: number;
  yardsToGo?: number;
  scoreDifferential?: number;
  quarter?: number;
  timeRemainingSeconds?: number;
  timeouts?: number;
}

export interface GameMomentumPlayNode {
  playIndex: number;
  quarter: number;
  gameClock: string;
  down: number;
  distance: number;
  yardLine: number;
  description: string;
  homeWinProb: number;
  awayWinProb: number;
  playEpa: number;
  isKeyEvent: boolean;
}

export interface MomentumFlowResponse {
  gameId: number;
  playNodes: GameMomentumPlayNode[];
  currentHomeWp: number;
  currentAwayWp: number;
  homeTeamAbbr: string;
  awayTeamAbbr: string;
  homeScore: number;
  awayScore: number;
}

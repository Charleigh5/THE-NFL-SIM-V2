export interface TurfCell {
  gridX: number;
  gridY: number;
  wearLevel: number; // 0.0 (pristine) to 1.0 (heavily degraded)
  friction: number; // 1.0 down to 0.70
  tacklesCount: number;
}

export interface TurfGridData {
  rows: number;
  cols: number;
  cells: TurfCell[][];
}

export type CognitiveStressState = "RELAXED" | "FOCUSED" | "STRESSED" | "PANICKED" | "FLOW";

export interface PlayerCognitiveTelemetry {
  playerId: number | string;
  name: string;
  jerseyNumber: number;
  position: string;
  x: number; // Field coordinate yards (0-100)
  y: number; // Field coordinate yards (0-53.3)
  orientationRad: number; // Angle in radians
  visionConeAngleDeg: number; // Vision cone angle (e.g. 90-130 deg)
  visionDepthYards: number; // Vision depth in yards
  cognitiveState: CognitiveStressState;
  s2LatencyMs: number; // Processing latency ms
  isOffense: boolean;
}

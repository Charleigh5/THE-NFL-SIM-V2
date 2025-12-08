export const MomentumState = {
  COLD: "COLD",
  NEUTRAL: "NEUTRAL",
  HEATING_UP: "HEATING_UP",
  ON_FIRE: "ON_FIRE",
  ICE_COLD: "ICE_COLD",
} as const;

export type MomentumState = (typeof MomentumState)[keyof typeof MomentumState];

export interface TeamMomentum {
  score: number; // 0-100
  state: MomentumState;
  consecutiveSuccesses: number;
}

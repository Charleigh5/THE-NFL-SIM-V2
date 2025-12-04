export const InteractionOutcome = {
  DOMINANT_WIN: "DOMINANT_WIN",
  WIN: "WIN",
  SLIGHT_WIN: "SLIGHT_WIN",
  NEUTRAL: "NEUTRAL",
  SLIGHT_LOSS: "SLIGHT_LOSS",
  LOSS: "LOSS",
  DOMINANT_LOSS: "DOMINANT_LOSS",
} as const;

export type InteractionOutcome = (typeof InteractionOutcome)[keyof typeof InteractionOutcome];

export interface InteractionResult {
  interaction_name: string;
  attacker_name: string;
  defender_name: string;
  outcome: InteractionOutcome;
  winner_boost: number;
  loser_penalty: number;
  narrative: string;
  raw_differential: number;
  modifiers: Record<string, number>;
}

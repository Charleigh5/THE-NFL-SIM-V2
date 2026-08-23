/**
 * Pillar 2 Frontend Data Contracts: Dynasty RPG & Empire Economics
 * File: frontend/src/types/dynasty.ts
 */

export type DevelopmentTier = 'NORMAL' | 'STAR' | 'SUPERSTAR' | 'XFACTOR';
export type ZoneAbilityStatus = 'INACTIVE' | 'ACTIVE' | 'KNOCKED_OUT';

export interface AbilityDefinition {
  key: string;
  name: string;
  tier: 'COMMON' | 'SILVER' | 'GOLD' | 'ELITE';
  category: 'MENTAL' | 'PHYSICAL_TECHNIQUE' | 'COVERAGE' | 'RECEIVING' | 'TRENCH' | 'LEADERSHIP';
  positionRequirements: string[];
  levelRequirement: number;
  xpCost: number;
  attributeRequirements: Record<string, number>;
  effects: Record<string, number>;
}

export interface PlayerDynastyState {
  playerId: number;
  developmentTier: DevelopmentTier;
  xp: number;
  level: number;
  skillPoints: number;
  equippedPassives: string[];
  zoneAbilityKey?: string;
  zoneStatus: ZoneAbilityStatus;
  hiddenPotentialRevealed: boolean;
  scoutedPotentialRange: [number, number];
}

export interface CapologyLedgerItem {
  playerId: number;
  playerName: string;
  position: string;
  baseSalary: number;
  proratedBonus: number;
  rosterBonus: number;
  capHit: number;
  cashOutlay: number;
  deadMoneyIfCutPreJune1: number;
  deadMoneyIfCutPostJune1: number;
  restructureSavingsPossible: number;
}

export interface MedicalTriageState {
  playerId: number;
  bodyPart: 'HEAD' | 'NECK' | 'SHOULDER' | 'TORSO' | 'KNEE' | 'HAMSTRING' | 'ANKLE' | 'ACHILLES';
  severityGrade: number;
  weeksToRecovery: number;
  canPlayThrough: boolean;
  toradolActive: boolean;
  braceEquipped: boolean;
  recurrenceRiskPct: number;
  penalties: Record<string, number>;
}

export interface DAGStorylinePrompt {
  nodeId: string;
  arcName: string;
  headline: string;
  narrativeText: string;
  initiatorPlayerName?: string;
  initiatorPlayerOvr?: number;
  choices: {
    choiceId: string;
    label: string;
    consequencesSummary: string;
    moraleDelta: number;
    capDelta: number;
  }[];
}

export interface TradeEvaluationPayload {
  proposingTeamId: number;
  receivingTeamId: number;
  offeredPlayerIds: number[];
  offeredPicks: { year: number; round: number }[];
  requestedPlayerIds: number[];
  requestedPicks: { year: number; round: number }[];
  netValueDelta: number;
  aiAcceptanceProbability: number;
}
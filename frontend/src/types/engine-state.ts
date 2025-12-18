/**
 * Engine State Types
 *
 * Strictly typed interfaces for simulation engine data.
 * Replaces Record<string, unknown> with explicit types for better
 * type safety and debugging.
 */

// =============================================================================
// GENESIS KERNEL - Biological/Physical State
// =============================================================================

export interface GenesisPlayerState {
  playerId: number;
  fatigueLevel: number; // 0-100
  injuryRisk: number; // 0-1
  staminaRemaining: number; // 0-100
  hydration: number; // 0-100
}

export interface GenesisState {
  players: Record<number, GenesisPlayerState>;
  environmentalEffects: {
    temperature: number;
    altitude: number;
    humidity: number;
  };
  overallFatigueHome: number;
  overallFatigueAway: number;
}

// =============================================================================
// EMPIRE KERNEL - XP/Progression State
// =============================================================================

export interface EmpirePlayerXP {
  playerId: number;
  currentXP: number;
  level: number;
  xpToNextLevel: number;
  recentGains: Array<{
    amount: number;
    reason: string;
    timestamp: number;
  }>;
}

export interface EmpireState {
  players: Record<number, EmpirePlayerXP>;
  gameXPMultiplier: number;
  bonusXPActive: boolean;
}

// =============================================================================
// HIVE KERNEL - Chemistry/Team Dynamics
// =============================================================================

export interface HiveUnitChemistry {
  unitName: string; // e.g., "Offensive Line"
  chemistryLevel: number; // 0-100
  consecutiveGames: number;
  bonuses: {
    passBlock: number;
    runBlock: number;
    awareness: number;
  };
}

export interface HiveState {
  homeTeamChemistry: number;
  awayTeamChemistry: number;
  units: Record<string, HiveUnitChemistry>;
  rivalryIntensity: number;
}

// =============================================================================
// SOCIETY KERNEL - Momentum/Social State
// =============================================================================

export interface SocietyMomentumEvent {
  type: string;
  team: "home" | "away";
  impact: number;
  description: string;
  timestamp: number;
}

export interface SocietyState {
  homeMomentum: number; // -100 to 100
  awayMomentum: number;
  crowdEnergy: number; // 0-100
  recentEvents: SocietyMomentumEvent[];
  isHomeField: boolean;
}

// =============================================================================
// RPG KERNEL - Traits/Abilities State
// =============================================================================

export interface RPGActiveAbility {
  abilityId: string;
  playerId: number;
  cooldownRemaining: number;
  isActive: boolean;
}

export interface RPGTraitActivation {
  traitName: string;
  playerId: number;
  triggerCondition: string;
  effectDescription: string;
}

export interface RPGState {
  activeAbilities: RPGActiveAbility[];
  traitActivations: RPGTraitActivation[];
  clutchModeActive: boolean;
  starPlayerBoosts: Record<number, number>;
}

// =============================================================================
// COMBINED ENGINE DATA
// =============================================================================

export interface TypedEngineData {
  genesis: GenesisState;
  empire: EmpireState;
  hive: HiveState;
  society: SocietyState;
  rpg: RPGState;
}

// Default empty states for initialization
export const DEFAULT_GENESIS_STATE: GenesisState = {
  players: {},
  environmentalEffects: {
    temperature: 70,
    altitude: 0,
    humidity: 50,
  },
  overallFatigueHome: 0,
  overallFatigueAway: 0,
};

export const DEFAULT_EMPIRE_STATE: EmpireState = {
  players: {},
  gameXPMultiplier: 1.0,
  bonusXPActive: false,
};

export const DEFAULT_HIVE_STATE: HiveState = {
  homeTeamChemistry: 50,
  awayTeamChemistry: 50,
  units: {},
  rivalryIntensity: 0,
};

export const DEFAULT_SOCIETY_STATE: SocietyState = {
  homeMomentum: 0,
  awayMomentum: 0,
  crowdEnergy: 50,
  recentEvents: [],
  isHomeField: true,
};

export const DEFAULT_RPG_STATE: RPGState = {
  activeAbilities: [],
  traitActivations: [],
  clutchModeActive: false,
  starPlayerBoosts: {},
};

export const DEFAULT_ENGINE_DATA: TypedEngineData = {
  genesis: DEFAULT_GENESIS_STATE,
  empire: DEFAULT_EMPIRE_STATE,
  hive: DEFAULT_HIVE_STATE,
  society: DEFAULT_SOCIETY_STATE,
  rpg: DEFAULT_RPG_STATE,
};

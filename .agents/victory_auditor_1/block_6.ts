/**
 * Formal Data Contracts - TypeScript Definitions
 * File: frontend/src/types/domain_contracts.ts
 */

// =============================================================================
// 1. ENUMERATIONS & CONSTANTS
// =============================================================================

export const DevTrait = {
  NORMAL: "NORMAL",
  STAR: "STAR",
  SUPERSTAR: "SUPERSTAR",
  XFACTOR: "XFACTOR",
} as const;
export type DevTrait = (typeof DevTrait)[keyof typeof DevTrait];

export const OvrTier = {
  CLUB_99: "99_CLUB",
  ELITE: "ELITE",
  GOLD: "GOLD",
  SILVER: "SILVER",
  BRONZE: "BRONZE",
} as const;
export type OvrTier = (typeof OvrTier)[keyof typeof OvrTier];

export const InjuryStatus = {
  HEALTHY: "HEALTHY",
  QUESTIONABLE: "QUESTIONABLE",
  DOUBTFUL: "DOUBTFUL",
  OUT: "OUT",
  INJURED_RESERVE: "INJURED_RESERVE",
} as const;
export type InjuryStatus = (typeof InjuryStatus)[keyof typeof InjuryStatus];

export const AnatomicalZone = {
  HEAD: "HEAD",
  NECK: "NECK",
  SHOULDER: "SHOULDER",
  TORSO: "TORSO",
  ARM_ELBOW: "ARM_ELBOW",
  HIP_GROIN: "HIP_GROIN",
  KNEE: "KNEE",
  ANKLE_FOOT: "ANKLE_FOOT",
} as const;
export type AnatomicalZone = (typeof AnatomicalZone)[keyof typeof AnatomicalZone];

export const MedicalIntervention = {
  CONSERVATIVE_REHAB: "CONSERVATIVE_REHAB",
  SURGICAL_REPAIR: "SURGICAL_REPAIR",
  PAIN_MANAGEMENT_TORADOL: "PAIN_MANAGEMENT_TORADOL",
  HEAVY_BRACE: "HEAVY_BRACE",
} as const;
export type MedicalIntervention = (typeof MedicalIntervention)[keyof typeof MedicalIntervention];

export const BroadcastPhase = {
  IDLE_STADIUM: "IDLE_STADIUM",
  PRE_PLAY: "PRE_PLAY",
  PRE_SNAP: "PRE_SNAP",
  IN_PLAY: "IN_PLAY",
  POST_PLAY_REACTION: "POST_PLAY_REACTION",
  HUD_UPDATE: "HUD_UPDATE",
  HIGHLIGHT_REPLAY: "HIGHLIGHT_REPLAY",
} as const;
export type BroadcastPhase = (typeof BroadcastPhase)[keyof typeof BroadcastPhase];

export const AudioTriggerType = {
  WHISTLE: "WHISTLE",
  COLLISION_HIT: "COLLISION_HIT",
  CROWD_ROAR_SWELL: "CROWD_ROAR_SWELL",
  CROWD_SILENCE: "CROWD_SILENCE",
  STADIUM_HORN: "STADIUM_HORN",
  STINGER_3RD_DOWN: "STINGER_3RD_DOWN",
  STINGER_TOUCHDOWN: "STINGER_TOUCHDOWN",
  UI_SNAP: "UI_SNAP",
} as const;
export type AudioTriggerType = (typeof AudioTriggerType)[keyof typeof AudioTriggerType];

export interface Vector3D {
  readonly x: number;
  readonly y: number;
  readonly z: number;
}

// =============================================================================
// 2. PLAYER & BIOMETRIC INTERFACES
// =============================================================================

export interface PlayerGenesisBiometrics {
  readonly fastTwitchRatio: number;
  readonly wingspanInches: number;
  readonly handSizeInches: number;
  readonly s2CognitionScore: number;
  readonly reactionLatencyMs: number;
  readonly maxAccelerationCap: number;
  readonly medicalRiskFlags: readonly string[];
}

export interface PlayerAttributes {
  readonly speed: number;
  readonly acceleration: number;
  readonly agility: number;
  readonly strength: number;
  readonly awareness: number;
  readonly throwPower?: number;
  readonly throwAccuracyShort?: number;
  readonly throwAccuracyDeep?: number;
  readonly carrying?: number;
  readonly catching?: number;
  readonly catchInTraffic?: number;
  readonly passBlock?: number;
  readonly runBlock?: number;
  readonly blockShedding?: number;
  readonly tackle?: number;
  readonly manCoverage?: number;
  readonly zoneCoverage?: number;
}

export interface PlayerContract {
  readonly yearsRemaining: number;
  readonly totalValue: number;
  readonly guaranteedAmount: number;
  readonly currentYearBaseSalary: number;
  readonly currentYearSigningBonusProration: number;
  readonly currentYearCapHit: number;
  readonly deadCapIfCutPreJune1: number;
  readonly deadCapIfCutPostJune1: number;
  readonly restructureEligible: boolean;
}

export interface PlayerFatigueState {
  readonly atpPcStamina: number;
  readonly glycolyticBurn: number;
  readonly aerobicRecoveryRate: number;
  readonly cnsNeurologicalFatigue: number;
  readonly compositeAthleticPenalty: number;
}

export interface PlayerEntity {
  readonly id: number;
  readonly firstName: string;
  readonly lastName: string;
  readonly jerseyNumber: number;
  readonly position: string;
  readonly overallRating: number;
  readonly ovrTier: OvrTier;
  readonly devTrait: DevTrait;
  readonly age: number;
  readonly teamId?: number;
  readonly injuryStatus: InjuryStatus;
  readonly biometrics: PlayerGenesisBiometrics;
  readonly attributes: PlayerAttributes;
  readonly contract: PlayerContract;
  readonly fatigue: PlayerFatigueState;
}

// =============================================================================
// 3. TEAM & FINANCIAL INTERFACES
// =============================================================================

export interface CoachingPhilosophy {
  readonly offensiveScheme: string;
  readonly defensiveScheme: string;
  readonly runPassRatio: number;
  readonly offensiveTempo: "HURRY_UP" | "STANDARD" | "CHEW_CLOCK";
  readonly fourthDownAggressiveness: number;
  readonly blitzFrequency: number;
}

export interface TeamCapSheet {
  readonly teamId: number;
  readonly leagueSalaryCap: number;
  readonly totalCommittedSalaries: number;
  readonly totalDeadMoney: number;
  readonly availableCapSpace: number;
  readonly capRolloverPreviousYear: number;
  readonly fourYearCashSpendingFloorPct: number;
}

export interface TeamEntity {
  readonly id: number;
  readonly city: string;
  readonly name: string;
  readonly abbreviation: string;
  readonly conference: "AFC" | "NFC";
  readonly division: "NORTH" | "SOUTH" | "EAST" | "WEST";
  readonly primaryColor: string;
  readonly secondaryColor: string;
  readonly accentColor: string;
  readonly stadiumName: string;
  readonly stadiumRoofType: "OUTDOOR" | "DOME" | "RETRACTABLE";
  readonly overallRating: number;
  readonly offenseRating: number;
  readonly defenseRating: number;
  readonly chemistryScore: number;
  readonly moraleScore: number;
  readonly capSheet: TeamCapSheet;
  readonly philosophy: CoachingPhilosophy;
}

// =============================================================================
// 4. SIMULATION & TELEMETRY INTERFACES
// =============================================================================

export interface TelemetryPlayerState {
  readonly playerId: number;
  readonly jerseyNumber: number;
  readonly teamId: number;
  readonly position: Vector3D;
  readonly velocity: Vector3D;
  readonly facingAngle: number;
  readonly staminaPct: number;
  readonly currentAction: string;
}

export interface TrenchCollisionVector {
  readonly offensiveLinemanId: number;
  readonly defensiveRusherId: number;
  readonly contactPoint: Vector3D;
  readonly kineticForceNewtons: number;
  readonly leverageAdvantageBias: number;
}

export interface TelemetryFrame {
  readonly frameIndex: number;
  readonly gameClockSeconds: number;
  readonly ballPosition: Vector3D;
  readonly ballVelocity: Vector3D;
  readonly players: readonly TelemetryPlayerState[];
  readonly trenchCollisions: readonly TrenchCollisionVector[];
}

export interface PlayCallInput {
  readonly gameId: number;
  readonly possessionTeamId: number;
  readonly playType: "RUN" | "PASS" | "PLAY_ACTION" | "SCREEN" | "FIELD_GOAL" | "PUNT" | "KNEEL" | "SPIKE";
  readonly offensiveFormation: string;
  readonly offensiveConcept: string;
  readonly defensiveScheme: string;
  readonly defensiveBlitzCount: number;
  readonly primaryTargetReceiverId?: number;
  readonly hotRouteAdjustments: Readonly<Record<number, string>>;
}

// =============================================================================
// 5. BROADCAST & AUDIO INTERFACES
// =============================================================================

export interface CameraShot {
  readonly id: string;
  readonly position: Vector3D;
  readonly target: Vector3D;
  readonly fov?: number;
  readonly roll?: number;
  readonly duration: number;
  readonly interpolation?: "linear" | "smooth" | "snap";
}

export interface OverlayCue {
  readonly id: string;
  readonly type: "lower_third" | "matchup_card" | "score_bug" | "telestrator" | "stat_popover" | "laser_hud";
  readonly data: Readonly<Record<string, string | number | boolean | readonly string[]>>;
  readonly duration?: number;
  readonly animation?: "fade" | "slide" | "pop" | "laser_sweep";
  readonly layer?: number;
}

export interface ClipCue {
  readonly id: string;
  readonly clipType: "formation_sweep" | "matchup_card" | "situation_lower_third" | "replay_angle" | "celebration";
  readonly cameras: readonly CameraShot[];
  readonly overlays: readonly OverlayCue[];
  readonly duration: number;
  readonly audioCue?: string;
  readonly skippable?: boolean;
}

export interface AudioTriggerPayload {
  readonly triggerType: AudioTriggerType;
  readonly intensity: number;
  readonly frequencyOverride?: number;
  readonly kineticEnergy?: number;
  readonly stadiumDecibels?: number;
}

// =============================================================================
// 6. MEDICAL & INJURY INTERFACES
// =============================================================================

export interface AnatomicalZoneInjury {
  readonly zone: AnatomicalZone;
  readonly diagnosis: string;
  readonly severityGrade: "MILD" | "MODERATE" | "SEVERE" | "CATASTROPHIC";
  readonly painIndex: number;
  readonly estimatedWeeksOut: number;
  readonly selectedIntervention: MedicalIntervention;
  readonly reinjuryProbabilityMultiplier: number;
}

export interface InjuryTriageRecord {
  readonly id: string;
  readonly playerId: number;
  readonly gameId?: number;
  readonly timestamp: number;
  readonly activeInjuries: readonly AnatomicalZoneInjury[];
  readonly medicalStaffRating: number;
  readonly clearedForLimitedPractice: boolean;
}

// =============================================================================
// 7. WEBSOCKET DISCRIMINATED UNIONS
// =============================================================================

export interface GameStateSyncPayload {
  readonly gameId: number;
  readonly quarter: number;
  readonly clockSecondsRemaining: number;
  readonly homeScore: number;
  readonly awayScore: number;
  readonly down: number;
  readonly distance: number;
  readonly yardLine: number;
  readonly possessionTeamId: number;
  readonly broadcastPhase: BroadcastPhase;
}

export type WebSocketBroadcastMessage =
  | {
      readonly sequenceId: number;
      readonly messageType: "STATE_SYNC";
      readonly timestamp: number;
      readonly gameId: number;
      readonly payload: GameStateSyncPayload;
    }
  | {
      readonly sequenceId: number;
      readonly messageType: "CLIP_DISPATCH";
      readonly timestamp: number;
      readonly gameId: number;
      readonly payload: ClipCue;
    }
  | {
      readonly sequenceId: number;
      readonly messageType: "TELEMETRY_FRAME";
      readonly timestamp: number;
      readonly gameId: number;
      readonly payload: TelemetryFrame;
    }
  | {
      readonly sequenceId: number;
      readonly messageType: "AUDIO_TRIGGER";
      readonly timestamp: number;
      readonly gameId: number;
      readonly payload: AudioTriggerPayload;
    }
  | {
      readonly sequenceId: number;
      readonly messageType: "INJURY_EVENT";
      readonly timestamp: number;
      readonly gameId: number;
      readonly payload: InjuryTriageRecord;
    };
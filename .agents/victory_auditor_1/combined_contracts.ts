export interface Vector3D {
  x: number; // Width: -26.65 to +26.65 yds
  y: number; // Length: 0.0 to 100.0 yds
  z: number; // Height: 0.0 to 25.0 yds
}

export interface S2CognitiveProfile {
  playerId: string;
  s2CompositeScore: number;
  visualProcessingSpeed: number;
  trackingCapacity: number;
  trajectoryEstimation: number;
  highSpeedDecisionMaking: number;
  impulsivityControl: number;
  spatialAwareness: number;
  distractionControl: number;
  rhythmTiming: number;
}

export interface BiometricCompartmentState {
  playerId: string;
  atpPcCapacity: number;
  glycolyticCapacity: number;
  lactateConcentration: number;
  aerobicBaseCapacity: number;
  neuralCnsCapacity: number;
  cumulativeSnaps: number;
  currentHeartRateBpm: number;
  effectiveSpeedMultiplier: number;
  effectiveStrengthMultiplier: number;
  effectiveReactionMultiplier: number;
  injuryRiskMultiplier: number;
}

export type PassRushTechnique =
  | 'BULL_RUSH'
  | 'SWIM'
  | 'RIP'
  | 'SPIN'
  | 'STUNT_LOOP'
  | 'STUNT_CRASH'
  | 'CONTAIN';

export interface TrenchEngagement {
  olPlayerId: string;
  dlPlayerId: string;
  engagementFrameStart: number;
  padLevelLeverageRatio: number;
  contactForceVector: Vector3D;
  activeTechnique: PassRushTechnique;
  isShed: boolean;
  shedVector?: Vector3D;
  pocketPressureContribution: number;
}

export interface PocketEnvelopeState {
  frameIndex: number;
  convexHullPoints: Vector3D[];
  pocketAreaSqYds: number;
  pocketCollapseRateSqYdsPerSec: number;
  qbPressureIndex: number;
  pocketStatus: 'CLEAN' | 'CLOSING' | 'COLLAPSED' | 'BROKEN';
}

export interface BallState {
  frameIndex: number;
  position: Vector3D;
  velocity: Vector3D;
  spinRateRpm: number;
  spinAxisUnitVector: Vector3D;
  wobbleAngleDegrees: number;
  isInFlight: boolean;
  throwType?: 'BULLET' | 'TOUCH' | 'LOB' | 'SCREEN';
  targetReceiverId?: string;
  flightTimeSeconds: number;
}

export interface PhysicsTickFrameState {
  tickNumber: number;
  playTimeSeconds: number;
  ball: BallState;
  playerPositions: Record<string, Vector3D>;
  playerVelocities: Record<string, Vector3D>;
  playerFacingAnglesDeg: Record<string, number>;
  trenchEngagements: TrenchEngagement[];
  pocketEnvelope: PocketEnvelopeState;
  frameSha256Hash: string;
}

// --- NEW BLOCK ---

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

// --- NEW BLOCK ---

export function playRefereeWhistle(audioCtx: AudioContext, intensity: number = 1.0): void {
  const now = audioCtx.currentTime;
  
  const osc1 = audioCtx.createOscillator();
  const osc2 = audioCtx.createOscillator();
  const lfo = audioCtx.createOscillator();
  const lfoGain = audioCtx.createGain();
  const masterGain = audioCtx.createGain();
  
  // Dual fundamental frequencies creating acoustic beat interference
  osc1.type = "sine";
  osc1.frequency.setValueAtTime(2780, now);
  osc2.type = "sine";
  osc2.frequency.setValueAtTime(3090, now);
  
  // 28.5 Hz Pea Rattle Modulation
  lfo.type = "sine";
  lfo.frequency.setValueAtTime(28.5, now);
  lfoGain.gain.setValueAtTime(160, now);
  lfo.connect(osc1.frequency);
  lfo.connect(osc2.frequency);
  
  // ADSR Gain Envelope
  const peakGain = 0.38 * Math.min(1.0, Math.max(0.1, intensity));
  masterGain.gain.setValueAtTime(0.0001, now);
  masterGain.gain.linearRampToValueAtTime(peakGain, now + 0.035);
  masterGain.gain.setValueAtTime(peakGain, now + 0.28);
  masterGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.48);
  
  osc1.connect(masterGain);
  osc2.connect(masterGain);
  masterGain.connect(audioCtx.destination);
  
  lfo.start(now);
  osc1.start(now);
  osc2.start(now);
  
  lfo.stop(now + 0.5);
  osc1.stop(now + 0.5);
  osc2.stop(now + 0.5);
}

// --- NEW BLOCK ---

export function playTackleImpact(audioCtx: AudioContext, kineticEnergyJoules: number): void {
  const now = audioCtx.currentTime;
  const normalizedEnergy = Math.min(1.0, Math.max(0.1, kineticEnergyJoules / 3500));
  
  // Layer 1: Sub-Bass Thud
  const thudOsc = audioCtx.createOscillator();
  const thudGain = audioCtx.createGain();
  thudOsc.type = "sine";
  thudOsc.frequency.setValueAtTime(140, now);
  thudOsc.frequency.exponentialRampToValueAtTime(28, now + 0.16);
  thudGain.gain.setValueAtTime(0.65 * normalizedEnergy, now);
  thudGain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
  thudOsc.connect(thudGain);
  thudGain.connect(audioCtx.destination);
  thudOsc.start(now);
  thudOsc.stop(now + 0.2);
  
  // Layer 2: Pad Crack (Filtered Noise Burst)
  const bufferSize = audioCtx.sampleRate * 0.04;
  const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }
  const noiseSource = audioCtx.createBufferSource();
  noiseSource.buffer = noiseBuffer;
  
  const padFilter = audioCtx.createBiquadFilter();
  padFilter.type = "bandpass";
  padFilter.frequency.setValueAtTime(3200, now);
  padFilter.Q.setValueAtTime(2.2, now);
  
  const padGain = audioCtx.createGain();
  padGain.gain.setValueAtTime(0.85 * normalizedEnergy, now);
  padGain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
  
  noiseSource.connect(padFilter);
  padFilter.connect(padGain);
  padGain.connect(audioCtx.destination);
  noiseSource.start(now);
}

// --- NEW BLOCK ---

/**
 * Catmull-Rom Spline Telestrator Path Smoother
 * Converts raw discrete pointer samples into smooth cubic Bezier control points.
 */
export interface TelestratorPoint {
  x: number;
  y: number;
  t: number; // timestamp ms
}

export function generateSmoothTelestratorPath(points: readonly TelestratorPoint[]): string {
  if (points.length < 2) return "";
  if (points.length === 2) {
    return `M ${points[0].x},${points[0].y} L ${points[1].x},${points[1].y}`;
  }

  let d = `M ${points[0].x},${points[0].y}`;
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = i > 0 ? points[i - 1] : points[i];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = i != points.length - 2 ? points[i + 2] : p2;

    const cp1x = p1.x + (p2.x - p0.x) / 6;
    const cp1y = p1.y + (p2.y - p0.y) / 6;
    const cp2x = p2.x - (p3.x - p1.x) / 6;
    const cp2y = p2.y - (p3.y - p1.y) / 6;

    d += ` C ${cp1x.toFixed(2)},${cp1y.toFixed(2)} ${cp2x.toFixed(2)},${cp2y.toFixed(2)} ${p2.x.toFixed(2)},${p2.y.toFixed(2)}`;
  }
  return d;
}

// --- NEW BLOCK ---

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
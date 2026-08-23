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
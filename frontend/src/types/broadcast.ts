/**
 * Broadcast & 3D Visualization System Types
 *
 * Core types for the cutscene/animation bridge and 3D live visualization.
 * Central single source of truth for:
 * - State machine-driven phase transitions (PRE_PLAY -> PLAY_EXEC -> POST_PLAY -> REPLAY -> BETWEEN_DOWNS)
 * - Cutscene clips, camera paths, and graphic overlays
 * - 3D player models, team branding, and field positioning
 */

/**
 * BroadcastPhase - The 7 legal states of the broadcast state machine
 */
export const BroadcastPhase = {
  /** Initial state before any play action */
  IDLE: "IDLE",
  /** Pre-play cinematics: formation showcase, matchup cards */
  PRE_PLAY: "PRE_PLAY",
  /** Active play execution: snap to whistle */
  PLAY_EXEC: "PLAY_EXEC",
  /** Post-play reactions: celebrations, sideline shots */
  POST_PLAY: "POST_PLAY",
  /** Instant replay sequence */
  REPLAY: "REPLAY",
  /** Transition between downs: score updates, next play setup */
  BETWEEN_DOWNS: "BETWEEN_DOWNS",
  /** Halftime/show break state */
  HALFTIME: "HALFTIME",
} as const;

export type BroadcastPhase = (typeof BroadcastPhase)[keyof typeof BroadcastPhase];

/**
 * Legal phase transitions table
 * Key: current phase, Value: array of allowed next phases
 */
export const PHASE_TRANSITIONS: Record<BroadcastPhase, BroadcastPhase[]> = {
  [BroadcastPhase.IDLE]: [BroadcastPhase.PRE_PLAY],
  [BroadcastPhase.PRE_PLAY]: [BroadcastPhase.PLAY_EXEC, BroadcastPhase.IDLE],
  [BroadcastPhase.PLAY_EXEC]: [BroadcastPhase.POST_PLAY, BroadcastPhase.REPLAY],
  [BroadcastPhase.POST_PLAY]: [BroadcastPhase.REPLAY, BroadcastPhase.BETWEEN_DOWNS],
  [BroadcastPhase.REPLAY]: [BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.POST_PLAY],
  [BroadcastPhase.BETWEEN_DOWNS]: [BroadcastPhase.PRE_PLAY, BroadcastPhase.HALFTIME],
  [BroadcastPhase.HALFTIME]: [BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.IDLE],
};

/**
 * Validate if a phase transition is legal
 * @throws Error if transition is illegal
 */
export function validateTransition(from: BroadcastPhase, to: BroadcastPhase): boolean {
  const allowed = PHASE_TRANSITIONS[from];
  if (!allowed || !allowed.includes(to)) {
    throw new Error(
      `Illegal broadcast phase transition: ${from} -> ${to}. Allowed: ${allowed ? allowed.join(", ") : "none"}`
    );
  }
  return true;
}

/**
 * CameraShot - A single camera configuration in 3D world space
 */
export interface CameraShot {
  id: string;
  position: { x: number; y: number; z: number };
  target: { x: number; y: number; z: number };
  fov?: number;
  roll?: number;
  duration?: number;
  interpolation?: "linear" | "smooth" | "snap";
}

/**
 * OverlayCue - HUD/graphic overlay instruction
 */
export interface OverlayCue {
  id: string;
  type: "lower_third" | "matchup_card" | "score_bug" | "telestrator" | "stat_popover";
  data: Record<string, unknown>;
  duration?: number;
  animation?: "fade" | "slide" | "pop";
  layer?: number;
}

/**
 * ClipCue - A complete cutscene clip instruction
 */
export interface ClipCue {
  id: string;
  clipType:
    | "formation_sweep"
    | "matchup_card"
    | "situation_lower_third"
    | "replay_angle"
    | "celebration";
  cameras: CameraShot[];
  overlays: OverlayCue[];
  duration: number;
  audioCue?: string;
  skippable?: boolean;
}

/**
 * BroadcastPlayResult - Simulation output driving cutscenes and broadcasts
 */
export interface BroadcastPlayResult {
  playId: number;
  playType: "pass" | "run" | "sack" | "punt" | "field_goal" | "extra_point";
  outcome: "complete" | "incomplete" | "touchdown" | "turnover" | "no_play";
  yardsGained: number;
  passerId?: number;
  receiverId?: number;
  tacklerIds?: number[];
  ballCarrierId?: number;
  startTime: number;
  endTime: number;
  isHighlightWorthy?: boolean;
  isSack?: boolean;
}

// Backward compatibility alias for PlayResult within broadcast context
export type PlayResult = BroadcastPlayResult;

/**
 * BroadcastEvent - Events triggering state machine transitions
 */
export type BroadcastEvent =
  | { type: "PLAY_CALLED"; playResult: BroadcastPlayResult }
  | { type: "SNAP" }
  | { type: "WHISTLE"; playResult: BroadcastPlayResult }
  | { type: "REPLAY_REQUESTED"; angle?: string }
  | { type: "REPLAY_COMPLETE" }
  | { type: "NEXT_DOWN" }
  | { type: "HALFTIME_START" }
  | { type: "GAME_END" }
  | { type: "SKIP_CLIP" };

/**
 * BroadcastState - Full state container for broadcast system
 */
export interface BroadcastState {
  phase: BroadcastPhase;
  activeClip: ClipCue | null;
  currentCameraIndex: number;
  overlays: OverlayCue[];
  clipQueue: ClipCue[];
  lastPlayResult: BroadcastPlayResult | null;
  reducedMotion: boolean;
}

export type BroadcastReducer = (state: BroadcastState, event: BroadcastEvent) => BroadcastState;

// =============================================================================
// 3D VISUALIZATION MODEL TYPES (Single authoritative source of truth)
// =============================================================================

export type BodyType = "large" | "medium" | "lean" | "athletic" | "pocket" | "muscular" | "average";

export interface HelmetDesign {
  base: string;
  stripe: string;
  logo_side: boolean;
  facemask: string;
}

export interface PlayerVisuals {
  body_type: BodyType;
  jersey_color_primary: string;
  jersey_color_secondary: string;
  helmet_design: HelmetDesign;
  face_mask_color: string;
  cleat_color: string;
  accessories: string[];
}

export interface PlayerVisualData {
  id: number;
  name: string;
  number: number;
  position: string;
  position_group: "offense" | "defense" | "special_teams" | "unknown";
  height: number;
  weight: number;
  team_id?: number;
  visuals: PlayerVisuals;
}

export interface TeamVisualData {
  id: number;
  name: string;
  abbreviation: string;
  primary_color: string;
  secondary_color: string;
  logo_url: string;
  players: PlayerVisualData[];
}

export interface VisualTeam {
  id: number | string;
  name: string;
  city?: string;
  abbreviation: string;
  primary_color: string;
  secondary_color: string;
  logo_url?: string | null;
  players?: PlayerVisualData[];
}

export interface GameRosterData {
  game_id: number;
  home_team: TeamVisualData;
  away_team: TeamVisualData;
}

export interface PlayerFormationPosition {
  position: string;
  x: number;
  y: number;
  z: number;
}

export interface FormationData {
  play_id: number;
  formation: {
    offense: {
      name: string;
      players: PlayerFormationPosition[];
    };
    defense: {
      name: string;
      players: PlayerFormationPosition[];
    };
  };
}

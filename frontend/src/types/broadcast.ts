/**
 * Broadcast System Types
 * 
 * Core types for the cutscene/animation bridge system.
 * These types enable state machine-driven transitions between
 * PRE_PLAY → PLAY_EXEC → POST_PLAY → REPLAY → BETWEEN_DOWNS
 */

/**
 * BroadcastPhase - The 7 legal states of the broadcast state machine
 */
export enum BroadcastPhase {
  /** Initial state before any play action */
  IDLE = "IDLE",
  /** Pre-play cinematics: formation showcase, matchup cards */
  PRE_PLAY = "PRE_PLAY",
  /** Active play execution: snap to whistle */
  PLAY_EXEC = "PLAY_EXEC",
  /** Post-play reactions: celebrations, sideline shots */
  POST_PLAY = "POST_PLAY",
  /** Instant replay sequence */
  REPLAY = "REPLAY",
  /** Transition between downs: score updates, next play setup */
  BETWEEN_DOWNS = "BETWEEN_DOWNS",
  /** Halftime/show break state */
  HALFTIME = "HALFTIME",
}

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
  if (!allowed.includes(to)) {
    throw new Error(
      `Illegal broadcast phase transition: ${from} → ${to}. Allowed: ${allowed.join(", ")}`
    );
  }
  return true;
}

/**
 * CameraShot - A single camera configuration
 */
export interface CameraShot {
  /** Unique shot identifier */
  id: string;
  /** Camera position in world coordinates */
  position: { x: number; y: number; z: number };
  /** Camera look-at target */
  target: { x: number; y: number; z: number };
  /** Field of view in degrees */
  fov?: number;
  /** Camera roll in radians */
  roll?: number;
  /** Duration in seconds (for automated sequences) */
  duration?: number;
  /** Interpolation type: linear, smooth, snap */
  interpolation?: "linear" | "smooth" | "snap";
}

/**
 * OverlayCue - HUD/graphic overlay instruction
 */
export interface OverlayCue {
  /** Unique overlay identifier */
  id: string;
  /** Overlay type */
  type: "lower_third" | "matchup_card" | "score_bug" | "telestrator" | "stat_popover";
  /** Data to display */
  data: Record<string, unknown>;
  /** Show duration in seconds */
  duration?: number;
  /** Animation in/out */
  animation?: "fade" | "slide" | "pop";
  /** Z-index layering */
  layer?: number;
}

/**
 * ClipCue - A complete clip/cutscene instruction
 */
export interface ClipCue {
  /** Unique clip identifier */
  id: string;
  /** Clip type/category */
  clipType: "formation_sweep" | "matchup_card" | "situation_lower_third" | "replay_angle" | "celebration";
  /** Ordered camera shots for this clip */
  cameras: CameraShot[];
  /** Overlay cues synchronized with this clip */
  overlays: OverlayCue[];
  /** Total clip duration in seconds */
  duration: number;
  /** Optional audio cue identifier */
  audioCue?: string;
  /** Skip condition (for reduced motion, user skip) */
  skippable?: boolean;
}

/**
 * PlayResult - Simulation output that drives broadcast cues
 * This mirrors the backend PlayResult structure
 */
export interface PlayResult {
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
  /** Whether this play is highlight-worthy (big gain, score, turnover) */
  isHighlightWorthy?: boolean;
  /** Whether the play was a sack */
  isSack?: boolean;
}

/**
 * BroadcastEvent - Events that trigger state machine transitions
 */
export type BroadcastEvent =
  | { type: "PLAY_CALLED"; playResult: PlayResult }
  | { type: "SNAP" }
  | { type: "WHISTLE"; playResult: PlayResult }
  | { type: "REPLAY_REQUESTED"; angle?: string }
  | { type: "REPLAY_COMPLETE" }
  | { type: "NEXT_DOWN" }
  | { type: "HALFTIME_START" }
  | { type: "GAME_END" }
  | { type: "SKIP_CLIP" };

/**
 * BroadcastState - Complete state container for broadcast system
 */
export interface BroadcastState {
  /** Current phase */
  phase: BroadcastPhase;
  /** Currently active clip (if any) */
  activeClip: ClipCue | null;
  /** Current camera shot index */
  currentCameraIndex: number;
  /** Active overlays */
  overlays: OverlayCue[];
  /** Queue of upcoming clips */
  clipQueue: ClipCue[];
  /** Last play result */
  lastPlayResult: PlayResult | null;
  /** Reduced motion preference */
  reducedMotion: boolean;
}

/**
 * BroadcastReducer - State machine reducer function signature
 */
export type BroadcastReducer = (
  state: BroadcastState,
  event: BroadcastEvent
) => BroadcastState;

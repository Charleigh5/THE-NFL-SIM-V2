import { create } from "zustand";
import {
  BroadcastPhase,
  BroadcastState,
  BroadcastEvent,
  BroadcastReducer,
  ClipCue,
  OverlayCue,
  PlayResult,
  validateTransition,
} from "../types/broadcast";

/**
 * Default initial state for the broadcast system
 */
const initialState: BroadcastState = {
  phase: BroadcastPhase.IDLE,
  activeClip: null,
  currentCameraIndex: 0,
  overlays: [],
  clipQueue: [],
  lastPlayResult: null,
  reducedMotion: false,
};

/**
 * Broadcast reducer - handles state machine transitions
 * Validates all phase transitions and updates state accordingly
 */
export const broadcastReducer: BroadcastReducer = (state, event) => {
  const { type } = event;

  switch (type) {
    case "PLAY_CALLED": {
      // Transition from IDLE or BETWEEN_DOWNS to PRE_PLAY
      validateTransition(state.phase, BroadcastPhase.PRE_PLAY);
      return {
        ...state,
        phase: BroadcastPhase.PRE_PLAY,
        lastPlayResult: event.playResult,
        // Generate clip queue based on play result (simplified - CutsceneDirector will do this)
        clipQueue: [],
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "SNAP": {
      // Transition from PRE_PLAY to PLAY_EXEC
      validateTransition(state.phase, BroadcastPhase.PLAY_EXEC);
      return {
        ...state,
        phase: BroadcastPhase.PLAY_EXEC,
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "WHISTLE": {
      // Transition from PLAY_EXEC to POST_PLAY
      validateTransition(state.phase, BroadcastPhase.POST_PLAY);
      return {
        ...state,
        phase: BroadcastPhase.POST_PLAY,
        lastPlayResult: event.playResult,
        activeClip: null,
        currentCameraIndex: 0,
      };
    }

    case "REPLAY_REQUESTED": {
      // Transition to REPLAY from POST_PLAY or PLAY_EXEC
      const targetPhase = state.phase === BroadcastPhase.PLAY_EXEC
        ? BroadcastPhase.REPLAY
        : BroadcastPhase.REPLAY;
      validateTransition(state.phase, targetPhase);
      return {
        ...state,
        phase: BroadcastPhase.REPLAY,
        activeClip: null,
        currentCameraIndex: 0,
        // Could store requested angle here
      };
    }

    case "REPLAY_COMPLETE": {
      // Transition from REPLAY to BETWEEN_DOWNS
      validateTransition(state.phase, BroadcastPhase.BETWEEN_DOWNS);
      return {
        ...state,
        phase: BroadcastPhase.BETWEEN_DOWNS,
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "NEXT_DOWN": {
      // Transition from BETWEEN_DOWNS to PRE_PLAY (or HALFTIME)
      const nextPhase = state.lastPlayResult?.outcome === "touchdown" || 
                        state.lastPlayResult?.outcome === "turnover"
        ? BroadcastPhase.PRE_PLAY
        : BroadcastPhase.PRE_PLAY;
      validateTransition(state.phase, nextPhase);
      return {
        ...state,
        phase: nextPhase,
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "HALFTIME_START": {
      // Transition to HALFTIME
      validateTransition(state.phase, BroadcastPhase.HALFTIME);
      return {
        ...state,
        phase: BroadcastPhase.HALFTIME,
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "GAME_END": {
      // Return to IDLE
      validateTransition(state.phase, BroadcastPhase.IDLE);
      return {
        ...initialState,
        phase: BroadcastPhase.IDLE,
      };
    }

    case "SKIP_CLIP": {
      // Skip current clip - advance phase based on current state
      if (state.phase === BroadcastPhase.PRE_PLAY) {
        return {
          ...state,
          phase: BroadcastPhase.PLAY_EXEC,
          activeClip: null,
          currentCameraIndex: 0,
          overlays: [],
        };
      }
      if (state.phase === BroadcastPhase.POST_PLAY) {
        return {
          ...state,
          phase: BroadcastPhase.BETWEEN_DOWNS,
          activeClip: null,
          currentCameraIndex: 0,
          overlays: [],
        };
      }
      if (state.phase === BroadcastPhase.REPLAY) {
        return {
          ...state,
          phase: BroadcastPhase.BETWEEN_DOWNS,
          activeClip: null,
          currentCameraIndex: 0,
          overlays: [],
        };
      }
      return state;
    }

    default:
      return state;
  }
};

/**
 * BroadcastStore interface
 */
interface BroadcastStore extends BroadcastState {
  /** Dispatch an event to the state machine */
  dispatch: (event: BroadcastEvent) => void;
  
  /** Set the active clip */
  setActiveClip: (clip: ClipCue | null) => void;
  
  /** Advance to next camera shot in current clip */
  nextCameraShot: () => void;
  
  /** Set current camera index */
  setCameraIndex: (index: number) => void;
  
  /** Add overlay to stack */
  addOverlay: (overlay: OverlayCue) => void;
  
  /** Remove overlay by ID */
  removeOverlay: (overlayId: string) => void;
  
  /** Clear all overlays */
  clearOverlays: () => void;
  
  /** Add clip to queue */
  enqueueClip: (clip: ClipCue) => void;
  
  /** Dequeue next clip */
  dequeueClip: () => ClipCue | undefined;
  
  /** Clear clip queue */
  clearClipQueue: () => void;
  
  /** Set reduced motion preference */
  setReducedMotion: (enabled: boolean) => void;
  
  /** Reset to initial state */
  reset: () => void;
  
  /** Force set phase (for debugging only) */
  _debugSetPhase: (phase: BroadcastPhase) => void;
}

/**
 * Zustand store for broadcast system state management
 * 
 * Provides:
 * - State machine-driven phase transitions
 * - Clip queue management
 * - Overlay stack management
 * - Camera shot navigation
 * - Reduced motion support
 */
export const useBroadcastStore = create<BroadcastStore>((set, get) => ({
  // Initial state spread
  ...initialState,

  /**
   * Dispatch an event to trigger state machine transition
   */
  dispatch: (event: BroadcastEvent) => {
    set((state) => broadcastReducer(state, event));
  },

  /**
   * Set the currently active clip
   */
  setActiveClip: (clip: ClipCue | null) => {
    set({ 
      activeClip: clip,
      currentCameraIndex: 0,
    });
  },

  /**
   * Advance to next camera shot in current clip
   */
  nextCameraShot: () => {
    const { activeClip, currentCameraIndex } = get();
    if (!activeClip) return;
    
    const nextIndex = currentCameraIndex + 1;
    if (nextIndex < activeClip.cameras.length) {
      set({ currentCameraIndex: nextIndex });
    }
  },

  /**
   * Set current camera index directly
   */
  setCameraIndex: (index: number) => {
    const { activeClip } = get();
    if (!activeClip) return;
    
    const clampedIndex = Math.max(0, Math.min(index, activeClip.cameras.length - 1));
    set({ currentCameraIndex: clampedIndex });
  },

  /**
   * Add overlay to stack
   */
  addOverlay: (overlay: OverlayCue) => {
    set((state) => ({
      overlays: [...state.overlays, overlay],
    }));
  },

  /**
   * Remove overlay by ID
   */
  removeOverlay: (overlayId: string) => {
    set((state) => ({
      overlays: state.overlays.filter((o) => o.id !== overlayId),
    }));
  },

  /**
   * Clear all overlays
   */
  clearOverlays: () => {
    set({ overlays: [] });
  },

  /**
   * Add clip to queue
   */
  enqueueClip: (clip: ClipCue) => {
    set((state) => ({
      clipQueue: [...state.clipQueue, clip],
    }));
  },

  /**
   * Dequeue next clip (FIFO)
   */
  dequeueClip: () => {
    let dequeued: ClipCue | undefined;
    set((state) => {
      if (state.clipQueue.length === 0) return {};
      
      const [first, ...rest] = state.clipQueue;
      dequeued = first;
      return { clipQueue: rest };
    });
    return dequeued;
  },

  /**
   * Clear clip queue
   */
  clearClipQueue: () => {
    set({ clipQueue: [] });
  },

  /**
   * Set reduced motion preference
   */
  setReducedMotion: (enabled: boolean) => {
    set({ reducedMotion: enabled });
  },

  /**
   * Reset to initial state
   */
  reset: () => {
    set(initialState);
  },

  /**
   * Force set phase (DEBUG ONLY - bypasses validation)
   */
  _debugSetPhase: (phase: BroadcastPhase) => {
    console.warn(`[BroadcastStore] Debug phase set: ${phase}`);
    set({ phase });
  },
}));

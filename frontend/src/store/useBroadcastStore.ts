import { create } from "zustand";
import {
  BroadcastPhase,
  type BroadcastState,
  type BroadcastEvent,
  type BroadcastReducer,
  type ClipCue,
  type OverlayCue,
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
      validateTransition(state.phase, BroadcastPhase.PRE_PLAY);
      return {
        ...state,
        phase: BroadcastPhase.PRE_PLAY,
        lastPlayResult: event.playResult,
        clipQueue: [],
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "SNAP": {
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
      validateTransition(state.phase, BroadcastPhase.REPLAY);
      return {
        ...state,
        phase: BroadcastPhase.REPLAY,
        activeClip: null,
        currentCameraIndex: 0,
      };
    }

    case "REPLAY_COMPLETE": {
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
      validateTransition(state.phase, BroadcastPhase.PRE_PLAY);
      return {
        ...state,
        phase: BroadcastPhase.PRE_PLAY,
        activeClip: null,
        currentCameraIndex: 0,
        overlays: [],
      };
    }

    case "HALFTIME_START": {
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
      validateTransition(state.phase, BroadcastPhase.IDLE);
      return {
        ...initialState,
        phase: BroadcastPhase.IDLE,
      };
    }

    case "SKIP_CLIP": {
      if (state.phase === BroadcastPhase.PRE_PLAY) {
        return {
          ...state,
          phase: BroadcastPhase.PLAY_EXEC,
          activeClip: null,
          currentCameraIndex: 0,
          overlays: [],
        };
      }
      if (state.phase === BroadcastPhase.POST_PLAY || state.phase === BroadcastPhase.REPLAY) {
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

interface BroadcastStore extends BroadcastState {
  dispatch: (event: BroadcastEvent) => void;
  setActiveClip: (clip: ClipCue | null) => void;
  nextCameraShot: () => void;
  setCameraIndex: (index: number) => void;
  addOverlay: (overlay: OverlayCue) => void;
  removeOverlay: (overlayId: string) => void;
  clearOverlays: () => void;
  enqueueClip: (clip: ClipCue) => void;
  dequeueClip: () => ClipCue | undefined;
  clearClipQueue: () => void;
  setReducedMotion: (enabled: boolean) => void;
  reset: () => void;
  _debugSetPhase: (phase: BroadcastPhase) => void;
}

export const useBroadcastStore = create<BroadcastStore>((set, get) => ({
  ...initialState,

  dispatch: (event: BroadcastEvent) => {
    set((state) => broadcastReducer(state, event));
  },

  setActiveClip: (clip: ClipCue | null) => {
    set({
      activeClip: clip,
      currentCameraIndex: 0,
    });
  },

  nextCameraShot: () => {
    const { activeClip, currentCameraIndex } = get();
    if (!activeClip) return;

    const nextIndex = currentCameraIndex + 1;
    if (nextIndex < activeClip.cameras.length) {
      set({ currentCameraIndex: nextIndex });
    }
  },

  setCameraIndex: (index: number) => {
    const { activeClip } = get();
    if (!activeClip) return;

    const clampedIndex = Math.max(0, Math.min(index, activeClip.cameras.length - 1));
    set({ currentCameraIndex: clampedIndex });
  },

  addOverlay: (overlay: OverlayCue) => {
    set((state) => ({
      overlays: [...state.overlays, overlay],
    }));
  },

  removeOverlay: (overlayId: string) => {
    set((state) => ({
      overlays: state.overlays.filter((o) => o.id !== overlayId),
    }));
  },

  clearOverlays: () => {
    set({ overlays: [] });
  },

  enqueueClip: (clip: ClipCue) => {
    set((state) => ({
      clipQueue: [...state.clipQueue, clip],
    }));
  },

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

  clearClipQueue: () => {
    set({ clipQueue: [] });
  },

  setReducedMotion: (enabled: boolean) => {
    set({ reducedMotion: enabled });
  },

  reset: () => {
    set(initialState);
  },

  _debugSetPhase: (phase: BroadcastPhase) => {
    console.warn(`[BroadcastStore] Debug phase set: ${phase}`);
    set({ phase });
  },
}));

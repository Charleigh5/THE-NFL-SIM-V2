import { create } from "zustand";
import type { BroadcastStyle, NarrationContextRequest, NarrationResponse } from "../types/narrator";
import { narratorApi } from "../services/narrator";

export const NARRATOR_PREFS_STORAGE_KEY = "nfl-sim-narrator-prefs";

export interface NarratorPreferences {
  enabled: boolean;
  autoNarrate: boolean;
  isMuted: boolean;
  style: BroadcastStyle;
}

const DEFAULT_PREFS: NarratorPreferences = {
  enabled: true,
  autoNarrate: false,
  isMuted: false,
  style: "ESPN",
};

const loadStoredPrefs = (): NarratorPreferences => {
  if (typeof window === "undefined") {
    return DEFAULT_PREFS;
  }
  try {
    const raw = window.localStorage.getItem(NARRATOR_PREFS_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw) as Partial<NarratorPreferences>;
      return {
        enabled: typeof parsed.enabled === "boolean" ? parsed.enabled : DEFAULT_PREFS.enabled,
        autoNarrate:
          typeof parsed.autoNarrate === "boolean" ? parsed.autoNarrate : DEFAULT_PREFS.autoNarrate,
        isMuted: typeof parsed.isMuted === "boolean" ? parsed.isMuted : DEFAULT_PREFS.isMuted,
        style:
          parsed.style === "ESPN" ||
          parsed.style === "CBS" ||
          parsed.style === "FOX" ||
          parsed.style === "NFL_NETWORK"
            ? parsed.style
            : DEFAULT_PREFS.style,
      };
    }
  } catch {
    // Ignore storage read errors
  }
  return DEFAULT_PREFS;
};

const saveStoredPrefs = (prefs: NarratorPreferences): void => {
  if (typeof window === "undefined") {
    return;
  }
  try {
    window.localStorage.setItem(NARRATOR_PREFS_STORAGE_KEY, JSON.stringify(prefs));
  } catch {
    // Ignore storage write errors
  }
};

export interface NarratorStoreState extends NarratorPreferences {
  isLoading: boolean;
  isSpeaking: boolean;
  currentNarration: NarrationResponse | null;
  voiceSource: "voicestudio" | "browser";
  degraded: boolean;
  needsUserGesture: boolean;
  error: string | null;
  requestId: number;
  abortController: AbortController | null;
  setEnabled: (enabled: boolean) => void;
  setAutoNarrate: (autoNarrate: boolean) => void;
  setMuted: (isMuted: boolean) => void;
  toggleMute: () => void;
  setStyle: (style: BroadcastStyle) => void;
  setSpeaking: (isSpeaking: boolean) => void;
  setNeedsUserGesture: (needsUserGesture: boolean) => void;
  cancelActiveRequest: () => void;
  requestNarration: (
    request: Omit<NarrationContextRequest, "style"> & { style?: BroadcastStyle }
  ) => Promise<NarrationResponse | null>;
}

const initialPrefs = loadStoredPrefs();

export const useNarratorStore = create<NarratorStoreState>((set, get) => ({
  ...initialPrefs,
  isLoading: false,
  isSpeaking: false,
  currentNarration: null,
  voiceSource: "browser",
  degraded: false,
  needsUserGesture: false,
  error: null,
  requestId: 0,
  abortController: null,

  setEnabled: (enabled: boolean) => {
    const state = get();
    saveStoredPrefs({
      enabled,
      autoNarrate: state.autoNarrate,
      isMuted: state.isMuted,
      style: state.style,
    });
    if (!enabled) {
      state.cancelActiveRequest();
    }
    set({ enabled });
  },

  setAutoNarrate: (autoNarrate: boolean) => {
    const state = get();
    saveStoredPrefs({
      enabled: state.enabled,
      autoNarrate,
      isMuted: state.isMuted,
      style: state.style,
    });
    set({ autoNarrate });
  },

  setMuted: (isMuted: boolean) => {
    const state = get();
    saveStoredPrefs({
      enabled: state.enabled,
      autoNarrate: state.autoNarrate,
      isMuted,
      style: state.style,
    });
    set({ isMuted });
  },

  toggleMute: () => {
    const nextMuted = !get().isMuted;
    get().setMuted(nextMuted);
  },

  setStyle: (style: BroadcastStyle) => {
    const state = get();
    saveStoredPrefs({
      enabled: state.enabled,
      autoNarrate: state.autoNarrate,
      isMuted: state.isMuted,
      style,
    });
    set({ style });
  },

  setSpeaking: (isSpeaking: boolean) => set({ isSpeaking }),

  setNeedsUserGesture: (needsUserGesture: boolean) => set({ needsUserGesture }),

  cancelActiveRequest: () => {
    const currentAbort = get().abortController;
    if (currentAbort) {
      currentAbort.abort();
    }
    set((s) => ({
      abortController: null,
      isLoading: false,
      isSpeaking: false,
      requestId: s.requestId + 1,
    }));
  },

  requestNarration: async (req) => {
    const prevAbort = get().abortController;
    if (prevAbort) {
      prevAbort.abort();
    }

    const controller = new AbortController();
    const nextRequestId = get().requestId + 1;
    const chosenStyle = req.style ?? get().style;

    set({
      isLoading: true,
      error: null,
      requestId: nextRequestId,
      abortController: controller,
    });

    try {
      const response = await narratorApi.narrateScreen(
        {
          page: req.page,
          team_id: req.team_id,
          player_id: req.player_id ?? null,
          game_id: req.game_id ?? null,
          style: chosenStyle,
        },
        controller.signal
      );

      if (get().requestId !== nextRequestId) {
        return null;
      }

      set({
        isLoading: false,
        currentNarration: response,
        voiceSource: response.voice_source,
        degraded: response.degraded,
        abortController: null,
      });
      return response;
    } catch (err: unknown) {
      if (controller.signal.aborted || get().requestId !== nextRequestId) {
        return null;
      }
      const message = err instanceof Error ? err.message : "Narration unavailable";
      set({
        isLoading: false,
        error: message,
        abortController: null,
      });
      return null;
    }
  },
}));

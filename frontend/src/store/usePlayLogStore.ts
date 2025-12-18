/**
 * Play Log Store
 *
 * Sliced store for play history.
 * Extracted from useSimulationStore for single responsibility.
 */

import { create } from "zustand";
import type { PlayResult } from "../types/simulation";

interface PlayLogStore {
  // State
  plays: PlayResult[];
  maxPlays: number;

  // Actions
  addPlay: (play: PlayResult) => void;
  clearPlays: () => void;
  getRecentPlays: (count: number) => PlayResult[];
}

export const usePlayLogStore = create<PlayLogStore>((set, get) => ({
  plays: [],
  maxPlays: 100, // Limit stored plays to prevent memory issues

  addPlay: (play) =>
    set((state) => {
      const newPlays = [play, ...state.plays];
      // Trim to maxPlays
      if (newPlays.length > state.maxPlays) {
        return { plays: newPlays.slice(0, state.maxPlays) };
      }
      return { plays: newPlays };
    }),

  clearPlays: () => set({ plays: [] }),

  getRecentPlays: (count) => {
    const { plays } = get();
    return plays.slice(0, count);
  },
}));

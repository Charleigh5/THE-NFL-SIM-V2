/**
 * Scoreboard Store
 *
 * Sliced store for scoreboard-related state.
 * Extracted from useSimulationStore for single responsibility.
 */

import { create } from "zustand";
import { MomentumState } from "../types/momentum";

export interface ScoreboardState {
  // Scores
  homeScore: number;
  awayScore: number;

  // Clock
  quarter: number;
  timeLeft: string;
  clockStrategy?: string;

  // Possession
  possession: "home" | "away";
  down: number;
  distance: number;
  yardLine: number;

  // Timeouts
  homeTimeouts: number;
  awayTimeouts: number;

  // Momentum
  homeMomentum: MomentumState;
  awayMomentum: MomentumState;
}

interface ScoreboardStore extends ScoreboardState {
  // Actions
  updateScore: (team: "home" | "away", points: number) => void;
  updateClock: (timeLeft: string, quarter?: number) => void;
  updatePossession: (data: {
    possession?: "home" | "away";
    down?: number;
    distance?: number;
    yardLine?: number;
  }) => void;
  useTimeout: (team: "home" | "away") => boolean;
  updateMomentum: (home: MomentumState, away: MomentumState) => void;
  setClockStrategy: (strategy: string) => void;
  updateFromServer: (state: Partial<ScoreboardState>) => void;
  reset: () => void;
}

const initialState: ScoreboardState = {
  homeScore: 0,
  awayScore: 0,
  quarter: 1,
  timeLeft: "15:00",
  possession: "home",
  down: 1,
  distance: 10,
  yardLine: 25,
  homeTimeouts: 3,
  awayTimeouts: 3,
  homeMomentum: MomentumState.NEUTRAL,
  awayMomentum: MomentumState.NEUTRAL,
};

export const useScoreboardStore = create<ScoreboardStore>((set, get) => ({
  ...initialState,

  updateScore: (team, points) =>
    set((state) => ({
      homeScore: team === "home" ? state.homeScore + points : state.homeScore,
      awayScore: team === "away" ? state.awayScore + points : state.awayScore,
    })),

  updateClock: (timeLeft, quarter) =>
    set((state) => ({
      timeLeft,
      quarter: quarter ?? state.quarter,
    })),

  updatePossession: (data) =>
    set((state) => ({
      possession: data.possession ?? state.possession,
      down: data.down ?? state.down,
      distance: data.distance ?? state.distance,
      yardLine: data.yardLine ?? state.yardLine,
    })),

  useTimeout: (team) => {
    const state = get();
    const key = team === "home" ? "homeTimeouts" : "awayTimeouts";
    if (state[key] > 0) {
      set({ [key]: state[key] - 1 });
      return true;
    }
    return false;
  },

  updateMomentum: (home, away) =>
    set({
      homeMomentum: home,
      awayMomentum: away,
    }),

  setClockStrategy: (strategy) => set({ clockStrategy: strategy }),

  updateFromServer: (serverState) =>
    set((state) => ({
      ...state,
      ...serverState,
    })),

  reset: () => set(initialState),
}));

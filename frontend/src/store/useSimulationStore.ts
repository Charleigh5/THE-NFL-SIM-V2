import { create } from "zustand";
import type { PlayResult } from "../types/simulation";

interface GameState {
  homeScore: number;
  awayScore: number;
  quarter: number;
  timeLeft: string; // e.g., "15:00"
  possession: "home" | "away";
  down: number;
  distance: number;
  yardLine: number; // 0-100
}

interface SimulationStore {
  // State
  gameId: string | null;
  gameState: GameState;
  playLog: PlayResult[];
  isLive: boolean;
  engineData: {
    genesis: Record<string, unknown>;
    empire: Record<string, unknown>;
    hive: Record<string, unknown>;
    society: Record<string, unknown>;
    rpg: Record<string, unknown>;
  };

  // Actions
  setGameId: (id: string) => void;
  updateGameState: (state: Partial<GameState>) => void;
  addPlay: (play: PlayResult) => void;
  setLiveStatus: (status: boolean) => void;
  updateEngineData: (
    engine: keyof SimulationStore["engineData"],
    data: Record<string, unknown>
  ) => void;
  resetSimulation: () => void;
}

export const useSimulationStore = create<SimulationStore>((set) => ({
  gameId: null,
  gameState: {
    homeScore: 0,
    awayScore: 0,
    quarter: 1,
    timeLeft: "15:00",
    possession: "home",
    down: 1,
    distance: 10,
    yardLine: 25,
  },
  playLog: [],
  isLive: false,
  engineData: {
    genesis: {},
    empire: {},
    hive: {},
    society: {},
    rpg: {},
  },

  setGameId: (id) => set({ gameId: id }),
  updateGameState: (newState) =>
    set((state) => ({
      gameState: { ...state.gameState, ...newState },
    })),
  addPlay: (play) =>
    set((state) => ({
      playLog: [play, ...state.playLog],
    })),
  setLiveStatus: (status) => set({ isLive: status }),
  updateEngineData: (engine, data) =>
    set((state) => ({
      engineData: { ...state.engineData, [engine]: data },
    })),
  resetSimulation: () =>
    set({
      gameId: null,
      gameState: {
        homeScore: 0,
        awayScore: 0,
        quarter: 1,
        timeLeft: "15:00",
        possession: "home",
        down: 1,
        distance: 10,
        yardLine: 25,
      },
      playLog: [],
      isLive: false,
      engineData: {
        genesis: {},
        empire: {},
        hive: {},
        society: {},
        rpg: {},
      },
    }),
}));

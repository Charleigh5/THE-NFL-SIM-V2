import { api } from "./api";
import type { PlayResult } from "../types/simulation";

export interface SimulationStatus {
  isRunning: boolean;
  currentQuarter: number;
  timeLeft: string;
  homeScore: number;
  awayScore: number;
  possession: "home" | "away";
  down: number;
  distance: number;
  yardLine: number;
}

export const simulationService = {
  startSimulation: async () => {
    const response = await api.post<PlayResult>("/api/simulation/start", {});
    return response.data;
  },

  startLiveSimulation: async (numPlays: number = 100) => {
    const response = await api.post("/api/simulation/start-live", {
      num_plays: numPlays,
    });
    return response.data;
  },

  stopSimulation: async () => {
    const response = await api.post("/api/simulation/stop");
    return response.data;
  },

  getSimulationStatus: async () => {
    const response = await api.get<SimulationStatus>("/api/simulation/status");
    return response.data;
  },

  getPlayByPlay: async (gameId: string) => {
    const response = await api.get<PlayResult[]>(`/api/simulation/${gameId}/plays`);
    return response.data;
  },
};

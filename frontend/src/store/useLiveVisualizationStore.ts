import { create } from "zustand";
import type { TeamVisualData, FormationData } from "../types/broadcast";

interface LiveVisualizationStore {
  // State
  gameId: number | null;
  isConnected: boolean;
  homeTeam: TeamVisualData | null;
  awayTeam: TeamVisualData | null;
  currentFormation: FormationData | null;
  wsError: string | null;

  // Actions
  setGameId: (id: number) => void;
  setConnectionStatus: (connected: boolean) => void;
  setTeams: (home: TeamVisualData, away: TeamVisualData) => void;
  setFormation: (formation: FormationData) => void;
  setWsError: (error: string | null) => void;
  fetchRoster: (gameId: number) => Promise<void>;
  fetchFormation: (gameId: number, playId: number) => Promise<void>;
  connectWebSocket: (gameId: number) => WebSocket;
  reset: () => void;
}

export const useLiveVisualizationStore = create<LiveVisualizationStore>((set) => ({
  gameId: null,
  isConnected: false,
  homeTeam: null,
  awayTeam: null,
  currentFormation: null,
  wsError: null,

  setGameId: (id) => set({ gameId: id }),

  setConnectionStatus: (connected) => set({ isConnected: connected }),

  setTeams: (home, away) => set({ homeTeam: home, awayTeam: away }),

  setFormation: (formation) => set({ currentFormation: formation }),

  setWsError: (error) => set({ wsError: error }),

  fetchRoster: async (gameId: number) => {
    try {
      const response = await fetch(`/api/live/game/${gameId}/roster`);
      if (!response.ok) throw new Error("Failed to fetch roster");

      const data = await response.json();
      set({
        homeTeam: data.home_team,
        awayTeam: data.away_team,
        gameId: data.game_id,
      });
    } catch (error) {
      set({ wsError: error instanceof Error ? error.message : "Unknown error" });
      throw error;
    }
  },

  fetchFormation: async (gameId: number, playId: number) => {
    try {
      const response = await fetch(`/api/live/game/${gameId}/formation/${playId}`);
      if (!response.ok) throw new Error("Failed to fetch formation");

      const data = await response.json();
      set({ currentFormation: data });
    } catch (error) {
      console.error("Formation fetch error:", error);
    }
  },

  connectWebSocket: (gameId: number) => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/api/live/ws/game/${gameId}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      set({ isConnected: true, wsError: null });
      console.log("3D Visualization WebSocket connected");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("3D Live WS Message:", data);
      } catch (err) {
        console.warn("Invalid WS message:", err);
      }
    };

    ws.onclose = () => {
      set({ isConnected: false });
      console.log("3D Visualization WebSocket disconnected");
    };

    ws.onerror = (error) => {
      set({ wsError: "WebSocket connection error" });
      console.error("WebSocket error:", error);
    };

    return ws;
  },

  reset: () =>
    set({
      gameId: null,
      isConnected: false,
      homeTeam: null,
      awayTeam: null,
      currentFormation: null,
      wsError: null,
    }),
}));

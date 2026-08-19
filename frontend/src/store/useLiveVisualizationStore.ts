import { create } from "zustand";

export interface PlayerVisualData {
  id: number;
  name: string;
  number: number;
  position: string;
  position_group: "offense" | "defense" | "special_teams";
  height: number;
  weight: number;
  visuals: {
    body_type: "large" | "medium" | "lean" | "athletic" | "pocket" | "muscular";
    jersey_color_primary: string;
    jersey_color_secondary: string;
    helmet_design: {
      base: string;
      stripe: string;
      logo_side: boolean;
      facemask: string;
    };
    face_mask_color: string;
    cleat_color: string;
    accessories: string[];
  };
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

export interface FormationData {
  play_id: number;
  formation: {
    offense: {
      name: string;
      players: Array<{ position: string; x: number; y: number; z: number }>;
    };
    defense: {
      name: string;
      players: Array<{ position: string; x: number; y: number; z: number }>;
    };
  };
}

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

export const useLiveVisualizationStore = create<LiveVisualizationStore>((set, get) => ({
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
      console.log("WebSocket connected");
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Handle real-time updates (camera sync, etc.)
      console.log("WS Message:", data);
    };
    
    ws.onclose = () => {
      set({ isConnected: false });
      console.log("WebSocket disconnected");
    };
    
    ws.onerror = (error) => {
      set({ wsError: "WebSocket connection error" });
      console.error("WebSocket error:", error);
    };
    
    return ws;
  },

  reset: () => set({
    gameId: null,
    isConnected: false,
    homeTeam: null,
    awayTeam: null,
    currentFormation: null,
    wsError: null,
  }),
}));

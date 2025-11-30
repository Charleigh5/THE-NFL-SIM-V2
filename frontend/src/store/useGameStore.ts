import { create } from "zustand";

interface GameState {
  isConnected: boolean;
  setIsConnected: (status: boolean) => void;
}

export const useGameStore = create<GameState>((set) => ({
  isConnected: false,
  setIsConnected: (status) => set({ isConnected: status }),
}));

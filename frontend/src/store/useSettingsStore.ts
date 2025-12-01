import { create } from "zustand";
import { api } from "../services/api";

interface SettingsState {
  userTeamId: number | null;
  difficultyLevel: string;
  isLoading: boolean;
  fetchSettings: () => Promise<void>;
  setUserTeam: (teamId: number) => Promise<void>;
  setDifficulty: (level: string) => Promise<void>;
}

export const useSettingsStore = create<SettingsState>((set) => ({
  userTeamId: null,
  difficultyLevel: "All-Pro",
  isLoading: false,

  fetchSettings: async () => {
    set({ isLoading: true });
    try {
      const response = await api.get("/api/settings");
      set({
        userTeamId: response.data.user_team_id,
        difficultyLevel: response.data.difficulty_level,
        isLoading: false,
      });
    } catch (error) {
      console.error("Failed to fetch settings:", error);
      set({ isLoading: false });
    }
  },

  setUserTeam: async (teamId: number) => {
    try {
      await api.put("/api/settings", { user_team_id: teamId });
      set({ userTeamId: teamId });
    } catch (error) {
      console.error("Failed to update user team:", error);
    }
  },

  setDifficulty: async (level: string) => {
    try {
      await api.put("/api/settings", { difficulty_level: level });
      set({ difficultyLevel: level });
    } catch (error) {
      console.error("Failed to update difficulty:", error);
    }
  },
}));

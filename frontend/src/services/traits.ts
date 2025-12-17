import { api } from "./api";
import type { Trait, TraitUnlockRequest } from "../types/trait";

export const traitsApi = {
  // Get all available traits in the system
  getAllTraits: async (): Promise<Trait[]> => {
    const response = await api.get<Trait[]>("/api/traits/");
    return response.data;
  },

  // Get traits for a specific player
  getPlayerTraits: async (playerId: number): Promise<Trait[]> => {
    // Note: Backend currently returns List[Trait]
    const response = await api.get<Trait[]>(`/api/traits/players/${playerId}`);
    return response.data;
  },

  // Unlock a trait for a player
  unlockTrait: async (playerId: number, traitName: string): Promise<boolean> => {
    const req: TraitUnlockRequest = { trait_name: traitName };
    // Assuming backend endpoint follows this signature
    const response = await api.post<boolean>(`/api/traits/players/${playerId}/unlock`, req);
    return response.data;
  },
};

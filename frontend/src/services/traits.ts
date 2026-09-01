import { apiClient } from "./api";
import type { Trait, PlayerTrait, TraitAssignment, TraitUnlockRequest } from "../types/trait";

/**
 * Unified Trait API Service
 * Consolidates traitsApi and traitService into a single canonical module
 */
export const traitsApi = {
  // Get all available traits in the system
  getAllTraits: async (): Promise<Trait[]> => {
    const response = await apiClient.get<Trait[]>("/api/traits/");
    return response.data;
  },

  // Get traits for a specific player
  getPlayerTraits: async (playerId: number): Promise<Trait[]> => {
    const response = await apiClient.get<Trait[]>(`/api/traits/players/${playerId}`);
    return response.data;
  },

  // Unlock a trait for a player
  unlockTrait: async (playerId: number, traitName: string): Promise<boolean> => {
    const req: TraitUnlockRequest = { trait_name: traitName };
    const response = await apiClient.post<boolean>(`/api/traits/players/${playerId}/unlock`, req);
    return response.data;
  },

  // Assign a trait to a player
  assignTrait: async (playerId: number, assignment: TraitAssignment): Promise<PlayerTrait> => {
    const response = await apiClient.post<PlayerTrait>(
      `/api/traits/players/${playerId}`,
      assignment
    );
    return response.data;
  },
};

export class TraitService {
  async getAllTraits(): Promise<Trait[]> {
    return traitsApi.getAllTraits();
  }

  async getPlayerTraits(playerId: number): Promise<Trait[]> {
    return traitsApi.getPlayerTraits(playerId);
  }

  async unlockTrait(playerId: number, traitName: string): Promise<boolean> {
    return traitsApi.unlockTrait(playerId, traitName);
  }

  async assignTrait(playerId: number, assignment: TraitAssignment): Promise<PlayerTrait> {
    return traitsApi.assignTrait(playerId, assignment);
  }
}

export const traitService = new TraitService();
export default traitsApi;

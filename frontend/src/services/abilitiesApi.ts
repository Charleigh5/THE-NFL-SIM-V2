import { apiClient } from "./api";
import type {
  AbilityDefinition,
  PlayerAbilityStatus,
  UnlockAbilityResponse,
  PreSnapInsightRequest,
  PreSnapInsightResponse,
} from "../types/ability";

export const abilitiesApi = {
  /**
   * Fetch the full catalog of RPG abilities.
   */
  async getCatalog(): Promise<AbilityDefinition[]> {
    const response = await apiClient.get<AbilityDefinition[]>("/abilities/catalog");
    return response.data;
  },

  /**
   * Fetch unlock and eligibility status of all abilities for a player.
   */
  async getPlayerAbilityStatus(playerId: number): Promise<Record<string, PlayerAbilityStatus>> {
    const response = await apiClient.get<Record<string, PlayerAbilityStatus>>(
      `/abilities/players/${playerId}`
    );
    return response.data;
  },

  /**
   * Fetch list of unlocked abilities for a player.
   */
  async getPlayerUnlockedAbilities(playerId: number): Promise<AbilityDefinition[]> {
    const response = await apiClient.get<AbilityDefinition[]>(
      `/abilities/players/${playerId}/unlocked`
    );
    return response.data;
  },

  /**
   * Unlock an ability for a player using XP.
   */
  async unlockAbility(playerId: number, abilityKey: string): Promise<UnlockAbilityResponse> {
    const response = await apiClient.post<UnlockAbilityResponse>(
      `/abilities/players/${playerId}/unlock`,
      { ability_key: abilityKey }
    );
    return response.data;
  },

  /**
   * Execute Pre-Snap Read insight simulation (The Read mechanic).
   */
  async getPreSnapInsight(request: PreSnapInsightRequest): Promise<PreSnapInsightResponse> {
    const response = await apiClient.post<PreSnapInsightResponse>(
      "/abilities/match/insight",
      request
    );
    return response.data;
  },
};

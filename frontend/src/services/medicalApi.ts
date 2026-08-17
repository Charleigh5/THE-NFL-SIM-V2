import { apiClient } from "./api";
import type {
  BodyHealth,
  BioMetrics,
  FatigueState,
  TreatmentDecisionRequest,
  TreatmentDecisionResponse,
  InjuredPlayer,
  SurgeryRisk,
} from "../types/medical";

export const medicalApi = {
  /**
   * Fetch 7-zone body health for a player.
   */
  async getPlayerHealth(playerId: number): Promise<BodyHealth> {
    const response = await apiClient.get<BodyHealth>(`/api/medical/player/${playerId}`);
    return response.data;
  },

  /**
   * Fetch GENESIS biological metrics for a player.
   */
  async getPlayerBioMetrics(playerId: number, temperatureF: number = 72.0): Promise<BioMetrics> {
    const response = await apiClient.get<BioMetrics>(
      `/api/genesis/player/${playerId}/bio-metrics`,
      { params: { temperature_f: temperatureF } }
    );
    return response.data;
  },

  /**
   * Fetch fatigue state and biological recovery metrics for a player.
   */
  async getPlayerFatigue(playerId: number): Promise<FatigueState> {
    const response = await apiClient.get<FatigueState>(`/api/genesis/player/${playerId}/fatigue`);
    return response.data;
  },

  /**
   * Apply medical treatment decision (REST, SURGERY, PLAY_THROUGH).
   */
  async applyTreatment(request: TreatmentDecisionRequest): Promise<TreatmentDecisionResponse> {
    const response = await apiClient.post<TreatmentDecisionResponse>(
      "/api/medical/treatment",
      request
    );
    return response.data;
  },

  /**
   * Fetch all injured players for a given team.
   */
  async getTeamInjuries(teamId: number): Promise<InjuredPlayer[]> {
    const response = await apiClient.get<InjuredPlayer[]>(`/api/medical/team/${teamId}/injuries`);
    return response.data;
  },

  /**
   * Calculate surgery risk for an injured player.
   */
  async getSurgeryRisk(playerId: number): Promise<SurgeryRisk> {
    const response = await apiClient.get<SurgeryRisk>(`/api/medical/surgery-risk/${playerId}`);
    return response.data;
  },
};

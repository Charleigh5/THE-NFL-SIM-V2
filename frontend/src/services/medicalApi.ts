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
import type {
  MedicalProtocolType,
  OrthopedicProtocolOption,
  TriageDecisionResult,
} from "../types/deepDive";

export interface InjuryDiagnosis {
  injury_type?: string;
  severity: number;
  weeks_to_recovery: number;
  body_zone: string;
  current_integrity: number;
}

export interface TriageProtocolsResponse {
  player_id: number;
  current_diagnosis: InjuryDiagnosis;
  protocols: OrthopedicProtocolOption[];
}

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

  /**
   * Fetch available 5-pathway orthopedic triage protocols for an injured player.
   */
  async getPlayerTriageProtocols(playerId: number): Promise<TriageProtocolsResponse> {
    const response = await apiClient.get<TriageProtocolsResponse>(
      `/api/medical/players/${playerId}/triage/protocols`
    );
    return response.data;
  },

  /**
   * Apply an orthopedic triage protocol (REST, PRP_THERAPY, ARTHROSCOPIC_SURGERY, RECONSTRUCTIVE_SURGERY, CORTISONE_STABILIZATION).
   */
  async applyOrthopedicTriage(
    playerId: number,
    protocol: MedicalProtocolType | string,
    zoneKey?: string
  ): Promise<TriageDecisionResult> {
    const response = await apiClient.post<TriageDecisionResult>(
      `/api/medical/players/${playerId}/triage/apply`,
      { protocol, zone_key: zoneKey }
    );
    return response.data;
  },
};

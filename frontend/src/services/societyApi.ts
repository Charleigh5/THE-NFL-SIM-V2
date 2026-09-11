import { api } from "./api";
import type {
  PsychologicalDNA,
  LockerRoomEventResponse,
  LockerRoomResolutionRequest,
  LockerRoomResolutionResponse,
} from "../types/society";

export interface SocietyPlayerDetail {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  tension_score?: number;
  morale?: number;
  trust_in_coach?: number;
  trust_in_qb?: number;
  psychological_dna?: PsychologicalDNA;
}

/**
 * Society & Locker Room API Client
 * Interfaces with /api/society endpoints in backend/app/api/endpoints/society.py
 */
export const societyApi = {
  /**
   * Evaluates team locker room atmosphere.
   * If any player has tension >= 75.0, returns Tier 3 closed-door confrontation event.
   * Returns null if locker room is calm (<75.0 tension).
   */
  evaluateLockerRoom: async (
    teamId: number,
    week: number = 1
  ): Promise<LockerRoomEventResponse | null> => {
    try {
      // Backend router mounts @router.post("/teams/{team_id}/locker-room/evaluate")
      const response = await api.post<LockerRoomEventResponse | null>(
        `/api/society/teams/${teamId}/locker-room/evaluate?week=${week}`
      );
      return response.data;
    } catch (primaryErr: unknown) {
      // Robust fallback to GET if backend exposes both or is aliased
      try {
        const getRes = await api.get<LockerRoomEventResponse | null>(
          `/api/society/teams/${teamId}/locker-room/evaluate?week=${week}`
        );
        return getRes.data;
      } catch {
        throw primaryErr;
      }
    }
  },

  /**
   * Applies GM / Head Coach resolution choice to active closed-door incident.
   */
  resolveLockerRoom: async (
    teamId: number,
    request: LockerRoomResolutionRequest
  ): Promise<LockerRoomResolutionResponse> => {
    const payload: LockerRoomResolutionRequest = {
      team_id: teamId,
      action_id: request.action_id,
      week: request.week,
      active_actor_ids: request.active_actor_ids,
    };
    const response = await api.post<LockerRoomResolutionResponse>(
      `/api/society/teams/${teamId}/locker-room/resolve`,
      payload
    );
    return response.data;
  },

  /**
   * Retrieves Psychological DNA profile (ego, greed, loyalty, resilience, paranoia, professionalism)
   * for a specific player.
   */
  getPlayerPsychologicalDNA: async (playerId: number): Promise<PsychologicalDNA> => {
    const response = await api.get<PsychologicalDNA>(
      `/api/society/players/${playerId}/psychological-dna`
    );
    return response.data;
  },

  /**
   * Updates Psychological DNA profile for a specific player.
   */
  updatePlayerPsychologicalDNA: async (
    playerId: number,
    dna: PsychologicalDNA
  ): Promise<PsychologicalDNA> => {
    const response = await api.post<PsychologicalDNA>(
      `/api/society/players/${playerId}/psychological-dna`,
      dna
    );
    return response.data;
  },
};

export default societyApi;

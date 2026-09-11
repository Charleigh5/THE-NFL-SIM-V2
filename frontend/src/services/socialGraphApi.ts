/**
 * Social Graph & Media Leaks API Client
 * Connects frontend to backend Social Graph Engine endpoints.
 */

import { apiClient } from "./api";
import type {
  LockerRoomSocialNetworkResponse,
  HoldoutResolutionRequest,
} from "../types/socialGraph";

export const socialGraphApi = {
  /**
   * Fetches the 2D social network graph, cliques, and active media leaks for a team.
   */
  getSocialGraph: async (teamId: number): Promise<LockerRoomSocialNetworkResponse> => {
    const res = await apiClient.get<LockerRoomSocialNetworkResponse>(
      `/api/society/teams/${teamId}/social-graph`
    );
    return res.data;
  },

  /**
   * Submits GM action to resolve an active athlete holdout.
   */
  resolveHoldout: async (
    teamId: number,
    playerId: number,
    request: HoldoutResolutionRequest
  ): Promise<LockerRoomSocialNetworkResponse> => {
    const res = await apiClient.post<LockerRoomSocialNetworkResponse>(
      `/api/society/teams/${teamId}/holdouts/${playerId}/resolve`,
      request
    );
    return res.data;
  },

  /**
   * Triggers a simulated contract holdout for demonstration and testing.
   */
  seedHoldout: async (
    teamId: number,
    playerId: number
  ): Promise<LockerRoomSocialNetworkResponse> => {
    const res = await apiClient.post<LockerRoomSocialNetworkResponse>(
      `/api/society/teams/${teamId}/social-graph/seed-holdout/${playerId}`
    );
    return res.data;
  },
};

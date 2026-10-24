import { apiClient } from "./api";
import type { NarrationContextRequest, NarrationResponse } from "../types/narrator";

export interface VoiceHealthResponse {
  available: boolean;
  voice_source: "voicestudio" | "browser";
  model: string;
}

export const narratorApi = {
  narrateScreen: async (
    payload: NarrationContextRequest,
    signal?: AbortSignal
  ): Promise<NarrationResponse> => {
    const response = await apiClient.post<NarrationResponse>("/api/broadcast/narrate", payload, {
      signal,
    });
    return response.data;
  },

  getVoiceHealth: async (signal?: AbortSignal): Promise<VoiceHealthResponse> => {
    const response = await apiClient.get<VoiceHealthResponse>("/api/broadcast/voices/health", {
      signal,
    });
    return response.data;
  },

  getAudioUrl: (audioPathOrCacheKey: string): string => {
    const baseUrl = (apiClient.defaults.baseURL || "http://localhost:8000").replace(/\/$/, "");
    if (audioPathOrCacheKey.startsWith("http://") || audioPathOrCacheKey.startsWith("https://")) {
      return audioPathOrCacheKey;
    }
    if (audioPathOrCacheKey.startsWith("/")) {
      return `${baseUrl}${audioPathOrCacheKey}`;
    }
    return `${baseUrl}/api/broadcast/audio/${audioPathOrCacheKey}`;
  },
};

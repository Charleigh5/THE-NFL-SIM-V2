import { apiClient } from "./api";

export interface ProviderStatus {
  provider_name: string;
  is_authenticated: boolean;
  masked_key: string | null;
  description: string;
  last_sync_timestamp: string | null;
  available_features: string[];
}

export interface SyncTransferItem {
  player_id: number;
  player_name: string;
  position: string;
  from_team: string;
  to_team: string;
}

export interface SyncDepthItem {
  player_id: number;
  player_name: string;
  position: string;
  team: string;
  old_rank: number;
  new_rank: number;
}

export interface SyncInjuryItem {
  player_id: number;
  player_name: string;
  team: string;
  status: string;
  injury_type: string | null;
}

export interface SyncResult {
  provider: string;
  timestamp: string;
  dry_run: boolean;
  transfers_count: number;
  depth_updates_count: number;
  injuries_count: number;
  unmatched_count: number;
  transfers: SyncTransferItem[];
  depth_updates: SyncDepthItem[];
  injuries: SyncInjuryItem[];
  unmatched: string[];
  message: string;
}

export interface ProviderOption {
  id: string;
  name: string;
  configured: boolean;
  cost: string;
  description: string;
}

export interface ProvidersListResponse {
  current_configured_mode: string;
  providers: ProviderOption[];
}

export const rosterSyncApi = {
  /**
   * Fetch current roster provider connection and authentication health.
   */
  getStatus: async (provider?: string): Promise<ProviderStatus> => {
    const params = provider ? { provider } : {};
    const res = await apiClient.get<ProviderStatus>("/api/roster-sync/status", { params });
    return res.data;
  },

  /**
   * List available external providers and their configuration status.
   */
  getProviders: async (): Promise<ProvidersListResponse> => {
    const res = await apiClient.get<ProvidersListResponse>("/api/roster-sync/providers");
    return res.data;
  },

  /**
   * Execute real-time roster synchronization (live update or dry-run preview).
   */
  executeSync: async (dryRun: boolean = false, provider?: string): Promise<SyncResult> => {
    const params: { dry_run: boolean; provider?: string } = { dry_run: dryRun };
    if (provider) {
      params.provider = provider;
    }

    const res = await apiClient.post<SyncResult>("/api/roster-sync/execute", null, { params });
    return res.data;
  },
};

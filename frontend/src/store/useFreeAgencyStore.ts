import { create } from "zustand";
import { useShallow } from "zustand/react/shallow";
import type {
  FreeAgentMarketPlayer,
  FreeAgentBidResponse,
  FreeAgentBidRequest,
} from "../types/offseason";
import type { Team } from "../services/api";
import { api } from "../services/api";
import {
  createInitialEntityState,
  createEntitySliceActions,
} from "./slices/createEntitySlice";
import type { EntityState, EntitySliceActions } from "../types/entityState";
import {
  computeFilteredPlayers,
  type PositionFilter,
  type TierFilter,
} from "../utils/filterFreeAgents";

export type { PositionFilter, TierFilter };
export { computeFilteredPlayers };

export interface FreeAgencyStoreState {
  // Normalized Entity State
  players: EntityState<FreeAgentMarketPlayer, number>;
  playerActions: EntitySliceActions<FreeAgentMarketPlayer, number>;
  filteredPlayers: FreeAgentMarketPlayer[];

  // Team & Cap Context
  teamId: number;
  seasonId: number;
  team: Team | null;
  capSpace: number;

  // Filters
  positionFilter: PositionFilter;
  tierFilter: TierFilter;
  searchQuery: string;

  // Bidding Modal State
  selectedPlayerId: number | null;
  bidYears: number;
  bidTotalAmount: number;
  bidSigningBonus: number;
  bidGuaranteed: number;
  voidYears: number;
  postJune1: boolean;
  submittingBid: boolean;
  bidResponse: FreeAgentBidResponse | null;

  // Actions
  loadMarketData: (seasonId?: number, teamId?: number) => Promise<void>;
  setPositionFilter: (filter: PositionFilter) => void;
  setTierFilter: (filter: TierFilter) => void;
  setSearchQuery: (query: string) => void;
  openBidModal: (playerId: number) => void;
  closeBidModal: () => void;
  setBidYears: (years: number) => void;
  setBidTotalAmount: (amount: number) => void;
  setBidSigningBonus: (bonus: number) => void;
  setBidGuaranteed: (guaranteed: number) => void;
  setVoidYears: (years: number) => void;
  setPostJune1: (enabled: boolean) => void;
  submitBid: () => Promise<boolean>;
  removePlayer: (playerId: number) => void;
  updateCapSpace: (newCap: number) => void;
}


export const useFreeAgencyStore = create<FreeAgencyStoreState>((set, get) => {
  const entityActions = createEntitySliceActions<FreeAgentMarketPlayer, number>((updater) => {
    set((state) => ({
      players: {
        ...state.players,
        ...updater(state.players),
      },
    }));
  });

  return {
    players: createInitialEntityState<FreeAgentMarketPlayer, number>(),
    playerActions: entityActions,
    filteredPlayers: [],

    teamId: 1,
    seasonId: 1,
    team: null,
    capSpace: 15000000,

    positionFilter: "ALL",
    tierFilter: "ALL",
    searchQuery: "",

    selectedPlayerId: null,
    bidYears: 3,
    bidTotalAmount: 30000000,
    bidSigningBonus: 9000000,
    bidGuaranteed: 18000000,
    voidYears: 0,
    postJune1: false,
    submittingBid: false,
    bidResponse: null,

    loadMarketData: async (seasonId = 1, teamId = 1) => {
      set((state) => ({
        seasonId,
        teamId,
        players: { ...state.players, isLoading: true, error: null },
      }));

      try {
        // 1. Fetch team cap info
        try {
          const teamData = await api.getTeam(teamId);
          set({
            team: teamData,
            capSpace: teamData.salary_cap_space ?? 15000000,
          });
        } catch (err: unknown) {
          console.warn("Failed to fetch team data for cap space:", err);
        }

        // 2. Fetch free agents
        const marketRes = await api.get<FreeAgentMarketPlayer[]>(
          `/api/seasons/${seasonId}/free-agency/market`
        );

        const marketPlayers = Array.isArray(marketRes.data) ? marketRes.data : [];
        entityActions.setAll(marketPlayers, (p) => p.player_id);

        // Apply initial filter
        const current = get();
        const { filteredIds, filteredPlayers } = computeFilteredPlayers(
          current.players.byId,
          current.players.allIds,
          current.positionFilter,
          current.tierFilter,
          current.searchQuery
        );
        entityActions.setFilterIds(filteredIds);
        set({ filteredPlayers });
      } catch (err: unknown) {
        console.error("Error fetching free agency market:", err);
        const msg =
          err instanceof Error ? err.message : "Failed to load free agency market players.";
        entityActions.setError(msg);
      }
    },

    setPositionFilter: (filter: PositionFilter) => {
      set({ positionFilter: filter });
      const current = get();
      const { filteredIds, filteredPlayers } = computeFilteredPlayers(
        current.players.byId,
        current.players.allIds,
        filter,
        current.tierFilter,
        current.searchQuery
      );
      entityActions.setFilterIds(filteredIds);
      set({ filteredPlayers });
    },

    setTierFilter: (filter: TierFilter) => {
      set({ tierFilter: filter });
      const current = get();
      const { filteredIds, filteredPlayers } = computeFilteredPlayers(
        current.players.byId,
        current.players.allIds,
        current.positionFilter,
        filter,
        current.searchQuery
      );
      entityActions.setFilterIds(filteredIds);
      set({ filteredPlayers });
    },

    setSearchQuery: (query: string) => {
      set({ searchQuery: query });
      const current = get();
      const { filteredIds, filteredPlayers } = computeFilteredPlayers(
        current.players.byId,
        current.players.allIds,
        current.positionFilter,
        current.tierFilter,
        query
      );
      entityActions.setFilterIds(filteredIds);
      set({ filteredPlayers });
    },


    openBidModal: (playerId: number) => {
      const player = get().players.byId[playerId];
      if (!player) return;

      const projYears = Math.max(1, Math.min(5, player.projected_years || 3));
      const projAAV = player.projected_aav || 5000000;
      const total = projAAV * projYears;
      const bonus = Math.round(total * 0.3);
      const guaranteed = Math.round(total * 0.55);

      set({
        selectedPlayerId: playerId,
        bidResponse: null,
        voidYears: 0,
        postJune1: false,
        bidYears: projYears,
        bidTotalAmount: total,
        bidSigningBonus: bonus,
        bidGuaranteed: guaranteed,
      });
      entityActions.setSelectedId(playerId);
    },

    closeBidModal: () => {
      set({ selectedPlayerId: null, bidResponse: null });
      entityActions.setSelectedId(null);
    },

    setBidYears: (years: number) => set({ bidYears: years }),
    setBidTotalAmount: (amount: number) => set({ bidTotalAmount: amount }),
    setBidSigningBonus: (bonus: number) => set({ bidSigningBonus: bonus }),
    setBidGuaranteed: (guaranteed: number) => set({ bidGuaranteed: guaranteed }),
    setVoidYears: (years: number) => set({ voidYears: years }),
    setPostJune1: (enabled: boolean) => set({ postJune1: enabled }),

    submitBid: async () => {
      const state = get();
      const { selectedPlayerId, teamId, seasonId, bidYears, bidTotalAmount, bidSigningBonus, bidGuaranteed } = state;
      if (selectedPlayerId === null) return false;

      set({ submittingBid: true, bidResponse: null });

      const payload: FreeAgentBidRequest = {
        player_id: selectedPlayerId,
        team_id: teamId,
        years: bidYears,
        total_amount: bidTotalAmount,
        signing_bonus: bidSigningBonus,
        guaranteed_amount: bidGuaranteed,
      };

      try {
        const res = await api.post<FreeAgentBidResponse>(
          `/api/seasons/${seasonId}/free-agency/bid`,
          payload
        );

        set({ bidResponse: res.data });

        if (res.data.accepted) {
          set((state) => ({
            capSpace: res.data.updated_cap_space,
            filteredPlayers: state.filteredPlayers.filter(
              (p) => p.player_id !== selectedPlayerId
            ),
          }));
          // Atomically remove signed player from normalized dictionary
          entityActions.removeOne(selectedPlayerId);
        }
        return res.data.accepted;
      } catch (err: unknown) {
        console.error("Bid submission failed:", err);
        set({
          bidResponse: {
            status: "ERROR",
            accepted: false,
            message:
              err instanceof Error
                ? err.message
                : "Network error while submitting contract bid.",
            updated_cap_space: state.capSpace,
          },
        });
        return false;
      } finally {
        set({ submittingBid: false });
      }
    },

    removePlayer: (playerId: number) => {
      entityActions.removeOne(playerId);
      set((state) => ({
        filteredPlayers: state.filteredPlayers.filter((p) => p.player_id !== playerId),
      }));
    },

    updateCapSpace: (newCap: number) => {
      set({ capSpace: newCap });
    },
  };
});

/**
 * Granular shallow selectors for zero-cascade component re-renders
 */
export const useFilteredFreeAgents = () =>
  useFreeAgencyStore((state) => state.filteredPlayers);

export const useFilteredFreeAgentIds = () =>
  useFreeAgencyStore((state) => state.players.filterIds);

export const useFreeAgent = (playerId: number) =>
  useFreeAgencyStore((state) => state.players.byId[playerId]);

export const useSelectedFreeAgent = () =>
  useFreeAgencyStore((state) =>
    state.selectedPlayerId !== null ? state.players.byId[state.selectedPlayerId] : null
  );

export const useFreeAgencyMarketStatus = () =>
  useFreeAgencyStore(
    useShallow((state) => ({
      isLoading: state.players.isLoading,
      error: state.players.error,
      totalCount: state.players.allIds.length,
      filteredCount: state.players.filterIds.length,
      capSpace: state.capSpace,
      team: state.team,
    }))
  );

export const useFreeAgencyFilterState = () =>
  useFreeAgencyStore(
    useShallow((state) => ({
      positionFilter: state.positionFilter,
      tierFilter: state.tierFilter,
      searchQuery: state.searchQuery,
    }))
  );

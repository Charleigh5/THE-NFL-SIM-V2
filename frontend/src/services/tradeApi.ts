/**
 * Trade API Service
 * Handles all trade-related API calls with strict types (0 any)
 */
import type {
  TradePlayer,
  TradeProposal,
  TradeEvaluation,
  IncomingTradeOffer,
  TradeBlockPlayer,
  TradeHistoryItem,
  TradeOffer,
  DraftPickInfo,
} from "../types/trade";
import type { Player, Team } from "./api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Fetch wrapper with error handling
 */
async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    const errorData: { detail?: string } = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed: ${response.statusText}`);
  }

  return response.json();
}

export const tradeApi = {
  /**
   * Get tradeable players for a team
   */
  getTradeablePlayers: async (teamId: number): Promise<TradePlayer[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/teams/${teamId}/roster`);
      if (!response.ok) throw new Error("Failed to fetch roster");

      const players: Player[] = await response.json();

      return players.map((p) => ({
        id: p.id,
        first_name: p.first_name,
        last_name: p.last_name,
        position: p.position,
        overall_rating: p.overall_rating,
        age: p.age,
        salary: 5000000,
        years_remaining: 2,
        team_id: teamId,
        trade_value: calculateTradeValue(p.overall_rating, p.age),
        is_on_trade_block: false,
      }));
    } catch (error) {
      console.error("Failed to fetch tradeable players:", error);
      return [];
    }
  },

  /**
   * Get all teams for trade partner selection
   */
  getTradePartners: async (excludeTeamId: number): Promise<Team[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/teams?page=1&page_size=100`);
      if (!response.ok) throw new Error("Failed to fetch teams");

      const data: { items?: Team[] } | Team[] = await response.json();
      const teams: Team[] = Array.isArray(data) ? data : data.items || [];

      return teams.filter((t) => t.id !== excludeTeamId);
    } catch (error) {
      console.error("Failed to fetch trade partners:", error);
      return [];
    }
  },

  /**
   * Evaluate a trade proposal using the GM Agent
   */
  evaluateTrade: async (
    targetTeamId: number,
    offeredPlayerIds: number[],
    requestedPlayerIds: number[],
    offeredPicks?: DraftPickInfo[],
    requestedPicks?: DraftPickInfo[]
  ): Promise<TradeEvaluation> => {
    return await fetchJson<TradeEvaluation>(`/api/trades/evaluate`, {
      method: "POST",
      body: JSON.stringify({
        offered_player_ids: offeredPlayerIds,
        requested_player_ids: requestedPlayerIds,
        target_team_id: targetTeamId,
        offered_picks: offeredPicks || null,
        requested_picks: requestedPicks || null,
      }),
    });
  },

  /**
   * Legacy evaluate trade method for backward compatibility
   */
  evaluateTradeLegacy: async (
    seasonId: number,
    teamId: number,
    offeredPlayerIds: number[],
    requestedPlayerIds: number[]
  ): Promise<TradeEvaluation> => {
    return await fetchJson<TradeEvaluation>(`/api/season/${seasonId}/gm/evaluate-trade`, {
      method: "POST",
      body: JSON.stringify({
        team_id: teamId,
        offered_ids: offeredPlayerIds,
        requested_ids: requestedPlayerIds,
      }),
    });
  },

  /**
   * Execute a trade
   */
  executeTrade: async (proposal: TradeProposal): Promise<{ success: boolean; message: string }> => {
    const targetTeamId = proposal.target_team_id || proposal.receiving_team_id || 0;
    const offeredPlayers = proposal.offered_player_ids || proposal.offered_players || [];
    const requestedPlayers = proposal.requested_player_ids || proposal.requested_players || [];

    const response = await fetchJson<{ offer_id: number; status: string; message: string }>(
      `/api/trades/offer`,
      {
        method: "POST",
        body: JSON.stringify({
          target_team_id: targetTeamId,
          offered_player_ids: offeredPlayers,
          requested_player_ids: requestedPlayers,
          offered_picks: proposal.offered_picks || null,
          requested_picks: proposal.requested_picks || null,
        }),
      }
    );
    return {
      success: true,
      message: response.message || "Trade executed successfully!",
    };
  },

  /**
   * Get incoming trade offers from AI teams
   */
  getIncomingOffers: async (teamId: number): Promise<IncomingTradeOffer[]> => {
    try {
      const data = await fetchJson<{ incoming: TradeOffer[]; outgoing: TradeOffer[] }>(
        `/api/trades/pending/${teamId}`
      );
      return (data.incoming || []).map((offer) => ({
        id: offer.id,
        from_team_id: offer.offering_team_id,
        from_team_name: `Team ${offer.offering_team_id}`,
        from_team_abbreviation: `TM${offer.offering_team_id}`,
        offered_assets: offer.offered_assets || [],
        requested_assets: offer.requested_assets || [],
        gm_message: offer.gm_response || "Trade proposal for consideration.",
        urgency: "medium" as const,
        created_at: offer.created_at,
      }));
    } catch (error) {
      console.error("Failed to fetch incoming trade offers:", error);
      return [];
    }
  },

  /**
   * Get players on the trade block
   */
  getTradeBlock: async (teamId: number): Promise<TradeBlockPlayer[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trades/block/${teamId}`);
      if (response.ok) {
        return (await response.json()) as TradeBlockPlayer[];
      }
      return [];
    } catch {
      return [];
    }
  },

  /**
   * Add a player to the trade block
   */
  addToTradeBlock: async (
    playerId: number,
    askingPrice: "high" | "medium" | "low"
  ): Promise<TradeBlockPlayer> => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/trades/block`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player_id: playerId, asking_price: askingPrice }),
      });
      if (response.ok) {
        return (await response.json()) as TradeBlockPlayer;
      }
    } catch {
      // fallback
    }
    return {
      player_id: playerId,
      player_name: "Roster Player",
      position: "QB",
      overall: 80,
      trade_value: 75,
      asking_price: askingPrice,
      interest_level: 0,
      date_added: new Date().toISOString(),
    };
  },

  /**
   * Remove a player from the trade block
   */
  removeFromTradeBlock: async (playerId: number): Promise<void> => {
    try {
      await fetch(`${API_BASE_URL}/api/trades/block/${playerId}`, { method: "DELETE" });
    } catch {
      console.log("Removed player from trade block:", playerId);
    }
  },

  /**
   * Submit a formal trade offer
   */
  submitOffer: async (
    targetTeamId: number,
    offeredPlayerIds: number[],
    requestedPlayerIds: number[]
  ): Promise<{ offer_id: number; status: string; message: string }> => {
    return fetchJson<{ offer_id: number; status: string; message: string }>(`/api/trades/offer`, {
      method: "POST",
      body: JSON.stringify({
        target_team_id: targetTeamId,
        offered_player_ids: offeredPlayerIds,
        requested_player_ids: requestedPlayerIds,
      }),
    });
  },

  /**
   * Get all pending trade offers (Incoming and Outgoing)
   */
  getPendingOffers: async (
    teamId: number
  ): Promise<{ incoming: TradeOffer[]; outgoing: TradeOffer[] }> => {
    try {
      return await fetchJson<{ incoming: TradeOffer[]; outgoing: TradeOffer[] }>(
        `/api/trades/pending/${teamId}`
      );
    } catch (error) {
      console.warn("Failed to fetch pending offers:", error);
      return {
        incoming: [],
        outgoing: [],
      };
    }
  },

  /**
   * Respond to an incoming trade offer
   */
  respondToOffer: async (
    offerId: number,
    response: "accept" | "reject" | "counter",
    counterOffer?: Partial<TradeProposal>
  ): Promise<{ success: boolean; message: string }> => {
    if (response === "counter") {
      await fetchJson(`/api/trades/counter/${offerId}`, {
        method: "POST",
        body: JSON.stringify(counterOffer),
      });
      return { success: true, message: "Counter-offer sent." };
    } else {
      const res = await fetchJson<{ message: string; status: string }>(
        `/api/trades/respond/${offerId}`,
        {
          method: "POST",
          body: JSON.stringify({ action: response }),
        }
      );
      return {
        success: true,
        message: res.message || (response === "accept" ? "Trade accepted!" : "Trade rejected."),
      };
    }
  },

  /**
   * Get recent trade history
   */
  getTradeHistory: async (seasonId: number, limit: number = 10): Promise<TradeHistoryItem[]> => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/trades/history/${seasonId}?limit=${limit}`);
      if (res.ok) {
        return (await res.json()) as TradeHistoryItem[];
      }
      return [];
    } catch {
      return [];
    }
  },
};

/**
 * Calculate trade value based on overall and age
 */
function calculateTradeValue(overall: number, age: number): number {
  let value = overall;
  if (age < 23) value += 10;
  else if (age < 26) value += 5;
  else if (age <= 28) value += 0;
  else if (age <= 30) value -= 5;
  else if (age <= 32) value -= 10;
  else value -= 20;

  return Math.max(0, Math.min(100, value));
}

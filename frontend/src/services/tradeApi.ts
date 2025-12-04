/**
 * Trade API Service
 * Handles all trade-related API calls
 */
import type {
  TradePlayer,
  TradePick,
  TradeProposal,
  TradeEvaluation,
  IncomingTradeOffer,
  TradeBlockPlayer,
  TradeHistoryItem,
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
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed: ${response.statusText}`);
  }

  return response.json();
}

export const tradeApi = {
  /**
   * Get tradeable players for a team
   */
  getTradeablePlayers: async (teamId: number): Promise<TradePlayer[]> => {
    // For now, we'll fetch the roster and transform it
    // In a real implementation, this would be a dedicated endpoint
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
        salary: 5000000, // Default salary since not in Player type
        years_remaining: 2, // Default
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

      const data = await response.json();
      const teams: Team[] = data.items || data;

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
    seasonId: number,
    teamId: number,
    offeredPlayerIds: number[],
    requestedPlayerIds: number[]
  ): Promise<TradeEvaluation> => {
    const response = await fetchJson<TradeEvaluation>(`/api/season/${seasonId}/gm/evaluate-trade`, {
      method: "POST",
      body: JSON.stringify({
        team_id: teamId,
        offered_ids: offeredPlayerIds,
        requested_ids: requestedPlayerIds,
      }),
    });
    return response;
  },

  /**
   * Execute a trade (placeholder - would need backend implementation)
   */
  executeTrade: async (proposal: TradeProposal): Promise<{ success: boolean; message: string }> => {
    // This would be a real API call in production
    console.log("Executing trade proposal:", proposal);
    return {
      success: true,
      message: "Trade executed successfully!",
    };
  },

  /**
   * Get incoming trade offers from AI teams
   */
  getIncomingOffers: async (teamId: number): Promise<IncomingTradeOffer[]> => {
    // Mock data for MVP - would be real endpoint
    return generateMockIncomingOffers(teamId);
  },

  /**
   * Get players on the trade block
   */
  getTradeBlock: async (teamId: number): Promise<TradeBlockPlayer[]> => {
    // Mock implementation - would be real endpoint
    return [];
  },

  /**
   * Add a player to the trade block
   */
  addToTradeBlock: async (
    playerId: number,
    askingPrice: "high" | "medium" | "low"
  ): Promise<TradeBlockPlayer> => {
    // Mock implementation
    return {
      player_id: playerId,
      player_name: "Unknown Player",
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
    // Mock implementation
    console.log("Removing player from trade block:", playerId);
  },

  /**
   * Respond to an incoming trade offer
   */
  respondToOffer: async (
    offerId: number,
    response: "accept" | "reject" | "counter",
    counterOffer?: Partial<TradeProposal>
  ): Promise<{ success: boolean; message: string }> => {
    // Mock implementation
    return {
      success: true,
      message:
        response === "accept"
          ? "Trade accepted!"
          : response === "reject"
            ? "Trade rejected."
            : "Counter-offer sent.",
    };
  },

  /**
   * Get recent trade history
   */
  getTradeHistory: async (seasonId: number, limit: number = 10): Promise<TradeHistoryItem[]> => {
    // Mock implementation
    return [];
  },
};

/**
 * Calculate trade value based on overall and age
 */
function calculateTradeValue(overall: number, age: number): number {
  // Base value from overall rating
  let value = overall;

  // Age modifier (peak is 26-28)
  if (age < 23)
    value += 10; // Young potential
  else if (age < 26)
    value += 5; // Entering prime
  else if (age <= 28)
    value += 0; // Prime
  else if (age <= 30)
    value -= 5; // Leaving prime
  else if (age <= 32)
    value -= 10; // Declining
  else value -= 20; // Old

  return Math.max(0, Math.min(100, value));
}

/**
 * Generate mock incoming offers for testing
 */
function generateMockIncomingOffers(teamId: number): IncomingTradeOffer[] {
  // Return empty for now - can be populated with test data later
  return [];
}

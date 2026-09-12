import type { FreeAgentMarketPlayer } from "../types/offseason";

export type PositionFilter =
  | "ALL"
  | "OFF"
  | "DEF"
  | "ST"
  | "QB"
  | "RB"
  | "WR"
  | "TE"
  | "OL"
  | "DL"
  | "LB"
  | "DB"
  | "K/P";

export type TierFilter = "ALL" | "Tier 1" | "Tier 2" | "Tier 3" | "Tier 4";

/**
 * High-performance deterministic filter computation over normalized dictionary
 */
export function computeFilteredPlayers(
  byId: Record<number, FreeAgentMarketPlayer>,
  allIds: number[],
  positionFilter: PositionFilter,
  tierFilter: TierFilter,
  searchQuery: string
): { filteredIds: number[]; filteredPlayers: FreeAgentMarketPlayer[] } {
  const q = searchQuery.trim().toLowerCase();
  const hasQuery = q.length > 0;
  const filteredIds: number[] = [];
  const filteredPlayers: FreeAgentMarketPlayer[] = [];

  for (let i = 0; i < allIds.length; i++) {
    const id = allIds[i];
    const player = byId[id];
    if (!player) continue;

    // Position Filter
    if (positionFilter === "OFF") {
      if (
        !["QB", "RB", "WR", "TE", "OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(player.position)
      )
        continue;
    } else if (positionFilter === "DEF") {
      if (
        !["DE", "DT", "LB", "MLB", "OLB", "CB", "S", "FS", "SS", "EDGE"].includes(player.position)
      )
        continue;
    } else if (positionFilter === "ST") {
      if (!["K", "P", "LS"].includes(player.position)) continue;
    } else if (positionFilter === "OL") {
      if (!["OT", "OG", "C", "LT", "LG", "RG", "RT"].includes(player.position)) continue;
    } else if (positionFilter === "DL") {
      if (!["DE", "DT", "EDGE"].includes(player.position)) continue;
    } else if (positionFilter === "DB") {
      if (!["CB", "S", "FS", "SS"].includes(player.position)) continue;
    } else if (positionFilter === "K/P") {
      if (!["K", "P", "LS"].includes(player.position)) continue;
    } else if (positionFilter !== "ALL") {
      if (player.position !== positionFilter) continue;
    }

    // Tier Filter
    if (tierFilter !== "ALL") {
      const playerTier = (player.tier || "").toLowerCase();
      if (!playerTier.includes(tierFilter.toLowerCase().replace("tier ", ""))) {
        continue;
      }
    }

    // Search Query
    if (hasQuery) {
      const name = (player.player_name || player.name || "").toLowerCase();
      const pos = player.position.toLowerCase();
      if (!name.includes(q) && !pos.includes(q)) {
        continue;
      }
    }

    filteredIds.push(id);
    filteredPlayers.push(player);
  }

  return { filteredIds, filteredPlayers };
}

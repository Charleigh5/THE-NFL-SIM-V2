/**
 * Team Utilities & Canonical Franchise Lookups
 * Maps database integer team identifiers to official 3-letter NFL abbreviations.
 */

export const TEAM_ID_TO_ABBR: Record<number, string> = {
  1: "ARI",
  2: "ATL",
  3: "BAL",
  4: "BUF",
  5: "CAR",
  6: "CHI",
  7: "CIN",
  8: "CLE",
  9: "DAL",
  10: "DEN",
  11: "DET",
  12: "GB",
  13: "HOU",
  14: "IND",
  15: "JAX",
  16: "KC",
  17: "LV",
  18: "LAC",
  19: "LAR",
  20: "MIA",
  21: "MIN",
  22: "NE",
  23: "NO",
  24: "NYG",
  25: "NYJ",
  26: "PHI",
  27: "PIT",
  28: "SF",
  29: "SEA",
  30: "TB",
  31: "TEN",
  32: "WAS",
};

/**
 * Returns the 3-letter abbreviation for a team ID, or fallback.
 */
export function getTeamAbbr(teamId?: number | null, fallback = "DET"): string {
  if (!teamId) return fallback;
  return TEAM_ID_TO_ABBR[teamId] || fallback;
}

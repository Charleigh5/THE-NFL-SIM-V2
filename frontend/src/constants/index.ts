/**
 * Application-wide constants
 */

// API Configuration
export const API_TIMEOUT = 30000; // 30 seconds

// Pagination
export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;

// Season Configuration
export const REGULAR_SEASON_WEEKS = 18;
export const PLAYOFF_WEEKS = 4;

// UI Refresh Intervals
export const STANDINGS_REFRESH_INTERVAL = 30000; // 30 seconds
export const GAME_REFRESH_INTERVAL = 5000; // 5 seconds during live sim

// League Leaders
export const DEFAULT_LEADERS_COUNT = 5;

// Query Keys
export const QUERY_KEYS = {
  HEALTH: ["health"],
  TEAMS: ["teams"],
  TEAM: (id: number) => ["team", id],
  ROSTER: (teamId: number) => ["roster", teamId],
  SEASON: (id: number) => ["season", id],
  CURRENT_SEASON: ["season", "current"],
  STANDINGS: (seasonId: number) => ["standings", seasonId],
  SCHEDULE: (seasonId: number, week?: number) => ["schedule", seasonId, week],
  LEADERS: (seasonId: number) => ["leaders", seasonId],
  PLAYOFF_BRACKET: (seasonId: number) => ["playoff-bracket", seasonId],
} as const;
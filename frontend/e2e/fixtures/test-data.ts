/**
 * Shared E2E Test Fixtures
 * Mock data that matches actual API response shapes
 */

// ============================================================================
// TEAM DATA
// ============================================================================

export const mockTeam = {
  id: 1,
  name: "Cardinals",
  city: "Arizona",
  abbreviation: "ARI",
  conference: "NFC",
  division: "West",
};

export const mockTeams = [
  {
    id: 1,
    name: "Cardinals",
    city: "Arizona",
    abbreviation: "ARI",
    conference: "NFC",
    division: "West",
  },
  {
    id: 2,
    name: "49ers",
    city: "San Francisco",
    abbreviation: "SF",
    conference: "NFC",
    division: "West",
  },
  {
    id: 3,
    name: "Seahawks",
    city: "Seattle",
    abbreviation: "SEA",
    conference: "NFC",
    division: "West",
  },
  {
    id: 4,
    name: "Rams",
    city: "Los Angeles",
    abbreviation: "LAR",
    conference: "NFC",
    division: "West",
  },
];

// ============================================================================
// PLAYER DATA
// ============================================================================

export const mockPlayers = [
  {
    id: 1,
    first_name: "Kyler",
    last_name: "Murray",
    position: "QB",
    overall_rating: 88,
    team_id: 1,
    jersey_number: 1,
    age: 27,
  },
  {
    id: 2,
    first_name: "James",
    last_name: "Conner",
    position: "RB",
    overall_rating: 84,
    team_id: 1,
    jersey_number: 6,
    age: 29,
  },
  {
    id: 3,
    first_name: "Marvin",
    last_name: "Harrison Jr",
    position: "WR",
    overall_rating: 82,
    team_id: 1,
    jersey_number: 18,
    age: 22,
  },
];

// ============================================================================
// SEASON DATA
// ============================================================================

export const mockSeason = {
  id: 1,
  year: 2024,
  status: "REGULAR_SEASON",
  current_week: 2,
  total_weeks: 18,
};

export const mockSeasonSummary = {
  season: mockSeason,
  completion_percentage: 11.1,
  teams: mockTeams,
};

export const mockStandings = [
  {
    team_id: 2,
    team_name: "San Francisco 49ers",
    team_abbreviation: "SF",
    wins: 6,
    losses: 1,
    ties: 0,
    pct: 0.857,
    conference: "NFC",
    division: "West",
  },
  {
    team_id: 1,
    team_name: "Arizona Cardinals",
    team_abbreviation: "ARI",
    wins: 5,
    losses: 2,
    ties: 0,
    pct: 0.714,
    conference: "NFC",
    division: "West",
  },
  {
    team_id: 3,
    team_name: "Seattle Seahawks",
    team_abbreviation: "SEA",
    wins: 4,
    losses: 3,
    ties: 0,
    pct: 0.571,
    conference: "NFC",
    division: "West",
  },
  {
    team_id: 4,
    team_name: "Los Angeles Rams",
    team_abbreviation: "LAR",
    wins: 3,
    losses: 4,
    ties: 0,
    pct: 0.429,
    conference: "NFC",
    division: "West",
  },
];

export const mockSchedule = [
  {
    id: 1,
    week: 2,
    home_team_id: 1,
    away_team_id: 2,
    home_team: { id: 1, name: "Cardinals", abbreviation: "ARI" },
    away_team: { id: 2, name: "49ers", abbreviation: "SF" },
    home_score: 0,
    away_score: 0,
    is_played: false,
    scheduled_date: "2024-09-15T16:00:00Z",
    weather_info: null,
  },
];

export const mockLeaders = {
  passing: [
    {
      player_id: 101,
      name: "Kyler Murray",
      team: "ARI",
      position: "QB",
      yards: 2500,
      touchdowns: 18,
    },
  ],
  rushing: [
    {
      player_id: 102,
      name: "James Conner",
      team: "ARI",
      position: "RB",
      yards: 800,
      touchdowns: 6,
    },
  ],
  receiving: [
    {
      player_id: 103,
      name: "Marvin Harrison Jr",
      team: "ARI",
      position: "WR",
      yards: 1000,
      touchdowns: 8,
    },
  ],
};

export const mockAwards = {
  mvp: [{ player_id: 101, name: "Kyler Murray", team: "ARI", position: "QB", score: 85.5 }],
  opoy: [{ player_id: 103, name: "Marvin Harrison Jr", team: "ARI", position: "WR", score: 78.2 }],
  dpoy: [],
  oroy: [],
  droy: [],
};

// ============================================================================
// NEWS DATA
// ============================================================================

export const mockNewsResponse = {
  items: [
    {
      headline: "Cardinals Win Big in Week 1",
      source: "NFL Network",
      date: new Date().toISOString(),
      category: "game",
      is_breaking: false,
    },
    {
      headline: "49ers Acquire Star Receiver",
      source: "ESPN",
      date: new Date().toISOString(),
      category: "trades",
      is_breaking: true,
    },
  ],
  total: 2,
  last_updated: new Date().toISOString(),
};

// ============================================================================
// DRAFT DATA
// ============================================================================

export const mockProspects = [
  {
    id: 1,
    name: "Caleb Williams",
    first_name: "Caleb",
    last_name: "Williams",
    position: "QB",
    college: "USC",
    overall_grade: 95,
    projected_round: 1,
    overall_rating: 95,
  },
  {
    id: 2,
    name: "Marvin Harrison Jr",
    first_name: "Marvin",
    last_name: "Harrison Jr",
    position: "WR",
    college: "Ohio State",
    overall_grade: 94,
    projected_round: 1,
    overall_rating: 94,
  },
  {
    id: 3,
    name: "Drake Maye",
    first_name: "Drake",
    last_name: "Maye",
    position: "QB",
    college: "North Carolina",
    overall_grade: 92,
    projected_round: 1,
    overall_rating: 92,
  },
];

export const mockDraftPick = {
  id: 1,
  season_id: 1,
  round: 1,
  pick_number: 1,
  team_id: 1,
  original_team_id: 1,
  player_id: undefined,
};

// ============================================================================
// TRAINING DATA
// ============================================================================

export const mockCoachingStyles = [
  {
    id: "smart",
    name: "smart",
    display_name: "Smart",
    description: "Balanced approach",
    xp_multiplier: 1.0,
    injury_risk_multiplier: 1.0,
    fatigue_multiplier: 1.0,
    recovery_multiplier: 1.0,
  },
  {
    id: "aggressive",
    name: "aggressive",
    display_name: "Aggressive",
    description: "High risk high reward",
    xp_multiplier: 1.3,
    injury_risk_multiplier: 1.5,
    fatigue_multiplier: 1.2,
    recovery_multiplier: 0.8,
  },
  {
    id: "conservative",
    name: "conservative",
    display_name: "Conservative",
    description: "Safe and steady",
    xp_multiplier: 0.8,
    injury_risk_multiplier: 0.5,
    fatigue_multiplier: 0.8,
    recovery_multiplier: 1.4,
  },
];

export const mockDrills = [
  {
    id: "1",
    name: "Oklahoma Drill",
    category: "CONTACT",
    target_stat: "Strength",
    description: "High intensity blocking drill",
    xp_multiplier: 1.5,
    injury_risk: 0.1,
  },
  {
    id: "2",
    name: "7-on-7 Skeleton",
    category: "PASSING",
    target_stat: "Route Running",
    description: "Passing game practice",
    xp_multiplier: 1.2,
    injury_risk: 0.03,
  },
];

// ============================================================================
// HELPER: Setup common API routes for season dashboard tests
// Routes match localhost:8000 (API server) URLs
// ============================================================================

import type { Page } from "@playwright/test";

export async function setupSeasonDashboardMocks(page: Page) {
  // Teams endpoint - paginated response
  await page.route("**/api/teams**", async (route) => {
    await route.fulfill({
      json: { items: mockTeams, total: mockTeams.length, page: 1, page_size: 100, total_pages: 1 },
    });
  });

  // Season summary endpoint
  await page.route("**/api/season/summary", async (route) => {
    await route.fulfill({ json: mockSeasonSummary });
  });

  // Standings endpoint
  await page.route("**/api/season/*/standings**", async (route) => {
    await route.fulfill({ json: mockStandings });
  });

  // Schedule endpoint
  await page.route("**/api/season/*/schedule**", async (route) => {
    await route.fulfill({ json: mockSchedule });
  });

  // Leaders endpoint
  await page.route("**/api/season/*/leaders", async (route) => {
    await route.fulfill({ json: mockLeaders });
  });

  // Projected awards endpoint
  await page.route("**/api/season/*/awards/projected", async (route) => {
    await route.fulfill({ json: mockAwards });
  });

  // News league endpoint (used by NewsFeed component)
  await page.route("**/api/news/league**", async (route) => {
    await route.fulfill({ json: mockNewsResponse });
  });

  // Fallback for any living news endpoints
  await page.route("**/api/news/living/**", async (route) => {
    await route.fulfill({ json: { items: [], total_count: 0 } });
  });
}

export async function setupTrainingMocks(page: Page) {
  await page.route("**/api/training/styles", async (route) => {
    await route.fulfill({ json: mockCoachingStyles });
  });

  await page.route("**/api/training/drills**", async (route) => {
    await route.fulfill({ json: { drills: mockDrills, total: mockDrills.length } });
  });

  await page.route("**/api/v1/players/*/training-profile", async (route) => {
    await route.fulfill({
      json: {
        player_id: 1,
        player_name: "Test Player",
        position: "WR",
        age: 25,
        weaknesses: ["route_running"],
        fatigue: 20,
      },
    });
  });
}

// ============================================================================
// SCOUTING MOCK DATA
// ============================================================================

export const mockScoutingReport = {
  player_id: 1,
  player_name: "Caleb Williams",
  position: "QB",
  overall_grade: 95,
  strengths: [
    "Elite arm talent with ability to make any throw",
    "Outstanding mobility and escapability",
    "Excellent field vision and decision making",
  ],
  weaknesses: [
    "Tendency to hold the ball too long",
    "Can be too aggressive with throws into coverage",
  ],
  nfl_comparison: "Patrick Mahomes",
  ceiling: 98,
  floor: 82,
  summary: "Generational talent with rare combination of arm strength, accuracy, and mobility.",
  generated_at: new Date().toISOString(),
};

// ============================================================================
// HELPER: Setup draft room mocks
// ============================================================================

export async function setupDraftMocks(page: Page) {
  // Mock settings - both with and without /api prefix to be safe
  await page.route("**/api/settings", async (route) => {
    await route.fulfill({ json: { user_team_id: 1 } });
  });
  await page.route("**/settings", async (route) => {
    await route.fulfill({ json: { user_team_id: 1 } });
  });

  // Season current - for draftRoomLoader
  const mockSeasonData = { id: 1, year: 2024, status: "OFF_SEASON", current_week: 0 };
  await page.route("**/api/season/current", async (route) => {
    await route.fulfill({ json: mockSeasonData });
  });
  await page.route("**/api/seasons/current", async (route) => {
    await route.fulfill({ json: mockSeasonData });
  });
  await page.route("**/season/current", async (route) => {
    await route.fulfill({ json: mockSeasonData });
  });

  // Teams list - for draftRoomLoader (getTeams uses pagination)
  await page.route("**/api/teams?**", async (route) => {
    await route.fulfill({
      json: {
        items: [mockTeam],
        total: 1,
        page: 1,
        page_size: 100,
      },
    });
  });

  // Individual team
  await page.route("**/api/teams/1", async (route) => {
    await route.fulfill({ json: mockTeam });
  });
  await page.route("**/teams/1", async (route) => {
    await route.fulfill({ json: mockTeam });
  });

  // Current pick - for draftRoomLoader
  await page.route("**/api/season/*/draft/current-pick", async (route) => {
    await route.fulfill({
      json: { id: 1, season_id: 1, round: 1, pick_number: 1, team_id: 1, original_team_id: 1 },
    });
  });

  // Draft board - critical for draftService.getDraftBoard()
  await page.route("**/draft/board**", async (route) => {
    await route.fulfill({ json: mockProspects });
  });

  // Team needs - for DraftRoom
  await page.route("**/api/season/*/offseason/needs/**", async (route) => {
    await route.fulfill({
      json: [{ position: "QB", current_count: 2, target_count: 3, need_score: 4.5 }],
    });
  });

  // Draft order
  await page.route("**/draft/order**", async (route) => {
    await route.fulfill({
      json: [
        { round: 1, pick: 1, team_id: 1, team_name: "Cardinals" },
        { round: 1, pick: 2, team_id: 2, team_name: "Bears" },
      ],
    });
  });
}

// ============================================================================
// HELPER: Setup scouting mocks
// ============================================================================

export async function setupScoutingMocks(page: Page) {
  await setupDraftMocks(page);

  await page.route("**/api/scouting/report/*", async (route) => {
    await route.fulfill({ json: mockScoutingReport });
  });

  await page.route("**/api/players/*/backstory**", async (route) => {
    await route.fulfill({
      json: {
        player_id: 1,
        player_name: "Caleb Williams",
        content:
          "Caleb Williams grew up in Washington D.C. where he developed his passion for football.",
        generated_at: new Date().toISOString(),
      },
    });
  });
}

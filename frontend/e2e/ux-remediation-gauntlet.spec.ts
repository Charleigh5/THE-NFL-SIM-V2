/**
 * UX Remediation & War Room Hardening Gauntlet (TASK-042)
 * =======================================================
 * Exhaustive End-to-End Playwright Verification Suite covering all 10 UX Remediation Tickets:
 *
 *  - Ticket 1: Modal Stack Hierarchy (Escape dismissal, modal stack store registration)
 *  - Ticket 2: Standings Table Accessibility (WCAG 2.1 AA Contrast >= 4.5:1, Tabular Numerals)
 *  - Ticket 3: Trade Analyzer Ergonomics & Accessible Tooltips (Pts, Team Need Fit, Tooltips)
 *  - Ticket 4: Depth Chart Magnetic Card Hitbox & Touch Targets (min-height >= 72px, handles >= 44x44px)
 *  - Ticket 5: Progressive Disclosure Player Attributes Grid (4-card hero grid, details disclosure)
 *  - Ticket 6: Positional Vacancy Alert Badges on Depth Chart (Underfilled warning badges)
 *  - Ticket 7: Standings Conference Quick-Toggles (ALL / AFC / NFC instant filtering)
 *  - Ticket 8: Scheme Fit Affinity Tagging (Scheme name, fit score %, tier badge)
 *  - Ticket 9: Depth Chart Master Unit Keyboard Hotkeys (Keys 1 & 2 unit switching, kbd chips)
 *  - Ticket 10: Sticky Gameday Roster HUD Bar (Sticky layout, Active 46/46, Inactive 7/7, Cap Room)
 */

import { test, expect, type Page } from "@playwright/test";

// ============================================================================
// WCAG 2.1 Contrast Calculation Utilities
// ============================================================================

function parseRgb(colorStr: string): [number, number, number] {
  const match = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
  if (match) {
    return [parseInt(match[1], 10), parseInt(match[2], 10), parseInt(match[3], 10)];
  }
  return [0, 0, 0];
}

function getRelativeLuminance(r: number, g: number, b: number): number {
  const [sR, sG, sB] = [r, g, b].map((val) => {
    const c = val / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * sR + 0.7152 * sG + 0.0722 * sB;
}

function calculateContrastRatio(
  fgRgb: [number, number, number],
  bgRgb: [number, number, number]
): number {
  const lum1 = getRelativeLuminance(fgRgb[0], fgRgb[1], fgRgb[2]);
  const lum2 = getRelativeLuminance(bgRgb[0], bgRgb[1], bgRgb[2]);
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// ============================================================================
// Mock Data Fixtures
// ============================================================================

const MOCK_TEAMS = [
  {
    id: 11,
    city: "Detroit",
    name: "Lions",
    abbreviation: "DET",
    conference: "NFC",
    division: "North",
    wins: 12,
    losses: 5,
    ties: 0,
    salary_cap_space: 34200000,
    primary_color: "#0076B6",
    secondary_color: "#B0B7BC",
    logo_url: "https://static.www.nfl.com/image/private/f_auto/league/ocvxwnadsyjxolnrjhld",
  },
  {
    id: 1,
    city: "Kansas City",
    name: "Chiefs",
    abbreviation: "KC",
    conference: "AFC",
    division: "West",
    wins: 14,
    losses: 3,
    ties: 0,
    salary_cap_space: 18000000,
    primary_color: "#E31837",
    secondary_color: "#FFB81C",
  },
  {
    id: 2,
    city: "Baltimore",
    name: "Ravens",
    abbreviation: "BAL",
    conference: "AFC",
    division: "North",
    wins: 13,
    losses: 4,
    ties: 0,
    salary_cap_space: 22000000,
    primary_color: "#241773",
    secondary_color: "#000000",
  },
];

/**
 * Constructs an authentic 53-man NFL roster for Detroit.
 * Configured with 2 QBs (target 3) to trigger positional vacancy alert badges.
 */
function create53ManDetroitRoster() {
  const players: Array<Record<string, unknown>> = [
    // 2 QBs (underfilled: target is 3)
    {
      id: 289,
      first_name: "Jared",
      last_name: "Goff",
      position: "QB",
      jersey_number: 16,
      overall_rating: 88,
      age: 29,
      experience: 8,
      height: 76,
      weight: 217,
      team_id: 11,
      speed: 72,
      acceleration: 75,
      strength: 68,
      agility: 74,
      awareness: 91,
      stamina: 92,
      throw_power: 89,
      throw_accuracy_short: 92,
      pass_block: 60,
      run_block: 50,
      tackle: 45,
      traits: ["Precision Passer", "Play Action Maestro"],
      contract: { salary: "$53.0M / 4 Yrs", contract_salary: 53000000, years_remaining: 4 },
    },
    {
      id: 290,
      first_name: "Hendon",
      last_name: "Hooker",
      position: "QB",
      jersey_number: 12,
      overall_rating: 73,
      age: 26,
      experience: 2,
      height: 76,
      weight: 222,
      team_id: 11,
      speed: 84,
      acceleration: 86,
      strength: 70,
      agility: 80,
      awareness: 75,
      throw_power: 91,
      throw_accuracy_short: 78,
      traits: ["Dual Threat"],
      contract: { salary: "$1.5M / 3 Yrs", contract_salary: 1500000, years_remaining: 3 },
    },
    // 3 RBs (target: 3)
    {
      id: 2333,
      first_name: "Jahmyr",
      last_name: "Gibbs",
      position: "RB",
      jersey_number: 26,
      overall_rating: 89,
      age: 22,
      experience: 2,
      height: 69,
      weight: 200,
      team_id: 11,
      speed: 95,
      acceleration: 96,
      strength: 72,
      agility: 94,
      awareness: 86,
      traits: ["Lightning In A Bottle"],
      contract: { salary: "$4.5M / 3 Yrs", contract_salary: 4500000, years_remaining: 3 },
    },
    {
      id: 2334,
      first_name: "David",
      last_name: "Montgomery",
      position: "RB",
      jersey_number: 5,
      overall_rating: 84,
      age: 27,
      experience: 6,
      height: 71,
      weight: 224,
      team_id: 11,
      speed: 86,
      acceleration: 88,
      strength: 84,
      agility: 83,
      awareness: 85,
      contract: { salary: "$6.0M / 2 Yrs", contract_salary: 6000000, years_remaining: 2 },
    },
    {
      id: 2335,
      first_name: "Sione",
      last_name: "Vaki",
      position: "RB",
      jersey_number: 33,
      overall_rating: 72,
      age: 23,
      experience: 1,
      height: 71,
      weight: 210,
      team_id: 11,
      speed: 88,
      acceleration: 89,
      strength: 74,
      agility: 85,
      awareness: 72,
      contract: { salary: "$1.0M / 4 Yrs", contract_salary: 1000000, years_remaining: 4 },
    },
    // 5 WRs (target: 5)
    {
      id: 1417,
      first_name: "Amon-Ra",
      last_name: "St. Brown",
      position: "WR",
      jersey_number: 14,
      overall_rating: 94,
      age: 24,
      experience: 4,
      height: 72,
      weight: 202,
      team_id: 11,
      speed: 89,
      acceleration: 93,
      strength: 78,
      agility: 95,
      awareness: 96,
      catching: 96,
      route_running: 95,
      contract: { salary: "$30.0M / 4 Yrs", contract_salary: 30000000, years_remaining: 4 },
    },
    {
      id: 1418,
      first_name: "Jameson",
      last_name: "Williams",
      position: "WR",
      jersey_number: 9,
      overall_rating: 83,
      age: 23,
      experience: 3,
      height: 73,
      weight: 180,
      team_id: 11,
      speed: 98,
      acceleration: 97,
      strength: 65,
      agility: 92,
      awareness: 79,
      catching: 82,
      route_running: 81,
      contract: { salary: "$4.0M / 2 Yrs", contract_salary: 4000000, years_remaining: 2 },
    },
    {
      id: 1419,
      first_name: "Kalif",
      last_name: "Raymond",
      position: "WR",
      jersey_number: 11,
      overall_rating: 77,
      age: 30,
      experience: 8,
      height: 68,
      weight: 180,
      team_id: 11,
      speed: 91,
      acceleration: 91,
      strength: 60,
      agility: 90,
      awareness: 82,
      contract: { salary: "$3.5M / 2 Yrs", contract_salary: 3500000, years_remaining: 2 },
    },
    {
      id: 1420,
      first_name: "Donovan",
      last_name: "Peoples-Jones",
      position: "WR",
      jersey_number: 80,
      overall_rating: 76,
      age: 25,
      experience: 5,
      height: 74,
      weight: 204,
      team_id: 11,
      speed: 88,
      acceleration: 89,
      strength: 72,
      agility: 84,
      awareness: 78,
      contract: { salary: "$1.5M / 1 Yr", contract_salary: 1500000, years_remaining: 1 },
    },
    {
      id: 1421,
      first_name: "Antoine",
      last_name: "Green",
      position: "WR",
      jersey_number: 84,
      overall_rating: 71,
      age: 24,
      experience: 2,
      height: 74,
      weight: 199,
      team_id: 11,
      speed: 90,
      acceleration: 90,
      strength: 68,
      agility: 83,
      awareness: 70,
      contract: { salary: "$0.9M / 2 Yrs", contract_salary: 900000, years_remaining: 2 },
    },
    // 3 TEs
    {
      id: 1501,
      first_name: "Sam",
      last_name: "LaPorta",
      position: "TE",
      jersey_number: 87,
      overall_rating: 89,
      age: 23,
      experience: 2,
      height: 76,
      weight: 245,
      team_id: 11,
      speed: 86,
      acceleration: 88,
      strength: 82,
      agility: 87,
      awareness: 86,
      catching: 91,
      contract: { salary: "$2.5M / 3 Yrs", contract_salary: 2500000, years_remaining: 3 },
    },
    {
      id: 1502,
      first_name: "Brock",
      last_name: "Wright",
      position: "TE",
      jersey_number: 89,
      overall_rating: 74,
      age: 25,
      experience: 4,
      height: 77,
      weight: 255,
      team_id: 11,
      speed: 78,
      acceleration: 80,
      strength: 83,
      agility: 76,
      awareness: 76,
      contract: { salary: "$2.0M / 2 Yrs", contract_salary: 2000000, years_remaining: 2 },
    },
    {
      id: 1503,
      first_name: "James",
      last_name: "Mitchell",
      position: "TE",
      jersey_number: 82,
      overall_rating: 71,
      age: 25,
      experience: 3,
      height: 76,
      weight: 249,
      team_id: 11,
      speed: 80,
      acceleration: 81,
      strength: 79,
      agility: 78,
      awareness: 72,
      contract: { salary: "$1.0M / 2 Yrs", contract_salary: 1000000, years_remaining: 2 },
    },
    // 10 Offensive Linemen (OT, OG, C)
    {
      id: 1351,
      first_name: "Penei",
      last_name: "Sewell",
      position: "OT",
      jersey_number: 58,
      overall_rating: 96,
      age: 23,
      experience: 4,
      height: 77,
      weight: 335,
      team_id: 11,
      speed: 78,
      acceleration: 82,
      strength: 98,
      agility: 85,
      awareness: 94,
      pass_block: 95,
      run_block: 98,
      contract: { salary: "$28.0M / 4 Yrs", contract_salary: 28000000, years_remaining: 4 },
    },
    {
      id: 1352,
      first_name: "Taylor",
      last_name: "Decker",
      position: "OT",
      jersey_number: 68,
      overall_rating: 87,
      age: 31,
      experience: 9,
      height: 79,
      weight: 318,
      team_id: 11,
      speed: 71,
      acceleration: 74,
      strength: 92,
      agility: 78,
      awareness: 90,
      pass_block: 89,
      run_block: 86,
      contract: { salary: "$15.0M / 2 Yrs", contract_salary: 15000000, years_remaining: 2 },
    },
    {
      id: 1353,
      first_name: "Dan",
      last_name: "Skipper",
      position: "OT",
      jersey_number: 70,
      overall_rating: 72,
      age: 29,
      experience: 7,
      height: 81,
      weight: 330,
      team_id: 11,
      speed: 64,
      acceleration: 68,
      strength: 90,
      agility: 69,
      awareness: 76,
      contract: { salary: "$1.2M / 1 Yr", contract_salary: 1200000, years_remaining: 1 },
    },
    {
      id: 1354,
      first_name: "Colby",
      last_name: "Sorsdal",
      position: "OT",
      jersey_number: 75,
      overall_rating: 70,
      age: 24,
      experience: 2,
      height: 78,
      weight: 305,
      team_id: 11,
      speed: 70,
      acceleration: 73,
      strength: 87,
      agility: 74,
      awareness: 72,
      contract: { salary: "$1.0M / 3 Yrs", contract_salary: 1000000, years_remaining: 3 },
    },
    {
      id: 1355,
      first_name: "Kevin",
      last_name: "Zeitler",
      position: "OG",
      jersey_number: 71,
      overall_rating: 84,
      age: 34,
      experience: 13,
      height: 76,
      weight: 340,
      team_id: 11,
      speed: 65,
      acceleration: 68,
      strength: 94,
      agility: 72,
      awareness: 93,
      pass_block: 88,
      run_block: 86,
      contract: { salary: "$6.0M / 1 Yr", contract_salary: 6000000, years_remaining: 1 },
    },
    {
      id: 1356,
      first_name: "Graham",
      last_name: "Glasgow",
      position: "OG",
      jersey_number: 60,
      overall_rating: 81,
      age: 32,
      experience: 9,
      height: 78,
      weight: 315,
      team_id: 11,
      speed: 66,
      acceleration: 70,
      strength: 90,
      agility: 73,
      awareness: 87,
      contract: { salary: "$5.0M / 2 Yrs", contract_salary: 5000000, years_remaining: 2 },
    },
    {
      id: 1357,
      first_name: "Kayode",
      last_name: "Awosika",
      position: "OG",
      jersey_number: 74,
      overall_rating: 69,
      age: 26,
      experience: 4,
      height: 75,
      weight: 315,
      team_id: 11,
      speed: 68,
      acceleration: 71,
      strength: 88,
      agility: 72,
      awareness: 71,
      contract: { salary: "$1.0M / 1 Yr", contract_salary: 1000000, years_remaining: 1 },
    },
    {
      id: 1358,
      first_name: "Christian",
      last_name: "Mahogany",
      position: "OG",
      jersey_number: 73,
      overall_rating: 68,
      age: 23,
      experience: 1,
      height: 75,
      weight: 322,
      team_id: 11,
      speed: 69,
      acceleration: 72,
      strength: 89,
      agility: 73,
      awareness: 69,
      contract: { salary: "$0.9M / 4 Yrs", contract_salary: 900000, years_remaining: 4 },
    },
    {
      id: 1359,
      first_name: "Frank",
      last_name: "Ragnow",
      position: "C",
      jersey_number: 77,
      overall_rating: 93,
      age: 28,
      experience: 7,
      height: 77,
      weight: 311,
      team_id: 11,
      speed: 72,
      acceleration: 75,
      strength: 95,
      agility: 79,
      awareness: 96,
      pass_block: 92,
      run_block: 96,
      contract: { salary: "$13.5M / 3 Yrs", contract_salary: 13500000, years_remaining: 3 },
    },
    {
      id: 1360,
      first_name: "Michael",
      last_name: "Niese",
      position: "C",
      jersey_number: 63,
      overall_rating: 67,
      age: 26,
      experience: 2,
      height: 77,
      weight: 295,
      team_id: 11,
      speed: 66,
      acceleration: 69,
      strength: 87,
      agility: 71,
      awareness: 72,
      contract: { salary: "$0.9M / 1 Yr", contract_salary: 900000, years_remaining: 1 },
    },
    // Defensive Linemen (DL / DE / DT) - 10 players
    {
      id: 1543,
      first_name: "Aidan",
      last_name: "Hutchinson",
      position: "DL",
      jersey_number: 97,
      overall_rating: 92,
      age: 24,
      experience: 3,
      height: 79,
      weight: 268,
      team_id: 11,
      speed: 86,
      acceleration: 89,
      strength: 92,
      agility: 88,
      awareness: 90,
      pass_rush_finesse: 95,
      pass_rush_power: 92,
      block_shed: 90,
      tackle: 88,
      traits: ["Motor That Never Stops", "Bulls-Eye Rusher"],
      contract: { salary: "$9.5M / 2 Yrs", contract_salary: 9500000, years_remaining: 2 },
    },
  ];

  // Fill up to exactly 53 players across defense and specialists (23 offense + 30 defense/specialists = 53 total)
  let currentId = 1544;
  const positionsToFill: Array<{ pos: string; count: number }> = [
    { pos: "DL", count: 9 }, // Total 10 DL
    { pos: "LB", count: 8 }, // 8 LB
    { pos: "CB", count: 5 }, // 5 CB
    { pos: "S", count: 4 }, // 4 S
    { pos: "K", count: 1 }, // 1 K
    { pos: "P", count: 1 }, // 1 P
    { pos: "LS", count: 1 }, // 1 LS
  ];

  positionsToFill.forEach(({ pos, count }) => {
    for (let i = 0; i < count; i++) {
      players.push({
        id: currentId++,
        first_name: `Player`,
        last_name: `${pos}_${i + 1}`,
        position: pos,
        jersey_number: (currentId % 90) + 10,
        overall_rating: 74 + (i % 8),
        age: 24 + (i % 6),
        experience: 2 + (i % 5),
        height: 74,
        weight: 230,
        team_id: 11,
        speed: 82,
        acceleration: 84,
        strength: 80,
        agility: 80,
        awareness: 78,
        tackle: 78,
        pass_rush_power: 76,
        pass_rush_finesse: 76,
        block_shed: 76,
        contract: { salary: "$1.5M / 2 Yrs", contract_salary: 1500000, years_remaining: 2 },
      });
    }
  });

  return players;
}

const MOCK_SEASON_SUMMARY = {
  season: {
    id: 1,
    year: 2024,
    current_week: 5,
    status: "REGULAR_SEASON",
  },
  completion_percentage: 28,
  standings: [
    {
      conference: "AFC",
      divisions: [
        {
          division: "North",
          teams: [
            {
              team_id: 2,
              team_name: "Baltimore Ravens",
              team_abbreviation: "BAL",
              conference: "AFC",
              division: "North",
              wins: 4,
              losses: 1,
              ties: 0,
              win_percentage: 0.8,
              points_for: 140,
              points_against: 100,
              point_differential: 40,
              strength_of_schedule: 0.52,
              conference_rank: 1,
              division_rank: 1,
              elo_rating: 1650,
            },
          ],
        },
        {
          division: "West",
          teams: [
            {
              team_id: 1,
              team_name: "Kansas City Chiefs",
              team_abbreviation: "KC",
              conference: "AFC",
              division: "West",
              wins: 5,
              losses: 0,
              ties: 0,
              win_percentage: 1.0,
              points_for: 150,
              points_against: 90,
              point_differential: 60,
              strength_of_schedule: 0.55,
              conference_rank: 2,
              division_rank: 1,
              elo_rating: 1710,
            },
          ],
        },
      ],
    },
    {
      conference: "NFC",
      divisions: [
        {
          division: "North",
          teams: [
            {
              team_id: 11,
              team_name: "Detroit Lions",
              team_abbreviation: "DET",
              conference: "NFC",
              division: "North",
              wins: 4,
              losses: 1,
              ties: 0,
              win_percentage: 0.8,
              points_for: 155,
              points_against: 110,
              point_differential: 45,
              strength_of_schedule: 0.51,
              conference_rank: 1,
              division_rank: 1,
              elo_rating: 1680,
            },
          ],
        },
      ],
    },
  ],
  league_leaders: {
    passing: [
      {
        player_id: 289,
        name: "Jared Goff",
        team: "DET",
        position: "QB",
        value: 1580,
        rank: 1,
      },
    ],
    rushing: [
      {
        player_id: 2333,
        name: "Jahmyr Gibbs",
        team: "DET",
        position: "RB",
        value: 520,
        rank: 1,
      },
    ],
    receiving: [
      {
        player_id: 1417,
        name: "Amon-Ra St. Brown",
        team: "DET",
        position: "WR",
        value: 610,
        rank: 1,
      },
    ],
    sacks: [
      {
        player_id: 1543,
        name: "Aidan Hutchinson",
        team: "DET",
        position: "DL",
        value: 14.5,
        rank: 1,
      },
    ],
    tackles: [
      {
        player_id: 1543,
        name: "Aidan Hutchinson",
        team: "DET",
        position: "DL",
        value: 58,
        rank: 1,
      },
    ],
    defense: [
      {
        player_id: 1543,
        name: "Aidan Hutchinson",
        team: "DET",
        position: "DL",
        value: 14.5,
        rank: 1,
      },
    ],
    field_goal_percentage: [],
  },
};

// ============================================================================
// Network Route Interceptor Setup
// ============================================================================

async function setupGauntletMocks(page: Page) {
  const detroitRoster = create53ManDetroitRoster();

  await page.addInitScript(() => {
    localStorage.setItem("selectedTeamId", "11");
    localStorage.setItem("nfl_sim_sound_muted", "true");
  });

  // Settings mock
  await page.route("**/api/settings", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: { user_team_id: 11, selected_season_id: 1 },
    });
  });

  // Teams list mock
  await page.route("**/api/teams?*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: {
        items: MOCK_TEAMS,
        total: MOCK_TEAMS.length,
        page: 1,
        page_size: 100,
        total_pages: 1,
      },
    });
  });

  await page.route("**/api/teams", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_TEAMS,
    });
  });

  // Individual teams
  await page.route("**/api/teams/11", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_TEAMS[0],
    });
  });

  await page.route("**/api/teams/1", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_TEAMS[1],
    });
  });

  await page.route("**/api/teams/2", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_TEAMS[2],
    });
  });

  // Detroit Roster
  await page.route("**/api/teams/11/roster", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: detroitRoster,
    });
  });

  // Kansas City Roster (trade partner)
  await page.route("**/api/teams/1/roster", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: [
        {
          id: 201,
          first_name: "Patrick",
          last_name: "Mahomes",
          position: "QB",
          jersey_number: 15,
          overall_rating: 99,
          age: 28,
          experience: 8,
          team_id: 1,
          salary: 50000000,
          contract_salary: 50000000,
          years_remaining: 5,
        },
        {
          id: 202,
          first_name: "Travis",
          last_name: "Kelce",
          position: "TE",
          jersey_number: 87,
          overall_rating: 95,
          age: 34,
          experience: 12,
          team_id: 1,
          salary: 17000000,
          contract_salary: 17000000,
          years_remaining: 2,
        },
      ],
    });
  });

  // Chemistry endpoints
  await page.route("**/api/teams/*/chemistry", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: {
        chemistry_level: 3,
        consecutive_games: 8,
        status: "SYNERGIZED",
        bonuses: { pass_block: 3, run_block: 4, awareness: 2 },
      },
    });
  });

  // Depth Chart updates
  await page.route("**/api/teams/*/depth-chart", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: { message: "Depth chart order preserved successfully." },
    });
  });

  // Season endpoints
  await page.route("**/api/season/current", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_SEASON_SUMMARY.season,
    });
  });

  await page.route("**/api/seasons/current", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_SEASON_SUMMARY.season,
    });
  });

  await page.route("**/api/season/summary", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_SEASON_SUMMARY,
    });
  });

  await page.route("**/api/season/*/standings*", async (route) => {
    const flatStandings = MOCK_SEASON_SUMMARY.standings.flatMap((c) =>
      c.divisions.flatMap((d) => d.teams)
    );
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: flatStandings,
    });
  });

  await page.route("**/api/season/*/schedule*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: [],
    });
  });

  await page.route("**/api/season/*/awards*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: { mvp: [], opoy: [], dpoy: [] },
    });
  });

  await page.route("**/api/season/*/leaders*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: MOCK_SEASON_SUMMARY.league_leaders,
    });
  });

  // Player endpoints
  await page.route("**/api/players/1543", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: detroitRoster.find((p) => p.id === 1543) || detroitRoster[0],
    });
  });

  await page.route("**/api/players/1543/stats", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: {
        games_played: 17,
        tackles: 58,
        tackles_solo: 42,
        tackles_assist: 16,
        sacks: 14.5,
        interceptions: 2,
        pass_deflections: 7,
        forced_fumbles: 3,
        tackles_for_loss: 18,
        qb_pressures: 48,
      },
    });
  });

  await page.route("**/api/players/289", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: detroitRoster.find((p) => p.id === 289) || detroitRoster[0],
    });
  });

  await page.route("**/api/players/289/stats", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: {
        games_played: 17,
        passing_yards: 4575,
        passing_tds: 30,
        interceptions: 9,
      },
    });
  });

  // Trade endpoints
  await page.route("**/api/trades/pending/*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: { incoming: [], outgoing: [] },
    });
  });

  await page.route("**/api/trades/evaluate", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      json: {
        score: 12.5,
        decision: "ACCEPTED",
        reasoning: "Mutually beneficial value distribution aligning with both franchises.",
        offered_value: 1450,
        requested_value: 1200,
        user_side: { grade: "A" },
        ai_side: { grade: "B+" },
        narrative_notes: [
          "High TNI on defensive front addressing critical pass rush shortage.",
          "Draft EV Decay accounted for in 2027 draft assets.",
          "Cap Surcharge absorbed within luxury margin.",
        ],
      },
    });
  });
}

// ============================================================================
// Playwright Test Suite
// ============================================================================

test.describe("TASK-042: UX Remediation & War Room Hardening Gauntlet", () => {
  test.beforeEach(async ({ page }) => {
    await setupGauntletMocks(page);
  });

  // --------------------------------------------------------------------------
  // Ticket 1: Modal Stack Hierarchy (Escape dismissal, modal stack store)
  // --------------------------------------------------------------------------
  test("Ticket 1: Modal Stack Hierarchy - dismisses top modal upon Escape press", async ({
    page,
  }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="tab-leaders"]', { timeout: 8000 });

    // Switch to leaders tab in SeasonDashboard
    await page.locator('[data-testid="tab-leaders"]').click();
    await page.waitForSelector('[data-testid="league-leaders-container"]', { timeout: 8000 });

    // Open League Leaders defense tab and click Aidan Hutchinson to trigger PlayerModal
    const defTab = page.locator('[data-testid="tab-defense"]');
    await defTab.click();

    const leaderHeading = page.locator(".leader-info h4").first();
    await expect(leaderHeading).toBeVisible();
    await leaderHeading.click();

    // Verify PlayerModal opened and registered in ModalShell
    const playerModal = page.locator('[data-testid="player-modal"]');
    await expect(playerModal).toBeVisible({ timeout: 5000 });
    const modalShell = page.locator('[data-testid="player-modal-shell"]');
    await expect(modalShell).toBeVisible();

    // Press Escape key
    await page.keyboard.press("Escape");

    // Top modal must be dismissed
    await expect(playerModal).not.toBeVisible();
  });

  // --------------------------------------------------------------------------
  // Ticket 2: Standings Table Accessibility & Tabular Numbers
  // --------------------------------------------------------------------------
  test("Ticket 2: Standings Table Accessibility - high-contrast th headers (>= 4.5:1) & tabular numerals", async ({
    page,
  }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="tab-standings"]', { timeout: 8000 });

    // Switch to Standings tab to access full StandingsTable with quick-toggles and th headers
    await page.locator('[data-testid="tab-standings"]').click();
    await page.waitForSelector('[data-testid="standings-table"]', { timeout: 8000 });

    const thHeaders = page.locator(".standings-table th");
    const thCount = await thHeaders.count();
    expect(thCount).toBeGreaterThan(0);

    // Verify th color (#e4e4e7 -> rgb(228, 228, 231)) and WCAG 2.1 AA contrast ratio >= 4.5:1
    for (let i = 0; i < thCount; i++) {
      const th = thHeaders.nth(i);
      const computed = await th.evaluate((el) => {
        const style = window.getComputedStyle(el);
        return {
          color: style.color,
          bgColor: style.backgroundColor,
          fontWeight: style.fontWeight,
        };
      });

      expect(computed.color).toBe("rgb(228, 228, 231)");

      // Compute contrast against header dark background (#2a2a2a = rgb(42, 42, 42))
      const fgRgb = parseRgb(computed.color);
      const bgRgb = parseRgb(
        computed.bgColor.includes("rgba(0, 0, 0, 0)") ? "rgb(42, 42, 42)" : computed.bgColor
      );
      const contrast = calculateContrastRatio(fgRgb, bgRgb);
      expect(contrast).toBeGreaterThanOrEqual(4.5);
    }

    // Verify stat-cell numbers enforce tabular numerals
    const statCells = page.locator(".standings-table td.stat-cell");
    const sampleCell = statCells.first();
    const cellStyles = await sampleCell.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return {
        fontVariantNumeric: s.fontVariantNumeric,
        fontFamily: s.fontFamily,
      };
    });

    expect(cellStyles.fontVariantNumeric).toContain("tabular-nums");
    expect(cellStyles.fontFamily).toMatch(/monospace|SFMono|Menlo|ui-monospace/i);
  });

  // --------------------------------------------------------------------------
  // Ticket 3: Trade Analyzer Ergonomics & Accessible Tooltips
  // --------------------------------------------------------------------------
  test("Ticket 3: Trade Analyzer Ergonomics - humanized metrics (Pts, Team Need Fit) & AccessibleTooltip", async ({
    page,
  }) => {
    await page.goto("/empire/trade-center");
    await page.waitForSelector('[data-testid="trade-negotiator"]', { timeout: 8000 });

    // Select Kansas City Chiefs as trade partner
    const partnerSelect = page.locator('[data-testid="trade-partner-select"]');
    await partnerSelect.selectOption("1");

    // Wait for partner assets to render
    const partnerAsset = page.locator('[data-testid^="draggable-partner-player-"]').first();
    await partnerAsset.waitFor({ state: "visible", timeout: 8000 });

    // Add 1 user player and 1 partner player to unlock analysis
    const userAsset = page.locator('[data-testid^="draggable-user-player-"]').first();
    await userAsset.click();
    await partnerAsset.click();

    // Click Analyze Fairness button
    const analyzeBtn = page.locator('[data-testid="analyze-btn"]');
    await expect(analyzeBtn).toBeEnabled({ timeout: 5000 });
    await analyzeBtn.click();

    // Assert evaluation results appear
    const evalResult = page.locator('[data-testid="evaluation-result"]');
    await expect(evalResult).toBeVisible({ timeout: 5000 });

    // 1. Assert natural language Trade Value Points ('Pts' instead of raw 'TVP')
    const offeredCap = page.locator('[data-testid="offered-capital-val"]');
    const receivedCap = page.locator('[data-testid="received-capital-val"]');
    await expect(offeredCap).toContainText("Pts");
    await expect(receivedCap).toContainText("Pts");
    await expect(page.locator(".tvp-values-row")).not.toContainText("TVP");

    // 2. Assert humanized narrative tags (Team Need Fit instead of raw TNI)
    const narrativeContainer = page.locator('[data-testid="narrative-tags"]');
    await expect(narrativeContainer).toBeVisible();
    await expect(narrativeContainer).toContainText("Team Need Fit");
    await expect(narrativeContainer).toContainText("Draft Value Drift");
    await expect(narrativeContainer).toContainText("Salary Cap Impact");
    await expect(narrativeContainer).not.toContainText(/\bTNI\b/);

    // 3. Assert AccessibleTooltip activates on hover/focus and dismisses on Escape
    const tooltipTrigger = page.locator(".accessible-tooltip-trigger").first();
    await tooltipTrigger.hover();

    const tooltipBubble = page.locator('[data-testid="accessible-tooltip-bubble"]');
    await expect(tooltipBubble).toBeVisible();
    await expect(tooltipBubble).toHaveAttribute("role", "tooltip");

    // Keyboard dismissal via Escape key
    await page.keyboard.press("Escape");
    await expect(tooltipBubble).not.toBeVisible();
  });

  // --------------------------------------------------------------------------
  // Ticket 4: Depth Chart Magnetic Card Hitbox & Touch Targets
  // --------------------------------------------------------------------------
  test("Ticket 4: Depth Chart Magnetic Card Hitbox & Touch Targets - min-height >= 72px & 44x44px handles", async ({
    page,
  }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForSelector('[data-testid^="depth-player-"]', { timeout: 8000 });

    const card = page.locator('[data-testid^="depth-player-"]').first();
    const cardComputed = await card.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return parseFloat(s.minHeight);
    });

    // Assert min-height >= 72px (specifically styled at 76px / 4.75rem)
    expect(cardComputed).toBeGreaterThanOrEqual(72);
    expect(cardComputed).toBe(76);

    // Assert drag handle touch target >= 44x44px (WCAG touch target criterion)
    const dragHandle = page.locator(".depth-drag-handle").first();
    const handleBox = await dragHandle.boundingBox();
    expect(handleBox).not.toBeNull();
    expect(handleBox!.width).toBeGreaterThanOrEqual(44);
    expect(handleBox!.height).toBeGreaterThanOrEqual(44);

    const handleStyles = await dragHandle.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return {
        minWidth: parseFloat(s.minWidth),
        minHeight: parseFloat(s.minHeight),
      };
    });
    expect(handleStyles.minWidth).toBeGreaterThanOrEqual(44);
    expect(handleStyles.minHeight).toBeGreaterThanOrEqual(44);
  });

  // --------------------------------------------------------------------------
  // Ticket 5: Progressive Disclosure Player Attributes Grid
  // --------------------------------------------------------------------------
  test("Ticket 5: Progressive Disclosure Player Attributes Grid - hero grid & closed full-traits disclosure", async ({
    page,
  }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="tab-leaders"]', { timeout: 8000 });

    // Switch to leaders tab in SeasonDashboard
    await page.locator('[data-testid="tab-leaders"]').click();
    await page.waitForSelector('[data-testid="league-leaders-container"]', { timeout: 8000 });

    // Open League Leaders defense tab and click Aidan Hutchinson
    await page.locator('[data-testid="tab-defense"]').click();
    await page.locator(".leader-info h4").first().click();

    await page.waitForSelector('[data-testid="player-modal"]', { timeout: 5000 });

    // Assert Primary Key Attributes are displayed in hero cards
    const primaryGrid = page.locator('[data-testid="primary-attributes-grid"]');
    await expect(primaryGrid).toBeVisible();
    const primaryCards = primaryGrid.locator(".primary-attribute-card");
    await expect(primaryCards).toHaveCount(4);

    // Assert Full Traits Disclosure (<details>) is closed by default
    const disclosure = page.locator('[data-testid="full-traits-disclosure"]');
    await expect(disclosure).toBeVisible();
    await expect(disclosure).not.toHaveAttribute("open");

    // Expand disclosure on summary click
    const summary = disclosure.locator("summary");
    await summary.click();

    // Assert disclosure opens and reveals secondary traits
    await expect(disclosure).toHaveAttribute("open");
    const secondaryTraits = disclosure.locator('[data-testid^="secondary-trait-"]');
    expect(await secondaryTraits.count()).toBeGreaterThan(0);
  });

  // --------------------------------------------------------------------------
  // Ticket 6: Positional Vacancy Alert Badges on Depth Chart
  // --------------------------------------------------------------------------
  test("Ticket 6: Positional Vacancy Alert Badges on Depth Chart - alert badge on underfilled positions", async ({
    page,
  }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForSelector('[data-testid="gameday-roster-hud"]', { timeout: 8000 });

    // With 2 QBs on roster against a target of 3, the QB vacancy alert badge must render
    const vacancyBadge = page.locator('[data-testid="underfilled-badge-QB"]');
    await expect(vacancyBadge).toBeVisible();
    await expect(vacancyBadge).toHaveClass(/underfilled-pos-badge/);
    await expect(vacancyBadge).toHaveAttribute("title", /underfilled/i);
    await expect(vacancyBadge.locator("svg")).toBeVisible();
  });

  // --------------------------------------------------------------------------
  // Ticket 7: Standings Conference Quick-Toggles
  // --------------------------------------------------------------------------
  test("Ticket 7: Standings Conference Quick-Toggles - instant filtering by ALL, AFC, and NFC", async ({
    page,
  }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="tab-standings"]', { timeout: 8000 });

    // Switch to Standings tab to access full StandingsTable with quick-toggles
    await page.locator('[data-testid="tab-standings"]').click();
    await page.waitForSelector('[data-testid="standings-table"]', { timeout: 8000 });

    const afcRow = page.locator('[data-testid="standings-table-row-Baltimore Ravens"]');
    const nfcRow = page.locator('[data-testid="standings-table-row-Detroit Lions"]');

    // Default 'ALL' view: both AFC and NFC rows visible
    await expect(afcRow).toBeVisible();
    await expect(nfcRow).toBeVisible();

    // Toggle AFC filter
    const afcToggle = page
      .locator('[data-testid="standings-toggle-afc"], [data-testid="quick-toggle-afc"]')
      .first();
    await afcToggle.click();
    await expect(afcRow).toBeVisible();
    await expect(nfcRow).not.toBeVisible();

    // Toggle NFC filter
    const nfcToggle = page
      .locator('[data-testid="standings-toggle-nfc"], [data-testid="quick-toggle-nfc"]')
      .first();
    await nfcToggle.click();
    await expect(nfcRow).toBeVisible();
    await expect(afcRow).not.toBeVisible();

    // Reset to ALL view
    const allToggle = page
      .locator('[data-testid="standings-toggle-all"], [data-testid="quick-toggle-all"]')
      .first();
    await allToggle.click();
    await expect(afcRow).toBeVisible();
    await expect(nfcRow).toBeVisible();
  });

  // --------------------------------------------------------------------------
  // Ticket 8: Scheme Fit Affinity Tagging
  // --------------------------------------------------------------------------
  test("Ticket 8: Scheme Fit Affinity Tagging - displays scheme fit score, name, and tier badge", async ({
    page,
  }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="tab-leaders"]', { timeout: 8000 });

    // Switch to leaders tab in SeasonDashboard
    await page.locator('[data-testid="tab-leaders"]').click();
    await page.waitForSelector('[data-testid="league-leaders-container"]', { timeout: 8000 });

    // Open PlayerModal for Aidan Hutchinson
    await page.locator('[data-testid="tab-defense"]').click();
    await page.locator(".leader-info h4").first().click();

    await page.waitForSelector('[data-testid="player-modal"]', { timeout: 5000 });

    // Assert Scheme Fit Badge
    const schemeBadge = page.locator('[data-testid="scheme-fit-badge"]');
    await expect(schemeBadge).toBeVisible();
    await expect(schemeBadge.locator(".scheme-fit-label")).toHaveText("Scheme Fit:");

    const schemeVal = schemeBadge.locator(".scheme-fit-val");
    await expect(schemeVal).toBeVisible();
    await expect(schemeVal).toHaveText(/\d+%\s*•\s*.+/);

    // Verify tier styling class
    const badgeClass = await schemeBadge.getAttribute("class");
    expect(badgeClass).toMatch(/elite-fit|compatible-fit|neutral-fit/);
  });

  // --------------------------------------------------------------------------
  // Ticket 9: Depth Chart Master Unit Keyboard Hotkeys
  // --------------------------------------------------------------------------
  test("Ticket 9: Depth Chart Master Unit Keyboard Hotkeys - keys 1 and 2 switch unit with visual kbd chips", async ({
    page,
  }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForSelector('[data-testid="gameday-roster-hud"]', { timeout: 8000 });

    // Assert kbd chips are present on unit tabs
    const hotkeyChips = page.locator(".unit-hotkey-chip");
    await expect(hotkeyChips).toHaveCount(4);
    await expect(page.locator('[data-testid="unit-hotkey-1"]')).toHaveText("1");
    await expect(page.locator('[data-testid="unit-hotkey-2"]')).toHaveText("2");

    // Initially OFFENSE is active
    const offenseTab = page.locator('[data-testid="unit-tab-offense"]');
    const defenseTab = page.locator('[data-testid="unit-tab-defense"]');
    await expect(offenseTab).toHaveAttribute("aria-pressed", "true");
    await expect(defenseTab).toHaveAttribute("aria-pressed", "false");

    // Press hotkey '2' to switch to DEFENSE
    await page.keyboard.press("2");
    await expect(defenseTab).toHaveAttribute("aria-pressed", "true");
    await expect(offenseTab).toHaveAttribute("aria-pressed", "false");

    // Press hotkey '1' to switch back to OFFENSE
    await page.keyboard.press("1");
    await expect(offenseTab).toHaveAttribute("aria-pressed", "true");
    await expect(defenseTab).toHaveAttribute("aria-pressed", "false");
  });

  // --------------------------------------------------------------------------
  // Ticket 10: Sticky Gameday Roster HUD Bar
  // --------------------------------------------------------------------------
  test("Ticket 10: Sticky Gameday Roster HUD Bar - sticky positioning and active/inactive/cap counters", async ({
    page,
  }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForSelector('[data-testid="gameday-roster-hud"]', { timeout: 8000 });

    const hud = page.locator('[data-testid="gameday-roster-hud"]');
    await expect(hud).toBeVisible();

    // Verify sticky layout styling
    const hudStyles = await hud.evaluate((el) => {
      const s = window.getComputedStyle(el);
      return {
        position: s.position,
        top: s.top,
      };
    });
    expect(hudStyles.position).toBe("sticky");
    expect(hudStyles.top).toBe("0px");

    // Verify 46-Active / 7-Inactive / 53-Total / Cap Room metrics
    await expect(hud).toContainText("GAMEDAY ACTIVE:");
    await expect(hud).toContainText("46 / 46");
    await expect(hud).toContainText("INACTIVE:");
    await expect(hud).toContainText("7 / 7");
    await expect(hud).toContainText("TOTAL ROSTER:");
    await expect(hud).toContainText("53 / 53");
    await expect(hud).toContainText("CAP ROOM:");
    await expect(hud).toContainText("$34.2M");
  });
});

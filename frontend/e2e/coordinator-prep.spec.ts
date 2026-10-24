import { test, expect } from "@playwright/test";

const BASE_URL = "http://localhost:5199";

const mockSeason = {
  id: 1,
  year: 2026,
  current_week: 3,
  is_active: true,
  status: "REGULAR_SEASON",
  total_weeks: 18,
  playoff_weeks: 4,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

const mockSummary = {
  season: mockSeason,
  current_week: 3,
  total_weeks: 18,
  is_active: true,
  status: "REGULAR_SEASON",
  completion_percentage: 11,
};

const mockTeams = [
  {
    id: 11,
    city: "Detroit",
    name: "Lions",
    abbreviation: "DET",
    conference: "NFC",
    division: "North",
    wins: 1,
    losses: 1,
    salary_cap_space: 25000000,
  },
  {
    id: 1,
    city: "Atlanta",
    name: "Falcons",
    abbreviation: "ATL",
    conference: "NFC",
    division: "South",
    wins: 2,
    losses: 0,
    salary_cap_space: 20000000,
  },
];

const mockStandings = [
  {
    team_id: 11,
    team_name: "Detroit Lions",
    team_abbreviation: "DET",
    conference: "NFC",
    division: "North",
    wins: 1,
    losses: 1,
    ties: 0,
    win_percentage: 0.5,
    points_for: 52,
    points_against: 48,
    point_differential: 4,
  },
  {
    team_id: 1,
    team_name: "Atlanta Falcons",
    team_abbreviation: "ATL",
    conference: "NFC",
    division: "South",
    wins: 2,
    losses: 0,
    ties: 0,
    win_percentage: 1.0,
    points_for: 60,
    points_against: 34,
    point_differential: 26,
  },
];

const mockSchedule = [
  {
    id: 201,
    season_id: 1,
    week: 3,
    home_team_id: 11,
    away_team_id: 1,
    scheduled_date: "2026-09-27T17:00:00Z",
    date: "2026-09-27T17:00:00Z",
    is_played: false,
    game_type: "REGULAR",
    home_score: 0,
    away_score: 0,
  },
];

test.describe("Coordinator Game-Week Prep & Laminated Call-Sheet", () => {
  test.beforeEach(async ({ page }) => {
    // Intercept API calls to supply deterministic season & matchup fixtures
    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockSummary),
      });
    });

    await page.route("**/api/teams", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockTeams),
      });
    });

    await page.route("**/api/season/1/standings", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockStandings),
      });
    });

    await page.route("**/api/season/1/schedule?week=3", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockSchedule),
      });
    });

    await page.route("**/api/season/1/leaders", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ passing: [], rushing: [], receiving: [] }),
      });
    });

    await page.route("**/api/season/1/projected-awards", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(null),
      });
    });

    await page.route("**/api/gameplan/install", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({ success: true, message: "Installed" }),
      });
    });
  });

  test("renders coordinator install pipeline, scouting report, and 4-quadrant call-sheet", async ({
    page,
  }) => {
    // Set franchise ID to Detroit Lions (11)
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "11");
    });

    await page.goto(`${BASE_URL}/season`);

    // Verify main card and header test IDs
    const summaryCard = page.getByTestId("season-summary-card");
    await expect(summaryCard).toBeVisible();

    const seasonYear = page.getByTestId("season-year");
    await expect(seasonYear).toHaveText("2026 Season");

    const currentWeek = page.getByTestId("current-week");
    await expect(currentWeek).toHaveText("Week 3");

    // Verify Monday-to-Sunday Install Pipeline
    const pipelineLabel = page.locator(".pipeline-label");
    await expect(pipelineLabel).toContainText("COORDINATOR GAME-WEEK INSTALL SCHEDULE");

    // Verify Matchup Scouting Card
    const scoutingCard = page.locator(".scouting-card");
    await expect(scoutingCard).toBeVisible();
    await expect(page.locator(".matchup-hero")).toContainText("ARI");
    await expect(page.locator(".matchup-hero")).toContainText("DET");

    // Verify 4-Quadrant Situational Call-Sheet
    const callSheet = page.locator(".callsheet-container");
    await expect(callSheet).toBeVisible();
    await expect(page.locator(".q-cyan .q-badge")).toContainText("Q1 • 1ST & 10 BASE");
    await expect(page.locator(".q-gold .q-badge")).toContainText("Q2 • 3RD & MONEY");
    await expect(page.locator(".q-emerald .q-badge")).toContainText("Q3 • RED ZONE");
    await expect(page.locator(".q-crimson .q-badge")).toContainText("Q4 • NEUTRALIZER");

    // Test clicking an option in Q1
    const insideZoneBtn = page.locator(".call-option-btn", {
      hasText: "Inside Zone Duo",
    });
    await insideZoneBtn.click();
    await expect(insideZoneBtn).toHaveClass(/selected/);

    // Test Auto-Scout button
    const autoScoutBtn = page.locator(".auto-scout-btn");
    await expect(autoScoutBtn).toBeVisible();
    await autoScoutBtn.click();

    // Test Lock Weekly Call-Sheet button
    const lockBtn = page.locator(".lock-callsheet-btn");
    await expect(lockBtn).toBeVisible();
    await lockBtn.click();
    await expect(lockBtn).toContainText("✓ Call-Sheet Locked");

    // Verify Quick Actions simulate-btn is present and clickable
    const simWeekBtn = page.getByTestId("simulate-btn");
    await expect(simWeekBtn).toBeVisible();
  });
});

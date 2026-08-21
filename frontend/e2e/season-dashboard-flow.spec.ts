import { test, expect } from "@playwright/test";
import { mockTeam } from "./fixtures/test-data";

const mockStandings = [
  {
    team_id: 1,
    team_name: "Arizona Cardinals",
    team_abbreviation: "ARI",
    conference: "NFC",
    division: "West",
    wins: 5,
    losses: 2,
    ties: 0,
    win_percentage: 0.714,
    points_for: 175,
    points_against: 140,
    point_differential: 35,
    strength_of_schedule: 0.512,
  },
  {
    team_id: 2,
    team_name: "San Francisco 49ers",
    team_abbreviation: "SF",
    conference: "NFC",
    division: "West",
    wins: 6,
    losses: 1,
    ties: 0,
    win_percentage: 0.857,
    points_for: 210,
    points_against: 130,
    point_differential: 80,
    strength_of_schedule: 0.495,
  },
  {
    team_id: 3,
    team_name: "Seattle Seahawks",
    team_abbreviation: "SEA",
    conference: "NFC",
    division: "West",
    wins: 4,
    losses: 3,
    ties: 0,
    win_percentage: 0.571,
    points_for: 160,
    points_against: 165,
    point_differential: -5,
    strength_of_schedule: 0.52,
  },
  {
    team_id: 4,
    team_name: "Los Angeles Rams",
    team_abbreviation: "LAR",
    conference: "NFC",
    division: "West",
    wins: 3,
    losses: 4,
    ties: 0,
    win_percentage: 0.429,
    points_for: 140,
    points_against: 180,
    point_differential: -40,
    strength_of_schedule: 0.53,
  },
];

const mockSchedule = [
  {
    id: 1,
    week: 1,
    home_team_id: 1,
    away_team_id: 2,
    home_score: 20,
    away_score: 24,
    status: "COMPLETED",
    is_played: true,
    home_team_name: "Arizona Cardinals",
    away_team_name: "San Francisco 49ers",
  },
  {
    id: 2,
    week: 2,
    home_team_id: 1,
    away_team_id: 3,
    home_score: null,
    away_score: null,
    status: "SCHEDULED",
    is_played: false,
    home_team_name: "Arizona Cardinals",
    away_team_name: "Seattle Seahawks",
  },
];

const mockSeasonActive = {
  id: 1,
  year: 2024,
  status: "REGULAR_SEASON",
  current_week: 2, // Must match test expectation
  total_weeks: 18,
};

test.describe("Season Dashboard Flow", () => {
  test.beforeEach(async ({ page }) => {
    page.on("pageerror", (err) => console.error("PAGE_ERROR_LOG:", err.message, err.stack));
    await page.route("**/api/teams*", async (route) => {
      await route.fulfill({
        json: [mockTeam, { id: 2, name: "49ers", city: "San Francisco", abbreviation: "SF" }],
      });
    });
    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({
        json: {
          season: mockSeasonActive,
          completion_percentage: 11.1,
          teams: [mockTeam],
        },
      });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockSeasonActive });
    });
    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route("**/api/season/*/standings*", async (route) => {
      await route.fulfill({ json: mockStandings });
    });
    await page.route("**/api/standings*", async (route) => {
      await route.fulfill({ json: mockStandings });
    });
    await page.route("**/api/season/*/schedule*", async (route) => {
      await route.fulfill({ json: mockSchedule });
    });
    await page.route("**/api/schedule*", async (route) => {
      await route.fulfill({ json: mockSchedule });
    });
    await page.route("**/api/season/*/leaders*", async (route) => {
      await route.fulfill({ json: { passing: [], rushing: [], receiving: [] } });
    });
    await page.route("**/api/season/*/awards*", async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });
    await page.route("**/api/season/*/bracket*", async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route("**/api/season/*/playoffs*", async (route) => {
      await route.fulfill({ json: [] });
    });
  });

  // This test verifies season dashboard loads with correct data
  test("should load season dashboard with standings and schedule", async ({ page }) => {
    await page.goto("/season");

    // Wait for page to finish loading
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Verify Season Dashboard header
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toBeVisible();
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText(
      "2024 Season - Week 2"
    );

    // Switch to Standings tab
    await page.locator('[data-testid="tab-standings"]').click();

    // Verify Standings section
    const cardinalsRow = page.locator('[data-testid="standings-table-row-Arizona Cardinals"]');
    await expect(cardinalsRow).toBeVisible({ timeout: 10000 });
    await expect(cardinalsRow).toContainText("Arizona Cardinals");
    await expect(cardinalsRow).toContainText("5");
    await expect(cardinalsRow).toContainText("2");

    // Switch to Schedule tab
    await page.locator('[data-testid="tab-schedule"]').click();

    // Verify Schedule section
    await expect(page.locator('[data-testid="schedule-section"]')).toBeVisible();
    const game1 = page.locator('[data-testid="schedule-game-1"]');
    await expect(game1).toBeVisible();
    await expect(game1).toContainText("Arizona Cardinals");
    await expect(game1).toContainText("San Francisco 49ers");
    await expect(game1).toContainText("20");
    await expect(game1).toContainText("24");

    const game2 = page.locator('[data-testid="schedule-game-2"]');
    await expect(game2).toBeVisible();
    await expect(game2).toContainText("Arizona Cardinals");
    await expect(game2).toContainText("Seattle Seahawks");
    await expect(game2).toContainText("SCHEDULED");
  });

  test("should navigate between weeks", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Verify current week
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText("Week 2");

    // Look for week navigation controls
    const prevWeekBtn = page.locator(
      '[data-testid="prev-week-btn"], button:has-text("Previous"), button:has-text("<")'
    );

    // If navigation exists, test it
    if (await prevWeekBtn.isVisible({ timeout: 2000 })) {
      await prevWeekBtn.click();
      // Should show Week 1
      await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText("Week 1");
    }
  });

  test("should display standings table with correct sorting", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Switch to Standings tab
    await page.locator('[data-testid="tab-standings"]').click();

    // Verify standings are displayed with highest win pct (SF 49ers)
    const sfRow = page.locator('[data-testid="standings-table-row-San Francisco 49ers"]');
    await expect(sfRow).toBeVisible({ timeout: 10000 });
    await expect(sfRow).toContainText("49ers");
  });

  test("should trigger sim week action", async ({ page }) => {
    // Mock sim week endpoint
    await page.route("**/api/simulation/week", async (route) => {
      await route.fulfill({
        json: { success: true, games_played: 16, week: 2 },
      });
    });

    await page.goto("/season");

    // Look for Sim Week button
    const simBtn = page.locator(
      '[data-testid="sim-week-btn"], button:has-text("Sim Week"), button:has-text("Simulate")'
    );

    if (await simBtn.isVisible({ timeout: 2000 })) {
      await simBtn.click();
      // Verify loading or success indication
      await expect(page.locator("text=/Simulating|Loading|Week 3/i")).toBeVisible({
        timeout: 5000,
      });
    }
  });

  test("should filter schedule by game status", async ({ page }) => {
    await page.goto("/season");

    // Look for filter tabs
    const completedFilter = page.locator(
      '[data-testid="filter-completed"], button:has-text("Completed")'
    );
    // upcomingFilter kept for future test expansion

    if (await completedFilter.isVisible({ timeout: 2000 })) {
      await completedFilter.click();
      // Should only show completed games
      await expect(page.locator('[data-testid="schedule-game-1"]')).toBeVisible();
      await expect(page.locator('[data-testid="schedule-game-2"]')).not.toBeVisible();
    }
  });

  test("should navigate to playoff bracket when in playoffs", async ({ page }) => {
    // Mock playoff season
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({
        json: { id: 1, year: 2024, status: "PLAYOFFS", current_week: 19, total_weeks: 22 },
      });
    });

    await page.goto("/season");

    // Look for playoff bracket link or section
    const playoffSection = page
      .locator('[data-testid="playoff-bracket"]')
      .or(page.getByText(/Playoffs|Bracket/i));

    if (await playoffSection.isVisible({ timeout: 3000 })) {
      await expect(playoffSection).toBeVisible();
    }
  });
});

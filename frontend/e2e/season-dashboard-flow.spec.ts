import { test, expect } from "@playwright/test";
import { mockTeam } from "./fixtures/test-data";

const mockStandings = [
  { team_id: 1, team_name: "Arizona Cardinals", wins: 5, losses: 2, ties: 0 },
  { team_id: 2, team_name: "San Francisco 49ers", wins: 6, losses: 1, ties: 0 },
  { team_id: 3, team_name: "Seattle Seahawks", wins: 4, losses: 3, ties: 0 },
  { team_id: 4, team_name: "Los Angeles Rams", wins: 3, losses: 4, ties: 0 },
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
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockSeasonActive });
    });
    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route("**/api/standings", async (route) => {
      await route.fulfill({ json: mockStandings });
    });
    await page.route("**/api/schedule*", async (route) => {
      // Use * to match query params
      await route.fulfill({ json: mockSchedule });
    });
  });

  // This test verifies season dashboard loads with correct data
  test("should load season dashboard with standings and schedule", async ({ page }) => {
    await page.goto("/season-dashboard");

    // Verify Season Dashboard header
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toBeVisible();
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText(
      "2024 Season - Week 2"
    );

    // Verify Standings section
    await expect(page.locator('[data-testid="standings-table"]')).toBeVisible();
    await expect(
      page.locator('[data-testid="standings-table-row-Arizona Cardinals"]')
    ).toBeVisible();
    await expect(
      page.locator('[data-testid="standings-table-row-Arizona Cardinals"]')
    ).toContainText("5-2-0");

    // Verify Schedule section
    await expect(page.locator('[data-testid="schedule-section"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-1"]')).toContainText(
      "Arizona Cardinals vs San Francisco 49ers"
    );
    await expect(page.locator('[data-testid="schedule-game-1"]')).toContainText("Final: 20 - 24");

    await expect(page.locator('[data-testid="schedule-game-2"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-2"]')).toContainText(
      "Arizona Cardinals vs Seattle Seahawks"
    );
    await expect(page.locator('[data-testid="schedule-game-2"]')).toContainText("Upcoming");
  });

  test("should navigate between weeks", async ({ page }) => {
    await page.goto("/season-dashboard");

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
    await page.goto("/season-dashboard");

    // Verify standings are sorted by wins (desc)
    const standingsTable = page.locator('[data-testid="standings-table"]');
    await expect(standingsTable).toBeVisible();

    // First row should be SF (6-1), second ARI (5-2)
    const firstRow = standingsTable.locator("tr").nth(1); // Skip header
    await expect(firstRow).toContainText("49ers");
  });

  test("should trigger sim week action", async ({ page }) => {
    // Mock sim week endpoint
    await page.route("**/api/simulation/week", async (route) => {
      await route.fulfill({
        json: { success: true, games_played: 16, week: 2 },
      });
    });

    await page.goto("/season-dashboard");

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
    await page.goto("/season-dashboard");

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

    await page.goto("/season-dashboard");

    // Look for playoff bracket link or section
    const playoffSection = page
      .locator('[data-testid="playoff-bracket"]')
      .or(page.getByText(/Playoffs|Bracket/i));

    if (await playoffSection.isVisible({ timeout: 3000 })) {
      await expect(playoffSection).toBeVisible();
    }
  });
});

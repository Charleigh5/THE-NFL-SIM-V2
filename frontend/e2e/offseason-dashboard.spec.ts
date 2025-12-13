import { test, expect } from "@playwright/test";

const mockOffseasonSeason = {
  id: 1,
  year: 2024,
  status: "OFF_SEASON",
  current_week: 0,
};

test.describe("Offseason Dashboard Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Ensure settings resolves so the page doesn't redirect.
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({
        json: { user_team_id: 1, difficulty_level: "Pro", game_speed: "medium" },
      });
    });

    // Ensure user team resolves quickly.
    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          city: "Arizona",
          name: "Cardinals",
          abbreviation: "ARI",
          conference: "NFC",
          division: "West",
          wins: 0,
          losses: 0,
          salary_cap_space: 25000000,
        },
      });
    });

    // Mock the current season to be in OFF_SEASON status
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockOffseasonSeason });
    });

    // Mock season summary for general dashboard info
    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({ json: { season: mockOffseasonSeason, completion_percentage: 100 } });
    });

    // Keep additional offseason fetches fast (page still renders without them,
    // but some environments can hang on network timeouts).
    await page.route("**/api/season/1/offseason/prospects*", async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route("**/api/season/1/offseason/needs/1*", async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route("**/api/season/team/1/salary-cap*", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          team_name: "Arizona Cardinals",
          total_cap: 220000000,
          used_cap: 180000000,
          available_cap: 40000000,
          cap_percentage: 81.8,
          top_contracts: [],
          position_breakdown: [],
          league_avg_available: 0,
          projected_rookie_impact: 0,
        },
      });
    });
  });

  test("should load the Offseason Dashboard correctly", async ({ page }) => {
    await page.goto("/offseason");

    // Verify the Offseason Dashboard header is visible
    await expect(page.locator("h1", { hasText: "Offseason Dashboard" })).toBeVisible();
    await expect(page.locator("p", { hasText: "Prepare for the next season." })).toBeVisible();

    // Verify that offseason specific elements are visible
    await expect(page.locator('[data-testid="offseason-phase-display"]')).toBeVisible();
    await expect(page.locator('[data-testid="offseason-phase-display"]')).toContainText(
      "Current Phase: OFF_SEASON"
    );

    // Verify navigation links/buttons for offseason activities
    await expect(page.locator("a", { hasText: "Draft Room" })).toBeVisible();
    // Add checks for Free Agency once implemented
    // await expect(page.locator('a', { hasText: 'Free Agency' })).toBeVisible();
  });

  test("should navigate to Draft Room from Offseason Dashboard", async ({ page }) => {
    await page.goto("/offseason");

    // Ensure the Draft Room link is visible
    const draftRoomLink = page.locator("a", { hasText: "Draft Room" });
    await expect(draftRoomLink).toBeVisible();

    // Click the Draft Room link and wait for navigation
    const navigationPromise = page.waitForURL("/offseason/draft");
    await draftRoomLink.click();
    await navigationPromise;

    // Verify that the Draft Room page has loaded
    await expect(page.locator("h1", { hasText: "Draft Room" })).toBeVisible();
  });
});

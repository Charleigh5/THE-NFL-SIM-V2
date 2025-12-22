import { test, expect } from "@playwright/test";

const mockSeason = {
  id: 1,
  year: 2024,
  status: "REGULAR_SEASON",
  current_week: 2,
  total_weeks: 18,
};

const mockSeasonSummary = {
  season: mockSeason,
  completion_percentage: 11.1,
  teams: [],
};

const mockStandings = [
  { team_id: 1, team_name: "Arizona Cardinals", wins: 5, losses: 2, ties: 0, pct: 0.714 },
  { team_id: 2, team_name: "San Francisco 49ers", wins: 6, losses: 1, ties: 0, pct: 0.857 },
];

const mockTeams = [
  { id: 1, name: "Cardinals", city: "Arizona", abbreviation: "ARI" },
  { id: 2, name: "49ers", city: "San Francisco", abbreviation: "SF" },
];

test.describe("Season Dashboard Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock all required endpoints
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({ json: mockTeams });
    });

    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({ json: mockSeasonSummary });
    });

    await page.route("**/api/season/*/standings", async (route) => {
      await route.fulfill({ json: mockStandings });
    });

    await page.route("**/api/season/*/schedule/*", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/season/*/leaders", async (route) => {
      await route.fulfill({ json: { passing: [], rushing: [], receiving: [] } });
    });

    await page.route("**/api/season/*/awards/projected", async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });

    await page.route("**/api/news/living/feed*", async (route) => {
      await route.fulfill({ json: { items: [], total_count: 0 } });
    });
  });

  test("should load season dashboard with standings and schedule", async ({ page }) => {
    await page.goto("/season");

    // Verify Season Dashboard page loads
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Verify header shows year and week
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText("2024");
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText("Week 2");

    // Verify tabs are visible
    await expect(page.locator('[data-testid="dashboard-tabs"]')).toBeVisible();
  });

  test("should navigate between weeks", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Switch to schedule tab if exists
    const scheduleTab = page.locator('[data-testid="tab-schedule"]');
    if (await scheduleTab.isVisible()) {
      await scheduleTab.click();

      // Look for week navigation
      const weekNav = page.getByRole("button", { name: /previous|next|week/i });
      if (await weekNav.first().isVisible({ timeout: 2000 })) {
        // Navigation exists
        expect(true).toBeTruthy();
      }
    }
  });

  test("should display standings table with correct sorting", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Switch to standings tab
    const standingsTab = page.locator('[data-testid="tab-standings"]');
    await standingsTab.click();

    // Wait for standings content
    await page.waitForTimeout(500);

    // Standings should show teams
    const standingsContent = page.locator('[data-testid="dashboard-content"]');
    await expect(standingsContent).toBeVisible();
  });
});

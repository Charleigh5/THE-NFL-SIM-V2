import { test, expect } from "@playwright/test";

test.describe("Offseason Dashboard", () => {
  test.beforeEach(async ({ page }) => {
    // Mock the current season to be in OFF_SEASON
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          year: 2024,
          current_week: 18,
          is_active: true,
          status: "OFF_SEASON",
          total_weeks: 17,
          playoff_weeks: 4,
        },
      });
    });

    // Mock teams
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({
        json: [
          { id: 1, name: "Team 1", abbreviation: "T1", conference: "C1", division: "D1" },
          { id: 2, name: "Team 2", abbreviation: "T2", conference: "C1", division: "D1" },
        ],
      });
    });

    // Mock Team Needs
    await page.route("**/needs/enhanced/**", async (route) => {
      await route.fulfill({
        json: [
          { position: "QB", priority: "High", score: 80, description: "Need a starter" },
          { position: "WR", priority: "Medium", score: 50, description: "Depth needed" },
        ],
      });
    });

    // Mock Prospects
    await page.route("**/prospects**", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 101,
            name: "Rookie One",
            position: "QB",
            college: "State U",
            overall: 85,
            projected_round: 1,
          },
          {
            id: 102,
            name: "Rookie Two",
            position: "DE",
            college: "Tech",
            overall: 82,
            projected_round: 1,
          },
        ],
      });
    });

    // Mock Salary Cap
    await page.route("**/cap/**", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          season_id: 1,
          cap_space: 15000000,
          total_cap: 200000000,
          dead_cap: 5000000,
          active_cap: 180000000,
        },
      });
    });

    // Mock Actions (Start Offseason, etc.)
    await page.route("**/api/season/*/offseason/start", async (route) => {
      await route.fulfill({ status: 200, json: { success: true } });
    });

    await page.route("**/api/season/*/offseason/simulate-progression", async (route) => {
      await route.fulfill({ status: 200, json: [] });
    });

    await page.route("**/api/season/*/offseason/simulate-draft", async (route) => {
      await route.fulfill({ status: 200, json: [] });
    });

    await page.route("**/api/season/*/offseason/simulate-free-agency", async (route) => {
      await route.fulfill({ status: 200, json: [] });
    });

    // Navigate to the page (assuming route is /offseason)
    await page.goto("/offseason");
  });

  test("should load the offseason dashboard components", async ({ page }) => {
    // Verify Title
    await expect(page.getByRole("heading", { name: "Offseason Dashboard" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "2024 Offseason" })).toBeVisible();

    // Verify Timeline
    await expect(page.locator(".offseason-timeline")).toBeVisible();

    // Verify Team Needs
    await expect(page.getByText("Need a starter")).toBeVisible();

    // Verify Draft Board
    await expect(page.getByText("Rookie One")).toBeVisible();

    // Verify Salary Cap Widget
    await expect(page.getByText("Cap Space:")).toBeVisible();
  });

  test("should allow starting the offseason", async ({ page }) => {
    const startBtn = page.getByRole("button", { name: "Start Offseason" });
    await expect(startBtn).toBeVisible();
    await startBtn.click();
    await expect(page.getByText("Offseason started!")).toBeVisible();
  });
});

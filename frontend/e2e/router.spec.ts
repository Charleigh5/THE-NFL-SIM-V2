import { test, expect } from "@playwright/test";

test.describe("Router Navigation", () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { id: 1, name: "Test Team", city: "Test City", abbreviation: "TST" },
        ]),
      });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: 1,
          year: 2025,
          current_week: 1,
          status: "REGULAR_SEASON",
          is_active: true,
        }),
      });
    });

    await page.route("**/api/season/1/summary", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          season: { id: 1, year: 2025, current_week: 1, status: "REGULAR_SEASON" },
          completion_percentage: 0,
        }),
      });
    });

    // Mock other season endpoints
    await page.route("**/api/season/1/standings", async (route) => route.fulfill({ json: [] }));
    await page.route("**/api/season/1/schedule?week=1", async (route) =>
      route.fulfill({ json: [] })
    );
    await page.route("**/api/season/1/leaders", async (route) =>
      route.fulfill({ json: { passing_yards: [] } })
    );
    await page.route("**/api/season/1/awards/projected", async (route) =>
      route.fulfill({ json: {} })
    );
  });

  test("should navigate to Dashboard", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL("/");
    // Add assertion for dashboard content if known
  });

  test("should navigate to Team Selection", async ({ page }) => {
    await page.goto("/team-selection");
    await expect(page).toHaveURL("/team-selection");
    await expect(page.getByText(/Test Team/)).toBeVisible();
  });

  test("should navigate to Season Dashboard", async ({ page }) => {
    await page.goto("/season");
    await expect(page).toHaveURL("/season");
  });

  test("should handle 404", async ({ page }) => {
    await page.goto("/non-existent-route");
    await expect(page.getByText("404")).toBeVisible(); // Assuming NotFound component shows 404
  });
});

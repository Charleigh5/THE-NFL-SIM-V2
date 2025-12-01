import { test, expect } from "@playwright/test";

test.describe("Schedule View", () => {
  test.beforeEach(async ({ page }) => {
    // Mock Schedule Response
    await page.route("**/api/season/*/schedule", async (route) => {
      await route.fulfill({
        json: [
          {
            week: 1,
            games: [
              {
                id: 1,
                home_team: { name: "Team 1", abbreviation: "T1" },
                away_team: { name: "Team 2", abbreviation: "T2" },
                home_score: 21,
                away_score: 17,
                is_played: true,
              },
            ],
          },
          {
            week: 2,
            games: [
              {
                id: 2,
                home_team: { name: "Team 1", abbreviation: "T1" },
                away_team: { name: "Team 3", abbreviation: "T3" },
                is_played: false,
              },
            ],
          },
        ],
      });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({
        json: { id: 1, year: 2024, current_week: 2, is_active: true, status: "REGULAR_SEASON" },
      });
    });

    await page.goto("/schedule");
  });

  test("should display the season schedule", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Schedule" })).toBeVisible();

    // Check for Week 1 results
    await expect(page.getByText("Week 1")).toBeVisible();
    await expect(page.getByText("T1 21 - 17 T2")).toBeVisible();

    // Check for Week 2 upcoming
    await expect(page.getByText("Week 2")).toBeVisible();
    await expect(page.getByText("T1 vs T3")).toBeVisible();
  });
});

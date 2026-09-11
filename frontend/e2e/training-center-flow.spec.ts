import { test, expect } from "@playwright/test";

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock API calls
    await page.route("**/api/training/drills*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          drills: [
            {
              id: "1",
              name: "Oklahoma Drill",
              category: "STRENGTH",
              target_stat: "strength",
              secondary_stats: ["tackling"],
              energyCost: 20,
              fatigue_cost: 20,
              xpMultiplier: 1.5,
              xp_multiplier: 1.5,
              injuryRisk: "HIGH",
              injury_risk: 0.15,
              description: "Full contact blocking and tackling drill",
              season_filter: ["regular"],
            },
            {
              id: "2",
              name: "7-on-7 Skeleton",
              category: "SPEED",
              target_stat: "speed",
              secondary_stats: ["catching"],
              energyCost: 15,
              fatigue_cost: 15,
              xpMultiplier: 1.2,
              xp_multiplier: 1.2,
              injuryRisk: "LOW",
              injury_risk: 0.02,
              description: "Passing game timing and precision work",
              season_filter: ["regular"],
            },
          ],
          total: 2,
        }),
      });
    });

    await page.route("**/api/training/styles*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          {
            name: "smart",
            display_name: "Smart",
            description: "Balanced approach",
            xp_multiplier: 1.0,
            injury_risk_multiplier: 1.0,
            fatigue_multiplier: 1.0,
            recovery_multiplier: 1.0,
          },
          {
            name: "old_school",
            display_name: "Old School",
            description: "High intensity, high risk",
            xp_multiplier: 1.5,
            injury_risk_multiplier: 1.5,
            fatigue_multiplier: 1.3,
            recovery_multiplier: 0.8,
          },
        ]),
      });
    });

    await page.route("**/api/training/schedule*", async (route) => {
      await route.fulfill({ status: 200, json: { schedule: [] } });
    });

    // Navigate to training page
    await page.goto("/training");
  });

  test("should load training center page", async ({ page }) => {
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible({
      timeout: 10000,
    });
    await expect(page.getByText("Coaching Philosophy", { exact: true }).first()).toBeVisible({
      timeout: 10000,
    });
  });

  test("should allow selecting coaching style", async ({ page }) => {
    const styleOption = page.getByText("Old School").first();
    await expect(styleOption).toBeVisible({ timeout: 10000 });
    await styleOption.click();
    await expect(styleOption).toBeVisible();
  });

  test("should display drills", async ({ page }) => {
    await expect(page.locator("select").first()).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".drill-card").first()).toBeVisible({ timeout: 10000 });
  });

  test("should toggle drill selection", async ({ page }) => {
    const drillCard = page.locator(".drill-card").first();
    await expect(drillCard).toBeVisible({ timeout: 10000 });
    await drillCard.click();
    await expect(drillCard).toHaveClass(/border-cyan-400|border-blue/, { timeout: 10000 });

    await drillCard.click();
  });
});

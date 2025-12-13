import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Training Center
 * Covers: Page load, coach display, coaching philosophy, drill catalog
 */

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock training drills API
    await page.route("**/api/training/drills**", async (route) => {
      await route.fulfill({
        json: [
          {
            id: "sprint-1",
            name: "40-Yard Dash",
            category: "SPEED",
            position: "ALL",
            xp_gain: 25,
            fatigue_cost: 15,
            injury_risk: 0.02,
            description: "Explosive speed training",
          },
          {
            id: "tackle-1",
            name: "Tackling Drill",
            category: "FUNDAMENTALS",
            position: "DEF",
            xp_gain: 20,
            fatigue_cost: 20,
            injury_risk: 0.05,
            description: "Form tackling practice",
          },
          {
            id: "route-1",
            name: "Route Running",
            category: "SKILL",
            position: "WR",
            xp_gain: 30,
            fatigue_cost: 10,
            injury_risk: 0.01,
            description: "Precision route running",
          },
        ],
      });
    });

    // Mock training schedule API
    await page.route("**/api/training/schedule**", async (route) => {
      await route.fulfill({
        json: {
          coachingStyle: "SMART",
          weeklyLoad: 75,
          fatigueLevel: 20,
        },
      });
    });

    // Mock execute training API
    await page.route("**/api/training/execute**", async (route) => {
      await route.fulfill({
        json: {
          success: true,
          results: {
            xpGained: 150,
            fatigueIncrease: 25,
            injuriesOccurred: 0,
          },
        },
      });
    });

    // Mock coaching style update
    await page.route("**/api/training/coaching-style**", async (route) => {
      await route.fulfill({
        json: { success: true },
      });
    });
  });

  test("should load training center page", async ({ page }) => {
    await page.goto("/training");

    // Verify page loaded
    await expect(page.getByRole("heading", { name: "Training Center" })).toBeVisible();

    // Verify main sections exist
    await expect(page.getByRole("heading", { name: "Head Coach" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Coaching Philosophy" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "Drill Catalog" })).toBeVisible();
  });

  test("should display coach card component", async ({ page }) => {
    await page.goto("/training");

    // Verify coach card shows coach info
    await expect(page.locator("text=Andy Reid")).toBeVisible();
    await expect(page.getByRole("heading", { name: "Head Coach" })).toBeVisible();
  });

  test("should display drill cards from API", async ({ page }) => {
    await page.goto("/training");

    await page.waitForResponse("**/api/training/drills**");

    // Wait for drills to load
    await expect(page.locator("text=40-Yard Dash")).toBeVisible();
    await expect(page.locator("text=Tackling Drill")).toBeVisible();
    await expect(page.locator("text=Route Running")).toBeVisible();
  });

  test("should have execute week button", async ({ page }) => {
    await page.goto("/training");

    // Verify execute button exists
    const executeBtn = page.locator("text=Execute Week");
    await expect(executeBtn).toBeVisible();
    await expect(executeBtn).toBeEnabled();
  });

  test("should show coaching style picker", async ({ page }) => {
    await page.goto("/training");

    // Verify coaching philosophy section
    await expect(page.locator("text=Coaching Philosophy")).toBeVisible();

    // CoachingStylePicker should be present
    // The picker likely has style options
    await expect(page.locator("text=SMART").or(page.locator("text=Smart"))).toBeVisible();
  });
});

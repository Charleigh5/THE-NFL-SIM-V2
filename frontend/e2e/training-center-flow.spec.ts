import { test, expect } from "@playwright/test";

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock coaching styles API
    await page.route("**/api/v1/training/coaching-styles", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { id: "smart", name: "Smart", description: "Balanced approach", xpModifier: 1.0 },
          {
            id: "aggressive",
            name: "Aggressive",
            description: "High risk high reward",
            xpModifier: 1.3,
          },
          {
            id: "conservative",
            name: "Conservative",
            description: "Safe and steady",
            xpModifier: 0.8,
          },
        ]),
      });
    });

    // Mock drills API
    await page.route("**/api/v1/training/drills**", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          {
            id: "1",
            name: "Oklahoma Drill",
            category: "CONTACT",
            target_stat: "Strength",
            description: "High intensity blocking drill",
            xp_multiplier: 1.5,
            injury_risk: 0.1,
          },
          {
            id: "2",
            name: "7-on-7 Skeleton",
            category: "PASSING",
            target_stat: "Route Running",
            description: "Passing game practice",
            xp_multiplier: 1.2,
            injury_risk: 0.03,
          },
        ]),
      });
    });

    await page.route("**/api/v1/training/schedule", async (route) => {
      await route.fulfill({ status: 200, body: JSON.stringify({ currentWait: 0 }) });
    });

    // Navigate to training page
    await page.goto("/training");
  });

  test("should load training center page", async ({ page }) => {
    // Check for Training Center heading (uppercase in UI)
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible();
  });

  test("should display coaching style selector", async ({ page }) => {
    // Wait for styles to load
    await page.waitForTimeout(500);

    // Coaching style selector should be visible
    await expect(page.getByText("Smart")).toBeVisible();
  });

  test("should display drills", async ({ page }) => {
    // Wait for drills to load
    await expect(page.getByText("Oklahoma Drill")).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("7-on-7 Skeleton")).toBeVisible();
  });

  test("should select a drill and show action panel", async ({ page }) => {
    // Wait for drills to load
    await page.getByText("Oklahoma Drill").click({ timeout: 10000 });

    // Action panel should appear with drill details
    await expect(page.getByRole("button", { name: /initiate sequence/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /cancel/i })).toBeVisible();
  });
});

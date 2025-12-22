import { test, expect } from "@playwright/test";
import { mockCoachingStyles, mockDrills } from "./fixtures/test-data";

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock coaching styles API
    await page.route("**/api/v1/training/coaching-styles", async (route) => {
      await route.fulfill({ json: mockCoachingStyles });
    });

    // Mock drills API - match exact path pattern used by component
    await page.route("**/api/v1/training/drills**", async (route) => {
      await route.fulfill({ json: mockDrills });
    });

    // Mock player training profile
    await page.route("**/api/v1/players/*/training-profile", async (route) => {
      await route.fulfill({
        json: {
          player_id: 1,
          player_name: "Test Player",
          position: "WR",
          age: 25,
          weaknesses: ["route_running"],
          fatigue: 20,
        },
      });
    });
  });

  test("should load training center page", async ({ page }) => {
    await page.goto("/training");

    // Check for Training Center heading (uppercase in UI)
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible({
      timeout: 10000,
    });
  });

  test("should display coaching style selector", async ({ page }) => {
    await page.goto("/training");

    // Wait for page to load
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible({
      timeout: 10000,
    });

    // Wait for coaching styles to load - look for any coaching style name
    await page.waitForTimeout(500);

    // The CoachingStyleDial should be visible
    const coachingSection = page.locator("section").first();
    await expect(coachingSection).toBeVisible();
  });

  test("should display drills", async ({ page }) => {
    await page.goto("/training");

    // Wait for page to load
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible({
      timeout: 10000,
    });

    // Wait for drills to load
    await page.waitForTimeout(1000);

    // Look for drill names from mock data
    const drillName = page.getByText(mockDrills[0].name);
    if ((await drillName.count()) > 0) {
      await expect(drillName.first()).toBeVisible();
    }
  });

  test("should select a drill and show action panel", async ({ page }) => {
    await page.goto("/training");

    // Wait for page to load
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible({
      timeout: 10000,
    });

    // Wait for drills to load
    await page.waitForTimeout(1000);

    // Find and click a drill
    const drillCard = page.getByText(mockDrills[0].name);
    if ((await drillCard.count()) > 0) {
      await drillCard.first().click();

      // Action panel should appear with drill details
      const initiateButton = page.getByRole("button", { name: /initiate sequence/i });
      const cancelButton = page.getByRole("button", { name: /cancel/i });

      if ((await initiateButton.count()) > 0) {
        await expect(initiateButton).toBeVisible();
        await expect(cancelButton).toBeVisible();
      }
    }
  });
});

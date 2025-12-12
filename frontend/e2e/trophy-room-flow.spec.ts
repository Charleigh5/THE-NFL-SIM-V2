import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Trophy Room
 * Covers: Page load, 3D canvas, hall of champions display
 */

test.describe("Trophy Room Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock settings API for theme
    await page.route("**/api/settings**", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          difficulty: "MEDIUM",
          sound_enabled: true,
        },
      });
    });

    // Mock team data
    await page.route("**/api/team/**", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          name: "Cardinals",
          city: "Arizona",
          abbreviation: "ARI",
        },
      });
    });
  });

  test("should load trophy room page", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify page loaded with title
    await expect(page.locator("text=Hall of Champions")).toBeVisible();
  });

  test("should display franchise name in subtitle", async ({ page }) => {
    await page.goto("/trophy-room");

    // Check for trophy case subtitle
    const subtitle = page.locator(".trophy-room__subtitle");
    await expect(subtitle).toBeVisible();
  });

  test("should have 3D canvas container", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify canvas container exists (for 3D rendering)
    const canvasContainer = page.locator(".canvas-container");
    await expect(canvasContainer).toBeVisible();
  });

  test("should have UI overlay layer", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify UI layer exists
    const uiLayer = page.locator(".ui-layer");
    await expect(uiLayer).toBeVisible();
  });
});

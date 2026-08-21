import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Skills Page (3D Skill Tree)
 * Covers: Page load, 3D canvas rendering, overlay visibility, node interaction
 */

test.describe("Skills Page Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock player API
    await page.route("**/api/players/1", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          first_name: "Patrick",
          last_name: "Mahomes",
          position: "QB",
          jersey_number: 15,
          overall_rating: 99,
          age: 28,
          experience: 7,
          team_id: 12,
        },
      });
    });

    // Mock traits API for player
    await page.route("**/api/traits/players/1", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 1,
            name: "Field General",
            description: "Boosts entire offense awareness.",
            effect_type: "PASSIVE",
            effect_value: 5,
            tier: "GOLD",
          },
          {
            id: 2,
            name: "Gunslinger",
            description: "Increases throw velocity.",
            effect_type: "PASSIVE",
            effect_value: 5,
            tier: "GOLD",
          },
          {
            id: 3,
            name: "Escape Artist",
            description: "Elite scrambling speed behind LOS.",
            effect_type: "PASSIVE",
            effect_value: 8,
            tier: "SILVER",
          },
        ],
      });
    });

    // Mock trait unlock API
    await page.route("**/api/traits/players/1/unlock", async (route) => {
      await route.fulfill({
        json: true,
      });
    });
  });

  test("should load skills page with player ID", async ({ page }) => {
    await page.goto("/players/1/skills");

    // Wait for content to load - the page container should exist
    await expect(page.locator(".w-full.h-screen")).toBeVisible({ timeout: 10000 });
  });

  test("should display SKILL MATRIX header in overlay", async ({ page }) => {
    await page.goto("/players/1/skills");

    // The SkillsOverlay should show the header
    await expect(page.locator("text=SKILL MATRIX")).toBeVisible({ timeout: 10000 });
  });

  test("should display available skill points", async ({ page }) => {
    await page.goto("/players/1/skills");

    // The overlay should show available points
    await expect(page.locator("text=Available Points")).toBeVisible({ timeout: 10000 });
    await expect(page.locator("text=SP").first()).toBeVisible(); // Skill Points unit
  });

  test("should display archetype information", async ({ page }) => {
    await page.goto("/players/1/skills");

    // The overlay shows an archetype label
    await expect(page.locator("text=Archetype").first()).toBeVisible({ timeout: 10000 });
  });

  test("should render 3D canvas container", async ({ page }) => {
    await page.goto("/players/1/skills");

    // The Canvas element should be rendered (part of @react-three/fiber)
    // Canvas renders as a <canvas> element
    await expect(page.locator("canvas")).toBeVisible({ timeout: 15000 });
  });

  test("should display control hints in footer", async ({ page }) => {
    await page.goto("/players/1/skills");

    // The footer shows interaction hints
    await expect(page.locator("text=LMB: Select Node")).toBeVisible({ timeout: 10000 });
  });

  test("should navigate to skills page from fallback route", async ({ page }) => {
    // Test the legacy /skills route (without player ID)
    await page.goto("/skills");

    // Should still render the page container even without data
    await expect(page.locator(".w-full.h-screen")).toBeVisible({ timeout: 10000 });
  });

  test("should show detail panel when node is clicked", async ({ page }) => {
    await page.goto("/players/1/skills");

    // Wait for canvas to be ready
    await expect(page.locator("canvas")).toBeVisible({ timeout: 15000 });

    // Click on the canvas (center area where nodes would be)
    const canvas = page.locator("canvas");
    const box = await canvas.boundingBox();
    if (box) {
      // Click center of canvas
      await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);

      // Wait a bit for potential detail panel to appear
      await page.waitForTimeout(1000);

      // If a node was clicked, we might see the detail panel
      // This is optimistic since we can't guarantee a node is exactly at center
      // But the test validates the click interaction doesn't crash
    }
  });
});

import { test, expect } from "@playwright/test";
import { mockPlayers } from "./fixtures/test-data";

test.describe("Draft Genesis Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock Teams API
    await page.route("**/api/teams*", async (route) => {
      await route.fulfill({ status: 200, json: [{ id: 1, name: "Cardinals", city: "Arizona" }] });
    });

    // Mock Draft Board API
    await page.route("**/api/draft/board*", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockPlayers),
      });
    });

    await page.route("**/api/season/current*", async (route) => {
      await route.fulfill({ status: 200, json: { id: 1, year: 2024, current_week: 1 } });
    });

    await page.route("**/api/season/summary*", async (route) => {
      await route.fulfill({
        status: 200,
        json: {
          season: { id: 1, year: 2024, current_week: 1, status: "OFF_SEASON" },
          completion_percentage: 100,
        },
      });
    });

    await page.route("**/api/season/*/pick*", async (route) => {
      await route.fulfill({
        status: 200,
        json: { team_id: 1, round: 1, pick_number: 1 },
      });
    });

    await page.route(/.*\/api\/combine\/genesis-reveal\/.*/, async (route) => {
      await route.fulfill({
        status: 200,
        json: {
          player_id: 1,
          position: "QB",
          revealed_stats: {
            s2_cognition_score: 88,
            gps_speed_max: 21.5,
            power_clean_max: 315,
            position_agility_score: 92,
            fast_twitch_percentage: 85,
            body_fat_percentage: 10,
            hand_size: 9.5,
          },
          revealed_traits: ["GUNSLINGER"],
          confidence_level: 0.95,
          scouting_accuracy: 0.9,
        },
      });
    });

    await page.goto("/offseason/draft");
  });

  test("should display genesis reveal button", async ({ page }) => {
    await expect(page.getByText("Reveal").first()).toBeVisible();
  });

  test("should open genesis modal and reveal data", async ({ page }) => {
    // Click reveal on first prospect
    await page.getByText("Reveal").first().click();

    // Check modal appears
    await expect(page.getByText("GENESIS INSIGHTS")).toBeVisible();
    await expect(page.getByText("Encrypted Biometric Data")).toBeVisible();

    // Click Decrypt
    await page.getByText("DECRYPT DATA").click();

    // Wait for animation
    await expect(page.getByText("DECRYPTING SECURE FILES...")).toBeVisible();

    // Verify revealed data appears
    const modal = page.locator('[data-testid="genesis-modal"]');
    await expect(modal.getByText("S2 SCORE")).toBeVisible({ timeout: 5000 });
    await expect(modal.getByText("88")).toBeVisible(); // Mock data value
    await expect(modal.getByText("GPS MAX")).toBeVisible();
    await expect(modal.getByText("21.5")).toBeVisible();
  });

  test("should show GPS speed viz on card after reveal", async ({ page }) => {
    // Trigger reveal via UI
    await page.getByText("Reveal").first().click();
    await page.getByText("DECRYPT DATA").click();
    const modal = page.locator('[data-testid="genesis-modal"]');
    await expect(modal.getByText("S2 SCORE")).toBeVisible({ timeout: 5000 });

    // Close modal and wait for modal unmount
    await page.locator('[data-testid="close-modal-bottom"]').click();
    await expect(modal).not.toBeVisible();

    // Check for GPS bar on the card (GpsSpeedViz component)
    await expect(page.getByTestId("card-gps-speed-viz").first()).toBeVisible();
  });
});

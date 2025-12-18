import { test, expect } from "@playwright/test";
import { mockPlayers } from "./fixtures/test-data";

test.describe("Draft Genesis Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock Draft Board API
    await page.route("**/api/v1/draft/board", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(mockPlayers),
      });
    });

    await page.route("**/api/v1/season/current", async (route) => {
      await route.fulfill({ status: 200, body: JSON.stringify({ id: 1 }) });
    });

    await page.route("**/api/v1/season/1/pick", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ team_id: 1, round: 1, pick_number: 1 }),
      });
    });

    await page.goto("http://localhost:5173/offseason/draft");
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
    await expect(page.getByText("S2 SCORE")).toBeVisible({ timeout: 5000 });
    await expect(page.getByText("88")).toBeVisible(); // Mock data value
    await expect(page.getByText("GPS MAX")).toBeVisible();
    await expect(page.getByText("21.5")).toBeVisible();
  });

  test("should show GPS speed viz on card after reveal", async ({ page }) => {
    // Trigger reveal via UI
    await page.getByText("Reveal").first().click();
    await page.getByText("DECRYPT DATA").click();
    await expect(page.getByText("S2 SCORE")).toBeVisible({ timeout: 5000 });

    // Close modal
    await page.getByRole("button", { name: "✕" }).click();

    // Check for GPS bar on the card (GpsSpeedViz component)
    await expect(page.locator(".gps-speed-fill").first()).toBeVisible();
  });
});

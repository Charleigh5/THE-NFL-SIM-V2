import { test, expect } from "@playwright/test";
import { TestHelpers } from "./test-helpers";

test.describe("Season Management", () => {
  test.beforeEach(async ({ request }) => {
    // Ensure database is in a clean state with initial data
    await TestHelpers.seedDatabase(request);
  });

  test("Start New Season Flow", async ({ page }) => {
    // 1. Navigate to dashboard
    await page.goto("/");

    // 2. Verify "Start Season" button is visible
    const startButton = page.locator(".start-season-btn");
    await expect(startButton).toBeVisible();
    await expect(startButton).toHaveText(/Start (Next )?Season/);

    // 3. Click "Start Season" button
    const initResponsePromise = page.waitForResponse(
      (response) => response.url().includes("/api/season/init") && response.status() === 200
    );
    await startButton.click();
    const initResponse = await initResponsePromise;
    const seasonData = await initResponse.json();
    expect(seasonData.current_week).toBe(1);
    expect(seasonData.year).toBeGreaterThan(2020);

    // 4. Wait for page to reload/update
    // The button click triggers a reload, so we wait for the page to stabilize
    await page.waitForLoadState("networkidle");

    // 5. Verify season created (check for season year indicator or updated button text)
    // If a season is started, the button might change to "Start Next Season" or disappear depending on logic,
    // but based on Dashboard.tsx, it shows "Start Next Season" if currentSeason exists.
    // Also, usually there's a season indicator somewhere, but looking at Dashboard.tsx,
    // it doesn't seem to explicitly show "Season 2025" in the header,
    // but maybe the "Mission Control" or other components show it.
    // However, the button text changing is a good indicator.
    await expect(page.locator(".start-season-btn")).toHaveText("Start Next Season");

    // 6. Verify teams are loaded (check dashboard displays no errors)
    await TestHelpers.verifyDashboardLoaded(page);
  });
});

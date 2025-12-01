import { test, expect } from "@playwright/test";
import { TestHelpers } from "./test-helpers";

test.describe("Season Progression and Standings", () => {
  test.beforeEach(async ({ request, page }) => {
    await TestHelpers.seedDatabase(request);
    await page.goto("/");
    // Ensure a season is initialized before running tests that depend on it
    const startButton = page.locator(".start-season-btn");
    if (await startButton.isVisible()) {
      await startButton.click();
      await page.waitForResponse(
        (response) => response.url().includes("/api/season/init") && response.status() === 200
      );
      await page.waitForLoadState("networkidle");
    }
  });

  test("should advance week and update season status", async ({ page }) => {
    // Get initial week number
    const initialWeekText = await page.locator(".season-status span:has-text('Week')").innerText();
    const initialWeekMatch = initialWeekText.match(/Week (\d+)/);
    expect(initialWeekMatch).toBeDefined();
    const initialWeek = parseInt(initialWeekMatch![1]);

    // Click "Simulate Week"
    const simulateWeekButton = page.getByRole("button", { name: "Simulate Week" });
    await expect(simulateWeekButton).toBeVisible();

    const simulateWeekResponsePromise = page.waitForResponse(
      (response) =>
        response.url().includes("/api/season/") &&
        response.url().includes("/simulate-week") &&
        response.status() === 200
    );
    const advanceWeekResponsePromise = page.waitForResponse(
      (response) =>
        response.url().includes("/api/season/") &&
        response.url().includes("/advance-week") &&
        response.status() === 200
    );

    await simulateWeekButton.click();

    await simulateWeekResponsePromise;
    await advanceWeekResponsePromise;

    // Wait for button text to change back, indicating simulation is complete
    await expect(simulateWeekButton).toHaveText("Simulate Week");

    // Verify week number has incremented
    const updatedWeekText = await page.locator(".season-status span:has-text('Week')").innerText();
    const updatedWeekMatch = updatedWeekText.match(/Week (\d+)/);
    expect(updatedWeekMatch).toBeDefined();
    const updatedWeek = parseInt(updatedWeekMatch![1]);
    expect(updatedWeek).toBe(initialWeek + 1);

    // Verify some game results are visible (simple check)
    // Assuming there are "Recent Results" displayed on the overview tab
    const recentResultsHeader = page.getByRole("heading", { name: "Recent Results" });
    await expect(recentResultsHeader).toBeVisible();
    await expect(page.locator(".games-list-compact .game-card-compact")).toHaveCount(5); // Assuming 5 games are displayed
  });

  test("should display standings correctly", async ({ page }) => {
    // Navigate to Standings tab
    const standingsTabButton = page.getByRole("button", { name: "Standings" });
    await expect(standingsTabButton).toBeVisible();

    const standingsResponsePromise = page.waitForResponse(
      (response) =>
        response.url().includes("/api/season/") &&
        response.url().includes("/standings") &&
        response.status() === 200
    );

    await standingsTabButton.click();

    await standingsResponsePromise;

    // Verify Standings table is visible
    const standingsTableHeader = page.locator(".standings-table th:has-text('Team')");
    await expect(standingsTableHeader).toBeVisible();

    // Verify some team data is present
    const teamNameInStandings = page.locator(".standings-table tbody tr:first-child .team-name");
    await expect(teamNameInStandings).toBeVisible();
    await expect(teamNameInStandings).not.toBeEmpty();

    // Verify "Wins" and "Losses" headers are visible
    await expect(page.locator(".standings-table th:has-text('W')")).toBeVisible();
    await expect(page.locator(".standings-table th:has-text('L')")).toBeVisible();
  });
});

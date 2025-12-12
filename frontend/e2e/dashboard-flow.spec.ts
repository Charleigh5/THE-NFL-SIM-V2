import { test, expect } from "@playwright/test";

const mockSystemHealth = { status: "healthy" };

const mockCurrentSeasonActive = {
  id: 1,
  year: 2024,
  status: "REGULAR_SEASON",
  current_week: 1,
};

const mockCurrentSeasonNull = null; // Represents no active season

const mockInitializedSeason = {
  id: 2,
  year: 2025,
  status: "PRE_SEASON",
  current_week: 0,
};

test.describe("Dashboard Flow", () => {
  test("should display dashboard with active season and system health", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    await page.goto("/dashboard");

    // Verify header
    await expect(page.locator("h1", { hasText: "Mission Control" })).toBeVisible();
    await expect(
      page.locator("p", { hasText: "War Room overview under the stadium lights." })
    ).toBeVisible();

    // Verify system health
    await expect(page.locator(".system-status .badge")).toContainText("All Systems Online");

    // Verify season button text for active season
    await expect(page.locator(".start-season-btn")).toContainText("Start Next Season");

    // Verify engine cards (check one example)
    await expect(page.locator(".engine-card", { hasText: "Genesis Engine" })).toBeVisible();
  });

  test("should display dashboard with no active season and allow starting a new one", async ({
    page,
  }) => {
    // Mock initial state: no active season
    let currentSeasonMock: typeof mockCurrentSeasonActive | null = mockCurrentSeasonNull;

    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: currentSeasonMock });
    });

    // Mock season initialization
    await page.route("**/api/season/init", async (route) => {
      expect(route.request().method()).toBe("POST");
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty("year");
      expect(postData.year).toBe(2025); // Expecting year 2025 as currentSeason is null
      currentSeasonMock = mockInitializedSeason; // Update mock for subsequent getCurrentSeason calls
      await route.fulfill({ status: 200, json: mockInitializedSeason });
    });

    await page.goto("/dashboard");

    // Verify "Start Season" button
    await expect(page.locator(".start-season-btn")).toContainText("Start Season");

    // Mock window.location.reload()
    const reloadPromise = page.waitForEvent("framenavigated", (frame) =>
      frame.url().includes("/dashboard")
    );

    // Click Start Season button
    await page.locator(".start-season-btn").click();

    // Wait for the reload to happen and check for new button text
    await reloadPromise;
    await expect(page.locator(".start-season-btn")).toContainText("Start Next Season");

    // Verify that the season info (e.g. current year if displayed) updates
    // This might require a dedicated element in the UI to display the current season year.
    // For now, checking button text is sufficient.
  });

  test("should display Quick Actions section with navigation links", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    await page.goto("/dashboard");

    // Verify Quick Actions section exists
    await expect(page.locator("text=Quick Actions")).toBeVisible();

    // Verify all quick action links exist
    const quickActions = page.locator(".quick-actions-section");
    await expect(quickActions.locator(".quick-action-card", { hasText: "Roster" })).toBeVisible();
    await expect(
      quickActions.locator(".quick-action-card", { hasText: "Depth Chart" })
    ).toBeVisible();
    await expect(
      quickActions.locator(".quick-action-card", { hasText: "Trade Center" })
    ).toBeVisible();
    await expect(quickActions.locator(".quick-action-card", { hasText: "Season" })).toBeVisible();
    await expect(quickActions.locator(".quick-action-card", { hasText: "Training" })).toBeVisible();
    await expect(
      quickActions.locator(".quick-action-card", { hasText: "Draft Room" })
    ).toBeVisible();
  });

  test("should navigate to Roster via Quick Actions", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });
    // Mock teams and players for front-office
    await page.route("**/api/teams**", async (route) => {
      await route.fulfill({ json: { items: [] } });
    });
    await page.route("**/api/players**", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
    });

    await page.goto("/dashboard");

    // Click on Roster quick action
    await page.locator(".quick-action-card", { hasText: "Roster" }).click();

    // Verify navigation to front-office
    await page.waitForURL("**/empire/front-office");
    await expect(page.url()).toContain("/empire/front-office");
  });

  test("should navigate to Trade Center via Quick Actions", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });
    // Mock trade center APIs
    await page.route("**/api/settings**", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, difficulty_level: "All-Pro" } });
    });
    await page.route("**/api/trades/**", async (route) => {
      await route.fulfill({ json: { incoming: [], outgoing: [] } });
    });

    await page.goto("/dashboard");

    // Click on Trade Center quick action
    await page.locator(".quick-action-card", { hasText: "Trade Center" }).click();

    // Verify navigation
    await page.waitForURL("**/empire/trade-center");
    await expect(page.url()).toContain("/empire/trade-center");
  });

  test("should display season status card when season exists", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    await page.goto("/dashboard");

    // Verify season status card shows year and week
    await expect(page.locator("text=Current Season")).toBeVisible();
    await expect(page.locator(".season-year", { hasText: "2024" })).toBeVisible();
    await expect(page.locator(".season-week", { hasText: "Week 1" })).toBeVisible();
  });
});

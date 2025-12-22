import { test, expect } from "@playwright/test";

const mockSystemHealth = { status: "healthy" };

const mockCurrentSeasonActive = {
  id: 1,
  year: 2024,
  status: "REGULAR_SEASON",
  current_week: 1,
};

const mockCurrentSeasonNull = null;

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

    // Verify header - "Mission Control" heading is visible
    await expect(page.getByRole("heading", { name: "Mission Control" })).toBeVisible();

    // Verify system status shows ONLINE when healthy (uppercase in UI)
    await expect(page.getByText("ONLINE", { exact: true })).toBeVisible();

    // Verify season year is displayed somewhere on page
    await expect(page.getByText("2024").first()).toBeVisible();

    // Verify "Simulate Week" button exists when season is active
    await expect(page.getByRole("button", { name: /simulate week/i })).toBeVisible();
  });

  test("should display dashboard with no active season and allow starting a new one", async ({
    page,
  }) => {
    let currentSeasonMock: typeof mockCurrentSeasonActive | null = mockCurrentSeasonNull;

    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: currentSeasonMock, status: currentSeasonMock ? 200 : 404 });
    });

    await page.route("**/api/season/init", async (route) => {
      expect(route.request().method()).toBe("POST");
      currentSeasonMock = mockInitializedSeason;
      await route.fulfill({ status: 200, json: mockInitializedSeason });
    });

    await page.goto("/dashboard");

    // Verify "Start Season" button when no active season
    await expect(page.getByRole("button", { name: /start season/i })).toBeVisible();
  });

  test("should display Quick Actions section with navigation links", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    await page.goto("/dashboard");

    // Verify action cards exist - check for the visible labels in the action bar
    await expect(page.getByText("Depth Chart", { exact: true })).toBeVisible();
    await expect(page.getByText("Trade Center", { exact: true }).first()).toBeVisible();
    await expect(page.getByText("Draft Room", { exact: true })).toBeVisible();
    await expect(page.getByText("Training", { exact: true })).toBeVisible();
  });

  test("should navigate to Roster via Roster Health card", async ({ page }) => {
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });
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

    // Click on "Roster Health" card to navigate - use the link containing the text
    await page.locator("a", { hasText: "Roster Health" }).click();

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
    await page.route("**/api/settings**", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, difficulty_level: "All-Pro" } });
    });
    await page.route("**/api/trades/**", async (route) => {
      await route.fulfill({ json: { incoming: [], outgoing: [] } });
    });

    await page.goto("/dashboard");

    // Click on Trade Center action link (use the one with emoji in action bar)
    await page
      .getByRole("link", { name: /Trade Center/i })
      .first()
      .click();

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

    // Verify Season Control card heading
    await expect(page.getByRole("heading", { name: "Season Control" })).toBeVisible();

    // Verify year is shown in header
    await expect(page.locator("text=2024").first()).toBeVisible();

    // Week info is shown in the "Current Week" card
    await expect(page.getByText("WEEK 1")).toBeVisible();
  });
});

import { test, expect } from "@playwright/test";

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:5199";

test.describe("SportsCenter Broadcast Narrator HUD", () => {
  const mockChiefs = {
    id: 1,
    city: "Kansas City",
    name: "Chiefs",
    abbreviation: "KC",
    conference: "AFC",
    division: "West",
    wins: 6,
    losses: 1,
    ties: 0,
    salary_cap_space: 42000000,
    primary_color: "#E31837",
    secondary_color: "#FFB81C",
  };

  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
      localStorage.setItem("hasSelectedFranchise", "true");
    });

    await page.route("**/api/teams?*", async (route) => {
      await route.fulfill({
        json: {
          items: [mockChiefs],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockChiefs });
    });

    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/news/**", async (route) => {
      await route.fulfill({
        json: { items: [], total: 0, last_updated: new Date().toISOString() },
      });
    });

    await page.route("**/api/season/**", async (route) => {
      await route.fulfill({
        json: {
          season: {
            id: 1,
            year: 2026,
            current_week: 8,
            status: "REGULAR_SEASON",
            total_weeks: 18,
            playoff_weeks: 4,
            is_active: true,
          },
          completion_percentage: 40,
        },
      });
    });
  });

  test("triggers on-demand narration and displays Browser Voice fallback badge and script caption", async ({
    page,
  }) => {
    await page.route("**/api/broadcast/narrate", async (route) => {
      await route.fulfill({
        json: {
          script:
            "From the ESPN Broadcast Desk, Kansas City Chiefs (6-1) check in at Week 8 of the 2026 season after defeating Buffalo Bills 31-24.",
          headline_banner: "ESPN: KANSAS CITY CHIEFS (6-1) | WK 8 DASHBOARD",
          cache_key: "a".repeat(64),
          audio_url: null,
          voice_source: "browser",
          degraded: true,
          style: "ESPN",
        },
      });
    });

    await page.goto(`${BASE_URL}/dashboard`);

    const narratorBar = page.getByTestId("narrator-bar");
    await expect(narratorBar).toBeVisible();

    const voiceBadge = page.getByTestId("narrator-voice-badge");
    await expect(voiceBadge).toHaveText("Browser Voice");

    const triggerBtn = page.getByTestId("narrator-trigger-btn");
    await triggerBtn.click();

    await expect(page.getByTestId("narrator-headline-banner")).toHaveText(
      "ESPN: KANSAS CITY CHIEFS (6-1) | WK 8 DASHBOARD"
    );
    await expect(page.getByTestId("narrator-script-text")).toContainText(
      "Kansas City Chiefs (6-1) check in at Week 8"
    );
  });

  test("persists style and auto-narrate preferences across reloads", async ({ page }) => {
    await page.route("**/api/broadcast/narrate", async (route) => {
      await route.fulfill({
        json: {
          script: "Inside the Kansas City Chiefs war room on NFL Network.",
          headline_banner: "NFL_NETWORK: KANSAS CITY CHIEFS (6-1)",
          cache_key: "b".repeat(64),
          audio_url: null,
          voice_source: "browser",
          degraded: true,
          style: "NFL_NETWORK",
        },
      });
    });

    await page.goto(`${BASE_URL}/dashboard`);

    const styleSelect = page.getByTestId("narrator-style-select");
    await styleSelect.selectOption("NFL_NETWORK");

    const autoToggle = page.getByTestId("narrator-auto-toggle");
    await autoToggle.check();

    const storedPrefs = await page.evaluate(() => {
      const raw = localStorage.getItem("nfl-sim-narrator-prefs");
      return raw ? JSON.parse(raw) : null;
    });

    expect(storedPrefs).toBeTruthy();
    expect(storedPrefs.style).toBe("NFL_NETWORK");
    expect(storedPrefs.autoNarrate).toBe(true);

    await page.reload();
    await expect(page.getByTestId("narrator-style-select")).toHaveValue("NFL_NETWORK");
    await expect(page.getByTestId("narrator-auto-toggle")).toBeChecked();
  });
});

import { test, expect } from "@playwright/test";

const mockTeams = [
  {
    id: 11,
    name: "Lions",
    city: "Detroit",
    abbreviation: "DET",
    conference: "NFC",
    division: "North",
    wins: 12,
    losses: 5,
    ties: 0,
  },
  {
    id: 1,
    name: "Cardinals",
    city: "Arizona",
    abbreviation: "ARI",
    conference: "NFC",
    division: "West",
    wins: 4,
    losses: 13,
    ties: 0,
  },
  {
    id: 2,
    name: "49ers",
    city: "San Francisco",
    abbreviation: "SF",
    conference: "NFC",
    division: "West",
    wins: 12,
    losses: 5,
    ties: 0,
  },
];

const mockUserSettings = {
  user_team_id: 11,
  difficulty: "normal",
  game_speed: "medium",
};

test.describe("Launch Gateway & Franchise Onboarding", () => {
  test.beforeEach(async ({ page }) => {
    // Mock getTeams API
    await page.route("**/api/teams*", async (route) => {
      await route.fulfill({
        json: {
          items: mockTeams,
          total: mockTeams.length,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    // Mock settings API
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: mockUserSettings });
    });

    await page.route("**/api/settings/team", async (route) => {
      await route.fulfill({ status: 200, json: mockUserSettings });
    });

    // Mock season summary
    await page.route("**/api/seasons/current/summary", async (route) => {
      await route.fulfill({
        json: {
          season: { id: 1, year: 2026, current_week: 1, is_playoffs: false },
          user_team: mockTeams[0],
          upcoming_game: null,
          recent_games: [],
        },
      });
    });

    await page.route("**/api/seasons/current", async (route) => {
      await route.fulfill({
        json: { id: 1, year: 2026, current_week: 1, is_playoffs: false },
      });
    });
  });

  test("should display franchise selection on root / when no franchise is saved", async ({
    page,
  }) => {
    // Clear localStorage before visiting
    await page.addInitScript(() => {
      localStorage.clear();
    });

    await page.goto("/");

    // Verify Franchise Selection is presented
    await expect(page.locator("h1", { hasText: "Select Your Franchise" })).toBeVisible();

    // Verify Detroit Lions Quick-Start callout is visible
    await expect(page.getByText("DETROIT LIONS (DEFAULT FAVORITE) • NFC NORTH")).toBeVisible();
    const quickStartBtn = page.getByRole("button", { name: "CONFIRM & ENTER WAR ROOM" });
    await expect(quickStartBtn).toBeVisible();

    // Verify Detroit Lions card has selected styling by default
    const lionsCard = page.locator(".team-card:has-text('Detroit Lions')");
    await expect(lionsCard).toBeVisible();
    await expect(lionsCard).toHaveClass(/selected/);
  });

  test("clicking CONFIRM & ENTER WAR ROOM persists Detroit Lions and navigates to War Room", async ({
    page,
  }) => {
    await page.addInitScript(() => {
      localStorage.clear();
    });

    await page.goto("/");

    const quickStartBtn = page.getByRole("button", { name: "CONFIRM & ENTER WAR ROOM" });
    await quickStartBtn.click();

    // Verify localStorage persistence
    await expect.poll(async () => {
      return await page.evaluate(() => ({
        hasSelected: localStorage.getItem("hasSelectedFranchise"),
        teamId: localStorage.getItem("selectedTeamId"),
        teamAbbr: localStorage.getItem("selectedTeamAbbr"),
      }));
    }).toEqual({
      hasSelected: "true",
      teamId: "11",
      teamAbbr: "DET",
    });

    // Verify War Room / Dashboard is rendered
    await expect(page.locator("h1", { hasText: "Mission Control" })).toBeVisible({ timeout: 10000 });
  });

  test("should load Dashboard directly on root / when franchise is already stored in memory", async ({
    page,
  }) => {
    // Seed persistent storage with Detroit Lions
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "11");
      localStorage.setItem("selectedTeamAbbr", "DET");
      localStorage.setItem("hasSelectedFranchise", "true");
    });

    await page.goto("/");

    // Should immediately show Dashboard without rendering team selection
    await expect(page.locator("h1", { hasText: "Mission Control" })).toBeVisible();
    await expect(page.locator("h1", { hasText: "Select Your Franchise" })).not.toBeVisible();
  });

  test("allows manual navigation to /team-selection even after team is selected", async ({
    page,
  }) => {
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "11");
      localStorage.setItem("selectedTeamAbbr", "DET");
      localStorage.setItem("hasSelectedFranchise", "true");
    });

    await page.goto("/team-selection");

    // Must be able to switch teams at any time
    await expect(page.locator("h1", { hasText: "Select Your Franchise" })).toBeVisible();
  });

  test("verifies transparent container architecture and stadium backdrop visibility", async ({
    page,
  }) => {
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "11");
      localStorage.setItem("selectedTeamAbbr", "DET");
      localStorage.setItem("hasSelectedFranchise", "true");
    });

    await page.goto("/dashboard");

    // Confirm ThreeStadiumBackdrop canvas container exists
    const backdrop = page.locator("[data-testid='three-stadium-backdrop']");
    await expect(backdrop).toBeVisible();

    // Confirm layout root has transparent styling
    const mainLayout = page.locator("main");
    await expect(mainLayout).toBeVisible();
    const isBgTransparent = await mainLayout.evaluate((el) => {
      const style = window.getComputedStyle(el);
      return style.backgroundColor === "rgba(0, 0, 0, 0)" || style.backgroundColor === "transparent";
    });
    expect(isBgTransparent).toBe(true);
  });
});

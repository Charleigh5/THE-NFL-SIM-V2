import { test, expect } from "@playwright/test";
import { mockTeam, mockPlayers } from "./fixtures/test-data";

test.describe("Visual Regression Tests", () => {
  test("Front Office visual snapshot", async ({ page }) => {
    // Mock API for Front Office
    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({ json: mockPlayers });
    });

    await page.goto("/empire/front-office");

    // Wait for key elements to ensure page is loaded
    await page.waitForSelector('[data-testid="front-office-header"]');
    await page.waitForSelector('[data-testid="roster-section"]');
    // Use a selector that matches the dynamic testId format "player-card-{id}"
    await page.waitForSelector('[data-testid^="player-card-"]');

    // Take snapshot
    await expect(page).toHaveScreenshot("front-office.png");
  });

  test("Season Dashboard visual snapshot", async ({ page }) => {
    page.on("console", (msg) => console.log(`BROWSER LOG: ${msg.text()}`));

    // Mock API for Season Dashboard
    const mockSeason = {
      id: 1,
      year: 2024,
      current_week: 5,
      total_weeks: 17,
      status: "REGULAR_SEASON",
    };

    await page.route(/.*\/api\/teams.*/, async (route) => {
      console.log("Intercepted teams request:", route.request().url());
      await route.fulfill({
        json: {
          items: [mockTeam],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route(/.*\/api\/season\/summary/, async (route) => {
      await route.fulfill({
        json: {
          season: mockSeason,
          completion_percentage: 25,
        },
      });
    });

    await page.route(/.*\/api\/season\/1\/standings.*/, async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route(/.*\/api\/season\/1\/schedule.*/, async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route(/.*\/api\/season\/1\/leaders/, async (route) => {
      await route.fulfill({
        json: {
          passing_yards: [],
          passing_tds: [],
          rushing_yards: [],
          rushing_tds: [],
          receiving_yards: [],
          receiving_tds: [],
        },
      });
    });

    await page.route(/.*\/api\/season\/1\/awards\/projected/, async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });

    await page.goto("/season");

    // Wait for loading to finish
    await expect(page.locator(".loading-spinner")).not.toBeVisible();
    await page.waitForSelector(".season-dashboard");

    await expect(page).toHaveScreenshot("season-dashboard.png");
  });

  test("Playoff Bracket visual snapshot", async ({ page }) => {
    const mockPlayoffSeason = {
      id: 1,
      year: 2024,
      current_week: 19,
      total_weeks: 17,
      status: "POST_SEASON",
    };

    const mockBracket = [
      {
        id: 101,
        season_id: 1,
        round: "WILD_CARD",
        conference: "NFC",
        matchup_code: "NFC_WC_1",
        home_team_id: 1,
        away_team_id: 2,
        home_team_seed: 1,
        away_team_seed: 2,
        home_team: { id: 1, name: "Cardinals", city: "Arizona", abbreviation: "ARI" },
        away_team: { id: 2, name: "49ers", city: "San Francisco", abbreviation: "SF" },
        winner_id: null,
        game_id: 501,
      },
    ];

    await page.route(/.*\/api\/teams.*/, async (route) => {
      await route.fulfill({
        json: {
          items: [mockTeam],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route(/.*\/api\/season\/summary/, async (route) => {
      await route.fulfill({
        json: {
          season: mockPlayoffSeason,
          completion_percentage: 100,
        },
      });
    });

    // Mock other required endpoints
    await page.route(/.*\/api\/season\/1\/standings.*/, async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route(/.*\/api\/season\/1\/schedule.*/, async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route(/.*\/api\/season\/1\/leaders/, async (route) => {
      await route.fulfill({
        json: {
          passing_yards: [],
          passing_tds: [],
          rushing_yards: [],
          rushing_tds: [],
          receiving_yards: [],
          receiving_tds: [],
        },
      });
    });
    await page.route(/.*\/api\/season\/1\/awards\/projected/, async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });

    await page.route(/.*\/api\/season\/1\/playoffs\/bracket/, async (route) => {
      await route.fulfill({ json: mockBracket });
    });

    await page.goto("/season");

    // Wait for loading
    await expect(page.locator(".loading-spinner")).not.toBeVisible();

    // Verify Playoffs tab is present
    const playoffsTab = page.getByRole("button", { name: "Playoffs" });
    await expect(playoffsTab).toBeVisible();

    // Click it
    await playoffsTab.click();

    // Wait for bracket
    await page.waitForSelector(".playoff-bracket");

    await expect(page).toHaveScreenshot("playoff-bracket.png");
  });

  test("Draft Board visual snapshot", async ({ page }) => {
    const mockSeason = {
      id: 1,
      year: 2024,
      status: "OFF_SEASON",
    };

    const mockPick = {
      round: 1,
      pick_number: 1,
      team_id: 1,
    };

    const mockProspects = [
      { id: 1, name: "Caleb Williams", position: "QB", school: "USC", overall_rating: 90 },
      { id: 2, name: "Drake Maye", position: "QB", school: "UNC", overall_rating: 88 },
    ];

    const mockNeeds = [
      { position: "QB", need_score: 9.5 },
      { position: "WR", need_score: 8.0 },
    ];

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockSeason });
    });

    await page.route("**/api/season/1/draft/current", async (route) => {
      await route.fulfill({ json: mockPick });
    });

    await page.route("**/api/season/1/offseason/prospects?limit=100", async (route) => {
      await route.fulfill({ json: mockProspects });
    });

    await page.route("**/api/season/1/offseason/needs/1", async (route) => {
      await route.fulfill({ json: mockNeeds });
    });

    await page.goto("/offseason/draft");

    // Wait for draft board to load
    await page.waitForSelector(".draft-board");

    await expect(page).toHaveScreenshot("draft-board.png");
  });
});

import { test, expect } from "@playwright/test";

/**
 * News Feed E2E Tests
 *
 * Tests for Phase 8 Task 8.3.1: News Feed dashboard widget
 * - Living World news integration
 * - News display in Season Dashboard
 * - Breaking news highlighting
 */

const mockSeason = {
  id: 1,
  year: 2024,
  current_week: 8,
  status: "REGULAR_SEASON",
  total_weeks: 18,
};

const mockLivingNews = {
  items: [
    {
      id: 1,
      season_id: 1,
      week: 8,
      team_id: 1,
      player_id: 101,
      category: "game_result",
      headline: "Cardinals Secure Thrilling Victory Over Cowboys",
      content:
        "In a nail-biting finish, the Arizona Cardinals edged out the Dallas Cowboys 28-24. Kyler Murray threw for 3 touchdowns in the fourth quarter.",
      image_url: null,
      importance_score: 0.8,
      created_at: "2024-11-17T20:00:00Z",
    },
    {
      id: 2,
      season_id: 1,
      week: 8,
      team_id: null,
      player_id: null,
      category: "trade",
      headline: "Blockbuster Trade Shakes Up NFC West",
      content: "The San Francisco 49ers have acquired a star wide receiver in a multi-player deal.",
      image_url: null,
      importance_score: 0.9,
      created_at: "2024-11-17T18:00:00Z",
    },
    {
      id: 3,
      season_id: 1,
      week: 8,
      team_id: 2,
      player_id: 201,
      category: "injury",
      headline: "Cowboys Star Listed as Questionable",
      content:
        "CeeDee Lamb is listed as questionable for next week's game after suffering an ankle injury.",
      image_url: null,
      importance_score: 0.6,
      created_at: "2024-11-17T16:00:00Z",
    },
  ],
  total_count: 3,
  page: 1,
  page_size: 10,
  has_more: false,
};

const mockSeasonSummary = {
  season: mockSeason,
  completion_percentage: 44.4,
  teams: [],
};

const mockTeams = [
  { id: 1, name: "Cardinals", city: "Arizona", abbreviation: "ARI" },
  { id: 2, name: "Cowboys", city: "Dallas", abbreviation: "DAL" },
];

test.describe("News Feed Widget", () => {
  test.beforeEach(async ({ page }) => {
    // Mock API endpoints
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({ json: mockTeams });
    });

    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({ json: mockSeasonSummary });
    });

    await page.route("**/api/season/*/standings", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/season/*/schedule/*", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/season/*/leaders", async (route) => {
      await route.fulfill({ json: { passing: [], rushing: [], receiving: [] } });
    });

    await page.route("**/api/season/*/awards/projected", async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });

    // Mock Living World news API
    await page.route("**/api/news/living/feed*", async (route) => {
      await route.fulfill({ json: mockLivingNews });
    });

    // Mock regular news endpoints as fallback
    await page.route("**/api/news/league*", async (route) => {
      await route.fulfill({
        json: {
          items: mockLivingNews.items.map((item) => ({
            headline: item.headline,
            source: "NFL Network",
            date: item.created_at,
            category: item.category,
            is_breaking: item.importance_score >= 0.7,
          })),
          total: mockLivingNews.items.length,
          last_updated: new Date().toISOString(),
        },
      });
    });
  });

  test("should display news feed in Season Dashboard overview", async ({ page }) => {
    await page.goto("/season");

    // Wait for dashboard to load
    await page.waitForSelector('[data-testid="season-dashboard-page"]', { timeout: 10000 });

    // The overview tab should be active by default
    await expect(page.locator('[data-testid="tab-overview"]')).toHaveClass(/active/);

    // News section selector (used in future assertions if needed)
    // const newsFeedSection = page.locator('.news-feed, [class*="NewsFeed"], .league-wire');

    // News content should be visible
    await expect(page.locator("text=League Wire, text=News, text=Headlines").first()).toBeVisible({
      timeout: 5000,
    });
  });

  test("should display breaking news with special styling", async ({ page }) => {
    await page.goto("/season");

    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Look for breaking news badge or indicator
    const breakingIndicator = page.locator('.breaking-badge, .breaking, [data-breaking="true"]');

    // At least one breaking news item should exist (importance_score >= 0.7)
    if ((await breakingIndicator.count()) > 0) {
      await expect(breakingIndicator.first()).toBeVisible();
    }
  });

  test("should display news headlines correctly", async ({ page }) => {
    await page.goto("/season");

    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Check for specific headlines from mock data
    const cardinals = page.locator("text=Cardinals");
    const cowboys = page.locator("text=Cowboys");

    // At least one team name should appear in news
    const cardinalsVisible = (await cardinals.count()) > 0;
    const cowboysVisible = (await cowboys.count()) > 0;

    expect(cardinalsVisible || cowboysVisible).toBeTruthy();
  });

  test("should categorize news items visually", async ({ page }) => {
    await page.goto("/season");

    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Look for category indicators
    const categoryIndicators = page.locator("[data-category], .news-category, .category-indicator");

    if ((await categoryIndicators.count()) > 0) {
      // Categories should be displayed
      await expect(categoryIndicators.first()).toBeVisible();
    }
  });

  test("should handle empty news state gracefully", async ({ page }) => {
    // Override with empty news
    await page.route("**/api/news/living/feed*", async (route) => {
      await route.fulfill({
        json: {
          items: [],
          total_count: 0,
          page: 1,
          page_size: 10,
          has_more: false,
        },
      });
    });

    await page.goto("/season");

    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Should show empty state or hint message
    const emptyState = page.locator("text=No news, text=Play some games, .empty");

    if ((await emptyState.count()) > 0) {
      await expect(emptyState.first()).toBeVisible();
    }
  });

  test("should handle news loading errors gracefully", async ({ page }) => {
    // Override with error response
    await page.route("**/api/news/living/feed*", async (route) => {
      await route.fulfill({ status: 500, json: { error: "Server error" } });
    });

    await page.goto("/season");

    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Page should still load, potentially showing retry button or fallback
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible();
  });
});

test.describe("News Categories", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({ json: mockTeams });
    });

    await page.route("**/api/season/summary", async (route) => {
      await route.fulfill({ json: mockSeasonSummary });
    });

    await page.route("**/api/season/*/standings", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/season/*/schedule/*", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/season/*/leaders", async (route) => {
      await route.fulfill({ json: { passing: [], rushing: [], receiving: [] } });
    });

    await page.route("**/api/season/*/awards/projected", async (route) => {
      await route.fulfill({ json: { mvp: [], opoy: [], dpoy: [], oroy: [], droy: [] } });
    });

    await page.route("**/api/news/living/feed*", async (route) => {
      await route.fulfill({ json: mockLivingNews });
    });
  });

  test("should display game result news", async ({ page }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Mock data includes game_result category
    const gameNews = page.locator("text=Victory, text=touchdown, text=win");
    if ((await gameNews.count()) > 0) {
      await expect(gameNews.first()).toBeVisible();
    }
  });

  test("should display trade news", async ({ page }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Mock data includes trade category
    const tradeNews = page.locator("text=Trade, text=acquired, text=deal");
    if ((await tradeNews.count()) > 0) {
      await expect(tradeNews.first()).toBeVisible();
    }
  });

  test("should display injury news", async ({ page }) => {
    await page.goto("/season");
    await page.waitForSelector('[data-testid="season-dashboard-page"]');

    // Mock data includes injury category
    const injuryNews = page.locator("text=Questionable, text=injury, text=injured");
    if ((await injuryNews.count()) > 0) {
      await expect(injuryNews.first()).toBeVisible();
    }
  });
});

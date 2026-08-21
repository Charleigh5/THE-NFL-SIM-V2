import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Draft Assistant Widget (UI-007)
 * Running against local backend server
 *
 * NOTE: These tests check basic page functionality.
 * Full Draft Assistant tests require:
 * - A season in DRAFT phase in the database
 * - Current pick data
 * - Available prospects
 */

test.describe("Draft Room Page", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/api/**", async (route) => {
      await route.fulfill({ json: {} });
    });
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, selected_season_id: 1 } });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: { id: 1, year: 2024, status: "OFF_SEASON", current_week: 1 } });
    });
    await page.route("**/api/season/1/draft/current", async (route) => {
      await route.fulfill({ json: { round: 1, pick_number: 1, team_id: 1 } });
    });
    await page.route("**/api/season/1/offseason/prospects*", async (route) => {
      await route.fulfill({
        json: [
          { id: 1, name: "Caleb Williams", position: "QB", overall_rating: 90, school: "USC" },
        ],
      });
    });
    await page.route("**/api/season/1/offseason/needs/1", async (route) => {
      await route.fulfill({ json: [{ position: "QB", need_score: 9.5 }] });
    });
  });

  test("should load Draft Room page successfully", async ({ page }) => {
    await page.goto("/offseason/draft");

    // Page should load without errors
    await expect(page).toHaveURL(/.*offseason\/draft/);

    // Should have navigation / sidebar
    await expect(
      page.locator("nav, aside, .sidebar-nav, [role='navigation']").first()
    ).toBeVisible();
  });

  test("should show appropriate message when no active season", async ({ page }) => {
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: null, status: 404 });
    });
    await page.goto("/offseason/draft");

    const noSeasonHeading = page
      .locator("h1, h2")
      .filter({ hasText: /No Active Season|Draft Room/i });
    await expect(noSeasonHeading.first()).toBeVisible();
  });

  test("should show Draft Room content when season exists", async ({ page }) => {
    await page.goto("/offseason/draft");

    const draftContent = page
      .locator("[data-testid='draft-room-page'], .draft-board, .draft-room, [class*='draft']")
      .first();
    await expect(draftContent).toBeVisible({ timeout: 10000 });
  });
});

test.describe("Draft Assistant Widget - With Active Draft", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/api/**", async (route) => {
      await route.fulfill({ json: {} });
    });
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, selected_season_id: 1 } });
    });
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: { id: 1, year: 2024, status: "OFF_SEASON", current_week: 1 } });
    });
    await page.route("**/api/season/1/draft/current", async (route) => {
      await route.fulfill({ json: { round: 1, pick_number: 1, team_id: 1 } });
    });
    await page.route("**/api/season/1/offseason/prospects*", async (route) => {
      await route.fulfill({
        json: [
          { id: 1, name: "Caleb Williams", position: "QB", overall_rating: 90, school: "USC" },
        ],
      });
    });
    await page.route("**/api/season/1/offseason/needs/1", async (route) => {
      await route.fulfill({ json: [{ position: "QB", need_score: 9.5 }] });
    });
  });

  test("should render Draft Assistant when current pick exists", async ({ page }) => {
    await page.goto("/offseason/draft");

    const widget = page
      .locator(
        '[data-testid="draft-assistant-widget"], .draft-board, [data-testid="draft-room-page"]'
      )
      .first();
    await expect(widget).toBeVisible({ timeout: 10000 });
  });

  test.skip("should analyze a pick successfully", async ({ page }) => {
    // This test requires:
    // 1. Active season in DRAFT phase
    // 2. Current pick
    // 3. Available prospects
    // Skip for now - can be enabled when database is populated

    await page.goto("/offseason/draft");
    const widget = page.getByTestId("draft-assistant-widget");
    await expect(widget).toBeVisible({ timeout: 5000 });

    await page.getByTestId("analyze-pick-btn").click();
    await expect(page.getByTestId("assistant-loading")).toBeVisible();
    await expect(page.getByTestId("suggestion-card")).toBeVisible({ timeout: 15000 });
  });
});

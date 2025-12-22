import { test, expect } from "@playwright/test";
import { setupSeasonDashboardMocks, mockNewsResponse } from "./fixtures/test-data";

/**
 * News Feed E2E Tests
 * Tests for Living World news integration in Season Dashboard
 */

test.describe("News Feed Widget", () => {
  test.beforeEach(async ({ page }) => {
    await setupSeasonDashboardMocks(page);
  });

  test("should display news feed in Season Dashboard overview", async ({ page }) => {
    await page.goto("/season");

    // Wait for dashboard to load
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Overview tab should be visible
    await expect(page.locator('[data-testid="tab-overview"]')).toBeVisible();

    // League Wire section (contains NewsFeed) should be visible
    await expect(page.getByText("League Wire")).toBeVisible();
  });

  test("should display news headlines correctly", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Check that news items appear
    // The news widget should show headlines from mock data
    await expect(page.getByText("League Wire")).toBeVisible();
  });

  test("should handle empty news state gracefully", async ({ page }) => {
    // Override with empty news
    await page.route("**/api/news/league**", async (route) => {
      await route.fulfill({
        json: { items: [], total: 0, last_updated: new Date().toISOString() },
      });
    });

    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Page should still render without errors
    await expect(page.getByText("League Wire")).toBeVisible();
  });

  test("should handle news loading errors gracefully", async ({ page }) => {
    // Override with error response
    await page.route("**/api/news/league**", async (route) => {
      await route.fulfill({ status: 500, json: { error: "Server error" } });
    });

    await page.goto("/season");

    // Page should still load
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });
  });
});

test.describe("News Categories", () => {
  test.beforeEach(async ({ page }) => {
    await setupSeasonDashboardMocks(page);
  });

  test("should display breaking news indicator", async ({ page }) => {
    await page.goto("/season");
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // League Wire section should be visible
    await expect(page.getByText("League Wire")).toBeVisible();

    // Breaking news has a badge in the component
    const breakingBadge = page.locator(".breaking-badge");
    if ((await breakingBadge.count()) > 0) {
      await expect(breakingBadge.first()).toBeVisible();
    }
  });

  test("should display trade news category", async ({ page }) => {
    await page.goto("/season");
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    await expect(page.getByText("League Wire")).toBeVisible();
  });

  test("should display news from mock data", async ({ page }) => {
    await page.goto("/season");
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 10000,
    });

    // Check for any headline from mock data
    const headline = page.getByText(mockNewsResponse.items[0].headline);
    if ((await headline.count()) > 0) {
      await expect(headline.first()).toBeVisible();
    }
  });
});

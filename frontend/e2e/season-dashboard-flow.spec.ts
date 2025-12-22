import { test, expect } from "@playwright/test";
import { setupSeasonDashboardMocks, mockSeason } from "./fixtures/test-data";

test.describe("Season Dashboard Flow", () => {
  test.beforeEach(async ({ page }) => {
    await setupSeasonDashboardMocks(page);
  });

  test("should load season dashboard with standings and schedule", async ({ page }) => {
    await page.goto("/season");

    // Verify Season Dashboard page loads
    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 15000,
    });

    // Verify header shows year and week
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText(
      String(mockSeason.year)
    );
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText(
      `Week ${mockSeason.current_week}`
    );

    // Verify tabs are visible
    await expect(page.locator('[data-testid="dashboard-tabs"]')).toBeVisible();
  });

  test("should switch between tabs", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 15000,
    });

    // Switch to standings tab
    const standingsTab = page.locator('[data-testid="tab-standings"]');
    await expect(standingsTab).toBeVisible();
    await standingsTab.click();

    // Wait for content to change - check for standings table
    await expect(page.locator('[data-testid="standings-table"]')).toBeVisible({ timeout: 10000 });
  });

  test("should display standings table", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 15000,
    });

    // Switch to standings tab
    const standingsTab = page.locator('[data-testid="tab-standings"]');
    await expect(standingsTab).toBeVisible();
    await standingsTab.click();

    // Wait for standings content
    await expect(page.locator('[data-testid="standings-table"]')).toBeVisible({ timeout: 10000 });
  });

  test("should navigate to schedule tab", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 15000,
    });

    // Switch to schedule tab
    const scheduleTab = page.locator('[data-testid="tab-schedule"]');
    await expect(scheduleTab).toBeVisible();
    await scheduleTab.click();

    // Schedule view should be visible
    await expect(page.locator('[data-testid="schedule-view"]')).toBeVisible({ timeout: 10000 });
  });

  test("should navigate to leaders tab", async ({ page }) => {
    await page.goto("/season");

    await expect(page.locator('[data-testid="season-dashboard-page"]')).toBeVisible({
      timeout: 15000,
    });

    // Switch to leaders tab
    const leadersTab = page.locator('[data-testid="tab-leaders"]');
    await expect(leadersTab).toBeVisible();
    await leadersTab.click();

    // Leaders content should be visible
    await expect(page.locator('[data-testid="league-leaders-container"]')).toBeVisible({
      timeout: 10000,
    });
  });
});

import { test, expect } from '@playwright/test';

const mockOffseasonSeason = {
  id: 1,
  year: 2024,
  status: 'OFF_SEASON',
  current_week: 0,
};

test.describe('Offseason Dashboard Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock the current season to be in OFF_SEASON status
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: mockOffseasonSeason });
    });

    // Mock season summary for general dashboard info
    await page.route('**/api/season/summary', async route => {
      await route.fulfill({ json: { season: mockOffseasonSeason, completion_percentage: 100 } });
    });
  });

  test('should load the Offseason Dashboard correctly', async ({ page }) => {
    await page.goto('/offseason');

    // Verify the Offseason Dashboard header is visible
    await expect(page.locator('h1', { hasText: 'Offseason Dashboard' })).toBeVisible();
    await expect(page.locator('p', { hasText: 'Prepare for the next season.' })).toBeVisible();

    // Verify that offseason specific elements are visible
    await expect(page.locator('[data-testid="offseason-phase-display"]')).toBeVisible();
    await expect(page.locator('[data-testid="offseason-phase-display"]')).toContainText('Current Phase: OFF_SEASON');

    // Verify navigation links/buttons for offseason activities
    await expect(page.locator('a', { hasText: 'Draft Room' })).toBeVisible();
    // Add checks for Free Agency once implemented
    // await expect(page.locator('a', { hasText: 'Free Agency' })).toBeVisible(); 
  });

  test('should navigate to Draft Room from Offseason Dashboard', async ({ page }) => {
    await page.goto('/offseason');

    // Ensure the Draft Room link is visible
    const draftRoomLink = page.locator('a', { hasText: 'Draft Room' });
    await expect(draftRoomLink).toBeVisible();

    // Click the Draft Room link and wait for navigation
    const navigationPromise = page.waitForURL('/offseason/draft');
    await draftRoomLink.click();
    await navigationPromise;

    // Verify that the Draft Room page has loaded
    await expect(page.locator('h1', { hasText: 'Draft Room' })).toBeVisible();
  });
});

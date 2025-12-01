import { test, expect } from '@playwright/test';

const mockSystemHealth = { status: 'healthy' };

const mockCurrentSeasonActive = {
  id: 1,
  year: 2024,
  status: 'REGULAR_SEASON',
  current_week: 1,
};

const mockCurrentSeasonNull = null; // Represents no active season

const mockInitializedSeason = {
  id: 2,
  year: 2025,
  status: 'PRE_SEASON',
  current_week: 0,
};

test.describe('Dashboard Flow', () => {
  test('should display dashboard with active season and system health', async ({ page }) => {
    await page.route('**/api/system/health', async route => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    await page.goto('/dashboard');

    // Verify header
    await expect(page.locator('h1', { hasText: 'Mission Control' })).toBeVisible();
    await expect(page.locator('p', { hasText: 'Omniscient System Overview' })).toBeVisible();

    // Verify system health
    await expect(page.locator('.system-status .badge')).toContainText('All Systems Online');

    // Verify season button text for active season
    await expect(page.locator('.start-season-btn')).toContainText('Start Next Season');

    // Verify engine cards (check one example)
    await expect(page.locator('.engine-card', { hasText: 'Genesis Engine' })).toBeVisible();
  });

  test('should display dashboard with no active season and allow starting a new one', async ({ page }) => {
    // Mock initial state: no active season
    let currentSeasonMock = mockCurrentSeasonNull;

    await page.route('**/api/system/health', async route => {
      await route.fulfill({ json: mockSystemHealth });
    });
    
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: currentSeasonMock });
    });

    // Mock season initialization
    await page.route('**/api/season/init', async route => {
      expect(route.request().method()).toBe('POST');
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty('year');
      expect(postData.year).toBe(2025); // Expecting year 2025 as currentSeason is null
      currentSeasonMock = mockInitializedSeason; // Update mock for subsequent getCurrentSeason calls
      await route.fulfill({ status: 200, json: mockInitializedSeason });
    });

    await page.goto('/dashboard');

    // Verify "Start Season" button
    await expect(page.locator('.start-season-btn')).toContainText('Start Season');

    // Mock window.location.reload()
    const reloadPromise = page.waitForEvent('framenavigated', frame => frame.url().includes('/dashboard'));

    // Click Start Season button
    await page.locator('.start-season-btn').click();

    // Wait for the reload to happen and check for new button text
    await reloadPromise;
    await expect(page.locator('.start-season-btn')).toContainText('Start Next Season');

    // Verify that the season info (e.g. current year if displayed) updates
    // This might require a dedicated element in the UI to display the current season year.
    // For now, checking button text is sufficient.
  });
});

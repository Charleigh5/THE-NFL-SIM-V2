import { test, expect } from '@playwright/test';

const mockUserSettingsInitial = {
  user_team_id: 1,
  difficulty_level: 'Pro',
  game_speed: 'medium',
};

const mockUserSettingsUpdated = {
  user_team_id: 1,
  difficulty_level: 'All-Pro',
  game_speed: 'medium',
};

test.describe('Settings Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock initial user settings fetch
    await page.route('**/api/settings', async route => {
      await route.fulfill({ json: mockUserSettingsInitial });
    });

    // Mock settings update (for difficulty)
    await page.route('**/api/settings/difficulty', async route => {
      expect(route.request().method()).toBe('PUT');
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty('difficulty_level');
      expect(postData.difficulty_level).toBe('All-Pro'); // Expecting this update
      await route.fulfill({ status: 200, json: mockUserSettingsUpdated });
    });
  });

  test('should load settings and allow changing difficulty', async ({ page }) => {
    await page.goto('/settings');
    
    // Verify header
    await expect(page.locator('h1', { hasText: 'Settings' })).toBeVisible();

    // Verify initial difficulty level is 'Pro'
    const difficultySelect = page.locator('select[aria-label="Difficulty Level"]');
    await expect(difficultySelect).toHaveValue('Pro');

    // Change difficulty to 'All-Pro'
    await difficultySelect.selectOption('All-Pro');

    // Verify the select now shows 'All-Pro'
    await expect(difficultySelect).toHaveValue('All-Pro');

    // Verify navigation to team selection
    const navigationPromise = page.waitForURL('/team-selection');
    await page.locator('button', { hasText: 'Change Team' }).click();
    await navigationPromise;
  });
});

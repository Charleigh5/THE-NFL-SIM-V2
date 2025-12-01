import { test, expect } from '@playwright/test';

test.describe('Offseason Flow', () => {
  
  test('should load draft room', async ({ page }) => {
    // Mock season as OFF_SEASON
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ 
        json: {
          id: 1,
          year: 2024,
          status: 'OFF_SEASON',
          current_week: 1
        }
      });
    });

    // Mock draft data
    await page.route('**/api/season/1/draft/current', async route => {
      await route.fulfill({
        json: {
          round: 1,
          pick_number: 1,
          team_id: 1
        }
      });
    });

    await page.route('**/api/season/1/offseason/prospects?limit=100', async route => {
      await route.fulfill({ json: [] });
    });

    await page.route('**/api/season/1/offseason/needs/1', async route => {
      await route.fulfill({ json: [] });
    });

    await page.goto('/offseason/draft');
    
    // Verify draft room loads
    await expect(page.locator('.draft-room')).toBeVisible({ timeout: 10000 });
  });

});

import { test, expect } from '@playwright/test';
import { mockTeam } from './fixtures/test-data';

const mockRoster = [
  { 
    id: 1, first_name: 'Kyler', last_name: 'Murray', position: 'QB', overall_rating: 85,
    age: 26, jersey_number: 1, speed: 90, strength: 70, depth_chart_rank: 1, experience: 5
  },
  { 
    id: 2, first_name: 'David', last_name: 'Blough', position: 'QB', overall_rating: 60,
    age: 28, jersey_number: 9, speed: 70, strength: 60, depth_chart_rank: 2, experience: 3
  },
  { 
    id: 3, first_name: 'James', last_name: 'Conner', position: 'RB', overall_rating: 82,
    age: 28, jersey_number: 6, speed: 88, strength: 85, depth_chart_rank: 1, experience: 7
  },
  { 
    id: 4, first_name: 'Keaontay', last_name: 'Ingram', position: 'RB', overall_rating: 70,
    age: 24, jersey_number: 30, speed: 85, strength: 75, depth_chart_rank: 2, experience: 2
  },
  { 
    id: 5, first_name: 'Marquise', last_name: 'Brown', position: 'WR', overall_rating: 84,
    age: 27, jersey_number: 2, speed: 92, strength: 65, depth_chart_rank: 1, experience: 5
  },
];

test.describe('Depth Chart Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock team roster fetch
    await page.route('**/api/teams/1/roster', async route => {
      await route.fulfill({ json: mockRoster });
    });

    // Mock depth chart update
    await page.route('**/api/depth-chart/1/*', async route => {
      expect(route.request().method()).toBe('PUT');
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty('position');
      expect(postData).toHaveProperty('player_ids');
      await route.fulfill({ status: 200, json: { message: 'Depth chart updated' } });
    });
  });

  test('should load depth chart and display QB players', async ({ page }) => {
    await page.goto('/depth-chart');

    // Verify header
    await expect(page.locator('h1', { hasText: 'Depth Chart Editor' })).toBeVisible();

    // Verify QB position is selected
    await expect(page.locator('button', { hasText: 'QB' })).toHaveClass(/bg-cyan-600/);
    await expect(page.locator('h2', { hasText: 'QB Depth Chart' })).toBeVisible();

    // Verify QB players are displayed in order
    const qbPlayers = page.locator('.Reorder_Group > div');
    await expect(qbPlayers).toHaveCount(2);
    await expect(qbPlayers.nth(0)).toContainText('Kyler Murray');
    await expect(qbPlayers.nth(1)).toContainText('David Blough');
  });

  test('should switch position and display RB players', async ({ page }) => {
    await page.goto('/depth-chart');

    // Click RB position button
    await page.locator('button', { hasText: 'RB' }).click();

    // Verify RB position is selected
    await expect(page.locator('button', { hasText: 'RB' })).toHaveClass(/bg-cyan-600/);
    await expect(page.locator('h2', { hasText: 'RB Depth Chart' })).toBeVisible();

    // Verify RB players are displayed in order
    const rbPlayers = page.locator('.Reorder_Group > div');
    await expect(rbPlayers).toHaveCount(2);
    await expect(rbPlayers.nth(0)).toContainText('James Conner');
    await expect(rbPlayers.nth(1)).toContainText('Keaontay Ingram');
  });

  test('should reorder players and save changes', async ({ page }) => {
    await page.goto('/depth-chart');

    // Drag and drop Kyler Murray (index 0) to position 1 (after David Blough)
    const kyler = page.locator('.Reorder_Group > div').nth(0);
    const david = page.locator('.Reorder_Group > div').nth(1);

    await kyler.hover();
    await page.mouse.down();
    await david.hover();
    await page.mouse.up();
    
    // Verify UI reflects new order
    const qbPlayersAfterDrag = page.locator('.Reorder_Group > div');
    await expect(qbPlayersAfterDrag.nth(0)).toContainText('David Blough');
    await expect(qbPlayersAfterDrag.nth(1)).toContainText('Kyler Murray');

    // Click save button
    const saveRequestPromise = page.waitForRequest(request => 
      request.url().includes('/api/depth-chart/1/QB') && request.method() === 'PUT'
    );
    await page.locator('button', { hasText: 'Save Changes' }).click();

    // Wait for the save request to complete
    const saveRequest = await saveRequestPromise;
    const postData = saveRequest.postDataJSON();
    expect(postData.position).toBe('QB');
    expect(postData.player_ids).toEqual([2, 1]); // Expect new order

    // Verify alert message
    page.on('dialog', async dialog => {
      expect(dialog.message()).toContain('Depth chart saved successfully!');
      await dialog.accept();
    });
  });
});

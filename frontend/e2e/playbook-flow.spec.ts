import { test, expect } from '@playwright/test';

test.describe('Playbook Flow', () => {
  test('should load the playbook page', async ({ page }) => {
    await page.goto('/playbook');
    
    // Verify header
    await expect(page.locator('h1', { hasText: 'Playbook' })).toBeVisible();

    // Verify subtitle
    await expect(page.locator('p', { hasText: 'Offensive Scheme: West Coast' })).toBeVisible();

    // Verify the placeholder for the telestrator canvas
    await expect(page.locator('span', { hasText: 'TELESTRATOR_CANVAS_TARGET' })).toBeVisible();

    // Verify Draw and Clear buttons
    await expect(page.locator('button', { hasText: '✏️ Draw' })).toBeVisible();
    await expect(page.locator('button', { hasText: '🗑️ Clear' })).toBeVisible();
  });
});

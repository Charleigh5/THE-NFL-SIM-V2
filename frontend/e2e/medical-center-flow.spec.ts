import { test, expect } from '@playwright/test';

test.describe('Medical Center Flow', () => {
  test('should load the medical center page', async ({ page }) => {
    await page.goto('/medical-center');
    
    // Verify header
    await expect(page.locator('h1', { hasText: 'Medical Center' })).toBeVisible();

    // Verify subtitle
    await expect(page.locator('p', { hasText: 'Roster Health: 92%' })).toBeVisible();

    // Verify the placeholder for the diagram
    await expect(page.locator('span', { hasText: 'BODY_STATUS_DIAGRAM_TARGET' })).toBeVisible();
  });
});

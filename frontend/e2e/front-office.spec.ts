import { test, expect } from '@playwright/test';

test.describe('Front Office Journey', () => {
  
  test('should load front office with team roster', async ({ page }) => {
    await page.goto('/front-office');
    
    // Wait for data to load
    await page.waitForSelector('[data-testid="team-header"]');
    
    // Verify team name
    await expect(page.locator('[data-testid="team-header"]'))
      .toContainText('Arizona Cardinals');
    
    // Verify roster count
    await expect(page.locator('[data-testid="roster-count"]'))
      .toContainText('(52)');
    
    // Verify player cards rendered
    const playerCards = page.locator('[data-testid="player-card"]');
    await expect(playerCards).toHaveCount(52);
  });

  test('should filter roster by position', async ({ page }) => {
    await page.goto('/front-office');
    
    // Click QB filter
    await page.click('[data-testid="filter-qb"]');
    
    // Verify only QBs shown
    const playerCards = page.locator('[data-testid="player-card"]');
    const count = await playerCards.count();
    expect(count).toBeLessThanOrEqual(5); // Usually 2-3 QBs
    
    // Verify all show QB position
    for (let i = 0; i < count; i++) {
      await expect(playerCards.nth(i).locator('[data-testid="position"]'))
        .toHaveText('QB');
    }
  });

});

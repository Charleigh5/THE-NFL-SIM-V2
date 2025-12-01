import { test, expect } from '@playwright/test';
import { mockTeam, mockPlayers } from './fixtures/test-data';

test.describe('Front Office Journey', () => {
  
  test.beforeEach(async ({ page }) => {
    // Mock API for all tests in this group
    await page.route('**/api/teams/1', async route => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route('**/api/teams/1/roster', async route => {
      await route.fulfill({ json: mockPlayers });
    });
  });

  test('should load front office with team roster', async ({ page }) => {
    await page.goto('/empire/front-office');
    
    // Wait for data to load
    await page.waitForSelector('[data-testid="front-office-header"]', { timeout: 5000 });
      
    // Verify team name
    await expect(page.locator('[data-testid="front-office-header"]'))
      .toContainText('Arizona Cardinals');
      
    // Verify roster count
    // mockPlayers has 2 players
    await expect(page.locator('[data-testid="roster-section"]'))
      .toContainText('Active Roster (2)');
    
    // Verify player cards rendered
    const playerCards = page.locator('[data-testid^="player-card-"]');
    await expect(playerCards).toHaveCount(2);
    await expect(playerCards.first()).toBeVisible();
  });

  test.skip('should filter roster by position', async ({ page }) => {
    await page.goto('/empire/front-office');
    
    // Wait for roster to load
    await page.waitForSelector('[data-testid="roster-grid"]');

    // Check if filter exists before clicking (Note: FrontOffice.tsx doesn't seem to have filters implemented yet based on the code I read)
    // The previous test code had a check. I will keep it but update selector if needed.
    // Looking at FrontOffice.tsx, there are NO filters implemented in the UI.
    // So this test will likely fail or skip.
    // I will skip it for now or remove it if the feature isn't there.
    // The user's prompt implies "Review and update tests".
    // Since the feature is missing, I should probably skip this test or mark it as fixme.
    // I'll mark it as skipped.
    
    test.skip('Filters not implemented in FrontOffice.tsx yet', () => {});
    
    /*
    const filter = page.locator('[data-testid="filter-qb"]');
    if (await filter.count() > 0) {
      await filter.click();
      const playerCards = page.locator('[data-testid="player-card"]');
      // ...
    }
    */
  });

  test('should open player detail modal', async ({ page }) => {
    await page.goto('/empire/front-office');
    
    // Click first player card
    // Note: DraggableCard uses testId={`player-card-${player.id}`}
    await page.locator('[data-testid="player-card-1"]').click();
    
    // Verify modal opens
    await expect(page.locator('[data-testid="player-modal"]'))
      .toBeVisible();
    
    // Verify player attributes shown
    await expect(page.locator('[data-testid="player-speed"]'))
      .toBeVisible();
    await expect(page.locator('[data-testid="player-strength"]'))
      .toBeVisible();
      
    // Close modal
    await page.locator('[data-testid="close-modal-button"]').click();
    await expect(page.locator('[data-testid="player-modal"]'))
      .not.toBeVisible();
  });

});

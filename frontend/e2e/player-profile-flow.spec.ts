import { test, expect } from '@playwright/test';

const mockSystemHealth = { status: 'healthy' };

const mockCurrentSeasonActive = {
  id: 1,
  year: 2024,
  status: 'REGULAR_SEASON',
  current_week: 1,
};

const mockPlayerList = [
  { id: 'player1', name: 'Player One', position: 'QB', team: 'Team A' },
  { id: 'player2', name: 'Player Two', position: 'RB', team: 'Team A' },
];

const mockPlayerDetail = {
  id: 'player1',
  name: 'Player One',
  position: 'QB',
  team: 'Team A',
  age: 25,
  overall_rating: 90,
  // ... other player details
};

test.describe('Player Profile Flow', () => {
  test('should navigate to a player profile and display details', async ({ page }) => {
    // Mock system health and current season (common for most tests)
    await page.route('**/api/system/health', async route => {
      await route.fulfill({ json: mockSystemHealth });
    });
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: mockCurrentSeasonActive });
    });

    // Mock the API call for the roster page
    await page.route('**/api/roster', async route => {
      await route.fulfill({ json: mockPlayerList });
    });

    // Mock the API call for a specific player's detail
    await page.route('**/api/player/player1', async route => {
      await route.fulfill({ json: mockPlayerDetail });
    });

    // 1. Navigate to the roster page (assuming /roster is the path)
    await page.goto('/roster');

    // Verify roster page is loaded (e.g., check for a title or player list element)
    await expect(page.locator('h1', { hasText: 'Team Roster' })).toBeVisible();
    await expect(page.locator(`text=${mockPlayerList[0].name}`)).toBeVisible();

    // 2. Click on a player's name to go to their profile page
    await page.locator(`text=${mockPlayerList[0].name}`).click();

    // 3. Verify that the player's name and position are displayed on the profile page
    // Assuming the player profile page has an h1 with the player's name and a p with position
    await expect(page.locator('h1', { hasText: mockPlayerDetail.name })).toBeVisible();
    await expect(page.locator('p', { hasText: `Position: ${mockPlayerDetail.position}` })).toBeVisible();
    await expect(page.locator('p', { hasText: `Team: ${mockPlayerDetail.team}` })).toBeVisible();
    await expect(page.locator('p', { hasText: `Age: ${mockPlayerDetail.age}` })).toBeVisible();
    await expect(page.locator('p', { hasText: `Overall Rating: ${mockPlayerDetail.overall_rating}` })).toBeVisible();
  });
});

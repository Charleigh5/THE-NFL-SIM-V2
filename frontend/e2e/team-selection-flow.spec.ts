import { test, expect } from '@playwright/test';
import { mockTeam } from './fixtures/test-data'; // Re-using mockTeam for consistency

const mockAllTeams = [
  mockTeam, // Arizona Cardinals (id: 1)
  { id: 2, name: '49ers', city: 'San Francisco', abbreviation: 'SF', conference: 'NFC', division: 'West', wins: 0, losses: 0, ties: 0 },
  { id: 3, name: 'Seahawks', city: 'Seattle', abbreviation: 'SEA', conference: 'NFC', division: 'West', wins: 0, losses: 0, ties: 0 },
];

const mockUserSettings = {
  user_team_id: null, // Initially no team selected
  difficulty: 'normal',
  game_speed: 'medium',
};

const mockUserSettingsAfterSelection = {
  user_team_id: 1, // Arizona Cardinals selected
  difficulty: 'normal',
  game_speed: 'medium',
};

test.describe('Team Selection Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock getTeams API call
    await page.route('**/api/teams', async route => {
      await route.fulfill({ json: mockAllTeams });
    });

    // Mock initial user settings (no team selected)
    await page.route('**/api/settings', async route => {
      await route.fulfill({ json: mockUserSettings });
    });

    // Mock setting the user's team
    await page.route('**/api/settings/team', async route => {
      expect(route.request().method()).toBe('PUT');
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty('team_id');
      await route.fulfill({ status: 200, json: mockUserSettingsAfterSelection });
    });
  });

  test('should display all teams and allow selection', async ({ page }) => {
    await page.goto('/team-selection');
    
    // Verify header
    await expect(page.locator('h1', { hasText: 'Select Your Franchise' })).toBeVisible();
    await expect(page.locator('p', { hasText: 'Choose the team you will lead to glory.' })).toBeVisible();

    // Verify all mock team cards are displayed
    const teamCards = page.locator('.team-card');
    await expect(teamCards).toHaveCount(mockAllTeams.length);
    await expect(teamCards.first()).toContainText('Arizona Cardinals');
    await expect(teamCards.nth(1)).toContainText('San Francisco 49ers');
    await expect(teamCards.nth(2)).toContainText('Seattle Seahawks');

    // Click on a team card (e.g., Arizona Cardinals)
    const teamToSelect = mockAllTeams[0]; // Arizona Cardinals
    const teamCard = page.locator(`.team-card:has-text("${teamToSelect.city} ${teamToSelect.name}")`);
    await expect(teamCard).toBeVisible();

    // Expect navigation to dashboard after selection
    const navigationPromise = page.waitForURL('/dashboard');
    await teamCard.click();
    await navigationPromise;

    // Optionally, verify that the selected team has the 'selected' class (if not navigated immediately)
    // await expect(teamCard).toHaveClass(/selected/); 
    
    // After navigation, we can check if the dashboard loaded (assuming dashboard has a distinct element)
    await expect(page.locator('body')).not.toContainText('Select Your Franchise'); // No longer on team selection page
  });
});

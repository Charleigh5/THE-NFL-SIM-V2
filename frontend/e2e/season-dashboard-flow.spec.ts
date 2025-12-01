import { test, expect } from '@playwright/test';
import { mockTeam } from './fixtures/test-data';

const mockStandings = [
  { team_id: 1, team_name: 'Arizona Cardinals', wins: 5, losses: 2, ties: 0 },
  { team_id: 2, team_name: 'San Francisco 49ers', wins: 6, losses: 1, ties: 0 },
  { team_id: 3, team_name: 'Seattle Seahawks', wins: 4, losses: 3, ties: 0 },
  { team_id: 4, team_name: 'Los Angeles Rams', wins: 3, losses: 4, ties: 0 },
];

const mockSchedule = [
  { 
    id: 1, 
    week: 1, 
    home_team_id: 1, 
    away_team_id: 2, 
    home_score: 20, 
    away_score: 24, 
    status: 'COMPLETED',
    home_team_name: 'Arizona Cardinals',
    away_team_name: 'San Francisco 49ers',
  },
  { 
    id: 2, 
    week: 2, 
    home_team_id: 1, 
    away_team_id: 3, 
    home_score: null, 
    away_score: null, 
    status: 'SCHEDULED',
    home_team_name: 'Arizona Cardinals',
    away_team_name: 'Seattle Seahawks',
  },
];

const mockSeasonActive = {
  id: 1,
  year: 2024,
  status: 'REGULAR_SEASON',
  current_week: 2
};

test.describe('Season Dashboard Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: mockSeasonActive });
    });
    await page.route('**/api/teams/1', async route => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route('**/api/standings', async route => {
      await route.fulfill({ json: mockStandings });
    });
    await page.route('**/api/schedule*', async route => { // Use * to match query params
      await route.fulfill({ json: mockSchedule });
    });
  });

  test('should load season dashboard with standings and schedule', async ({ page }) => {
    await page.goto('/season-dashboard');
    
    // Verify Season Dashboard header
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toBeVisible();
    await expect(page.locator('[data-testid="season-dashboard-header"]')).toContainText('2024 Season - Week 2');

    // Verify Standings section
    await expect(page.locator('[data-testid="standings-table"]')).toBeVisible();
    await expect(page.locator('[data-testid="standings-table-row-Arizona Cardinals"]')).toBeVisible();
    await expect(page.locator('[data-testid="standings-table-row-Arizona Cardinals"]')).toContainText('5-2-0');

    // Verify Schedule section
    await expect(page.locator('[data-testid="schedule-section"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-1"]')).toContainText('Arizona Cardinals vs San Francisco 49ers');
    await expect(page.locator('[data-testid="schedule-game-1"]')).toContainText('Final: 20 - 24');

    await expect(page.locator('[data-testid="schedule-game-2"]')).toBeVisible();
    await expect(page.locator('[data-testid="schedule-game-2"]')).toContainText('Arizona Cardinals vs Seattle Seahawks');
    await expect(page.locator('[data-testid="schedule-game-2"]')).toContainText('Upcoming');
  });
});

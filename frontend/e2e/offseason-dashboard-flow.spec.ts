import { test, expect } from '@playwright/test';
import { mockTeam } from './fixtures/test-data';

const mockSeasonOffseason = {
  id: 1,
  year: 2024,
  status: 'OFF_SEASON',
  current_week: 0,
};

const mockTeamNeeds = [
  { position: 'QB', count: 1, current_overall: 70, description: 'Need a starting QB' },
  { position: 'WR', count: 2, current_overall: 75, description: 'Need depth at WR' },
];

const mockProspects = [
  { id: 1, first_name: 'Top', last_name: 'QB', position: 'QB', overall_rating: 90, age: 21, college: 'USC' },
  { id: 2, first_name: 'Mid', last_name: 'WR', position: 'WR', overall_rating: 80, age: 22, college: 'LSU' },
];

const mockSalaryCapData = {
  total_cap: 220000000,
  salary_committed: 180000000,
  cap_space: 40000000,
  players_under_contract: 45,
};

const mockPlayerProgressionResult = [
  { player_id: 1, player_name: 'Kyler Murray', old_overall: 85, new_overall: 86, change: 1, reason: 'Developed well' },
];

const mockDraftSummary = [
  { team_id: 1, team_name: 'Arizona Cardinals', round: 1, pick_number: 1, player_name: 'Top QB', player_position: 'QB', player_overall: 90 },
];

test.describe('Offseason Dashboard Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock user settings to ensure userTeamId is set
    await page.route('**/api/settings', async route => {
      await route.fulfill({ json: { user_team_id: mockTeam.id, difficulty_level: 'Pro', game_speed: 'medium' } });
    });
    await page.route('**/api/teams/1', async route => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route('**/api/season/current', async route => {
      await route.fulfill({ json: mockSeasonOffseason });
    });
    await page.route('**/api/season/1/offseason/needs/1', async route => {
      await route.fulfill({ json: mockTeamNeeds });
    });
    await page.route('**/api/season/1/offseason/salary-cap/1', async route => {
      await route.fulfill({ json: mockSalaryCapData });
    });
    await page.route('**/api/season/1/offseason/prospects*', async route => {
      await route.fulfill({ json: mockProspects });
    });
  });

  test('should load offseason dashboard and progress through phases', async ({ page }) => {
    await page.goto('/offseason-dashboard');

    // Verify initial load
    await expect(page.locator('h1', { hasText: 'Offseason Dashboard' })).toBeVisible();
    await expect(page.locator('[data-testid="offseason-header"]')).toContainText('2024 Offseason');
    await expect(page.locator('[data-testid="start-offseason-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="simulate-progression-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="simulate-draft-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="simulate-fa-button"]')).toBeVisible();

    // --- Phase 1: Start Offseason ---
    await page.route('**/api/season/1/offseason/start', async route => {
      await route.fulfill({ status: 200, json: { message: 'Offseason started!' } });
    });
    await page.locator('[data-testid="start-offseason-button"]').click();
    await expect(page.locator('.status-message')).toContainText('Offseason started!');

    // --- Phase 2: Simulate Progression ---
    await page.route('**/api/season/1/offseason/simulate-progression', async route => {
      await route.fulfill({ status: 200, json: mockPlayerProgressionResult });
    });
    await page.locator('[data-testid="simulate-progression-button"]').click();
    await expect(page.locator('.status-message')).toContainText('Player Progression Simulated!');
    await expect(page.locator('[data-testid="player-progression-card"]')).toContainText('Kyler Murray');

    // --- Phase 3: Simulate Draft ---
    await page.route('**/api/season/1/offseason/simulate-draft', async route => {
      await route.fulfill({ status: 200, json: mockDraftSummary });
    });
    await page.locator('[data-testid="simulate-draft-button"]').click();
    await expect(page.locator('.status-message')).toContainText('Draft Simulated!');
    await expect(page.locator('[data-testid="draft-summary"]')).toBeVisible();
    await expect(page.locator('[data-testid="draft-pick-item-1"]')).toContainText('Rd 1 Pick 1 QB Top QB');

    // --- Phase 4: Simulate Free Agency ---
    await page.route('**/api/season/1/offseason/simulate-free-agency', async route => {
      await route.fulfill({ status: 200, json: { message: 'Free Agency Simulated!' } });
    });
    await page.locator('[data-testid="simulate-fa-button"]').click();
    await expect(page.locator('.status-message')).toContainText('Free Agency Simulated!');
  });
});

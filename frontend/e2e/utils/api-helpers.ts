import { Page } from '@playwright/test';

export async function seedDatabase() {
  // Call backend API to reset and seed test data
  // Implementation depends on backend test endpoints
}

export async function createTestSeason(page: Page) {
  const response = await page.request.post('/api/season/init');
  return await response.json();
}

export async function simulateWeek(page: Page, seasonId: number, week: number) {
  const response = await page.request.post(`/api/season/simulate-week`, {
    data: { season_id: seasonId, week }
  });
  return await response.json();
}

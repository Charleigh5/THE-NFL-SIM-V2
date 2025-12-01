import { Page } from '@playwright/test';

export async function seedDatabase(page: Page) {
  // Call backend API to reset and seed test data
  // This is a placeholder. You might need to implement a specific endpoint in the backend for this.
  // For example: await page.request.post('/api/test/seed');
  console.log('Database seeding requested (not implemented)');
}

export async function createTestSeason(page: Page) {
  const response = await page.request.post('/api/season/init');
  if (!response.ok()) {
    throw new Error(`Failed to create test season: ${response.status()} ${response.statusText()}`);
  }
  return await response.json();
}

export async function simulateWeek(page: Page, seasonId: number, week: number) {
  const response = await page.request.post(`/api/season/simulate-week`, {
    data: { season_id: seasonId, week }
  });
  if (!response.ok()) {
    throw new Error(`Failed to simulate week: ${response.status()} ${response.statusText()}`);
  }
  return await response.json();
}
export async function setupCompletedSeason(page: Page) {
  const season = await createTestSeason(page);
  
  // Simulate to playoffs (this includes generating the bracket)
  const response = await page.request.post(`/api/season/${season.id}/simulate-to-playoffs`, {
    timeout: 60000 // Allow more time for full season simulation
  });
  
  if (!response.ok()) {
    throw new Error(`Failed to simulate to playoffs: ${response.status()} ${response.statusText()}`);
  }
  
  return season;
}

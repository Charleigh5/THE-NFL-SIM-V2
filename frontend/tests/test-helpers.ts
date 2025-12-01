import { APIRequestContext, Page, expect } from "@playwright/test";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export const TestHelpers = {
  /**
   * Seeds the database with initial data.
   * This calls the backend /genesis/seed endpoint.
   */
  async seedDatabase(request: APIRequestContext) {
    const response = await request.post(`${BACKEND_URL}/api/genesis/seed`);
    if (response.status() === 404) {
      console.warn("Seed endpoint not found, skipping seed.");
      return;
    }
    if (!response.ok()) {
      console.error(`Seed failed: ${response.status()} ${response.statusText()}`);
      console.error(await response.text());
    }
    expect(response.ok()).toBeTruthy();
  },

  /**
   * Waits for the season to be initialized.
   * This can be used to wait for the backend to finish processing.
   */
  async waitForSeasonInit(page: Page) {
    // Wait for the season year indicator to appear
    await expect(page.locator("text=/20\\d{2} Season/")).toBeVisible({ timeout: 60000 });
  },

  /**
   * Checks if the dashboard is loaded without errors.
   */
  async verifyDashboardLoaded(page: Page) {
    await expect(page.locator("text=Error")).not.toBeVisible();
    await expect(page.locator(".dashboard-title")).toBeVisible();
  },
};

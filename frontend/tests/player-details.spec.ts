import { test, expect } from "@playwright/test";
import { TestHelpers } from "./test-helpers";

test.describe("Player Details", () => {
  test.beforeEach(async ({ request }) => {
    await TestHelpers.seedDatabase(request);
  });

  test("View Player Details Modal", async ({ page }) => {
    // 1. Navigate to Season Dashboard
    await page.goto("/season");

    // Wait for initial loading to finish
    await expect(async () => {
      const startVisible = await page
        .locator("button.action-button", { hasText: "Initialize New Season" })
        .isVisible();
      const dashboardVisible = await page.locator(".dashboard-header").isVisible();
      expect(startVisible || dashboardVisible).toBeTruthy();
    }).toPass();

    // Start season if needed
    const startButton = page.locator("button.action-button", { hasText: "Initialize New Season" });
    if (await startButton.isVisible()) {
      await startButton.click();
      // Wait for season to be loaded (tabs to appear)
      await expect(page.locator('button[title="View league statistical leaders"]')).toBeVisible({
        timeout: 30000,
      });
    }

    // 2. Navigate to Leaders tab
    const leadersTab = page.locator('button[title="View league statistical leaders"]');
    await expect(leadersTab).toBeVisible();
    await leadersTab.click();

    // 3. Click on player name
    const playerLink = page.locator(".leader-info h4").first();
    await expect(playerLink).toBeVisible();
    const playerName = await playerLink.innerText();

    await playerLink.click();

    // 4. Verify player modal opens
    const modal = page.locator(".player-modal-overlay");
    await expect(modal).toBeVisible();

    // 5. Verify all attributes displayed
    const modalContent = modal.locator(".player-modal-content");
    await expect(modalContent).toContainText(playerName);
    await expect(modalContent).toContainText("Position");
    await expect(modalContent).toContainText("Team");
    await expect(modalContent).toContainText("Age");
    await expect(modalContent).toContainText("Overall");

    // 6. Verify career stats shown
    await expect(modalContent).toContainText("Career Stats");
    await expect(modalContent.locator("table.career-stats-table")).toBeVisible();
  });
});

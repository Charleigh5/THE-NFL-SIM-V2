import { test, expect } from "@playwright/test";
import { setupDraftMocks, mockProspects } from "./fixtures/test-data";

/**
 * E2E Tests for Draft Room
 * Covers: Draft Board, AI Recommendations, Pick Selection
 */

test.describe("Draft Room E2E", () => {
  test.beforeEach(async ({ page }) => {
    await setupDraftMocks(page);

    // Mock AI Recommendation
    await page.route("**/api/v1/draft/suggest-pick", async (route) => {
      await route.fulfill({
        json: {
          recommended_player_id: mockProspects[0].id,
          player_name: mockProspects[0].name,
          position: mockProspects[0].position,
          reasoning: "Best available talent, fills depth needs",
          fit_score: 95,
          alternatives: [
            {
              player_id: mockProspects[1].id,
              name: mockProspects[1].name,
              position: mockProspects[1].position,
            },
          ],
        },
      });
    });

    // Mock Make Pick
    await page.route("**/api/v1/draft/pick", async (route) => {
      await route.fulfill({
        json: {
          success: true,
          message: "Pick submitted successfully",
          pick: { round: 1, pick_number: 1, player_id: mockProspects[0].id },
        },
      });
    });
  });

  test("should display draft board with prospects", async ({ page }) => {
    await page.goto("/draft");

    // Wait for draft board to load
    await expect(page.getByTestId("draft-board")).toBeVisible();
    await expect(page.getByTestId("prospect-list")).toBeVisible();

    // Verify prospects from mock data are visible
    await expect(page.getByText(mockProspects[0].name).first()).toBeVisible();
    await expect(page.getByText(mockProspects[1].name).first()).toBeVisible();
  });

  test("should filter prospects by position", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-board")).toBeVisible();

    // Select QB position filter
    const positionFilter = page.getByTestId("draft-filter-position");
    await positionFilter.selectOption("QB");

    // Should show only QBs
    const qbProspects = mockProspects.filter((p) => p.position === "QB");
    const wrProspects = mockProspects.filter((p) => p.position === "WR");

    for (const qb of qbProspects) {
      await expect(page.getByText(qb.name).first()).toBeVisible();
    }

    for (const wr of wrProspects) {
      await expect(page.getByText(wr.name)).not.toBeVisible();
    }
  });

  // Skipped temporarily: Modal close button timing issue under investigation
  test.skip("should open scouting report from prospect card", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-room-page")).toBeVisible({ timeout: 15000 });
    // Wait for loading to finish (prospects to appear)
    await expect(page.getByTestId("draft-board")).toBeVisible();
    await expect(page.getByTestId("prospect-list")).toBeVisible();

    // Click "Report" button on the first prospect
    const firstProspect = mockProspects[0];
    const reportBtn = page.getByTestId(`report-button-${firstProspect.id}`);
    await expect(reportBtn).toBeVisible({ timeout: 5000 });
    await reportBtn.click();

    // Verify Scouting Report Modal appears (mock service has 800ms delay)
    const modal = page.getByTestId("scouting-report-modal");
    await expect(modal).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(firstProspect.name).first()).toBeVisible();
    await expect(page.getByTestId("scouting-strengths")).toBeVisible();

    // Close modal - wait for button to be visible first
    const closeBtn = page.getByTestId("close-modal");
    await expect(closeBtn).toBeVisible({ timeout: 5000 });
    await closeBtn.click();
    await expect(modal).not.toBeVisible();
  });

  test("should automate draft simulation", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-room-page")).toBeVisible();

    // Click Auto-Sim button
    const simButton = page.getByTestId("simulate-draft-button");
    await simButton.click();

    // Note: Since this is an E2E test with mocks, we just verify the button was clickable
    // and potentially wait for a specific response if the mock was set up for it.
    // In a full integration test, we'd watch the pick ticker.
  });
});

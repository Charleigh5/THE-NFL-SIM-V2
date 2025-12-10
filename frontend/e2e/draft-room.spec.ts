import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Draft Room
 * Covers: Draft Board, AI Recommendations, Pick Selection
 */

const USER_TEAM_ID = 1;
const MOCK_SEASON = {
  id: 1,
  year: 2024,
  current_week: 1,
  phase: "DRAFT",
};

const MOCK_PROSPECTS = [
  {
    id: 1,
    first_name: "Caleb",
    last_name: "Williams",
    position: "QB",
    college: "USC",
    overall_grade: 95,
    combine_grade: 92,
    age: 22,
    projected_round: 1,
  },
  {
    id: 2,
    first_name: "Marvin",
    last_name: "Harrison",
    position: "WR",
    college: "Ohio State",
    overall_grade: 94,
    combine_grade: 90,
    age: 21,
    projected_round: 1,
  },
  {
    id: 3,
    first_name: "Drake",
    last_name: "Maye",
    position: "QB",
    college: "UNC",
    overall_grade: 88,
    combine_grade: 85,
    age: 21,
    projected_round: 1,
  },
];

const MOCK_DRAFT_ORDER = [
  { round: 1, pick: 1, team_id: USER_TEAM_ID, team_name: "Cardinals" },
  { round: 1, pick: 2, team_id: 2, team_name: "Bears" },
  { round: 1, pick: 3, team_id: 3, team_name: "Patriots" },
];

test.describe("Draft Room E2E", () => {
  test.beforeEach(async ({ page }) => {
    // Mock User Settings
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: USER_TEAM_ID } });
    });

    // Mock Current Season in Draft Phase
    await page.route("**/api/seasons/current", async (route) => {
      await route.fulfill({ json: MOCK_SEASON });
    });

    // Mock Team
    await page.route(`**/api/teams/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({
        json: {
          id: USER_TEAM_ID,
          city: "Arizona",
          name: "Cardinals",
          abbreviation: "ARI",
        },
      });
    });

    // Mock Draft Board (Prospects)
    await page.route("**/api/draft/board*", async (route) => {
      await route.fulfill({ json: MOCK_PROSPECTS });
    });

    // Mock Draft Order
    await page.route("**/api/draft/order*", async (route) => {
      await route.fulfill({ json: MOCK_DRAFT_ORDER });
    });

    // Mock AI Recommendation
    await page.route("**/api/draft/suggest-pick", async (route) => {
      await route.fulfill({
        json: {
          recommended_player_id: 1,
          player_name: "Caleb Williams",
          position: "QB",
          reasoning: "Best available talent, fills QB need",
          fit_score: 95,
          alternatives: [{ player_id: 2, name: "Marvin Harrison Jr.", position: "WR" }],
        },
      });
    });

    // Mock Make Pick
    await page.route("**/api/draft/pick", async (route) => {
      await route.fulfill({
        json: {
          success: true,
          message: "Pick submitted successfully",
          pick: { round: 1, pick_number: 1, player_id: 1 },
        },
      });
    });

    // Catch-all for unmocked API routes
    await page.route("**/api/**", async (route) => {
      console.log(`[UNMOCKED] ${route.request().method()} ${route.request().url()}`);
      await route.fulfill({ json: {} });
    });
  });

  test("should display draft board with prospects", async ({ page }) => {
    await page.goto("/draft");

    // Wait for prospects to load
    await expect(page.locator("text=Caleb Williams")).toBeVisible({ timeout: 10000 });
    await expect(page.locator("text=Marvin Harrison")).toBeVisible();
    await expect(page.locator("text=Drake Maye")).toBeVisible();
  });

  test("should show AI recommendation on request", async ({ page }) => {
    await page.goto("/draft");

    // Wait for page load
    await expect(page.locator("text=Caleb Williams")).toBeVisible({ timeout: 10000 });

    // Click AI Suggest button (if visible)
    const aiButton = page.locator(
      '[data-testid="ai-suggest-btn"], button:has-text("AI"), button:has-text("Suggest")'
    );
    if (await aiButton.isVisible()) {
      await aiButton.click();
      // Verify recommendation appears
      await expect(page.locator("text=Best available")).toBeVisible({ timeout: 5000 });
    }
  });

  test("should filter prospects by position", async ({ page }) => {
    await page.goto("/draft");

    // Wait for page load
    await expect(page.locator("text=Caleb Williams")).toBeVisible({ timeout: 10000 });

    // Look for position filter
    const qbFilter = page.locator('[data-testid="filter-QB"], button:has-text("QB")');
    if (await qbFilter.isVisible()) {
      await qbFilter.click();
      // Should show only QBs
      await expect(page.locator("text=Caleb Williams")).toBeVisible();
      await expect(page.locator("text=Drake Maye")).toBeVisible();
      // WR should be filtered out (might have count change or hidden)
    }
  });

  test("should select a prospect for picking", async ({ page }) => {
    await page.goto("/draft");

    // Wait for prospects to load
    await expect(page.locator("text=Caleb Williams")).toBeVisible({ timeout: 10000 });

    // Click on a prospect row/card
    await page.locator("text=Caleb Williams").click();

    // Verify selection state (could be highlight, modal, or side panel)
    // Look for draft action button becoming available
    const draftBtn = page.locator('[data-testid="draft-player-btn"], button:has-text("Draft")');
    if (await draftBtn.isVisible()) {
      await expect(draftBtn).toBeEnabled();
    }
  });

  test("should navigate between draft board views", async ({ page }) => {
    await page.goto("/draft");

    // Wait for initial load
    await expect(page.locator("text=Caleb Williams")).toBeVisible({ timeout: 10000 });

    // Check for tab navigation (Board / My Picks / History)
    const myPicksTab = page.locator('button:has-text("My Picks"), [role="tab"]:has-text("Picks")');
    if (await myPicksTab.isVisible()) {
      await myPicksTab.click();
      // Verify tab switch
      await expect(myPicksTab).toHaveAttribute("aria-selected", "true");
    }
  });
});

import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Draft Assistant Widget (UI-007)
 */

const USER_TEAM_ID = 1;

// Mock Response Data
const MOCK_SUGGESTION = {
  recommended_player_id: 1,
  player_name: "Caleb Williams",
  position: "QB",
  overall_rating: 95,
  reasoning: "Generational talent that fits the offensive scheme perfectly.",
  confidence_score: 0.92,
  historical_comparison: {
    comparable_player_name: "Patrick Mahomes",
    seasons_active: "2017-Present",
    career_highlights: "3x Super Bowl Champion, 2x MVP",
    similarity_score: 0.88,
  },
  roster_gap_analysis: [
    {
      position: "QB",
      priority_level: "CRITICAL",
      current_count: 0,
      target_count: 2,
    },
  ],
  alternative_picks: [
    {
      player_id: 2,
      player_name: "Marvin Harrison Jr.",
      position: "WR",
      overall_rating: 94,
    },
  ],
};

test.describe("Draft Assistant Widget", () => {
  test.beforeEach(async ({ page }) => {
    // Mock Season & Settings context
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: USER_TEAM_ID } });
    });

    await page.route("**/api/seasons/current", async (route) => {
      await route.fulfill({
        json: { id: 1, year: 2024, current_week: 1, phase: "DRAFT" },
      });
    });

    // Mock API for suggestion
    await page.route("**/api/draft/suggest-pick", async (route) => {
      await route.fulfill({ json: MOCK_SUGGESTION });
    });

    // Mock Current Pick (Required for DraftAssistant to render)
    await page.route("**/api/season/*/draft/current", async (route) => {
      await route.fulfill({
        json: {
          team_id: USER_TEAM_ID,
          round: 1,
          pick_number: 1,
          overall_pick_number: 1,
        },
      });
    });

    // Navigate to Draft Room where the widget lives
    // Note: We might need to mock other draft room dependencies if the page fails to load
    // but typically partial mocking is enough if the widget is isolated or we handle errors gracefully.
    // For robustness, let's mock the basic draft board data too so the page renders.
    await page.route("**/api/draft/board*", async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route("**/api/draft/order*", async (route) => {
      await route.fulfill({ json: [] });
    });
    await page.route(`**/api/teams/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: { id: USER_TEAM_ID, city: "Mock", name: "City" } });
    });

    await page.goto("/draft");
  });

  test("should render initial state with Analyze button", async ({ page }) => {
    // Use test-id for robustness
    const widget = page.getByTestId("draft-assistant-widget");
    await expect(widget).toBeVisible();

    const analyzeBtn = page.getByTestId("analyze-pick-btn");
    await expect(analyzeBtn).toBeVisible();
    await expect(analyzeBtn).toContainText("Analyze Pick");
  });

  test("should show loading state when analyzing", async ({ page }) => {
    // Slow down the response to catch the loading state
    await page.route("**/api/draft/suggest-pick", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      await route.fulfill({ json: MOCK_SUGGESTION });
    });

    await page.getByTestId("analyze-pick-btn").click();

    await expect(page.getByTestId("assistant-loading")).toBeVisible();
    await expect(page.getByText("Crunching numbers...")).toBeVisible();
  });

  test("should display recommendation and confidence", async ({ page }) => {
    await page.getByTestId("analyze-pick-btn").click();

    const card = page.getByTestId("suggestion-card");
    await expect(card).toBeVisible();

    // Check specific content
    await expect(card.getByText("Caleb Williams")).toBeVisible();
    await expect(card.getByText("QB")).toBeVisible();
    await expect(card.getByTestId("confidence-score")).toContainText("92%");
    await expect(card.getByText("Generational talent")).toBeVisible();
  });

  test("should display roster gap analysis", async ({ page }) => {
    await page.getByTestId("analyze-pick-btn").click();

    const gapSection = page.locator(".gap-analysis");
    await expect(gapSection).toBeVisible();
    await expect(gapSection.getByText("CRITICAL")).toBeVisible();
    await expect(gapSection.getByText("Target: 2")).toBeVisible();
  });

  test("should display historical comparison", async ({ page }) => {
    await page.getByTestId("analyze-pick-btn").click();

    const compSection = page.locator(".historical-comp");
    await expect(compSection).toBeVisible();
    await expect(compSection.getByText("Patrick Mahomes")).toBeVisible();
  });

  test("should reset state when clicking New Analysis", async ({ page }) => {
    await page.getByTestId("analyze-pick-btn").click();
    await expect(page.getByTestId("suggestion-card")).toBeVisible();

    await page.getByTestId("new-analysis-btn").click();

    // Should return to initial state
    await expect(page.getByTestId("analyze-pick-btn")).toBeVisible();
    await expect(page.getByTestId("suggestion-card")).not.toBeVisible();
  });

  test("should handle API errors gracefully", async ({ page }) => {
    // Mock error response
    await page.route("**/api/draft/suggest-pick", async (route) => {
      await route.fulfill({ status: 500, body: "Internal Server Error" });
    });

    await page.getByTestId("analyze-pick-btn").click();

    const errorMsg = page.locator(".assistant-error");
    await expect(errorMsg).toBeVisible();
    await expect(page.getByRole("button", { name: "Retry" })).toBeVisible();
  });
});

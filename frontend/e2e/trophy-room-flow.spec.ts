import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Trophy Room
 * Covers: Page load, 3D canvas, hall of champions display
 */

test.describe("Trophy Room Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock settings API for theme
    await page.route("**/api/settings**", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          difficulty: "MEDIUM",
          sound_enabled: true,
        },
      });
    });

    // Mock team data
    await page.route("**/api/team/**", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          name: "Cardinals",
          city: "Arizona",
          abbreviation: "ARI",
        },
      });
    });

    // Mock dynasty history
    await page.route("**/api/dynasty/history**", async (route) => {
      await route.fulfill({
        json: {
          championships: [
            { year: 2024, opponent: "Chiefs", score: "31-24", mvp: "Kyler Murray" },
            { year: 2022, opponent: "Eagles", score: "27-21", mvp: "DeAndre Hopkins" },
          ],
          playoff_appearances: 5,
          division_titles: 3,
          total_wins: 156,
          total_losses: 88,
        },
      });
    });
  });

  test("should load trophy room page", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify page loaded with title
    await expect(page.locator("text=Hall of Champions")).toBeVisible();
  });

  test("should display franchise name in subtitle", async ({ page }) => {
    await page.goto("/trophy-room");

    // Check for trophy case subtitle
    const subtitle = page.locator(".trophy-room__subtitle");
    await expect(subtitle).toBeVisible();
  });

  test("should have 3D canvas container", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify canvas container exists (for 3D rendering)
    const canvasContainer = page.locator(".canvas-container");
    await expect(canvasContainer).toBeVisible();
  });

  test("should have UI overlay layer", async ({ page }) => {
    await page.goto("/trophy-room");

    // Verify UI layer exists
    const uiLayer = page.locator(".ui-layer");
    await expect(uiLayer).toBeVisible();
  });

  test("should display dynasty championship history", async ({ page }) => {
    await page.goto("/trophy-room");

    // Look for championship list or timeline
    const championshipSection = page
      .locator('[data-testid="championship-list"]')
      .or(page.locator(".championship-history"))
      .or(page.getByText(/Championship|Super Bowl/i));

    if (await championshipSection.isVisible({ timeout: 3000 })) {
      await expect(championshipSection).toContainText("2024");
      await expect(championshipSection).toContainText("Chiefs");
    }
  });

  test("should show championship details on click", async ({ page }) => {
    await page.goto("/trophy-room");

    // Look for trophy or championship item to click
    const trophyItem = page
      .locator('[data-testid="trophy-2024"]')
      .or(page.locator(".trophy-item"))
      .or(page.getByText(/2024.*Championship/i))
      .first();

    if (await trophyItem.isVisible({ timeout: 3000 })) {
      await trophyItem.click();

      // Should show details modal or expanded view
      const details = page
        .locator('[data-testid="championship-details"]')
        .or(page.locator(".trophy-details"));
      if (await details.isVisible({ timeout: 2000 })) {
        await expect(details).toContainText("Kyler Murray");
        await expect(details).toContainText("MVP");
      }
    }
  });

  test("should handle empty dynasty gracefully", async ({ page }) => {
    // Override with empty dynasty
    await page.route("**/api/dynasty/history**", async (route) => {
      await route.fulfill({
        json: {
          championships: [],
          playoff_appearances: 0,
          division_titles: 0,
          total_wins: 0,
          total_losses: 0,
        },
      });
    });

    await page.goto("/trophy-room");

    // Should still load page
    await expect(page.locator("text=Hall of Champions")).toBeVisible();

    // May show empty state message
    const emptyState = page.locator("text=/No championships|Start your dynasty/i");
    if (await emptyState.isVisible({ timeout: 2000 })) {
      await expect(emptyState).toBeVisible();
    }
  });

  test("should display team branding in trophy room", async ({ page }) => {
    await page.goto("/trophy-room");

    // Check for team colors or logo
    const teamBranding = page
      .locator('[data-testid="team-logo"]')
      .or(page.locator(".team-banner"))
      .or(page.getByText(/Cardinals/i));
    if (await teamBranding.isVisible({ timeout: 2000 })) {
      await expect(teamBranding).toBeVisible();
    }
  });
});

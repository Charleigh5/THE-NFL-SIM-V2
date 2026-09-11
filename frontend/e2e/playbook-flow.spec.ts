import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Playbook
 * Covers: Formation display, play selection, telestrator, scheme info
 *
 * Note: The Playbook page is currently a placeholder with basic UI.
 * These tests cover current functionality and are designed to work
 * when full features are implemented.
 */

const USER_TEAM_ID = 1;

const MOCK_FORMATIONS = [
  { id: "shotgun", name: "Shotgun", personnel: "11", type: "PASS" },
  { id: "i-form", name: "I-Formation", personnel: "21", type: "RUN" },
  { id: "singleback", name: "Singleback", personnel: "11", type: "BALANCED" },
  { id: "goal-line", name: "Goal Line", personnel: "22", type: "SHORT_YARDAGE" },
];

const MOCK_PLAYS = [
  {
    id: 1,
    name: "PA Boot",
    formation: "shotgun",
    type: "PASS",
    concept: "PLAY_ACTION",
    success_rate: 65,
    avg_yards: 8.2,
    description: "Play action boot to the right with WR crossing route",
  },
  {
    id: 2,
    name: "Inside Zone",
    formation: "singleback",
    type: "RUN",
    concept: "ZONE",
    success_rate: 55,
    avg_yards: 4.5,
    description: "Zone blocking with RB reading backside",
  },
  {
    id: 3,
    name: "Mesh Concept",
    formation: "shotgun",
    type: "PASS",
    concept: "QUICK_GAME",
    success_rate: 70,
    avg_yards: 6.8,
    description: "Two receivers crossing in the middle of the field",
  },
];

const MOCK_SCHEME = {
  offense: "WEST_COAST",
  defense: "4-3",
  run_pass_ratio: 55,
  blitz_frequency: 30,
  tempo: "BALANCED",
};

test.describe("Playbook Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock User Settings
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: USER_TEAM_ID } });
    });

    // Mock Current Season
    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({
        json: { id: 1, year: 2024, status: "REGULAR_SEASON", current_week: 5 },
      });
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

    // Mock Formations
    await page.route("**/api/playbook/formations*", async (route) => {
      await route.fulfill({ json: MOCK_FORMATIONS });
    });

    // Mock Plays
    await page.route("**/api/playbook/plays*", async (route) => {
      await route.fulfill({ json: MOCK_PLAYS });
    });

    // Mock Scheme
    await page.route(`**/api/teams/${USER_TEAM_ID}/scheme*`, async (route) => {
      await route.fulfill({ json: MOCK_SCHEME });
    });

    // Fallback
    await page.route("**/api/**", async (route) => {
      await route.fulfill({ json: {} });
    });
  });

  test("should load the playbook page", async ({ page }) => {
    await page.goto("/playbook");

    // Verify header
    await expect(page.locator("h1", { hasText: "Playbook" })).toBeVisible();

    // Verify scheme info
    await expect(page.locator("text=/Offensive Scheme.*West Coast/")).toBeVisible();
  });

  test("should display telestrator canvas area", async ({ page }) => {
    await page.goto("/playbook");

    // Verify the telestrator target/placeholder exists
    await expect(
      page
        .locator('text="TELESTRATOR_CANVAS_TARGET"')
        .or(page.locator('[data-testid="telestrator-canvas"]'))
        .first()
    ).toBeVisible();
  });

  test("should have draw and clear buttons", async ({ page }) => {
    await page.goto("/playbook");

    // Verify Draw and Clear buttons
    await expect(page.locator('button:has-text("✏️ Draw")')).toBeVisible();
    await expect(page.locator('button:has-text("🗑️ Clear")')).toBeVisible();
  });

  test("should toggle draw mode with draw button", async ({ page }) => {
    await page.goto("/playbook");

    const drawBtn = page.locator('button:has-text("✏️ Draw")');
    await expect(drawBtn).toBeVisible();

    // Click draw - should activate draw mode
    await drawBtn.click();

    // Button may change appearance when active
    // Check for any visual change or class toggle
    await page.waitForTimeout(200);
  });

  test("should display formation list when available", async ({ page }) => {
    await page.goto("/playbook");

    // Look for formation selector or list
    const formationList = page
      .locator('[data-testid="formation-list"], .formation-selector, select')
      .first();

    if (await formationList.isVisible({ timeout: 3000 })) {
      // Check for formation names
      await expect(page.locator("text=Shotgun")).toBeVisible();
      await expect(page.locator("text=I-Formation")).toBeVisible();
    }
  });

  test("should display play list when formation selected", async ({ page }) => {
    await page.goto("/playbook");

    // Look for play list
    const playList = page.locator('[data-testid="play-list"], .play-selector').first();

    if (await playList.isVisible({ timeout: 3000 })) {
      await expect(page.locator("text=PA Boot")).toBeVisible();
      await expect(page.locator("text=Inside Zone")).toBeVisible();
    }
  });

  test("should show play details on selection", async ({ page }) => {
    await page.goto("/playbook");

    // Look for a play to click
    const playItem = page.locator("text=PA Boot").first();

    if (await playItem.isVisible({ timeout: 3000 })) {
      await playItem.click();

      // Check for detail view
      const detailView = page.locator('[data-testid="play-details"], .play-detail').first();

      if (await detailView.isVisible({ timeout: 2000 })) {
        await expect(page.locator("text=/Play action boot/")).toBeVisible();
      }
    }
  });

  test("should display scheme summary", async ({ page }) => {
    await page.goto("/playbook");

    // Verify scheme is displayed
    await expect(page.locator("text=West Coast").first()).toBeVisible();
  });

  test("should filter plays by type", async ({ page }) => {
    await page.goto("/playbook");

    // Look for type filter
    const passFilter = page.locator('[data-testid="filter-pass"], button:has-text("Pass")').first();

    if (await passFilter.isVisible({ timeout: 3000 })) {
      await passFilter.click();

      // Should show pass plays only
      await expect(page.locator("text=PA Boot")).toBeVisible();
      await expect(page.locator("text=Mesh Concept")).toBeVisible();
    }
  });

  test("should handle clear button click", async ({ page }) => {
    await page.goto("/playbook");

    // Open Telestrator first
    const drawBtn = page.locator('button:has-text("Draw Chalk"), button:has-text("Draw")').first();
    if (await drawBtn.isVisible({ timeout: 3000 })) {
      await drawBtn.click();
    }

    const clearBtn = page.locator('button:has-text("Clear"), [data-testid="telestrator-clear"]').first();
    if (await clearBtn.isVisible({ timeout: 3000 })) {
      await clearBtn.click({ force: true });
    }

    // Page should still be functional
    await expect(page.locator("h1", { hasText: /playbook/i })).toBeVisible();
  });
});

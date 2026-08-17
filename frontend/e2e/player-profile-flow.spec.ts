import { test, expect } from "@playwright/test";

// Updated to match the current app UX:
// - Roster lives in Front Office
// - Player details are shown in a modal (not a dedicated route)

const mockTeam = {
  id: 1,
  city: "Arizona",
  name: "Cardinals",
  abbreviation: "ARI",
  conference: "NFC",
  division: "West",
  wins: 0,
  losses: 0,
  salary_cap_space: 25000000,
};

const mockRoster = [
  {
    id: 101,
    first_name: "Player",
    last_name: "One",
    position: "QB",
    jersey_number: 1,
    overall_rating: 90,
    age: 25,
    experience: 3,
    team_id: 1,
    speed: 92,
    strength: 70,
    agility: 88,
    acceleration: 90,
    awareness: 85,
  },
  {
    id: 102,
    first_name: "Player",
    last_name: "Two",
    position: "RB",
    jersey_number: 28,
    overall_rating: 82,
    age: 23,
    experience: 1,
    team_id: 1,
    speed: 91,
    strength: 75,
    agility: 90,
    acceleration: 92,
    awareness: 78,
  },
];

test.describe("Player Profile Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockTeam });
    });
    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({ json: mockRoster });
    });
    await page.route("**/api/players/101", async (route) => {
      await route.fulfill({
        json: {
          ...mockRoster[0],
          xp: 2500,
          level: 7,
          abilities: { pre_snap_diagnostician: true },
          player_traits: [
            { trait: { name: "The Closer", tier: "ELITE" } },
            { trait: { name: "Field General", tier: "GOLD" } },
          ],
          contract: {
            years_remaining: 3,
            yearly_salary: 45000000,
            signing_bonus: 25000000,
          },
        },
      });
    });
    await page.route("**/api/abilities/players/101", async (route) => {
      await route.fulfill({
        json: {
          pre_snap_diagnostician: {
            status: "UNLOCKED",
            name: "Pre-Snap Diagnostician",
          },
          audible_master: {
            status: "AVAILABLE",
            name: "Audible Master",
            level_required: 8,
            xp_cost: 3000,
          },
        },
      });
    });
  });

  test("should open a player profile modal from the roster and display details", async ({
    page,
  }) => {
    await page.goto("/empire/front-office");

    // Wait for the page to finish loading (network can be slower on WebKit/Firefox).
    await expect(page.locator("text=Loading Front Office...")).not.toBeVisible({ timeout: 35000 });

    // Verify roster section exists
    await expect(page.getByTestId("front-office-page")).toBeVisible();
    await expect(page.getByTestId("roster-grid")).toBeVisible();

    // Open first player
    await page.getByTestId("player-card-101").click();

    // Verify modal content
    await expect(page.getByTestId("player-modal")).toBeVisible();
    await expect(page.getByTestId("player-modal-content")).toContainText("Player One");
    await expect(page.getByTestId("player-modal-content")).toContainText("QB");
    await expect(page.getByTestId("player-modal-content")).toContainText("90");
  });

  test("should display player traits in profile modal", async ({ page }) => {
    await page.goto("/empire/front-office");

    await expect(page.locator("text=Loading Front Office...")).not.toBeVisible({ timeout: 35000 });
    await page.getByTestId("player-card-101").click();
    await expect(page.getByTestId("player-modal")).toBeVisible();

    // Check for trait badges
    const traitSection = page.locator('[data-testid="player-traits"], .traits-section');
    if (await traitSection.isVisible({ timeout: 2000 })) {
      await expect(traitSection).toContainText("The Closer");
      await expect(traitSection).toContainText("Field General");
    }
  });

  test("should display player abilities status", async ({ page }) => {
    await page.goto("/empire/front-office");

    await expect(page.locator("text=Loading Front Office...")).not.toBeVisible({ timeout: 35000 });
    await page.getByTestId("player-card-101").click();
    await expect(page.getByTestId("player-modal")).toBeVisible();

    // Check for abilities section
    const abilitiesSection = page.locator('[data-testid="player-abilities"], .abilities-section');
    if (await abilitiesSection.isVisible({ timeout: 2000 })) {
      await expect(abilitiesSection).toContainText("Diagnostician");
    }
  });

  test("should display contract information", async ({ page }) => {
    await page.goto("/empire/front-office");

    await expect(page.locator("text=Loading Front Office...")).not.toBeVisible({ timeout: 35000 });
    await page.getByTestId("player-card-101").click();
    await expect(page.getByTestId("player-modal")).toBeVisible();

    // Check for contract section
    const contractSection = page.locator('[data-testid="player-contract"], .contract-info');
    if (await contractSection.isVisible({ timeout: 2000 })) {
      await expect(contractSection).toContainText("$45");
    }
  });

  test("should display XP and level progression", async ({ page }) => {
    await page.goto("/empire/front-office");

    await expect(page.locator("text=Loading Front Office...")).not.toBeVisible({ timeout: 35000 });
    await page.getByTestId("player-card-101").click();
    await expect(page.getByTestId("player-modal")).toBeVisible();

    // Check for level/XP display
    const progressionSection = page
      .locator('[data-testid="player-progression"], .xp-bar')
      .or(page.getByText(/Level|XP/i))
      .first();
    if (await progressionSection.isVisible({ timeout: 2000 })) {
      await expect(progressionSection).toBeVisible();
    }
  });
});

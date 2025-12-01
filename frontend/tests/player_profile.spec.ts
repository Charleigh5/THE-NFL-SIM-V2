import { test, expect } from "@playwright/test";

test.describe("Player Profile", () => {
  test.beforeEach(async ({ page }) => {
    // Mock Roster Response
    await page.route("**/api/teams/*/roster", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 999,
            first_name: "Super",
            last_name: "Star",
            position: "QB",
            overall_rating: 99,
            age: 25,
          },
        ],
      });
    });

    // Mock Player Detail Response
    await page.route("**/api/players/999", async (route) => {
      await route.fulfill({
        json: {
          id: 999,
          first_name: "Super",
          last_name: "Star",
          position: "QB",
          height: 75,
          weight: 220,
          age: 25,
          experience: 3,
          college: "Football U",
          overall_rating: 99,
          potential_rating: 99,
          attributes: {
            throw_power: 95,
            accuracy: 90,
          },
        },
      });
    });

    // Mock Teams (needed for Front Office nav usually)
    await page.route("**/api/teams", async (route) => {
      await route.fulfill({
        json: [{ id: 1, name: "Team 1", abbreviation: "T1" }],
      });
    });
  });

  test("should navigate to player details from roster", async ({ page }) => {
    // Navigate to Front Office / Roster
    await page.goto("/front-office");

    // Locate the player in the list
    const playerLink = page.getByText("Super Star");
    await expect(playerLink).toBeVisible();

    // Click the player
    await playerLink.click();

    // Check URL
    await expect(page).toHaveURL(/\/players\/999/);

    // Check Profile content
    await expect(page.getByRole("heading", { name: "Super Star" })).toBeVisible();
    await expect(page.getByText("QB")).toBeVisible();
    await expect(page.getByText("Overall: 99")).toBeVisible();
    // Check attributes
    await expect(page.getByText("Throw Power")).toBeVisible();
  });
});

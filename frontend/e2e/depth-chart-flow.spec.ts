import { test, expect } from "@playwright/test";
const mockRoster = [
  {
    id: 1,
    first_name: "Kyler",
    last_name: "Murray",
    position: "QB",
    overall_rating: 85,
    age: 26,
    jersey_number: 1,
    speed: 90,
    strength: 70,
    depth_chart_rank: 1,
    experience: 5,
  },
  {
    id: 2,
    first_name: "David",
    last_name: "Blough",
    position: "QB",
    overall_rating: 60,
    age: 28,
    jersey_number: 9,
    speed: 70,
    strength: 60,
    depth_chart_rank: 2,
    experience: 3,
  },
  {
    id: 3,
    first_name: "James",
    last_name: "Conner",
    position: "RB",
    overall_rating: 82,
    age: 28,
    jersey_number: 6,
    speed: 88,
    strength: 85,
    depth_chart_rank: 1,
    experience: 7,
  },
  {
    id: 4,
    first_name: "Keaontay",
    last_name: "Ingram",
    position: "RB",
    overall_rating: 70,
    age: 24,
    jersey_number: 30,
    speed: 85,
    strength: 75,
    depth_chart_rank: 2,
    experience: 2,
  },
  {
    id: 5,
    first_name: "Marquise",
    last_name: "Brown",
    position: "WR",
    overall_rating: 84,
    age: 27,
    jersey_number: 2,
    speed: 92,
    strength: 65,
    depth_chart_rank: 1,
    experience: 5,
  },
];

test.describe("Depth Chart Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
    });

    await page.route("**/api/teams?page=1&page_size=100", async (route) => {
      await route.fulfill({
        json: {
          items: [
            {
              id: 1,
              city: "Arizona",
              name: "Cardinals",
              abbreviation: "ARI",
              conference: "NFC",
              division: "West",
              wins: 0,
              losses: 0,
              salary_cap_space: 0,
            },
          ],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route("**/api/teams/1/chemistry", async (route) => {
      await route.fulfill({
        json: {
          chemistry_level: 2,
          consecutive_games: 3,
          status: "BUILDING",
          bonuses: { pass_block: 1, run_block: 1, awareness: 1 },
          advanced_effects: {
            stunt_pickup_bonus: 0.05,
            penalty_reduction: 0.02,
            communication_boost: 0.03,
            blitz_pickup_improvement: 0.04,
          },
        },
      });
    });

    // Mock team roster fetch
    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({ json: mockRoster });
    });

    // Mock depth chart update
    await page.route("**/api/teams/1/depth-chart", async (route) => {
      expect(route.request().method()).toBe("PUT");
      const postData = route.request().postDataJSON();
      expect(postData).toHaveProperty("position");
      expect(postData).toHaveProperty("player_ids");
      await route.fulfill({ status: 200, json: { message: "Depth chart updated" } });
    });
  });

  test("should load depth chart and display QB players", async ({ page }) => {
    await page.goto("/depth-chart");

    // Verify header
    await expect(page.locator("h1", { hasText: /depth chart editor/i })).toBeVisible();

    // Verify QB position is selected
    await expect(page.locator("button", { hasText: "QB" }).first()).toHaveClass(/bg-cyan/);
    await expect(page.locator("h2", { hasText: /QB Depth Chart/i })).toBeVisible();

    // Verify QB players are displayed in order
    const qbPlayers = page.locator(".Reorder_Group > div");
    await expect(qbPlayers).toHaveCount(2);
    await expect(qbPlayers.nth(0)).toContainText("Kyler Murray");
    await expect(qbPlayers.nth(1)).toContainText("David Blough");
  });

  test("should switch position and display RB players", async ({ page }) => {
    await page.goto("/depth-chart");

    // Click RB position button
    await page.locator("button", { hasText: "RB" }).first().click();

    // Verify RB position is selected
    await expect(page.locator("button", { hasText: "RB" }).first()).toHaveClass(/bg-cyan/);

    // Verify RB players are displayed in order
    const rbPlayers = page.locator(".Reorder_Group > div");
    await expect(rbPlayers).toHaveCount(2);
    await expect(rbPlayers.nth(0)).toContainText("James Conner");
    await expect(rbPlayers.nth(1)).toContainText("Keaontay Ingram");
  });

  test("preserves an unsaved position draft when switching away and back", async ({ page }) => {
    await page.goto("/depth-chart");

    await page.getByRole("button", { name: "Demote Kyler Murray" }).click();
    await expect(page.getByTestId("depth-player-2")).toHaveAttribute("data-rank", "1");
    await expect(page.getByText("Unsaved order")).toBeVisible();

    await page.getByTestId("position-tab-RB").click();
    await page.getByTestId("position-tab-QB").click();

    await expect(page.getByTestId("depth-player-2")).toHaveAttribute("data-rank", "1");
    await expect(page.getByText("Unsaved order")).toBeVisible();
  });

  test("honors reduced motion for the spatial scene shell", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/depth-chart");

    await expect(page.getByTestId("depth-chart-scene")).toHaveAttribute("data-motion", "reduced");
  });

  test("captures the spatial proof slice as a Playwright artifact", async ({ page }, testInfo) => {
    await page.goto("/depth-chart");
    await expect(page.getByTestId("depth-chart-scene")).toHaveAttribute("data-scene-id", "SCN-005");
    await expect(page.getByRole("heading", { name: /depth chart editor/i })).toBeVisible();

    await page.screenshot({
      path: testInfo.outputPath("depth-chart-war-room.png"),
      fullPage: true,
    });
  });

  test("should reorder players and save changes", async ({ page }) => {
    await page.goto("/depth-chart");

    // Drag only from the dedicated handle so action buttons cannot accidentally reorder.
    const kylerHandle = page.getByTestId("depth-drag-handle-1");
    const david = page.getByTestId("depth-player-2");

    await kylerHandle.hover();
    await page.mouse.down();
    await david.hover();
    await page.mouse.up();

    // Verify UI reflects new order
    const qbPlayersAfterDrag = page.locator(".Reorder_Group > div");
    await expect(qbPlayersAfterDrag.nth(0)).toContainText("David Blough");
    await expect(qbPlayersAfterDrag.nth(1)).toContainText("Kyler Murray");

    // Click save button
    const saveRequestPromise = page.waitForRequest(
      (request) => request.url().includes("/api/teams/1/depth-chart") && request.method() === "PUT"
    );
    await page.locator("button", { hasText: "Save Changes" }).click();

    // Wait for the save request to complete
    const saveRequest = await saveRequestPromise;
    const postData = saveRequest.postDataJSON();
    expect(postData.position).toBe("QB");
    expect(postData.player_ids).toEqual([2, 1]); // Expect new order

    // Save confirmation is an accessible in-page status, not a browser dialog.
    await expect(page.getByRole("status")).toContainText(/saved successfully/i);
  });
});

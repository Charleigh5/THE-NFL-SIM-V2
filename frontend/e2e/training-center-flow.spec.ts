import { test, expect } from "@playwright/test";
import { setupTrainingMocks, mockDrills } from "./fixtures/test-data";

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    await setupTrainingMocks(page);

    // Mock training execution response
    await page.route("**/api/training/execute", async (route) => {
      await route.fulfill({
        json: {
          success: true,
          xp_gained: 150,
          drill_name: mockDrills[0].name,
          target_stat: mockDrills[0].target_stat,
          fatigue_added: 5,
          weekly_load: 45,
          injury_occurred: false,
        },
      });
    });
  });

  test("should load training center page", async ({ page }) => {
    await page.goto("/training");

    // Check for Training Center heading
    await expect(page.getByTestId("training-center-page")).toBeVisible();
    await expect(page.getByRole("heading", { name: /training center/i })).toBeVisible();
  });

  test("should display coaching style selector", async ({ page }) => {
    await page.goto("/training");
    await expect(page.getByTestId("training-center-page")).toBeVisible();

    // The CoachingStyleDial should be visible
    await expect(page.getByTestId("coaching-style-dial")).toBeVisible();
    await expect(page.getByText("Smart")).toBeVisible();
  });

  test("should filter and select a drill", async ({ page }) => {
    await page.goto("/training");
    await expect(page.getByTestId("training-center-page")).toBeVisible();

    // Wait for drills to be visible
    await expect(page.getByTestId("drill-selector")).toBeVisible();

    // Test search functionality
    const searchInput = page.getByTestId("drill-search-input");
    // Search is hidden by default behind the filter toggle
    await page.getByTestId("filter-toggle-button").click();
    await expect(searchInput).toBeVisible();

    await searchInput.fill(mockDrills[0].name);

    // Find and click the drill card
    const drillCard = page.getByTestId(`drill-card-${mockDrills[0].name}`);
    await drillCard.click();

    // Action panel should appear with details
    await expect(page.getByTestId("initiate-training-button")).toBeVisible();
    await expect(page.getByTestId("cancel-training-button")).toBeVisible();

    // Verify drill details in action shade
    await expect(page.getByText(mockDrills[0].name)).toHaveCount(2); // One in grid, one in shade
  });

  test("should complete a training sequence and closing result", async ({ page }) => {
    await page.goto("/training");
    await expect(page.getByTestId("training-center-page")).toBeVisible();

    // Select first drill
    await page.getByTestId(`drill-card-${mockDrills[0].name}`).click();

    // Click Initiate and wait for response
    const [response] = await Promise.all([
      page.waitForResponse("**/api/training/execute"),
      page.getByTestId("initiate-training-button").click(),
    ]);

    expect(response.status()).toBe(200);

    // Verify Result Modal appears
    await expect(page.getByTestId("training-result-container")).toBeVisible();
    await expect(page.getByText("Training Complete")).toBeVisible();
    await expect(page.getByText("+150 XP")).toBeVisible();

    // Close result
    await page.getByTestId("training-result-continue-button").click();
    await expect(page.getByTestId("training-result-container")).not.toBeVisible();
  });
});

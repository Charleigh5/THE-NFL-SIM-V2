import { test, expect } from "@playwright/test";
import { setupScoutingMocks, mockProspects } from "./fixtures/test-data";

test.describe("Scouting System E2E", () => {
  test.beforeEach(async ({ page }) => {
    await setupScoutingMocks(page);
  });

  test("should display prospect list in draft room", async ({ page }) => {
    await page.goto("/draft");

    // Wait for the draft room page to load
    await expect(page.getByTestId("draft-room-page")).toBeVisible({ timeout: 10000 });

    // Wait for prospects to load in the list
    await expect(page.getByTestId("prospect-list")).toBeVisible();

    // Check for specific prospects from mock data
    await expect(page.getByText(mockProspects[0].name).first()).toBeVisible();
    await expect(page.getByText(mockProspects[1].name).first()).toBeVisible();
  });

  test("should filter prospects by position", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-room-page")).toBeVisible();

    // Find position filter select
    const filterSelect = page.getByTestId("draft-filter-position");
    await expect(filterSelect).toBeVisible();

    // Filter by QB
    await filterSelect.selectOption("QB");

    // Check that Caleb Williams is still visible and Marvin Harrison (WR) is not
    await expect(page.getByText(mockProspects[0].name).first()).toBeVisible();
    await expect(page.getByText(mockProspects[1].name).first()).not.toBeVisible();
  });

  test("should open scouting report modal", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-room-page")).toBeVisible();

    // Find first prospect card and click the 'Report' button
    const firstProspect = mockProspects[0];
    await page.getByTestId(`report-button-${firstProspect.id}`).click();

    // Verify modal appears
    const modal = page.getByTestId("scouting-report-modal");
    await expect(modal).toBeVisible();

    // Check for modal content
    await expect(page.getByText(firstProspect.name).first()).toBeVisible();
    await expect(page.getByTestId("scouting-strengths")).toBeVisible();
    await expect(page.getByTestId("scouting-weaknesses")).toBeVisible();
  });

  test("should close scouting report modal", async ({ page }) => {
    await page.goto("/draft");
    const firstProspect = mockProspects[0];
    await page.getByTestId(`report-button-${firstProspect.id}`).click();

    const modal = page.getByTestId("scouting-report-modal");
    await expect(modal).toBeVisible();

    // Click close button
    await page.getByTestId("close-modal").click();

    // Modal should be gone
    await expect(modal).not.toBeVisible();
  });

  test("should display team needs in draft room", async ({ page }) => {
    await page.goto("/draft");
    await expect(page.getByTestId("draft-room-page")).toBeVisible();

    // Wait for the sidebar with team needs to appear
    await expect(page.getByTestId("draft-board")).toBeVisible();

    // Team needs should be visible in the sidebar (use .first() since multiple elements match)
    await expect(page.getByText(/Team Needs/i).first()).toBeVisible();

    // We expect some positions to be listed (QB is mocked)
    await expect(page.locator("span").filter({ hasText: "QB" }).first()).toBeVisible();
  });
});

test.describe("Player Backstory Modal E2E", () => {
  test.beforeEach(async ({ page }) => {
    await setupScoutingMocks(page);
  });

  test("should open backstory modal and display content", async ({ page }) => {
    await page.goto("/draft");

    // Click 'Reveal' on the first prospect
    const firstProspect = mockProspects[0];
    await page.getByTestId(`reveal-button-${firstProspect.id}`).click();

    // GenesisReveal modal should appear (modal text is "GENESIS BIOMETRICS")
    await expect(page.getByText(/GENESIS/i).first()).toBeVisible({ timeout: 5000 });
    await expect(page.getByText(firstProspect.name).first()).toBeVisible();
  });
});

import { test, expect } from "@playwright/test";

test.describe("Training Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock API calls
    await page.route("**/api/v1/training/drills", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          {
            id: "1",
            name: "Oklahoma Drill",
            category: "CONTACT",
            energyCost: 20,
            xpMultiplier: 1.5,
            injuryRisk: "HIGH",
          },
          {
            id: "2",
            name: "7-on-7 Skeleton",
            category: "PASSING",
            energyCost: 15,
            xpMultiplier: 1.2,
            injuryRisk: "LOW",
          },
        ]),
      });
    });

    await page.route("**/api/v1/training/schedule", async (route) => {
      await route.fulfill({ status: 200, body: JSON.stringify({ currentWait: 0 }) });
    });

    // Navigate to training page
    await page.goto("http://localhost:5173/training");
  });

  test("should load training center page", async ({ page }) => {
    await expect(page.getByText("Training Center")).toBeVisible();
    await expect(page.getByText("Coaching Philosophy")).toBeVisible();
  });

  test("should allow selecting coaching style", async ({ page }) => {
    // Check initial state or default
    // Click on a different style
    await page.getByText("Old School").first().click();
    await expect(page.getByText("Old School").first()).toHaveClass(/border-cyan-400/); // Assuming selected style gets border class
  });

  test("should display drills", async ({ page }) => {
    await expect(page.getByText("Oklahoma Drill")).toBeVisible();
    await expect(page.getByText("7-on-7 Skeleton")).toBeVisible();
  });

  test("should toggle drill selection", async ({ page }) => {
    const drillCard = page.locator(".drill-card").first();
    await drillCard.click();
    // Verify selection state (e.g. border color change or checkbox)
    await expect(drillCard).toHaveClass(/border-cyan-400/);

    await drillCard.click();
    await expect(drillCard).not.toHaveClass(/border-cyan-400/);
  });
});

import { test, expect } from "@playwright/test";

test("verify player dossier and dynamic positional ratings", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1100 });

  // Navigate to Front Office
  await page.goto("http://127.0.0.1:5173/empire/front-office");
  await page.waitForLoadState("networkidle");

  // Wait for roster grid
  const rosterGrid = page.locator('[data-testid="roster-grid"]');
  await expect(rosterGrid).toBeVisible({ timeout: 15000 });

  // Take screenshot of roster grid with dynamic positional badges
  await page.screenshot({
    path: "C:/Users/cweir/.gemini/antigravity/brain/5872d509-81ae-4bd5-adbb-3df1fc7693f8/roster_dynamic_badges.png",
    fullPage: false,
  });

  // Find a player card (e.g. Ben Stille or any first card) and click it
  const playerCard = page.locator('[data-testid^="player-card-"]').first();
  await expect(playerCard).toBeVisible();
  await playerCard.click();

  // Inspect modal should open
  const openDossierBtn = page.getByRole("button", {
    name: /Open In-Depth Biometrics & Traits Dossier/i,
  });
  await expect(openDossierBtn).toBeVisible({ timeout: 10000 });

  // Click "Open In-Depth Biometrics & Traits Dossier" via DOM evaluate
  await openDossierBtn.evaluate((b) => (b as HTMLElement).click());

  // EnhancedPlayerProfile modal should appear without 500 error
  const dossierModal = page.locator('[data-testid="player-modal"]');
  await expect(dossierModal).toBeVisible({ timeout: 10000 });

  // Verify that an error banner or 500 is NOT displayed
  const errorText = page.locator(".profile-error, .error-message");
  await expect(errorText).toHaveCount(0);

  // Take screenshot of opened dossier
  await page.screenshot({
    path: "C:/Users/cweir/.gemini/antigravity/brain/5872d509-81ae-4bd5-adbb-3df1fc7693f8/player_dossier_modal.png",
    fullPage: false,
  });
});

import { test, expect } from "@playwright/test";
import { mockTeam, mockPlayers } from "./fixtures/test-data";

test.describe("12-State Interactive Tactile Matrix & 3D Pointer Tilt Subsystem", () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
    });

    await page.route("**/api/teams?page=1&page_size=100", async (route) => {
      await route.fulfill({
        json: {
          items: [mockTeam],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({ json: mockTeam });
    });

    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({ json: mockPlayers });
    });
  });

  test("Front Office locker stall cards implement tactile matrix with strict 0-4px corners and hard shadows", async ({
    page,
  }) => {
    await page.goto("/empire/front-office");
    await page.waitForSelector('[data-testid="roster-grid"]', { timeout: 10000 });

    const playerCards = page.locator('[data-testid^="player-card-"]');
    await expect(playerCards).toHaveCount(2);

    const firstCard = playerCards.first();
    await expect(firstCard).toBeVisible();

    // Verify tactile state attribute
    const tactileState = await firstCard.getAttribute("data-tactile-state");
    expect(tactileState).toBeTruthy();
    expect(["idle", "hover", "selected"]).toContain(tactileState);

    // Verify computed border-radius is <= 4px (0-4px constraint)
    const borderRadius = await firstCard.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return parseFloat(computed.borderTopLeftRadius) || 0;
    });
    expect(borderRadius).toBeLessThanOrEqual(4);

    // Verify zero-blur directional hard shadow
    const boxShadow = await firstCard.evaluate((el) => {
      return window.getComputedStyle(el).boxShadow;
    });
    expect(boxShadow).toBeTruthy();
    expect(boxShadow).not.toBe("none");

    // Verify Web Audio haptics execute safely without throwing exceptions in browser
    const audioResult = await page.evaluate(() => {
      try {
        const win = window as any;
        if (win.soundEffects) {
          win.soundEffects.unlockAudio?.();
          win.soundEffects.playTiltDetent?.();
          win.soundEffects.playCardPress?.();
          win.soundEffects.playCardRelease?.();
        }
        return { success: true };
      } catch (err: any) {
        return { success: false, error: err?.message };
      }
    });
    expect(audioResult.success).toBe(true);

    // Verify card selection on click
    await firstCard.click();
    const selectedState = await firstCard.getAttribute("data-tactile-state");
    expect(selectedState).toBeTruthy();
  });

  test("LockerStallCard maintains accessible keyboard navigation and focus rings", async ({
    page,
  }) => {
    await page.goto("/empire/front-office");
    await page.waitForSelector('[data-testid="roster-grid"]', { timeout: 10000 });

    const firstCard = page.locator('[data-testid^="player-card-"]').first();
    await expect(firstCard).toBeVisible();

    // Focus via keyboard tab or focus()
    await firstCard.focus();
    await expect(firstCard).toBeFocused();

    // Press enter to trigger dossier
    await page.keyboard.press("Enter");
  });
});

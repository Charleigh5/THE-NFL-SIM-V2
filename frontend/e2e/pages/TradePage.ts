import { type Page, type Locator, expect } from "@playwright/test";

export class TradePage {
  readonly page: Page;
  readonly partnerSelect: Locator;
  readonly negotiateTab: Locator;
  readonly offersTab: Locator;
  readonly tradeBlockTab: Locator;
  readonly evaluateBtn: Locator;
  readonly submitOfferBtn: Locator;
  readonly clearTradeBtn: Locator;

  constructor(page: Page) {
    this.page = page;
    this.partnerSelect = page.getByRole("combobox").first(); // Adjust selector if needed
    this.negotiateTab = page.getByRole("tab", { name: "Negotiate" });
    this.offersTab = page.getByRole("tab", { name: "Offers" });
    this.tradeBlockTab = page.getByRole("tab", { name: "Trade Block" });
    this.evaluateBtn = page.getByRole("button", { name: "Get GM Response" });
    this.submitOfferBtn = page.getByRole("button", { name: "Submit Formal Offer" });
    this.clearTradeBtn = page.getByRole("button", { name: "Clear Trade" });
  }

  async goto() {
    await this.page.goto("/empire/trades");
    try {
      await this.negotiateTab.waitFor({ state: "visible", timeout: 10000 });
    } catch {
      // Retry navigation if first load fails (dev server quirks)
      console.log("Retrying navigation to Trade Center...");
      await this.page.goto("/empire/trades");
      await this.negotiateTab.waitFor({ state: "visible" });
    }
  }

  async selectPartner(teamId: string) {
    // Wait for the select to be populated (implied by waiting for page load, but good to be safe)
    await this.partnerSelect.waitFor();
    await this.partnerSelect.selectOption(teamId);
    // Wait for partner players to load
    await this.page
      .locator(".partner-assets .draggable-player-card")
      .first()
      .waitFor({ timeout: 5000 });
  }

  async dragPlayerToOffer(playerId: number) {
    const source = this.page.locator(`[data-testid="draggable-user-player-${playerId}"]`);
    const target = this.page.locator('[data-testid="offered-zone"]');

    // Manual drag for dnd-kit compatibility
    await source.hover();
    await this.page.mouse.down();
    // Move enough to trigger drag start (activationConstraint is 8px)
    const box = await source.boundingBox();
    if (box) {
      await this.page.mouse.move(box.x + box.width / 2 + 20, box.y + box.height / 2 + 20, {
        steps: 5,
      });
    }
    await target.hover();
    await this.page.mouse.up();
    // Wait for animation/state update
    await expect(source).not.toBeVisible(); // Or check if it appeared in target
  }

  async dragPlayerToRequest(playerId: number) {
    const source = this.page.locator(`[data-testid="draggable-partner-player-${playerId}"]`);
    const target = this.page.locator('[data-testid="requested-zone"]');

    await source.hover();
    await this.page.mouse.down();
    const box = await source.boundingBox();
    if (box) {
      await this.page.mouse.move(box.x + box.width / 2 + 20, box.y + box.height / 2 + 20, {
        steps: 5,
      });
    }
    await target.hover();
    await this.page.mouse.up();
  }

  async submitFormalOffer() {
    await this.submitOfferBtn.click();
  }

  async openOffersTab() {
    await this.offersTab.click();
    await this.page.locator(".pending-offers").waitFor();
  }

  async acceptOffer(offerId: number) {
    await this.page
      .locator(`[data-testid="offer-${offerId}"]`)
      .getByRole("button", { name: "Accept" })
      .click();
  }

  async rejectOffer(offerId: number) {
    await this.page
      .locator(`[data-testid="offer-${offerId}"]`)
      .getByRole("button", { name: "Reject" })
      .click();
  }

  async clickCounterOffer(offerId: number) {
    await this.page
      .locator(`[data-testid="offer-${offerId}"]`)
      .getByRole("button", { name: "Counter" })
      .click();
    // Should redirect to negotiate tab
    await this.negotiateTab.waitFor();
  }
}

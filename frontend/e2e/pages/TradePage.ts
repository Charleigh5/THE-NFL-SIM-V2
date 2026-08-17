import { type Page, type Locator } from "@playwright/test";

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
    this.partnerSelect = page.getByTestId("trade-partner-select");
    this.negotiateTab = page.getByTestId("tab-negotiate");
    this.offersTab = page.getByTestId("tab-offers");
    this.tradeBlockTab = page.getByTestId("tab-trade-block");
    this.evaluateBtn = page.getByTestId("evaluate-trade-btn");
    this.submitOfferBtn = page.getByRole("button", { name: "Submit Formal Offer" });
    this.clearTradeBtn = page.getByRole("button", { name: "Clear Trade" });
  }

  async goto() {
    await this.page.goto("/empire/trade-center");
    try {
      await this.negotiateTab.waitFor({ state: "visible", timeout: 10000 });
    } catch {
      // Retry navigation if first load fails (dev server quirks)
      console.log("Retrying navigation to Trade Center...");
      await this.page.goto("/empire/trade-center");
      await this.negotiateTab.waitFor({ state: "visible" });
    }
  }

  async selectPartner(teamId: string) {
    // Wait for the select to be populated (implied by waiting for page load, but good to be safe)
    await this.partnerSelect.waitFor();
    await this.partnerSelect.selectOption(teamId);
    // Wait for partner players to load (new TradeNegotiator markup)
    await this.page.locator('[data-testid^="draggable-partner-player-"]').first().waitFor({
      timeout: 5000,
    });
  }

  async dragPlayerToOffer(playerId: number) {
    const source = this.page.locator(`[data-testid="draggable-user-player-${playerId}"]`);
    await source.click();
    await this.page.waitForTimeout(100);
  }

  async dragPlayerToRequest(playerId: number) {
    const source = this.page.locator(`[data-testid="draggable-partner-player-${playerId}"]`);
    await source.click();
    await this.page.waitForTimeout(100);
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

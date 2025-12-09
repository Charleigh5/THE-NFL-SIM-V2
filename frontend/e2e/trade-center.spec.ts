import { test, expect } from "@playwright/test";

/**
 * E2E Tests for Trade Center
 * Tests the complete trade negotiation flow including:
 * - Team selection
 * - Player selection for trade
 * - Trade evaluation via GMAgent
 * - GM response display
 */

test.describe("Trade Center Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock teams list
    await page.route("**/api/teams?page=1&page_size=100", async (route) => {
      await route.fulfill({
        json: {
          items: [
            { id: 1, city: "Arizona", name: "Cardinals", abbreviation: "ARI", wins: 5, losses: 3 },
            { id: 2, city: "Kansas City", name: "Chiefs", abbreviation: "KC", wins: 7, losses: 1 },
            { id: 3, city: "Buffalo", name: "Bills", abbreviation: "BUF", wins: 6, losses: 2 },
          ],
        },
      });
    });

    // Mock user team roster (Team 1 - Cardinals)
    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 101,
            first_name: "Kyler",
            last_name: "Murray",
            position: "QB",
            overall_rating: 85,
            age: 26,
          },
          {
            id: 102,
            first_name: "James",
            last_name: "Conner",
            position: "RB",
            overall_rating: 78,
            age: 28,
          },
        ],
      });
    });

    // Mock partner team roster (Team 2 - Chiefs)
    await page.route("**/api/teams/2/roster", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 201,
            first_name: "Patrick",
            last_name: "Mahomes",
            position: "QB",
            overall_rating: 99,
            age: 28,
          },
          {
            id: 202,
            first_name: "Travis",
            last_name: "Kelce",
            position: "TE",
            overall_rating: 95,
            age: 34,
          },
        ],
      });
    });

    // Mock trade evaluation endpoint
    await page.route("**/api/trades/evaluate", async (route) => {
      const request = route.request();
      const postData = request.postDataJSON();

      // Simple mock logic: reject if requesting Mahomes
      const decision = postData.requested_player_ids?.includes(201) ? "REJECT" : "ACCEPT";
      const reasoning =
        decision === "REJECT"
          ? "We're not trading our franchise QB. Mahomes is untouchable."
          : "This trade looks fair. We'll accept this proposal.";

      await route.fulfill({
        json: {
          decision,
          score: decision === "ACCEPT" ? 12.5 : -25.0,
          reasoning,
          gm_philosophy: "WIN_NOW",
        },
      });
    });
  });

  test("should load Trade Center and display team selector", async ({ page }) => {
    await page.goto("/empire/trades");

    // Wait for Trade Center to load
    await page.waitForSelector('[data-testid="trade-center"]', { timeout: 5000 });

    // Verify header
    await expect(page.locator("h2")).toContainText("Trade Center");

    // Verify team selector exists
    const teamSelector = page.locator('[data-testid="trade-partner-select"]');
    await expect(teamSelector).toBeVisible();
  });

  test("should select trade partner and load their roster", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Select Chiefs as trade partner
    const teamSelector = page.locator('[data-testid="trade-partner-select"]');
    await teamSelector.selectOption("2"); // Chiefs team ID

    // Wait for partner roster to load
    await page.waitForSelector('[data-testid="partner-available-players"]', { timeout: 3000 });

    // Verify partner players are displayed
    const partnerPlayers = page.locator('[data-testid^="partner-player-"]');
    await expect(partnerPlayers).toHaveCount(2);

    // Verify Mahomes is shown
    await expect(page.locator('[data-testid="partner-player-201"]')).toContainText("Mahomes");
  });

  test("should add players to trade proposal", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Select trade partner
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");
    await page.waitForSelector('[data-testid="partner-available-players"]');

    // Add user's player to offer (Kyler Murray)
    await page.locator('[data-testid="user-player-101"]').click();

    // Verify player appears in offered zone
    await expect(page.locator('[data-testid="offered-player-101"]')).toBeVisible();

    // Add partner's player to request (Travis Kelce)
    await page.locator('[data-testid="partner-player-202"]').click();

    // Verify player appears in requested zone
    await expect(page.locator('[data-testid="requested-player-202"]')).toBeVisible();
  });

  test("should evaluate trade and display GM response - ACCEPT", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Setup trade: Murray for Kelce (should be accepted)
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");
    await page.waitForSelector('[data-testid="partner-available-players"]');

    await page.locator('[data-testid="user-player-101"]').click(); // Offer Murray
    await page.locator('[data-testid="partner-player-202"]').click(); // Request Kelce

    // Click evaluate button
    const evaluateBtn = page.locator('[data-testid="evaluate-trade-btn"]');
    await expect(evaluateBtn).toBeEnabled();
    await evaluateBtn.click();

    // Wait for GM response
    await page.waitForSelector('[data-testid="gm-response"]', { timeout: 5000 });

    // Verify response shows ACCEPT
    const gmResponse = page.locator('[data-testid="gm-response"]');
    await expect(gmResponse).toContainText("ACCEPT");
    await expect(gmResponse).toContainText("This trade looks fair");

    // Verify Execute Trade button appears
    await expect(page.locator('[data-testid="execute-trade-btn"]')).toBeVisible();
  });

  test("should evaluate trade and display GM response - REJECT", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Setup trade: Conner for Mahomes (should be rejected)
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");
    await page.waitForSelector('[data-testid="partner-available-players"]');

    await page.locator('[data-testid="user-player-102"]').click(); // Offer Conner
    await page.locator('[data-testid="partner-player-201"]').click(); // Request Mahomes

    // Click evaluate button
    await page.locator('[data-testid="evaluate-trade-btn"]').click();

    // Wait for GM response
    await page.waitForSelector('[data-testid="gm-response"]', { timeout: 5000 });

    // Verify response shows REJECT
    const gmResponse = page.locator('[data-testid="gm-response"]');
    await expect(gmResponse).toContainText("REJECT");
    await expect(gmResponse).toContainText("franchise QB");

    // Verify Execute Trade button does NOT appear
    await expect(page.locator('[data-testid="execute-trade-btn"]')).not.toBeVisible();
  });

  test("should clear trade proposal", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Setup trade
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");
    await page.waitForSelector('[data-testid="partner-available-players"]');

    await page.locator('[data-testid="user-player-101"]').click();
    await page.locator('[data-testid="partner-player-202"]').click();

    // Verify players are in trade zones
    await expect(page.locator('[data-testid="offered-player-101"]')).toBeVisible();
    await expect(page.locator('[data-testid="requested-player-202"]')).toBeVisible();

    // Click clear button
    await page.locator('button:has-text("Clear Trade")').click();

    // Verify trade zones are empty
    await expect(page.locator('[data-testid="offered-player-101"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="requested-player-202"]')).not.toBeVisible();
  });

  test("should filter players by position", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Click QB filter
    await page.locator('button:has-text("QB")').first().click();

    // Verify only QB is shown (Murray)
    const visiblePlayers = page.locator('[data-testid^="user-player-"]');
    await expect(visiblePlayers).toHaveCount(1);
    await expect(page.locator('[data-testid="user-player-101"]')).toBeVisible();
  });

  test("should search for players", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Type in search box
    const searchInput = page.locator('[data-testid="user-player-search"]');
    await searchInput.fill("Murray");

    // Verify only Murray is shown
    await expect(page.locator('[data-testid="user-player-101"]')).toBeVisible();
    await expect(page.locator('[data-testid="user-player-102"]')).not.toBeVisible();
  });

  test("should disable evaluate button when trade is empty", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Select partner but don't add any players
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");

    // Verify evaluate button is disabled
    const evaluateBtn = page.locator('[data-testid="evaluate-trade-btn"]');
    await expect(evaluateBtn).toBeDisabled();
  });

  test("should show loading state during evaluation", async ({ page }) => {
    await page.goto("/empire/trades");

    await page.waitForSelector('[data-testid="trade-center"]');

    // Setup trade
    await page.locator('[data-testid="trade-partner-select"]').selectOption("2");
    await page.waitForSelector('[data-testid="partner-available-players"]');

    await page.locator('[data-testid="user-player-101"]').click();
    await page.locator('[data-testid="partner-player-202"]').click();

    // Click evaluate and check for loading text
    await page.locator('[data-testid="evaluate-trade-btn"]').click();

    // Button should show "Analyzing..." briefly
    await expect(page.locator('[data-testid="evaluate-trade-btn"]')).toContainText("Analyzing");
  });
});

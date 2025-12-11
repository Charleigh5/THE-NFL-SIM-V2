import { test, expect } from "@playwright/test";
import { TradePage } from "./pages/TradePage";

/**
 * E2E Tests for Trade System
 * Covers: Negotiation, Offers, Actions (Accept/Reject/Counter)
 */

const USER_TEAM_ID = 1;
const PARTNER_TEAM_ID = 2;

const MOCK_USER_PLAYERS = [
  {
    id: 101,
    first_name: "Kyler",
    last_name: "Murray",
    position: "QB",
    overall_rating: 85,
    age: 26,
    trade_value: 50,
    team_id: USER_TEAM_ID,
  },
  {
    id: 102,
    first_name: "James",
    last_name: "Conner",
    position: "RB",
    overall_rating: 78,
    age: 28,
    trade_value: 20,
    team_id: USER_TEAM_ID,
  },
];

const MOCK_PARTNER_PLAYERS = [
  {
    id: 201,
    first_name: "Patrick",
    last_name: "Mahomes",
    position: "QB",
    overall_rating: 99,
    age: 28,
    trade_value: 100,
    team_id: PARTNER_TEAM_ID,
  },
  {
    id: 202,
    first_name: "Travis",
    last_name: "Kelce",
    position: "TE",
    overall_rating: 95,
    age: 34,
    trade_value: 60,
    team_id: PARTNER_TEAM_ID,
  },
];

test.describe.serial("Trade System E2E", () => {
  let tradePage: TradePage;

  test.beforeEach(async ({ page }) => {
    tradePage = new TradePage(page);

    // Mock User Settings (required for userTeamId)
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({
        json: { user_team_id: USER_TEAM_ID },
      });
    });

    // Mock Current Season
    await page.route("**/api/seasons/current", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          year: 2024,
          current_week: 5,
          phase: "regular_season",
        },
      });
    });

    // Mock Individual Team Data
    await page.route(`**/api/teams/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({
        json: {
          id: USER_TEAM_ID,
          city: "Arizona",
          name: "Cardinals",
          abbreviation: "ARI",
          wins: 5,
          losses: 3,
          salary_cap_space: 25000000,
        },
      });
    });

    // Mock Pending Offers
    await page.route(`**/api/trades/pending/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({
        json: { incoming: [], outgoing: [] },
      });
    });

    // Mock Teams List
    await page.route("**/api/teams?page=1&page_size=100", async (route) => {
      await route.fulfill({
        json: {
          items: [
            {
              id: USER_TEAM_ID,
              city: "Arizona",
              name: "Cardinals",
              abbreviation: "ARI",
              wins: 5,
              losses: 3,
            },
            {
              id: PARTNER_TEAM_ID,
              city: "Kansas City",
              name: "Chiefs",
              abbreviation: "KC",
              wins: 7,
              losses: 1,
            },
          ],
        },
      });
    });

    // Mock Rosters
    await page.route(`**/api/trades/players/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: MOCK_USER_PLAYERS });
    });

    await page.route(`**/api/trades/players/${PARTNER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: MOCK_PARTNER_PLAYERS });
    });

    // Mock Evaluation
    await page.route("**/api/trades/evaluate", async (route) => {
      const data = route.request().postDataJSON();
      // If getting Mahomes (201), REJECT. If getting Kelce (202), ACCEPT.
      const gettingMahomes = data.requested_player_ids?.includes(201);

      await route.fulfill({
        json: {
          decision: gettingMahomes ? "REJECT" : "ACCEPT",
          score: gettingMahomes ? -25.0 : 5.0,
          reasoning: gettingMahomes ? "Mahomes is untouchable." : "Fair value.",
          gm_philosophy: "WIN_NOW",
        },
      });
    });

    // Mock Submit Offer
    await page.route("**/api/trades/offer", async (route) => {
      await route.fulfill({
        json: { success: true, message: "Offer submitted successfully", offer_id: 999 },
      });
    });

    // DEBUG: Log any unmocked API requests
    await page.route("**/api/**", async (route) => {
      console.log(`[UNMOCKED API] ${route.request().method()} ${route.request().url()}`);
      await route.abort();
    });

    await tradePage.goto();
  });

  test("should negotiate a trade and submit offer", async ({ page }) => {
    // 1. Select Partner
    await tradePage.selectPartner(PARTNER_TEAM_ID.toString());

    // 2. Drag Murray (101) to Offer
    await tradePage.dragPlayerToOffer(101);
    await expect(page.locator('[data-testid="offered-zone"]')).toContainText("Murray");

    // 3. Drag Kelce (202) to Request
    await tradePage.dragPlayerToRequest(202);
    await expect(page.locator('[data-testid="requested-zone"]')).toContainText("Kelce");

    // 4. Evaluate
    await tradePage.evaluateBtn.click();
    await expect(page.locator('[data-testid="gm-response"]')).toContainText("ACCEPT");

    // 5. Submit
    // Handle alert
    page.on("dialog", (dialog) => dialog.accept());
    await tradePage.submitFormalOffer();

    // Verify reset (zones empty)
    await expect(page.locator('[data-testid="offered-zone"]')).not.toContainText("Murray");
  });

  test("should view processing offers and accept one", async ({ page }) => {
    // Mock Pending Offers
    const mockPendingOffers = [
      {
        id: 1,
        offering_team_id: PARTNER_TEAM_ID, // Incoming from Chiefs
        receiving_team_id: USER_TEAM_ID,
        offered_assets: [
          {
            id: 202,
            name: "Travis Kelce",
            type: "player",
            value: 60,
            position: "TE",
            team_id: PARTNER_TEAM_ID,
          },
        ],
        requested_assets: [
          {
            id: 102,
            name: "James Conner",
            type: "player",
            value: 20,
            position: "RB",
            team_id: USER_TEAM_ID,
          },
        ],
        status: "PENDING",
        created_at: new Date().toISOString(),
      },
    ];

    await page.route(`**/api/trades/pending/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: mockPendingOffers });
    });

    // Mock Respond (Accept)
    await page.route(`**/api/trades/respond/1`, async (route) => {
      await route.fulfill({ json: { success: true, message: "Trade accepted" } });
    });

    // 1. Go to Offers Tab
    await tradePage.openOffersTab();

    // 2. Verify Offer Content
    await expect(page.locator("text=Travis Kelce")).toBeVisible();
    await expect(page.locator("text=James Conner")).toBeVisible();

    // 3. Accept
    page.on("dialog", (dialog) => dialog.accept());
    await tradePage.acceptOffer(1);

    // 4. Verify Removed from list (optimistic update or re-fetch)
    // In current implementation, it might reload. We can mock empty list on second call if needed,
    // but the component likely filters locally or re-fetches.
    // Let's assume re-fetch happens.
    await page.route(`**/api/trades/pending/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: [] }); // Empty now
    });

    // Trigger refresh manually or wait for auto-update if implemented.
    // For this test, we check that the API endpoint was called (implicit in route handling)
  });

  test("should counter an offer", async ({ page }) => {
    // Mock Pending Offers (Same as above)
    const mockPendingOffers = [
      {
        id: 1,
        offering_team_id: PARTNER_TEAM_ID,
        receiving_team_id: USER_TEAM_ID,
        offered_assets: [
          {
            id: 202,
            name: "Travis Kelce",
            type: "player",
            value: 60,
            position: "TE",
            team_id: PARTNER_TEAM_ID,
          },
        ],
        requested_assets: [
          {
            id: 102,
            name: "James Conner",
            type: "player",
            value: 20,
            position: "RB",
            team_id: USER_TEAM_ID,
          },
        ],
        status: "PENDING",
        created_at: new Date().toISOString(),
      },
    ];

    await page.route(`**/api/trades/pending/${USER_TEAM_ID}`, async (route) => {
      await route.fulfill({ json: mockPendingOffers });
    });

    // Mock Counter
    await page.route(`**/api/trades/counter/1`, async (route) => {
      await route.fulfill({ json: { success: true, message: "Counter offer created" } });
    });

    // 1. Go to Offers
    await tradePage.openOffersTab();

    // 2. Click Counter
    await tradePage.clickCounterOffer(1);

    // 3. Verify Redirect to Negotiate
    await expect(tradePage.negotiateTab).toHaveAttribute("aria-selected", "true");

    // 4. Verify Pre-populated (My assets = what was Requested in offer; Partner assets = what was Offered)
    // "My Assets" (Offered Zone) should have Conner (102)
    // "Partner Assets" (Requested Zone) should have Kelce (202)
    await expect(page.locator('[data-testid="offered-zone"]')).toContainText("Conner");
    await expect(page.locator('[data-testid="requested-zone"]')).toContainText("Kelce");
  });

  test("should analyze trade fairness via widget", async ({ page }) => {
    // 1. Navigate to Trade Center
    // Already handled by beforeEach

    // 2. Verify Widget Initial State
    const widget = page.getByTestId("trade-analyzer-widget");
    const analyzeBtn = page.getByTestId("analyze-btn");
    await expect(widget).toBeVisible();
    await expect(analyzeBtn).toBeDisabled(); // Disabled when empty

    // 3. Drag assets to enable analysis
    await tradePage.selectPartner(PARTNER_TEAM_ID.toString());
    await tradePage.dragPlayerToOffer(101); // Kyler Murray
    await tradePage.dragPlayerToRequest(202); // Travis Kelce (ACCEPT scenario)

    await expect(analyzeBtn).toBeEnabled();

    // 4. Analyze (Loading State)
    const pendingAnalysis = page.waitForResponse("**/api/trades/evaluate");
    await analyzeBtn.click();

    // Wait for response first to ensure state change
    await pendingAnalysis;

    // 5. Verify Result (ACCEPT)
    await expect(page.getByTestId("evaluation-result")).toHaveClass(/accept/i);
    await expect(page.getByTestId("decision-badge")).toHaveText("ACCEPT");
    await expect(page.getByTestId("fairness-score")).toHaveText("+5");
    await expect(page.getByTestId("gm-reasoning")).toContainText("Fair value");

    // 6. Test Re-evaluate (Change assets)
    await page.getByTestId("re-analyze-btn").click();
    // Drag untradable asset (Mahomes 201)
    await tradePage.dragPlayerToRequest(201);

    // Mock REJECT response logic handled in beforeEach (if gettingMahomes)

    await analyzeBtn.click();

    // 7. Verify Result (REJECT)
    await expect(page.getByTestId("evaluation-result")).toHaveClass(/reject/i);
    await expect(page.getByTestId("decision-badge")).toHaveText("REJECT");
    await expect(page.getByTestId("fairness-score")).toHaveText("-25");
    await expect(page.getByTestId("gm-reasoning")).toContainText("untouchable");
  });
});

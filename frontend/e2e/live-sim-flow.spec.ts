import { test, expect } from "@playwright/test";

// Mock game state updates for WebSocket
const mockGameUpdates = [
  {
    event: "game_update",
    payload: {
      score: { home: 3, away: 0 },
      quarter: 1,
      time_remaining: "10:00",
      play_by_play: "Kickoff, touchback.",
    },
  },
  {
    event: "game_update",
    payload: {
      score: { home: 7, away: 0 },
      quarter: 1,
      time_remaining: "05:30",
      play_by_play: "TOUCHDOWN! Home team scores.",
    },
  },
  {
    event: "game_update",
    payload: {
      score: { home: 7, away: 3 },
      quarter: 2,
      time_remaining: "12:00",
      play_by_play: "Field Goal good for away team.",
    },
  },
];

test.describe("Live Simulation Flow", () => {
  test.beforeEach(async ({ page }) => {
    // Mock start and stop simulation API calls
    await page.route("**/api/simulation/live/start*", async (route) => {
      await route.fulfill({ status: 200, json: { message: "Simulation started" } });
    });
    await page.route("**/api/simulation/live/stop*", async (route) => {
      await route.fulfill({ status: 200, json: { message: "Simulation stopped" } });
    });

    // Native Playwright WebSocket route
    await page.routeWebSocket(/.*\/ws.*/, (ws) => {
      let i = 0;
      const interval = setInterval(() => {
        if (i < mockGameUpdates.length) {
          ws.send(JSON.stringify(mockGameUpdates[i]));
          i++;
        } else {
          clearInterval(interval);
        }
      }, 300);

      ws.onClose(() => {
        clearInterval(interval);
      });
    });
  });

  test("should load live sim and start simulation, receiving updates", async ({ page }) => {
    await page.goto("/live-sim");

    // Verify initial state: KICKOFF button is visible
    await expect(page.locator("button", { hasText: "KICKOFF" })).toBeVisible();

    // Click KICKOFF button
    await page.locator("button", { hasText: "KICKOFF" }).click();

    // Verify loading state, then Pause/FastForward buttons
    await expect(page.locator("button", { hasText: "Starting..." })).toBeVisible();
    await expect(page.locator("button", { hasText: "Pause" })).toBeVisible({ timeout: 5000 });
    await expect(page.locator("button", { hasText: "FastForward" })).toBeVisible();

    // Verify UI updates based on mock WebSocket messages
    // First update: Score 3-0, Q1, 10:00
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText("3", {
      timeout: 3000,
    });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText("0");
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText("Q1");
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText("10:00");
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText(
      "Kickoff, touchback."
    );

    // Second update: Score 7-0, Q1, 05:30
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText("7", {
      timeout: 3000,
    });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText("0");
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText("Q1");
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText("05:30");
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText(
      "TOUCHDOWN! Home team scores."
    );

    // Third update: Score 7-3, Q2, 12:00
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toContainText("7", {
      timeout: 3000,
    });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toContainText("3");
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toContainText("Q2");
    await expect(page.locator('[data-testid="game-clock-time"]')).toContainText("12:00");
    await expect(page.locator('[data-testid="play-by-play-feed"]')).toContainText(
      "Field Goal good for away team."
    );

    await page.locator("button", { hasText: "Pause" }).click();
    await expect(page.locator("button", { hasText: "KICKOFF" })).toBeVisible();
  });

  test("should display momentum indicators in scoreboard", async ({ page }) => {
    await page.goto("/live-sim");
    // Check that momentum indicators are present.
    // They are rendered as divs with specific classes inside the scoreboard.
    // We can rely on structure or add specific data-testids in the component if needed.
    // Ideally we would add data-testid="momentum-indicator" to the MomentumIndicator component.
    // For now, let's look for the component by its visual structure (the wrapper div)
    // The component wrapper has "flex items-center gap-1 px-3 py-1 bg-slate-900/50 rounded-full border border-white/10"

    // Waiting for page load
    await expect(page.locator("button", { hasText: "KICKOFF" })).toBeVisible();

    // Verify indicators exist (rendered in primary scoreboard and viewport panels)
    const momentumContainers = page.locator('[data-testid="momentum-indicator"]');
    await expect(momentumContainers.first()).toBeVisible();
    await expect(momentumContainers).toHaveCount(4);

    // Initial state should be NEUTRAL (Minus icon)
    await expect(page.locator("svg.lucide-minus").first()).toBeVisible();
  });
});

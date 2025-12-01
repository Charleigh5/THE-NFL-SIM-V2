import { test, expect } from "@playwright/test";
import { TestHelpers } from "./test-helpers";

/**
 * E2E Tests for Enhanced Season Dashboard
 * Tests the new dashboard features including:
 * - Quick action buttons
 * - Season summary card
 * - League leaders display
 * - Playoff functionality
 */
test.describe("Enhanced Season Dashboard", () => {
  test.beforeEach(async ({ request, page }) => {
    // Seed database and initialize a season
    await TestHelpers.seedDatabase(request);

    // Navigate to dashboard
    await page.goto("/");

    // Initialize a new season
    const startButton = page.locator("button:has-text('Initialize New Season')");
    if (await startButton.isVisible()) {
      await startButton.click();
      await page.waitForLoadState("networkidle");
    }

    // Wait for season data to load
    await page.waitForSelector(".season-summary-card", { timeout: 10000 });
  });

  test("Quick action buttons appear and work", async ({ page }) => {
    // Verify all quick action buttons are present in the Season Summary Card
    const simulateBtn = page.locator("button:has-text('Simulate Week')");
    const simToPlayoffsBtn = page.locator("button:has-text('Sim to Playoffs')");
    const playoffsBtn = page.locator("button:has-text('View Playoffs')");

    // Check that buttons are visible
    await expect(simulateBtn).toBeVisible();
    await expect(simToPlayoffsBtn).toBeVisible();

    // View Playoffs should be visible but disabled initially (regular season)
    await expect(playoffsBtn).toBeVisible();
    await expect(playoffsBtn).toBeDisabled();

    // Verify Simulate Week button is enabled
    await expect(simulateBtn).toBeEnabled();

    // Verify Sim to Playoffs button is enabled during regular season
    await expect(simToPlayoffsBtn).toBeEnabled();

    // Verify button tooltips/titles are present
    await expect(simulateBtn).toHaveAttribute("title", /simulate all games/i);
    await expect(simToPlayoffsBtn).toHaveAttribute("title", /simulate remaining/i);
  });

  test("Simulate Week functionality end-to-end", async ({ page }) => {
    // Get current week number before simulation
    const weekText = await page.locator(".season-summary-card .week-info").textContent();
    const currentWeek = parseInt(weekText?.match(/Week (\\d+)/)?.[1] || "1");

    // Click Simulate Week button
    const simulateBtn = page.locator("button:has-text('Simulate Week')");
    await simulateBtn.click();

    // Verify loading state appears
    await expect(page.locator(".loading-overlay")).toBeVisible({ timeout: 2000 });
    await expect(page.locator("text=Simulating...")).toBeVisible();

    // Wait for simulation to complete (loading overlay should disappear)
    await expect(page.locator(".loading-overlay")).not.toBeVisible({ timeout: 30000 });

    // Verify week has advanced
    const newWeekText = await page.locator(".season-summary-card .week-info").textContent();
    const newWeek = parseInt(newWeekText?.match(/Week (\\d+)/)?.[1] || "1");
    expect(newWeek).toBeGreaterThan(currentWeek);

    // Verify games are marked as played
    await page.click("button:has-text('Schedule')");
    await page.waitForTimeout(500); // Wait for tab switch
    const playedGames = page.locator(".game-card.played, .game-status:has-text('Final')");
    await expect(playedGames.first()).toBeVisible({ timeout: 5000 });
  });

  test("League leaders display correctly", async ({ page }) => {
    // Verify League Leaders section is visible
    const leadersContainer = page.locator(".league-leaders-container");
    await expect(leadersContainer).toBeVisible();

    // Check header
    await expect(leadersContainer.locator("h3:has-text('League Leaders')")).toBeVisible();

    // Verify top leader card shows player info
    const topLeader = page.locator(".leader-top");
    await expect(topLeader).toBeVisible();

    // Check player name is clickable
    const playerName = topLeader.locator("h4");
    await expect(playerName).toBeVisible();

    // Check team logo and stats are displayed
    await expect(topLeader.locator(".leader-team-logo, .leader-info p")).toBeVisible();
    await expect(topLeader.locator(".stat-value")).toBeVisible();
    await expect(topLeader.locator(".stat-label:has-text('YDS')")).toBeVisible();

    // Verify leader list shows ranks 2-5
    const leaderRows = page.locator(".leader-row");
    const rowCount = await leaderRows.count();
    expect(rowCount).toBeGreaterThanOrEqual(1);
    expect(rowCount).toBeLessThanOrEqual(4);

    // Check first row has rank 2
    if (rowCount > 0) {
      const firstRank = await leaderRows.first().locator(".rank").textContent();
      expect(firstRank).toBe("2");
    }
  });

  test("Leader category tabs switch correctly", async ({ page }) => {
    const leadersContainer = page.locator(".league-leaders-container");

    // Get tab buttons
    const passingTab = leadersContainer.locator("button:has-text('Pass')");
    const rushingTab = leadersContainer.locator("button:has-text('Rush')");
    const receivingTab = leadersContainer.locator("button:has-text('Rec')");

    // Verify Passing tab is active by default
    await expect(passingTab).toHaveClass(/active/);

    // Store the first passing leader name
    const passingLeaderName = await page.locator(".leader-top h4").textContent();

    // Switch to Rushing tab
    await rushingTab.click();
    await page.waitForTimeout(300); // Small delay for UI update

    // Verify Rushing tab is now active
    await expect(rushingTab).toHaveClass(/active/);
    await expect(passingTab).not.toHaveClass(/active/);

    // Verify rushing stats are displayed
    await expect(page.locator(".leader-top .stat-value")).toBeVisible();

    // Switch to Receiving tab
    await receivingTab.click();
    await page.waitForTimeout(300);

    // Verify Receiving tab is active
    await expect(receivingTab).toHaveClass(/active/);
    await expect(rushingTab).not.toHaveClass(/active/);

    // Switch back to Passing
    await passingTab.click();
    await page.waitForTimeout(300);

    // Verify we're back to passing and same leader
    await expect(passingTab).toHaveClass(/active/);
    const finalPassingLeaderName = await page.locator(".leader-top h4").textContent();
    expect(finalPassingLeaderName).toBe(passingLeaderName);
  });

  test("Season summary shows correct data", async ({ page }) => {
    const summaryCard = page.locator(".season-summary-card");

    // Verify season summary card is visible
    await expect(summaryCard).toBeVisible();

    // Check season year is displayed
    const yearText = await summaryCard
      .locator(".season-year, .summary-item:has-text('Season')")
      .textContent();
    expect(yearText).toMatch(/20\d{2}/); // Should contain a year like 2024, 2025, etc.

    // Check current week is displayed
    const weekInfo = summaryCard.locator(".week-info, .summary-item:has-text('Week')");
    await expect(weekInfo).toBeVisible();
    const weekText = await weekInfo.textContent();
    expect(weekText).toMatch(/Week \d+/);

    // Check status/phase is displayed
    const statusInfo = summaryCard.locator(
      ".season-status, .summary-item:has-text('Status'), .summary-item:has-text('Phase')"
    );
    await expect(statusInfo.first()).toBeVisible();

    // Verify games played/remaining info
    const gamesInfo = page.locator(".summary-item:has-text('Games'), .games-played");
    if ((await gamesInfo.count()) > 0) {
      const gamesText = await gamesInfo.first().textContent();
      expect(gamesText).toMatch(/\d+/); // Should contain numbers
    }

    // Verify progress indicator if present
    const progressBar = summaryCard.locator(".progress-bar, .season-progress");
    if ((await progressBar.count()) > 0) {
      await expect(progressBar.first()).toBeVisible();
    }
  });

  test("Playoff button appears when appropriate", async ({ page }) => {
    // Initially in regular season, playoff button should be disabled
    const playoffsBtn = page.locator("button:has-text('View Playoffs')");
    await expect(playoffsBtn).toBeVisible();
    await expect(playoffsBtn).toBeDisabled();

    // Simulate to playoffs
    const simToPlayoffsBtn = page.locator("button:has-text('Sim to Playoffs')");
    await expect(simToPlayoffsBtn).toBeEnabled();

    await simToPlayoffsBtn.click();

    // Wait for simulation to complete
    await expect(page.locator(".loading-overlay")).toBeVisible({ timeout: 2000 });
    await expect(page.locator(".loading-overlay")).not.toBeVisible({ timeout: 60000 });

    // Now playoff button should be enabled
    await expect(playoffsBtn).toBeEnabled();

    // Verify status changed to POST_SEASON
    const statusText = await page
      .locator(".season-status, .summary-item:has-text('Status'), .summary-item:has-text('Phase')")
      .first()
      .textContent();
    expect(statusText).toMatch(/playoff|post.?season/i);

    // Click playoff button and verify navigation
    await playoffsBtn.click();
    await page.waitForTimeout(500);

    // Verify Playoffs tab is active
    const playoffsTab = page.locator("button.tab-button:has-text('Playoffs')");
    await expect(playoffsTab).toBeVisible();
    await expect(playoffsTab).toHaveClass(/active/);

    // Verify playoff bracket is displayed
    const playoffBracket = page.locator(".playoff-bracket, .bracket-container");
    await expect(playoffBracket).toBeVisible({ timeout: 5000 });
  });

  test("Player modal opens from league leaders", async ({ page }) => {
    // Click on top passing leader's name
    const leaderName = page.locator(".leader-top h4").first();
    await leaderName.click();

    // Verify player modal opens
    const modal = page.locator(".player-modal, .modal");
    await expect(modal).toBeVisible({ timeout: 3000 });

    // Verify modal shows player information
    const modalContent = modal.locator(".modal-content, .player-modal-content");
    await expect(modalContent).toBeVisible();

    // Close modal
    const closeBtn = modal.locator("button:has-text('Close'), .close-button, .modal-close");
    if ((await closeBtn.count()) > 0) {
      await closeBtn.first().click();
      await expect(modal).not.toBeVisible();
    }
  });

  test("Dashboard tabs navigation works", async ({ page }) => {
    // Test Overview tab
    const overviewTab = page.locator("button.tab-button:has-text('Overview')");
    await overviewTab.click();
    await expect(overviewTab).toHaveClass(/active/);
    await expect(page.locator(".overview-grid, .overview-section")).toBeVisible();

    // Test Standings tab
    const standingsTab = page.locator("button.tab-button:has-text('Standings')");
    await standingsTab.click();
    await expect(standingsTab).toHaveClass(/active/);
    await expect(page.locator(".standings-table, table")).toBeVisible();

    // Test Schedule tab
    const scheduleTab = page.locator("button.tab-button:has-text('Schedule')");
    await scheduleTab.click();
    await expect(scheduleTab).toHaveClass(/active/);
    await expect(page.locator(".schedule-view, .games-list")).toBeVisible();

    // Test Leaders tab
    const leadersTab = page.locator("button.tab-button:has-text('Leaders')");
    await leadersTab.click();
    await expect(leadersTab).toHaveClass(/active/);
    await expect(page.locator(".league-leaders-container")).toBeVisible();
  });

  test("Responsive layout on mobile", async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Verify dashboard is still usable
    const summaryCard = page.locator(".season-summary-card");
    await expect(summaryCard).toBeVisible();

    // Verify quick actions are accessible
    const simulateBtn = page.locator("button:has-text('Simulate Week')");
    await expect(simulateBtn).toBeVisible();

    // Verify league leaders are displayed
    const leadersContainer = page.locator(".league-leaders-container");
    await expect(leadersContainer).toBeVisible();

    // Verify tabs are accessible
    const tabs = page.locator(".dashboard-tabs");
    await expect(tabs).toBeVisible();

    // Test tab switching on mobile
    const standingsTab = page.locator("button.tab-button:has-text('Standings')");
    await standingsTab.click();
    await expect(standingsTab).toHaveClass(/active/);
  });
});

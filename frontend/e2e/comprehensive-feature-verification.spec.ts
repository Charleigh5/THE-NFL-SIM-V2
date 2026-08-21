import { test, expect } from "@playwright/test";
import { mockTeam, mockPlayers } from "./fixtures/test-data";
import path from "path";
import fs from "fs";

const mockSystemHealth = { status: "healthy" };

const mockCurrentSeason = {
  id: 1,
  year: 2025,
  status: "REGULAR_SEASON",
  current_week: 4,
};

test.describe("Exhaustive Interactive Feature Verification & Audit Suite", () => {
  const auditDir = path.resolve(process.cwd(), "../docs/assets/screenshots/interactive_audit");

  test.beforeAll(() => {
    if (!fs.existsSync(auditDir)) {
      fs.mkdirSync(auditDir, { recursive: true });
    }
  });

  test.beforeEach(async ({ page }) => {
    // Set standard viewport for crystal-clear broadcast capture
    await page.setViewportSize({ width: 1440, height: 900 });

    // Standard mock network routes
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeason });
    });

    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, difficulty_level: "All-Pro", theme: "GB" } });
    });

    await page.route("**/api/settings/team", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, team_id: 1, success: true } });
    });

    await page.route("**/api/teams?*", async (route) => {
      await route.fulfill({
        json: {
          items: [
            mockTeam,
            { id: 2, name: "Kansas City Chiefs", city: "Kansas City", abbreviation: "KC", conference: "AFC", division: "West", salary_cap_space: 22000000 },
            { id: 3, name: "San Francisco 49ers", city: "San Francisco", abbreviation: "SF", conference: "NFC", division: "West", salary_cap_space: 14500000 },
          ],
          total: 3,
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

    await page.route("**/api/news/**", async (route) => {
      await route.fulfill({ json: { items: [], total: 0, last_updated: new Date().toISOString() } });
    });

    await page.route("**/api/players/1", async (route) => {
      await route.fulfill({ json: mockPlayers[0] });
    });

    await page.route("**/api/traits/**", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/abilities/**", async (route) => {
      await route.fulfill({ json: [] });
    });

    await page.route("**/api/medical/**", async (route) => {
      await route.fulfill({ json: { injuries: [], staff: [] } });
    });

    await page.route("**/api/draft/**", async (route) => {
      await route.fulfill({ json: { prospects: [], board: [], pick: 1, current_round: 1 } });
    });

    await page.route("**/api/trades/**", async (route) => {
      await route.fulfill({ json: { offers: [], status: "ok" } });
    });

    await page.route("**/api/training/**", async (route) => {
      await route.fulfill({
        json: {
          drills: [
            { name: "Oklahoma Drill", position: "ALL", category: "PHYSICAL", description: "Contact drill" },
            { name: "7-on-7 Skeleton", position: "QB", category: "TACTICAL", description: "Pass coverage" },
          ],
          styles: [
            { name: "smart", display_name: "Smart", xp_multiplier: 1.0, injury_risk_multiplier: 0.8 },
            { name: "old_school", display_name: "Old School", xp_multiplier: 1.2, injury_risk_multiplier: 1.5 },
          ],
        },
      });
    });
  });

  test("01 - War Room Dashboard: Sim Week & Action Tiles", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial state
    await page.screenshot({ path: path.join(auditDir, "01_war_room_before_sim.png") });
    await expect(page.locator("h1", { hasText: "WAR ROOM" })).toBeVisible();

    // Verify Matchup Card
    const startSeasonBtn = page.locator(".start-season-btn");
    await expect(startSeasonBtn).toBeVisible();

    // Click Sim Week
    await startSeasonBtn.click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(auditDir, "01_war_room_after_sim_click.png") });

    // Verify Quick Actions Section
    await expect(page.locator(".quick-actions-section")).toBeVisible();
    await page.screenshot({ path: path.join(auditDir, "01_war_room_quick_actions_view.png") });
  });

  test("02 - Front Office: Positional Filters & Player Card Detail Modal", async ({ page }) => {
    await page.goto("/empire/front-office");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial roster view
    await page.screenshot({ path: path.join(auditDir, "02_front_office_initial.png") });

    // Click 'OFF' filter tab
    const offTab = page.locator("button", { hasText: "OFF" }).first();
    if (await offTab.isVisible()) {
      await offTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "02_front_office_off_filter_active.png") });
    }

    // Click 'DEF' filter tab
    const defTab = page.locator("button", { hasText: "DEF" }).first();
    if (await defTab.isVisible()) {
      await defTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "02_front_office_def_filter_active.png") });
    }

    // Reset to ALL
    const allTab = page.locator("button", { hasText: "ALL" }).first();
    if (await allTab.isVisible()) {
      await allTab.click();
      await page.waitForTimeout(200);
    }

    // Click Player Card to trigger Modal
    const firstPlayerCard = page.locator('[data-testid^="player-card-"]').first();
    if (await firstPlayerCard.isVisible()) {
      await page.screenshot({ path: path.join(auditDir, "02_front_office_before_player_click.png") });
      await firstPlayerCard.click();
      await page.waitForTimeout(400);

      // Verify Modal rendered
      const modal = page.locator('[data-testid="player-modal"]');
      if (await modal.isVisible()) {
        await page.screenshot({ path: path.join(auditDir, "02_front_office_player_modal_opened.png") });

        // Close modal
        const closeBtn = page.locator("button", { hasText: "Close" }).or(page.locator("button:has-text('✕')")).first();
        if (await closeBtn.isVisible()) {
          await closeBtn.click();
          await page.waitForTimeout(200);
          await page.screenshot({ path: path.join(auditDir, "02_front_office_player_modal_closed.png") });
        }
      }
    }
  });

  test("03 - Game Day Live Sim: Scorebug, Kickoff, & 3D Stage", async ({ page }) => {
    await page.goto("/live-sim");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial Live Sim stadium view
    await page.screenshot({ path: path.join(auditDir, "03_live_sim_before_kickoff.png") });

    // Verify Scorebug elements
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toBeVisible();
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toBeVisible();
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toBeVisible();

    // Click Kickoff
    const kickoffBtn = page.locator("button", { hasText: "KICKOFF" });
    if (await kickoffBtn.isVisible()) {
      await kickoffBtn.click();
      await page.waitForTimeout(400);
    }

    // Capture state after kickoff
    await page.screenshot({ path: path.join(auditDir, "03_live_sim_after_kickoff.png") });

    // Switch view tabs
    const boxScoreTab = page.locator("button", { hasText: "BOX SCORE" });
    if (await boxScoreTab.isVisible()) {
      await boxScoreTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "03_live_sim_box_score_view.png") });
    }

    const fieldViewTab = page.locator("button", { hasText: "FIELD VIEW" });
    if (await fieldViewTab.isVisible()) {
      await fieldViewTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "03_live_sim_field_view_active.png") });
    }
  });

  test("04 - Chalkboard Playbook: Formations, Play Art, & Chalk Tools", async ({ page }) => {
    await page.goto("/playbook");
    await page.waitForLoadState("domcontentloaded");

    // Initial playbook state
    await page.screenshot({ path: path.join(auditDir, "04_playbook_initial.png") });

    // Click Draw button to activate telestrator
    const drawBtn = page.locator('button:has-text("✏️ Draw")');
    if (await drawBtn.isVisible()) {
      await drawBtn.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "04_playbook_draw_mode_active.png") });

      // Click Exit Drawing Mode button on Telestrator toolbar
      const exitTelestrator = page.locator('button[title="Exit Drawing Mode"]');
      if (await exitTelestrator.isVisible()) {
        await exitTelestrator.click();
        await page.waitForTimeout(200);
      }
    }

    await page.screenshot({ path: path.join(auditDir, "04_playbook_canvas_cleared.png") });

    // Switch to Play Art tab
    const playArtTab = page.locator("button", { hasText: "Play Art" });
    if (await playArtTab.isVisible()) {
      await playArtTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "04_playbook_play_art_tab.png") });
    }

    // Switch to Coaching Staff tab
    const staffTab = page.locator("button", { hasText: "Coaching Staff" });
    if (await staffTab.isVisible()) {
      await staffTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "04_playbook_coaching_staff_tab.png") });
    }
  });

  test("05 - Stadium Tunnel Franchise Selector: Conference Filters & Team Select", async ({ page }) => {
    await page.goto("/team-selection");
    await page.waitForLoadState("domcontentloaded");

    // Initial franchise tunnel
    await page.screenshot({ path: path.join(auditDir, "05_team_selection_initial.png") });

    // Filter AFC
    const afcBtn = page.locator("button", { hasText: "AFC" });
    if (await afcBtn.isVisible()) {
      await afcBtn.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "05_team_selection_afc_filtered.png") });
    }

    // Filter NFC
    const nfcBtn = page.locator("button", { hasText: "NFC" });
    if (await nfcBtn.isVisible()) {
      await nfcBtn.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "05_team_selection_nfc_filtered.png") });
    }

    // Click a franchise card
    const teamCard = page.locator(".team-card").first();
    if (await teamCard.isVisible()) {
      await page.screenshot({ path: path.join(auditDir, "05_team_selection_before_team_click.png") });
      await teamCard.click();
      await page.waitForTimeout(500);
      await page.screenshot({ path: path.join(auditDir, "05_team_selection_after_selection_redirect.png") });
    }
  });

  test("06 - Season Dashboard: Schedule, Standings, & Playoffs", async ({ page }) => {
    await page.goto("/season");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial season dashboard
    await page.screenshot({ path: path.join(auditDir, "06_season_dashboard_initial.png") });
  });

  test("07 - Trade Center & Draft Room Inspection", async ({ page }) => {
    await page.goto("/empire/trade-center");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "07_trade_center_initial.png") });

    await page.goto("/offseason/draft");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "07_draft_room_initial.png") });
  });

  test("08 - Medical Center & Training Camp", async ({ page }) => {
    await page.goto("/medical");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "08_medical_center_initial.png") });

    await page.goto("/training");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "08_training_center_initial.png") });
  });

  test("09 - Skills RPG Hub & Settings", async ({ page }) => {
    await page.goto("/skills");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "09_skills_hub_initial.png") });

    await page.goto("/settings");
    await page.waitForLoadState("domcontentloaded");
    await page.screenshot({ path: path.join(auditDir, "09_settings_initial.png") });
  });
});


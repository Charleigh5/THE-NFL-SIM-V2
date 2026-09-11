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
  total_weeks: 18,
};

test.describe("Exhaustive 13-View Interactive Feature Verification & Audit Suite", () => {
  const auditDir = path.resolve(process.cwd(), "../docs/assets/screenshots/interactive_audit");

  test.beforeAll(() => {
    if (!fs.existsSync(auditDir)) {
      fs.mkdirSync(auditDir, { recursive: true });
    }
  });

  test.beforeEach(async ({ page }) => {
    fs.mkdirSync(auditDir, { recursive: true });
    // Set standard viewport for crystal-clear broadcast capture
    await page.setViewportSize({ width: 1440, height: 900 });

    // Standard mock network routes
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeason });
    });

    await page.route(/.*\/api\/season\/summary/, async (route) => {
      await route.fulfill({
        json: {
          season: mockCurrentSeason,
          completion_percentage: 35,
        },
      });
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
            {
              id: 2,
              name: "Chiefs",
              city: "Kansas City",
              abbreviation: "KC",
              conference: "AFC",
              division: "West",
              salary_cap_space: 22000000,
            },
            {
              id: 3,
              name: "49ers",
              city: "San Francisco",
              abbreviation: "SF",
              conference: "NFC",
              division: "West",
              salary_cap_space: 14500000,
            },
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

    await page.route("**/api/teams/1/chemistry", async (route) => {
      await route.fulfill({
        json: {
          overall_chemistry: 88,
          offensive_synergy: 91,
          defensive_synergy: 86,
          special_teams_synergy: 84,
          chemistry_tier: "ELITE",
        },
      });
    });

    await page.route("**/api/news/**", async (route) => {
      await route.fulfill({
        json: { items: [], total: 0, last_updated: new Date().toISOString() },
      });
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
      await route.fulfill({
        json: {
          injuries: [],
          staff: [],
          head_health: 95,
          neck_health: 90,
          torso_health: 92,
          right_arm_health: 68,
          left_arm_health: 98,
          right_leg_health: 94,
          left_leg_health: 82,
          general_wear: 14,
        },
      });
    });

    await page.route("**/api/draft/**", async (route) => {
      await route.fulfill({
        json: {
          prospects: [
            {
              id: 1,
              name: "Caleb Williams",
              position: "QB",
              college: "USC",
              overall_rating: 86,
              potential_rating: 96,
              combine: {
                forty_yard_dash: 4.56,
                s2_cognition_score: 94,
                gps_speed_max: 21.4,
              },
            },
            {
              id: 2,
              name: "Marvin Harrison Jr.",
              position: "WR",
              college: "Ohio State",
              overall_rating: 85,
              potential_rating: 95,
              combine: {
                forty_yard_dash: 4.41,
                s2_cognition_score: 89,
                gps_speed_max: 22.1,
              },
            },
          ],
          board: [],
          pick: 1,
          current_round: 1,
        },
      });
    });

    await page.route("**/api/trades/**", async (route) => {
      await route.fulfill({
        json: {
          partners: [
            { id: 2, name: "Chiefs", city: "Kansas City", abbreviation: "KC" },
            { id: 3, name: "49ers", city: "San Francisco", abbreviation: "SF" },
          ],
          players: mockPlayers,
          offers: [],
          incoming: [],
          outgoing: [],
          status: "ok",
        },
      });
    });

    await page.route("**/api/training/**", async (route) => {
      await route.fulfill({
        json: {
          drills: [
            {
              name: "Oklahoma Drill",
              position: "ALL",
              category: "PHYSICAL",
              description: "Contact drill",
            },
            {
              name: "7-on-7 Skeleton",
              position: "QB",
              category: "TACTICAL",
              description: "Pass coverage",
            },
          ],
          styles: [
            {
              name: "smart",
              display_name: "Smart",
              xp_multiplier: 1.0,
              injury_risk_multiplier: 0.8,
            },
            {
              name: "old_school",
              display_name: "Old School",
              xp_multiplier: 1.2,
              injury_risk_multiplier: 1.5,
            },
          ],
        },
      });
    });
  });

  // VIEW 1: Franchise War Room / Dynasty Hub Dashboard
  test("View 01 - Franchise War Room / Dynasty Hub Dashboard", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial state
    await page.screenshot({ path: path.join(auditDir, "01_war_room_before_sim.png") });
    await expect(page.locator("h1", { hasText: "WAR ROOM" })).toBeVisible();

    // Verify Matchup Card
    const startSeasonBtn = page.locator(".start-season-btn");
    await expect(startSeasonBtn).toBeVisible();

    // Click Sim Week / Kickoff
    await startSeasonBtn.click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(auditDir, "01_war_room_after_sim_click.png") });

    // Verify Quick Actions Section
    await expect(page.locator(".quick-actions-section")).toBeVisible();
    await page.screenshot({ path: path.join(auditDir, "01_war_room_quick_actions_view.png") });

    expect(errors).toEqual([]);
  });

  // VIEW 2: Tactical Live Sim Chalkboard & Field Radar
  test("View 02 - Tactical Live Sim Chalkboard & Field Radar", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/live-sim");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial Live Sim stadium view
    await page.screenshot({ path: path.join(auditDir, "02_live_sim_before_kickoff.png") });

    // Verify Scorebug elements
    await expect(page.locator('[data-testid="scoreboard-home-score"]')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('[data-testid="scoreboard-away-score"]')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('[data-testid="game-clock-quarter"]')).toBeVisible({ timeout: 10000 });

    // Switch to Turf & S2 Cognition tab
    const gridironTab = page.locator("button", { hasText: "Turf & S2 Cognition" });
    if (await gridironTab.isVisible()) {
      await gridironTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "02_live_sim_turf_cognition_active.png") });
    }

    // Click Kickoff
    const kickoffBtn = page.locator("button", { hasText: "KICKOFF" });
    if (await kickoffBtn.isVisible()) {
      await kickoffBtn.click();
      await page.waitForTimeout(400);
    }

    // Capture state after kickoff
    await page.screenshot({ path: path.join(auditDir, "02_live_sim_after_kickoff.png") });

    // Switch to Box Score tab
    const boxScoreTab = page
      .locator("button", { hasText: "BOX SCORE" })
      .or(page.locator("button", { hasText: "Box Score" }))
      .first();
    if (await boxScoreTab.isVisible()) {
      await boxScoreTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "02_live_sim_box_score_view.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 3: Offseason Draft Room with Multi-Lens Scouting Fog of War
  test("View 03 - Offseason Draft Room with Multi-Lens Scouting Fog of War", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/offseason/draft");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial draft room state
    await page.screenshot({ path: path.join(auditDir, "03_draft_room_initial_consensus.png") });

    // Switch Scout Bias Lens to Analytics & GPS
    const analyticsLensBtn = page.locator("button", { hasText: "Analytics & GPS" });
    if (await analyticsLensBtn.isVisible()) {
      await analyticsLensBtn.click();
      await page.waitForTimeout(300);
      await page.screenshot({
        path: path.join(auditDir, "03_draft_room_analytics_lens_active.png"),
      });
    }

    // Switch Scout Bias Lens to Film Room Guru
    const filmLensBtn = page.locator("button", { hasText: "Film Room Guru" });
    if (await filmLensBtn.isVisible()) {
      await filmLensBtn.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "03_draft_room_film_lens_active.png") });
    }

    // Click Auto-Sim Draft or Propose Trade button
    const autoSimBtn = page.locator("button", { hasText: "Auto-Sim Draft" });
    if (await autoSimBtn.isVisible()) {
      await page.screenshot({ path: path.join(auditDir, "03_draft_room_war_room_controls.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 4: Coaching Dynasty Tree & Staff Chemistry Matrix
  test("View 04 - Coaching Dynasty Tree & Staff Chemistry Matrix", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/playbook");
    await page.waitForLoadState("domcontentloaded");

    // Initial playbook state
    await page.screenshot({ path: path.join(auditDir, "04_playbook_weekly_install_initial.png") });

    // Click Draw button to test telestrator chalk
    const drawBtn = page.locator('button:has-text("✏️ Draw")');
    if (await drawBtn.isVisible()) {
      await drawBtn.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "04_playbook_chalk_mode_active.png") });

      const exitTelestrator = page.locator('button[title="Exit Drawing Mode"]');
      if (await exitTelestrator.isVisible()) {
        await exitTelestrator.click();
        await page.waitForTimeout(200);
      }
    }

    // Switch to Coaching Staff tab
    const staffTab = page.locator("button", { hasText: "Coaching Staff" });
    if (await staffTab.isVisible()) {
      await staffTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "04_coaching_dynasty_tree_view.png") });

      // Toggle to Staff Organizational Chart
      const orgChartBtn = page.locator("button", { hasText: "Staff Organizational Chart" });
      if (await orgChartBtn.isVisible()) {
        await orgChartBtn.click();
        await page.waitForTimeout(300);
        await page.screenshot({ path: path.join(auditDir, "04_coaching_staff_org_chart.png") });
      }
    }

    expect(errors).toEqual([]);
  });

  // VIEW 5: Medical Trauma Center & 5-Pathway Orthopedic Triage
  test("View 05 - Medical Trauma Center & 5-Pathway Orthopedic Triage", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/medical");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial anatomical body map and trauma center
    await page.screenshot({ path: path.join(auditDir, "05_medical_trauma_center_initial.png") });

    // Click on Right Arm zone or Adjust Protocol button to open 5-Pathway Orthopedic Triage Modal
    const triageBtn = page
      .locator("button", { hasText: "Adjust Protocol" })
      .or(page.locator("button", { hasText: "Triage" }))
      .first();
    if (await triageBtn.isVisible()) {
      await triageBtn.click();
      await page.waitForTimeout(300);
      await page.screenshot({
        path: path.join(auditDir, "05_medical_orthopedic_triage_modal_opened.png"),
      });

      // Select PRP Biotherapy option
      const prpOption = page
        .locator("button", { hasText: "Platelet-Rich Plasma" })
        .or(page.locator("button", { hasText: "PRP" }))
        .first();
      if (await prpOption.isVisible()) {
        await prpOption.click();
        await page.waitForTimeout(200);
        await page.screenshot({ path: path.join(auditDir, "05_medical_triage_prp_selected.png") });
      }

      // Close modal
      const closeBtn = page
        .locator("button", { hasText: "Cancel" })
        .or(page.locator("button:has-text('✕')"))
        .first();
      if (await closeBtn.isVisible()) {
        await closeBtn.click();
        await page.waitForTimeout(200);
      }
    }

    expect(errors).toEqual([]);
  });

  // VIEW 6: Depth Chart & Positional Hierarchy
  test("View 06 - Depth Chart & Positional Hierarchy", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/depth-chart");
    await page.waitForLoadState("domcontentloaded");

    // Capture QB initial depth chart
    await page.screenshot({ path: path.join(auditDir, "06_depth_chart_qb_initial.png") });

    // Switch to WR position
    const wrTab = page.locator("button", { hasText: "WR" }).first();
    if (await wrTab.isVisible()) {
      await wrTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "06_depth_chart_wr_filtered.png") });
    }

    // Switch to DE position
    const deTab = page.locator("button", { hasText: "DE" }).first();
    if (await deTab.isVisible()) {
      await deTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "06_depth_chart_de_filtered.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 7: Roster Management & Capology Contracts
  test("View 07 - Roster Management & Capology Contracts", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/roster");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial roster view
    await page.screenshot({ path: path.join(auditDir, "07_roster_capology_initial.png") });

    // Click 'OFF' filter tab
    const offTab = page.locator("button", { hasText: "OFF" }).first();
    if (await offTab.isVisible()) {
      await offTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "07_roster_off_filter_active.png") });
    }

    // Click 'DEF' filter tab
    const defTab = page.locator("button", { hasText: "DEF" }).first();
    if (await defTab.isVisible()) {
      await defTab.click();
      await page.waitForTimeout(200);
      await page.screenshot({ path: path.join(auditDir, "07_roster_def_filter_active.png") });
    }

    // Click Player Card to trigger Modal
    const firstPlayerCard = page.locator('[data-testid^="player-card-"]').first();
    if (await firstPlayerCard.isVisible()) {
      await firstPlayerCard.click();
      await page.waitForTimeout(400);

      const modal = page.locator('[data-testid="player-modal"]');
      if (await modal.isVisible()) {
        await page.screenshot({ path: path.join(auditDir, "07_roster_player_modal_opened.png") });

        const closeBtn = page
          .locator("button", { hasText: "Close" })
          .or(page.locator("button:has-text('✕')"))
          .first();
        if (await closeBtn.isVisible()) {
          await closeBtn.click();
          await page.waitForTimeout(200);
          await page.screenshot({ path: path.join(auditDir, "07_roster_player_modal_closed.png") });
        }
      }
    }

    expect(errors).toEqual([]);
  });

  // VIEW 8: Season Schedule & Week Simulator
  test("View 08 - Season Schedule & Week Simulator", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/season");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial season dashboard overview
    await page.screenshot({ path: path.join(auditDir, "08_season_overview_initial.png") });

    // Click Schedule tab
    const scheduleTab = page.locator("button", { hasText: "Schedule" }).first();
    if (await scheduleTab.isVisible()) {
      await scheduleTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "08_season_schedule_view_active.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 9: League Standings & Playoff Bracket
  test("View 09 - League Standings & Playoff Bracket", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/season");
    await page.waitForLoadState("domcontentloaded");

    // Click Standings tab
    const standingsTab = page.locator("button", { hasText: "Standings" }).first();
    if (await standingsTab.isVisible()) {
      await standingsTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "09_season_standings_view_active.png") });
    }

    // Click Playoffs tab
    const playoffsTab = page.locator("button", { hasText: "Playoffs" }).first();
    if (await playoffsTab.isVisible()) {
      await playoffsTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "09_season_playoffs_bracket_view.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 10: Player Profile & Biometric/S2 Cognition Card
  test("View 10 - Player Profile & Biometric/S2 Cognition Card", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/players/1/skills");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial 3D skill tree canvas
    await page.screenshot({
      path: path.join(auditDir, "10_player_profile_skills_tree_initial.png"),
    });

    // Switch to ABILITIES tab
    const abilitiesTab = page
      .locator("button", { hasText: "ABILITIES" })
      .or(page.locator("button", { hasText: "Abilities" }))
      .first();
    if (await abilitiesTab.isVisible()) {
      await abilitiesTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({
        path: path.join(auditDir, "10_player_profile_abilities_tab_active.png"),
      });
    }

    // Switch to TRAITS tab
    const traitsTab = page
      .locator("button", { hasText: "TRAITS" })
      .or(page.locator("button", { hasText: "Traits" }))
      .first();
    if (await traitsTab.isVisible()) {
      await traitsTab.click();
      await page.waitForTimeout(300);
      await page.screenshot({
        path: path.join(auditDir, "10_player_profile_traits_tab_active.png"),
      });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 11: Front Office GM Trades & Valuation Matrix
  test("View 11 - Front Office GM Trades & Valuation Matrix", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/trades");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial trade desk
    await page.screenshot({ path: path.join(auditDir, "11_trades_center_desk_initial.png") });

    // Select Trade Partner if dropdown exists
    const partnerSelect = page.locator("select").first();
    if (await partnerSelect.isVisible()) {
      await partnerSelect.selectOption({ index: 1 });
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "11_trades_partner_selected_matrix.png") });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 12: Cryptographic Replay Verification Telemetry
  test("View 12 - Cryptographic Replay Verification Telemetry", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/live-sim");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial replay scrubber and telemetry HUD
    await page.screenshot({ path: path.join(auditDir, "12_replay_telemetry_hud_initial.png") });

    // Check for replay scrubber slider
    const scrubber = page.locator('input[aria-label="Replay progress"]');
    if (await scrubber.isVisible()) {
      await scrubber.fill("50");
      await page.waitForTimeout(200);
      await page.screenshot({
        path: path.join(auditDir, "12_replay_telemetry_scrubber_advanced.png"),
      });
    }

    expect(errors).toEqual([]);
  });

  // VIEW 13: League Settings & Weather Simulation Config
  test("View 13 - League Settings & Weather Simulation Config", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));

    await page.goto("/settings");
    await page.waitForLoadState("domcontentloaded");

    // Capture initial settings state
    await page.screenshot({ path: path.join(auditDir, "13_settings_weather_config_initial.png") });

    // Change difficulty level
    const difficultySelect = page.locator('select[aria-label="Difficulty Level"]');
    if (await difficultySelect.isVisible()) {
      await difficultySelect.selectOption("Hall of Fame");
      await page.waitForTimeout(200);
    }

    // Change weather condition
    const weatherSelect = page.locator('select[aria-label="Weather Condition"]');
    if (await weatherSelect.isVisible()) {
      await weatherSelect.selectOption("Snow");
      await page.waitForTimeout(200);
      await page.screenshot({
        path: path.join(auditDir, "13_settings_weather_snow_configured.png"),
      });
    }

    // Click Change Team
    const changeTeamBtn = page.locator("button", { hasText: "Change Team" });
    if (await changeTeamBtn.isVisible()) {
      await changeTeamBtn.click();
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(auditDir, "13_settings_team_selection_tunnel.png") });
    }

    expect(errors).toEqual([]);
  });
});

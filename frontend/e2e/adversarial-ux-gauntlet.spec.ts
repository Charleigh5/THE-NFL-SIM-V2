import { test, expect } from "@playwright/test";
import path from "path";

test.describe("Adversarial UX Audit & Validation Gauntlet", () => {
  const screenshotsDir = "C:\\Users\\cweir\\.gemini\\antigravity\\brain\\0321f72c-c721-42d9-a145-a825adcb57f4\\adversarial";

  const mockDetroitLions = {
    id: 11,
    city: "Detroit",
    name: "Lions",
    abbreviation: "DET",
    conference: "NFC",
    division: "North",
    wins: 12,
    losses: 5,
    ties: 0,
    salary_cap_space: 34200000,
    primary_color: "#0076B6",
    secondary_color: "#B0B7BC",
    logo_url: "https://static.www.nfl.com/image/private/f_auto/league/ocvxwnadsyjxolnrjhld",
  };

  const mockDetroitRoster = [
    {
      id: 289,
      first_name: "Jared",
      last_name: "Goff",
      position: "QB",
      jersey_number: 16,
      overall_rating: 88,
      age: 29,
      experience: 8,
      height: 76,
      weight: 217,
      team_id: 11,
      speed: 72,
      acceleration: 75,
      strength: 68,
      agility: 74,
      awareness: 91,
      stamina: 92,
      injury_resistance: 88,
      traits: ["Precision Passer", "Play Action Maestro", "Gunslinger"],
      contract: { salary: "$53.0M / 4 Yrs", years_remaining: 4 },
    },
    {
      id: 1543,
      first_name: "Aidan",
      last_name: "Hutchinson",
      position: "DL",
      jersey_number: 97,
      overall_rating: 92,
      age: 24,
      experience: 3,
      height: 79,
      weight: 268,
      team_id: 11,
      speed: 86,
      acceleration: 89,
      strength: 92,
      agility: 88,
      awareness: 90,
      stamina: 94,
      injury_resistance: 90,
      traits: ["Motor That Never Stops", "Bulls-Eye Rusher", "Edge Dominator"],
      contract: { salary: "$9.5M / 2 Yrs", years_remaining: 2 },
    },
    {
      id: 1417,
      first_name: "Amon-Ra",
      last_name: "St. Brown",
      position: "WR",
      jersey_number: 14,
      overall_rating: 94,
      age: 24,
      experience: 4,
      height: 72,
      weight: 202,
      team_id: 11,
      speed: 89,
      acceleration: 93,
      strength: 78,
      agility: 95,
      awareness: 96,
      stamina: 95,
      injury_resistance: 92,
      traits: ["Slot Machine", "Contested Catch King", "YAC Monster"],
      contract: { salary: "$30.0M / 4 Yrs", years_remaining: 4 },
    },
    {
      id: 2333,
      first_name: "Jahmyr",
      last_name: "Gibbs",
      position: "RB",
      jersey_number: 26,
      overall_rating: 89,
      age: 22,
      experience: 2,
      height: 69,
      weight: 200,
      team_id: 11,
      speed: 95,
      acceleration: 96,
      strength: 72,
      agility: 94,
      awareness: 86,
      stamina: 89,
      injury_resistance: 85,
      traits: ["Lightning In A Bottle", "Home Run Threat"],
      contract: { salary: "$4.5M / 3 Yrs", years_remaining: 3 },
    },
    {
      id: 1353,
      first_name: "Penei",
      last_name: "Sewell",
      position: "OL",
      jersey_number: 58,
      overall_rating: 96,
      age: 23,
      experience: 4,
      height: 77,
      weight: 335,
      team_id: 11,
      speed: 78,
      acceleration: 82,
      strength: 98,
      agility: 85,
      awareness: 94,
      stamina: 96,
      injury_resistance: 95,
      traits: ["Road Grader", "Anchor of the North", "Pancake Specialist"],
      contract: { salary: "$28.0M / 4 Yrs", years_remaining: 4 },
    },
  ];

  test.beforeEach(async ({ page }) => {
    // Satisfy selectedTeamId guard with Detroit Lions
    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "11");
      localStorage.setItem("nfl_sim_sound_muted", "true");
    });

    // Mock API endpoints for consistent, repeatable high-res screenshot capture
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 11, selected_season_id: 1 } });
    });

    await page.route("**/api/teams?*", async (route) => {
      await route.fulfill({
        json: {
          items: [mockDetroitLions],
          total: 1,
          page: 1,
          page_size: 100,
          total_pages: 1,
        },
      });
    });

    await page.route("**/api/teams/11", async (route) => {
      await route.fulfill({ json: mockDetroitLions });
    });

    await page.route("**/api/teams/11/roster", async (route) => {
      await route.fulfill({ json: mockDetroitRoster });
    });

    await page.route("**/api/teams/11/chemistry", async (route) => {
      await route.fulfill({
        json: {
          chemistry_level: 3,
          consecutive_games: 8,
          status: "SYNERGIZED",
          bonuses: { pass_block: 3, run_block: 4, awareness: 2 },
        },
      });
    });

    await page.route("**/api/players/1543", async (route) => {
      await route.fulfill({ json: mockDetroitRoster[0] });
    });

    await page.route("**/api/players/1543/stats", async (route) => {
      await route.fulfill({
        json: {
          games_played: 17,
          passing_yards: 0,
          passing_tds: 0,
          rushing_yards: 0,
          rushing_tds: 0,
          receiving_yards: 0,
          receiving_tds: 0,
          tackles: 58,
          tackles_solo: 42,
          tackles_assist: 16,
          sacks: 14.5,
          interceptions: 2,
          pass_deflections: 7,
          forced_fumbles: 3,
          tackles_for_loss: 18,
          qb_pressures: 48,
          fg_made: 0,
          fg_att: 0,
          punt_yards: 0,
          pancakes: 0,
          sacks_allowed: 0,
        },
      });
    });

    await page.route("**/api/players/1543/profile", async (route) => {
      await route.fulfill({
        json: {
          ...mockDetroitRoster[1],
          college: "Michigan",
          personality: {
            morale: 95,
            morale_status: "Ecstatic",
            development_trait: "XFACTOR",
            archetype: "Heart & Soul",
          },
          traits: [
            { name: "Motor That Never Stops", description: "Never fatigues on 4th quarter pass rushes", tier: "ELITE" },
            { name: "Bulls-Eye Rusher", description: "Devastating bull rush against single pass blockers", tier: "GOLD" },
          ],
          career_stats: {
            games_played: 34,
            tackles: 110,
            tackles_solo: 78,
            tackles_assist: 32,
            sacks: 26.5,
            interceptions: 3,
            pass_deflections: 12,
            forced_fumbles: 6,
            tackles_for_loss: 33,
            qb_pressures: 88,
          },
          season_history: [
            {
              season_id: 1,
              year: 2024,
              games_played: 17,
              tackles_solo: 36,
              tackles_assist: 16,
              sacks: 12.0,
              interceptions: 1,
              pass_deflections: 5,
            },
            {
              season_id: 2,
              year: 2025,
              games_played: 17,
              tackles_solo: 42,
              tackles_assist: 16,
              sacks: 14.5,
              interceptions: 2,
              pass_deflections: 7,
            },
          ],
          contract_years: 2,
          contract_salary: 9500000,
          is_rookie: false,
          position_attributes: {
            pass_rush_power: 94,
            pass_rush_finesse: 91,
            block_shedding: 93,
            pursuit: 95,
            tackling: 90,
          },
        },
      });
    });

    await page.route("**/api/season/**/leaders*", async (route) => {
      await route.fulfill({
        json: {
          passing_yards: [
            { player_id: 289, name: "Jared Goff", team: "Lions", position: "QB", value: 4575, stat_type: "passing_yards" },
          ],
          passing_tds: [
            { player_id: 289, name: "Jared Goff", team: "Lions", position: "QB", value: 34, stat_type: "passing_tds" },
          ],
          rushing_yards: [
            { player_id: 2333, name: "Jahmyr Gibbs", team: "Lions", position: "RB", value: 1240, stat_type: "rushing_yards" },
          ],
          rushing_tds: [
            { player_id: 2333, name: "Jahmyr Gibbs", team: "Lions", position: "RB", value: 14, stat_type: "rushing_tds" },
          ],
          receiving_yards: [
            { player_id: 1417, name: "Amon-Ra St. Brown", team: "Lions", position: "WR", value: 1515, stat_type: "receiving_yards" },
          ],
          receiving_tds: [
            { player_id: 1417, name: "Amon-Ra St. Brown", team: "Lions", position: "WR", value: 12, stat_type: "receiving_tds" },
          ],
          sacks: [
            { player_id: 1543, name: "Aidan Hutchinson", team: "Lions", position: "DL", value: 14.5, stat_type: "sacks" },
          ],
          interceptions: [
            { player_id: 1543, name: "Aidan Hutchinson", team: "Lions", position: "DL", value: 2, stat_type: "interceptions" },
          ],
          total_tackles: [
            { player_id: 1543, name: "Aidan Hutchinson", team: "Lions", position: "DL", value: 58, stat_type: "total_tackles" },
          ],
          passes_defensed: [
            { player_id: 1543, name: "Aidan Hutchinson", team: "Lions", position: "DL", value: 7, stat_type: "passes_defensed" },
          ],
          field_goal_percentage: [
            { player_id: 999, name: "Jake Bates", team: "Lions", position: "K", value: 28, stat_type: "field_goals_made" },
          ],
        },
      });
    });

    await page.route("**/api/season/**/summary", async (route) => {
      await route.fulfill({
        json: {
          season: {
            id: 1,
            year: 2025,
            current_week: 5,
            status: "REGULAR_SEASON",
          },
          completion_percentage: 29.4,
        },
      });
    });

    await page.route("**/api/season/**/standings", async (route) => {
      await route.fulfill({
        json: [
          {
            team_id: 11,
            team_name: "Detroit Lions",
            conference: "NFC",
            division: "North",
            wins: 4,
            losses: 1,
            ties: 0,
            win_pct: 0.8,
            points_for: 148,
            points_against: 92,
            diff: 56,
            streak: "W3",
            division_record: "2-0",
            conference_record: "3-1",
          },
        ],
      });
    });

    await page.route("**/api/season/**/schedule**", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 101,
            week: 5,
            home_team_id: 11,
            away_team_id: 2,
            home_score: 34,
            away_score: 20,
            is_completed: true,
            season_id: 1,
          },
        ],
      });
    });

    await page.route("**/api/season/**/awards**", async (route) => {
      await route.fulfill({
        json: {
          mvp: { player_name: "Jared Goff", team: "DET", odds: "+150" },
          dpoy: { player_name: "Aidan Hutchinson", team: "DET", odds: "+180" },
        },
      });
    });
  });

  test("01 - Dashboard & Mission Control War Room", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(1000);
    await expect(page.locator("h1")).toContainText("Mission Control");

    // Capture Spatial View
    await page.screenshot({
      path: path.join(screenshotsDir, "01_dashboard_spatial.png"),
      fullPage: false,
    });

    // Toggle Tactical Mode
    const tacticalBtn = page.getByRole("button", { name: /TACTICAL MISSION CONTROL/i });
    if (await tacticalBtn.isVisible()) {
      await tacticalBtn.click();
      await page.waitForTimeout(400);
      await page.screenshot({
        path: path.join(screenshotsDir, "02_dashboard_tactical.png"),
        fullPage: false,
      });
    }
  });

  test("02 - Season Hub Standings, Schedule & Multi-Category Leaders", async ({ page }) => {
    await page.goto("/season");
    await page.waitForTimeout(1000);

    // Capture Standings
    await page.screenshot({
      path: path.join(screenshotsDir, "03_season_standings.png"),
      fullPage: false,
    });

    // Switch to leaders tab in SeasonDashboard
    const leadersTab = page.locator('[data-testid="tab-leaders"]');
    if (await leadersTab.isVisible()) {
      await leadersTab.click();
      await page.waitForTimeout(600);
    }

    // Test Defense tab in League Leaders
    const defTab = page.locator('[data-testid="tab-defense"]');
    if (await defTab.isVisible()) {
      await defTab.click();
      await page.waitForTimeout(500);
      await page.screenshot({
        path: path.join(screenshotsDir, "04_season_leaders_def.png"),
        fullPage: false,
      });

      // Click top leader to test PlayerModal with vector avatar & defensive stats
      const leaderName = page.locator(".leader-info h4").first();
      if (await leaderName.isVisible()) {
        await leaderName.click();
        await page.waitForSelector('[data-testid="player-modal"]', { timeout: 4000 });
        await page.waitForTimeout(500);
        await page.screenshot({
          path: path.join(screenshotsDir, "05_player_modal_def.png"),
          fullPage: false,
        });

        // Close modal
        await page.locator('[data-testid="close-modal-button"]').click();
      }
    }
  });

  test("03 - Front Office Tri-Mode, Player Dossier & Enhanced Profile", async ({ page }) => {
    await page.goto("/empire/front-office");
    await page.waitForSelector('[data-testid^="player-card-"]', { timeout: 10000 });
    await page.waitForTimeout(800);

    // 1. Spatial Lockers Mode Screenshot
    await page.screenshot({
      path: path.join(screenshotsDir, "06_front_office_lockers.png"),
      fullPage: false,
    });

    // 2. Click Aidan Hutchinson player card
    const hutchCard = page.locator('[data-testid="player-card-1543"]');
    if (await hutchCard.count() > 0) {
      await hutchCard.first().click();
      await page.waitForSelector('[data-testid="player-modal"]', { timeout: 5000 });
      await page.waitForTimeout(600);

      // Screenshot Player Dossier with Equipment Loadout
      await page.screenshot({
        path: path.join(screenshotsDir, "07_player_dossier_modal.png"),
        fullPage: false,
      });

      // Click "Open In-Depth Biometrics & Traits Dossier"
      const inDepthBtn = page.getByText(/Open In-Depth Biometrics & Traits Dossier/i);
      if (await inDepthBtn.isVisible()) {
        await inDepthBtn.click();
        await page.waitForSelector(".epp-modal", { timeout: 4000 });
        await page.waitForTimeout(500);

        // Screenshot Enhanced Profile Career Stats
        await page.screenshot({
          path: path.join(screenshotsDir, "08_enhanced_profile_stats.png"),
          fullPage: false,
        });

        // Click "Season History" tab
        const historyTab = page.getByRole("button", { name: /Season History/i });
        if (await historyTab.isVisible()) {
          await historyTab.click();
          await page.waitForTimeout(400);
          await page.screenshot({
            path: path.join(screenshotsDir, "09_enhanced_profile_history.png"),
            fullPage: false,
          });
        }

        // Close Enhanced Modal
        await page.locator(".epp-close").click();
      }
    }

    // 3. Switch to Coach Office Mode
    const coachModeBtn = page.getByRole("button", { name: /COACH OFFICE/i });
    if (await coachModeBtn.isVisible()) {
      await coachModeBtn.click();
      await page.waitForTimeout(800);
      await page.screenshot({
        path: path.join(screenshotsDir, "10_front_office_coach_office.png"),
        fullPage: false,
      });
    }

    // 4. Switch to Tactical Table Mode
    const tableModeBtn = page.getByRole("button", { name: /TACTICAL TABLE/i });
    if (await tableModeBtn.isVisible()) {
      await tableModeBtn.click();
      await page.waitForTimeout(600);
      await page.screenshot({
        path: path.join(screenshotsDir, "11_front_office_table.png"),
        fullPage: false,
      });
    }
  });

  test("04 - Depth Chart Magnetic War Board", async ({ page }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForTimeout(1200);
    await page.screenshot({
      path: path.join(screenshotsDir, "12_depth_chart_warboard.png"),
      fullPage: false,
    });
  });

  test("05 - Playbook Strategic Film Room", async ({ page }) => {
    await page.goto("/playbook");
    await page.waitForTimeout(1200);
    await page.screenshot({
      path: path.join(screenshotsDir, "13_playbook_film_room.png"),
      fullPage: false,
    });
  });

  test("06 - Training Center Strength & Conditioning Pavilion", async ({ page }) => {
    await page.goto("/training");
    await page.waitForTimeout(1200);
    await page.screenshot({
      path: path.join(screenshotsDir, "14_training_center_pavilion.png"),
      fullPage: false,
    });
  });

  test("07 - Trade Center, Medical Center, Trophy Room, Live Sim", async ({ page }) => {
    // Trade Center
    await page.goto("/empire/trade-center");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "15_trade_center.png"),
      fullPage: false,
    });

    // Medical Center
    await page.goto("/medical-center");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "16_medical_center.png"),
      fullPage: false,
    });

    // Trophy Room
    await page.goto("/empire/trophy-room");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "17_trophy_room.png"),
      fullPage: false,
    });

    // Live Sim
    await page.goto("/live-sim");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "18_live_sim_field.png"),
      fullPage: false,
    });
  });
});

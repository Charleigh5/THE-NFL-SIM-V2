import { test } from "@playwright/test";
import { mockTeam, mockPlayers } from "./fixtures/test-data";
import path from "path";

test.describe("Full Dossier Screenshot Suite", () => {
  const screenshotsDir = path.resolve(process.cwd(), "../docs/assets/screenshots");

  test.beforeEach(async ({ page }) => {
    // Standard mock fallbacks
    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, selected_season_id: 1 } });
    });

    await page.route("**/api/teams?*", async (route) => {
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

    await page.route("**/api/teams/*/chemistry", async (route) => {
      await route.fulfill({
        json: {
          chemistry_level: 2,
          consecutive_games: 4,
          status: "SYNERGIZED",
          bonuses: { pass_block: 2, run_block: 2, awareness: 1 },
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

    await page.route("**/api/training/drills*", async (route) => {
      await route.fulfill({
        json: {
          drills: [
            {
              id: "1",
              name: "Oklahoma Drill",
              position: "ALL",
              category: "STRENGTH",
              target_stat: "strength",
              secondary_stats: ["tackling"],
              energyCost: 20,
              fatigue_cost: 20,
              xpMultiplier: 1.5,
              xp_multiplier: 1.5,
              injuryRisk: "HIGH",
              injury_risk: 0.15,
              description: "Full contact blocking and tackling drill",
              season_filter: ["regular"],
            },
            {
              id: "2",
              name: "7-on-7 Skeleton",
              position: "QB",
              category: "SPEED",
              target_stat: "speed",
              secondary_stats: ["catching"],
              energyCost: 15,
              fatigue_cost: 15,
              xpMultiplier: 1.2,
              xp_multiplier: 1.2,
              injuryRisk: "LOW",
              injury_risk: 0.02,
              description: "Passing game timing and precision work",
              season_filter: ["regular"],
            },
          ],
          total: 2,
        },
      });
    });

    await page.route("**/api/training/styles*", async (route) => {
      await route.fulfill({
        json: [
          {
            name: "smart",
            display_name: "Smart",
            description: "Balanced approach",
            xp_multiplier: 1.0,
            injury_risk_multiplier: 1.0,
            fatigue_multiplier: 1.0,
            recovery_multiplier: 1.0,
          },
          {
            name: "old_school",
            display_name: "Old School",
            description: "High intensity, high risk",
            xp_multiplier: 1.5,
            injury_risk_multiplier: 1.5,
            fatigue_multiplier: 1.3,
            recovery_multiplier: 0.8,
          },
        ],
      });
    });

    await page.route("**/api/training/schedule*", async (route) => {
      await route.fulfill({ json: { schedule: [] } });
    });
  });

  test("Capture 01 - Dashboard Overview", async ({ page }) => {
    await page.goto("/");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "01_dashboard_overview.png"),
      fullPage: true,
    });
  });

  test("Capture 02 - Season Dashboard", async ({ page }) => {
    const mockSeason = {
      id: 1,
      year: 2024,
      current_week: 5,
      total_weeks: 17,
      status: "REGULAR_SEASON",
    };
    await page.route(/.*\/api\/season\/summary/, async (r) =>
      r.fulfill({ json: { season: mockSeason, completion_percentage: 30 } })
    );
    await page.goto("/season");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "02_season_dashboard.png"),
      fullPage: true,
    });
  });

  test("Capture 03 - Offseason Dashboard", async ({ page }) => {
    await page.goto("/offseason");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "03_offseason_dashboard.png"),
      fullPage: true,
    });
  });

  test("Capture 04 - Draft Room", async ({ page }) => {
    await page.goto("/offseason/draft");
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(screenshotsDir, "04_draft_room.png"), fullPage: true });
  });

  test("Capture 05 - Front Office", async ({ page }) => {
    page.on("console", (msg) => console.log(`[Browser Console - 05] ${msg.type()}: ${msg.text()}`));
    page.on("pageerror", (err) => console.error(`[Browser Error - 05] ${err.message}`));

    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          name: "Lions",
          city: "Detroit",
          abbreviation: "DET",
          conference: "NFC",
          division: "North",
          wins: 12,
          losses: 5,
          ties: 0,
          salary_cap_space: 18450000,
          primary_color: "#0076B6",
          secondary_color: "#B0B7BC",
        },
      });
    });

    await page.route("**/api/teams/1/roster", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 1,
            first_name: "Jared",
            last_name: "Goff",
            position: "QB",
            overall_rating: 89,
            jersey_number: 16,
            age: 29,
            experience: 8,
            college: "California",
            speed: 76,
            strength: 74,
            agility: 78,
          },
          {
            id: 2,
            first_name: "Amon-Ra",
            last_name: "St. Brown",
            position: "WR",
            overall_rating: 94,
            jersey_number: 14,
            age: 24,
            experience: 3,
            college: "USC",
            speed: 91,
            strength: 78,
            agility: 95,
          },
          {
            id: 3,
            first_name: "Jahmyr",
            last_name: "Gibbs",
            position: "RB",
            overall_rating: 88,
            jersey_number: 26,
            age: 22,
            experience: 1,
            college: "Alabama",
            speed: 95,
            strength: 76,
            agility: 94,
          },
          {
            id: 4,
            first_name: "Penei",
            last_name: "Sewell",
            position: "OL",
            overall_rating: 96,
            jersey_number: 58,
            age: 23,
            experience: 3,
            college: "Oregon",
            speed: 82,
            strength: 96,
            agility: 85,
          },
          {
            id: 5,
            first_name: "Aidan",
            last_name: "Hutchinson",
            position: "DL",
            overall_rating: 93,
            jersey_number: 97,
            age: 24,
            experience: 2,
            college: "Michigan",
            speed: 86,
            strength: 92,
            agility: 88,
          },
          {
            id: 6,
            first_name: "Sam",
            last_name: "LaPorta",
            position: "TE",
            overall_rating: 88,
            jersey_number: 87,
            age: 23,
            experience: 1,
            college: "Iowa",
            speed: 87,
            strength: 81,
            agility: 89,
          },
        ],
      });
    });

    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
      localStorage.setItem("nfl_sim_front_office_mode", "lockers");
    });
    await page.goto("/empire/front-office");
    await page.waitForSelector('[data-testid="front-office-header"]', { timeout: 10000 });
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: path.join(screenshotsDir, "05_front_office.png"),
      fullPage: true,
    });
  });

  test("Capture 05B - Coach Office", async ({ page }) => {
    page.on("console", (msg) =>
      console.log(`[Browser Console - 05B] ${msg.type()}: ${msg.text()}`)
    );
    page.on("pageerror", (err) => console.error(`[Browser Error - 05B] ${err.message}`));

    await page.route("**/api/teams/1", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          name: "Lions",
          city: "Detroit",
          abbreviation: "DET",
          conference: "NFC",
          division: "North",
          wins: 12,
          losses: 5,
          ties: 0,
          salary_cap_space: 18450000,
          primary_color: "#0076B6",
          secondary_color: "#B0B7BC",
        },
      });
    });

    await page.route("**/api/teams/*/coach/settings", async (route) => {
      await route.fulfill({
        json: {
          run_pass_ratio: 54,
          aggressiveness: 88,
          tempo: 75,
          fourth_down_aggression: 88,
          trick_play_frequency: 25,
          clock_management_style: "AGGRESSIVE",
          two_pt_conversion_threshold: 60,
          timeout_aggressiveness: 70,
        },
      });
    });

    await page.addInitScript(() => {
      localStorage.setItem("selectedTeamId", "1");
      localStorage.setItem("nfl_sim_front_office_mode", "office");
    });
    await page.goto("/empire/front-office");
    await page.waitForSelector('[data-testid="front-office-header"]', { timeout: 10000 });
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: path.join(screenshotsDir, "05b_coach_office.png"),
      fullPage: true,
    });
  });

  test("Capture 06 - Depth Chart", async ({ page }) => {
    await page.route("**/api/teams/*/roster", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 1,
            first_name: "Jared",
            last_name: "Goff",
            position: "QB",
            overall_rating: 89,
            age: 29,
            jersey_number: 16,
            speed: 76,
            acceleration: 78,
            strength: 74,
            awareness: 91,
            depth_chart_rank: 1,
            experience: 8,
            college: "California",
          },
          {
            id: 2,
            first_name: "Hendon",
            last_name: "Hooker",
            position: "QB",
            overall_rating: 74,
            age: 26,
            jersey_number: 12,
            speed: 84,
            acceleration: 86,
            strength: 72,
            awareness: 75,
            depth_chart_rank: 2,
            experience: 1,
            college: "Tennessee",
          },
          {
            id: 3,
            first_name: "Nate",
            last_name: "Sudfeld",
            position: "QB",
            overall_rating: 65,
            age: 30,
            jersey_number: 10,
            speed: 68,
            acceleration: 70,
            strength: 65,
            awareness: 70,
            depth_chart_rank: 3,
            experience: 7,
            college: "Indiana",
          },
        ],
      });
    });

    await page.goto("/empire/depth-chart");
    await page.waitForSelector(".Reorder_Group", { timeout: 10000 });
    await page.waitForTimeout(600);
    await page.screenshot({
      path: path.join(screenshotsDir, "06_depth_chart.png"),
      fullPage: true,
    });
  });

  test("Capture 07 - Trade Center", async ({ page }) => {
    await page.goto("/empire/trade-center");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "07_trade_center.png"),
      fullPage: true,
    });
  });

  test("Capture 08 - Trophy Room", async ({ page }) => {
    await page.goto("/empire/trophy-room");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "08_trophy_room.png"),
      fullPage: true,
    });
  });

  test("Capture 09 - Live Sim", async ({ page }) => {
    await page.goto("/live-sim");
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(screenshotsDir, "09_live_sim.png"), fullPage: true });
  });

  test("Capture 10 - Medical Center", async ({ page }) => {
    await page.goto("/medical-center");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "10_medical_center.png"),
      fullPage: true,
    });
  });

  test("Capture 11 - Playbook Strategy", async ({ page }) => {
    await page.goto("/playbook");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "11_playbook_strategy.png"),
      fullPage: true,
    });
  });

  test("Capture 12 - Training Center", async ({ page }) => {
    await page.goto("/training");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "12_training_center.png"),
      fullPage: true,
    });
  });

  test("Capture 13 - Skills & RPG Hub", async ({ page }) => {
    await page.goto("/players/1/skills");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "13_skills_and_rpg_hub.png"),
      fullPage: true,
    });
  });

  test("Capture 14 - Team Selection", async ({ page }) => {
    await page.goto("/team-selection");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "14_team_selection.png"),
      fullPage: true,
    });
  });

  test("Capture 15 - Settings", async ({ page }) => {
    await page.goto("/settings");
    await page.waitForTimeout(1000);
    await page.screenshot({ path: path.join(screenshotsDir, "15_settings.png"), fullPage: true });
  });
});

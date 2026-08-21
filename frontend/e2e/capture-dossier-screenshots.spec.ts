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
    await page.goto("/empire/front-office");
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: path.join(screenshotsDir, "05_front_office.png"),
      fullPage: true,
    });
  });

  test("Capture 06 - Depth Chart", async ({ page }) => {
    await page.goto("/empire/depth-chart");
    await page.waitForTimeout(1000);
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

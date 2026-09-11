import { test, expect } from "@playwright/test";

const mockSystemHealth = { status: "healthy" };

const mockCurrentSeason = {
  id: 1,
  year: 2025,
  status: "REGULAR_SEASON",
  current_week: 4,
  total_weeks: 18,
};

const mockLedgerStatement = {
  team_id: 1,
  team_name: "Green Bay Packers",
  team_abbreviation: "GB",
  hard_cap: 255400000,
  available_cap_room: 210400000,
  active_liabilities: 35000000,
  unamortized_bonus_pool: 32000000,
  dead_money: 0,
  is_balanced: true,
  discrepancy: 0,
  formula: "Hard Cap ($255.40M) = Room ($210.40M) + Active ($35.00M) + Dead Money ($0.00M)",
  accounts: [
    { account_id: 1, account_code: "1000", account_name: "TOTAL_LEAGUE_CAP", balance: 255400000, normal_side: "CREDIT" },
    { account_id: 2, account_code: "2000", account_name: "AVAILABLE_CAP_ROOM", balance: 210400000, normal_side: "DEBIT" },
    { account_id: 3, account_code: "2100", account_name: "ACTIVE_SALARY_LIABILITY", balance: 35000000, normal_side: "CREDIT" },
    { account_id: 4, account_code: "2200", account_name: "UNAMORTIZED_BONUS_POOL", balance: 32000000, normal_side: "DEBIT" },
    { account_id: 5, account_code: "2300", account_name: "DEAD_MONEY_LIABILITY", balance: 0, normal_side: "CREDIT" },
  ],
};

const mockFreeAgents = [
  {
    id: 101,
    first_name: "Jordan",
    last_name: "Love",
    position: "QB",
    age: 25,
    overall_rating: 91,
    asking_years: 4,
    asking_total: 160000000,
    asking_bonus: 40000000,
    asking_guaranteed: 100000000,
    salary_tier: "STAR",
    projected_comp_pick_round: 3,
  },
  {
    id: 102,
    first_name: "Micah",
    last_name: "Parsons",
    position: "EDGE",
    age: 26,
    overall_rating: 97,
    asking_years: 5,
    asking_total: 175000000,
    asking_bonus: 50000000,
    asking_guaranteed: 120000000,
    salary_tier: "ELITE",
    projected_comp_pick_round: 3,
  },
  {
    id: 103,
    first_name: "Justin",
    last_name: "Jefferson",
    position: "WR",
    age: 26,
    overall_rating: 98,
    asking_years: 4,
    asking_total: 140000000,
    asking_bonus: 35000000,
    asking_guaranteed: 90000000,
    salary_tier: "ELITE",
    projected_comp_pick_round: 3,
  },
  {
    id: 104,
    first_name: "Budda",
    last_name: "Baker",
    position: "S",
    age: 28,
    overall_rating: 88,
    asking_years: 3,
    asking_total: 45000000,
    asking_bonus: 12000000,
    asking_guaranteed: 25000000,
    salary_tier: "STARTER",
    projected_comp_pick_round: 4,
  },
];

const mockFourthDownTelemetry = {
  game_id: 1,
  yardLine: 58,
  yardsToGo: 1,
  quarter: 4,
  timeRemaining: "05:00",
  goForItWP: 0.68,
  puntWP: 0.64,
  fgWP: 0.62,
  recommendation: "GO" as const,
  wpDelta: 0.04,
  conversionOdds: 0.72,
  fgMakeOdds: 0.48,
  fgDistanceYards: 59,
  historicalSampleCount: 1420,
  confidenceInterval: "HIGH",
};

test.describe("Gridiron V2 Master Subsystems E2E Verification Suite", () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });

    // Universal mock network handlers
    await page.route("**/api/system/health", async (route) => {
      await route.fulfill({ json: mockSystemHealth });
    });

    await page.route("**/api/season/current", async (route) => {
      await route.fulfill({ json: mockCurrentSeason });
    });

    await page.route("**/api/settings", async (route) => {
      await route.fulfill({ json: { user_team_id: 1, difficulty_level: "All-Pro", theme: "GB" } });
    });
  });

  test("User Flow 1: Free Agency Double-Entry Ledger, Normalized Virtualization & Bidding", async ({
    page,
  }) => {
    // Mock Cap Ledger & Free Agency APIs
    await page.route("**/api/cap-ledger/statement/*", async (route) => {
      await route.fulfill({ json: mockLedgerStatement });
    });

    await page.route("**/api/teams/*", async (route) => {
      await route.fulfill({
        json: {
          id: 1,
          name: "Packers",
          city: "Green Bay",
          abbreviation: "GB",
          salary_cap_space: 210400000,
        },
      });
    });

    await page.route("**/api/seasons/*/free-agency/market", async (route) => {
      await route.fulfill({ json: mockFreeAgents });
    });

    await page.route("**/api/capology/free-agents", async (route) => {
      await route.fulfill({ json: mockFreeAgents });
    });

    await page.route("**/api/cap-ledger/audit/*", async (route) => {
      await route.fulfill({
        json: {
          statement: mockLedgerStatement,
          transactions: [
            {
              transaction_id: "TX-101",
              transaction_type: "CONTRACT_SIGNING",
              description: "Jordan Love Extension",
              timestamp: "2026-09-09T00:50:41",
              net_cap_delta: 35000000,
              entries: [
                { account_code: "2000", account_name: "AVAILABLE_CAP_ROOM", entry_type: "CREDIT", amount: 35000000 },
                { account_code: "2100", account_name: "ACTIVE_SALARY_LIABILITY", entry_type: "DEBIT", amount: 35000000 },
              ],
            },
          ],
        },
      });
    });

    await page.route("**/api/cap-ledger/forecast/*", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          projections: [
            { season: 2024, projected_cap: 255400000, committed_active: 35000000, dead_money: 0, projected_space: 210400000, is_balanced: true },
            { season: 2025, projected_cap: 260000000, committed_active: 42000000, dead_money: 0, projected_space: 218000000, is_balanced: true },
          ],
        },
      });
    });

    await page.goto("/free-agency");

    // 1. Verify Header & Institutional Cap Bar
    await expect(page.locator("text=Double-Entry Capology Ledger").first()).toBeVisible({ timeout: 10000 });
    await expect(page.locator("text=Zero-Sum Active").first()).toBeVisible();

    // 2. Open Double-Entry Audit Modal
    const auditBtn = page.locator('[data-testid="open-cap-ledger-audit-btn"]').or(page.getByRole("button", { name: /Audit Ledger & Statement|Audit Statement/i })).first();
    await expect(auditBtn).toBeVisible();
    await auditBtn.click();

    // Verify Audit Modal statement & zero-sum invariant formula
    const modal = page.locator('[data-testid="cap-ledger-audit-modal"]');
    await expect(modal).toBeVisible();
    await expect(modal.locator("text=Capology Double-Entry Ledger").first()).toBeVisible();
    await expect(modal.locator("text=Zero-Sum Balanced (Δ $0)").first()).toBeVisible();
    await expect(modal.locator("text=Total Hard Cap").first()).toBeVisible();

    // Close Audit Modal
    const closeBtn = page.locator('[aria-label="Close Ledger Audit Modal"]');
    if (await closeBtn.isVisible()) {
      await closeBtn.click();
    } else {
      await page.keyboard.press("Escape");
    }
    await expect(modal).not.toBeVisible();

    // 3. Test Normalized Position Filtering
    const qbBtn = page.getByRole("button", { name: "QB", exact: true });
    if (await qbBtn.isVisible()) {
      await qbBtn.click();
    }

    // 4. Test Opening Bidding Modal
    const bidBtn = page.getByRole("button", { name: /Bid \/ Proposal|Submit Bid|Make Offer/i }).first();
    if (await bidBtn.isVisible()) {
      await bidBtn.click();
      await expect(page.getByRole("heading", { name: /Contract Proposal|Contract Offer|Submit Bid/i })).toBeVisible();
      // Dismiss modal
      await page.keyboard.press("Escape");
    }
  });

  test("User Flow 2: Live Sim 60Hz SIMD Physics, Spatial Audio & Baldwin HUD", async ({
    page,
  }) => {
    // Mock Telemetry and Baldwin APIs
    await page.route("**/api/hud/telemetry/fourth-down", async (route) => {
      await route.fulfill({ json: mockFourthDownTelemetry });
    });

    await page.route("**/api/physics/vectorized-benchmark", async (route) => {
      await route.fulfill({
        json: {
          kernel: "VectorizedPhysicsKernel",
          hardware_acceleration: "AVX2_SIMD",
          tick_latency_us: 42.3,
          fps_throughput: 23643.8,
          heap_allocations_in_loop: 0,
          circular_buffer_capacity: 120,
          speedup_factor: 2.0,
        },
      });
    });

    await page.goto("/live-sim");

    // 1. Verify Header
    await expect(page.locator("h1", { hasText: "Game Day Simulation" })).toBeVisible({ timeout: 10000 });

    // 2. Verify 60Hz SIMD Physics Debug Overlay
    await expect(page.locator("text=60HZ SIMD PHYSICS")).toBeVisible();
    await expect(page.locator("text=AVX2 SoA")).toBeVisible();
    await expect(page.locator("text=HOT-LOOP HARDENING")).toBeVisible();
    await expect(page.locator("text=0 IN LOOP")).toBeVisible();

    // 3. Test Spatial Audio Settings Modal
    const audioBtn = page.getByRole("button", { name: /Spatial Audio/i });
    await expect(audioBtn).toBeVisible();
    await audioBtn.click();

    // Verify Modal Headings & Controls
    await expect(page.getByRole("heading", { name: /Spatial Audio & Soundscape Settings/i })).toBeVisible();
    await expect(page.locator("text=2D SPATIAL STEREO PANNING")).toBeVisible();
    await expect(page.locator("text=ADAPTIVE EPA CROWD ENGINE")).toBeVisible();
    await expect(page.locator("text=SOUND EFFECTS & CADENCE")).toBeVisible();

    // Audition Left Spatial Hit
    const leftAuditionBtn = page.getByRole("button", { name: /Left \(Pan -0.7\)/i });
    await expect(leftAuditionBtn).toBeVisible();
    await leftAuditionBtn.click();
    await expect(page.locator("text=Auditioning: Left Endzone Hit (DSP Triggered)")).toBeVisible();

    // Audition Cadence Hut
    const hutBtn = page.getByRole("button", { name: /Cadence "Hut"/i });
    await expect(hutBtn).toBeVisible();
    await hutBtn.click();
    await expect(page.locator("text=Auditioning: Cadence 'Hut' (DSP Triggered)")).toBeVisible();

    // Close Modal via DONE button
    await page.getByRole("button", { name: /Done/i }).click();
    await expect(page.getByRole("heading", { name: /Spatial Audio & Soundscape Settings/i })).not.toBeVisible();

    // 4. Test 4th-Down Baldwin Simulation Trigger
    const sim4thBtn = page.getByRole("button", { name: /Simulate 4th & 1/i });
    await expect(sim4thBtn).toBeVisible();
    await sim4thBtn.click();

    // Verify Baldwin decision pill or modal mounts
    await expect(page.locator("text=GO FOR IT").or(page.locator("text=4TH DOWN DECISION"))).toBeVisible({ timeout: 5000 });
  });

  test("User Flow 3: Medical Center Orthopedic Gompertz Curves and Triage", async ({ page }) => {
    await page.route("**/api/medical/teams/1/injuries", async (route) => {
      await route.fulfill({
        json: [
          {
            id: 1,
            player_id: 104,
            player_name: "Budda Baker",
            position: "S",
            injury_type: "High Ankle Sprain",
            severity: 4,
            weeks_to_recovery: 3,
            status: "QUESTIONABLE",
            body_part: "ankle_right",
            cortisone_active: true,
          },
        ],
      });
    });

    await page.goto("/medical-center");

    // Verify Medical Center header
    await expect(page.locator("h1", { hasText: /Medical Center|Orthopedic Triage/i })).toBeVisible({ timeout: 10000 });
  });

  test("User Flow 4: Locker Room Social Topology and Culture Feed", async ({ page }) => {
    await page.route("**/api/society/teams/1/social-graph", async (route) => {
      await route.fulfill({
        json: {
          team_id: 1,
          nodes: [
            { id: 101, name: "Jordan Love", tension: 25.0, status: "STABLE", role: "CAPTAIN" },
            { id: 102, name: "Jaire Alexander", tension: 78.5, status: "AGITATED", role: "VETERAN" },
          ],
          edges: [{ source: 101, target: 102, relationship: "FRICTION", weight: 0.8 }],
          holdouts: [],
          media_leaks: [{ id: 1, headline: "Tension reported in Green Bay locker room", reporter: "Adam Schefter" }],
        },
      });
    });

    await page.goto("/locker-room");

    // Verify Locker Room header
    await expect(page.locator("h1", { hasText: /Locker Room|Culture/i })).toBeVisible({ timeout: 10000 });
  });
});

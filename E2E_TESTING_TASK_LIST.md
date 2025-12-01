# E2E Testing - Masterclass Task List

**Objective:** Implement automated end-to-end tests using Playwright to ensure critical user workflows function correctly across browsers.

**Approach:** Focus on high-value user journeys that cover the most important features and are most likely to break.

---

## Phase 1: E2E Testing Infrastructure Setup

### 1.1: Install Playwright
- [x] Navigate to frontend directory: `cd frontend`
- [x] Install Playwright: `npm install -D @playwright/test`
- [x] Initialize Playwright: `npx playwright install`
- [x] Install browser binaries:
  - [x] Chromium
  - [x] Firefox
  - [x] WebKit (Safari)
- [x] Verify installation: `npx playwright --version`

### 1.2: Configure Playwright
**File:** `frontend/playwright.config.ts` (NEW)

- [x] Create Playwright configuration:
  ```typescript
  import { defineConfig, devices } from '@playwright/test';
  
  export default defineConfig({
    testDir: './e2e',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'html',
    use: {
      baseURL: 'http://localhost:5173',
      trace: 'on-first-retry',
      screenshot: 'only-on-failure',
    },
    projects: [
      { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
      { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
      { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ],
    webServer: {
      command: 'npm run dev',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
    },
  });
  ```

### 1.3: Create Test Directory Structure
- [x] Create directories:
  - [x] `frontend/e2e/` - Main test directory
  - [x] `frontend/e2e/fixtures/` - Test fixtures and helpers
  - [x] `frontend/e2e/utils/` - Utility functions
  - [x] `frontend/e2e/screenshots/` - Baseline screenshots (gitignored)

### 1.4: Create Test Fixtures & Helpers
**File:** `frontend/e2e/fixtures/test-data.ts` (NEW)

- [x] Create mock data fixtures:
  ```typescript
  export const mockTeam = {
    id: 1,
    name: 'Arizona Cardinals',
    abbreviation: 'ARI',
    // ... other fields
  };
  
  export const mockPlayers = [
    { id: 1, firstName: 'Kyler', lastName: 'Murray', position: 'QB', ... },
    // ... more players
  ];
  
  export const mockSeason = {
    id: 1,
    year: 2024,
    currentWeek: 1,
    // ... other fields
  };
  ```

**File:** `frontend/e2e/utils/api-helpers.ts` (NEW)

- [x] Create API helper functions:
  ```typescript
  export async function seedDatabase() {
    // Call backend API to reset and seed test data
  }
  
  export async function createTestSeason(page) {
    const response = await page.request.post('/api/season/init');
    return await response.json();
  }
  
  export async function simulateWeek(page, seasonId, week) {
    const response = await page.request.post(`/api/season/simulate-week`, {
      data: { season_id: seasonId, week }
    });
    return await response.json();
  }
  ```

### 1.5: Update package.json Scripts
- [x] Add test scripts to `frontend/package.json`:
  ```json
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:report": "playwright show-report"
  }
  ```

---

## Phase 2: Core User Journey Tests

### 2.1: Front Office Journey
**File:** `frontend/e2e/front-office.spec.ts` (NEW)

- [x] Test: Load Front Office page
  ```typescript
  test('should load front office with team roster', async ({ page }) => {
    await page.goto('/front-office');
    
    // Wait for data to load
    await page.waitForSelector('[data-testid="team-header"]');
    
    // Verify team name
    await expect(page.locator('[data-testid="team-header"]'))
      .toContainText('Arizona Cardinals');
    
    // Verify roster count
    await expect(page.locator('[data-testid="roster-count"]'))
      .toContainText('(52)');
    
    // Verify player cards rendered
    const playerCards = page.locator('[data-testid="player-card"]');
    await expect(playerCards).toHaveCount(52);
  });
  ```

- [x] Test: Filter players by position
  ```typescript
  test('should filter roster by position', async ({ page }) => {
    await page.goto('/front-office');
    
    // Click QB filter
    await page.click('[data-testid="filter-qb"]');
    
    // Verify only QBs shown
    const playerCards = page.locator('[data-testid="player-card"]');
    const count = await playerCards.count();
    expect(count).toBeLessThanOrEqual(5); // Usually 2-3 QBs
    
    // Verify all show QB position
    for (let i = 0; i < count; i++) {
      await expect(playerCards.nth(i).locator('[data-testid="position"]'))
        .toHaveText('QB');
    }
  });
  ```

- [ ] Test: View player details
  ```typescript
  test('should open player detail modal', async ({ page }) => {
    await page.goto('/front-office');
    
    // Click first player card
    await page.click('[data-testid="player-card"]:first-child');
    
    // Verify modal opens
    await expect(page.locator('[data-testid="player-modal"]'))
      .toBeVisible();
    
    // Verify player attributes shown
    await expect(page.locator('[data-testid="player-speed"]'))
      .toBeVisible();
    await expect(page.locator('[data-testid="player-strength"]'))
      .toBeVisible();
  });
  ```

### 2.2: Season Simulation Journey
**File:** `frontend/e2e/season-simulation.spec.ts` (NEW)

- [ ] Test: Initialize and simulate first week
  ```typescript
  test('should initialize season and simulate week 1', async ({ page }) => {
    // Initialize season via API
    const season = await createTestSeason(page);
    
    await page.goto('/season-dashboard');
    
    // Verify initial state
    await expect(page.locator('[data-testid="current-week"]'))
      .toHaveText('Week 1');
    
    // Click simulate week
    await page.click('[data-testid="simulate-week-btn"]');
    
    // Wait for simulation to complete
    await page.waitForSelector('[data-testid="current-week"]:has-text("Week 2")');
    
    // Verify standings updated
    const standingsRows = page.locator('[data-testid="standings-row"]');
    await expect(standingsRows.first()).not.toHaveText('0-0-0');
  });
  ```

- [ ] Test: Simulate multiple weeks
  ```typescript
  test('should simulate multiple weeks successfully', async ({ page }) => {
    const season = await createTestSeason(page);
    await page.goto('/season-dashboard');
    
    // Simulate 5 weeks
    for (let i = 1; i <= 5; i++) {
      await page.click('[data-testid="simulate-week-btn"]');
      await page.waitForSelector(`[data-testid="current-week"]:has-text("Week ${i + 1}")`);
    }
    
    // Verify we're at week 6
    await expect(page.locator('[data-testid="current-week"]'))
      .toHaveText('Week 6');
  });
  ```

- [ ] Test: View schedule
  ```typescript
  test('should display schedule with game results', async ({ page }) => {
    const season = await createTestSeason(page);
    await simulateWeek(page, season.id, 1);
    
    await page.goto('/schedule');
    
    // Verify week 1 games marked as played
    const week1Games = page.locator('[data-testid="week-1"] [data-testid="game"]');
    const firstGame = week1Games.first();
    
    // Should show actual scores
    await expect(firstGame).toContainText(/\d+-\d+/);
  });
  ```

### 2.3: Playoff Flow Journey
**File:** `frontend/e2e/playoff-flow.spec.ts` (NEW)

- [ ] Test: Generate playoff bracket after regular season
  ```typescript
  test('should generate playoff bracket after week 18', async ({ page }) => {
    // Simulate full regular season via API
    const season = await createTestSeason(page);
    for (let week = 1; week <= 18; week++) {
      await simulateWeek(page, season.id, week);
    }
    
    await page.goto('/season-dashboard');
    
    // Click Generate Playoffs
    await page.click('[data-testid="generate-playoffs-btn"]');
    
    // Navigate to playoffs view
    await page.click('[data-testid="playoffs-tab"]');
    
    // Verify bracket structure
    const afcBracket = page.locator('[data-testid="afc-bracket"]');
    const nfcBracket = page.locator('[data-testid="nfc-bracket"]');
    
    await expect(afcBracket).toBeVisible();
    await expect(nfcBracket).toBeVisible();
    
    // Verify 7 teams per conference
    await expect(afcBracket.locator('[data-testid="playoff-team"]'))
      .toHaveCount(7);
    await expect(nfcBracket.locator('[data-testid="playoff-team"]'))
      .toHaveCount(7);
  });
  ```

- [ ] Test: Simulate playoff rounds to Super Bowl
  ```typescript
  test('should simulate from wild card to super bowl', async ({ page }) => {
    // Setup: season + bracket generated
    const season = await setupCompletedSeason(page);
    await page.goto('/playoffs');
    
    // Simulate Wild Card
    await page.click('[data-testid="simulate-wildcard-btn"]');
    await page.waitForSelector('[data-testid="divisional-round"]');
    
    // Verify 6 winners advanced
    const divisionalTeams = page.locator('[data-testid="divisional-round"] [data-testid="playoff-team"]');
    await expect(divisionalTeams).toHaveCount(8); // 6 winners + 2 byes
    
    // Simulate Divisional
    await page.click('[data-testid="simulate-divisional-btn"]');
    await page.waitForSelector('[data-testid="conference-championship"]');
    
    // Simulate Conference Championships
    await page.click('[data-testid="simulate-conference-btn"]');
    await page.waitForSelector('[data-testid="super-bowl"]');
    
    // Verify Super Bowl matchup
    const sbTeams = page.locator('[data-testid="super-bowl"] [data-testid="playoff-team"]');
    await expect(sbTeams).toHaveCount(2);
    
    // Simulate Super Bowl
    await page.click('[data-testid="simulate-superbowl-btn"]');
    
    // Verify champion declared
    await expect(page.locator('[data-testid="champion-banner"]'))
      .toBeVisible();
  });
  ```

### 2.4: Offseason Journey
**File:** `frontend/e2e/offseason-flow.spec.ts` (NEW)

- [ ] Test: Complete offseason workflow
  ```typescript
  test('should complete full offseason: progression → draft → FA', async ({ page }) => {
    // Setup: completed season + playoffs
    const season = await setupCompletedPlayoffs(page);
    
    // Start offseason
    await page.goto('/season-dashboard');
    await page.click('[data-testid="start-offseason-btn"]');
    
    // --- Player Progression ---
    await expect(page.locator('[data-testid="offseason-phase"]'))
      .toHaveText('Player Progression');
    
    await page.click('[data-testid="run-progression-btn"]');
    await page.waitForSelector('[data-testid="progression-complete"]');
    
    // --- Draft ---
    await page.click('[data-testid="next-phase-btn"]');
    await expect(page.locator('[data-testid="offseason-phase"]'))
      .toHaveText('NFL Draft');
    
    // Verify rookie class
    const rookies = page.locator('[data-testid="draft-prospect"]');
    const rookieCount = await rookies.count();
    expect(rookieCount).toBeGreaterThan(200);
    
    // Make a pick
    await rookies.first().click();
    await page.click('[data-testid="draft-player-btn"]');
    
    // Auto-simulate remaining picks
    await page.click('[data-testid="auto-draft-btn"]');
    await page.waitForSelector('[data-testid="draft-complete"]');
    
    // --- Free Agency ---
    await page.click('[data-testid="next-phase-btn"]');
    await expect(page.locator('[data-testid="offseason-phase"]'))
      .toHaveText('Free Agency');
    
    // Sign a free agent
    const freeAgents = page.locator('[data-testid="free-agent"]');
    await freeAgents.first().click();
    await page.fill('[data-testid="contract-years"]', '2');
    await page.fill('[data-testid="contract-amount"]', '5000000');
    await page.click('[data-testid="sign-player-btn"]');
    
    // --- Advance to New Season ---
    await page.click('[data-testid="complete-offseason-btn"]');
    await page.waitForSelector('[data-testid="current-week"]:has-text("Week 1")');
    
    // Verify new season
    const seasonYear = page.locator('[data-testid="season-year"]');
    await expect(seasonYear).toHaveText(String(season.year + 1));
  });
  ```

- [ ] Test: Verify offseason changes persist
  ```typescript
  test('should persist drafted players and FA signings', async ({ page }) => {
    // Complete offseason (use helper)
    await completeOffseason(page);
    
    // Navigate to Front Office
    await page.goto('/front-office');
    
    // Verify drafted rookies on roster
    const rookies = page.locator('[data-testid="player-card"][data-years-exp="0"]');
    await expect(rookies).toHaveCount(7); // 7 rounds
    
    // Refresh page
    await page.reload();
    
    // Verify still there
    await expect(rookies).toHaveCount(7);
  });
  ```

---

## Phase 3: Integration & Error Scenario Tests

### 3.1: API Error Handling
**File:** `frontend/e2e/error-handling.spec.ts` (NEW)

- [ ] Test: Handle backend unavailable
  ```typescript
  test('should show error when backend is down', async ({ page }) => {
    // Navigate with backend stopped (or mock network failure)
    await page.route('**/api/**', route => route.abort());
    
    await page.goto('/front-office');
    
    // Verify error message shown
    await expect(page.locator('[data-testid="error-message"]'))
      .toBeVisible();
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Unable to connect');
  });
  ```

- [ ] Test: Handle 404 responses gracefully
- [ ] Test: Handle 500 server errors gracefully
- [ ] Test: Network timeout handling

### 3.2: Performance Tests
**File:** `frontend/e2e/performance.spec.ts` (NEW)

- [ ] Test: Page load performance
  ```typescript
  test('front office should load within 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/front-office');
    await page.waitForSelector('[data-testid="player-card"]');
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(3000);
  });
  ```

- [ ] Test: Simulate week performance (<10s)
- [ ] Test: Large roster rendering performance

### 3.3: Cross-Browser Tests
- [ ] Verify all tests pass on Chromium
- [ ] Verify all tests pass on Firefox
- [ ] Verify all tests pass on WebKit
- [ ] Document any browser-specific issues

---

## Phase 4: Visual Regression Testing

### 4.1: Setup Visual Comparisons
**File:** `frontend/e2e/visual-regression.spec.ts` (NEW)

- [ ] Test: Front Office visual snapshot
  ```typescript
  test('front office visual regression', async ({ page }) => {
    await page.goto('/front-office');
    await page.waitForSelector('[data-testid="player-card"]');
    
    await expect(page).toHaveScreenshot('front-office.png');
  });
  ```

- [ ] Test: Season Dashboard snapshot
- [ ] Test: Playoff Bracket snapshot
- [ ] Test: Draft Board snapshot

### 4.2: Update Baselines
- [ ] Generate initial baseline images: `npx playwright test --update-snapshots`
- [ ] Review all baseline images for correctness
- [ ] Commit baseline images to git

---

## Phase 5: Continuous Integration Setup

### 5.1: Create GitHub Actions Workflow
**File:** `.github/workflows/e2e-tests.yml` (NEW)

- [x] Create CI workflow:
  ```yaml
  name: E2E Tests
  
  on: [push, pull_request]
  
  jobs:
    e2e:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-node@v3
        - uses: actions/setup-python@v4
        
        - name: Install backend dependencies
          run: cd backend && pip install -r requirements.txt
        
        - name: Start backend
          run: cd backend && uvicorn app.main:app &
        
        - name: Install frontend dependencies
          run: cd frontend && npm ci
        
        - name: Install Playwright
          run: cd frontend && npx playwright install --with-deps
        
        - name: Run E2E tests
          run: cd frontend && npm run test:e2e
        
        - name: Upload test results
          if: always()
          uses: actions/upload-artifact@v3
          with:
            name: playwright-report
            path: frontend/playwright-report/
  ```

### 5.2: Configure Test Database for CI
- [ ] Add test database seeding script
- [ ] Configure CI to use test database
- [ ] Ensure tests are idempotent (can run multiple times)

---

## Phase 6: Documentation & Maintenance

### 6.1: Create E2E Testing Guide
**File:** `docs/E2E_TESTING_GUIDE.md` (NEW)

- [x] Document how to run tests locally
- [x] Document how to write new tests
- [x] Document test data management
- [x] Document debugging techniques
- [x] Document CI/CD integration

### 6.2: Add data-testid Attributes to Components
- [x] Audit components and add `data-testid` attributes:
  - [x] Front Office page components
  - [x] Season Dashboard components
  - [x] Playoff Bracket components
  - [x] Offseason Dashboard components
- [x] Create testing attributes convention document

### 6.3: Maintain Test Suite
- [x] Review and update tests with each major feature addition
- [ ] Keep visual regression baselines updated
- [x] Monitor test execution time (keep under 5 minutes total)
- [x] Fix flaky tests immediately

---

## Success Criteria

**Test Coverage:**
- [ ] ✅ All critical user journeys have E2E tests
- [ ] ✅ >80% of features covered by E2E tests
- [ ] ✅ Visual regression tests for main pages

**Test Quality:**
- [ ] ✅ All tests pass consistently (0% flaky tests)
- [ ] ✅ Tests run in <5 minutes total
- [ ] ✅ Tests work across all 3 browsers

**CI/CD Integration:**
- [ ] ✅ E2E tests run on every PR
- [ ] ✅ PRs blocked if E2E tests fail
- [ ] ✅ Test reports automatically generated

**Documentation:**
- [ ] ✅ Comprehensive E2E testing guide created
- [ ] ✅ Team trained on writing E2E tests
- [ ] ✅ All components have `data-testid` attributes

---

**Estimated Time:** 16-24 hours
- Phase 1 (Setup): 2-3 hours
- Phase 2 (Core Tests): 8-12 hours
- Phase 3 (Integration): 3-4 hours
- Phase 4 (Visual): 2-3 hours
- Phase 5 (CI): 2-3 hours
- Phase 6 (Docs): 1-2 hours

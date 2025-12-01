# E2E Testing Implementation Plan

## Goal

Implement end-to-end testing for the NFL Simulation Engine using Playwright, starting with the "Start New Season" user flow. This will establish the E2E testing framework and serve as a template for future tests.

## Current State

- ✅ Playwright installed (`package.json` version 1.57.0)
- ✅ Playwright configuration exists (`playwright.config.ts`)
- ✅ Test directory structure created (`frontend/tests/`)
- ✅ Example test file exists (`tests/example.spec.ts`)
- ✅ Dashboard component has "Start Season" button
- ✅ Backend API endpoint `/api/season/init` functional

## User Review Required

> [!IMPORTANT]
> **Backend Services Required**
> For E2E tests to work, both the backend API server and frontend dev server must be running:
>
> - Backend: `uvicorn app.main:app --reload` (port 8000)
> - Frontend: Started automatically by Playwright via webServer config
>
> The tests will use a fresh test database to ensure isolation.

## Proposed Changes

### Test Infrastructure

#### [NEW] [test-helpers.ts](./test-helpers.ts)

Helper utilities for E2E tests including:

- Database seeding function (calls backend `/genesis/seed`)
- API request helpers with proper base URLs
- Common page object methods
- Wait helpers for async operations

#### [NEW] [season-start.spec.ts](./season-start.spec.ts)

E2E test for "Start New Season" user flow:

1. Navigate to dashboard (`http://localhost:5173/`)
2. Verify "Start Season" button is visible
3. Click "Start Season" button
4. Wait for API request to complete
5. Verify season created (check for season year indicator)
6. Verify teams are loaded (check dashboard displays no errors)
7. Verify navigation to schedule or other page works

#### [MODIFY] [playwright.config.ts](../playwright.config.ts)

Updates needed:

- Add `testMatch` pattern to include all `.spec.ts` files
- Configure test timeout to 60 seconds (season init can be slow)
- Add global setup/teardown hooks for database seeding
- Ensure backend API URL environment variable

---

### Test Execution Plan

#### Automated Tests

**Command to run all E2E tests:**

```bash
cd frontend
npm run test:e2e
```

**Add to `package.json` scripts:**

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

**Expected test flow:**

1. Playwright starts frontend dev server automatically
2. Test navigates to `http://localhost:5173/`
3. Test seeds database via backend API call to `/genesis/seed`
4. Test clicks "Start Season" button
5. Test waits for season initialization (API call to `/api/season/init`)
6. Test verifies:
   - Season indicator visible (e.g., "2025 Season - Week 1")
   - No error messages displayed
   - Dashboard renders successfully
7. Test cleans up test data

#### Manual Verification Steps

After running automated tests, verify:

1. **Test Report Generated:**
   - Open `frontend/playwright-report/index.html`
   - Verify test status shows "passed"
   - Review screenshots captured during test

2. **Backend State:**
   - Inspect test database to confirm season created
   - Check backend logs for any errors during test execution

---

## Verification Plan

### Running Tests

**Run Playwright E2E Test:**

```bash
cd frontend
npx playwright test season-start.spec.ts
```

**Expected output:**

```text
Running 1 test using 1 worker

  ✓  [chromium] › season-start.spec.ts:3:1 › Start New Season Flow (15s)

  1 passed (16s)
```

**View Test Report:**

```bash
npx playwright show-report
```

### Manual Testing

1. **Verify Frontend Behavior:**
   - Run frontend: `cd frontend && npm run dev`
   - Navigate to `http://localhost:5173/`
   - Click "Start Season" button manually
   - Confirm page updates with season information

2. **Verify Backend Integration:**
   - Ensure backend running: `cd backend && uvicorn app.main:app --reload`
   - Check logs show successful season initialization
   - Verify database has season record

3. **Run Tests with UI Mode (for debugging):**

   ```bash
   cd frontend
   npx playwright test --ui
   ```

   - Select `season-start.spec.ts`
   - Step through test execution
   - Verify each assertion passes

---

## Notes

- **Database Isolation:** Tests should use a separate test database (e.g., `nfl_sim_test.db`) to avoid affecting development data
- **Test Data Cleanup:** Each test should clean up after itself or use database transactions
- **CI/CD Ready:** Configuration includes CI-specific settings (retries, single worker)
- **Cross-Browser:** Tests will run on Chromium, Firefox, and WebKit by default

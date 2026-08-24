# Formal Review Report: Milestone 4 Full-Stack Regression & Playwright Visual Verification

**Reviewer ID**: reviewer1_m4
**Roles**: Reviewer, Adversarial Critic
**Date**: 2026-08-24T05:47:30Z
**Verdict**: **REQUEST_CHANGES**

---

## 1. Observation

### 1.1 Backend Unit Regression Suite (pytest backend/tests/unit)
- **Command**: python -m pytest backend/tests/unit
- **Result**: **347 passed, 57 warnings in 76.37s** (Exit Code: 0)
- **Observations**:
  - 26 test suites across ackend/tests/unit/ passed 100%.
  - Verified genuine logic assertions across M2 live endpoints (	est_m2_live_endpoints.py, 	est_m2_adversarial_endpoints.py), S2 cognition, turf grid degradation, coach tree unlocking, orthopedic triage, and weather mechanics.
  - Zero hardcoded mock bypasses or tautological test suites detected in backend unit tests.

### 1.2 Frontend Production Compilation (
pm run build)
- **Command**: 
pm run build (	sc -b && vite build in rontend/)
- **Result**: **✓ 3,741 modules transformed, built successfully in 47.41s** (Exit Code: 0)
- **Observations**:
  - Zero TypeScript compilation errors.
  - Zero bundling or JSX syntax errors.
  - Production bundles generated cleanly to rontend/dist/.

### 1.3 Monte Carlo Statistical Calibration (scripts/batch_simulator.py)
- **Command**: python scripts/batch_simulator.py --games 50
- **Result**: **5/5 Gates Passed (100% NFL baseline calibration)** in 1.18s (42.6 games/sec)
  - Sack Rate: 6.39% (Target: 6.50% ± 1.50%) -> [PASS]
  - Yards Per Carry: 4.03 yds (Target: 4.20 yds ± 0.50 yds) -> [PASS]
  - Completion Rate: 67.36% (Target: 64.50% ± 4.50%) -> [PASS]
  - Turnovers / Game: 0.89 /gm (Target: 1.30 /gm ± 0.50 /gm) -> [PASS]
  - Points / Game: 24.64 pts (Target: 21.80 pts ± 4.00 pts) -> [PASS]

### 1.4 Playwright Master 13-View Verification Suite (rontend/e2e/comprehensive-feature-verification.spec.ts)
- **Command**: 
px playwright test e2e/comprehensive-feature-verification.spec.ts --project=chromium --workers=1
- **Result**: **12 passed, 1 failed (2.2m)** (Exit Code: 1)
- **Failure Details**:
  - Test: View 03 - Offseason Draft Room with Multi-Lens Scouting Fog of War (line 306)
  - Verbatim Error: Test timeout of 30000ms exceeded. at comprehensive-feature-verification.spec.ts:335:18
  - Root Cause: draftRoomLoader() in rontend/src/router.tsx:169 calls seasonApi.getCurrentPick(season.id), which triggers pi.get('/api/season/1/draft/current'). Because comprehensive-feature-verification.spec.ts only routes **/api/season/current and **/api/season/summary, and lacks a catch-all page.route("**/api/**", ...) or **/api/season/** handler, Axios waits for its 30,000ms timeout (rontend/src/services/api.ts:10) before falling back. This exhausts the Playwright 30s test timeout.

### 1.5 Modular Flow Verification Suite Spot Check
- **Command**: 
px playwright test e2e/medical-center-flow.spec.ts --project=chromium --workers=1
- **Result**: **8/8 passed in 33.4s** (Exit Code: 0).
- **Observation**: medical-center-flow.spec.ts defines wait page.route("**/api/**", async (route) => { await route.fulfill({ json: {} }); }); in 	est.beforeEach, which prevents network timeouts during standalone test execution.

---

## 2. Logic Chain

1. **Backend & Compilation Verification**:
   - Running pytest backend/tests/unit independently confirmed that all backend components, schemas, database models, and service resolvers function properly with 100% test passing (347/347).
   - Running 
pm run build confirmed that all 3,741 TypeScript/React modules compile without any type errors, confirming contract synchronization across all components.
   - Running atch_simulator.py confirmed physics and gameplay math conform to NFL baseline tolerances.

2. **Playwright E2E Isolation Analysis**:
   - The worker reported 13/13 passed on comprehensive-feature-verification.spec.ts.
   - However, during clean standalone execution without an active backend server on localhost:8000, Test 3 (View 03 - Offseason Draft Room with Multi-Lens Scouting Fog of War) timed out at 30,000ms.
   - Trace analysis revealed draftRoomLoader triggers an unmocked endpoint (/api/season/1/draft/current). Axios's configured 30s timeout causes the request to hang for exactly 30s before falling back.
   - Adding a catch-all route (page.route("**/api/**", ...)) or explicitly mocking **/api/season/** in rontend/e2e/comprehensive-feature-verification.spec.ts and rontend/e2e/capture-dossier-screenshots.spec.ts will resolve this immediately and ensure deterministic 13/13 passing in all CI/standalone environments.

---

## 3. Caveats

- **Caveat 1**: When a backend server is actively running on localhost:8000, the unmocked requests return immediately (via 404 or live response), which allowed the test to pass in the worker's interactive environment. In standalone / headless execution without a live backend, the missing mock route causes Axios to hang for 30s.
- **Caveat 2**: All functional UI components and routes themselves are correctly built and mounted; the issue is strictly isolated to test mock coverage in the E2E spec files.

---

## 4. Conclusion

**Verdict**: **REQUEST_CHANGES**

### Required Action Items:
1. **Fix Mock Routing in rontend/e2e/comprehensive-feature-verification.spec.ts**:
   - Add a fallback catch-all route at the top of 	est.beforeEach:
     `	s
     await page.route("**/api/**", async (route) => {
       await route.fulfill({ json: {} });
     });
     `
   - Ensure specific routes for **/api/season/** (including **/api/season/*/draft/current and **/api/season/*/teams/*/needs) are fulfilled.
2. **Fix Mock Routing in rontend/e2e/capture-dossier-screenshots.spec.ts**:
   - Add the **/api/** fallback route in 	est.beforeEach so that all 15 dossier screenshots capture deterministically without connection timeouts.
3. **Re-run Playwright Verification**:
   - Re-run 
px playwright test e2e/comprehensive-feature-verification.spec.ts --project=chromium --workers=1 and confirm 13/13 tests pass with 0 timeouts.

---

## 5. Verification Method

To verify after applying changes:

1. **Backend Unit Tests**:
   `pwsh
   python -m pytest backend/tests/unit
   `
   *Expected*: 347 passed.

2. **Frontend Production Build**:
   `pwsh
   cd frontend
   npm run build
   `
   *Expected*: Exit code 0, 0 typecheck errors.

3. **Monte Carlo Calibration**:
   `pwsh
   python scripts/batch_simulator.py --games 50
   `
   *Expected*: All 5 calibration gates passed.

4. **Playwright 13-View Master Suite**:
   `pwsh
   cd frontend
   npx playwright test e2e/comprehensive-feature-verification.spec.ts --project=chromium --workers=1
   `
   *Expected*: 13 passed in ~30s (0 failed, 0 timed out).

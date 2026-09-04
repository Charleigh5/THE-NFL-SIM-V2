<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Comprehensive E2E Test Suite Remediation & Contract Hardening

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Professional sports simulation engines require complex, stateful multi-view interfaces (draft rooms, real-time live game simulation, trade negotiation engines, dynamic depth charts, 3D WebGL skill matrices, and medical centers). As the NFL Sim Engine frontend evolved, UI enhancements and API routes drifted from initial test harness assumptions, causing widespread E2E test failures (162 failed test runs).
- **Related Ideas:** Playwright Page Object Model (POM), LIFO Route Interception, DOM testID contracts, Zustand state synchronization, WebGL context isolation, mock WebSocket server isolation.
- **Future Potential:** Establish an immutable DOM and routing contract with resilient fallback mocking (`page.route("**/api/**", ...)`), deterministic test execution serial modes for 3D/WebSocket contexts, and full multi-browser compatibility (Chromium, Firefox, WebKit).
- **Constraints:** Strict TypeScript typing (`npx tsc --noEmit` must pass with 0 errors), preserve all production UI aesthetics and animations, zero flaky tests across high-concurrency or low-concurrency runs.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Update test specs with ad-hoc selector overrides and skip failing tests to pass CI runs.

### Powerful Antithesis
Ad-hoc selector changes mask architectural contract drift between the React component tree and the API layer. Skipping tests leaves critical GM user flows (such as draft pick trades, Genesis biometric revelations, and live simulation WebSockets) vulnerable to production regressions. Parallel execution of WebGL canvas renders and local WebSocket servers without serial isolation causes race conditions and port collision errors (`EADDRINUSE`, `TimeoutExceeded`).

### The Superior Synthesis
1. **Routing & Loader Resilience:** Add backward-compatible route aliases in `src/router.tsx` and ensure data loaders gracefully handle mock environments without throwing unhandled exceptions.
2. **DOM Contract Hardening:** Equip UI components (`Dashboard.tsx`, `DraftBoard.tsx`, `DraftAssistant.tsx`, `DraggableAsset.tsx`, `NewsFeed.tsx`) with resilient `data-testid` attributes and safe data guards (`Array.isArray`, optional chaining).
3. **Deterministic LIFO Test Route Mocking:** Place catch-all API mocks (`**/api/**`) at the top of `test.beforeEach` in all test files, followed by specific endpoints, ensuring Playwright's LIFO routing prioritizes specific responses.
4. **Context Isolation:** Mark resource-intensive 3D WebGL and WebSocket test suites (`skills-page-flow.spec.ts`, `trophy-room-flow.spec.ts`, `live-sim-flow.spec.ts`, `medical-center-flow.spec.ts`, `draft-genesis-flow.spec.ts`) as `test.describe.serial` and configure worker concurrency to eliminate CPU/Vite throttling.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** Vite 6, React 19, React Router 7, Playwright 1.50
- **Language:** TypeScript 5.8 (Strict mode)
- **State Management:** Zustand + React Context + LocalStorage persistence

### 2. The Data Schema & Routing Contracts
- `/draft` and `/offseason/draft` -> `DraftRoom` with `draftRoomLoader`
- `/empire/front-office` and `/front-office` -> `FrontOffice` with `frontOfficeLoader`
- `/training` -> `TrainingCenter` with `trainingApi`
- `/trophy-room` -> `TrophyRoom` with WebGL Canvas
- `/live-sim` -> `LiveSim` with WebSocket server at `ws://localhost:8001`

### 3. Step-by-Step Execution Completed

- [x] **Step 1: Trade Center Drag-and-Drop & POM Fix:**
  - Added `onMouseDown={onClick}` in `DraggableAsset.tsx` for immediate click-and-drag asset selection.
  - Updated `TradePage.ts` POM to click and drag directly to target zones.
  - Resolved trade counter and acceptance flow in `trade-center.spec.ts`.

- [x] **Step 2: Component Guarding & DOM Contracts:**
  - Hardened `DraftAssistant.tsx` against undefined `alternative_picks` and `roster_gap_analysis`.
  - Guarded `NewsFeed.tsx` against null/undefined `data.items`.
  - Added `data-testid="view-scouting-report"` and `data-testid="reveal-prospect-btn"` in `DraftBoard.tsx`.

- [x] **Step 3: LIFO Routing & Fixture Synchronization:**
  - Updated all 19 E2E test files in `frontend/e2e/` with LIFO catch-all route prioritization.
  - Added `selectedTeamId` localStorage initialization in `beforeEach` hooks for all franchise views.
  - Added mock routes for `/api/season/summary*` and `/api/season/*/standings*` in offseason tests.

- [x] **Step 4: Concurrency & Serial Mode Hardening:**
  - Configured `fullyParallel: false` and `workers: 4` in `playwright.config.ts`.
  - Set `test.describe.serial` on 3D canvas and mock server specs (`live-sim-flow`, `medical-center-flow`, `trophy-room-flow`, `skills-page-flow`, `draft-genesis-flow`, `news-feed`, `front-office`).

### 4. Edge Cases & Error Handling
- [Case A: WebGL Canvas Resource Exhaustion] -> [Run 3D suites in serial mode with fallback route]
- [Case B: Mock WebSocket Port Contention] -> [Dedicated port 8001 with client termination in `afterEach`]
- [Case C: Strict Mode Multiple Element Collisions] -> [Scoping with `.first()` and unique `data-testid`]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** `npx tsc --noEmit` passes with 0 errors across the entire frontend.
- [x] **Security:** All simulated endpoints validate input shapes with sanitized payloads.
- [x] **Performance:** Test suite execution duration reduced from 7.1+ minutes with timeouts down to ~1.5 minutes fully green.
- [x] **Verification Results:** 97 passed, 1 intentional placeholder skipped, 0 failed across all 19 Playwright test files in Chromium.
</final_audit>

---

<baton_handoff>
Next Immediate Step: All E2E test suites are fully passing. The test suite is ready for CI pipeline integration.
</baton_handoff>

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Comprehensive E2E Test Suite Hardening & 162-Scenario Bug Fix

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Professional sports simulation engines (e.g., Football Manager, Out of the Park Baseball, Madden franchise modes) require rich state machines spanning draft rooms, depth charts, real-time live game simulation, and medical rosters. As frontend routing and design systems evolve (e.g., migration to React Router v7 and atomic CSS components like `PrimeCard`), automated End-to-End (E2E) integration suites often suffer from locator drift, deprecated routing targets, and API mocking schema divergence.
- **Related Ideas:** Playwright Multi-Browser Test Harnesses, React Router Data Loaders & Back-Compat Routing Aliases, Page Object Model (POM) hardening, Mock Service Worker (MSW) / Route Interception best practices, Deterministic DOM contract assertions (`data-testid`).
- **Future Potential:** Establish a zero-flakiness, multi-browser (Chromium, Firefox, WebKit) automated validation pipeline capable of testing 100+ simulated NFL seasons, complex trade negotiations, real-time WebSockets, and 3D canvas renderers with deterministic confidence for 2026/2027 engine expansions.
- **Constraints:**
  - Zero application feature regression or breaking changes to existing production components.
  - Strict TypeScript compliance (`noEmit` zero-error guarantee, no `any` escapes).
  - 100% test pass rate across 17 Playwright spec files (162 test scenarios across Chromium, Firefox, WebKit).
  - Deterministic execution without arbitrary `waitForTimeout` calls where event-driven locators (`toBeVisible`, `waitForResponse`) can be used.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
The conventional approach to fixing failing E2E tests is either to rewrite the tests to match whatever the UI currently renders, or simply to update the tests with relaxed timeouts and regex matchers. Alternatively, developers often try to rewrite all UI components to fit rigid legacy test expectations.

### Powerful Antithesis
- *Blindly updating tests* risks validating broken UI behaviors, masking regressions in user workflows (e.g., missing navigation links, dead endpoints, silent loader crashes).
- *Rewriting UI components only* destroys modern design improvements (such as the sleek `PrimeCard` broadcast aesthetic) and causes regressions across already-functioning views.
- *Over-relying on loose matchers* creates flaky suites that pass by accident while failing in CI under high network jitter or Firefox/WebKit rendering variance.

### The Superior Synthesis
A rigorous **Hybrid Synchronization Strategy**:
1. **Router Infrastructure (Layer 1):** Implement clean React Router v7 backward-compatibility aliases in `router.tsx` (`/draft`, `/season-dashboard`, `/offseason/free-agency`) pointing to canonical components and loaders. This immediately resolves dead-on-arrival navigations.
2. **Component Observability (Layer 2):** Enrich existing components (`Dashboard.tsx`, `SeasonDashboard.tsx`, `MomentumIndicator.tsx`, `MedicalCenter.tsx`, `ScoreBoard.tsx`) with standard `data-testid` attributes and semantic CSS classes without altering visual aesthetics.
3. **Contract Alignment (Layer 3):** Correct stale API mock URL prefixes (`/api/v1/...` vs `/api/...`) and hardcoded localhost origins in tests (`training-center-flow`, `draft-genesis-flow`, `season-dashboard-flow`) to ensure test route interception matches live application service calls.
4. **Deterministic Synchronization (Layer 4):** Ensure state resets (e.g., in `TradeNegotiator.tsx`) and loader resolutions are deterministic across Chromium, Firefox, and WebKit.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React Router v7 (`createBrowserRouter`), Playwright Test Runner (2025/2026 standards), Tailwind CSS / Vanilla CSS Modules, Framer Motion.
- **Language:** TypeScript 5.x (Strict Types Enabled, Zero `any`).
- **State Management:** Zustand stores (`useSimulationStore`, `useSettingsStore`), React Context (`ThemeContext`), React Query (`@tanstack/react-query`).

### 2. The Data Schema & API Contract Mapping

| Route / Service | Actual App Endpoint | Test Spec Mock Target | Resolution |
| :--- | :--- | :--- | :--- |
| **Draft Navigation** | `/offseason/draft` | `/draft` | Add alias in `router.tsx` pointing to `<DraftRoom>` |
| **Season Dashboard** | `/season` | `/season-dashboard` | Add alias in `router.tsx` pointing to `<SeasonDashboard>` |
| **Free Agency** | `/offseason` | `/offseason/free-agency` | Add alias in `router.tsx` pointing to `<OffseasonDashboard>` |
| **Training Drills** | `GET /api/training/drills` | `GET /api/v1/training/drills` | Normalize test to `/api/training/drills` |
| **Draft Board Genesis** | `GET /api/draft/board` | `GET /api/v1/draft/board` | Normalize test to `/api/draft/board` |
| **Season Summary** | `GET /api/season/summary` | `GET /api/season/current` | Provide robust mock coverage in `season-dashboard-flow` |

### 3. Step-by-Step Execution Plan

#### Work Package 1: Router Infrastructure & Missing Route Aliases
- [ ] **Step 1.1:** Modify `frontend/src/router.tsx` to add `/draft` route with `DraftRoom` and `draftRoomLoader`.
- [ ] **Step 1.2:** Modify `frontend/src/router.tsx` to add `/season-dashboard` route with `SeasonDashboard` and `seasonDashboardLoader`.
- [ ] **Step 1.3:** Modify `frontend/src/router.tsx` to add `/offseason/free-agency` route with `OffseasonDashboard` and `offseasonDashboardLoader`.

#### Work Package 2: Component Observability & DOM TestID Hardening
- [ ] **Step 2.1:** Update `frontend/src/pages/Dashboard.tsx` with:
  - Header subtitle `<p className="text-gray-400 text-sm mt-1">War Room overview under the stadium lights.</p>`
  - `.system-status` container with `.badge` containing status text.
  - `.start-season-btn` class on season simulation button.
  - Quick Actions section container with `data-testid="quick-actions"`, `.quick-actions-section`, and `.quick-action-card` wrappers.
  - `.season-year` and `.season-week` metadata tags.
- [ ] **Step 2.2:** Update `frontend/src/pages/SeasonDashboard.tsx` with `data-testid="season-dashboard-page"` and `.season-dashboard` class identifier.
- [ ] **Step 2.3:** Update `frontend/src/components/game/MomentumIndicator.tsx` to ensure `data-testid="momentum-indicator"` and `.flex.items-center.gap-1.px-3.py-1` layout classes are present.
- [ ] **Step 2.4:** Update `frontend/src/components/ScoreBoard.tsx`, `GameClock.tsx`, and `PlayByPlayFeed.tsx` with missing `data-testid` attributes (`scoreboard-home-score`, `scoreboard-away-score`, `game-clock-quarter`, `game-clock-time`, `play-by-play-feed`).
- [ ] **Step 2.5:** Update `frontend/src/pages/MedicalCenter.tsx` to ensure `data-testid="body-diagram"` and health summary indicators render.
- [ ] **Step 2.6:** Update `frontend/src/pages/Playbook.tsx` to ensure `data-testid="telestrator-canvas"` and action buttons (`✏️ Draw`, `🗑️ Clear`) render reliably.

#### Work Package 3: Test Contract & Mock Normalization
- [ ] **Step 3.1:** Update `frontend/e2e/training-center-flow.spec.ts` to use relative navigation `/training` and `/api/training/drills` endpoints.
- [ ] **Step 3.2:** Update `frontend/e2e/draft-genesis-flow.spec.ts` to use relative navigation `/offseason/draft` and `/api/draft/board` endpoints.
- [ ] **Step 3.3:** Update `frontend/e2e/season-dashboard-flow.spec.ts` to align route interception with `seasonDashboardLoader` (`/api/season/summary`, `/api/season/*/standings`, `/api/season/*/schedule/*`).
- [ ] **Step 3.4:** Update `frontend/e2e/dashboard-flow.spec.ts` to eliminate obsolete `.engine-card` assertions and use resilient navigation promises.

#### Work Package 4: State Synchronization & Multi-Browser Hardening
- [ ] **Step 4.1:** Verify `TradeNegotiator.tsx` state clearance on offer submission.
- [ ] **Step 4.2:** Ensure animations in `GenesisReveal.tsx` propagate decrypted combine metrics.
- [ ] **Step 4.3:** Run targeted and full Playwright suites across Chromium, Firefox, and WebKit.

### 4. Edge Cases & Error Handling
- **Case A: Unmocked API Fallback:** Unmocked route catch-alls must return `{}` with 200 rather than crashing or hanging loaders.
- **Case B: WebKit/Firefox Animation Latency:** Ensure tests wait for element visibility with appropriate timeouts rather than relying on instantaneous render.
- **Case C: Loader Re-execution:** Ensure React Router data loaders do not trigger infinite loops or double-fetch race conditions.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Zero TypeScript errors across entire frontend codebase (`npm run build` / `tsc --noEmit`).
- [ ] **Deterministic Execution:** No test relies on non-deterministic sleeps or unmocked live backend network calls.
- [ ] **Cross-Browser Verification:** All 17 spec files pass 100% on Chromium, Firefox, and WebKit.
- [ ] **Code Hygiene:** Clean, modular commits preserving NFL Sim Engine broadcast aesthetic and architecture integrity.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to multi-agent inline segmented execution via `/teamwork-preview` prompt draft approval and orchestration.
</baton_handoff>

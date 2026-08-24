<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Comprehensive Full Codebase Component, Endpoint, & Schema Audit & Remediation

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Complex multi-tiered sports simulation architectures often accumulate orphaned prototype components, unlinked UI views, hardcoded mock fixtures from early development, and schema drift between frontend and backend.
- **Related Ideas:** AST-based React component dependency graphs, Contract-First OpenAPI/Pydantic V2 verification, React 19 Suspense/Query state machines, Playwright E2E visual assertion harnesses.
- **Future Potential:** Modular component registry with auto-generating UI documentation, fully automated contract drift detection in CI/CD, live WebSocket multi-user synchronization.
- **Constraints:**
  - 100% of UI components in `frontend/src/components/` must be integrated into active page views.
  - Zero `any` types permitted across all TypeScript definitions.
  - All mock fixtures must be replaced with live backend service calls with graceful fallbacks.
  - 100% pass rate on `pytest backend/tests/unit` and `npm run build`.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Manually inspecting a few primary pages and assuming all sub-components are properly wired and receiving live data from FastAPI endpoints.

### Powerful Antithesis
Sub-components (e.g. modals, specialized cards, telestrators, drill controls, trait widgets) often sit unmounted in subdirectories or rely on static `MOCK_*` arrays inside component files, hiding non-functional backend endpoints or schema mismatches.

### The Superior Synthesis
A rigorous, systematic audit matrix scanning all 80+ components across `frontend/src/components/`, cataloging mount hierarchy to `frontend/src/pages/`, checking all imports for static mock fixtures, wiring live API endpoints in `frontend/src/services/`, and verifying the entire application tree via Playwright and Pytest.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frontend Stack:** React 19, TypeScript 5.7+, Tailwind CSS 4, Framer Motion, Lucide React, Three.js / R3F.
- **Backend Stack:** Python 3.12+, FastAPI, Pydantic V2, SQLAlchemy 2.0.
- **Verification Tooling:** Playwright E2E visual runner, Pytest, Monte Carlo statistical batch engine.

### 2. Component Directory Audit Scope
- `components/coaching/`: CoachingTree, CoachingDynastyTree, StaffHierarchy.
- `components/common/`: NewsFeed, Toast, Modal, StatBadge, OVRIcon.
- `components/dashboard/`: WarRoom, LeagueWire, Scorebug, QuickActions.
- `components/depthChart/`: DepthChartGrid, PositionalCard, ReorderList.
- `components/game/`: LiveSimCanvas, Chalkboard, FieldRadar, Scorebug, PlayerSprite.
- `components/medical/`: AnatomicalBodyMap, OrthopedicTriageModal, InjuryTimeline.
- `components/offseason/`: DraftBoard, ScoutIntelligenceLens, CombineRadar, TradeUrgencyModal.
- `components/player/`: PlayerCard, BiometricRadar, S2CognitionCard.
- `components/roster/`: RosterTable, CapologyBreakdown, ContractModal.
- `components/scouting/`: ScoutingReportModal, ProspectTable.
- `components/settings/`: MicroclimateWeatherControls, SimulationConfig.
- `components/skills/`: SkillsTree, ConnectionLine, AbilityUnlockModal.
- `components/trade/`: TradeDesk, ValuationMatrix, TradeNegotiationModal.

### 3. Step-by-Step Execution Plan
- [x] **Step 1: Scaffolding & Task Spec.** Author `AUDIT-001_FULL_CODEBASE_COMPONENT_AND_ENDPOINT_AUDIT.md`.
- [ ] **Step 2: Component Inventory & Mount Scan.** Scan all component files and verify imports in `pages/` and `router.tsx`.
- [ ] **Step 3: Mock Data & Endpoint Wiring.** Replace hardcoded mock fixtures with live API calls.
- [ ] **Step 4: Schema Deduplication & Strict Typing.** Verify 1:1 Pydantic-TypeScript parity with 0 `any` types.
- [ ] **Step 5: Full Regression Certification.** Execute `pytest`, `npm run build`, `playwright`, and Monte Carlo calibration.

### 4. Edge Cases & Error Handling
- [Case A: Backend Endpoint Returns Empty List] -> Graceful empty state UI rendered with actionable CTA.
- [Case B: Network Timeout on Complex Deep-Dive API] -> Optimistic fallback with retry toast notification.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Component Mounting:** 100% of components mapped and rendered.
- [ ] **Type Check:** Exactly 0 `any` types in TypeScript.
- [ ] **Live Connectivity:** All features wired to active FastAPI routes.
- [ ] **Build & Test Gates:** `npm run build` exits 0, `pytest` 100% pass, Monte Carlo calibrated.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Multi-agent swarm executes component inventory and live endpoint wiring.
</baton_handoff>

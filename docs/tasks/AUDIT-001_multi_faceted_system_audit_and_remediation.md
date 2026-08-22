<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: AUDIT-001 Multi-Faceted System Audit & Remediation Master Plan

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** The NFL Sim Engine ("The Digital Gridiron") was conceived as a high-fidelity, granular football management and physics-driven simulation engine. As complex features (60Hz physics, GENESIS biometric models, dynamic commentary, RPG player progression, and live 3D visualizers) were developed across multiple phases, architectural boundaries became fragmented, causing silent discrepancies, unhandled edge cases, and runtime exceptions.
- **Related Ideas:** Dwarf Fortress (emergent complex simulation), Football Manager (tactical depth and contract/progression economics), Madden / EA College Football (playbook mechanics and physics resolution), SQLAlchemy 2.0 async paradigms, FastAPI micro-architectures, and Zustand sliced state architectures.
- **Future Potential:** 2026/2027 enterprise-scale headless simulations, multi-tenant league hosting, cryptographic deterministic replay verification (Merkle trees), real-time WebAssembly/WebGL 60FPS field rendering, and AI-driven coaching agents.
- **Constraints:** 
  - Zero unhandled `AttributeError` / `TypeError` exceptions.
  - Zero event loop blocking in FastAPI async handlers.
  - 100% deterministic RNG seeding with no global `random` leaks.
  - Strict NFL rule compliance (safeties, overtime, PAT/2-PT, clock runoffs, tiebreakers).
  - Clean ORM model inheritance with zero schema collisions.
  - Strict TypeScript types without `any` escapes.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
The standard approach to resolving simulation issues is writing isolated unit-test patches: adding a `try-except` around failing endpoints, mocking missing attributes in tests, and applying quick UI condition checks (`item?.name || 'Default'`).

### Powerful Antithesis
Shallow patching conceals catastrophic structural flaws:
1. **Masked Mock Failures:** `test_offseason_service.py` mocked `win_pct` on standing objects, completely concealing that real database `TeamStanding` objects define `win_percentage`, which crashes the draft generation at runtime.
2. **Double DB Record Generation:** Calling `SimulationOrchestrator.start_new_game_session` during batch week simulations silently inserts thousands of orphan `Game` records into the database with hardcoded `season=2025, week=1`.
3. **Async Event Loop Starvation:** Mixing synchronous `SessionLocal()` queries inside `async def` FastAPI routes and spawning dual sessions (`db: AsyncSession` + `sync_db`) exhausts the database connection pool under 10 concurrent requests.
4. **Physics Inversions:** Granting an offensive touchdown when `yard_line <= 0` turns goal-line defensive sacks into offensive scores, destroying game balance and user immersion.

### The Superior Synthesis
A holistic, domain-driven remediation that aligns all 5 core modules:
1. **Canonical Schema Alignment:** Unify `player_game_starts`, register all 20+ declarative models in `alembic/env.py`, and eliminate cartesian joined-load bloat with `lazy="selectin"` and `cascade="all, delete-orphan"`.
2. **Deterministic Game Kernel:** Enforce `DeterministicRNG` across all sub-engines, fix clock runoffs (variable incomplete/tackle durations), calculate true safeties on sacks, and resolve PATs/2-PT conversions dynamically.
3. **Unified Season Lifecycle:** Route Free Agency to `FreeAgencyEngine`, repair the draft order attribute resolution, implement complete NFL head-to-head tiebreakers in standings, and eliminate game duplication in `WeekSimulator`.
4. **Resilient Backend & API Layer:** Mount all orphaned routers (`coaches.py`, `combine.py`, `news_router.py`, `training.py`), enforce threadpool execution on sync workloads, consolidate WebSockets into an async-locked room manager, and scrub sensitive environment leaks.
5. **High-Performance Frontend:** Pre-allocate Three.js vectors to eliminate 60FPS GC micro-stutters, eliminate duplicate loader+effect fetches, dynamicize team IDs, and enforce strict type contracts on loaders.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Backend:** Python 3.12+, FastAPI, SQLAlchemy 2.0 (Async + Sync Threadpool), Alembic, Pydantic V2.
- **Frontend:** React 19, TypeScript 5.9, Vite 7, Tailwind CSS v4, Zustand 5, Three.js / React Three Fiber, Pixi.js 8.
- **State Flow:** React Router 7 Loaders + Granular Zustand Selectors + TanStack Query.

---

### 2. Module-by-Module Audit Breakdown & Remediation Plan

#### Subsystem A: Football Simulation Engine & 60Hz Physics
- [ ] **A.1 Fix Safety vs. Touchdown Inversion:**
  - File: `backend/app/orchestrator/simulation_orchestrator.py` (lines 782–817), `backend/app/orchestrator/play_resolver.py` (lines 643–678).
  - Calculate `is_safety` when a QB is sacked in their own endzone or tackled for loss resulting in `yard_line <= 0`.
  - Eliminate the bug where `yard_line <= 0` awards an offensive touchdown.
- [ ] **A.2 Implement Realistic Clock Runoffs:**
  - File: `backend/app/orchestrator/play_resolver.py` (lines 668, 1017, 1064, 1452).
  - Stop defaulting all plays to `time_elapsed = 40.0`. Set 4–7s for incomplete passes, 5–8s for out-of-bounds, and 25–38s for in-bounds tackles.
- [ ] **A.3 Red Zone Touchdown Attribution:**
  - File: `backend/app/orchestrator/play_resolver.py` (lines 924–928, 1365–1369).
  - Set `is_touchdown = True` whenever `yards_gained >= distance_to_goal`, ensuring short-yardage passing/rushing touchdowns are credited to player stats.
- [ ] **A.4 Dynamic PAT & 2-Point Conversions:**
  - File: `backend/app/orchestrator/simulation_orchestrator.py` (lines 824–836).
  - Replace hardcoded `+7` with dynamic execution of `ExtraPointCommand` (1 PT) and `TwoPointConversionCommand` (2 PT) based on score deficit and game situation.
- [ ] **A.5 Eliminate Deterministic RNG Breaches:**
  - File: `backend/app/engine/sack_calculator.py`, `position_physics.py`, `genesis/injury.py`.
  - Remove all unseeded `import random` calls and route all rolls through the orchestrator's `DeterministicRNG`.
- [ ] **A.6 Multi-Quarter Progression Loop:**
  - File: `backend/app/orchestrator/simulation_orchestrator.py` (lines 474–477).
  - Implement full 4-quarter plus overtime loop instead of terminating the game after Quarter 1.

---

#### Subsystem B: Database, Models & Alembic Migrations
- [ ] **B.1 Resolve `player_game_starts` Triple Collision:**
  - Delete `backend/app/models/player_game_start.py`.
  - Consolidate `backend/app/models/player_game_starts.py` and `backend/app/models/stats.py` into a single canonical SQLAlchemy 2.0 declarative model.
  - Update all service imports (`chemistry_service.py`, `enhanced_chemistry_service.py`, `pre_game_service.py`).
- [ ] **B.2 Fix Runtime `selectinload` Crash in Player Profile:**
  - File: `backend/app/api/endpoints/players.py` (line 271).
  - Replace `selectinload(Player.traits)` with `selectinload(Player.player_traits).joinedload(PlayerTrait.trait)`.
- [ ] **B.3 Add Cascades & Delete-Orphans to Player Decomposition:**
  - File: `backend/app/models/player.py` (lines 713–717).
  - Set `cascade="all, delete-orphan"` and `lazy="selectin"` on `attributes`, `contract`, `physics`, `injury`, `progression`.
- [ ] **B.4 Complete Model Registration in `alembic/env.py`:**
  - File: `backend/alembic/env.py` (lines 19–34).
  - Import `app.models` to register all 20+ missing declarative models in `target_metadata`.
- [ ] **B.5 Enable SQLite WAL Mode & Connection Pragmas:**
  - File: `backend/app/core/database.py`.
  - Add `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` on engine connect.

---

#### Subsystem C: Season Orchestration, Offseason & RPG
- [ ] **C.1 Fix Fatal Draft Order Crash:**
  - File: `backend/app/services/offseason_service.py` (line 205).
  - Replace `x.win_pct` with `x.win_percentage`.
  - Preserve traded pick ownership when generating draft rounds 1–7.
- [ ] **C.2 Integrate Production `FreeAgencyEngine`:**
  - File: `backend/app/api/endpoints/season.py` (lines 877–891).
  - Replace naive stub with `FreeAgencyEngine(sync_db).simulate_free_agency(season_id)`.
- [ ] **C.3 Eliminate Game Record Duplication in `WeekSimulator`:**
  - File: `backend/app/services/week_simulator.py` (lines 130–152, 272).
  - Attach orchestrator directly to existing `Game.id` without `INSERT`ing a new record.
  - Await `orchestrator.save_game_result()`.
- [ ] **C.4 NFL Head-to-Head Standings Tiebreakers:**
  - File: `backend/app/services/standings_calculator.py` (lines 277–306).
  - Calculate actual head-to-head records among tied opponents and include in the sort key tuple before point differential.
- [ ] **C.5 Offseason State Machine Guards:**
  - Introduce `OffseasonPhase` enum (`RETIREMENTS -> RESIGNING -> FREE_AGENCY -> DRAFT -> ROOKIE_SIGNINGS -> COMPLETED`) to prevent out-of-order execution and repeated aging.

---

#### Subsystem D: Backend API, Core Architecture & Security
- [ ] **D.1 Mount All Orphaned API Routers:**
  - File: `backend/app/core/setup.py` (lines 68–120).
  - Register `coaches.py`, `combine.py`, `news_router.py`, and `training.py` with consistent `/api/` prefixes.
  - Deprecate duplicate mock files (`app/api/endpoints/news.py` mock vs `news_router.py`).
- [ ] **D.2 Eliminate Async Event Loop Blocking:**
  - Replace synchronous SQLAlchemy calls inside `async def` endpoints with `def` endpoints or `run_in_threadpool`.
  - Eliminate duplicate session initialization (`get_async_db` + `SessionLocal()`) in `season.py`.
- [ ] **D.3 Room-Isolated WebSocket Manager:**
  - Consolidate `websocket.py` and `live_visualization.py` into a unified `ChannelConnectionManager` with asyncio locks, per-game room isolation, ping-pong timeouts, and non-blocking broadcasts.
- [ ] **D.4 Security Hardening & Secret Scrubbing:**
  - Scrub hardcoded API key in `backend/.env.example`.
  - Add API key / admin authentication guards to `POST /api/genesis/seed`.
  - Sanitize raw SQL / exception disclosures in `error_handlers.py`.

---

#### Subsystem E: Frontend UI/UX, State Management & Performance
- [ ] **E.1 Fix Route Loader Type Safety:**
  - File: `frontend/src/hooks/useLoaderData.ts`.
  - Reconcile `Season | null`, `Team | null`, `noSeason: boolean` with `router.tsx` loaders.
- [ ] **E.2 Pre-allocate Three.js Vectors for 60FPS Animation:**
  - File: `frontend/src/components/3d/PlayerCharacter.tsx` and `EnhancedPlayerCharacter.tsx`.
  - Pre-allocate reusable `THREE.Vector3` to eliminate 2,640 allocations/second GC thrashing.
- [ ] **E.3 Eliminate Duplicate API Calls on Mount:**
  - File: `frontend/src/pages/SeasonDashboard.tsx`.
  - Remove duplicate `useEffect` fetch that duplicates the 7 API calls executed by `seasonDashboardLoader`.
- [ ] **E.4 Dynamicize Hardcoded URLs & Team IDs:**
  - File: `frontend/src/pages/FrontOffice.tsx`, `DepthChart.tsx`, `LiveSim.tsx`, `TrainingCenter.tsx`.
  - Replace hardcoded `localhost:8000` with `getWebSocketUrl()` and dynamic `userTeamId` from `useSettingsStore`.
- [ ] **E.5 Clean Up Dead Stores & Legacy Files:**
  - Purge unreferenced files: `DraftLegacy.tsx`, `FrontOffice_Baseline.tsx`, `SeasonDashboardLegacy.tsx`, `season.ts.backup`.
  - Add missing navigation links (`/medical-center`, `/empire/trophy-room`, `/offseason`, `/skills`) to `Navigation.tsx`.

---

### 3. Step-by-Step Execution Sequence

- [ ] **Step 1: Scaffolding & Critical Schema Cleanups.**
  - Resolve `player_game_starts` collision, register models in `alembic/env.py`, add SQLite WAL pragmas.
- [ ] **Step 2: Core Simulation & Football Engine Fixes.**
  - Fix safety/TD inversions, clock runoff calculations, red zone TD stats, PAT/2-PT execution, and deterministic RNG leaks.
- [ ] **Step 3: Season Lifecycle & Orchestrator Repair.**
  - Fix draft order `win_percentage` bug, connect `FreeAgencyEngine`, eliminate game duplication in `WeekSimulator`, and fix H2H standings tiebreakers.
  - Fix `Player.speed` hybrid_property query expression comparator for DraftAssistant.
- [ ] **Step 4: API, WebSockets & Security Hardening.**
  - Mount orphaned routers, eliminate sync event loop blocking, unify room-based WebSockets, scrub `.env.example`, and sanitize exception handlers.
- [ ] **Step 5: Frontend State, Performance & UX Overhaul.**
  - Reconcile loader types, fix 3D vector GC thrashing, eliminate duplicate data fetches, dynamicize team IDs, and clean dead stores/legacy files.

---

### 4. Edge Cases & Error Handling

- **[Case A: Goal-Line Sacks on Own 1-Yard Line]** -> Correctly awarded as a 2-point safety to defense with free kick from 20, never an offensive touchdown.
- **[Case B: 4th & Goal Lead Protection]** -> AI kicks field goal when leading by 3 late in the 4th quarter rather than unconditionally going for it.
- **[Case C: Mid-Season Traded Draft Picks]** -> Preserved during offseason draft order generation rather than overwritten with default team IDs.
- **[Case D: Slow WebSocket Client]** -> Isolated non-blocking broadcast with 2-second timeout prevents stuttering other connected clients.
- **[Case E: Missing Active Season on Offseason Page]** -> Strict nullable typing in loader presents clean "Initialize Season" banner rather than crashing `TypeError`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Backend passes Pydantic V2 validation; Frontend passes `tsc -b` with strict loader interfaces.
- [ ] **Security:** No hardcoded credentials in git-tracked `.env.example`; administrative seed endpoints protected; database exceptions sanitized.
- [ ] **Performance:** Simulation loop executes 18-week seasons without memory leaks or duplicate game rows; Three.js 3D animations maintain steady 60 FPS without GC thrashing.
- [ ] **Self-Critique:** Are there remaining hidden mocks? Ensure `test_offseason_service.py` uses real `TeamStanding` attributes and verify all 1,000+ pytest tests pass.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to Step 1 of the remediation plan: resolve the fatal database schema collision on `player_game_starts`, fix `Player.traits` attribute crash in `players.py`, and patch the `offseason_service.py` draft order attribute bug.
</baton_handoff>

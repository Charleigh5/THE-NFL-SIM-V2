# Master Plan: THE-NFL-SIM-V2 Remediation

## Objective
Execute full end-to-end remediation of THE-NFL-SIM-V2 across all 5 core tracks (R1 Database, R2 Simulation/Physics, R3 Season/Offseason/RPG, R4 Backend API/Security/Concurrency, R5 Frontend/State/Performance) and complete end-to-end verification.

## Execution Tracks & Milestones

### Phase 0: Survey & Environment Assessment
- Dispatch 3 parallel Explorers / Spec Miners to map existing codebase state, test setups, dependencies, model definitions, simulation engine, season lifecycle, API endpoints, and frontend build pipeline.
- Generate unified `PROJECT.md` with full feature inventory and interface contracts.

### Track A: E2E Testing Suite Track
- Milestone TEST: Build Opaque-Box E2E Test Suite across Tiers 1-4
  - Tier 1: Feature Coverage (Database, Physics, Engine, Offseason, API, UI)
  - Tier 2: Boundary & Corner Cases (Safety behind goal line, tiebreakers, clock runoff limits, cap space limits)
  - Tier 3: Cross-Feature Combinations (Simulate week -> update standings -> trigger injuries -> progress cap)
  - Tier 4: Real-World Scenarios (Full season simulation, draft cycle, offseason FA, multi-quarter games)
  - Publish `TEST_READY.md`.

### Track B: Implementation Track
- Milestone R1: Database Schema Consolidation & ORM Integrity
  - Unify `player_game_starts` declarative model
  - Register all 20+ models in Alembic metadata (`Season`, `PlayoffMatchup`, `DepthChart`, `NewsItem`, etc.)
  - Fix `Player.traits` and `Player.speed` hybrid property expressions
  - Add `cascade="all, delete-orphan"` to 1:1 decomposition relationships
  - Configure SQLite WAL connection pragmas
  - Verification: `alembic check`, unit tests, profile endpoint test, draft assistant speed query test.

- Milestone R2: Core Football Simulation & Physics Engine Correction
  - Fix safety scoring: yard_line <= 0 awards 2 points to defense and sets possession to receiving team at 35 (free kick from 20)
  - Dynamic play clock runoffs (4-7s incomplete, 5-8s out-of-bounds, 25-38s in-bounds)
  - Fix red zone TD stat attribution
  - Dynamic PAT & 2-point conversions
  - Deterministic seeded RNG (eliminate global random leaks)
  - Full multi-quarter simulation loop (Q1->Q4 + OT)

- Milestone R3: Season Lifecycle, Offseason & RPG Repair
  - Fix draft order attribute collision (`win_percentage` vs `win_pct`)
  - Preserve traded draft pick ownership across rounds 1-7
  - Route `/free-agency/simulate` to full `FreeAgencyEngine` with salary cap updates
  - Eliminate duplicate `Game` row creation in `WeekSimulator`
  - Await `save_game_result()`
  - Implement head-to-head tiebreakers in `StandingsCalculator` before point differential
  - Enforce `OffseasonPhase` state machine transitions

- Milestone R4: Backend API Architecture, Concurrency & Security Hardening
  - Mount orphaned routers (`coaches.py`, `combine.py`, `news_router.py`, `training.py`)
  - Eliminate blocking synchronous DB calls in `async def` endpoints
  - Eliminate duplicate session acquisition in `season.py`
  - Consolidate real-time broadcasting into room-isolated thread-safe WebSocket manager with async locks
  - Scrub hardcoded API keys from `.env.example`
  - Add admin guards to `/api/genesis/seed`
  - Sanitize database error disclosures

- Milestone R5: Frontend State Management, Type Safety & Performance Overhaul
  - Reconcile loader type contracts in `useLoaderData.ts` to strictly handle nullable seasons/teams
  - Pre-allocate Three.js `Vector3` instances to eliminate 60FPS GC thrashing
  - Remove redundant component-mount API fetches duplicating route loaders in `SeasonDashboard.tsx`
  - Dynamicize hardcoded URLs and franchise IDs (`userTeamId`)
  - Purge dead Zustand stores and legacy files
  - Add missing views to primary navigation (`/medical-center`, `/empire/trophy-room`, `/offseason`, `/skills`)
  - Verification: `npm run build` cleanly with zero TypeScript errors.

- Final Milestone: Full E2E Test Suite Execution & Tier 5 Adversarial Coverage Hardening
  - Verify 100% pass rate on Tiers 1-4
  - Execute Tier 5 Adversarial Coverage Hardening via Challenger loop
  - Final Forensic Audit & Verification Signoff.

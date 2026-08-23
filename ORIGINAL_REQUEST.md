# Original User Request

## 2026-08-22T16:18:01Z

Execute the complete end-to-end remediation of the NFL Sim Engine based on the AUDIT-001 master plan across all 5 core modules (Game Engine & Physics, Database & ORM Models, Season Lifecycle & RPG, Backend API & Security, Frontend UI/UX & State Flow) governed by the Hive-Mind Multi-Agent Architecture (`.agent/tasks/TASK_HIVE_MIND_AGENT_ARCHITECTURE.md`).

Working directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2
Integrity mode: development

## Requirements

### R1. Database Schema Consolidation & ORM Integrity
Unify the conflicting `player_game_starts` table into a single canonical SQLAlchemy 2.0 declarative model, register all 20+ models in Alembic metadata, fix the `Player.traits` and `Player.speed` hybrid property expressions, add `cascade="all, delete-orphan"` to 1:1 decomposition relationships, and configure SQLite WAL connection pragmas.

### R2. Core Football Simulation & Physics Engine Correction
Correct safety calculation so sacks or tackles behind the offensive goal line (`yard_line <= 0`) award a 2-point safety to the defense with a free kick from the 20 rather than an offensive touchdown. Implement dynamic play clock runoffs (4-7s for incomplete passes, 5-8s out-of-bounds, 25-38s in-bounds), fix red zone touchdown player stat attribution, integrate dynamic PAT/2-point conversions, eliminate unseeded `random` calls in favor of deterministic seeded RNG, and add a full multi-quarter simulation loop (`Q1 -> Q4 + OT`).

### R3. Season Lifecycle, Offseason & RPG Repair
Fix the draft order attribute collision (`win_percentage`), preserve traded draft pick ownership across rounds 1-7, route `/free-agency/simulate` to the full `FreeAgencyEngine`, eliminate duplicate `Game` row creation in `WeekSimulator`, await `save_game_result()`, implement head-to-head tiebreakers in `StandingsCalculator`, and enforce `OffseasonPhase` state machine transitions.

### R4. Backend API Architecture, Concurrency & Security Hardening
Mount all orphaned routers (`coaches.py`, `combine.py`, `news_router.py`, `training.py`), eliminate blocking synchronous database calls inside `async def` endpoints, eliminate duplicate session acquisition in `season.py`, consolidate real-time broadcasting into a room-isolated thread-safe WebSocket manager with async locks, scrub hardcoded API keys from `.env.example`, add admin guards to `/api/genesis/seed`, and sanitize database error disclosures.

### R5. Frontend State Management, Type Safety & Performance Overhaul
Reconcile loader type contracts in `useLoaderData.ts` to strictly handle nullable seasons/teams, pre-allocate Three.js `Vector3` instances to eliminate 60FPS GC allocation thrashing, remove redundant component-mount API fetches duplicating route loaders, dynamicize hardcoded URLs and franchise IDs (`userTeamId`), purge dead Zustand stores and legacy files, and add missing views to primary navigation.

## Acceptance Criteria

### Database & ORM Verification
- [ ] `PlayerGameStarts` is unified into a single declarative model without duplicate definitions in `app/models/`.
- [ ] `GET /api/players/{player_id}/profile` loads without `AttributeError` on `Player.player_traits`.
- [ ] `DraftAssistant` executes draft pick suggestions using `Player.speed` without SQLAlchemy `Comparator` exceptions.
- [ ] `alembic check` and model metadata autogenerate discover all tables including `Season`, `PlayoffMatchup`, `DepthChart`, and `NewsItem`.

### Football Engine & Physics Verification
- [ ] Sacks and tackles resulting in `yard_line <= 0` award 2 points to the defense and reset possession to receiving team at the 35 (free kick from 20).
- [ ] Incomplete passes consume between 4 and 7 seconds of game clock instead of a flat 40 seconds.
- [ ] Red zone touchdowns scored inside the 20-yard line are credited to the scoring player's passing/rushing/receiving statistics.
- [ ] PATs and 2-point conversions execute dynamically after touchdowns with variable scoring (1, 2, or 0 points).
- [ ] Deterministic replay checksums match 100% across identical game seed runs with zero global `random` leaks.

### Season & Offseason Lifecycle Verification
- [ ] Draft order generates successfully from active standings without `AttributeError: 'TeamStanding' object has no attribute 'win_pct'`.
- [ ] `POST /api/season/{id}/free-agency/simulate` executes multi-round market bidding through `FreeAgencyEngine` with salary cap updates.
- [ ] Batch week simulations complete without inserting duplicate `Game` rows with `season=2025, week=1`.
- [ ] Head-to-head records among tied opponents are evaluated before point differential in conference/division standings.

### API, Security & Real-Time Verification
- [ ] All mounted routes under `/api/coaches`, `/api/combine`, `/api/news`, and `/api/training` return valid JSON responses rather than 404s.
- [ ] Synchronous endpoints execute in worker threadpools without blocking the asyncio event loop.
- [ ] WebSocket connections on `/api/live/ws/game/{game_id}` receive game-isolated play events with backpressure timeouts and concurrency locks.
- [ ] No plaintext API keys are present in `.env.example`.

### Frontend & UI/UX Verification
- [ ] `npm run build` (`tsc -b && vite build`) executes cleanly with zero TypeScript errors.
- [ ] Route loaders in `useLoaderData.ts` safely handle `season: null` and `noSeason: true` states without early render crashes.
- [ ] Three.js 3D player animations render without frame drops or per-frame vector allocations.
- [ ] `SeasonDashboard.tsx` does not duplicate API fetches on mount.
- [ ] Navigation sidebar includes working links for `/medical-center`, `/empire/trophy-room`, `/offseason`, and `/skills`.

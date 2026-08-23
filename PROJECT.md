# Project: THE-NFL-SIM-V2 Remediation & Production Hardening

## Architecture
THE-NFL-SIM-V2 is a full-stack professional football simulation platform comprising:
- **Backend API & Engine (Python 3.11+ / FastAPI / SQLAlchemy 2.0 / Alembic)**:
  - `app/models/`: Canonical SQLAlchemy 2.0 declarative database models with strict cascades and hybrid property expressions.
  - `app/engine/`: 60Hz physics, deterministic CSPRNG mechanics, play resolvers, dynamic clock runoffs, safeties, PAT/2-pt conversion logic, and multi-quarter continuous simulation.
  - `app/orchestrator/`: Game sessions, week simulators, season progression, and event lifecycles.
  - `app/services/`: Offseason management, FreeAgencyEngine multi-wave market bidding, DraftAssistant, StandingsCalculator with head-to-head tiebreakers, and depth chart management.
  - `app/api/`: FastAPI REST endpoints, room-isolated thread-safe WebSocket managers, admin authentication guards, and sanitized error disclosures.
- **Frontend User Interface (React 19 / TypeScript 5.9 / Vite 7 / Tailwind CSS 4 / Three.js)**:
  - `frontend/src/pages/`: Franchise management views (FrontOffice, DepthChart, SeasonDashboard, OffseasonDashboard, LiveSim, DraftRoom, MedicalCenter, TrophyRoom, SkillsPage).
  - `frontend/src/hooks/useLoaderData.ts`: Strictly typed route loader contracts with nullable season/team handling.
  - `frontend/src/components/3d/`: Three.js Canvas field and player visualizers optimized with module-level scratch vectors.
  - `frontend/src/store/`: Zustand state management for user settings, active game broadcasts, and simulation state.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | `PlayerGameStarts` Unification | Consolidate triple definition into single declarative model with all columns and relationships | M1 | Survey R1 |
| F02 | Alembic Model Discovery | Register all 20+ models in Alembic metadata (`Season`, `PlayoffMatchup`, `DepthChart`, `NewsItem`, etc.) | M1 | Survey R1 |
| F03 | `Player.traits` Relationship | Fix `AttributeError` on `Player.player_traits` in `GET /api/players/{player_id}/profile` | M1 | Survey R1 |
| F04 | Hybrid Property Expressions | Implement `@expression` SQL subqueries for `Player.speed`, `strength`, `agility`, etc. for `DraftAssistant` | M1 | Survey R1 |
| F05 | 1:1 Decomposition Cascades & Loading | Add `cascade="all, delete-orphan"` and `lazy="selectin"` to Player decomposition relationships | M1 | Survey R1 |
| F06 | SQLite WAL Connection Pragmas | Configure `journal_mode=WAL` and `busy_timeout=5000` on database engine connections | M1 | Survey R1 |
| F07 | Safety Scoring & Possession Reset | Fix safety on `yard_line <= 0` awarding 2 pts to defense + free kick from 20 (possession at 35) | M2 | Survey R2 |
| F08 | Dynamic Play Clock Runoffs | Implement 4-7s incomplete, 5-8s out-of-bounds, 25-38s in-bounds, 6-9s sacks, 5-8s special teams runoffs | M2 | Survey R2 |
| F09 | Red Zone TD Stat Attribution | Correct red zone goal line touchdown resolution and player passing/rushing/receiving stat credits | M2 | Survey R2 |
| F10 | Dynamic PAT & 2-Pt Conversions | Execute dynamic point-after-touchdown and 2-point conversions with variable scoring (1, 2, or 0 pts) | M2 | Survey R2 |
| F11 | Deterministic Seeded RNG | Eliminate unseeded global `random` calls in physics, sack, and injury calculators in favor of seeded RNG | M2 | Survey R2 |
| F12 | Multi-Quarter & Overtime Simulation | Implement full Q1 -> Q4 simulation loop with 15-min quarters, halftime kickoff, and OT rules | M2 | Survey R2 |
| F13 | Draft Order Attribute Resolution | Fix `win_percentage` vs `win_pct` attribute collision in `OffseasonService` standings sorting | M3 | Survey R3 |
| F14 | Traded Draft Pick Ownership | Preserve draft pick trades across rounds 1-7 in trade execution and draft order generation | M3 | Survey R3 |
| F15 | Free Agency Engine Integration | Route `/free-agency/simulate` to full `FreeAgencyEngine` with multi-wave bidding & salary cap updates | M3 | Survey R3 |
| F16 | WeekSimulator Game Row Deduplication | Attach `SimulationOrchestrator` to existing game IDs, eliminate dummy row insertions, await `save_game_result()` | M3 | Survey R3 |
| F17 | Head-to-Head Tiebreaker Logic | Evaluate head-to-head records among tied opponents before conference/division records and point diff | M3 | Survey R3 |
| F18 | OffseasonPhase State Machine | Enforce ordered offseason phase progression (Retirements -> Resignings -> FA -> Draft -> Rookies -> Camp) | M3 | Survey R3 |
| F19 | Orphaned Router Mounting | Mount unmounted routers (`coaches.py`, `combine.py`, `news_router.py`, `training.py`) in `setup.py` | M4 | Survey R4 |
| F20 | Async/Sync Concurrency Sanitation | Convert sync `async def` endpoints to `def` or worker threadpools to eliminate event loop blocking | M4 | Survey R4 |
| F21 | Session Allocation Optimization | Eliminate duplicate `db: AsyncSession` acquisition on synchronous threadpool endpoints in `season.py` | M4 | Survey R4 |
| F22 | Room-Isolated WebSocket Manager | Implement thread-safe WebSocket manager with per-game room isolation, `asyncio.Lock()`, and task fanout | M4 | Survey R4 |
| F23 | Secret Scrubbing in .env.example | Remove hardcoded plaintext Vertex API key from `.env.example` template | M4 | Survey R4 |
| F24 | Admin Authentication Guard | Protect `/api/genesis/seed` with admin authentication guards against unauthorized database resets | M4 | Survey R4 |
| F25 | Database Error Payload Sanitization | Sanitize database exception disclosures and eliminate unbuffered debug file writes | M4 | Survey R4 |
| F26 | Route Loader Type Contracts | Update `useLoaderData.ts` to strictly handle `season: Season | null`, `noSeason: boolean`, `team: Team | null` | M5 | Survey R5 |
| F27 | Three.js GC Allocation Elimination | Replace per-frame `new THREE.Vector3` with pre-allocated module-level scratch vectors in 3D visualizers | M5 | Survey R5 |
| F28 | Redundant Component Mount Fetch Purge | Remove duplicate mount `useEffect` API calls in `SeasonDashboard.tsx`, `OffseasonDashboard.tsx`, etc. | M5 | Survey R5 |
| F29 | Network & Franchise ID Dynamicization | Replace hardcoded URLs (`localhost:8000`) and team ID `1` with runtime environment and store configs | M5 | Survey R5 |
| F30 | Dead Store & Legacy File Cleanup | Delete 5 unreferenced Zustand stores and 4 legacy files | M5 | Survey R5 |
| F31 | Primary Navigation Expansion | Add missing navigation links (`/offseason`, `/medical-center`, `/empire/trophy-room`, `/skills`) to `Navigation.tsx` | M5 | Survey R5 |
| F32 | Comprehensive Opaque-Box E2E Suite | 4-Tier requirement-driven test suite with >=11*N test cases and `TEST_READY.md` publication | M_TEST | Test Track |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M_TEST | E2E Testing Suite Track | Implement 4-tier opaque-box test suite across all 32 inventoried features and publish `TEST_READY.md` | none | IN_PROGRESS |
| M1 | Database Schema & ORM Consolidation | Features F01, F02, F03, F04, F05, F06 | none | DONE |
| M2 | Core Football Simulation & Physics | Features F07, F08, F09, F10, F11, F12 | M1 | IN_PROGRESS |
| M3 | Season Lifecycle, Offseason & RPG | Features F13, F14, F15, F16, F17, F18 | M1, M2 | PLANNED |
| M4 | Backend API Architecture & Security | Features F19, F20, F21, F22, F23, F24, F25 | M1, M3 | PLANNED |
| M5 | Frontend State & Performance | Features F26, F27, F28, F29, F30, F31 | M4 | PLANNED |
| M_FINAL | 100% E2E Pass & Tier 5 Hardening | Full E2E test execution + Adversarial Challenger coverage hardening | M_TEST, M1, M2, M3, M4, M5 | PLANNED |

---

## Interface Contracts

### Backend Database Models ↔ Service Layer
- `PlayerGameStarts`: Canonical table `player_game_starts` with columns `id` (int PK), `player_id` (int FK), `game_id` (int FK), `team_id` (int FK), `season_id` (int FK), `week` (int), `position` (str), `teammates_hash` (str), `created_at` (datetime).
- `Player.speed`, `Player.strength`, `Player.agility`: Hybrid properties with `@speed.expression` scalar subqueries selecting corresponding column from `PlayerAttributes` where `player_id == Player.id`.
- `Player.player_traits`: ORM relationship returning `List[PlayerTrait]` with `selectinload` or `joinedload(PlayerTrait.trait)`.

### Game Engine ↔ Simulation Orchestrator
- `PlayResult`: `yards_gained: int`, `is_touchdown: bool`, `is_safety: bool`, `is_turnover: bool`, `is_sack: bool`, `time_elapsed: float`, `passer_id: Optional[int]`, `rusher_id: Optional[int]`, `receiver_id: Optional[int]`.
- Safety rule: If `is_safety` or offensive play results in `yard_line <= 0`, award +2 points to defensive team, reset possession to non-scoring team, set ball at 35 (free kick from 20).
- Clock runoffs: Incomplete = 4.0-7.0s, Out-of-bounds = 5.0-8.0s, In-bounds = 25.0-38.0s, Sack = 6.0-9.0s.

### Season Orchestration ↔ Offseason Engine
- `StandingsCalculator`: Sort key evaluates `(is_div_winner, win_percentage, head_to_head_win_pct, div_win_pct, conf_win_pct, sos, point_differential)`.
- `FreeAgencyEngine.simulate_free_agency(season_id: int)` returns `List[FreeAgentSigning]` and decrements `team.salary_cap_space`.
- `DraftPick`: Preserves `team_id` (current owner) and `original_team_id`.

### Frontend Route Loaders ↔ UI Components
- `OffseasonDashboardLoaderData`: `{ teams: Team[], season: Season | null, isOffseason: boolean, noSeason: boolean }`.
- `DepthChartLoaderData`: `{ teams: Team[], team: Team | null, roster: Player[] }`.

---

## Code Layout
- Backend: `backend/app/`
  - `models/`: Database ORM definitions
  - `engine/`: Core simulation, physics, calculations
  - `orchestrator/`: Session lifecycle, week simulation, play routing
  - `services/`: Business logic, standings, draft, free agency, chemistry
  - `api/`: REST routes, dependency injection, WebSocket managers
  - `core/`: Config, database engines, error handling, security
- Frontend: `frontend/src/`
  - `components/`: UI and Three.js 3D visualizers
  - `pages/`: Route page views
  - `hooks/`: Custom hooks and route loader data bindings
  - `store/`: Active Zustand state stores
  - `services/`: Axios HTTP client and WebSocket helpers
- Tests:
  - `backend/tests/`: Pytest unit, integration, and physics test suites
  - `frontend/e2e/`: Playwright end-to-end user journey tests

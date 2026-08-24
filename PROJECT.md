# Project: THE-NFL-SIM-V2 Full Codebase Component & Endpoint Audit (AUDIT-001)

## Architecture
- **Backend Architecture**: FastAPI REST API (`backend/app/api/`), Domain Services (`backend/app/services/`), Simulation Engine (`backend/app/engine/`), RPG Kernels (`backend/app/rpg/`), SQLAlchemy/Alembic Database Models (`backend/app/models/`), Pydantic V2 Schemas (`backend/app/schemas/`).
- **Frontend Architecture**: React 19 / TypeScript / Vite (`frontend/src/`), React Router v7 Data Routers (`router.tsx`), Zustand & Context State Stores, Tailwind CSS + Framer Motion animations, Three.js / HTML5 Canvas Gridiron Visualizer.
- **Testing & Calibration Architecture**: Pytest Unit & Integration Suite (`backend/tests/`), Batch Monte Carlo Physics & Stat Calibration (`scripts/batch_simulator.py`), Playwright E2E Browser Automation Suite (`frontend/e2e/`).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Component Mount Hierarchy Audit | Mount high-value unmounted components (`ReplayScrubber`, `TreatmentModal`, `EnhancedPlayerProfile`, `StorylineTracker`, `NewsFeedWidget`, `LogoTimeline`) and isolate legacy pages | M1 | Survey / R1 |
| 2 | Medical 5-Pathway Orthopedic Triage API | Expose REST endpoints for 5 triage protocols (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`) | M2 | Survey / R2 |
| 3 | Coaching Dynasty Tree & Synergy API | Expose REST endpoints for coach skill trees, node unlocking, and staff synergy calculations | M2 | Survey / R2 |
| 4 | Multi-Lens Scouting Intelligence API | Expose REST endpoints for scouting bias lenses and trade urgency calculations | M2 | Survey / R2 |
| 5 | Frontend API Service Prefix & Endpoint Wire-up | Fix URL prefix mismatches (`/abilities`, `/physics`, `/scouting`) and wire live endpoints replacing mock stubs in services and loaders | M2 | Survey / R2 |
| 6 | Engine & Service Deduplication | Harmonize OL Chemistry calculation, consolidate 7-archetype RPG system, remove deprecated traits, unify duplicate training and news routers | M3 | Survey / R3 |
| 7 | Contract & TypeScript Parity | Ensure 100% Pydantic V2 / TypeScript contract parity (add `neck_health`, eliminate `any` casts, align Trade schemas, deduplicate trait services) | M3 | Survey / R3 |
| 8 | Full-Stack Testing & Calibration Gate | Verify 100% pass rate on `pytest backend/tests/unit`, Monte Carlo calibration (`batch_simulator.py`), frontend production build (`npm run build`), and Playwright E2E browser tests | M4 | Survey / R4 |
| 9 | Formal Audit Spec & Documentation Sync | Author `docs/tasks/AUDIT-001_FULL_CODEBASE_COMPONENT_AND_ENDPOINT_AUDIT.md` complying with task-list-template.md and synchronize `docs/FEATURE_STATUS_MATRIX.md` | M5 | Survey / R5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | UI Component Mounting & Route Integration | Mount unmounted components in views (LiveSim, MedicalCenter, FrontOffice/DepthChart, Dashboard, TrophyRoom) | none | DONE |
| M2 | Live FastAPI Endpoint Implementation & Wire-up | Expose triage, coaching tree, scouting APIs; fix frontend services and replace mock fallbacks | M1 | DONE |
| M3 | Logic & Schema Deduplication | Harmonize chemistry/archetypes, eliminate duplicate routers/services, guarantee strict schema parity with 0 `any` types | M2 | IN_PROGRESS |
| M4 | Full-Stack Verification & Playwright Tests | Run pytest unit tests, Monte Carlo statistical calibration, frontend build, and Playwright E2E specs | M3 | PLANNED |
| M5 | Formal Audit Spec & Matrix Sync | Author AUDIT-001 task report and update FEATURE_STATUS_MATRIX.md | M4 | PLANNED |

## Interface Contracts
### Medical Triage API
- `GET /api/medical/players/{player_id}/triage/protocols` -> `TriageProtocolsResponse` (protocols: List[TriageProtocolOption], current_diagnosis: InjuryDiagnosis)
- `POST /api/medical/players/{player_id}/triage/apply` -> Request: `TriageDecisionRequest(protocol: TriageProtocolType)`, Response: `TriageDecisionResult`
- `GET /api/medical/players/{player_id}/health` -> `BodyHealthResponse` (including `neck_health: float`)

### Coaching Dynasty Tree API
- `GET /api/coaches/{coach_id}/tree` -> `CoachDynastyTreeResponse`
- `POST /api/coaches/{coach_id}/unlock-node` -> Request: `UnlockNodeRequest(node_id: str)`, Response: `CoachDynastyTreeResponse`
- `GET /api/coaches/staff/synergy/{team_id}` -> `StaffSynergyResponse`

### Scouting Multi-Lens Intelligence API
- `GET /api/scouts/prospects/{prospect_id}/intelligence` -> `ProspectIntelligenceResponse` (consensus, film, analytics, regional)
- `GET /api/scouts/trade-urgency/{team_id}` -> `TradeUrgencyResponse`

### Trade Proposals & Blocks
- `POST /api/trades/proposals` -> Request: `TradeOfferRequest(proposing_team_id: int, target_team_id: int, offered_player_ids: List[int], requested_player_ids: List[int], offered_draft_pick_ids: List[int], requested_draft_pick_ids: List[int])`

## Code Layout
- `backend/app/api/endpoints/`: Canonical FastAPI route controllers
- `backend/app/services/`: Canonical business logic and simulation support services
- `backend/app/schemas/`: Canonical Pydantic V2 schema definitions
- `backend/app/engine/`: Core simulation math and physics engines
- `frontend/src/components/`: Modular UI components organized by domain
- `frontend/src/pages/`: 13 core application views connected via React Router v7
- `frontend/src/services/`: Axios and typed client services connecting to `/api/...`
- `frontend/src/types/`: Strict TypeScript interface models mirroring backend schemas
- `docs/tasks/`: Formal audit specifications and execution records

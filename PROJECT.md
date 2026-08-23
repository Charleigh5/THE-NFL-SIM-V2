# Project: THE-NFL-SIM-V2 ("The Digital Gridiron")

## Architecture
THE-NFL-SIM-V2 is a full-stack professional football simulation platform comprising:
- **Backend (Python / FastAPI / SQLAlchemy / Alembic)**:
  - High-performance simulation engine (`backend/app/engine/`) with 60Hz deterministic frame physics, CSPRNG commit-reveal seeds, and Monte Carlo calibrated play resolution.
  - Deep-dive RPG subsystems (`backend/app/services/` & `backend/app/schemas/deep_dive.py`): Multi-Lens Scouting Fog of War, Coaching Dynasty DAG trees & staff synergy, and 5-Pathway Orthopedic Triage with Cox hazard modeling.
  - 26 REST & WebSocket API modules (`backend/app/api/endpoints/`) serving all franchise management and live broadcast endpoints.
- **Frontend (React / Vite / TypeScript / Tailwind / Framer Motion / Three.js / Pixi.js)**:
  - 13 core views covering Franchise War Room, Tactical Live Sim, Offseason Draft Room, Coaching Dynasty Tree, Medical Trauma Center, Depth Chart, Roster/Capology, Schedule, Standings/Playoffs, Player Profile/S2, GM Trades, Cryptographic Replay Telemetry, and League Settings.
  - Strict TypeScript schema contract alignment (`frontend/src/types/`) with zero `any` types.
- **Testing & Calibration Infrastructure**:
  - Playwright browser automation test suite (`frontend/e2e/`) capturing pre/post interaction states across all 13 core views.
  - Pytest unit suite (`backend/tests/unit/`) with 300+ tests covering simulation, AI, RPG, medical, and broadcast models.
  - Monte Carlo batch simulator (`scripts/batch_simulator.py`) enforcing NFL historical benchmark calibration.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | 13-View UI Route Graph & Navigation | Complete routing across all 13 views with route aliases (`/medical`, `/roster`, `/trades`) | M1, M2 | ORIGINAL_REQUEST §R1 |
| 2 | Strict Contract Parity & 0 `any` Types | 1:1 parity between FastAPI Pydantic V2 schemas and TypeScript definitions | M1 | ORIGINAL_REQUEST §R2 |
| 3 | Schema Synchronization (Scouting, PlayResult, Team) | Harmonize scouting report fields, `is_safety`, and team medical/staff properties | M1 | ORIGINAL_REQUEST §R2 |
| 4 | Automated Browser Navigation & Pre/Post Visual Proof | Capture high-resolution screenshots of pre- and post-interaction states for 13 views | M2 | ORIGINAL_REQUEST §R1 |
| 5 | Defect Isolation & Closed-Loop Remediation | Zero console errors, broken transitions, or UI clipping across all views | M2 | ORIGINAL_REQUEST §R3 |
| 6 | Backend Unit Test Suite Verification | 100% pass rate on `pytest backend/tests/unit` | M3 | ORIGINAL_REQUEST §R4 |
| 7 | Monte Carlo Statistical Calibration | 100% calibration compliance across sack rate, YPC, completion rate, turnovers, PPG | M3 | ORIGINAL_REQUEST §R4 |
| 8 | Frontend Production Compilation | 100% clean build on `npm run build` (`tsc -b && vite build`) with exit code 0 | M3 | ORIGINAL_REQUEST §R4 |
| 9 | Formal Task Documentation TASK-003 | Comprehensive specification in `docs/tasks/TASK-003_13_VIEW_VISUAL_AUDIT_AND_REMEDIATION.md` | M4 | ORIGINAL_REQUEST §R5 |
| 10 | Multi-Agent Final Verification & Audit Gate | Independent Reviewers, Challengers, and Forensic Auditor verification | M5 | System Governance |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Contract Parity & Type Alignment | Eliminate residual `any` types in `frontend/src/`, synchronize scouting/simulation/team schemas, add route aliases | none | DONE |
| 2 | 13-View UI & Broadcast Visual Verification | Execute Playwright visual capture suite for all 13 views (pre & post interaction), verify 0 console errors | M1 | DONE |
| 3 | Production Testing & Statistical Calibration | Run full `pytest backend/tests/unit`, `npm run build`, and `python scripts/batch_simulator.py` | M1, M2 | DONE |
| 4 | Formal Task Documentation TASK-003 | Author `docs/tasks/TASK-003_13_VIEW_VISUAL_AUDIT_AND_REMEDIATION.md` per task-list-template.md | M1, M2, M3 | DONE |
| 5 | Final Gate & Forensic Integrity Audit | Multi-agent review, adversarial challenge, and binary forensic audit | M1, M2, M3, M4 | DONE |

## Interface Contracts
### `backend/app/schemas/scouting.py` ↔ `frontend/src/types/api/scouting.ts`
- `ScoutingReport`: `ceiling_projection`, `floor_projection`, `draft_grade`, `fit_analysis`, `pros`, `cons`, `summary`.
- `PlayerBackstory`: `hometown`, `background`, `personality_traits`, `motivations`, `notable_college_moments`, `adversity_overcome`.

### `backend/app/schemas/play.py` ↔ `frontend/src/types/simulation.ts`
- `PlayResult`: `play_id`, `play_type`, `quarter`, `time_remaining`, `yard_line`, `down`, `distance`, `yards_gained`, `is_touchdown`, `is_interception`, `is_fumble`, `is_incomplete`, `is_sack`, `is_penalty`, `is_safety`, `points_scored`, `description`.

### `backend/app/schemas/team.py` ↔ `frontend/src/services/api.ts`
- `Team`: `id`, `city`, `name`, `abbreviation`, `conference`, `division`, `wins`, `losses`, `ties`, `salary_cap_space`, `logo_url`, `primary_color`, `secondary_color`, `medical_rating`, `training_staff_quality`, `medical_budget`, `elo_rating`.

## Code Layout
- `backend/app/schemas/`: Pydantic V2 schema definitions
- `backend/app/api/endpoints/`: FastAPI REST endpoints and WebSockets
- `backend/app/engine/`: Simulation core, 60Hz physics, RNG verification
- `backend/tests/unit/`: Pytest unit and integration test suites
- `frontend/src/types/`: TypeScript interface definitions
- `frontend/src/pages/`: 13 core view page components
- `frontend/src/components/`: Subsystem UI components (coaching, medical, draft, trades, live sim)
- `frontend/e2e/`: Playwright E2E and visual capture test suites
- `docs/assets/screenshots/`: Captured high-resolution UI screenshots (pre and post interaction)
- `docs/tasks/`: Formal task documentation specifications

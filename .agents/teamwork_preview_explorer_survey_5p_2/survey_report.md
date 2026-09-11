# Technical Survey & Codebase Audit Report: TASK-012 & TASK-013

**Date:** 2026-09-06
**Auditor:** Teamwork Explorer (`teamwork_preview_explorer_survey_5p_2`)
**Scope:**
1. TASK-012: Medical Center Live Roster & Surgical Triage Integration
2. TASK-013: In-Game Play-Calling HUD & 60Hz Live Physics Telemetry
3. Telemetry & Latency Budgets (60Hz delivery <16ms, 4th-down lookups <10ms)
4. Schema & Contract Parity Audit (Pydantic V2 vs TypeScript, `any` type scan)

---

## Executive Summary

An exhaustive read-only inspection of `THE-NFL-SIM-V2` was conducted covering backend database models, service layers, FastAPI route handlers, WebSocket streamers, and frontend React/TypeScript components.

- **TASK-012 (Medical Center)**: The backend provides an advanced 5-pathway clinical triage engine (`OrthopedicTriageService` in `backend/app/services/medical/orthopedic_triage_service.py`) and corresponding endpoints in `backend/app/api/endpoints/medical.py`. However, the frontend `MedicalCenter.tsx` is completely unhooked from live data: it uses hardcoded mock players (Kyler Murray, James Conner, Hollywood Brown), never fetches `GET /api/medical/team/{team_id}/injuries`, hardcodes protocol options inside `useMemo` in `OrthopedicTriageModal.tsx`, and reduces all 5 protocols to 3 legacy options ("REST", "SURGERY", "PLAY_THROUGH") sent to `/api/medical/treatment`. Furthermore, two critical backend defects were uncovered: a status enum bug where healthy players evaluate to `is_injured=True` due to a mismatch (`"HEALTHY"` vs `"ACTIVE"`), and a list-subscript bug (`player.body_health[0]`) in `medical_service.py` that fails on SQLAlchemy 2.0 1:1 scalar relationships.
- **TASK-013 (In-Game Play-Calling HUD)**: The live simulation (`LiveSim.tsx`) operates purely in "Spectator Mode" using a hardcoded mock trajectory generator. The interactive play-calling HUD drawer (`PlayCallingHUD.tsx`), timeout controller (`ClockManagementBar.tsx`), and Ben Baldwin 4th-down analytics modal (`FourthDownModal.tsx`) have **not yet been implemented** in `frontend/src/components/game/`. In the backend, `FramePhysicsEngine` executes 60Hz deterministic physics in $< 10$ms, but there is no 4th-down EPA/Win Probability calculator service (`fourth_down_calculator.py`), and the live WebSocket endpoint (`/ws/simulation/live`) only responds to ping/pong without play injection capabilities.
- **Telemetry & Latency Budgets**: The 60Hz physics loop meets its operational target ($< 10$ms execution for a full 600-frame play, $< 0.05$ms per frame), but the WebSocket streamer in `physics_api.py` uses uncompensated `asyncio.sleep(DELTA_T)` subject to OS timer jitter. Telemetry frame payloads are compact (~823 bytes).
- **Schema & Contract Parity**: Zero `any` types exist across frontend types and components. However, significant schema drift exists between `physics_api.py` and `frontend/src/types/physics.ts` regarding player state enums, coordinate representations (flat `x, y` vs nested `Vector2`), and missing orientation angles. Master domain contracts defined in `docs/design_theory/nfl_simulation_blueprint/ui_design_system.md` have 100% theoretical parity in blueprint test scripts, but have not yet been extracted into production code modules (`domain_contracts.py` / `domain_contracts.ts`).

---

## 1. TASK-012: Medical Center Live Roster & Surgical Triage Integration

### 1.1 Backend Architecture & File Locations

| Component | File Path | Responsibilities & Status |
|---|---|---|
| **Database Model: Body Health** | `backend/app/models/medical.py:6-31` | `BodyPart` table `body_health`. Tracks 7 anatomical zones (`head_health`, `neck_health`, `torso_health`, `right_arm_health`, `left_arm_health`, `right_leg_health`, `left_leg_health`) and `general_wear`. |
| **Database Model: Injury Event** | `backend/app/models/medical.py:32-53` | `InjuryEvent` table `injury_events`. Historical record of injuries, severity (1-10), duration, and treatment chosen. |
| **Database Model: Player Injury** | `backend/app/models/player_injury.py:17-40` | `PlayerInjury` table `player_injury`. 1:1 relation with `Player`. Holds `injury_status` (`ACTIVE`, `QUESTIONABLE`, `DOUBTFUL`, `OUT`, `IR`), `weeks_to_recovery`, `injury_severity`, `injury_recurrence_risk`. |
| **Database Model: Player** | `backend/app/models/player.py:854-909, 999` | Connects `body_health` (`uselist=False`) and proxies injury fields via hybrid properties to `PlayerInjury`. |
| **Orthopedic Triage Service** | `backend/app/services/medical/orthopedic_triage_service.py` | 5-pathway clinical recovery calculator (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`) with Cox hazard multiplier and complication rolls. |
| **Medical Service** | `backend/app/services/medical_service.py` | Applies post-game wear and weekly recovery. Contains list-subscript defect on lines 24 and 70. |
| **FastAPI Endpoints** | `backend/app/api/endpoints/medical.py` | Exposes REST endpoints for player health, wear, treatment, team injuries, surgery risk, and orthopedic triage. |

### 1.2 Identified Backend Bugs & Defects

1. **Enum Mismatch on Healthy Status (`medical.py:61`)**:
   ```python
   # Line 61 in medical.py:
   is_injured=player.injury_status != "HEALTHY"
   ```
   *Defect:* In `PlayerInjury` and `Player`, the enum value for an uninjured player is `InjuryStatus.ACTIVE` (`"ACTIVE"`). Comparing `player.injury_status != "HEALTHY"` returns `True` for active players, causing all healthy players to be flagged as injured.
   *Fix Required:* Change to `is_injured=player.injury_status != InjuryStatus.ACTIVE` (or `player.injury_status != "ACTIVE"`).

2. **Subscript Error on 1:1 Relationship (`medical_service.py:24, 70`)**:
   ```python
   # Lines 24 & 70 in medical_service.py:
   health = player.body_health[0] # One-to-one list
   ```
   *Defect:* In `Player` (`backend/app/models/player.py:999`), `body_health` is defined with `uselist=False`. Accessing `player.body_health[0]` throws `TypeError: 'BodyPart' object is not subscriptable`.
   *Fix Required:* Check `isinstance(player.body_health, list)` or directly reference `player.body_health`.

3. **Incomplete Triage State Mutation (`medical.py:395-406`)**:
   In `apply_player_triage_protocol` (`POST /api/medical/players/{player_id}/triage/apply`):
   - It correctly mutates `player.weeks_to_recovery`, `player.injury_recurrence_risk`, and `player.injury_status`.
   - **Missing:** It fails to update `player.body_health` with the projected zone integrity (`result.final_integrity_forecast`).
   - **Missing:** It does not insert an `InjuryEvent` record into the `injury_events` table for career medical history tracking.

### 1.3 Frontend Implementation & Integration Disconnects

| Component | File Path | Current Status & Audit Finding |
|---|---|---|
| **Medical Center Page** | `frontend/src/pages/MedicalCenter.tsx` | **Disconnected / Mocked**. State `injuredRoster` is initialized with 3 hardcoded mock players (`Kyler Murray`, `James Conner`, `Hollywood Brown`). It never fetches `GET /api/medical/team/{team_id}/injuries`. |
| **Zero-Injury Handling** | `frontend/src/pages/MedicalCenter.tsx:75` | If `injuredRoster` is empty, `activePlayer` evaluates to `undefined`, leading to crashes in downstream subcomponents (`BodyMap`). Preventative maintenance mode is missing. |
| **Orthopedic Triage Modal** | `frontend/src/components/medical/OrthopedicTriageModal.tsx` | Protocol options are hardcoded in a local `useMemo` hook (lines 42-100) instead of being retrieved via `GET /api/medical/players/{player_id}/triage/protocols`. |
| **Triage Protocol Confirm** | `frontend/src/pages/MedicalCenter.tsx:119-152` | `handleProtocolConfirm` attempts to downsample 5 clinical pathways into `"REST"`, `"SURGERY"`, or `"PLAY_THROUGH"` and posts to legacy `/api/medical/treatment` instead of calling `/api/medical/players/{player_id}/triage/apply`. |
| **Medical API Client** | `frontend/src/services/medicalApi.ts` | Lacks functions for `applyOrthopedicTriage` (`POST /api/medical/players/{id}/triage/apply`) and `getPlayerTriageProtocols` (`GET /api/medical/players/{id}/triage/protocols`). |
| **State Management** | `frontend/src/store/useMedicalStore.ts` | Does not exist. State is managed via local `useState` in `MedicalCenter.tsx`. |

---

## 2. TASK-013: In-Game Play-Calling HUD & 60Hz Live Physics

### 2.1 Backend Physics Engine & Streaming

| Component | File Path | Status & Performance Observations |
|---|---|---|
| **60Hz Physics Engine** | `backend/app/engine/frame_physics.py` | Complete and verified. Runs 60Hz kinematic frame simulation (`FRAMES_PER_SECOND = 60`, `DELTA_T = 0.016667s`). Tracks 22 players + ball, collision detection, tackle probabilities, and Merkle tree SHA-256 state hashes. |
| **Physics REST API** | `backend/app/api/endpoints/physics_api.py` | Exposes `POST /api/physics/simulate` and `GET /api/physics/constants`. |
| **Physics WebSocket Streamer** | `backend/app/api/endpoints/physics_api.py:170-250` | Exposes WebSocket at `/api/physics/stream`. Streams frames paced with `await asyncio.sleep(DELTA_T)`. |
| **Live Game WebSocket** | `backend/app/api/endpoints/websocket.py` | Exposes `/ws/simulation/live`. Accepts only `"PING"` and emits `{"type": "PONG"}`. **Zero play injection support**. |
| **Simulation Orchestrator** | `backend/app/orchestrator/simulation_orchestrator.py` | Autonomous loop that simulates plays sequentially. Lacks an interactive pause/wait state for user coach play calls. |

### 2.2 4th-Down Decision Modeling & Ben Baldwin Analytics

1. **Current Codebase State**:
   - `backend/app/core/nfl_reference_data.py:130-140` defines a `FourthDownAnalytics` dataclass with baseline thresholds (`always_go_distance=1`, `consider_go_distance=5`, `go_for_it_zone_start=40`, `go_for_it_zone_end=60`).
   - `backend/app/services/playbook/coaching_ai.py:40-98` implements heuristic 4th-down decision making for autonomous AI coaches.
   - **Gaps**:
     - `backend/app/engine/fourth_down_calculator.py` **does not exist**.
     - `backend/app/engine/analytics/baldwin_conversion_model.py` **does not exist**.
     - No REST or WebSocket endpoint exists to calculate real-time Win Probability (WP) and Expected Points Added (EPA) deltas across Go, FG, and Punt options.

### 2.3 Frontend Play-Calling HUD Architecture

1. **Current `LiveSim.tsx` Status**:
   - Operates solely in "Spectator Mode".
   - Connects to `/ws/simulation/live`.
   - Controls are limited to "KICKOFF", "Pause", and "Fast Forward".
   - Utilizes `generateMockPlay()` generating a hardcoded 120-frame mock trajectory for canvas animation.
2. **Missing Frontend Components**:
   - `PlayCallingHUD.tsx` (offensive run/pass concepts and defensive coverages/blitzes) is **missing**.
   - `FourthDownModal.tsx` (cinematic analytics popup with Go/Punt/FG recommendations) is **missing**.
   - `ClockManagementBar.tsx` (timeouts, hurry-up/chew-clock tempo, spike, kneel) is **missing**.
   - `CoachModeToggle` (switch between spectator auto-sim and user play-calling) is **missing**.
   - `frontend/src/types/playcalling.ts` and `backend/app/schemas/playcalling.py` are **missing**.

---

## 3. Telemetry & Latency Budgets

| Metric / Operation | Budget | Observed / Measured Performance | Compliance |
|---|---|---|---|
| **60Hz Physics Frame Calculation** | $< 16.67$ms per tick | Measured in `test_60hz_physics.py`: 600-frame full play executes in $< 10$ms total wall-clock time ($< 0.017$ms per frame). | ✅ PASS (Exceeds budget by $1000\times$) |
| **Telemetry Frame WebSocket Delivery** | $< 16.67$ms interval | Paced via `asyncio.sleep(DELTA_T)` in `physics_api.py`. Windows OS timer resolution (~15.6ms) causes slight jitter. Frame payload is compact (~823 bytes). | ⚠️ CONDITIONAL (Requires drift-compensating timer) |
| **4th-Down Recommendation Lookup** | $< 10$ms | Not currently exposed as an endpoint. In-memory heuristic calculations in `coaching_ai.py` resolve in $< 0.05$ms. An analytical Baldwin lookup model will easily satisfy $< 10$ms. | ⚠️ UNTESTED (Needs implementation) |
| **Locker Room Society Calculation** | $< 2$ms | Deterministic ODE math verified in `test_tension_engine.py` executes in $< 0.8$ms. | ✅ PASS |
| **Capology Multi-Year Proration** | $< 40$ms | Jimmy Johnson and Cap calculations execute in $< 5$ms in memory. | ✅ PASS |

---

## 4. Schema & Contract Parity Audit

### 4.1 Strict 1:1 Field Mapping Analysis

#### A. Medical Center Schemas

1. **`BodyHealthResponse` (`medical.py`) vs `BodyHealth` (`medical.ts`)**:
   - `player_id`: `int` $\leftrightarrow$ `number` (Match)
   - `head_health`, `neck_health`, `torso_health`, `right_arm_health`, `left_arm_health`, `right_leg_health`, `left_leg_health`, `general_wear`: `float` $\leftrightarrow$ `number` (Match)
   - `is_injured`: `bool` $\leftrightarrow$ `boolean` (Match)
   - *Parity Rating: 100% Structural Parity*.

2. **`InjuredPlayerResponse` (`medical.py`) vs `InjuredPlayer` (`medical.ts`)**:
   - `player_id`, `first_name`, `last_name`, `position`, `injury_type`, `injury_status`, `severity`: All match.
   - `weeks_remaining`: Matches `weeks_remaining` in TS and `p.weeks_to_recovery` in DB.
   - `body_part`: Present as optional in TypeScript `InjuredPlayer`, but omitted from backend `InjuredPlayerResponse`.

3. **`TriageDecisionResult` (`deep_dive.py`) vs `TriageDecisionResult` (`deepDive.ts`)**:
   - All 8 fields match 1:1 with exact types (`player_id`, `zone_key`, `protocol_applied`, `projected_recovery_weeks`, `complication_occurred`, `final_integrity_forecast`, `re_injury_risk_index`, `message`).
   - *Parity Rating: 100% Structural Parity*.

#### B. Physics & Telemetry Frame Schemas

1. **`PhysicsFrame` (`physics_api.py`) vs `PhysicsFrame` (`physics.ts`)**:
   - **Critical Structural Mismatch**:
     - `physics_api.py` uses flat fields on `PlayerPosition`: `x`, `y`, `velocity_x`, `velocity_y`.
     - `physics.ts` uses nested vector objects on `PlayerFrame`: `position: Vector2`, `velocity: Vector2`.
     - `PlayerPosition` in `physics_api.py` lacks `orientation: number`.
     - `BallPosition` in `physics_api.py` uses `x`, `y`, `height`, `is_in_air`, `carrier_id`.
     - `BallFrame` in `physics.ts` uses `position: Vector2`, `height`, `rotation`.
   - **Enum Values Mismatch**:
     - Backend `PlayerState`: `IDLE`, `RUNNING`, `BLOCKING`, `RUSHING`, `COVERING`, `ROUTE_RUNNING`, `TACKLING`, `TACKLED`, `CATCHING`, `HAS_BALL`.
     - Frontend `PlayerFrame.state`: `"IDLE" | "RUN" | "BLOCK" | "TACKLE" | "CELEBRATE" | "FALL"`.
   - **WebSocket Stream Shape**:
     - `physics_api.py` `/stream` outputs `id` instead of `player_id`.

#### C. Master Blueprint Domain Contracts

- In `docs/design_theory/nfl_simulation_blueprint/ui_design_system.md`:
  - 21 master domain models are specified in Python and TypeScript.
  - Verified by `scripts/verify_blueprint_contracts.py` and `scripts/check_field_parity.py` with 100% type parity.
  - **Gap**: Neither `backend/app/schemas/domain_contracts.py` nor `frontend/src/types/domain_contracts.ts` has been written to the actual codebase directories.

### 4.2 Audit of `any` Types

- Scanned `frontend/src/types/`: **0 instances of `any`**.
- Scanned `frontend/src/components/medical/`: **0 instances of `any`**.
- Scanned `frontend/src/pages/MedicalCenter.tsx`: **0 instances of `any`**.
- Scanned `frontend/src/pages/LiveSim.tsx`: **0 instances of `any`**.
- Frontend production build (`tsc -b && vite build`): **Compiled with 0 errors in 12.09s**.

---

## 5. Summary of Recommended Technical Action Items

1. **Medical Center Backend Remediation**:
   - Fix `medical.py:61`: Update `is_injured=player.injury_status != InjuryStatus.ACTIVE`.
   - Fix `medical_service.py:24, 70`: Replace `player.body_health[0]` with `player.body_health`.
   - Update `medical.py:apply_player_triage_protocol`: Persist `final_integrity_forecast` to `player.body_health` for the triaged zone and record an `InjuryEvent` in `injury_events`.
   - Add `body_part` calculation to `InjuredPlayerResponse` in `medical.py:get_team_injuries`.

2. **Medical Center Frontend Remediation**:
   - Remove hardcoded mock array from `MedicalCenter.tsx` and bind to `useTeamStore.getState().userTeamId` with `medicalApi.getTeamInjuries(teamId)`.
   - Implement zero-injury fallback view (Preventative Maintenance / Starter Wear).
   - Wire `OrthopedicTriageModal.tsx` to fetch protocols dynamically from `medicalApi.getPlayerTriageProtocols(playerId)`.
   - Update `handleProtocolConfirm` in `MedicalCenter.tsx` to call `medicalApi.applyOrthopedicTriage(playerId, request)`.

3. **In-Game Play-Calling HUD Implementation (TASK-013)**:
   - Create schemas: `backend/app/schemas/playcalling.py` and `frontend/src/types/playcalling.ts`.
   - Implement `backend/app/engine/fourth_down_calculator.py` with the Ben Baldwin expected win probability matrix for Go vs FG vs Punt.
   - Expose endpoint `POST /api/simulation/fourth-down-recommendation`.
   - Implement `PlayCallingHUD.tsx`, `FourthDownModal.tsx`, and `ClockManagementBar.tsx` in `frontend/src/components/game/`.
   - Mount HUD components into `frontend/src/pages/LiveSim.tsx` with a Coach Mode vs Spectator Mode toggle.
   - Update live simulation loop to support interactive pause on snap and accept play-call commands over WebSocket / REST.

4. **Telemetry & Schema Parity Alignment**:
   - Reconcile `PlayerPosition` in `physics_api.py` with `PlayerFrame` in `physics.ts` (unify on nested `position` / `velocity` or provide dual serialization).
   - Standardize `PlayerState` enum values between backend and frontend.
   - Implement drift compensation for the 60Hz WebSocket broadcast loop.

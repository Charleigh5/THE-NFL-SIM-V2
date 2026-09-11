## 2026-09-06T03:29:12Z

You are the Project Orchestrator for THE-NFL-SIM-V2 ("The Digital Gridiron").

Your working directory is:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_5pillar`
Maintain your `BRIEFING.md` and `progress.md` inside your working directory.

The authoritative user request is recorded in:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`
and `.agents\ORIGINAL_REQUEST.md`.

Workspace root: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2`
Integrity mode: demo

## Mission & Scope
Execute the 5-Pillar Architectural Review & Optimization Framework across four core subsystems in THE-NFL-SIM-V2:
1. Free Agency Market & Contract Bidding Hub (TASK-010)
2. Locker Room & Closed-Door Council UI (TASK-011)
3. Medical Center Live Roster & Surgical Triage Integration (TASK-012)
4. In-Game Play-Calling HUD (TASK-013)

Verify system health through automated static contract gates, operational latency benchmarks, domain boundary continuity, and empirical NFL statistical validation.

Requested Team Structure:
Decompose into parallel specialist tracks:
- Track 1: Contract/Capology Specialist
- Track 2: Frontend UI Virtualization Specialist
- Track 3: Physics/HUD Telemetry Specialist
- Track 4: QA/Validation Specialist

## Requirements
### R1. Type and Contract Parity Gate
Eliminate schema and naming drift between the FastAPI/Pydantic V2 backend and the React/TypeScript frontend. Disallow `any` types in TypeScript code. Validate that all API payloads and WebSocket frame schemas share strict 1:1 parity and discriminated unions across boundaries.
Tools: `python scripts/verify_blueprint_contracts.py`, `python scripts/check_field_parity.py`, `npm --prefix frontend run build`.

### R2. Subsystem Delivery and Integration
Implement and wire the full-stack features for the four target sprint modules:
1. **Interactive Free Agency Market (TASK-010)**: Real-time contract negotiations with NFL CBA-compliant signing bonus proration, post-June 1st cap splits, top-51 offseason rule, and multi-team concurrent AI GM bidding.
2. **Locker Room & Closed-Door Council UI (TASK-011)**: Deterministic Tier 1 locker-room morale/chemistry differential equations, council narrative events, and team dynamic telemetry.
3. **Medical Center & Surgical Triage (TASK-012)**: Anatomical injury triage, surgery vs. rehab decision paths, body health state transitions, and roster status synchronization.
4. **In-Game Play-Calling HUD (TASK-013)**: Interactive play-calling interface operational during 60Hz live physics simulation, integrated with Ben Baldwin 4th-down decision modeling (Go/Punt/FG).

### R3. Latency Budgets & UI Rendering Performance
Maintain strict operational performance thresholds:
- Live physics and telemetry frame delivery: <16ms (60 FPS)
- Capology multi-year proration and AI GM bidding resolution: <40ms
- Table and roster rendering for 1,500+ free agents and 53-man rosters: 60 FPS without frame drops, using virtualized list rendering
- 4th-down decision recommendation lookups: <10ms
- Locker room society chemistry evaluation: <2ms per team

### R4. Domain Boundary Continuity and Statistical Calibration
Ensure state mutations in one domain (e.g. physics injury, contract signing, morale shift) propagate through broadcast, dynasty, and medical layers to the UI without loss or desynchronization. Ensure Monte Carlo simulation outputs align with official NFL statistical distributions (yards per carry, pass completion rate, sack rate, and injury incidence).
Tools: `python scripts/test_domain_boundary_pipeline.py`, `python scripts/batch_simulator.py --games 100 --calibrate`, `python backend/scripts/run_statistical_validation.py`.

### R5. Architecture Records & Living System Dossiers
Document architectural trade-offs in formal Architecture Decision Records (ADRs) within `docs/decisions/`. Update `docs/FEATURE_STATUS_MATRIX.md` to reflect production readiness, and synchronize `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` with all player mechanic and injury state updates.

## Acceptance Criteria:
- `python scripts/verify_blueprint_contracts.py` passes with zero contract mismatches or schema discrepancies.
- `npm --prefix frontend run build` compiles with zero TypeScript errors under strict mode.
- `python scripts/test_domain_boundary_pipeline.py` succeeds across all domain boundaries (Physics -> Broadcast -> Medical -> WebSocket Frame).
- `python backend/scripts/benchmark_mcp.py` passes with all tested subsystems operating strictly within latency ceilings (<16ms telemetry, <40ms capology, <2ms society math).
- Roster and Free Agency views render with virtualized scrolling at a stable 60 FPS with >1,000 player records.
- `python scripts/batch_simulator.py --games 100 --calibrate` produces game stats conforming to NFL reference distribution bounds (YPC 4.1-4.4, Pass Completion 63.5-66.0%, Sack Rate 6.0-7.2%).
- New ADRs are recorded in `docs/decisions/` covering major architectural design choices.
- `docs/FEATURE_STATUS_MATRIX.md` reflects updated status for TASK-010 through TASK-013.
- `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` is updated and synchronized with implemented mechanics.

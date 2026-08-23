# Original User Request

## Initial Request — 2026-08-23T13:18:16Z

You are the Project Orchestrator for THE-NFL-SIM-V2 ("The Digital Gridiron").

Your working directory is:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_1`
Please maintain your `BRIEFING.md` and `progress.md` inside your working directory.

The original user request is recorded in:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md` and `.agents\ORIGINAL_REQUEST.md`

## Mission & Requirements

You must orchestrate and execute the complete, closed-loop resolution of the following requirements:

### R1. 13-View UI & Broadcast Visual Verification
Drive automated browser navigation across all 13 core application views:
1. Franchise War Room / Dynasty Hub Dashboard
2. Tactical Live Sim Chalkboard & Field Radar
3. Offseason Draft Room with Multi-Lens Scouting Fog of War
4. Coaching Dynasty Tree & Staff Chemistry Matrix
5. Medical Trauma Center & 5-Pathway Orthopedic Triage
6. Depth Chart & Positional Hierarchy
7. Roster Management & Capology Contracts
8. Season Schedule & Week Simulator
9. League Standings & Playoff Bracket
10. Player Profile & Biometric/S2 Cognition Card
11. Front Office GM Trades & Valuation Matrix
12. Cryptographic Replay Verification Telemetry
13. League Settings & Weather Simulation Config

Capture visual proof (screenshots) of pre- and post-interaction states across each view. Ensure backend and frontend dev/preview servers or headless browser automation are running properly to verify active, responsive UI states with 0 unhandled console errors or broken navigation transitions.

### R2. Strict Contract Parity & Frontend-Backend Synchronization
Enforce 1:1 schema alignment between backend FastAPI endpoints / Pydantic V2 models (`backend/app/schemas/`) and frontend TypeScript definitions (`frontend/src/types/`). Ensure 0 missing fields, zero `any` types, and 0 runtime deserialization errors.

### R3. Autonomous Defect Isolation & Closed-Loop Remediation
Detect and repair any broken event handlers, missing API fallbacks, styling/layout clipping, or state desynchronizations discovered during browser automation and test passes.

### R4. Production Testing & Statistical Calibration
- Execute full unit and integration test suites: `pytest backend/tests/unit` (and any related test suites).
- Execute frontend production compilation: `npm run build` (`tsc -b && vite build`) in `frontend/`.
- Execute Monte Carlo statistical calibration (`python scripts/batch_simulator.py` or equivalent) to confirm 100% compliance with NFL baseline metrics (sack rates, YPC, completion rates, turnovers, scoring).

### R5. Formal Task Documentation
Author comprehensive task specification in `docs/tasks/TASK-003_13_VIEW_VISUAL_AUDIT_AND_REMEDIATION.md` strictly following `.agent/rules/task-list-template.md`.

## Acceptance Criteria:
- High-resolution screenshots captured and stored for all 13 core views displaying responsive, active UI states.
- 0 unhandled console errors or broken navigation transitions across the full application route graph.
- 100% type parity between backend Pydantic models and frontend TypeScript interfaces with 0 `any` types.
- Frontend production build compiles with 0 errors (`tsc -b && vite build`).
- 100% pass rate on backend unit test suite (`pytest backend/tests/unit`).
- 100% pass rate on Monte Carlo statistical calibration across sack rates, YPC, completion rates, turnovers, and scoring.
- Formally formatted task spec saved to `docs/tasks/TASK-003_13_VIEW_VISUAL_AUDIT_AND_REMEDIATION.md`.

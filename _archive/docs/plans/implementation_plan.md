# Implementation Plan - Phase 3: Simulation Persistence & Data Integrity

## Goal Description

Ensure that the simulation data (plays, game state, simulation requests) is correctly persisted to the database and that the frontend accurately reflects this persisted state. This follows the completion of Phase 2 (Visual Regression Testing).

## User Review Required

> [!IMPORTANT]
> This plan assumes that Phase 2 (Visual Regression Testing) is complete or near completion. Please verify the status of `frontend/docs/visual-regression-testing-plan.md` before proceeding fully with Phase 3.

## Proposed Changes

### Backend

#### [NEW] [test_persistence.py](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/backend/tests/test_persistence.py)

- Create a new test file to explicitly verify database persistence.
- **Tests to include:**
  - `test_save_simulation_request`: Verify `SimulationRequest` is saved to DB.
  - `test_save_play_result`: Verify `PlayResult` is saved to DB after a play is resolved.
  - `test_game_state_persistence`: Verify game state (score, time, etc.) is updated in DB.

#### [MODIFY] [simulation_orchestrator.py](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/backend/app/orchestrator/simulation_orchestrator.py)

- Review and ensure `save_play_result` and `update_game_state` methods are correctly calling the repository/DB layer.
- Add logging for successful persistence to aid debugging.

### Frontend

#### [MODIFY] [LiveSim.tsx](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/frontend/src/pages/LiveSim.tsx)

- Verify that the component fetches initial state from the backend if a simulation is resumed.
- Ensure that data received via WebSocket is consistent with what would be fetched from the DB.

## Verification Plan

### Automated Tests

- Run the new persistence tests:

  ```bash
  pytest backend/tests/test_persistence.py
  ```

- Run existing tests to ensure no regressions:

  ```bash
  pytest backend/tests
  ```

### Manual Verification

1. **Start the Application**:
   - Backend: `uvicorn backend.app.main:app --reload`
   - Frontend: `npm run dev`
2. **Run a Simulation**:
   - Navigate to the Live Sim page.
   - Start a simulation.
   - Let it run for a few plays.
3. **Verify DB Persistence**:
   - Stop the backend.
   - Inspect the SQLite database (`backend/nfl_sim.db`) using a tool or script to confirm rows exist in `play_results` and `simulation_requests`.
4. **Verify Frontend Consistency**:
   - Restart the backend.
   - Reload the Live Sim page.
   - Verify that the game state (score, time) is restored (if resume functionality is implemented) or that the history is visible.

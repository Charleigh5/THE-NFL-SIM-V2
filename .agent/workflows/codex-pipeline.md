---
description: Automated 6-stage engineering lifecycle runner (Research, Synthesize, Write, Review, Critique, Advance) per task-list-template.md
---

# Codex Pipeline Workflow

Execute the autonomous 6-stage cognitive engineering loop for any feature or subsystem in **THE-NFL-SIM-V2 ("The Digital Gridiron")**.

## Steps

1. **Invoke Task Specification Generator**:
   Run `scripts/codex_pipeline_runner.py` with the required Task ID and Title:
   ```powershell
   python scripts/codex_pipeline_runner.py --id <TASK_ID> --title "<Feature Title>"
   ```

2. **Phase 1: Conceptual Exploration & Phase 2: Adversarial Synthesis**:
   - Inspect the generated task markdown in `docs/tasks/<TASK_ID>_<feature_name>.md`.
   - Formulate the *Primary Thesis*, attack with *Powerful Antithesis*, and lock the *Superior Synthesis*.

3. **Phase 3: Write Production Code**:
   - Implement the core logic with strict typing and 100% test coverage.
   - Synchronize schemas between `backend/app/schemas/` and `frontend/src/types/`.

4. **Phase 4: The Auditor & Test Verification**:
   - Run backend unit tests:
     ```powershell
     pytest backend/tests/unit -q
     ```
   - Verify static typing with Pyright and ESLint.

5. **Phase 5: Critique & Calibration**:
   - Run Monte Carlo batch simulations:
     ```powershell
     python scripts/batch_simulator.py --games 1000 --calibrate
     ```

6. **Phase 6: Advance & Dossier Sync**:
   - Update `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` or `docs/game-engine/GAME_ENGINE_DOSSIER.md`.
   - Update `docs/FEATURE_STATUS_MATRIX.md` with the new feature status (`🎯 PRODUCTION_READY`).

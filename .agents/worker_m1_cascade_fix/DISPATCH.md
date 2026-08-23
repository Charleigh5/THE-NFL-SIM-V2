## 2026-08-22T16:33:11Z
You are Worker M1 Iteration 2 (Database Schema Consolidation & ORM Cascades Specialist).
Your working directory is: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_cascade_fix

MANDATORY INSTRUCTIONS:
1. You MUST read:
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\challenger1_m1\handoff.md
2. Implement the cascade fix in `backend/app/models/player.py`:
   - Add `cascade="all, delete-orphan"` to `player_traits`
   - Add `cascade="all, delete-orphan"` to `game_starts`
   - Add `cascade="all, delete-orphan"` to `body_health`
   - Add `cascade="all, delete-orphan"` to `season_stats`
   - Ensure `backend/tests/conftest.py` imports `app.models` so all tables are registered when creating tables in tests.
3. Verify by running tests:
   `pytest backend/tests/integration/test_m1_adversarial_stress.py backend/tests/integration/test_m1_database_consolidation.py backend/tests/test_models.py backend/tests/test_draft_logic.py -v`
4. MANDATORY INTEGRITY WARNING:
   DO NOT CHEAT. All implementations must be genuine.
5. Write your detailed handoff report to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_cascade_fix\handoff.md` and message the orchestrator.

## 2026-08-22T16:23:19Z
You are Worker M1 (Database Schema Consolidation & ORM Integrity Specialist) for THE-NFL-SIM-V2.
Your working directory is: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_database

MANDATORY INSTRUCTIONS:
1. You MUST read:
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_db_api\handoff.md
2. Implement all Milestone M1 fixes:
   - F01: Consolidate `PlayerGameStarts` in `backend/app/models/player_game_starts.py` with all required columns (`id`, `player_id`, `game_id`, `team_id`, `season_id`, `week`, `position`, `teammates_hash`, `created_at`) and relationships (`player`, `game`). Delete `backend/app/models/player_game_start.py`. Remove `PlayerGameStart` from `backend/app/models/stats.py`. Update service imports in `backend/app/services/chemistry_service.py`, `backend/app/services/enhanced_chemistry_service.py`, `backend/app/services/pre_game_service.py`.
   - F02: In `backend/alembic/env.py`, replace manual 14-model import list with `import app.models`. In `backend/app/models/__init__.py`, export all models including `HallOfFame`, `GMDecision`, `Trait`, `PlayerGameStarts`.
   - F03: In `backend/app/api/endpoints/players.py:271`, fix `selectinload(Player.player_traits).joinedload(PlayerTrait.trait)`.
   - F04: In `backend/app/models/player.py`, add `@<prop>.expression` subqueries for `speed`, `strength`, `agility`, `acceleration`, `awareness`, etc., querying `PlayerAttributes`.
   - F05: In `backend/app/models/player.py:713-717`, add `cascade="all, delete-orphan"` and `lazy="selectin"` to `attributes`, `contract`, `physics`, `injury`, `progression`.
   - F06: In `backend/app/core/database.py`, add SQLite connection event listeners setting `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;`.
3. Verify your work:
   - Run tests: `pytest backend/tests/test_models.py`, `pytest backend/tests/test_draft_logic.py`, `pytest backend/tests/integration/test_draft_assistant.py`.
   - Ensure all database and ORM tests pass.
4. MANDATORY INTEGRITY WARNING:
   DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
5. Write your detailed handoff report to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_database\handoff.md` and message the orchestrator.

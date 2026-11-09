# Codebase Review Report

## Frontend Issues

### TypeScript Issues
No TypeScript issues found during `npx tsc -b --force`.

### ESLint Issues
No ESLint issues found remaining (resolved them locally during audit).

## Backend Python Issues (Ruff)

Found 2289 Ruff issues. To prevent the file from being too large, here is a sampling of the 50 most common issues and how to solve them:

- **File**: `/app/_archive/alien_code/main.py`
  - **Line**: 30
  - **Error**: f-string without any placeholders (F541)
  - **Proposed Solve**: Remove the 'f' prefix from the string since it has no placeholders. `content = "string without f"`

- **File**: `/app/_archive/dead_code/simulation_orchestrator.py`
  - **Line**: 145
  - **Error**: Multiple statements on one line (colon) (E701)
  - **Proposed Solve**: Move the statement after the colon to a new line. `if condition:
    do_something()`

- **File**: `/app/_archive/dead_code/simulation_orchestrator.py`
  - **Line**: 272
  - **Error**: Multiple statements on one line (colon) (E701)
  - **Proposed Solve**: Move the statement after the colon to a new line. `if condition:
    do_something()`

- **File**: `/app/_archive/dead_code/simulation_orchestrator.py`
  - **Line**: 452
  - **Error**: Multiple statements on one line (colon) (E701)
  - **Proposed Solve**: Move the statement after the colon to a new line. `if condition:
    do_something()`

- **File**: `/app/_archive/dead_code/simulation_orchestrator.py`
  - **Line**: 453
  - **Error**: Multiple statements on one line (colon) (E701)
  - **Proposed Solve**: Move the statement after the colon to a new line. `if condition:
    do_something()`

- **File**: `/app/_archive/dead_code/simulation_orchestrator.py`
  - **Line**: 454
  - **Error**: Multiple statements on one line (colon) (E701)
  - **Proposed Solve**: Move the statement after the colon to a new line. `if condition:
    do_something()`

- **File**: `/app/_archive/dead_code/training.py`
  - **Line**: 17
  - **Error**: `app.services.training.drills.Drill` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/dead_code/training.py`
  - **Line**: 27
  - **Error**: `app.services.training.coaching_philosophy.CoachingStyle` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/dead_code/training.py`
  - **Line**: 28
  - **Error**: `app.services.training.coaching_philosophy.CoachingStyleName` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 16
  - **Error**: `typing.List` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 295
  - **Error**: Undefined name `Any` (F821)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 302
  - **Error**: Undefined name `Any` (F821)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 330
  - **Error**: Local variable `max_cut` is assigned to but never used (F841)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 456
  - **Error**: Undefined name `Any` (F821)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/legacy_engine/position_physics.py`
  - **Line**: 587
  - **Error**: Undefined name `Any` (F821)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/check_db_state.py`
  - **Line**: 12
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/check_db_state.py`
  - **Line**: 13
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/check_db_state.py`
  - **Line**: 14
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/check_standings.py`
  - **Line**: 1
  - **Error**: `app.services.standings_calculator.StandingsCalculator` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 12
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 13
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 14
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 15
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 16
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_db_state.py`
  - **Line**: 17
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/fix_task_linting.py`
  - **Line**: 1
  - **Error**: `os` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/inspect_mcp.py`
  - **Line**: 2
  - **Error**: `inspect` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_match_context.py`
  - **Line**: 105
  - **Error**: Do not use bare `except` (E722)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/verify_mcp_servers.py`
  - **Line**: 8
  - **Error**: `backend.mcp_servers.nfl_stats_server.server` imported but unused; consider using `importlib.util.find_spec` to test for availability (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_mcp_servers.py`
  - **Line**: 12
  - **Error**: `backend.mcp_servers.weather_server.server` imported but unused; consider using `importlib.util.find_spec` to test for availability (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_mcp_servers.py`
  - **Line**: 16
  - **Error**: `backend.mcp_servers.sports_news_server.server` imported but unused; consider using `importlib.util.find_spec` to test for availability (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_offseason_flow.py`
  - **Line**: 34
  - **Error**: `random` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_offseason_flow.py`
  - **Line**: 39
  - **Error**: f-string without any placeholders (F541)
  - **Proposed Solve**: Remove the 'f' prefix from the string since it has no placeholders. `content = "string without f"`

- **File**: `/app/_archive/scripts/verify_offseason_flow.py`
  - **Line**: 91
  - **Error**: Comparison to `None` should be `cond is None` (E711)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/verify_offseason_flow.py`
  - **Line**: 130
  - **Error**: Do not use bare `except` (E722)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/_archive/scripts/verify_omniscient_system.py`
  - **Line**: 3
  - **Error**: `unittest` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_omniscient_system.py`
  - **Line**: 52
  - **Error**: f-string without any placeholders (F541)
  - **Proposed Solve**: Remove the 'f' prefix from the string since it has no placeholders. `content = "string without f"`

- **File**: `/app/_archive/scripts/verify_playoff_flow.py`
  - **Line**: 16
  - **Error**: `app.services.standings_calculator.StandingsCalculator` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/_archive/scripts/verify_playoff_flow.py`
  - **Line**: 133
  - **Error**: f-string without any placeholders (F541)
  - **Proposed Solve**: Remove the 'f' prefix from the string since it has no placeholders. `content = "string without f"`

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 1
  - **Error**: Import block is un-sorted or un-formatted (I001)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 16
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 16
  - **Error**: Import block is un-sorted or un-formatted (I001)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 17
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 18
  - **Error**: Module level import not at top of file (E402)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/env.py`
  - **Line**: 18
  - **Error**: `app.models` imported but unused (F401)
  - **Proposed Solve**: Remove the unused import statement.

- **File**: `/app/backend/alembic/versions/00d0f05763a5_add_proposed_feature_enhancements_and_.py`
  - **Line**: 8
  - **Error**: Import from `collections.abc` instead: `Sequence` (UP035)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/versions/00d0f05763a5_add_proposed_feature_enhancements_and_.py`
  - **Line**: 8
  - **Error**: Import block is un-sorted or un-formatted (I001)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/versions/00d0f05763a5_add_proposed_feature_enhancements_and_.py`
  - **Line**: 16
  - **Error**: Use `X | Y` for type annotations (UP007)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/versions/00d0f05763a5_add_proposed_feature_enhancements_and_.py`
  - **Line**: 17
  - **Error**: Use `X | Y` for type annotations (UP007)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

- **File**: `/app/backend/alembic/versions/00d0f05763a5_add_proposed_feature_enhancements_and_.py`
  - **Line**: 18
  - **Error**: Use `X | Y` for type annotations (UP007)
  - **Proposed Solve**: Run `ruff check --fix` to automatically resolve this formatting issue.

## Missing Documentation & Files Audit

The codebase appears to have comprehensive documentation, including README.md, PROJECT.md, and various guides. A full check of all individual source files for inline documentation was not performed, but high-level project documentation is present.
No obvious missing files based on typical project structure.

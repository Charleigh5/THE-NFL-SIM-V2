# Code Review Report

**To:** cweir45@gmail.com
**Date:** 2025-05-15
**Subject:** Comprehensive Code Review & Bug Report

## Summary

A comprehensive review of the `backend` and `frontend` codebases was conducted. The analysis utilized static type checking (`mypy`), linting (`ruff`), and manual verification of critical logic paths.

**Key Findings:**
- **Critical Runtime Errors:** Found in the simulation orchestrator (missing `await`) and play calling logic (undefined names causing `NameError`).
- **Type Safety Violations:** Significant number of type mismatches in data files (`scouts.py`) and calculation services.
- **Code Redundancy:** Duplicate function definitions in `weather.py` and `season.py`.
- **Frontend Gaps:** The Draft Room loader is currently using hardcoded mock data instead of the API.
- **Missing Configuration:** `AGENTS.md` and `apts/__init__.py` are missing.

---

## Detailed Findings & Solves

### 1. Backend: Critical Logic Bugs

| File | Line(s) | Error | Proposed Solve |
|------|---------|-------|----------------|
| `backend/app/orchestrator/simulation_orchestrator.py` | 425 | **RuntimeWarning/Bug:** Synchronous method `run_simulation` calls async method `_save_progress` without `await`. This results in progress not being saved. | **Convert method to async or use `asyncio.run` (recommended async conversion):**<br><br>```python<br>async def run_simulation(self) -> PlayResult:<br>    # ... (existing code)<br>    logger.debug("Play resolved")<br><br>    await self._save_progress()<br><br>    return result<br>``` |
| `backend/app/orchestrator/play_caller.py` | 152 | **NameError:** Type hint `qb: "Player"` uses a forward reference, but `Player` is not imported at module scope for runtime resolution in some contexts, and `from app.models.player import Player` is inside the function. | **Move import to top of file with `TYPE_CHECKING`:**<br><br>```python<br>from typing import TYPE_CHECKING<br>if TYPE_CHECKING:<br>    from app.models.player import Player<br><br># ...<br>def call_audible(<br>    self,<br>    qb: "Player",<br>    # ...<br>``` |
| `backend/app/kernels/genesis/trauma_center.py` | 21 | **NameError:** Argument `anatomy: 'AnatomyModel'` references undefined class. | **Import the missing model:**<br><br>```python<br>from typing import TYPE_CHECKING<br>if TYPE_CHECKING:<br>    from app.models.medical import AnatomyModel<br>``` |
| `backend/app/kernels/core/sim_engine.py` | 25-26 | **NameError:** `PhysicsKernel` and `AIKernel` are undefined in type hints. | **Add `TYPE_CHECKING` imports:**<br><br>```python<br>from typing import TYPE_CHECKING<br>if TYPE_CHECKING:<br>    from app.kernels.core.physics_kernel import PhysicsKernel<br>    from app.kernels.core.ai_kernel import AIKernel<br>``` |
| `backend/app/api/endpoints/season.py` | 392 | **NameError:** `timedelta` is used but not imported (only `datetime` is imported). | **Add import:**<br><br>```python<br>from datetime import datetime, timedelta<br>``` |

### 2. Backend: Code Quality & Redundancy

| File | Line(s) | Error | Proposed Solve |
|------|---------|-------|----------------|
| `backend/app/api/endpoints/season.py` | 893, 1172 | **Redefinition:** Function `suggest_draft_pick` is defined twice with different signatures. | **Rename one or merge logic.**<br><br>Rename the second one (line 1172) to `suggest_draft_pick_ai` or similar, and ensure route paths are unique.<br>```python<br>@router.post("/draft/suggest-pick-ai", ...)<br>async def suggest_draft_pick_ai(...):<br>``` |
| `backend/app/kernels/hive/weather.py` | 20-40, 63+ | **Redefinition:** Methods `get_ballistic_modifiers` etc. are defined as stubs and then immediately redefined below. | **Remove the empty stub definitions** (lines 20-40) and keep the implemented versions. |
| `backend/app/models/player.py` | 76-657 | **Redefinition:** Attributes like `speed`, `acceleration` appear to be defined twice (likely once as Column/Field and once as hybrid_property or similar). | **Review SQLAlchemy definitions.** Ensure `Mapped[...]` is used correctly and `hybrid_property` names do not conflict with column names if they are meant to proxy them. |

### 3. Backend: Type Safety

| File | Line(s) | Error | Proposed Solve |
|------|---------|-------|----------------|
| `backend/app/data/scouts.py` | 28+ | **Type Mismatch:** `ScoutData` defines `specialty` as `str`, but `None` is passed in `TEAM_SCOUTS`. | **Update Dataclass Definition:**<br><br>```python<br>from typing import Optional<br>@dataclass<br>class ScoutData:<br>    # ...<br>    specialty: Optional[str]<br>``` |
| `backend/app/services/rating_calculator.py` | 297 | **Type Mismatch:** Mypy detects `float | Any` assigned to `int`. | **Explicit Cast:**<br><br>```python<br>return int(max(40, min(99, int(total / len(core_attrs)))))<br>``` |

### 4. Frontend: Functionality & Documentation

| File | Line(s) | Error | Proposed Solve |
|------|---------|-------|----------------|
| `frontend/src/router.tsx` | ~160 | **Mock Data:** `draftRoomLoader` returns hardcoded mock data. | **Connect to API:**<br><br>```typescript<br>export async function draftRoomLoader() {<br>  const teams = await api.getTeams();<br>  const season = await seasonApi.getCurrentSeason();<br>  const currentPick = await seasonApi.getCurrentDraftPick(season.id);<br>  return { teams, season, currentPick, noSeason: false };<br>}<br>``` |
| `frontend/src/services/api.ts` | All | **Documentation:** Missing JSDoc for exported API methods. | **Add JSDoc comments** specifying parameters and return types for all methods in `api` object. |

### 5. Missing Files

| File | Description | Solve |
|------|-------------|-------|
| `AGENTS.md` | Missing agent instructions file. | Create `AGENTS.md` with project coding standards and instructions. |
| `apts/__init__.py` | Missing package initialization file. | Create empty `apts/__init__.py` to allow package importing. |

---

**Next Steps:**
It is recommended to apply the "Solves" listed above immediately to restore build stability and prevent runtime crashes in the simulation engine.

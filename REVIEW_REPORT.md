# Code Review Report
**To:** cweir45@gmail.com
**Date:** 2024-05-23
**Subject:** Comprehensive Codebase Review

## Summary
A comprehensive review of the `backend` and `frontend` codebase was performed. Several issues were identified ranging from type safety errors, potential runtime bugs, deprecated usage, and missing documentation. Below is a detailed list of findings with proposed solutions.

---

## Backend Issues

### 1. Missing Type Annotations
**File:** `backend/app/services/standings_calculator.py`
**Lines:** ~226, ~239
**Error:** `mypy` error `Need type annotation for "divisions"` and `"conferences"`. The variables are initialized as empty dictionaries without type hints.
**Proposed Solution:**
```python
# backend/app/services/standings_calculator.py

# ... inside _assign_ranks method
    divisions: Dict[str, List[Dict]] = {}
    # ...
    conferences: Dict[str, List[Dict]] = {}
```

### 2. Potential Type Mismatch (Float vs Int)
**File:** `backend/app/services/rating_calculator.py`
**Lines:** ~297 (in `calculate_overall_rating`)
**Error:** `mypy` flags incompatible types in assignment where a float might be assigned to an int variable or vice versa during calculation.
**Proposed Solution:**
Ensure explicit casting to `int` before returning, which is already present but might need clarification for the type checker or strict handling of intermediate variables.
```python
# backend/app/services/rating_calculator.py

# ... inside calculate_overall_rating
    if total_weight > 0:
        raw_rating = weighted_sum / total_weight
    else:
        raw_rating = 50.0  # Ensure float

    # Clamp to valid range
    return int(max(40, min(99, round(raw_rating))))
```

### 3. Type Mismatch in Chemistry Calculation
**File:** `backend/app/services/society/social_graph.py`
**Lines:** ~149, ~151 (in `get_chemistry_score`)
**Error:** Variables `positive_rels` and `negative_rels` are initialized as `0` (int) but are added with `float` values, causing type inference issues.
**Proposed Solution:**
Initialize them as floats.
```python
# backend/app/services/society/social_graph.py

# ... inside get_chemistry_score
    total_rels = 0
    positive_rels = 0.0  # Initialize as float
    negative_rels = 0.0  # Initialize as float
```

### 4. JSON Parsing Vulnerability
**File:** `backend/app/services/ai/gemini_client.py`
**Lines:** ~160 (in `generate_structured`)
**Error:** `json.loads(response.text)` is called without verifying if `response.text` is `None` or empty. `response.text` can be `None` if generation fails.
**Proposed Solution:**
Add a check before parsing.
```python
# backend/app/services/ai/gemini_client.py

# ... inside generate_structured
    if not response.text:
        logger.error("Empty response from Gemini")
        return None

    import json
    data = json.loads(response.text)
    return response_schema.model_validate(data)
```

### 5. Duplicate Function Definition
**File:** `backend/app/api/endpoints/season.py`
**Lines:** ~893 and ~1172
**Error:** The function `suggest_draft_pick` is defined twice with different signatures. The second definition overwrites the first.
**Proposed Solution:**
Rename one of the functions to be unique, e.g., `suggest_draft_pick_legacy` or `suggest_draft_pick_api`.
```python
# backend/app/api/endpoints/season.py

# First definition (around line 893)
@router.post("/{season_id}/draft/suggest-pick")
@handle_errors
async def suggest_draft_pick_legacy(season_id: int, team_id: int, db: AsyncSession = Depends(get_async_db)):
    # ... implementation ...
```

### 6. Deprecated Typing and Unused Imports
**File:** `backend/app/api/combine.py`
**Lines:** 14
**Error:** Usage of `typing.List` is deprecated (use `list`). Unused imports `Optional` and `CombineResults`.
**Proposed Solution:**
```python
# backend/app/api/combine.py

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional # Keep if used, remove if not.
# Use built-in list instead of typing.List if on Python 3.9+
from app.services.scouting.combine import (
    CombineSimulation,
    GenesisRevealData,
)
```

### 7. Synchronous Method Calling Async
**File:** `backend/app/orchestrator/simulation_orchestrator.py`
**Lines:** ~435 (in `run_simulation`)
**Error:** The synchronous method `run_simulation` calls the asynchronous method `self._save_progress()` without `await` (and cannot `await` it). This results in the coroutine never being scheduled.
**Proposed Solution:**
Convert `run_simulation` to `async` or use `asyncio.create_task` (if fire-and-forget is acceptable, though risky) or run in an event loop. Given `simulation_orchestrator.py` uses `async` heavily, making it `async` is best.
```python
# backend/app/orchestrator/simulation_orchestrator.py

    async def run_simulation(self) -> PlayResult: # Changed to async
        self.is_running = True
        logger.debug("Setting up simulation scenario: Pass Play")
        # ...
        await self._save_progress() # Added await
        return result
```

---

## Frontend Issues

### 1. Missing Documentation (JSDoc)
**File:** `frontend/src/services/api.ts`
**Error:** Exported methods like `getTeams`, `getPlayer`, etc., lack JSDoc comments explaining parameters and return types.
**Proposed Solution:**
Add JSDoc comments.
```typescript
// frontend/src/services/api.ts

  /**
   * Fetch a paginated list of teams.
   * @param page - Page number (default 1)
   * @param pageSize - Number of items per page (default 100)
   * @returns Array of Team objects
   */
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
    // ...
  },
```

### 2. Hardcoded Mock Data
**File:** `frontend/src/router.tsx`
**Lines:** ~140 (in `draftRoomLoader`)
**Error:** The `draftRoomLoader` returns hardcoded mock data instead of fetching from the API.
**Proposed Solution:**
Replace mock data with API calls.
```typescript
// frontend/src/router.tsx

export async function draftRoomLoader() {
  try {
     const teams = await api.getTeams();
     const season = await seasonApi.getCurrentSeason();
     const currentPick = await seasonApi.getCurrentDraftPick(season.id); // Assuming this method exists
     return { teams, season, currentPick, noSeason: false };
  } catch (e) {
     console.error("Failed to load draft room data", e);
     throw new Response("Failed to load draft room data", { status: 500 });
  }
}
```

---

## Missing Documentation & Files

The following files/directories were found to be missing or require attention:
1.  **`docs/architecture`**: Directory missing. Expected to contain architectural diagrams/notes.
2.  **`docs/data`**: Directory missing. Expected to contain data schemas or reference data.
3.  **`AGENTS.md`**: File missing. Expected to contain instructions for AI agents.
4.  **`scripts/check_docs.py`**: Script missing. Expected to be a utility for verifying documentation coverage.

**Recommendation:** Restore these files from backup or recreate them to ensure project maintainability.

---

## General Recommendations
1.  **Type Safety:** Enable stricter `mypy` checks and address the `import-not-found` errors by installing missing stubs or correcting environment paths.
2.  **Frontend Linting:** Address the lack of output from `tsc`/`eslint` by ensuring dependencies are correctly installed and configuration files are valid.
3.  **Code Cleanup:** Remove deprecated `typing` usages and unused imports across the backend.

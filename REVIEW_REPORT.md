# Code Review Report

**To:** cweir45@gmail.com
**Date:** 2024-05-22
**Subject:** Comprehensive Code Review Findings

## Executive Summary

This report outlines the findings from a comprehensive review of the `backend/` and `frontend/` codebases. Automated tools (`ruff`, `mypy`, `eslint`, `tsc`) were used alongside manual inspection.

**Summary of Findings:**
*   **Backend (Python/FastAPI):**
    *   **Critical Bugs:** 1 (Async call in synchronous function)
    *   **Logic Errors:** 2 (Function redefinition, Return type mismatch)
    *   **Linting Errors:** 943 (primarily imports and whitespace)
    *   **Type Errors:** 234 (missing imports, `None` handling)
*   **Frontend (React/TypeScript):**
    *   **Critical Issues:** 0
    *   **Code Quality:** Missing JSDoc documentation for API services.
    *   **Logic:** Hardcoded mock data used in production routes.

---

## 1. Critical Bugs (High Priority)

### 1.1 Synchronous Call to Async Method
**File:** `backend/app/orchestrator/simulation_orchestrator.py`
**Line:** 425
**Error:** The synchronous method `run_simulation` calls the asynchronous method `self._save_progress()` without `await`. This results in a `RuntimeWarning` and the progress is **not saved** to the database.

**Proposed Solve:**
Convert `run_simulation` to an async method and await the call.

```python
<<<<<<< SEARCH
    def run_simulation(self) -> PlayResult:
        """
        Sets up and runs a simple simulation of a single pass play.
        (Legacy method for backward compatibility)
        """
        self.is_running = True
=======
    async def run_simulation(self) -> PlayResult:
        """
        Sets up and runs a simple simulation of a single pass play.
        (Legacy method for backward compatibility)
        """
        self.is_running = True
>>>>>>> REPLACE
```

And update the call site:
```python
<<<<<<< SEARCH
        self._save_progress()

        return result
=======
        await self._save_progress()

        return result
>>>>>>> REPLACE
```

---

## 2. Logic & Architecture Errors (Medium Priority)

### 2.1 Function Redefinition Shadowing
**File:** `backend/app/api/endpoints/season.py`
**Line:** 1172 (and 893)
**Error:** The function `suggest_draft_pick` is defined twice in the module. The second definition (line 1172) overwrites the first (line 893). This can lead to unexpected behavior depending on import order and decorator registration.

**Proposed Solve:**
Rename the second function to clarify its distinct purpose (it uses the AI Assistant).

```python
<<<<<<< SEARCH
@router.post("/draft/suggest-pick", response_model=draft_schemas.DraftSuggestionResponse)
@handle_errors
async def suggest_draft_pick(
    request: draft_schemas.DraftSuggestionRequest,
    db: AsyncSession = Depends(get_async_db)
):
=======
@router.post("/draft/suggest-pick", response_model=draft_schemas.DraftSuggestionResponse)
@handle_errors
async def suggest_draft_pick_ai(
    request: draft_schemas.DraftSuggestionRequest,
    db: AsyncSession = Depends(get_async_db)
):
>>>>>>> REPLACE
```

### 2.2 Incorrect Return Type Annotation
**File:** `backend/app/services/week_simulator.py`
**Line:** 101
**Error:** The method `simulate_week` is annotated to return `Dict[int, Dict]`, but it returns a dictionary with mixed keys (`"week"`, `"games_simulated"`, `"results"`), which corresponds to `Dict[str, Any]`.

**Proposed Solve:**
Update the type hint to reflect the actual return structure.

```python
<<<<<<< SEARCH
    async def simulate_week(
        self,
        season_id: int,
        week: int,
        play_count: int = 100,
        use_fast_sim: bool = True
    ) -> Dict[int, Dict]:
=======
    async def simulate_week(
        self,
        season_id: int,
        week: int,
        play_count: int = 100,
        use_fast_sim: bool = True
    ) -> Dict[str, Any]:
>>>>>>> REPLACE
```

### 2.3 Implicit Optional Types
**File:** `backend/app/rpg/injury_system.py`
**Line:** 12
**Error:** Argument `seed` defaults to `None` but is typed as `int`. Modern MyPy (strict mode) flags this as an error.

**Proposed Solve:**
Use `Optional[int]` or `int | None`.

```python
<<<<<<< SEARCH
    def __init__(self, seed: int = None):
=======
    def __init__(self, seed: Optional[int] = None):
>>>>>>> REPLACE
```

---

## 3. Frontend Issues (Low Priority)

### 3.1 Hardcoded Mock Data in Production Route
**File:** `frontend/src/router.tsx`
**Line:** 135
**Error:** The `draftRoomLoader` function returns hardcoded mock data instead of fetching from the API. This will cause the Draft Room to display incorrect data in production.

**Proposed Solve:**
Replace mock data with `seasonApi` calls.

```typescript
<<<<<<< SEARCH
// Draft Room Loader
export async function draftRoomLoader() {
  // Mock data for UI verification
  const mockTeams: Team[] = [
    {
      id: 1,
...
  return {
    teams: mockTeams,
    season: mockSeason,
    currentPick: mockCurrentPick,
    noSeason: false,
  };
}
=======
// Draft Room Loader
export async function draftRoomLoader() {
  try {
    const summary = await seasonApi.getSeasonSummary();
    const currentPick = await seasonApi.getCurrentPick(summary.season.id);
    const teams = await api.getTeams();

    return {
      teams,
      season: summary.season,
      currentPick,
      noSeason: false
    };
  } catch (error) {
    console.error("Failed to load draft room data:", error);
    return {
      teams: [],
      season: null,
      currentPick: null,
      noSeason: true
    };
  }
}
>>>>>>> REPLACE
```

### 3.2 Missing JSDoc Documentation
**File:** `frontend/src/services/api.ts`
**Line:** Entire file
**Error:** Exported methods like `getTeams`, `getPlayer` lack documentation explaining parameters and return values.

**Proposed Solve:**
Add JSDoc comments.

```typescript
<<<<<<< SEARCH
  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await apiClient.get(`/api/players/${playerId}`);
    return response.data;
  },
=======
  /**
   * Fetches a player's profile by ID.
   * @param playerId - The unique ID of the player.
   * @returns Promise resolving to the Player object.
   */
  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await apiClient.get(`/api/players/${playerId}`);
    return response.data;
  },
>>>>>>> REPLACE
```

---

## 4. Missing Files & Documentation

*   **`docs/architecture/`**: Directory is referenced but missing.
*   **`docs/data/`**: Directory is referenced but missing.
*   **`AGENTS.md`**: File is missing from the root directory.

**Recommendation:** Create these directories and file to align with project structure expectations.

---

## 5. Automated Check Summary

### Backend
*   **Linting (Ruff):** 943 errors found. Most are auto-fixable (imports, whitespace).
    *   *Action:* Run `ruff check backend/ --fix`.
*   **Type Checking (MyPy):** 234 errors found.
    *   *Action:* Address missing type stubs (`types-aiofiles`) and fix `None` handling.

### Frontend
*   **Linting (ESLint):** 0 errors reported (verify config).
*   **Type Checking (TSC):** 0 errors reported.

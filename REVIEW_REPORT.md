To: cweir45@gmail.com

# Code Review Report

## Executive Summary
A comprehensive review of the codebase was performed, covering backend (Python/FastAPI) and frontend (React/TypeScript). The review identified several critical bugs, type safety issues, missing documentation, and structural inconsistencies.

## 1. Critical Bugs & Logic Errors

### Backend
**File:** `backend/app/engine/core/enhanced_event_bus.py`
**Line:** 105
**Issue:** `AsyncHandler` type definition causes `mypy` errors when using `loop.create_task` because `asyncio.Future[None]` is not compatible with `Coroutine`.
**Proposed Solve:**
```python
from typing import Awaitable

# Update the type definition
AsyncHandler = Callable[[GameEvent], Awaitable[None]]
```

**File:** `backend/app/orchestrator/simulation_orchestrator.py`
**Line:** 219 (and others accessing `self.db_session`)
**Issue:** `self.db_session` is `Optional[AsyncSession]` but accessed without strict narrowing in some contexts, causing potential runtime errors if the session is `None` (though often guarded, static analysis flags it).
**Proposed Solve:**
```python
# Use local variable for narrowing
async def _save_progress(self) -> None:
    session = self.db_session
    if not session or not self.current_game_id:
        return

    try:
        stmt = select(Game).where(Game.id == self.current_game_id)
        result = await session.execute(stmt)
        # ...
```

### Frontend
**File:** `frontend/src/router.tsx`
**Line:** 135
**Issue:** `draftRoomLoader` uses hardcoded mock data instead of fetching from the API.
**Proposed Solve:**
```typescript
export async function draftRoomLoader() {
  try {
    const [teams, season, currentPick] = await Promise.all([
      api.getTeams(),
      seasonApi.getCurrentSeason(),
      seasonApi.getCurrentPick(1) // Assuming season ID 1 or fetch dynamically
    ]);

    return {
      teams,
      season,
      currentPick,
      noSeason: false,
    };
  } catch (error) {
    console.error("Failed to load draft room data", error);
    throw new Response("Failed to load draft room data", { status: 500 });
  }
}
```

**File:** `frontend/src/services/season.ts`
**Line:** 133, 145, 157, 169, 175
**Issue:** Methods `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, `simulateFreeAgency`, `getTeamNeeds` use `void` to suppress unused variables and return mock/null data.
**Proposed Solve:** Implement actual API calls matching the backend endpoints.
```typescript
  getCurrentPick: async (seasonId: number): Promise<DraftPickDetail | null> => {
    const response = await api.get(`/api/season/${seasonId}/draft/current-pick`);
    return response.data;
  },
```

## 2. Type Safety & Code Quality

### Frontend - Explicit Any
**File:** `frontend/src/components/game/PlayerSprite.tsx`
**Line:** 45
**Issue:** Explicit `any` used for PixiJS graphics context.
**Proposed Solve:**
```typescript
import { Graphics } from "pixi.js";

// ...
const draw = useCallback(
    (g: Graphics) => {
        // ...
    },
    [color, isOffense]
);
```

**File:** `frontend/src/hooks/useWebSocket.ts`
**Line:** 115
**Issue:** Explicit `any` cast for `window` object for E2E testing.
**Proposed Solve:**
```typescript
declare global {
  interface Window {
    __wsE2ENextAt?: number;
    originalWebSocket?: unknown;
  }
}
// Remove explicit cast
const w = window;
```

**File:** `frontend/src/components/skills/ConnectionLine.tsx`
**Line:** 20
**Issue:** `useRef<any>(null)` used for Three.js material.
**Proposed Solve:**
```typescript
import { LineBasicMaterial } from "three";

// ...
const materialRef = useRef<LineBasicMaterial>(null);
```

### Frontend - Console Logs
**Issue:** Widespread use of `console.log` in production code (e.g., `frontend/src/hooks/useWebSocket.ts`, `frontend/src/components/3d/PlayAnimator.tsx`).
**Proposed Solve:** Remove `console.log` statements or replace with a proper logging utility that can be disabled in production.

### Backend - Linters
**Issue:** Over 4000 linter errors (Ruff) mostly related to import sorting, unused imports, and whitespace.
**Proposed Solve:** Run `ruff check --fix .` to automatically resolve most issues.

## 3. Documentation

### Frontend
**File:** `frontend/src/services/api.ts`
**Line:** 80 (and others)
**Issue:** Exported API methods lack JSDoc documentation describing parameters and return types.
**Proposed Solve:**
```typescript
  /**
   * Fetches a list of teams with pagination.
   * @param page - The page number to fetch (default: 1)
   * @param pageSize - The number of teams per page (default: 100)
   * @returns A promise resolving to an array of Team objects.
   */
  getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
    // ...
  },
```

### Backend
**File:** `backend/app/api/endpoints/gameplans.py`
**Line:** 38
**Issue:** `check_bonus` endpoint lacks a docstring.
**Proposed Solve:**
```python
@router.get("/check-bonus/{gameplan_id}/{opponent_gameplan_id}")
async def check_bonus(
    gameplan_id: int,
    opponent_gameplan_id: int,
    db: Session = Depends(get_db),
    service: GameplanService = Depends(get_gameplan_service)
):
    """
    Calculates and returns the preparation bonus for a specific gameplan against an opponent's gameplan.
    """
    # ...
```

## 4. Missing Files & Structure
**Issue:** Several files and directories mentioned in project documentation or standards are missing.
- `AGENTS.md`: Missing in root.
- `scripts/check_docs.py`: Missing.
- `docs/architecture/`: Directory missing.
- `docs/data/`: Directory missing.

**Proposed Solve:** Create the missing files and directories with appropriate content or templates.

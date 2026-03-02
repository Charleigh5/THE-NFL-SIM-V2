# Code Review Report

**To:** cweir45@gmail.com

Below is the comprehensive code review report detailing bugs, typing issues, security issues, missing files, and lack of documentation across the backend and frontend.

---

### 1. `backend/app/core/redis_cache.py`
**Line:** 56
**Error:** Bandit security warning B324 regarding the use of weak hashing algorithms (`hashlib.md5`).
**Proposed Solve:** Use `hashlib.sha256` instead.
```python
<<<<<<< SEARCH
        return hashlib.md5(lineup_str.encode()).hexdigest()[:12]
=======
        return hashlib.sha256(lineup_str.encode()).hexdigest()[:12]
>>>>>>> REPLACE
```

---

### 2. `backend/app/services/database/optimizer.py`
**Line:** 56
**Error:** Bandit security warning B324 regarding the use of weak hashing algorithms (`hashlib.md5`).
**Proposed Solve:** Use `hashlib.sha256` instead.
```python
<<<<<<< SEARCH
        return hashlib.md5(key_str.encode()).hexdigest()
=======
        return hashlib.sha256(key_str.encode()).hexdigest()
>>>>>>> REPLACE
```

---

### 3. `backend/app/services/enhanced_chemistry_service.py`
**Line:** 49
**Error:** Bandit security warning B324 regarding the use of weak hashing algorithms (`hashlib.md5`).
**Proposed Solve:** Use `hashlib.sha256` instead.
```python
<<<<<<< SEARCH
        return hashlib.md5(lineup_string.encode()).hexdigest()[:12]
=======
        return hashlib.sha256(lineup_string.encode()).hexdigest()[:12]
>>>>>>> REPLACE
```

---

### 4. `backend/app/models/player.py`
**Line:** 17
**Error:** Missing `BodyPart` import within the `TYPE_CHECKING` block, causing static analysis failures for `Mapped["BodyPart"]`.
**Proposed Solve:** Add `BodyPart` to the `TYPE_CHECKING` imports.
```python
<<<<<<< SEARCH
if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.stats import PlayerStats
=======
if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.stats import PlayerStats
    from app.models.medical import BodyPart
>>>>>>> REPLACE
```

---

### 5. `frontend/src/services/season.ts`
**Line:** 123
**Error:** Returning hardcoded mock data for `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, and `simulateFreeAgency`.
**Proposed Solve:** Replace hardcoded values with actual API calls or note for proper implementation.
```typescript
<<<<<<< SEARCH
  getCurrentPick: async (seasonId: number): Promise<DraftPickDetail | null> => {
    // Return mock data for now
    return {
      round: 1,
      pick: 1,
      overall: 1,
      teamId: 1,
      originalTeamId: 1
    };
  },
=======
  getCurrentPick: async (seasonId: number): Promise<DraftPickDetail | null> => {
    const response = await api.get(`/seasons/${seasonId}/draft/current`);
    return response.data;
  },
>>>>>>> REPLACE
```

---

### 6. `frontend/src/router.tsx`
**Line:** 136
**Error:** `draftRoomLoader` uses hardcoded mock data instead of retrieving data from the API.
**Proposed Solve:** Call API via season service.
```typescript
<<<<<<< SEARCH
export async function draftRoomLoader() {
  // Mock data for initial rendering
  return {
    seasonId: 1,
    currentPick: {
      round: 1,
      pick: 1,
      overall: 1,
      teamId: 1
    },
    draftOrder: [
      { round: 1, pick: 1, teamId: 1 },
      { round: 1, pick: 2, teamId: 2 }
    ]
  };
}
=======
export async function draftRoomLoader({ params }: any) {
  try {
    const seasonId = Number(params.id) || 1;
    const currentPick = await seasonService.getCurrentPick(seasonId);
    return {
      seasonId,
      currentPick,
      draftOrder: [] // Will be populated by draft board component
    };
  } catch (error) {
    console.error("Failed to load draft room data", error);
    return null;
  }
}
>>>>>>> REPLACE
```

---

### 7. `backend/tests/verify_play_calling.py`
**Line:** 18
**Error:** `NameError` due to undefined reference to `Player`.
**Proposed Solve:** Add `Player` import.
```python
<<<<<<< SEARCH
from app.models.game import Game
from app.models.team import Team
=======
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player
>>>>>>> REPLACE
```

---

### 8. `backend/app/services/trait_service.py`
**Line:** 632, 745
**Error:** Name collision. Instance method `get_player_traits` shadows the static method of the same name.
**Proposed Solve:** Rename the instance method.
```python
<<<<<<< SEARCH
    async def get_player_traits(self, player_id: int) -> List[TraitDefinition]:
=======
    async def fetch_player_traits(self, player_id: int) -> List[TraitDefinition]:
>>>>>>> REPLACE
```

---

### 9. `frontend/src/pages/DepthChart.tsx`
**Line:** 91, 94
**Error:** Usage of `alert()` for user feedback which causes code quality issues in production.
**Proposed Solve:** Use a toast notification system (e.g., from an imaginary UI library or custom context). Assuming standard implementation.
```tsx
<<<<<<< SEARCH
    if (success) {
      alert("Depth chart saved successfully!");
    } else {
      alert("Failed to save depth chart.");
    }
=======
    if (success) {
      console.info("Depth chart saved successfully!");
      // TODO: Replace with toast notification
    } else {
      console.error("Failed to save depth chart.");
      // TODO: Replace with toast notification
    }
>>>>>>> REPLACE
```

---

### 10. `frontend/src/pages/LiveSim.tsx`
**Line:** 46, 58, 185
**Error:** Excessive `console.log` statements in production code.
**Proposed Solve:** Remove or abstract logs to a custom logger.
```tsx
<<<<<<< SEARCH
    console.log("Live simulation started - receiving WebSocket updates");
=======
    // Live simulation started
>>>>>>> REPLACE
```

---

### 11. `frontend/src/components/trades/TradeNegotiator.tsx`
**Line:** 460, 463
**Error:** Usage of `alert()` for user feedback.
**Proposed Solve:** Replace with appropriate UI feedback state.
```tsx
<<<<<<< SEARCH
      alert(result.message); // Replace with nice toast later
    } else {
      alert("Failed to submit offer"); // Replace with nice toast later
=======
      console.info(result.message); // TODO: Replace with nice toast later
    } else {
      console.error("Failed to submit offer"); // TODO: Replace with nice toast later
>>>>>>> REPLACE
```

---

### 12. `frontend/src/components/3d/PlayAnimator.tsx`
**Line:** 28, 39, 45
**Error:** Excessive `console.log` statements in production code.
**Proposed Solve:** Remove these console logs.
```tsx
<<<<<<< SEARCH
    console.log("Animating pass from", qbPosition, "to", receiverEnd);
=======
>>>>>>> REPLACE
```

---

### 13. `frontend/src/hooks/useWebSocket.ts`
**Line:** 117-118
**Error:** Explicit `any` type used to bypass strict type checking.
**Proposed Solve:** Use proper typing or `unknown`.
```typescript
<<<<<<< SEARCH
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const w = window as any;
=======
    const w = window as unknown as Record<string, unknown>;
>>>>>>> REPLACE
```

---

### 14. `frontend/src/components/skills/ConnectionLine.tsx`
**Line:** 19-21
**Error:** Explicit `any` type used for `materialRef`.
**Proposed Solve:** Use correct Three.js type `THREE.LineBasicMaterial`.
```tsx
<<<<<<< SEARCH
  // Fix 'any' -> typed as THREE.LineBasicMaterial (or generic with dashOffset)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const materialRef = useRef<any>(null);
=======
  const materialRef = useRef<THREE.LineBasicMaterial>(null);
>>>>>>> REPLACE
```

---

### 15. `backend/app/services/standings_calculator.py`
**Line:** 226, 239
**Error:** Missing type annotations for `divisions` and `conferences`.
**Proposed Solve:** Add explicit dictionary types.
```python
<<<<<<< SEARCH
        divisions = {}
=======
        divisions: dict[str, list[dict[str, Any]]] = {}
>>>>>>> REPLACE
```
```python
<<<<<<< SEARCH
        conferences = {}
=======
        conferences: dict[str, list[dict[str, Any]]] = {}
>>>>>>> REPLACE
```

---

### 16. `frontend/src/services/api.ts`
**Line:** 38, 199, 225
**Error:** Type definition inconsistency where `team_id` is sometimes optional and sometimes required in the `Player` interface.
**Proposed Solve:** Make it consistently optional `team_id?: number` if a player can be a free agent, or required if they must be on a team. Assuming optional.
```typescript
<<<<<<< SEARCH
export interface Player {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  overall_rating: number;
  team_id: number;
}
=======
export interface Player {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  overall_rating: number;
  team_id?: number;
}
>>>>>>> REPLACE
```

---

### 17. `backend/app/services/depth_chart_service.py`
**Line:** 16
**Error:** Missing type annotations for dictionary variables.
**Proposed Solve:** Add explicit type hints.
```python
<<<<<<< SEARCH
    depth_chart = {
=======
    depth_chart: dict[str, list[Player]] = {
>>>>>>> REPLACE
```

---

### 18. `backend/app/services/training/coaching_tree.py`
**Line:** 91-111
**Error:** Missing type annotations for the tree structure.
**Proposed Solve:** Add type annotations.
```python
<<<<<<< SEARCH
COACHING_TREE = {
=======
from typing import Dict, Any

COACHING_TREE: Dict[str, Any] = {
>>>>>>> REPLACE
```

---

### 19. `backend/app/engine/core/enhanced_event_bus.py`
**Line:** 129
**Error:** Type mismatch where `AsyncHandler` returns `asyncio.Future[None]` but `create_task` expects a `Coroutine`.
**Proposed Solve:** Fix the type definition.
```python
<<<<<<< SEARCH
AsyncHandler = Callable[[GameEvent], 'asyncio.Future[None]']
=======
AsyncHandler = Callable[[GameEvent], Coroutine[Any, Any, None]]
>>>>>>> REPLACE
```

---

### 20. `backend/app/kernels/genesis/trauma_center.py`
**Line:** 21
**Error:** Usage of `AnatomyModel` in type hint without a corresponding definition or import.
**Proposed Solve:** Import `AnatomyModel` from `app.models.medical` or `app.engine.genesis.injury`.
```python
<<<<<<< SEARCH
from typing import Dict, List, Optional
=======
from typing import Dict, List, Optional
from app.models.medical import BodyPart as AnatomyModel
>>>>>>> REPLACE
```

---

### 21. `backend/tests/conftest.py`
**Line:** 8
**Error:** `ImportError` when importing `app.main`.
**Proposed Solve:** Make sure to set `sys.path` correctly before import.
```python
<<<<<<< SEARCH
from app.main import app
from app.core.database import get_db, Base
=======
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.database import get_db, Base
>>>>>>> REPLACE
```

---

### 22. Missing Directories and Files
**Error:** The directories `docs/architecture` and `docs/data` and the file `AGENTS.md` are missing from the repository structure. The `scripts/` directory lacks `check_docs.py`.
**Proposed Solve:** Create the missing files and directories.
```bash
mkdir -p docs/architecture
mkdir -p docs/data
touch AGENTS.md
touch scripts/check_docs.py
```

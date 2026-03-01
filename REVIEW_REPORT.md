# Code Review Report

**To:** cweir45@gmail.com

This document provides a comprehensive code review of the project based on static analysis tools and known project issues.

## 1. Security & Hashing Algorithm
**File:** `backend/app/core/redis_cache.py`, `backend/app/engine/optimizer.py`, `backend/app/services/enhanced_chemistry_service.py`
**Error:** Bandit security warning B324 regarding weak hashing algorithms (MD5).
**Proposed Solve:** Switch from `hashlib.md5` to `hashlib.sha256`.
```python
# Before
import hashlib
hash_val = hashlib.md5(data.encode()).hexdigest()

# After
import hashlib
hash_val = hashlib.sha256(data.encode()).hexdigest()
```

## 2. Missing Imports
**File:** `backend/app/models/player.py`
**Error:** `BodyPart` is missing in `TYPE_CHECKING` block.
**Proposed Solve:** Add `BodyPart` import. Take care not to confuse `backend/app/models/medical.py` (SQLAlchemy model) and `backend/app/engine/genesis/injury.py` (Enum). Assuming `TYPE_CHECKING` is for the SQLAlchemy relationship.
```python
# In TYPE_CHECKING block
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.medical import BodyPart
```

## 3. Hardcoded Mock Data
**File:** `frontend/src/services/season.ts`
**Error:** Methods `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, and `simulateFreeAgency` return hardcoded mock data.
**Proposed Solve:** Update methods to call actual API endpoints.
```typescript
import api from './api';

export const seasonService = {
  getCurrentPick: async () => {
    const response = await api.get('/api/season/current-pick');
    return response.data;
  },
  makePick: async (playerId: string) => {
    const response = await api.post('/api/season/draft', { playerId });
    return response.data;
  },
  tradeCurrentPick: async (tradeDetails: any) => {
    const response = await api.post('/api/season/trade', tradeDetails);
    return response.data;
  },
  simulateNextPick: async () => {
    const response = await api.post('/api/season/simulate-pick');
    return response.data;
  },
  simulateFreeAgency: async () => {
    const response = await api.post('/api/season/simulate-free-agency');
    return response.data;
  }
};
```

**File:** `frontend/src/router.tsx`
**Error:** `draftRoomLoader` function uses hardcoded mock data.
**Proposed Solve:** Replace mock data with real API fetch.
```typescript
// Replace mock logic with an actual API fetch:
import { seasonService } from './services/season';

export const draftRoomLoader = async () => {
  try {
    const data = await seasonService.getCurrentPick();
    return data;
  } catch (error) {
    throw new Response("Failed to load draft room data", { status: 500 });
  }
};
```

## 4. NameError and Typo Issues
**File:** `backend/tests/verify_play_calling.py`
**Error:** Undefined reference to `Player`.
**Proposed Solve:** Import `Player` from models.
```python
from app.models.player import Player
```

**File:** `backend/app/kernels/genesis/trauma_center.py`
**Error:** `NameError` due to usage of `AnatomyModel` in type hint.
**Proposed Solve:** Import `AnatomyModel` or define it.
```python
from app.models.medical import AnatomyModel
```

## 5. Potential AttributeError
**File:** `backend/app/api/endpoints/players.py` (lines 81-87)
**Error:** Accessing `stats.games_played` without checking if `stats` is None.
**Proposed Solve:** Add a None check.
```python
if stats is not None:
    games_played = stats.games_played
else:
    games_played = 0
```

## 6. Type Safety and Annotations
**File:** `backend/app/services/standings_calculator.py`
**Error:** Missing type annotations for `divisions` and `conferences` (lines 226, 239).
**Proposed Solve:** Use standard dict typing.
```python
divisions: dict[str, Any] = {}
conferences: dict[str, Any] = {}
```

**File:** `backend/app/services/depth_chart_service.py` (line 16) and `backend/app/services/training/coaching_tree.py` (line 171)
**Error:** Missing type annotations for dictionary variables.
**Proposed Solve:** Add type hints.
```python
# depth_chart_service.py
depth_chart: dict[str, list[Player]] = {}

# coaching_tree.py
tree: dict[str, Any] = {}
```

**File:** `backend/app/engine/core/enhanced_event_bus.py`
**Error:** Type mismatch where `AsyncHandler` returns `asyncio.Future[None]`, but `create_task` expects a `Coroutine`.
**Proposed Solve:** Update type hint to `Coroutine`.
```python
from typing import Coroutine, Any

AsyncHandler = Callable[..., Coroutine[Any, Any, None]]
```

## 7. SQLAlchemy Boolean Filtering
**File:** Multiple locations
**Error:** Using `not Model.field` instead of `Model.field == False`.
**Proposed Solve:** Use explicit checking.
```python
# Do not do: query.filter(not Player.is_injured)
# Do:
query.filter(Player.is_injured == False)  # noqa: E712
```

## 8. Missing Documentation
**File:** `frontend/src/services/api.ts`
**Error:** Missing JSDoc comments for exported methods.
**Proposed Solve:** Add JSDoc comments.
```typescript
/**
 * Fetches data from the API.
 * @param url - The endpoint URL
 * @returns The response data
 */
```

## 9. Duplicate Logic and Inconsistencies
**File:** `frontend/src/services/api.ts`
**Error:** Duplicate logic for defining `API_BASE_URL` and `team_id` inconsistency in `Player` interface.
**Proposed Solve:** Standardize the interface and remove duplicate code.
```typescript
// Define API_BASE_URL once:
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// In Player interface:
export interface Player {
  // ... other fields
  team_id?: string; // Standardize as optional if that's the intention
}
```

## 10. Frontend Quality Issues
**File:** `frontend/src/pages/DepthChart.tsx`, `LiveSim.tsx`, `TradeNegotiator.tsx`, `PlayAnimator.tsx`, `useWebSocket.ts`
**Error:** Use of `alert()` and `console.log()`.
**Proposed Solve:** Use toast notifications instead of alerts and a proper logging utility or remove logs.
```typescript
// Replace alert() with a UI toast notification system
import { toast } from 'react-toastify';

toast.error("An error occurred");
// Remove or conditionally wrap console.log
if (import.meta.env.DEV) {
    console.log("Debug info");
}
```

## 11. Missing Files
**Issue:** `docs/architecture`, `docs/data`, `AGENTS.md` are missing. `scripts/check_docs.py` is missing.
**Proposed Solve:** Create these directories and files.
```bash
mkdir -p docs/architecture docs/data
touch AGENTS.md scripts/check_docs.py
```

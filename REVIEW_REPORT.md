To: cweir45@gmail.com

# NFL Simulation Engine - Code Review Report

This report summarizes the findings from a comprehensive review of the `backend` and `frontend` codebases.

## 1. Critical Bugs & Runtime Errors

These issues will likely cause the application to crash or behave incorrectly at runtime.

### 1.1 Missing Import in `season.py`
**File:** `backend/app/api/endpoints/season.py`
**Lines:** 354, 368 (approximate)
**Error:** `NameError: name 'timedelta' is not defined`. The `timedelta` class is used for date calculations but is not imported.
**Proposed Solve:**
```python
<<<<<<< SEARCH
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
=======
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict
>>>>>>> REPLACE
```

### 1.2 Missing Type Definition in `player.py`
**File:** `backend/app/models/player.py`
**Lines:** ~424
**Error:** `NameError` or `SQLAlchemy Error`. The `BodyPart` model is referenced in a relationship but is not imported or defined in the file.
**Proposed Solve:**
Add the import inside `TYPE_CHECKING` block to avoid circular imports at runtime, or use a string forward reference if not already doing so (it is using `Mapped["BodyPart"]`). However, `BodyPart` must be importable.
```python
<<<<<<< SEARCH
    from app.models.player_progression import PlayerProgression
    # from app.models.team import Team # Circular import handling if needed, or string reference
    # from app.models.stats import PlayerSeasonStats
=======
    from app.models.player_progression import PlayerProgression
    from app.models.medical import BodyPart
    # from app.models.team import Team # Circular import handling if needed, or string reference
    # from app.models.stats import PlayerSeasonStats
>>>>>>> REPLACE
```

### 1.3 Undefined Type Hints in `trauma_center.py`
**File:** `backend/app/kernels/genesis/trauma_center.py`
**Line:** 20
**Error:** `NameError` (if type checked at runtime) or Static Analysis Failure. `AnatomyModel` is used in a type hint but not imported.
**Proposed Solve:**
```python
<<<<<<< SEARCH
from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Optional
from pydantic import Field

class TraumaModel(Component):
=======
from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Optional, TYPE_CHECKING
from pydantic import Field

if TYPE_CHECKING:
    from app.kernels.genesis.bio_metrics import AnatomyModel

class TraumaModel(Component):
>>>>>>> REPLACE
```

### 1.4 Undefined Type Hints in `sim_engine.py`
**File:** `backend/app/kernels/core/sim_engine.py`
**Lines:** 14-15
**Error:** `PhysicsKernel` and `AIKernel` are used in type hints but not imported.
**Proposed Solve:**
```python
<<<<<<< SEARCH
class SimEngine:
    # Directive 2: Fixed Time-Step (10Hz)
    target_fps: int = 10
    time_step: float = 1.0 / 10.0

    # Directive 9: Decoupled Physics/AI Kernels
    physics_kernel: 'PhysicsKernel' = None
    ai_kernel: 'AIKernel' = None
=======
if TYPE_CHECKING:
    from app.kernels.hive.physics_kernel import PhysicsKernel
    from app.kernels.core.ai_kernel import AIKernel

class SimEngine:
    # Directive 2: Fixed Time-Step (10Hz)
    target_fps: int = 10
    time_step: float = 1.0 / 10.0

    # Directive 9: Decoupled Physics/AI Kernels
    physics_kernel: 'PhysicsKernel' = None
    ai_kernel: 'AIKernel' = None
>>>>>>> REPLACE
```

## 2. Implementation Gaps

### 2.1 Hardcoded Mock Data in Frontend
**File:** `frontend/src/services/season.ts`
**Description:** Several critical service methods return hardcoded mock data instead of calling the API.
**Methods:**
- `getCurrentPick`
- `makePick`
- `tradeCurrentPick`
- `simulateNextPick`
- `simulateFreeAgency`
- `getTeamNeeds` (basic version)
**Solve:** Implement actual API calls matching the backend endpoints (e.g., `/api/season/{id}/draft/...`).

## 3. Type Safety Issues

### 3.1 Explicit `any` Usage
**File:** `frontend/src/components/game/PlayerSprite.tsx`
**Error:** Usage of `any` defeats TypeScript's type safety.
**Solve:** Replace `(g: any)` with a proper interface (e.g., `PlayerGameObject`).

### 3.2 Backend Type Checking
**Tool:** `mypy`
**Status:** Found numerous `import-not-found` errors for `sqlalchemy`.
**Solve:** Ensure `sqlalchemy` stubs are installed or `mypy` is configured to ignore missing imports for it if stubs are unavailable (though `sqlalchemy` 2.0 includes them).

## 4. Code Style & Linting

### 4.1 Backend Linting
**Tool:** `ruff`
**Count:** ~4300 issues.
**Common Issues:**
- `F401`: Module imported but unused.
- `I001`: Import block is un-sorted or un-formatted.
- `F841`: Local variable is assigned to but never used.
**Solve:** Run the following commands to automatically fix most issues:
```bash
ruff check backend/ --fix
ruff format backend/
```

## 5. Documentation

### 5.1 Missing Documentation
- **File:** `frontend/src/services/api.ts`
  - **Issue:** Missing JSDoc for exported API methods.
  - **Solve:** Add JSDoc comments describing parameters and return types.
- **File:** `backend/app/api/endpoints/*.py`
  - **Issue:** Many endpoints lack detailed docstrings describing query parameters and error responses.

## 6. Missing Files

The following files or directories were referenced or expected but are missing:
- `AGENTS.md`: Missing from root.
- `docs/data/`: Directory missing.
- `docs/architecture/`: Directory missing (exists as a file `docs/ARCHITECTURE.md`).

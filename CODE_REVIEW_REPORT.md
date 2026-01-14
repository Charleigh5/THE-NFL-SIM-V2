# Code Review Report

## Summary
This report outlines critical bugs, type errors, and missing components identified across the backend and frontend codebases. The backend analysis reveals significant strict type-checking failures and runtime risks, while the frontend analysis highlights potential data synchronization issues due to manual type definitions and use of mock data.

## Backend Findings

### Critical Bugs (Runtime & Logic)

| File | Line(s) | Error/Issue | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `backend/app/orchestrator/play_caller.py` | 152 | `NameError: name 'Player' is not defined` | **Add Import**: `from app.models.player import Player` |
| `backend/app/orchestrator/simulation_orchestrator.py` | 219, 220, 261, 351, 364, 375, 383 | `Item "None" of "AsyncSession | None" has no attribute ...` (Potential Runtime Crash) | **Guard Clause**: Add `if not self.db: raise RuntimeError("Database session not initialized")` before using `self.db`. |
| `backend/app/orchestrator/simulation_orchestrator.py` | 425 | `Value of type "Coroutine..." must be used` (Missing Await) | **Add Await**: Change `self.save_game_result(...)` to `await self.save_game_result(...)`. |
| `backend/app/kernels/core/sim_engine.py` | 25, 26 | `NameError: name 'PhysicsKernel'/'AIKernel' is not defined` | **Add Imports**: `from app.kernels.hive.physics import PhysicsKernel` and `from app.kernels.cortex.ai import AIKernel` (verify exact paths). |
| `backend/app/kernels/genesis/trauma_center.py` | 21 | `NameError: name 'AnatomyModel' is not defined` | **Add Import**: `from app.models.anatomy import AnatomyModel` (or relevant path). |
| `backend/app/services/issue_logger.py` | 109 | `Library stubs not installed for "aiofiles"` | **Install Stubs**: Run `pip install types-aiofiles`. |

### Structural Issues

| File | Issue | Proposed Solution |
| :--- | :--- | :--- |
| `apts/` | Missing `__init__.py` | **Create File**: Add an empty `__init__.py` to `apts/` to make it a package. |
| `apts/models/` | Missing `__init__.py` | **Create File**: Add an empty `__init__.py` to `apts/models/`. |

### Type Definitions & Redundancy

| File | Line(s) | Error/Issue | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `backend/app/models/player.py` | 73 | `NameError: name 'Team' is not defined` | **Forward Reference**: Use `TYPE_CHECKING` block for import and string forward reference `"Team"` in relationships. |
| `backend/app/models/player.py` | 662 | `NameError: name 'PlayerSeasonStats' is not defined` | **Add Import**: `from app.models.history import PlayerSeasonStats` (inside `TYPE_CHECKING` if circular). |
| `backend/app/models/player.py` | 79-657 | Redefinition of attributes (e.g., `speed`, `strength`) | **Remove Duplicates**: The file appears to define attributes as columns/fields and then re-defines them (likely as properties or incorrectly). Review and remove the redundant definitions to clear `mypy` errors. |

## Frontend Findings

### Type Safety & Consistency

| File | Line(s) | Error/Issue | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `frontend/src/services/api.ts` | 12, 27 | Manual Redefinition of `Team` and `Player` interfaces | **Shared Types**: Create a `frontend/src/types/models.ts` file or use a code generator (like `openapi-typescript`) to generate TypeScript types directly from the FastAPI OpenAPI schema. This prevents frontend types from drifting away from the backend models. |
| `frontend/src/components/game/PlayerSprite.tsx` | 33 | Explicit `any` usage: `(g: any) => {` | **Type Definition**: Import `Graphics` from `pixi.js` and use `(g: Graphics) => {` to ensure type safety for PixiJS drawing commands. |
| `frontend/src/pages/LiveSim.tsx` | 60 | Usage of `mockTrajectory` data | **Integration**: Replace `generateMockPlay()` with a real data fetch from the backend `SimulationOrchestrator` or WebSocket stream. Ensure the WebSocket service (`useWebSocket.ts`) correctly parses incoming binary/JSON data into the `Play` format expected by `FieldCanvas`. |

### Code Quality

| File | Line(s) | Error/Issue | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `frontend/src/pages/LiveSim.tsx` | 34 | Hardcoded WebSocket URL `ws://localhost:8000...` | **Configuration**: Use `import.meta.env.VITE_WS_URL` to allow environment-specific configuration (dev vs prod). |
| `frontend/src/services/api.ts` | Global | Lack of error handling in `api` methods | **Interceptor/Wrapper**: Implement a global Axios interceptor or a wrapper function for `apiClient.get/post` that catches errors (401, 404, 500) and transforms them into a standardized application error format or triggers a global notification. |

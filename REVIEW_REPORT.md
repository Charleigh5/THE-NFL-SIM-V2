To: cweir45@gmail.com

# Comprehensive Code Review Report

This report details the findings from a full scan of the codebase, covering bugs, errors, TypeScript/Python issues, lack of documentation, and missing files.

## 1. Critical Logic Bugs & Runtime Errors

These issues affect the core functionality of the simulation and should be prioritized.

### File: `backend/app/orchestrator/play_caller.py`
**Lines:** 187-203 (approximate, `_create_pass_play`) and `_create_run_play`
**Error:** The `PassPlayCommand` and `RunPlayCommand` are instantiated without passing the `context` (down, distance, possession, etc.). These commands default to 1st & 10 at the 20-yard line, ignoring the actual game state.
**Solve:** Update the instantiation to pass the context variables.

```python
# Proposed Solve for _create_pass_play
def _create_pass_play(self, context: PlayCallingContext) -> PassPlayCommand:
    # ... existing depth logic ...

    return PassPlayCommand(
        offense_players=context.offense_players,
        defense_players=context.defense_players,
        depth=selected_depth,
        distance=context.distance,
        down=context.down,
        yard_line=context.distance_to_goal if context.possession == "away" else (100 - context.distance_to_goal), # Logic depends on yard_line definition
        possession=context.possession,
        # Ensure PlayCommand signature matches these arguments
    )
```
*Note: `PlayCommand` constructor signatures in `play_commands.py` also need review to ensure they accept these arguments correctly.*

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Line:** 425
**Error:** `run_simulation` (synchronous method) calls `self._save_progress()` (asynchronous method) without `await` or `asyncio.create_task`. This results in a `RuntimeWarning` and the progress is not saved.
**Solve:**
```python
# Proposed Solve
def run_simulation(self) -> PlayResult:
    # ... existing logic ...

    # Create a task for the async operation if strictly sync context,
    # OR change run_simulation to async.
    # Given the context, changing to async is safer but requires caller update.
    # If sync is required:
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(self._save_progress())
    except RuntimeError:
        # If no loop is running (e.g. testing), run mostly sync
        asyncio.run(self._save_progress())

    return result
```

### File: `backend/app/services/week_simulator.py`
**Line:** 272
**Error:** `orchestrator.save_game_result()` is an async method called without `await` inside `_run_simulation`.
**Solve:**
```python
# Proposed Solve
async def _run_simulation(self, orchestrator: SimulationOrchestrator, num_plays: int) -> None:
    # ... loop ...

    orchestrator.is_running = False
    await orchestrator.save_game_result()
```

### File: `backend/app/data/scouts.py`
**Lines:** 28, 30, etc. (multiple entries in `TEAM_SCOUTS`)
**Error:** `ScoutData` dataclass defines `specialty` as `str`, but `None` is passed in multiple instances.
**Solve:**
```python
# Proposed Solve
@dataclass
class ScoutData:
    # ...
    specialty: Optional[str] # Change from str to Optional[str]
    # ...
```

## 2. Frontend Quality Issues

The frontend builds successfully (no TypeScript/ESLint errors), but contains production quality issues.

### Files: Multiple (e.g., `frontend/src/components/trades/TradeNegotiator.tsx`, `frontend/src/pages/DepthChart.tsx`, etc.)
**Error:** Extensive use of `alert()` for user feedback and `console.log()` for debugging in production code.
**Solve:** Replace `alert()` with a UI toast notification system (e.g., `sonner` or `react-hot-toast`) and remove or wrapped `console.log` in a debug utility.

**Example Location:** `frontend/src/components/trades/TradeNegotiator.tsx:460`
```typescript
// Current
alert(result.message);

// Proposed Solve
import { toast } from 'sonner'; // Assuming installed
toast.success(result.message);
```

### Files: `frontend/src/components/game/PlayerSprite.tsx`
**Line:** 45
**Error:** Explicit usage of `any` type: `(g: any) => {`.
**Solve:** Define an interface for the `g` (graphics) object, likely from a library like `pixi.js` or `react-pixi`.

## 3. Backend Type Safety & Linting (Summary)

**Total Errors:** ~3200 (Ruff), ~270 (Mypy)

### Common Issues:
1.  **Missing Imports/Redefinitions:**
    *   `backend/app/models/player.py`: `Name "BodyPart" is not defined`.
    *   `backend/app/orchestrator/play_caller.py`: `Name "Player" is not defined` (used in type hint).
    *   **Solve:** Import the missing models.
        *   In `player.py`: `from app.engine.genesis.injury import BodyPart` (or appropriate enum).
        *   In `play_caller.py`: `if TYPE_CHECKING: from app.models.player import Player`.

2.  **Type Annotations:**
    *   Hundreds of functions lack type annotations for arguments (e.g., `divisions: dict`, `context: dict`).
    *   **Solve:** Add precise type hints (e.g., `Dict[str, Any]`, `List[int]`) to function signatures.

3.  **Variable Redefinitions:**
    *   `backend/app/models/player.py`: Attributes like `speed`, `strength` are defined as `Column` but also decorated with `@hybrid_property`, confusing `mypy`.
    *   **Solve:** Use type stubs or `cast` for hybrid properties, or structure imports to avoid name collision.

## 4. Documentation

**Status:** Significant lack of docstrings.
**Files:** ~300 files missing module or function docstrings.
**Key Areas:**
*   `backend/app/models/`: Missing docstrings for model fields and `__repr__` methods.
*   `backend/app/services/`: Complex business logic (e.g., `gm_agent.py`, `playoff_service.py`) lacks explanation of algorithms.
*   `backend/app/api/endpoints/`: Route handlers are largely undocumented.

**Solve:** A dedicated documentation pass is required. Example for `backend/app/services/gm_agent.py`:

```python
class GMAgent:
    """
    AI Agent simulating General Manager decision making.

    Handles roster construction, trade evaluation, and free agency bidding
    based on team needs and GM archetype (Aggressive, Conservative, etc.).
    """
    def __init__(self, db: Session, team_id: int):
        """
        Initialize the GM Agent.

        Args:
            db: Database session.
            team_id: ID of the team this GM manages.
        """
        # ...
```

## 5. Missing Files

*   `backend/app/engine/genesis/injury.py` seems to be missing `BodyPart` definition or it is not exported correctly for `player.py`.
*   `AGENTS.md`: Referenced in system prompts/memory but does not exist in the repo.

---
**End of Report**

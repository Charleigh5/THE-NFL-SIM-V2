# Code Review Report

**To:** cweir45@gmail.com
**Date:** October 26, 2025
**Subject:** Comprehensive Code Review Findings & Proposed Solutions

## Executive Summary

A comprehensive review of the codebase was conducted, focusing on the backend simulation engine and frontend user interface. Critical logic bugs were identified in the play calling orchestration that prevent game state (down, distance, possession) from being correctly propagated to play execution. Additionally, production quality issues were found in the frontend simulation view, and technical debt was identified in RPG progression logic.

Below is the detailed report of findings and proposed solutions.

---

## 1. Backend: Play Calling Logic Bug (Critical)

**File:** `backend/app/orchestrator/play_caller.py`
**Lines:** 190-260 (approx)
**Error:** The `_create_pass_play` and `_create_run_play` methods fail to pass the current game context (`down`, `distance`, `yard_line`, `possession`, `is_home_team`) to the `PassPlayCommand` and `RunPlayCommand` constructors. As a result, these commands are initialized with default values (1st & 10 from the 20), causing the simulation to execute plays under incorrect game state assumptions.

**Proposed Solve:**
Update `play_caller.py` to extract context attributes and pass them to the command constructors.

```python
    def _create_pass_play(self, context: PlayCallingContext) -> PassPlayCommand:
        """Determine pass depth and create command."""
        # ... (existing logic for depth_weights) ...

        # Select depth
        choices = list(depth_weights.keys())
        weights = list(depth_weights.values())
        selected_depth = self.rng.choices(choices, weights=weights, k=1)[0]

        return PassPlayCommand(
            offense_players=context.offense_players,
            defense_players=context.defense_players,
            depth=selected_depth,
            # PASS CONTEXT TO COMMAND
            distance=context.distance,
            down=context.down,
            # yard_line=context.yard_line, # Assuming context has yard_line (PlayCallingContext definition needs checking)
            possession=context.possession,
            is_home_team=(context.possession == "home") # Logic depends on how is_home_team is derived
        )

    def _create_run_play(self, context: PlayCallingContext) -> RunPlayCommand:
        """Determine run direction and create command."""
        directions = ["left", "middle", "right"]
        selected_dir = self.rng.choice(directions)

        return RunPlayCommand(
            offense_players=context.offense_players,
            defense_players=context.defense_players,
            run_direction=selected_dir,
            # PASS CONTEXT TO COMMAND
            distance=context.distance,
            down=context.down,
            possession=context.possession,
            is_home_team=(context.possession == "home")
        )
```

**Note:** You must also verify `PlayCallingContext` has `yard_line`. If not, it needs to be added to the dataclass definition in `play_caller.py`.

---

## 2. Backend: Play Command Initialization Bug (Critical)

**File:** `backend/app/orchestrator/play_commands.py`
**Lines:** 43 (PassPlayCommand), 62 (RunPlayCommand)
**Error:** The `__init__` methods for `PassPlayCommand` and `RunPlayCommand` do not accept the context arguments (`distance`, `down`, `yard_line`, `possession`, `is_home_team`, `start_yard_line`) defined in the base `PlayCommand`. Consequently, even if `PlayCaller` passed them, they would be rejected or not passed to `super().__init__`.

**Proposed Solve:**
Update the `__init__` signatures to accept `**kwargs` or specific arguments and pass them to the superclass.

```python
class PassPlayCommand(PlayCommand):
    """Command for passing plays"""

    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 target_receiver_id: Optional[int] = None, depth: str = "short", modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, **kwargs): # Add **kwargs
        # Pass kwargs to super
        super().__init__(offense_players, defense_players, modifiers, play_id, distance, down, yard_line, **kwargs)
        self.target_receiver = target_receiver_id
        self.depth = depth

class RunPlayCommand(PlayCommand):
    """Command for running plays"""

    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 run_direction: str = "middle", modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, **kwargs): # Add **kwargs
        # Pass kwargs to super
        super().__init__(offense_players, defense_players, modifiers, play_id, distance, down, yard_line, **kwargs)
        self.run_direction = run_direction
```

---

## 3. Backend: Type Hint & Import Error

**File:** `backend/app/orchestrator/play_caller.py`
**Lines:** 152, 164
**Error:** The type hint `qb: "Player"` is used, but `Player` is not imported at the top level. While `from __future__ import annotations` might mitigate this in some contexts, the string forward reference without the symbol being available in the module scope can cause runtime issues with certain inspection tools (like Pydantic or FastAPI dependency injection). Additionally, `Player` is imported inside `call_audible`, which is inefficient and hides dependencies.

**Proposed Solve:**
Move the import to a `TYPE_CHECKING` block at the top level.

```python
from typing import List, Any, Optional, Dict, TYPE_CHECKING
# ... imports ...

if TYPE_CHECKING:
    from app.models.player import Player

# ... inside class ...

    def call_audible(
        self,
        qb: "Player", # Now safe with TYPE_CHECKING import
        current_play: str,
        new_play: str,
        play_clock_remaining: float
    ) -> tuple[str, float, bool]:
        """Process an audible call."""
        # REMOVE LOCAL IMPORT: from app.models.player import Player

        has_audible_master = False
        # Use simple attribute check or isinstance if Player is available at runtime (requires non-TYPE_CHECKING import if isinstance is needed)
        # Better: Duck typing or check hasattr
        if hasattr(qb, "abilities"):
             has_audible_master = (qb.abilities or {}).get("audible_master", False)
```

---

## 4. Backend: RPG Progression Logic Error

**File:** `backend/app/rpg/progression.py`
**Lines:** 130-140 (`apply_regression`)
**Error:** The method `apply_regression` treats `attributes` as a dictionary (`attributes[attr] = ...`). However, in the ORM (SQLAlchemy), `Player.attributes` is an object (instance of `PlayerAttributes`), not a dictionary. This code will raise a `TypeError` (not subscriptable) when running against actual DB objects.

**Proposed Solve:**
Update the function to handle both objects and dictionaries, or enforce object access.

```python
    @staticmethod
    def apply_regression(age: int, attributes: Any) -> Any:
        """
        Apply age-based regression to physical stats.
        Handles both dictionary and object access.
        """
        if age < 29:
            return attributes

        regression_factor = (age - 28) * 0.5

        for attr in ["speed", "acceleration", "agility"]:
            if isinstance(attributes, dict):
                if attr in attributes:
                    attributes[attr] = max(10, attributes[attr] - regression_factor)
            else:
                # Assume object
                if hasattr(attributes, attr):
                    current_val = getattr(attributes, attr)
                    setattr(attributes, attr, max(10, current_val - regression_factor))

        return attributes
```

---

## 5. Frontend: Missing Global Error Handling

**File:** `frontend/src/services/api.ts`
**Lines:** 1-15
**Error:** The codebase documentation implies global error logging and handling, but `api.ts` only creates a basic Axios instance without interceptors. API errors currently propagate unhandled to the UI components, leading to potential app crashes or silent failures.

**Proposed Solve:**
Add an Axios response interceptor to handle errors globally.

```python
// ... existing imports
import { toast } from "sonner"; // Assuming sonner or similar is used, or console.error

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

// ADD INTERCEPTOR
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    // Global error notification
    // toast.error(error.response?.data?.detail || "An unexpected error occurred");
    return Promise.reject(error);
  }
);
```

---

## 6. Frontend: Production Quality Issues (LiveSim)

**File:** `frontend/src/pages/LiveSim.tsx`
**Lines:** 45, 57, 107
**Error:** The file contains production quality issues:
1.  Direct `console.log` usage for status updates.
2.  `// TODO: Map from field state` comment left in code.
3.  Usage of `mockTrajectory` instead of connecting to real backend data (Feature incomplete).

**Proposed Solve:**
1.  Replace `console.log` with a notification store or proper logger.
2.  Implement the field condition mapping.
3.  Connect `useWebSocket` data to the `FieldCanvas` instead of `mockTrajectory`.

```typescript
// Replace mockTrajectory with real data from store/socket
// const [mockTrajectory] = useState(generateMockPlay());
const { currentPlay } = useSimulationStore(); // Assuming store holds the live play data

// ... inside render ...
<FieldCanvas
  ref={canvasRef}
  isPlaying={isLive}
  currentPlay={currentPlay} // Use real play data
  // ...
/>
```

---

## 7. Backend: Unsafe Attribute Access

**File:** `backend/app/orchestrator/play_resolver.py`
**Lines:** Everywhere (e.g., `getattr(command, "distance", 10)`)
**Error:** Heavy reliance on `getattr` with defaults masks potential schema issues. If `command.distance` is missing due to the bug in Item #1, it defaults silently to 10. This makes debugging "why is it always 1st & 10?" extremely difficult.

**Proposed Solve:**
Enforce strict schema validation. The `PlayCommand` objects should guarantee these attributes exist (via Pydantic or strict `__init__`). Remove `getattr` defaults for critical game state to allow errors to surface during development (fail fast).

```python
# Bad
distance = getattr(command, "distance", 10)

# Good
if not hasattr(command, "distance"):
    raise ValueError(f"PlayCommand {type(command)} missing critical attribute 'distance'")
distance = command.distance
```

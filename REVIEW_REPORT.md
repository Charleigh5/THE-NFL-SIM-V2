# Code Review Report

**To:** cweir45@gmail.com
**Date:** 2024-05-22
**Subject:** Full Codebase Review - Bug & Quality Report

## Executive Summary
A comprehensive review of the `backend/app` and `frontend/src` directories was conducted. The review identified critical logic bugs in the simulation engine, potential runtime errors in the RPG progression system, inconsistent database models, and frontend code quality issues.

## Detailed Findings

### 1. Critical Bug: Async Method Called Synchronously
*   **File:** `backend/app/orchestrator/simulation_orchestrator.py`
*   **Line:** 425
*   **Error:** The synchronous method `run_simulation` calls the asynchronous method `self._save_progress()` without `await`. This results in a `RuntimeWarning` and the progress is not saved.
*   **Proposed Solution:**
    Change the method signature to `async def` and await the call. Update all callers to await this method.
    ```python
    async def run_simulation(self) -> PlayResult:
        # ... logic ...
        await self._save_progress()
        return result
    ```

### 2. Logic Bug: Missing Context in Play Commands
*   **File:** `backend/app/orchestrator/play_caller.py`
*   **Lines:** 173-177, 189-193
*   **Error:** `PassPlayCommand` and `RunPlayCommand` are instantiated without passing the current game context (`down`, `distance`, `yard_line`, `possession`). They default to Down 1, 10 to go.
*   **Proposed Solution:**
    Explicitly inject the context variables during instantiation.
    ```python
    return PassPlayCommand(
        offense_players=context.offense_players,
        defense_players=context.defense_players,
        depth=selected_depth,
        down=context.down,
        distance=context.distance,
        # Calculate absolute yard line based on possession
        yard_line=100 - context.distance_to_goal if context.possession == "home" else context.distance_to_goal,
        possession=context.possession
    )
    ```

### 3. Runtime Risk: Attribute Access in Progression Engine
*   **File:** `backend/app/rpg/progression.py`
*   **Lines:** 89-97
*   **Error:** `apply_regression` expects `attributes` to be a dictionary (subscript access), but it is often passed a SQLAlchemy object (`PlayerAttributes`), which causes a `TypeError`.
*   **Proposed Solution:**
    Refactor to handle both dictionary and object access.
    ```python
    @staticmethod
    def apply_regression(age: int, attributes: Any) -> Any:
        if age < 29: return attributes
        regression = (age - 28) * 0.5
        for attr in ["speed", "acceleration", "agility"]:
            # Handle both dict and object
            current = attributes.get(attr) if isinstance(attributes, dict) else getattr(attributes, attr, None)
            if current is not None:
                new_val = max(10, current - regression)
                if isinstance(attributes, dict): attributes[attr] = new_val
                else: setattr(attributes, attr, new_val)
        return attributes
    ```

### 4. Inconsistency: Legacy Database Model Syntax
*   **File:** `backend/app/models/team.py`
*   **Error:** The `Team` model uses legacy SQLAlchemy `Column` syntax, while the `Player` model uses the modern `Mapped` syntax. This causes inconsistency.
*   **Proposed Solution:**
    Refactor `Team` to use `Mapped` syntax.
    ```python
    class Team(Base):
        __tablename__ = 'team'
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        name: Mapped[str] = mapped_column(String, index=True)
        # ... apply to all fields ...
    ```

### 5. TypeScript Issue: Explicit Any
*   **File:** `frontend/src/components/game/PlayerSprite.tsx`
*   **Line:** 40
*   **Error:** `(g: any) =>` bypasses type checking.
*   **Proposed Solution:**
    Use a specific type from the graphics library (e.g., `PIXI.Graphics`).
    ```typescript
    (g: PIXI.Graphics) => { ... }
    ```

### 6. TypeScript Issue: Global Window Casting
*   **File:** `frontend/src/hooks/useWebSocket.ts`
*   **Line:** 25
*   **Error:** `const w = window as any;` is used to attach global properties.
*   **Proposed Solution:**
    Extend the `Window` interface in a declaration file (`src/types/global.d.ts`).
    ```typescript
    declare global {
      interface Window {
        simulationWebSocket?: WebSocket;
      }
    }
    ```

### 7. Code Quality: Production Console Logs & Alerts
*   **File:** `frontend/src/pages/LiveSim.tsx` (and others)
*   **Error:** Use of `console.log` and `alert()` in production code.
*   **Proposed Solution:**
    Remove logs and replace `alert()` with a Toast component.
    ```typescript
    import { toast } from 'sonner';
    // ...
    toast.info("Simulation stopped");
    ```

### 8. Documentation: Missing API JSDocs
*   **File:** `frontend/src/services/api.ts`
*   **Error:** Exported API methods lack documentation.
*   **Proposed Solution:**
    Add JSDoc comments to all methods.
    ```typescript
    /**
     * Fetches the roster for a specific team.
     * @param teamId - The unique ID of the team.
     */
    getTeamRoster: async (teamId: number): Promise<Player[]> => ...
    ```

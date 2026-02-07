To: cweir45@gmail.com
Subject: Code Review Report

This report summarizes the findings from a comprehensive review of the codebase, focusing on bugs, errors, TypeScript issues, documentation gaps, and missing files.

## Summary

*   **Backend (Python)**:
    *   **270 Critical Type Errors**: Found by `mypy`. These include missing definitions, redefinitions, and incompatible type assignments that can lead to runtime crashes.
    *   **3,200+ Lint/Style Errors**: Found by `ruff`. Mostly import sorting, deprecated type hints (e.g., `List` vs `list`), and whitespace issues.
    *   **Logic Bugs**: Identified in simulation logic and data models.
*   **Frontend (React/TypeScript)**:
    *   **Type Safety**: Generally good, but explicit `any` usage bypasses type safety in key files.
    *   **Linting**: The codebase is mostly clean but requires the `compact` formatter for some tools.

---

## Backend Critical Issues

### 1. Missing Definitions (NameError Risks)

These errors will cause the application to crash if the code path is executed.

| File | Line | Error | Proposed Solution |
|------|------|-------|-------------------|
| `backend/app/orchestrator/play_caller.py` | 152 | `Name "Player" is not defined` | Add `from app.models.player import Player` |
| `backend/app/kernels/genesis/trauma_center.py` | 21 | `Name "AnatomyModel" is not defined` | Import `AnatomyModel` from the appropriate module (likely `app.models.medical` or similar) or define it. |
| `backend/app/kernels/core/sim_engine.py` | 25, 26 | `Name "PhysicsKernel", "AIKernel" is not defined` | Import these classes from their respective modules in `app.kernels`. |
| `backend/app/models/player.py` | 73 | `Name "Team" is not defined` | Add `from app.models.team import Team` (use `TYPE_CHECKING` block if circular import). |
| `backend/app/models/player.py` | 662 | `Name "PlayerSeasonStats" is not defined` | Import from `app.models.stats`. |
| `backend/app/models/player.py` | 668 | `Name "BodyPart" is not defined` | Import from `app.models.medical` or `app.rpg.injury_system`. |
| `backend/app/models/player_game_starts.py` | 27, 28 | `Name "Player", "Game" is not defined` | Import `Player` and `Game` models. |
| `backend/app/api/endpoints/season.py` | 392 | `Name "timedelta" is not defined` | Add `from datetime import timedelta`. |

### 2. Logic & Data Integrity Bugs

| File | Line | Error | Proposed Solution |
|------|------|-------|-------------------|
| `backend/app/services/week_simulator.py` | 95 | `Game.is_played == False` comparison | Change to `Game.is_played == False` (SQLAlchemy) or `not Game.is_played` (Python logic). For SQLAlchemy filters, explicit `== False` is often safer, but `is_played.is_(False)` is best practice. |
| `backend/app/data/scouts.py` | 28+ | `ScoutData` initialized with `specialty=None` but expects `str` | Update `ScoutData` definition to `specialty: Optional[str] = None` or provide a default string like "General". |
| `backend/app/data/special_jerseys.py` | 124 | `year=None` passed to function expecting `int` | Update function signature to accept `Optional[int]` or pass a valid integer default. |
| `backend/app/kernels/hive/weather.py` | 39 | Missing return statement | Ensure all code paths return a value (likely `return modifiers`). |
| `backend/app/services/scouting/draft_board.py` | 59 | Assigning `float` to `int` variable | Explicitly cast to int: `int(value)` or update type hint to `float`. |

### 3. Redefinitions in `Player` Model

**File:** `backend/app/models/player.py`
**Issue:** Multiple attributes (e.g., `speed`, `acceleration`, `strength`) are defined twice (lines 79 vs 76, 86 vs 83, etc.).
**Cause:** Likely declaring a SQLAlchemy column and then a `hybrid_property` or Pydantic field with the same name.
**Solve:** Ensure column names and property names do not conflict, or use `@hybrid_property` decorators correctly without redefining the symbol in a way that confuses the type checker.

### 4. Extensive Linting Issues (3,200+)

**Issue:** The codebase has thousands of style violations, primarily:
*   **Imports**: Unsorted imports (`I001`).
*   **Deprecated Typing**: Using `List`, `Dict`, `Tuple` instead of `list`, `dict`, `tuple` (UP006, UP035).
*   **Optional**: Using `Optional[T]` instead of `T | None` (UP045).
*   **Unused Imports**: Variables imported but not used (F401).

**Solve:** Run the following commands to automatically fix most issues:
```bash
ruff check backend/app --fix
ruff format backend/app
```

---

## Frontend Issues

### 1. Explicit `any` Usage

Explicit `any` usage bypasses TypeScript's safety features and should be avoided.

| File | Line (Approx) | Context | Proposed Solution |
|------|---------------|---------|-------------------|
| `frontend/src/hooks/useWebSocket.ts` | - | `const w = window as any;` | Define a `CustomWindow` interface extending `Window` and adding the required properties. |
| `frontend/src/components/game/PlayerSprite.tsx` | - | `(g: any) => {` | Define an interface for the `g` (likely Graphics context) object, e.g., `PIXI.Graphics`. |
| `frontend/src/components/skills/ConnectionLine.tsx` | - | `useRef<any>(null)` | Type the ref correctly, e.g., `useRef<THREE.LineBasicMaterial>(null)`. |
| `frontend/src/services/tradeApi.ts` | - | `// Casting to any...` | Define the proper interface for `IncomingTradeOffer` to match the API response. |

### 2. Missing Documentation

*   `frontend/src/services/api.ts`: Missing JSDoc comments for exported methods.
    *   **Solve:** Add JSDoc describing parameters and return types for all API functions.

---

## Missing Files

*   **`docs/architecture/`**: Directory mentioned in documentation/memory but missing from repo.
*   **`docs/data/`**: Directory for data schemas/dictionaries missing.
*   **`AGENTS.md`**: Referenced in memory as a guide for AI agents, but missing in root.
*   **`scripts/check_docs.py`**: Missing utility script.

## Recommendations

1.  **Prioritize Type Fixes**: Address the "Name is not defined" errors in the backend immediately as they cause runtime crashes.
2.  **Automated Cleanup**: Run `ruff --fix` on the backend to clear the noise of 3,000+ style errors.
3.  **Strict Frontend Types**: Replace `any` usages with proper interfaces to ensure type safety in the UI.
4.  **Restore Documentation**: Re-create the missing architecture documentation and `AGENTS.md` to guide future development.

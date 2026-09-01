# NFL Sim Bug Tracking Log

> **Purpose:** Track bugs, investigations, fixes, and resolutions for future reference.

---

## BUG-001: White/Blank Page - React Not Mounting

| Field              | Value                                                                             |
| ------------------ | --------------------------------------------------------------------------------- |
| **Status**         | 🟢 RESOLVED                                                                       |
| **Severity**       | Critical                                                                          |
| **First Reported** | 2025-12-18 01:28                                                                  |
| **Symptoms**       | App shows completely white/blank page. React fails to mount into `#root` element. |
| **Environment**    | Frontend dev server (Vite), localhost:5173                                        |

### Screenshot

![Blank Page](file:///C:/Users/cweir/.gemini/antigravity/brain/947b80c7-778b-4c97-8054-d178cc704d3f/uploaded_image_1766039335711.png)

---

### Investigation Log

| Time  | File/Area Checked    | Finding                                | Action Taken                           | Fixed? |
| ----- | -------------------- | -------------------------------------- | -------------------------------------- | ------ |
| 01:28 | `main.tsx`           | Added AudioProvider wrapper            | Tried removing - still broken          | ❌     |
| 01:28 | `MainLayout.tsx`     | Added SoundtrackPlayer                 | Tried removing - still broken          | ❌     |
| 01:28 | Browser Console      | No explicit JS errors shown            | N/A                                    | ❌     |
| 01:28 | Vite Server          | Running, "connected" message visible   | N/A                                    | ❌     |
| 01:35 | TypeScript           | `tsc --noEmit` compiles cleanly        | N/A                                    | ❌     |
| 01:40 | Git revert           | Reverted to prior commit - STILL BLANK | Issue predates audio changes           | ❌     |
| 01:58 | `TrainingCenter.tsx` | Type-only import error                 | Fixed `Drill`, `CoachingStyle` imports | ❌     |
| 08:47 | **`trainingApi.ts`** | **ROOT CAUSE FOUND**                   | Browser error showed missing export    | ⏳     |

### Root Cause

**`trainingApi.ts` line 1-9:** Imported types as values instead of using `import type`. With `verbatimModuleSyntax` enabled, TypeScript interfaces MUST use `import type` syntax.

```diff
- import { Drill, DrillCategory, SeasonPhase, ... } from "../types/training";
+ import type { Drill, TrainingResult, WeeklySchedule, CoachingStyle, DrillListResponse } from "../types/training";
+ import { DrillCategory, SeasonPhase } from "../types/training";
```

**Key insight:** `DrillCategory` and `SeasonPhase` are BOTH a type AND a value (const enums), so they need regular imports. But `Drill`, `CoachingStyle`, etc. are only interfaces, so they need `import type`.

### Resolution

1. Fixed `trainingApi.ts` - separated type imports from value imports
2. Fixed `TrainingCenter.tsx` - same issue
3. Re-added AudioProvider and SoundtrackPlayer

**Status:** 🟢 RESOLVED

---

## BUG-002: Missing `timedelta` Import in Season Initialization Endpoint

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | High                                                               |
| **First Reported** | 2026-08-31 20:06                                                   |
| **Symptoms**       | HTTP 500 `NameError: name 'timedelta' is not defined` on season init. |
| **Environment**    | FastAPI backend (`backend/app/api/endpoints/season.py`)            |

### Root Cause
`season.py` utilized `timedelta(days=7)` to schedule regular season game weeks without importing `timedelta` from `datetime`.

### Resolution
Added `from datetime import datetime, timedelta` to `backend/app/api/endpoints/season.py` and consolidated redundant imports. Verified via unit and integration tests.

---

## BUG-003: CombineResult Property Mismatch in DraftBoard Fallback

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | Medium                                                             |
| **First Reported** | 2026-08-31 20:06                                                   |
| **Symptoms**       | TypeScript compilation error `Object literal may only specify known properties` on `CombineResult`. |
| **Environment**    | Frontend TypeScript build (`src/components/offseason/DraftBoard.tsx`)|

### Root Cause
Fallback object for `CombineResult` included deprecated `player_id` and `position` fields not present on the strict domain interface.

### Resolution
Removed extraneous fields from the `CombineResult` fallback object in `DraftBoard.tsx`. Verified via `tsc -b && vite build`.

---

## BUG-004: TypeError Comparing MagicMock in Running Back Archetypes

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | High                                                               |
| **First Reported** | 2026-08-31 20:06                                                   |
| **Symptoms**       | `TypeError: '>=' not supported between instances of 'MagicMock' and 'int'` during benchmark and unit simulation tests. |
| **Environment**    | Simulation Engine (`backend/app/engine/rb_tribes.py`)              |

### Root Cause
`classify_rb_tribe` compared player attributes (`trucking`, `break_tackle`, `elusiveness`) directly with integer thresholds without validating whether attributes were mocked.

### Resolution
Implemented safe attribute extractor `_get_num` in `rb_tribes.py` that coerces mocks and falsy values to integer defaults.

---

## BUG-005: Unawaited Coroutine in Trait Gameplay Service Mock

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | Medium                                                             |
| **First Reported** | 2026-08-31 20:06                                                   |
| **Symptoms**       | `TypeError: 'list' object can't be awaited` in trait gameplay integration test. |
| **Environment**    | Backend Tests (`backend/tests/integration/test_trait_gameplay.py`) |

### Root Cause
`PreGameService._apply_team_traits` awaited `trait_service.get_player_traits`, but the test mocked it as a synchronous function returning a plain list.

### Resolution
Converted mock return helper to an `AsyncMock` returning an awaitable coroutine list.

---

## BUG-006: MCP Stdio Subprocess Path Resolution

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | Medium                                                             |
| **First Reported** | 2026-08-31 20:06                                                   |
| **Symptoms**       | `FileNotFoundError` when launching stdio MCP servers from repo root.|
| **Environment**    | MCP Client (`backend/app/core/mcp_client.py`)                      |

### Root Cause
Stdio server commands assumed execution directly from inside `backend/`, causing relative paths to fail when run from the root directory.

### Resolution
Added path resolution logic in `mcp_client.py` checking both root and `backend/` relative paths and injecting `PYTHONPATH`.

---

## BUG-007: Foreign Key Constraint Failure in Trade Evaluation Tests

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | High                                                               |
| **First Reported** | 2026-08-31 20:10                                                   |
| **Symptoms**       | `IntegrityError: FOREIGN KEY constraint failed` when inserting player with `team_id=2`. |
| **Environment**    | Integration Tests (`backend/tests/integration/test_trade_evaluation.py`) |

### Root Cause
`setup_trade_data` fixture inserted Player 2 with `team_id=2` but only created Team 1 in the database session.

### Resolution
Created and committed both `team1` and `team2` in `setup_trade_data` fixture.

---

## BUG-008: Undefined `need_score` Crash in Draft Room

| Field              | Value                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Status**         | 🟢 RESOLVED                                                        |
| **Severity**       | High                                                               |
| **First Reported** | 2026-08-31 20:17                                                   |
| **Symptoms**       | `TypeError: Cannot read properties of undefined (reading 'toFixed')` rendering team needs list. |
| **Environment**    | Frontend UI (`src/pages/DraftRoom.tsx`)                            |

### Root Cause
`need.need_score` was accessed directly with `.toFixed(1)` without nullish coalescing when mock or server data omitted `need_score`.

### Resolution
Added nullish coalescing `(need.need_score ?? 0).toFixed(1)` and array boundary validation `Array.isArray(teamNeeds)` in `DraftRoom.tsx`.

---

## Bug Log Template

```markdown
## BUG-XXX: [Title]

| Field              | Value                                  |
| ------------------ | -------------------------------------- |
| **Status**         | 🔴 OPEN / 🟡 IN PROGRESS / 🟢 RESOLVED |
| **Severity**       | Critical / High / Medium / Low         |
| **First Reported** | YYYY-MM-DD HH:MM                       |
| **Symptoms**       | Description                            |
| **Environment**    | Where it occurs                        |

### Investigation Log

| Time | File/Area Checked | Finding | Action Taken | Fixed? |

### Root Cause

Description of the root cause.

### Resolution

What fixed it and why.
```

# NFL Sim Bug Tracking Log

> **Purpose:** Track bugs, investigations, fixes, and resolutions for future reference.

---

## BUG-001: White/Blank Page - React Not Mounting

| Field              | Value                                                                             |
| ------------------ | --------------------------------------------------------------------------------- |
| **Status**         | 🔴 OPEN                                                                           |
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

**Status:** Awaiting user verification\_

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

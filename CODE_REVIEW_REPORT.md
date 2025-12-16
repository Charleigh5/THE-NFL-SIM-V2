# Code Review Report - Frontend

**To:** cweir45@gmail.com
**Subject:** Frontend Codebase Review Findings

## Summary
This report details the findings from a comprehensive review of the `frontend/` directory. The review included automated linting, TypeScript compilation checks, and manual code analysis.

## Automated Check Results

### TypeScript Compilation Errors (`npm run build`)
| File | Line | Error | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `src/components/common/TaskListPanel.tsx` | 8 | `Annotation` is a type and must be imported using a type-only import. | Change `import { Annotation }` to `import type { Annotation }`. |
| `src/components/game/GameStats.tsx` | 18 | `gameState` is declared but its value is never read. | Remove the unused variable or prefix with `_` if intended to be kept. |

### Linting Issues (`npm run lint`)
A total of 410 problems were found. Most are formatting issues (Prettier) which can be automatically fixed, but there are significant React Hook rule violations.

| File | Line | Issue | Proposed Solution |
| :--- | :--- | :--- | :--- |
| `src/pages/OffseasonDashboard.tsx` | 51-77 | **Critical:** React Hooks (`useState`, `useEffect`, `useSettingsStore`, `useNavigate`) are called conditionally (after an early return). | Move all Hook calls to the top of the component, before any conditional return statements. |
| `src/components/season/NewsFeed.tsx` | 132 | `useEffect` missing dependency `fetchNews`. | Add `fetchNews` to the dependency array or wrap the function in `useCallback`. |
| `src/components/game/GameStats.tsx` | 18 | Unused variable `gameState`. | Remove unused variable. |
| `src/context/ThemeContext.tsx` | 80 | Fast refresh only works when a file only exports components. | Move non-component exports (constants/functions) to a separate file or ensure only components are exported. |
| Various files | - | Usage of `any` type (`@typescript-eslint/no-explicit-any`). | Replace `any` with specific types or interfaces to ensure type safety. |

## Manual Review Findings

### 1. `src/pages/OffseasonDashboard.tsx`
**Critical Logic Error:**
- **Issue:** The component has an early return (`if (loaderData?.noSeason) ...`) *before* calling hooks like `useState`, `useSettingsStore`, `useEffect`. This violates the Rules of Hooks and will cause the application to crash or behave unpredictably if the condition changes between renders.
- **Proposed Solution:** Move the early return logic *after* all hooks are declared. Use a derived state or a conditional render in the return statement instead of an early return that skips hooks.

### 2. `src/components/season/NewsFeed.tsx`
**Potential Infinite Loop / Stale Closure:**
- **Issue:** `useEffect` relies on `fetchNews` but doesn't list it as a dependency. If `fetchNews` changes, the effect won't run. If `fetchNews` is unstable (re-created every render), adding it might cause an infinite loop.
- **Proposed Solution:** Wrap `fetchNews` definition in `useCallback` and include it in the `useEffect` dependency array.

### 3. `src/context/ThemeContext.tsx`
**Architecture/HMR Issue:**
- **Issue:** The file exports values that are not React components, breaking Hot Module Replacement (Fast Refresh).
- **Proposed Solution:** Move utility functions or constants to a separate file (e.g., `src/utils/themeUtils.ts`) and import them.

### 4. `src/components/common/TaskListPanel.tsx`
**Type Import Issue:**
- **Issue:** `verbatimModuleSyntax` is likely enabled in `tsconfig`, requiring `import type` for type-only imports.
- **Proposed Solution:** Update import to `import type { Annotation } from "../../hooks/useAnnotationList";`.

### 5. General Code Quality
- **Unused Variables:** Several files have unused variables (e.g., `gameState` in `GameStats.tsx`). These add noise and should be removed.
- **Explicit `any`:** Multiple instances of `any` usage reduce the benefits of TypeScript. Recommended to define proper interfaces (DTOs) for these data structures.

## Missing Files / Documentation Gaps

1. **`src/types/` Coverage:**
   - While many types exist, some complex objects in `useSimulationStore` (`engineData` properties) are typed as `Record<string, unknown>`. Defining specific interfaces for `Genesis`, `Empire`, etc., would improve type safety.

2. **Test Coverage:**
   - The `tests/` directory seems sparse compared to the source code. Recommended to add unit tests for utility functions and critical hooks (like `useSimulationStore`).

3. **Documentation:**
   - Many components lack JSDoc headers explaining their purpose and props. Adding these would help future maintainers.

## Recommended Action Plan
1. **Fix Critical Hook Violations:** Immediately refactor `OffseasonDashboard.tsx` to move all hooks to the top level.
2. **Fix Build Errors:** Update `TaskListPanel.tsx` imports and remove unused variables to get a clean `npm run build`.
3. **Run Auto-Fixers:** Run `npm run format` (if available) or `eslint --fix` to resolve the 300+ formatting issues.
4. **Type Hardening:** Replace `any` usages with proper types in `TrophyAssets.tsx` and `ThemeContext.tsx`.

---
*Report generated by Jules*

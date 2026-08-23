# BRIEFING — 2026-08-22T16:21:40Z

## Mission
Investigate R5 (Frontend State Management, Type Safety, Three.js GC, Redundant Fetches, Hardcoded IDs/URLs, Dead Stores/Files/Nav) and Testing Infrastructure (Backend tests, Frontend tests, E2E fixtures and tiers) across the THE-NFL-SIM-V2 repository.

## 🔒 My Identity
- Archetype: explorer
- Roles: frontend-specialist, test-architect, synthesizer
- Working directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_frontend_tests
- Original parent: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Milestone: codebase-survey

## 🔒 Key Constraints
- Read-only investigation — do NOT implement or write source code fixes
- Document exact file paths, line numbers, root causes, and recommended surgical fix strategies
- Write comprehensive findings to handoff.md
- Communicate results via send_message to parent

## Current Parent
- Conversation ID: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Updated: 2026-08-22T16:21:40Z

## Investigation State
- **Explored paths**:
  - `frontend/package.json`, `frontend/tsconfig.json`, `frontend/tsconfig.app.json`
  - `frontend/src/hooks/useLoaderData.ts`, `frontend/src/router.tsx`
  - `frontend/src/components/3d/PlayerCharacter.tsx`, `EnhancedPlayerCharacter.tsx`, `SkillNode3D.tsx`
  - `frontend/src/pages/SeasonDashboard.tsx`, `OffseasonDashboard.tsx`, `FrontOffice.tsx`, `DepthChart.tsx`, `LiveSim.tsx`, `TrainingCenter.tsx`, `MedicalCenter.tsx`, `TrophyRoom.tsx`, `SkillsPage.tsx`
  - `frontend/src/components/Navigation.tsx`
  - `frontend/src/store/` (`useGameStore.ts`, `usePlayLogStore.ts`, `useScoreboardStore.ts`, `useLiveVisualizationStore.ts`, `useDebugStore.ts`, `useSettingsStore.ts`, `useSimulationStore.ts`, `useBroadcastStore.ts`)
  - Legacy files: `DraftLegacy.tsx`, `DraftLegacy.css`, `FrontOffice_Baseline.tsx`, `SeasonDashboardLegacy.tsx`, `season.ts.backup`
  - `backend/tests/` (146+ test files), `conftest.py`, `pytest.ini`, `backend/tests/test_offseason_service.py`, `backend/tests/integration/test_draft_assistant.py`
  - `frontend/playwright.config.ts`, `frontend/e2e/` (46 test files)
- **Key findings**:
  - Unaligned route loader contracts in `useLoaderData.ts` failing on nullable seasons/teams.
  - Per-frame `new THREE.Vector3()` GC thrashing in `PlayerCharacter.tsx`, `EnhancedPlayerCharacter.tsx`, `SkillNode3D.tsx` generating 2,640+ allocations/sec.
  - Duplicate API fetches in `SeasonDashboard.tsx`, `OffseasonDashboard.tsx`, `FrontOffice.tsx`, `DepthChart.tsx` duplicating route loaders on mount.
  - Hardcoded URLs (`ws://localhost:8000`, `http://localhost:8000`) and team IDs (`teamId = 1`).
  - 5 dead Zustand stores and 4 legacy files identified.
  - 4 missing navigation items in `Navigation.tsx` (`/medical-center`, `/empire/trophy-room`, `/offseason`, `/skills`).
  - Backend test failures on `Player.speed` hybrid property comparator; mock masking in `test_offseason_service.py` (`win_pct` vs `win_percentage`).
  - 4-Tier test architecture documented with concrete execution matrix.
- **Unexplored areas**: None for survey scope.

## Key Decisions Made
- [Synthesis Complete]: All observations mapped with exact line numbers and remediation blueprints.

## Artifact Index
- handoff.md — Comprehensive Handoff Report

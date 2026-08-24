# Handoff Report — Comprehensive Frontend Survey & Component Audit

**Agent:** `teamwork_preview_explorer_survey_fe`  
**Parent Agent:** `e2795446-c3c5-4e9f-8b68-8c7a1cd58475`  
**Date:** 2026-08-23T21:07:30-04:00  
**Status:** COMPLETE (Hard Handoff)  
**Survey Report Path:** `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_fe\survey_frontend.md`

---

## 1. Observation

Direct observations from automated code scanning and AST analysis across `frontend/src/`:

1. **Total File Metrics:**
   - Total files analyzed in `frontend/src/`: 214 TypeScript/TSX files.
   - Total page views in `frontend/src/pages/`: 18 `.tsx` files (15 mounted, 3 legacy unmounted).
   - Total UI components in `frontend/src/components/`: 129 components across 24 directories.
   - 93 components are actively mounted in the router / page hierarchy.
   - 36 components + 3 legacy pages are unmounted / orphaned (0 incoming import or render calls in the active application tree).

2. **Entry Point & Router Configuration:**
   - Entry point: `frontend/src/App.tsx` renders `<RouterProvider router={router} />`.
   - `frontend/src/router.tsx` configures 15 top-level / nested routes within `frontend/src/layouts/MainLayout.tsx`.
   - `MainLayout.tsx` renders `Navigation.tsx` (14 sidebar items), `FeedbackWidget.tsx` (with 5 subcomponents), `SoundtrackPlayer.tsx`, and `Outlet`.

3. **13 Core Views Mapping:**
   - View 1: Franchise War Room / Dynasty Hub Dashboard (`/` & `/dashboard`) -> `pages/Dashboard.tsx` (Mounted).
   - View 2: Tactical Live Sim Chalkboard & Field Radar (`/live-sim`) -> `pages/LiveSim.tsx` (Mounted).
   - View 3: Offseason Draft Room with Multi-Lens Scouting Fog of War (`/offseason/draft` & `/draft`) -> `pages/DraftRoom.tsx` (Mounted).
   - View 4: Coaching Dynasty Tree & Staff Chemistry Matrix (`/playbook` -> Coaching Tree Tab) -> `pages/Playbook.tsx` (Mounted; renders `CoachingTree.tsx` & `CoachingDynastyTree.tsx`).
   - View 5: Medical Trauma Center & 5-Pathway Orthopedic Triage (`/medical-center` & `/medical`) -> `pages/MedicalCenter.tsx` (Mounted; renders `BodyMap.tsx`, `GenesisBiometricCard.tsx`, `FatigueMonitor.tsx`, `OrthopedicTriageModal.tsx`).
   - View 6: Depth Chart & Positional Hierarchy (`/empire/depth-chart` & `/depth-chart`) -> `pages/DepthChart.tsx` (Mounted; renders `ChemistryBadge.tsx`).
   - View 7: Roster Management & Capology Contracts (`/empire/front-office` & `/roster`) -> `pages/FrontOffice.tsx` (Mounted; renders `DraggableCard.tsx`, `PlayerCard.tsx`, `CoachSettings.tsx`).
   - View 8: Season Schedule & Week Simulator (`/season` Schedule tab) -> `pages/SeasonDashboard.tsx` (Mounted; renders `ScheduleView.tsx`, `SeasonSummaryCard.tsx`, `QuickActions.tsx`).
   - View 9: League Standings & Playoff Bracket (`/season` Standings & Playoffs tabs) -> `pages/SeasonDashboard.tsx` (Mounted; renders `StandingsTable.tsx`, `PlayoffBracket.tsx`, `LeagueLeaders.tsx`).
   - View 10: Player Profile & Biometric/S2 Cognition Card (`/players/:playerId/skills` & `/skills`) -> `pages/SkillsPage.tsx` (Mounted; renders `SkillTreeCanvas.tsx`, `SkillsOverlay.tsx`, `AbilityUnlockTree.tsx`, `TraitBadgeGrid.tsx`, `ArchetypeBadge.tsx`). `EnhancedPlayerProfile.tsx` is unmounted.
   - View 11: Front Office GM Trades & Valuation Matrix (`/empire/trade-center` & `/trades`) -> `pages/TradeCenterPage.tsx` (Mounted; renders `TradeNegotiator.tsx`, `TradeBlock.tsx`, `PendingOffers.tsx`, `DroppableZone.tsx`, `DraggableAsset.tsx`, `TradeAnalyzer.tsx`).
   - View 12: Cryptographic Replay Verification Telemetry (`/live-sim`) -> `pages/LiveSim.tsx` (Mounted; renders `LiveGameVisualizer.tsx`, `FieldCanvas.tsx`, `GridironVisualizer.tsx`). `ReplayScrubber.tsx` and `PlayAnimator.tsx` are unmounted.
   - View 13: League Settings & Weather Simulation Config (`/settings`) -> `pages/Settings.tsx` (Mounted).

4. **Identified Mock & Placeholder Occurrences (16 key locations):**
   - `frontend/src/services/scouting.ts`: Inlines `MOCK_SCOUTING_REPORT` (Line 7) and `MOCK_BACKSHIORY` (Line 32).
   - `frontend/src/services/tradeApi.ts`: Inlines `generateMockIncomingOffers()` (Line 291), mock pending offers fallback (Line 221), and mock trade responses (Line 246).
   - `frontend/src/services/ImageGenService.ts`: Inlines `mockImages` array (Line 21) and mock generator (Line 54).
   - `frontend/src/router.tsx`: `draftRoomLoader()` (Lines 148-205) hardcodes `mockTeams`, `mockSeason`, `mockCurrentPick`.
   - `frontend/src/pages/Dashboard.tsx`: Hardcoded opponent calculation (Line 89).
   - `frontend/src/pages/LiveSim.tsx`: Mock ball trajectory fallback (Line 64).
   - `frontend/src/components/3d/LiveGameVisualizer.tsx`: Inlines `mockPlayResult` object (Lines 116-126).
   - `frontend/src/components/coaching/GameplanDashboard.tsx`: Hardcoded familiarity numbers (Lines 47, 87).
   - `frontend/src/components/game/FieldCanvas.tsx`: Offense/defense team color hardcoded by `player_id < 11` (Line 205).
   - `frontend/src/components/history/LogoTimeline.tsx`: `MOCK_HISTORY` array (Line 5).
   - `frontend/src/components/medical/GenesisBiometricCard.tsx`: Hardcoded default biometrics fallback (Line 23).
   - `frontend/src/components/skills/SkillTreeCanvas.tsx`: Defaults trait tier to `GOLD` (Line 89).
   - `frontend/src/components/skills/SkillsOverlay.tsx`: Mock trait info (Line 83).
   - `frontend/src/components/trades/PendingOffers.tsx`: Mock fallback on error (Line 25).
   - `frontend/src/pages/DraftRoom.tsx`: Commented TODO for recent picks ticker (Line 35).

5. **Legacy & Unmounted Prototypes:**
   - 3 Unmounted Pages: `pages/DraftLegacy.tsx`, `pages/FrontOffice_Baseline.tsx`, `pages/SeasonDashboardLegacy.tsx`.
   - 36 Unmounted Components: `3d/FieldVisualizer`, `3d/PlayAnimator`, `3d/PlayerCharacter`, `3d/SceneContainer`, `ErrorBoundary`, `FieldView`, `coaching/CoachCard`, `coaching/CoachingUnlockPanel`, `common/NewsFeed`, `common/TraitBadge`, `common/TraitTooltip`, `dev/TraitManager`, `game/FatigueIndicator`, `game/ReplayScrubber`, `history/LogoTimeline`, `immersive/SpotlightButton`, `medical/TreatmentModal`, `news/NewsFeedWidget`, `news/StorylineTracker`, `news/WeeklyRecapModal`, `news/index.ts`, `shared/TraitBadge`, `trades/TradeCenter`, `trades/index.ts`, `training/CampSchedulePlanner`, `training/CoachingStylePicker`, `training/DrillCard`, `training/PlayerProgressChart`, `transitions/PageTransition`, `transitions/index.ts`, `transitions/transitionVariants.ts`, `ui/Badge`, `ui/EnhancedPlayerProfile`, `ui/PrimeCard`, `ui/Sidebar`, `ui/TraitNotification`.

---

## 2. Logic Chain

1. From **Observation 1 & 2**, all application routes originate from `App.tsx` -> `router.tsx` -> `MainLayout.tsx`.
2. By traversing every route definition in `router.tsx`, each of the 15 active pages was traced down through all nested child JSX elements to map the full reachable component tree.
3. From **Observation 3**, all 13 core views mandated in `ORIGINAL_REQUEST.md` have corresponding page views and are reachable in the route graph.
4. From **Observation 4**, specific sub-views and services still rely on mock fallback data (notably `services/scouting.ts`, `services/tradeApi.ts`, `router.tsx` draftRoomLoader, and `GameplanDashboard.tsx` familiarity percentages) rather than querying live FastAPI backend endpoints.
5. From **Observation 5**, 36 component files were identified as unmounted. These fall into three distinct categories:
   - **High-Value Features to Wire:** `ReplayScrubber.tsx` (LiveSim replay mode), `TreatmentModal.tsx` (Medical 5-pathway triage), `EnhancedPlayerProfile.tsx` (Player card detail modal), `NewsFeedWidget.tsx` / `StorylineTracker.tsx` (Emergent world narrative in Dashboard), `LogoTimeline.tsx` (Franchise history in TrophyRoom).
   - **Superseded Early Prototypes:** `FieldVisualizer.tsx`, `PlayerCharacter.tsx`, `FieldView.tsx`, `CoachingStylePicker.tsx`, `DrillCard.tsx`, `TradeCenter.tsx`, `DraftLegacy.tsx`, `SeasonDashboardLegacy.tsx`.
   - **Atoms & Dead Barrels:** `Badge.tsx`, `PrimeCard.tsx`, `SpotlightButton.tsx`, `trades/index.ts`, `news/index.ts`, `transitions/index.ts`.

---

## 3. Caveats

- **No Source Modification Constraint:** In accordance with the Explorer archetype instructions, no source files in `frontend/src/` were edited. All proposals are documented in `survey_frontend.md`.
- **Backend Schema Sync Dependent:** Connecting components with mock services (`scouting.ts`, `tradeApi.ts`) will require the backend endpoints in `backend/app/api/` to be confirmed active and contract-aligned by the backend explorer/implementer.

---

## 4. Conclusion

The frontend codebase is well-structured with a modern React Router v7 data-driven routing architecture, a rich Three.js / Canvas live simulation visualizer, Framer Motion animations, and complete 13-view coverage. The primary remediation needs are:
1. **Wire High-Value Unmounted Components:** Mount `ReplayScrubber.tsx` (LiveSim), `TreatmentModal.tsx` (MedicalCenter), `EnhancedPlayerProfile.tsx` (FrontOffice/DepthChart), and `StorylineTracker.tsx` (Dashboard).
2. **Replace Mock Fallbacks in Services:** Convert `services/scouting.ts`, `services/tradeApi.ts`, and `router.tsx` `draftRoomLoader` to live API endpoints.
3. **Archive/Clean Legacy Prototypes:** Safely remove or isolate legacy unmounted prototype files.

---

## 5. Verification Method

To independently verify the frontend survey findings:

1. **Verify Component Catalog & Route Reachability:**
   ```powershell
   python .agents/teamwork_preview_explorer_survey_fe/graph_builder.py
   python .agents/teamwork_preview_explorer_survey_fe/inspect_components.py
   ```
2. **Verify Frontend Compilation:**
   ```powershell
   cd frontend
   npm run build
   ```
3. **Inspect Full Survey Documentation:**
   Open and read `.agents/teamwork_preview_explorer_survey_fe/survey_frontend.md`.

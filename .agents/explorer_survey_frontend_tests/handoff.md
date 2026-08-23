# Comprehensive Survey Report: Frontend State Management, Type Safety, Performance & Testing Infrastructure

**Author:** Explorer 3 (Frontend & Testing Infrastructure Specialist)  
**Target Project:** THE-NFL-SIM-V2  
**Working Directory:** `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_frontend_tests`  
**Date:** 2026-08-22  

---

## 1. Observation

Direct observations from codebase inspection, compiler diagnostics, and test execution:

### 1.1 Frontend Toolchain & Build Status
- **Package Manager & Scripts (`frontend/package.json` lines 6–18):**
  * `"build": "tsc -b && vite build"`
  * `"lint": "eslint ."`
  * `"test:e2e": "playwright test"`
  * Dependencies include React 19.2.0, React Router DOM 7.9.6, Vite 7.2.4, TypeScript 5.9.3, Three.js 0.181.2, @react-three/fiber 9.4.2, @react-three/drei 10.7.7, Zustand 5.0.8, Axios 1.13.2, Tailwind CSS 4.1.18.
- **Build Execution Result:**
  * Running `npm run build` (`tsc -b && vite build`) succeeded with 0 TypeScript compilation errors and bundled 3,729 modules in 28.54s into `frontend/dist/`.
  * Warning detected: `src/services/traits.ts` is dynamically imported in `router.tsx` and statically imported in `SkillsPage.tsx`.

### 1.2 Route Loader Type Contract Inconsistencies (`useLoaderData.ts` vs `router.tsx`)
- **`frontend/src/hooks/useLoaderData.ts` (lines 30–38):**
  ```typescript
  export interface OffseasonDashboardLoaderData {
    teams: Team[];
    season: Season; // Non-nullable type contract!
    isOffseason: boolean;
  }
  ```
- **`frontend/src/router.tsx` (lines 129–136):**
  ```typescript
  // When no season exists, router returns:
  return {
    teams,
    season: null,
    isOffseason: false,
    noSeason: true,
  };
  ```
- **Discrepancy Impact in `frontend/src/pages/OffseasonDashboard.tsx` (lines 28–33, 37):**
  * `OffseasonDashboard.tsx` bypassed `useLoaderData.ts` and created its own local interface `interface OffseasonLoaderData { teams: Team[]; season: Season | null; isOffseason: boolean; noSeason: boolean; }` because `useOffseasonDashboardData` in `useLoaderData.ts` has an invalid type contract that assumes `season` is never null and omits `noSeason`.
- **`frontend/src/hooks/useLoaderData.ts` (lines 65–73):**
  ```typescript
  export interface DepthChartLoaderData {
    teams: Team[];
    team: Team; // Non-nullable type contract!
    roster: Player[];
  }
  ```
  * In `router.tsx` (line 266), `const team = teams.find((t) => t.id === teamId) ?? null;` returns `Team | null`. The hook incorrectly asserts `team: Team`.

### 1.3 Three.js 60FPS GC Allocation Thrashing (Per-Frame `Vector3`)
- **`frontend/src/components/3d/PlayerCharacter.tsx` (lines 25–37):**
  ```typescript
  useFrame((state, delta) => {
    if (meshRef.current) {
      const target =
        isAnimating && targetPosition
          ? new THREE.Vector3(...targetPosition)
          : new THREE.Vector3(...position);

      meshRef.current.position.lerp(target, delta * 5);
  ```
  * Instantiates a `new THREE.Vector3` on every animation tick. With 22 players on field @ 60 FPS = **1,320 allocations/sec**.
- **`frontend/src/components/3d/EnhancedPlayerCharacter.tsx` (lines 61–68):**
  ```typescript
  useFrame((state, delta) => {
    if (groupRef.current) {
      const target =
        isAnimating && targetPosition
          ? new THREE.Vector3(...targetPosition)
          : new THREE.Vector3(...position);

      groupRef.current.position.lerp(target, delta * 5);
  ```
  * Instantiates a `new THREE.Vector3` on every animation tick for every enhanced character = **1,320 allocations/sec**. Combined with `PlayerCharacter`, this exceeds **2,640 allocations/sec**.
- **`frontend/src/components/skills/SkillNode3D.tsx` (lines 72–80):**
  ```typescript
  useFrame((_state, delta) => {
    if (meshRef.current) {
      const targetScale = hovered ? 1.2 : 1.0;
      meshRef.current.scale.lerp(
        new THREE.Vector3(targetScale, targetScale, targetScale),
        delta * 10
      );
  ```
  * Instantiates `new THREE.Vector3` on every frame for every node in the skill tree.

### 1.4 Redundant Component-Mount API Fetches Duplicating Route Loaders
- **`frontend/src/pages/SeasonDashboard.tsx` (lines 52–106):**
  * `useEffect(() => { const fetchData = async () => { ... } fetchData(); }, []);`
  * Executes `api.getTeams()`, `seasonApi.getSeasonSummary()`, `seasonApi.getStandings()`, `seasonApi.getSchedule()`, `seasonApi.getLeagueLeaders()`, `seasonApi.getProjectedAwards()`, `seasonApi.getPlayoffBracket()`.
  * This is an exact 1:1 duplicate of `seasonDashboardLoader` in `router.tsx` (lines 36–97), causing a duplicate burst of 7 API network calls immediately upon component mount.
- **`frontend/src/pages/OffseasonDashboard.tsx` (lines 73–100):**
  * `useEffect` unconditionally fetches `seasonApi.getCurrentSeason()` and `seasonApi.getTeamNeeds()`, duplicating loader data.
- **`frontend/src/pages/FrontOffice.tsx` (lines 35–50):**
  * Ignores `frontOfficeLoader` from `router.tsx` (lines 209–247) and executes its own `api.getTeam(1)` and `api.getTeamRoster(1)` in a mount `useEffect`.
- **`frontend/src/pages/DepthChart.tsx` (lines 27–29, 50–66):**
  * Ignores `depthChartLoader` from `router.tsx` (lines 250–274) and executes `api.getTeamRoster(1)` and `api.getTeamChemistry(1)` in a mount `useEffect`.

### 1.5 Hardcoded Network URLs & Hardcoded Franchise IDs
- **Hardcoded URLs (`http://localhost:8000` / `ws://localhost:8000`):**
  * `frontend/src/pages/LiveSim.tsx` (line 29): `const wsUrl = isLive ? "ws://localhost:8000/ws/simulation/live" : null;`
  * `frontend/src/pages/TrainingCenter.tsx` (lines 49–51): `axios.get("http://localhost:8000/api/v1/players/${playerId}/training-profile")`
  * `frontend/src/components/ui/EnhancedPlayerProfile.tsx` (line 167): `fetch("http://localhost:8000/api/players/${playerId}/profile")`
  * Environment variable inconsistency: `VITE_API_BASE_URL` used in `api.ts`, `physicsService.ts`, `tradeApi.ts`; whereas `VITE_API_URL` used in `traitService.ts` and `NewsFeed.tsx`.
- **Hardcoded Franchise IDs (`teamId = 1`):**
  * `frontend/src/pages/FrontOffice.tsx` (lines 38–39): `api.getTeam(1)`, `api.getTeamRoster(1)`
  * `frontend/src/pages/DepthChart.tsx` (lines 52, 56, 76): `api.getTeamRoster(1)`, `api.getTeamChemistry(1)`, `api.updateDepthChart(1, ...)`

### 1.6 Dead Zustand Stores, Legacy/Unused Files & Missing Navigation Links
- **Dead Zustand Stores in `frontend/src/store/` (0 external references):**
  1. `useGameStore.ts` (12 lines) — completely dead.
  2. `usePlayLogStore.ts` (43 lines) — dead; play logs are maintained inside `useSimulationStore.ts`.
  3. `useScoreboardStore.ts` (68 lines) — dead; scoreboard is managed inside `useSimulationStore.ts`.
  4. `useLiveVisualizationStore.ts` (25 lines) — dead; live game visualization uses `useBroadcastStore.ts`.
  5. `useDebugStore.ts` (42 lines) — dead; unreferenced.
  * Active stores confirmed: `useSettingsStore.ts`, `useSimulationStore.ts`, `useBroadcastStore.ts`.
- **Legacy & Unused Files:**
  * `frontend/src/pages/DraftLegacy.tsx` & `frontend/src/pages/DraftLegacy.css`
  * `frontend/src/pages/FrontOffice_Baseline.tsx`
  * `frontend/src/pages/SeasonDashboardLegacy.tsx`
  * `frontend/src/types/season.ts.backup`
- **Missing Navigation Items in `frontend/src/components/Navigation.tsx` (lines 36–48):**
  * Missing: `/offseason` (Offseason Hub / Dashboard)
  * Missing: `/medical-center` (Medical Center / Injury & Biometrics Triage)
  * Missing: `/empire/trophy-room` (Trophy Room / Hall of Champions)
  * Missing: `/skills` (Player Skills & Trait Tree)

### 1.7 Testing Infrastructure (Backend & Frontend)
- **Backend Test Harness (`backend/tests/conftest.py`, `pytest.ini`):**
  * Root config in `pytest.ini` defines custom markers.
  * `backend/tests/conftest.py` provides SQLite file-based WAL testing with session and function scoped fixtures: `db_session`, `async_db_session`, `client` (FastAPI TestClient with dependency overrides), `async_client` (httpx AsyncClient), `sample_teams`, `sample_players`, `clear_tables` (autouse cleanup).
  * Test execution observation: Running pytest triggered a fatal failure in `test_draft_assistant.py` and `test_draft_suggestion_api.py`:
    `AttributeError: Neither 'InstrumentedAttribute' object nor 'Comparator' object associated with Player.attributes has an attribute 'speed'` in `Player.speed` hybrid property.
  * Mock Masking observation: `backend/tests/test_offseason_service.py` (lines 61–67) defined `MockStandingEntry` with `self.win_pct = win_pct`, masking the fact that SQLAlchemy `TeamStanding` model uses `win_percentage`.
- **Frontend Test Harness (`frontend/playwright.config.ts`, `frontend/e2e/`):**
  * 46 Playwright spec files covering all major user journeys (`dashboard-flow`, `draft-room`, `front-office`, `live-sim-flow`, `offseason-flow`, `playbook-flow`, `season-dashboard-flow`, `trade-center-flow`, `visual-regression.spec.ts`, etc.).
  * Test webServer points to `http://localhost:5199` using `npx vite --port 5199`.

---

## 2. Logic Chain

```
[Observation 1.2: useLoaderData.ts defines season: Season non-null]
       + [Observation 1.2: router.tsx returns season: null, noSeason: true when uninitialized]
       ==> INFERENCE: Type contract violation between route loaders and page consumers.
       ==> CONSEQUENCE: OffseasonDashboard.tsx had to implement a local shadow type to avoid TypeScript compile errors; if consumer uses useOffseasonDashboardData(), accessing season.id causes unhandled TypeError at runtime.

[Observation 1.3: new THREE.Vector3 instantiated in useFrame() across 3 components]
       + [Math: 22 players * 2 visualizers * 60 FPS = 2,640 allocations/sec]
       ==> INFERENCE: High-frequency memory allocations trigger frequent JavaScript V8 Garbage Collection cycles.
       ==> CONSEQUENCE: Periodic micro-stutters and frame rate drops below 60 FPS on 3D field rendering and skill tree interactions.

[Observation 1.4: SeasonDashboard.tsx runs useEffect(fetchData, []) on mount]
       + [Observation 1.4: seasonDashboardLoader in router.tsx already fetches all 7 endpoints]
       ==> INFERENCE: Dual-fetch lifecycle creates redundant network traffic and potential race conditions.
       ==> CONSEQUENCE: Unnecessary server load (14 requests instead of 7 per page view) and potential UI flickering when initial loader state is replaced by mount state.

[Observation 1.5: Hardcoded localhost:8000 and teamId = 1 across pages]
       ==> INFERENCE: Pages are decoupled from runtime environment configs and active user franchise settings.
       ==> CONSEQUENCE: App fails when deployed behind a non-default host/port (e.g. Docker, staging domain) and user franchise selection in TeamSelection is ignored by FrontOffice and DepthChart.

[Observation 1.6: 5 dead stores, 4 legacy files, 4 missing navigation routes]
       ==> INFERENCE: Frontend codebase has dead artifact accumulation and incomplete primary navigation.
       ==> CONSEQUENCE: Developer confusion, bloated bundle size, and orphaned views unreachable from the main sidebar.
```

---

## 3. Caveats

1. **Production Bundle Verification**: While `npm run build` passes cleanly, E2E test runs require a live FastAPI backend with seeded database tables to prevent network timeout errors during Playwright assertions.
2. **WebSocket Port Configuration**: WebSocket endpoint paths differ between legacy `ws://localhost:8000/ws/simulation/live` and newer room-isolated `/api/live/ws/game/{game_id}`. The WebSocket helper must handle both single-game and legacy broadcast protocols.
3. **Playwright Visual Snapshots**: Visual regression tests (`visual-regression.spec.ts`) rely on exact platform rendering (win32). Screenshots may differ across operating systems (Linux CI vs Windows).

---

## 4. Conclusion & Actionable Remediation Blueprint

### Remediation Blueprint for R5 & Testing Infrastructure

#### Action 1: Reconcile Route Loader Types in `useLoaderData.ts`
- **File:** `frontend/src/hooks/useLoaderData.ts`
- **Surgical Changes:**
  1. Update `OffseasonDashboardLoaderData` to:
     ```typescript
     export interface OffseasonDashboardLoaderData {
       teams: Team[];
       season: Season | null;
       isOffseason: boolean;
       noSeason: boolean;
     }
     ```
  2. Update `DraftRoomLoaderData` to include `noSeason: boolean` and `season: Season | null`.
  3. Update `DepthChartLoaderData` to declare `team: Team | null`.
  4. Ensure `OffseasonDashboard.tsx` removes local `OffseasonLoaderData` and imports `useOffseasonDashboardData()`.

#### Action 2: Eliminate Three.js GC Allocations via Scratch Vectors
- **Files:** `frontend/src/components/3d/PlayerCharacter.tsx`, `frontend/src/components/3d/EnhancedPlayerCharacter.tsx`, `frontend/src/components/skills/SkillNode3D.tsx`
- **Surgical Changes:**
  1. In `PlayerCharacter.tsx` & `EnhancedPlayerCharacter.tsx`:
     * Declare module-level scratch vectors:
       ```typescript
       const _scratchTarget = new THREE.Vector3();
       ```
     * In `useFrame`, replace `new THREE.Vector3(...)` with:
       ```typescript
       if (isAnimating && targetPosition) {
         _scratchTarget.set(targetPosition[0], targetPosition[1], targetPosition[2]);
       } else {
         _scratchTarget.set(position[0], position[1], position[2]);
       }
       meshRef.current.position.lerp(_scratchTarget, delta * 5);
       ```
  2. In `SkillNode3D.tsx`:
     * Replace `meshRef.current.scale.lerp(new THREE.Vector3(...), delta * 10)` with:
       ```typescript
       const currentScale = meshRef.current.scale.x;
       const newScale = THREE.MathUtils.lerp(currentScale, targetScale, delta * 10);
       meshRef.current.scale.set(newScale, newScale, newScale);
       ```

#### Action 3: Remove Redundant Mount Fetches in Pages
- **Files:** `frontend/src/pages/SeasonDashboard.tsx`, `frontend/src/pages/OffseasonDashboard.tsx`, `frontend/src/pages/FrontOffice.tsx`, `frontend/src/pages/DepthChart.tsx`
- **Surgical Changes:**
  1. In `SeasonDashboard.tsx`: Remove the initial `fetchData()` `useEffect` on mount. Derive initial state strictly from `loaderData`. Retain `handleWeekChange` and manual refresh triggers.
  2. In `FrontOffice.tsx` & `DepthChart.tsx`: Consume `useFrontOfficeData()` and `useDepthChartData()` from route loaders instead of issuing redundant queries on mount.

#### Action 4: Unify Network Config & Franchise State
- **Files:** `frontend/src/config/network.ts` (or `frontend/src/utils/url.ts`), `frontend/src/pages/LiveSim.tsx`, `frontend/src/pages/TrainingCenter.tsx`, `frontend/src/components/ui/EnhancedPlayerProfile.tsx`, `frontend/src/pages/FrontOffice.tsx`, `frontend/src/pages/DepthChart.tsx`
- **Surgical Changes:**
  1. Create a canonical `getApiBaseUrl()` and `getWebSocketUrl(path: string)` helper reading `import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || "http://localhost:8000"`.
  2. Replace hardcoded `ws://localhost:8000` and `http://localhost:8000` with the helper.
  3. Replace hardcoded team `1` with `useSettingsStore((s) => s.userTeamId) ?? 1`.

#### Action 5: Purge Dead Stores, Legacy Files & Add Navigation Links
- **Purge 5 Dead Stores:** Delete `frontend/src/store/useGameStore.ts`, `usePlayLogStore.ts`, `useScoreboardStore.ts`, `useLiveVisualizationStore.ts`, `useDebugStore.ts`.
- **Purge 4 Legacy Files:** Delete `frontend/src/pages/DraftLegacy.tsx`, `DraftLegacy.css`, `FrontOffice_Baseline.tsx`, `SeasonDashboardLegacy.tsx`, `src/types/season.ts.backup`.
- **Update Navigation:** In `frontend/src/components/Navigation.tsx`, add:
  ```typescript
  { path: "/offseason", label: "OFFSEASON", icon: Sparkles, tag: "HUB" },
  { path: "/medical-center", label: "MEDICAL", icon: Stethoscope, tag: "HEALTH" },
  { path: "/empire/trophy-room", label: "TROPHIES", icon: Award, tag: "DYNASTY" },
  { path: "/skills", label: "SKILLS", icon: Zap, tag: "TREE" },
  ```

#### Action 6: 4-Tier Test Architecture Matrix
- **Tier 1 (Static Analysis & Type Contracts):**
  * Command: `cd frontend && npm run build` (`tsc -b && vite build`) & `cd backend && python -m pytest backend/tests/test_models.py`
  * Verifies: 0 TS compilation errors, ORM model registration in metadata, Pydantic V2 schema compliance.
- **Tier 2 (Unit & Physics Kernels):**
  * Command: `pytest backend/tests/test_60hz_physics.py backend/tests/test_engines.py backend/tests/test_depth_chart.py`
  * Verifies: Deterministic RNG checksums, safety scoring when `yard_line <= 0`, clock runoff math (4–7s incomplete vs 25–38s tackle), dynamic PAT/2-PT execution.
- **Tier 3 (Integration & Lifecycle Services):**
  * Command: `pytest backend/tests/integration/ backend/tests/test_offseason_service.py backend/tests/test_season_api.py`
  * Verifies: Real `TeamStanding.win_percentage` draft ordering, `FreeAgencyEngine` market bidding, `WeekSimulator` single-game ID reuse, room-isolated WebSocket broadcasts.
- **Tier 4 (End-to-End System & UI Journeys):**
  * Command: `cd frontend && npx playwright test e2e/router.spec.ts e2e/season-dashboard-flow.spec.ts e2e/offseason-flow.spec.ts e2e/front-office.spec.ts`
  * Verifies: Route loader empty states (`noSeason: true`), full multi-week season simulation, 3D Canvas visualizer rendering without frame drops, user franchise customization persistence.

---

## 5. Verification Method

To independently verify these findings:

1. **Verify Type Contract & Build:**
   ```powershell
   cd frontend
   npm run build
   ```
2. **Inspect Three.js Vector Allocations:**
   ```powershell
   Select-String -Path "frontend\src\components\3d\*.tsx", "frontend\src\components\skills\*.tsx" -Pattern "new THREE.Vector3"
   ```
3. **Inspect Dead Zustand Stores:**
   ```powershell
   Get-ChildItem -Path "frontend\src\store"
   ```
4. **Inspect Navigation Items:**
   ```powershell
   Select-String -Path "frontend\src\components\Navigation.tsx" -Pattern "path:"
   ```
5. **Run Backend Test Suite & Observe Hybrid Property / Mock Failures:**
   ```powershell
   cd backend
   pytest tests/integration/test_draft_assistant.py tests/test_offseason_service.py -v
   ```

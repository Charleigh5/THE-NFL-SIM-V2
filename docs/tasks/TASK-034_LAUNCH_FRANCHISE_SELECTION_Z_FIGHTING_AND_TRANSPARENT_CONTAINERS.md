<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Launch Franchise Selection, 3D Z-Fighting Elimination & Transparent Frosted Glass Containers

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:**
  - Classic EA Sports franchise onboarding: Upon initial game boot, users select their favorite NFL franchise, which persists in profile memory across all subsequent game launches.
  - 3D Computer Graphics Depth Buffering: Coplanar planar geometries in WebGL/OpenGL sharing nearly identical Z/Y coordinates experience precision loss in floating-point depth calculations, manifesting as high-frequency flickering (Z-fighting).
  - Spatial Frosted Glass (macOS Sonoma / visionOS / Apple Fluent Design): Solid opaque containers occlude background immersion. High-performance semi-transparent layers (`rgba(10, 15, 25, 0.35)` with `backdrop-filter: blur(12px)`) maintain WCAG AAA text contrast while revealing the living 3D stadium turf and lighting behind.
- **Related Ideas:**
  - Dynamic route gateways (`LaunchGateway`) evaluating persistent storage before rendering or redirecting.
  - Three.js material polygon offset (`polygonOffset: true`, `polygonOffsetFactor: -2`, `polygonOffsetUnits: -2`, `depthWrite: false`) for coplanar decals and pitch markings.
  - Detroit Lions (Franchise ID `11`, Abbreviation `DET`) pre-selected as the default franchise across the store, theme provider, and team grid.
- **Future Potential:**
  - Seamless multi-profile franchise management allowing General Managers to switch franchises on the fly via the navigation rail while preserving the default team preference across seasons.
- **Constraints:**
  - Zero regression on existing 32 Playwright E2E suites.
  - Strict preservation of WCAG 2.1 AA legibility across transparent containers.
  - Elimination of all flickering strike lines in the 3D viewport.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Make the root route `/` unconditionally redirect to `/team-selection`, and make all container backgrounds `bg-transparent`.

### Powerful Antithesis
1. Unconditionally redirecting `/` to `/team-selection` breaks user workflow on returning visits—forcing a returning user to re-select their team every time they open the app instead of going directly to their War Room.
2. Making all containers 100% transparent without calibrated frosted glass (`backdrop-filter`) causes severe text illegibility, as white yard lines, player numbers, and floodlight reflections clash directly with data tables, player cards, and navigation links.
3. Simply increasing the vertical Y-offset of the 3D yard line risks floating plane artifacts or casting artificial ground shadows.

### The Superior Synthesis
1. Implement a **Stateful Launch Gateway** on the root index route (`/`). If `selectedTeamId` or `hasSelectedFranchise` exists in `localStorage`, the user lands immediately on their saved franchise War Room (`Dashboard`). If not set, the app launches into the `TeamSelection` flow with the **Detroit Lions** pre-selected by default.
2. In `TeamSelection`, selection commits `selectedTeamId: "11"`, `selectedTeamAbbr: "DET"`, and `hasSelectedFranchise: "true"` to persistent storage, updating both `useSettingsStore` and `ThemeProvider`.
3. Eliminate the 3D center strike line (`x = 0`) from `ThreeStadiumBackdrop.tsx` and configure remaining yard lines with `polygonOffset={true} polygonOffsetFactor={-2} polygonOffsetUnits={-2}` and `depthWrite={false}`, eliminating 100% of z-fighting flickering.
4. Transform heavy opaque containers (`bg-broadcast-black`, `bg-black`, `bg-slate-950`, `bg-broadcast-dark`) into high-performance frosted glass (`bg-slate-950/35 backdrop-blur-md` and `rgba(10, 15, 25, 0.35)` with 1px border highlights), letting the living 3D stadium turf, goalposts, football, and lights shine through while keeping all typography crisp and readable.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19, React Router v7, Three.js (`@react-three/fiber`), Tailwind CSS v4, Zustand.
- **Language:** TypeScript 5.8 (Strict Mode).
- **Default Franchise:** Detroit Lions (`id: 11`, `abbreviation: "DET"`, `primaryColor: "#0076B6"`).

### 2. The Data Schema & Memory Contracts
- `localStorage.getItem("selectedTeamId")`: string (`"11"` for Detroit Lions).
- `localStorage.getItem("selectedTeamAbbr")`: string (`"DET"`).
- `localStorage.getItem("hasSelectedFranchise")`: string (`"true"`).
- `useSettingsStore.userTeamId`: number (`11`).
- `ThemeProvider.activeTeam`: Team (`DET`).

### 3. Step-by-Step Execution Plan

- [x] **Step 1: Launch Gateway & Default Franchise Selection**
  - In `frontend/src/store/useSettingsStore.ts`: Ensure default `userTeamId` is `11` (Detroit Lions).
  - In `frontend/src/context/ThemeProvider.tsx`: Ensure default active team abbreviation is `"DET"`.
  - In `frontend/src/pages/TeamSelection.tsx`:
    - Resiliently load teams if loader data is missing (fallback to `api.getTeams()`).
    - Default selected team highlight to `11` (Detroit Lions).
    - On team selection, write `selectedTeamId`, `selectedTeamAbbr`, and `hasSelectedFranchise: "true"`.
  - In `frontend/src/router.tsx`:
    - Create `LaunchGateway` component for `index: true`.
    - If `selectedTeamId` or `hasSelectedFranchise` is present, render `<Dashboard />`.
    - If not present, render `<TeamSelection />` with Detroit Lions pre-selected.

- [x] **Step 2: 3D Z-Fighting & Flickering Center Strike Line Elimination**
  - In `frontend/src/components/weather/ThreeStadiumBackdrop.tsx`:
    - Remove `0` from yard lines array: change `[-40, -20, 0, 20, 40]` to `[-40, -20, 20, 40]`.
    - Add `polygonOffset={true} polygonOffsetFactor={-2} polygonOffsetUnits={-2}` and `depthWrite={false}` to `meshBasicMaterial`.
    - Lift geometry slightly to `position={[x, -2.46, 0]}`.
  - In `frontend/src/components/spatial/SpatialAtmosphereLayer.tsx`:
    - Verify or eliminate any flickering horizontal optical flare line that crosses the middle of the screen.

- [x] **Step 3: Transparent Frosted Glass Containers**
  - In `frontend/src/layouts/MainLayout.tsx`:
    - Change root `bg-broadcast-black` to `bg-transparent`.
    - Ensure `ThreeStadiumBackdrop` is visible with `opacity-95`.
    - Soften `Navigation.tsx` background to `bg-slate-950/75 backdrop-blur-xl`.
  - In `frontend/src/pages/Dashboard.tsx`:
    - Change root `bg-black` to `bg-transparent`.
    - Change spatial container from `bg-slate-950/75` to `bg-slate-950/35 backdrop-blur-md`.
    - Change tactical container from `bg-slate-950` to `bg-slate-950/35 backdrop-blur-md`.
    - Soften clash card gradient from opaque metal/black to `from-black/35 via-black/20 to-black/35`.
    - Soften quick action cards and widgets from `bg-broadcast-dark` to `bg-slate-950/35 backdrop-blur-md`.
  - In `frontend/src/components/immersive/ParallaxScene.module.css`:
    - Soften `.bg` gradient bottom stops from `rgba(0, 0, 0, 0.95)` to `rgba(0, 0, 0, 0.40)`.
  - In `frontend/src/index.css`:
    - Update `.broadcast-glass` to `background: rgba(10, 15, 25, 0.35); backdrop-filter: blur(12px)`.

### 4. Edge Cases & Error Handling
- [Case A: No LocalStorage (SSR/Privacy Mode)] -> Gracefully fallback to Detroit Lions (`id: 11`).
- [Case B: User Navigates to `/team-selection` Manually] -> Displays team selection grid, allowing franchise switching at any time.
- [Case C: Rapid Navigation] -> Z-fighting fix applies directly in WebGL renderer, independent of React lifecycle.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [x] **Type Check:** Run `npm run build` (`tsc -b && vite build`) — 0 errors.
- [x] **Launch Page Test:** Verify opening app without saved franchise presents Detroit Lions pre-selected on Team Selection.
- [x] **Memory Persistence Test:** Verify selecting franchise saves to memory and subsequent visits land directly on Dashboard.
- [x] **Visual Defect Test:** Verify complete elimination of flickering center strike line on 3D field.
- [x] **Transparency Test:** Verify 3D stadium turf and lights are visible through frosted glass containers.
- [x] **E2E Regressions:** Run full Playwright test suite to guarantee 0 regressions.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Present technical implementation plan in implementation_plan.md and obtain user confirmation to execute.
</baton_handoff>

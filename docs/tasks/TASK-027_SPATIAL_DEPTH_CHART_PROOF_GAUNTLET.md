# TASK-027 — Spatial Depth Chart Proof Gauntlet

## Objective

Convert storyboard Scene 05 into a truthful, testable reference slice without inventing missing assets or replacing proven depth-chart persistence logic.

## Authority / Evidence

1. `STORYBOARD_UI_UX_ANIMATION_BLUEPRINT.md` — Scene 05 intent: magnetic war board, draggable player nameplates, snap feedback, diegetic spatial room.
2. Observed repository state at baseline commit `ffc8233f0418a74e6a3b588385521a17b9d8b653`.
3. Existing depth-chart API contract: `api.getTeamRoster()`, `api.getTeamChemistry()`, `api.updateDepthChart()`.
4. Existing React/Motion/R3F/Playwright stack.
5. The named production plate `depth_chart_warboard_1789227219044.jpg` is **MISSING** from the repository at this baseline.

## Proof-Slice Decisions

- Preserve current route and backend contract.
- Do not add a second WebGL canvas for the Depth Chart.
- Add a governed scene manifest and a DOM/CSS 2.5D procedural fallback.
- Suppress global stadium/weather canvases on this indoor scene.
- Respect OS reduced-motion at the application Motion boundary and in pointer parallax.
- Keep an accessible button-based reorder path in addition to pointer dragging.
- Never fabricate missing player attributes in the UI.
- Preserve unsaved per-position ordering when moving between position groups.
- Keep all work on a feature branch until build/E2E evidence is available.

## New Spatial Contract

`SpatialSceneManifest` separates scene identity, render mode, expected storyboard asset, asset status, motion budget, and route-level global effect policy.

Current Scene 05 classification:

- `id`: `SCN-005`
- `renderMode`: `PROCEDURAL_2_5D`
- `storyboardAsset`: `depth_chart_warboard_1789227219044.jpg`
- `assetStatus`: `MISSING`
- `fallback`: `PROCEDURAL_WAR_ROOM`

Promotion to `DEPTH_PLATE` requires the actual production plate plus depth/segmentation assets. Promotion to `TRUE_3D` requires independently verified geometry/model assets.

## Functional Defects Corrected

1. Unsaved reorder state was rebuilt from persisted roster state whenever the user switched positions.
2. Whole-row pointer-down could start a reorder when the user intended to press a dossier/action button.
3. The save E2E test expected an obsolete browser dialog instead of the current accessible status banner.
4. Missing player attributes were displayed using invented defaults.
5. Empty-state copy referenced a non-existent “+ Add Athlete” control.
6. Indoor Depth Chart unnecessarily inherited app-wide stadium/weather rendering.

## Verification Gate

Required before merge:

- `npm run lint`
- `npm run format:check`
- `npm run build`
- `npm run test:e2e -- depth-chart-flow.spec.ts`
- Chromium proof screenshot artifact
- reduced-motion assertion
- unsaved-order persistence regression
- save request payload regression

If CI cannot execute these, status remains `PARTIAL / NOT_RUNTIME_VERIFIED`.

## Remaining Scene Roadmap

### Wave 1 — Shared spatial foundation

- Extend the manifest to all storyboard scenes.
- Add render-tier and device-quality policies.
- Add scene transition graph separate from URL routing.
- Add source/asset provenance fields and fallback semantics.
- Add visual-regression baselines and ARIA snapshots.

### Wave 2 — Highest-value operational rooms

- Locker Room / Roster Hub.
- Football Ops / GM War Room.
- Film Theater / Strategy.
- Medical / Recovery.
- Coach Office / Morale.

### Wave 3 — Gameday continuity

- Arrival.
- Concourse.
- Tunnel Club.
- Field Entrance.
- Missing live-game command scene.
- Halftime.
- Outcome-aware postgame variants.

### Wave 4 — Expensive effects only after interaction proof

- Depth plates and segmentation.
- True 3D props/rooms where justified.
- Rigged characters only for event-driven moments.
- Spatial audio.
- Particles/volumetrics under a performance governor.

## Rollback

Delete the feature branch or revert the commits in this task. No backend schema or canonical data migration is introduced by this slice.

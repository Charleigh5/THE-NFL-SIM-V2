# UI/UX Overhaul Plan (Functionality-Preserving)

Scope: full visual redesign + motion redesign of all user-facing pages/components while preserving route paths, API calls, data models, and Playwright selectors.

Source of truth for routed pages: [`frontend/src/router.tsx`](frontend/src/router.tsx:241)

Runtime/tooling target: Node.js 20 LTS.

Asset usage note: plan assumes internal-dev reference use of official NFL team logos; licensing handled separately.

---

## 1) Current UI baseline (what we must not break)

Frontend stack and constraints:

- Vite + React 19 + React Router v7 + Framer Motion + Three.js + Zustand + React Query (see [`frontend/package.json`](frontend/package.json:1)).
- Global shell: [`frontend/src/layouts/MainLayout.tsx`](frontend/src/layouts/MainLayout.tsx:12)
- Navigation: [`frontend/src/components/Navigation.tsx`](frontend/src/components/Navigation.tsx:5)
- Team color theming already exists via CSS variables animated with Framer Motion: [`frontend/src/context/ThemeContext.tsx`](frontend/src/context/ThemeContext.tsx:26)
- E2E relies on `data-testid` attributes and stable flows; do not remove or rename without aliasing.
  - Example: Trade journey tests: [`frontend/e2e/trade-center.spec.ts`](frontend/e2e/trade-center.spec.ts:58)
  - Example: Dashboard journey tests: [`frontend/e2e/dashboard-flow.spec.ts`](frontend/e2e/dashboard-flow.spec.ts:21)

Pages in scope:

- Routed today: Dashboard, Season Dashboard, Offseason Dashboard, Draft Room, Front Office, Depth Chart, Trade Center, Trophy Room, Training Center, Settings, Team Selection, Not Found.
- Present in repo (include in redesign even if not routed currently): Live Sim, Medical Center, Playbook.
  - See [`frontend/src/pages/LiveSim.tsx`](frontend/src/pages/LiveSim.tsx:15), [`frontend/src/pages/MedicalCenter.tsx`](frontend/src/pages/MedicalCenter.tsx:1), [`frontend/src/pages/Playbook.tsx`](frontend/src/pages/Playbook.tsx:1)

---

## 2) Narrative spine (hyper-immersive and cohesive)

Dominant art direction: cinematic night game.

Single cohesive story across the app:

- Tunnel Entrance: identity + fandom + selection
- War Room: franchise decisions and system control
- Broadcast Studio: season flow, schedule drama, playoff momentum
- Facility: training, playbook craft, medical readiness
- Negotiation Table: trade mind games
- Hall of Champions: trophies, legacy, myth

Every page is a location in the same world; every key UI object is a prop from that location.

---

## 3) Design system (visual)

### 3.1 Materials and lighting

- Materials: wet asphalt, carbon fiber, brushed metal, stitched leather, visor glass.
- Lighting: stadium spotlights, rim-light glow, rain reflections, fog shafts.
- Team colors: used as emissive accents, glow edges, and secondary lights (not flat background fills).

### 3.2 Typography and numerals

- Headlines: condensed athletic / broadcast style.
- Body: clean sans.
- Numerals: tabular/mono for stats and cap.

### 3.3 Iconography

- Replace emoji UI affordances with SVG icon system + team marks.
- Keep lucide icons where already used, but wrap in “broadcast plate” containers and animate with reveals.

### 3.4 Layout grammar

- Avoid generic dashboard grids.
- Prefer cinematic compositions:
  - hero band
  - second band for narrative widgets
  - deep background scene layer
  - foreground “physical” UI objects with tilt and depth

---

## 4) Motion system (Framer Motion)

### 4.1 Motion tokens

Define motion tokens once and reuse:

- Micro: 120–200ms for toggles, focus, hover responses.
- Macro: 280–420ms for panels, drawers, card flips.
- Scene: 700–1200ms for route transitions and major state reveals.

Use spring-based “tactile equipment” motion for draggable objects and major CTAs.

### 4.2 Route transition language

Each route change is a broadcast cut:

- tunnel push-in for Team Selection -> Dashboard
- whip-pan for Dashboard -> War Room features
- rack focus for Season tabs

Implementation: a route transition wrapper around the Outlet in [`frontend/src/layouts/MainLayout.tsx`](frontend/src/layouts/MainLayout.tsx:12) using Framer Motion `AnimatePresence`.

### 4.3 Reduced motion

Respect `prefers-reduced-motion`:

- Keep contrast and composition.
- Reduce displacement and parallax amplitude.
- Keep essential affordance cues.

---

## 5) Immersive interaction toolkit

### 5.1 Parallax scenes

Per page, maintain 3–5 layers:

- background: crowd silhouettes, fog, stadium lighting arcs
- mid: LED ribbons, banners, confetti bursts for key moments
- foreground: interactive UI objects

Implementation: Framer Motion `useScroll` + `useTransform` for y/opacity/blur.

### 5.2 Pointer tilt and spotlight

Core interaction: “physical object under stadium light.”

- Tilt: 3D transform with subtle perspective.
- Spotlight: gradient highlight tracks pointer.
- Shadow: soft shift based on pointer.

Implementation: MotionValues driven by pointer position; clamp for performance.

### 5.3 Kinetic drag

- Trade assets and depth chart items should feel like magnets/placards.
- Add inertia and snap settle (visual only; do not alter logic).

### 5.4 Fan vibe layer

- Ambient crowd energy meter (visual only).
- Stadium ribbon tickers that react to major states.
- Optional confetti for champions and milestone events.

---

## 6) Page-by-page overhaul blueprint

### 6.1 Team Selection (Tunnel Entrance)

Current: basic grid and placeholder logo in [`frontend/src/pages/TeamSelection.tsx`](frontend/src/pages/TeamSelection.tsx:28)

Redesign:

- Full-screen tunnel scene with rain reflections, fog, and spotlight sweep.
- Team cards become locker plaques:
  - stitched SVG border draw on reveal
  - tilt + spotlight
  - team logo + abbreviation lockup
- Selection moment:
  - spotlight intensifies
  - team emissive glow ramps (via ThemeContext variables)
  - subtle “broadcast lower-third” confirmation plate

Keep functionality:

- Keep click selection and navigation behavior.
- Preserve any existing `data-testid` if added.

### 6.2 Dashboard (War Room)

Current: mission control header + engine cards in [`frontend/src/pages/Dashboard.tsx`](frontend/src/pages/Dashboard.tsx:95)

Redesign:

- Replace grids with a central “war table” hero module:
  - engines become orbiting modules with emissive rings
  - quick actions become physical chips sliding out of a console
- Start season becomes a ceremonial lever (animated cover, safety latch).
- System health becomes a live stadium power grid indicator.

Keep functionality:

- Keep `handleStartSeason()` behavior intact.
- Keep existing links and buttons; reskin only.

### 6.3 Season Dashboard (Broadcast Studio)

Current: tabbed dashboard in [`frontend/src/pages/SeasonDashboard.tsx`](frontend/src/pages/SeasonDashboard.tsx:330)

Redesign:

- Tabs become a broadcast switcher row with animated program monitors.
- Schedule becomes a week scrubber ribbon + matchup cards that feel like broadcast slates.
- Playoffs become a stadium-bracket projection:
  - glowing path lines to winners
  - confetti micro-burst on champion state
- Leaders become player spotlight panels with animated stat bars.

Keep functionality:

- Do not change loader contract from [`frontend/src/router.tsx`](frontend/src/router.tsx:254).
- Keep tab semantics and `data-testid` hooks.

### 6.4 Offseason Dashboard (GM Desk)

Current: action cards + widgets in [`frontend/src/pages/OffseasonDashboard.tsx`](frontend/src/pages/OffseasonDashboard.tsx:255)

Redesign:

- Phases become physical artifacts pinned to a wall:
  - contracts folder
  - progression report
  - draft card
  - free agency phone
- Salary cap becomes a ledger meter with tension and constraints.
- Draft results become cinematic reveal plaques for your team.

Keep functionality:

- Preserve calls to `seasonApi.startOffseason`, `simulateProgression`, `simulateDraft`, `simulateFreeAgency`.

### 6.5 Draft Room (Draft Theater)

Current: ticker, board, assistant in [`frontend/src/pages/DraftRoom.tsx`](frontend/src/pages/DraftRoom.tsx:142)

Redesign:

- DraftTicker becomes a true LED ribbon around the viewport.
- DraftBoard becomes a big board with layered scout notes and spotlight focus.
- DraftAssistant becomes an analyst overlay:
  - SVG underline reveals
  - confidence meter animation
- Trade modal becomes a phone call scene with spotlight.

Keep functionality:

- Keep draft pick logic and callbacks.
- Keep trade modal workflow.

### 6.6 Front Office (Locker Room Roster Wall)

Current: roster cards + modal in [`frontend/src/pages/FrontOffice.tsx`](frontend/src/pages/FrontOffice.tsx:34)

Redesign:

- Roster becomes jersey plates on a wall:
  - tilt, shine, stitched edges
  - quick filters as hanging tags (visual only if filters not implemented)
- Player modal becomes a broadcast spotlight with combine stat overlays.

Keep functionality:

- Preserve modal open and close behavior.
- Preserve card click and `data-testid` used in tests.

### 6.7 Depth Chart (Magnetic Whiteboard)

Current: reorder list in [`frontend/src/pages/DepthChart.tsx`](frontend/src/pages/DepthChart.tsx:150)

Redesign:

- Position selector becomes a formation strip.
- Reorder items become magnets with kinetic settle.
- Chemistry becomes a unit-bond visualization overlay.

Keep functionality:

- Preserve reorder semantics and save call.

### 6.8 Trade Center (Negotiation Table)

Current: tabs and negotiator in [`frontend/src/pages/TradeCenterPage.tsx`](frontend/src/pages/TradeCenterPage.tsx:118)

Redesign:

- Tabs become 3 stations around a table:
  - negotiate
  - inbox
  - trade block
- GM response becomes a dramatic decision stamp with animated reasoning note.
- Drag zones look like felt table regions, with spotlight emphasis.

Keep functionality:

- Preserve tab logic and API calls.
- Preserve `data-testid` and flow from Playwright.

### 6.9 Training Center (Practice Facility)

Current: drill catalog + coach blocks in [`frontend/src/pages/TrainingCenter.tsx`](frontend/src/pages/TrainingCenter.tsx:71)

Redesign:

- Drills become physical cones/clipboards with heat overlays.
- Coaching style becomes a scheme wheel.
- Execute becomes a whistle moment and summary reveal (visual only).

Keep functionality:

- Preserve `trainingService` calls.

### 6.10 Trophy Room (Hall of Champions)

Current: 3D scene and minimal overlay in [`frontend/src/pages/TrophyRoom.tsx`](frontend/src/pages/TrophyRoom.tsx:9)

Redesign:

- Expand overlay into museum placards with parallax.
- Add dust motes and spotlight sweeps.
- Optional subtle confetti when champion state exists.

Keep functionality:

- Do not change 3D scene logic; only wrap and style.

### 6.11 Live Sim, Medical Center, Playbook

- Live Sim: add broadcast lower thirds, crowd energy layer, weather scene overlays while preserving existing structure in [`frontend/src/pages/LiveSim.tsx`](frontend/src/pages/LiveSim.tsx:77)
- Medical Center: turn placeholder target into holographic anatomy station while preserving layout in [`frontend/src/pages/MedicalCenter.tsx`](frontend/src/pages/MedicalCenter.tsx:1)
- Playbook: telestrator becomes animated SVG route craft while preserving placeholder structure in [`frontend/src/pages/Playbook.tsx`](frontend/src/pages/Playbook.tsx:1)

---

## 7) Asset pipeline (team logos and SVG)

- Centralize team marks in a small registry: `getTeamMark(abbrev)` and optional `getTeamWordmark(abbrev)`.
- Source location: `frontend/public/logos` already contains some assets.
- Prefer SVG marks when feasible; PNG fallback.
- Normalize sizing and provide a single component wrapper that applies glow, mask reveals, and accessibility labels.

---

## 8) Implementation phases (no functionality changes)

Phase 0: guardrails

- Baseline screenshots for visual regression.
- Confirm Playwright flows and selectors.

Phase 1: foundations

- Introduce design tokens and motion tokens.
- Build shared primitives:
  - TiltCard
  - ParallaxScene
  - RibbonTicker
  - BroadcastPanel
  - SpotlightButton

Phase 2: shell

- Redesign navigation and global layout while preserving routes.

Phase 3: page migrations

- Team Selection -> Dashboard -> Season -> Trade -> Draft -> Offseason -> Depth Chart -> Training -> Trophy.

Phase 4: polish and performance

- Performance budget per page:
  - avoid animating box-shadow
  - use transform and opacity
  - throttle pointer listeners
- Accessibility pass:
  - focus states as part of the aesthetic
  - motion reduction supported

Phase 5: verification

- Run Playwright suite and fix any selector breakage.

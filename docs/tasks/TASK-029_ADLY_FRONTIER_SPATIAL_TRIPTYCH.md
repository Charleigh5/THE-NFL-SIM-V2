<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-029_ADLY_FRONTIER_SPATIAL_TRIPTYCH

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Professional football franchise facilities: player locker room stalls, Dan Campbell's head coach corner office overlooking the Detroit Lions facility, multi-screen analytics war room command centers.
  - Editorial monograph architecture: tactile typography, hard elevation, hairline structural rules, zero generic SaaS boilerplate or soft blur bubbles.
  - The Adly Frontier UI Architect design system: mobile-first, 12-state deterministic interactive matrix, fluid `clamp()` typography scales, domain vector grammars.
- **Related Ideas:**
  - `SpatialSceneViewport`: 2.5D hardware-accelerated multiplane perspective projection with LERP damping ($f = 0.075$).
  - Tri-mode spatial hub controller: `SPATIAL LOCKERS` (Scene 01), `COACH OFFICE` (Scene 04), and `TACTICAL TABLE`.
  - Dual-mode mission control: `SPATIAL COMMAND CENTER` (Scene 07) and `TACTICAL MISSION CONTROL`.
- **Future Potential:**
  - Complete unbroken franchise spatial walkthrough: Arrival hub -> Locker stalls -> Training gym -> Film auditorium -> GM office -> Sideline tablet -> Redzone clash -> Lombardi glory.
- **Constraints:**
  - Strict compliance with `AGENTS.md` (Anti-deception, verification before completion, surgical blast radius, bounded recursion ceiling max depth = 2).
  - Anti-Template Firewall Rules: Rule R1 (0 AI sparkles, domain vectors only), Rule R2 (crisp corner radius $\le 4\text{px}$), Rule R3 (fluid clamp typography), Rule R4/R5 (1px hairline rules, hard elevation).
  - Zero regression on existing Playwright test suites (`front-office.spec.ts` and `dashboard-flow.spec.ts`).
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Render 3D low-polygon models of locker room benches, office furniture, and analytics video monitors inside WebGL canvasses with Drei overlays.

### Powerful Antithesis
- **Performance Drag:** Running three concurrent WebGL canvas instances creates severe GPU thermal throttling and battery drain.
- **Visual Cheapness:** Low-poly 3D models fail to match the grit and authenticity of real architectural photography of Ford Field and the Detroit Lions facility.
- **Accessibility & Hit-Testing Breakdown:** Drei raycasting de-synchronizes from native DOM pointer events, breaking screen readers and Playwright automated tests.

### The Superior Synthesis
- Apply the **Adly Frontier UI Architect** system with **`SpatialSceneViewport`**:
  - Photorealistic Detroit Lions facility scenes projected in multiplane 2.5D with subtle mouse/gyro parallax and safe overscan.
  - Interactive UI sits on an unskewed 2D projection plane with 100% native hit testing, crisp typography, and 12-state interactive feedback.
  - Editorial monograph drafting decks with 1px hairline rules (`border-white/10`) and high-contrast frosted glass panels (`bg-slate-950/75 backdrop-blur-xl`).
  - Zero generic AI sparkles; all icons replaced with domain vectors.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19.2, Vite 7.3, Tailwind CSS 4.1, Framer Motion 12.23.
- **Language:** TypeScript 5.8 (Strict typing, no `any`).
- **Spatial Assets:**
  - Scene 01: `frontend/public/assets/spatial/ford_field_locker_roster_1789187061053.jpg`.
  - Scene 04: `frontend/public/assets/spatial/dan_campbell_office_1789188197446.jpg`.
  - Scene 07: `frontend/public/assets/spatial/team_analytics_warroom_1789227266940.jpg`.

### 2. Front Office Tri-Mode Implementation (`FrontOffice.tsx`)
- Tri-mode spatial switcher:
  - `lockers`: `SpatialSceneViewport` with Ford Field locker stalls. Nameplates stamped with brass/silver styling, OVR badges, and quick dossier triggers.
  - `office`: `SpatialSceneViewport` with Dan Campbell's corner desk. Houses Coach Settings and tactical tendencies.
  - `table`: High-density 2D virtualized roster table for rapid operations.
- Preserve all selectors: `[data-testid="front-office-header"]`, `[data-testid="roster-section"]`, `[data-testid^="player-card-"]`, `[data-testid="player-modal"]`, `[data-testid="player-speed"]`, `[data-testid="player-strength"]`, `[data-testid="close-modal-button"]`.

### 3. Mission Control War Room Implementation (`Dashboard.tsx`)
- Dual-mode switcher:
  - `spatial`: `SpatialSceneViewport` with Detroit Lions multi-screen analytics war room.
  - `tactical`: Direct 2D dashboard.
- Anti-template refinement: replace generic sparkles with domain vectors (`Flame`, `Activity`, `Compass`), apply editorial 1px hairline rules and fluid `clamp()` headers.
- Preserve all selectors: `h1: "Mission Control"`, `p: "War Room overview under the stadium lights."`, `.system-status .badge: "All Systems Online"`, `.start-season-btn`, `.quick-actions-section`, `.quick-action-card`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** `tsc -b && vite build` clean exit (code 0 in 10.23s, 3799 modules transformed).
- [x] **Security:** 3-Gate security pattern verified; 0 secrets, 0 dangerous loader flags.
- [x] **E2E Test Suites:** `front-office.spec.ts` and `dashboard-flow.spec.ts` passing at 100% (24 passed, 3 skipped across Chromium, Firefox, Webkit).
- [x] **Visual Audit:** Captured and verified screenshots via `view_file` (`01_dashboard_overview.png`, `05_front_office.png`, `05b_coach_office.png`).
</final_audit>

---

<baton_handoff>
Next Immediate Step: All 3 scenes verified and captured. Ready for commit and push to remote repository.
</baton_handoff>

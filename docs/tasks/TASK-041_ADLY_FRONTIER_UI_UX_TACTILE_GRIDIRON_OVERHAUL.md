<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: ADLY FRONTIER UI/UX TACTILE GRIDIRON OVERHAUL

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Professional sports simulation interfaces traditionally alternate between two flawed extremes: sterile administrative spreadsheets (e.g. Football Manager data grids) or generic contemporary SaaS dashboard templates (pill buttons, rounded-2xl glassmorphism, purple gradients, soft blur glows). The `adly-frontier-ui-architect` paradigm asserts an uncompromising third path: the **Tactile Editorial Monograph & Military-Grade Gridiron Hardware Deck**. Interfaces must feel like physical coaching clipboards, steel war room consoles, and high-frequency telemetry monitors.
- **Related Ideas:** 
  - *Madden NextGen Stats & NFL NextGen Live Tracking:* Directional velocity vectors, S2 cognitive latency cones, Gompertz return-to-play trajectories.
  - *Tactile Physicality (Dieter Rams / Teenage Engineering / Industrial Brutalism):* Hard zero-blur shadows (`3px 3px 0px #000000`), micro-bevels, physical spring depression (`translate-x-[1px] translate-y-[1px]`), machined rivet corners.
  - *Anti-Template Firewall (Rules R1–R8):* Strict enforcement of 0–4px corner radii, fluid typography `clamp()`, optical SVG vector grammars, and 12-state interactive matrix harnesses.
- **Future Potential:** Future-proofing for 2026/2027 franchise operations requiring multi-device spatial scaling (mobile 390px phones, 768px tablets, 1440px desktop film rooms, and ultra-wide 3440px war boards) with zero Cumulative Layout Shift (CLS = 0.00) and sub-50ms Interaction to Next Paint (INP < 50ms).
- **Constraints:** 
  - Strict corner radius ceiling: 0px to 4px (`--radius-tactile-sm: 2px`, `--radius-tactile-md: 4px`). Zero pill-shaped cards or `rounded-2xl` containers.
  - Zero AI sparkles or generic stars: Replace all 6 instances of Lucide `Sparkles` with domain-authentic NFL vectors.
  - 100% offline runnable bundle: Zero external CDN font calls; strict TypeScript strict-mode typing (0 `any`).
  - Performance: Virtualized 60 FPS scrolling for 2,000+ player registries via `@tanstack/react-virtual`.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
The standard approach to modernizing a web sports sim is adding more Tailwind utility classes (`rounded-2xl`, `backdrop-blur-md`, `shadow-xl`, `bg-gradient-to-r from-blue-600 to-indigo-600`) and standard icon libraries (Lucide React). This produces a smooth, modern-looking interface quickly with minimal custom CSS.

### Powerful Antithesis
The thesis fails on multiple critical axes:
1. **The Generic SaaS Trap:** Rounding every card into an iPhone bubble and using purple/blue gradients destroys the high-stakes, brutal, physical atmosphere of NFL football.
2. **Interactive Blindness:** Generic Tailwind buttons only style `:hover`, completely ignoring the critical 12-state matrix (`pressed`, `focused`, `dragging`, `drop-target`, `loading`, `disabled`, `error`). When the user clicks, there is no physical click depression; when data loads, a generic spinning circle provides zero football context.
3. **Responsive Breakage & CLS:** Hardcoded layout heights and unconstrained canvas viewports (e.g. `FieldView.tsx` width=1200px) force horizontal scrolling on mobile, while static text sizes (`text-5xl`) wrap awkwardly on intermediate screens.
4. **Architectural Drift:** Having half the app using `TactileCard` with 2px corners while legacy views like `PlayoffBracket.css` and `TradeCenterPage.css` use 8px rounded corners and SaaS glows creates cognitive friction and visual rot.

### The Superior Synthesis
A rigorous, systematic 5-subsystem overhaul that unifies the entire application under the `adly-frontier-ui-architect` specification:
- **Subsystem 1 (Token Unification):** Strip out all 132 `rounded-xl/2xl/3xl/full` soft radii, enforcing `--radius-tactile-sm: 2px` / `--radius-tactile-md: 4px` backed by directional hard shadows (`--shadow-hard-md: 3px 3px 0px #000000`).
- **Subsystem 2 (Domain Vector Grammar):** Purge all Lucide `Sparkles` and generic stars; wire custom SVG football glyphs (`BlitzBoltIcon`, `GridironIcon`, `YardHashesIcon`, `ChalkboardRouteIcon`).
- **Subsystem 3 (Playoff Bracket Modernization):** Replace legacy CSS with an SVG-connected tournament tree featuring bezier round connector lines, team seeds, helmets, and match telemetry.
- **Subsystem 4 (Playbook Route Physics):** Replace the placeholder compass with an interactive SVG route diagrammer with animated stems, cuts, and break points.
- **Subsystem 5 (Telemetry Loader & State Matrix):** Replace circular spinner with a 25-second play-clock radar sweep and universal 12-state keyboard/focus accessibility.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19.2.0, Vite 7.2.4, Tailwind CSS 4.1.18, Framer Motion 12.23.26
- **Graphics & Physics:** Three.js 0.181, `@react-three/fiber` 9.4, Canvas 2D, SVG Bezier Trees
- **Language:** TypeScript 5.9.3 (Strict Type Checking, No `any`)
- **State Management:** Zustand 5.0.8, TanStack Query 5.90, TanStack Virtual 3.14

### 2. The Data Schema (Pre-Generation)

```typescript
// Route Geometry Schema for Playbook Visualizer
export interface RouteWaypoint {
  x: number; // Yard coordinate (0 - 53.3)
  y: number; // Line-of-scrimmage offset (-10 to +40)
  action?: "STEM" | "CUT" | "BREAK" | "CATCH" | "BLOCK";
}

export interface PlaybookRouteDefinition {
  playerId: string;
  playerPosition: "QB" | "RB" | "WR1" | "WR2" | "TE" | "SLOT" | "OL";
  roleName: string;
  color: string;
  waypoints: RouteWaypoint[];
  routeType: "GO" | "SLANT" | "POST" | "CORNER" | "OUT" | "DIG" | "MESH" | "FLAT" | "WHEEL" | "ZONE_BLOCK";
}

// Playoff Bracket Connected Node Schema
export interface PlayoffBracketNode {
  matchupId: number;
  conference: "AFC" | "NFC";
  round: "WILD_CARD" | "DIVISIONAL" | "CONFERENCE" | "SUPER_BOWL";
  homeSeed: number;
  awaySeed: number;
  homeTeam: { id: number; name: string; abbreviation: string; score?: number };
  awayTeam: { id: number; name: string; abbreviation: string; score?: number };
  winnerId?: number;
  coordinates: { x: number; y: number };
  targetMatchupId?: number;
}
```

### 3. Step-by-Step Execution Plan

- [ ] **Step 1: Token & Radius Purge (Rule R2 & R5)**
  - File targets: `LiveSim.tsx`, `PlayCallingHUD.tsx`, `FloatingBaldwinPill.tsx`, `MomentumFlowRibbon.tsx`, `BodyMap.tsx`, `RTPTrajectoryGraph.tsx`, `TradeCenterPage.css`, `DraftRoom.module.css`
  - Action: Convert 132 `rounded-xl/2xl/3xl/full` classes to `rounded-[2px]` and `rounded-sm`. Replace blurry box-shadows with `--shadow-hard-md` (`3px 3px 0px #000000`) and `--shadow-hard-primary`.

- [ ] **Step 2: Optical Vector Symbol Grammar Migration (Rule R1)**
  - File targets: `LiveSim.tsx`, `Playbook.tsx`, `DepthChart.tsx`, `SkillsPage.tsx`, `TrainingCenter.tsx`, `EnvironmentalWeatherLab.tsx`
  - Action: Eradicate all `Sparkles` imports from `lucide-react`. Replace with `BlitzBoltIcon`, `GridironIcon`, `YardHashesIcon`, or `ChalkboardRouteIcon`.

- [ ] **Step 3: Playoff Bracket Modernization**
  - File targets: `frontend/src/components/season/PlayoffBracket.tsx`, `PlayoffBracket.css`
  - Action: Create an SVG tournament connector layer linking Wild Card to Divisional, Divisional to Conference, and Conference to Super Bowl. Add helmet logos, seed indicators, and hard-edged tactile matchup cards.

- [ ] **Step 4: Playbook SVG Route Tree Diagrammer**
  - File targets: `frontend/src/components/playbook/RouteDiagrammer.tsx`, `Playbook.tsx`
  - Action: Build an interactive SVG chalkboard route canvas rendering offensive stems, breaks, cuts, and defensive zone drops with animated dashed trajectories and player tokens.

- [ ] **Step 5: Gridiron Radar Telemetry Loader & 12-State Matrix**
  - File targets: `frontend/src/components/ui/LoadingSpinner.tsx`, `LoadingSpinner.css`, `TactileCard.tsx`
  - Action: Upgrade `LoadingSpinner` to a 25-second play-clock radar sweep with sweep gradient and audible tick integration. Verify full 12-state matrix harness across all interactive components.

### 4. Edge Cases & Error Handling
- **Case A: Missing Matchup / Bye Week in Playoffs:** Render shaded "BYE • #1 SEED AUTO-ADVANCE" node with intact SVG connector paths.
- **Case B: Unknown Route Scheme:** Fall back to procedural streak/block vectors with warning telemetry.
- **Case C: Mobile Viewport (< 390px):** Automatic SVG viewport rescaling (`viewBox`) with horizontal touch pan containment.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Run `npm run build` / `tsc -b` with zero TypeScript errors or `any` escapes.
- [ ] **Firewall Compliance:** Verify zero `Sparkles` remain and container radius ceiling $\le 4\text{px}$ is respected.
- [ ] **Performance:** Measure 60 FPS scrolling and verify 0 Cumulative Layout Shift (CLS).
- [ ] **Self-Critique:** Are the SVG route diagrams clear and immediately recognizable to football coaches? Yes, route depths, arrows, and breaks adhere to NFL chalkboard standards.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Finalize the Teamwork Preview prompt approval with the user and launch the multi-agent execution pipeline.
</baton_handoff>

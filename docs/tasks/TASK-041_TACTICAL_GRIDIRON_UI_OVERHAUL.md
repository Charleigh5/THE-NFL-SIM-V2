<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-041_TACTICAL_GRIDIRON_UI_OVERHAUL

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** The project aims to be the "Dwarf Fortress of football simulations" — a true digital gridiron. Soft generic SaaS templates, blurry neon glows, rounded pill buttons, and generic 4-point AI sparkles dilute the visceral, tactical feel of a high-stakes NFL war room. The anti-template firewall token enforcement establishes an uncompromising tactile identity.
- **Related Ideas:** Tactical military telemetric HUDs, retro-modern aerospace telemetry, Bloomberg terminals, and classic chalkboard playbooks. Zero-blur directional hard drop shadows (`3px 3px 0px #000000`), micro-bevel tactile corners (0-4px), and SVG vector graphics that trace genuine football concepts.
- **Future Potential:** Modular SVG components (`PlayoffBracket`, `RouteDiagrammer`, `LoadingSpinner`) provide scalable, vector-sharp graphics at any DPI, completely independent of brittle third-party chart libraries or CSS layout shifts.
- **Constraints:** 
  - Strict 0-4px corner radius ceiling across all layout viewports, modals, and HUD cards (purge `rounded-xl`, `rounded-2xl`, `rounded-3xl`, and pill `rounded-full`).
  - Strict 0-blur hard shadows (`--shadow-hard-md: 3px 3px 0px #000000`, `--shadow-hard-primary`, `--shadow-hard-pressed: 1px 1px 0px #000000`).
  - Zero imports/usages of `Sparkles` from `lucide-react` across `frontend/src`.
  - Zero Cumulative Layout Shift (CLS = 0) in `PlayoffBracket.tsx`.
  - TypeScript build (`npm run build`) succeeds with zero errors, bundle entry chunk < 450 kB.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Rely on standard CSS border-radius and external icon packs to quickly adjust cards and swap icons. Use simple flexboxes for tournament brackets and playbooks.

### Powerful Antithesis
A superficial search-and-replace will miss subtle pill classes, cause layout reflows when tournament rounds advance, break route chalkboard responsiveness on various viewports, and fail strict type audits. An uncoordinated multi-file edit can cause severe git merge conflicts and TypeScript build failures.

### The Superior Synthesis
Execute a decoupled, phased milestone architecture:
1. **Milestone 1:** Anti-Template Firewall & Vector Symbol Migration (purging all radius violations and replacing `Sparkles` across all 17 files with authentic vector icons).
2. **Milestone 2:** Deterministic 15-Slot Connected SVG Playoff Tournament Bracket (guaranteeing CLS = 0 with SVG cubic bezier connector splines and retiring legacy CSS).
3. **Milestone 3:** Interactive SVG Playbook Route Tree Diagrammer (dynamic vector passing stems, route breaks, cuts, and coverage drops for Go, Slant, Mesh, Dig, Zone).
4. **Milestone 4:** Digital Gridiron 25-Second Play-Clock Radar Sweep Loader & 12-State Interactive Matrix.
5. **Milestone 5:** Verification Gate, TypeScript compilation, Lint check, and Forensic Audit.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19, Tailwind CSS v4.1.18, Vite 6, TypeScript 5.8
- **Language:** Strict TypeScript (zero `any` types allowed)
- **State Management:** React local state, Zustand stores, SVG DOM attributes

### 2. The Data Schema (Pre-Generation)
- `PlayoffMatchup`: `id`, `round`, `conference`, `home_team`, `away_team`, `home_score`, `away_score`, `winner_id`, `status`
- `FootballRoute`: `player: string`, `route: string`, `stem: [number, number][]`, `breakPoint: [number, number]`, `cut: [number, number]`, `color: string`
- `TactileState`: `idle` | `hover` | `pressed` | `focused` | `dragging` | `drop-target` | `selected` | `disabled` | `loading` | `success` | `warning` | `error`

### 3. Step-by-Step Execution
- [ ] **Step 1: M1 - Anti-Template Firewall & Symbol Migration.** Purge `rounded-xl/2xl/3xl` and `Sparkles` from `frontend/src`.
- [ ] **Step 2: M2 - Connected SVG Playoff Bracket.** Modernize `PlayoffBracket.tsx` and delete `PlayoffBracket.css`.
- [ ] **Step 3: M3 - Interactive Playbook Route Diagrammer.** Create `RouteDiagrammer.tsx` and mount into `Playbook.tsx`.
- [ ] **Step 4: M4 - Gridiron Telemetry Loader & 12-State Matrix.** Upgrade `LoadingSpinner.tsx` and refine interactive matrix.
- [ ] **Step 5: M5 - Full Verification & Build Gate.** Pass `npm run build` and `npm run lint`.

### 4. Edge Cases & Error Handling
- [Case A: Bye Week in Playoff Bracket] -> Dedicated Seed 1 Bye visual badge, no generic TBD opponent.
- [Case B: Playoff Rounds Unplayed] -> Ghost cards rendered with dotted bezier connectors, maintaining exact grid dimensions.
- [Case C: Missing Route Coordinates] -> Default stem-and-break generator based on play concept name.
- [Case D: Narrow Viewports on Loader] -> Strict `max-w-full overflow-hidden` wrapper preventing horizontal scrollbars.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Strict `npm run build` (`tsc -b && vite build`) exit code 0.
- [ ] **Radius Ceiling:** Zero instances of `rounded-xl`, `rounded-2xl`, `rounded-3xl` in core layout viewports, modals, and HUD cards.
- [ ] **Symbol Grammar:** Zero imports/usages of `Sparkles` from `lucide-react` in `frontend/src`.
- [ ] **Bracket SVG:** Fully connected bezier splines, seeds, helmets, zero layout shift.
- [ ] **Playbook Diagrammer:** Dynamic route vectors for Go, Slant, Mesh, Dig, Zone.
- [ ] **Loader Telemetry:** 25s play-clock radar sweep with zero overflow.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Dispatch Worker for Milestone 1 (Anti-Template Firewall & Vector Symbol Migration).
</baton_handoff>

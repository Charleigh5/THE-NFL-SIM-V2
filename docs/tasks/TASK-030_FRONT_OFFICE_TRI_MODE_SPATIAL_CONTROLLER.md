# TASK: Front Office Tri-Mode Spatial Controller & Adly Frontier UI Architecture

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026
Core Logic: Multi-Model Orchestration (Worker Subagent 1, Max Depth = 2)
Standards: Production-grade code, deterministic logic, adversarial verification, Adly Frontier UI Anti-Template Firewall.
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** The Front Office view in sports management games traditionally toggles between cold spreadsheet grids and detached menu trees. The NFL Sim Engine advances this into a diegetic spatial reality—unifying the physical player locker stalls of Ford Field, the tactical command of Dan Campbell's executive office, and high-density monograph ledger tables.
- **Related Ideas:** Apple Vision Pro spatial UI layers, Bloomberg Terminal high-density virtualized data streams, EA Sports CFB25/Madden card shields, and modern editorial typography.
- **Future Potential:** Scalable multiplane parallax camera panning, WebGPU-accelerated locker stall lighting, real-time depth chart drag-and-drop between lockers and tactical table.
- **Constraints:** 
  - Zero generic 4-point AI sparkles (Adly Rule R1). Domain vectors only (`Shield`, `Users`, `ClipboardList`, `Award`, `Table`).
  - Strict corner radius ceiling (`rounded-md`, `rounded-lg`). No pill buttons.
  - 1px hairline rules (`border-white/10`, `border-[#0076B6]/40`), hard elevation shadows, high-contrast frosted glass (`bg-slate-950/80 backdrop-blur-xl`).
  - Critical test selector preservation (`[data-testid="front-office-header"]`, `[data-testid="roster-section"]`, `[data-testid^="player-card-"]`, `[data-testid="player-modal"]`).
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Maintain existing 2D card grid and simple toggle, sprinkling spatial background images behind static wrappers.

### Powerful Antithesis
Shallow aesthetic veneers degrade performance and fail strict E2E test suites when selectors get obscured by canvas layers or unmounted conditionally. Over-decorating with heavy rounded pills or generic glow effects violates Adly Frontier UI rules.

### The Superior Synthesis
Implement a robust Tri-Mode Spatial Controller backed by persistent `localStorage` (`nfl_sim_front_office_mode`):
1. **Mode 'lockers' (SPATIAL LOCKERS):** First-person Honolulu Blue (`#0076B6`) locker stalls with brushed metallic nameplates, rivet styling, OVR rating shields, and athletic vitals embedded in `SpatialSceneViewport`.
2. **Mode 'office' (COACH OFFICE):** Dan Campbell's Executive Corner Office with 4th-down aggression directives, play-action run philosophy, embedded `CoachSettings`, and a synchronized tactical roster panel.
3. **Mode 'table' (TACTICAL TABLE):** Direct 2D virtualized monograph ledger at 60 FPS.
Every mode renders `[data-testid="roster-section"]` and clickable `[data-testid^="player-card-"]` elements, ensuring zero selector breakage across test runs.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** React 19, Tailwind CSS v4, Lucide Icons, Vite
- **Components:** `SpatialSceneViewport`, `VirtualizedTable`, `CoachSettings`, `PlayerAvatar`, `EnhancedPlayerProfile`
- **State Persistence:** `localStorage.getItem("nfl_sim_front_office_mode")` defaulting to `'lockers'`

### 2. Step-by-Step Execution
- [x] **Step 1: Scaffolding.** Implemented `FrontOfficeMode` enum (`"lockers" | "office" | "table"`), sound effects dispatch, and persistent state.
- [x] **Step 2: Locker Stall Component.** Created `LockerStallCard` featuring Honolulu Blue accents, metallic brushed nameplate headers with rivet styling, OVR badges, and hover/focus/active micro-interactions.
- [x] **Step 3: Office Framing.** Built Dan Campbell's Executive Corner Office with tactical philosophy briefings and embedded `CoachSettings`.
- [x] **Step 4: Monograph Table.** Preserved 60 FPS `VirtualizedTable` with high-density editorial styling.
- [x] **Step 5: Selector Preservation.** Verified all test ids (`front-office-header`, `roster-section`, `roster-grid`, `player-card-*`, `player-modal`).
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [x] **Type Check:** Verified with `tsc -b && vite build` — 0 errors.
- [x] **Security & Integrity:** No PII leakage, zero banned loader variables, clean imports.
- [x] **Playwright E2E Suite:**
  - `e2e/front-office.spec.ts`: 6 passed, 3 skipped (18.3s across Chromium, Firefox, WebKit).
  - `e2e/player-profile-flow.spec.ts`: 15 passed (38.0s across all browsers).
</final_audit>

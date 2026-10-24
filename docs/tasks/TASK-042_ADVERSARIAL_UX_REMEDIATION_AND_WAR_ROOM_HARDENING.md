<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-042 ADVERSARIAL UX REMEDIATION AND WAR ROOM HARDENING

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  Early sports franchise management simulations (e.g., *Front Office Football*, *Out of the Park Baseball*, and *Madden Head Coach 09*) established the "desk simulator" genre—prioritizing dense tabular telemetry over human ergonomics. As modern web applications transitioned into reactive 3D spatial environments (React Three Fiber, 2.5D CSS parallax, and glassmorphic HUDs), visual embellishments frequently outpaced fundamental tactical usability. When veteran defensive coordinators ("Coach Hank Kowalski") evaluate game management software under high pressure (stadium booths, small laptop displays, tight play clocks), unbuffered modal stacks, micro-font contrast failures, and Wall Street financial acronyms introduce severe operational friction.

- **Related Ideas:**
  1. **W3C WAI-APG Modal Dialog Stack Pattern**: Managing a disciplined LIFO (Last-In-First-Out) dialog stack where only the top-most layer traps focus and captures the `Escape` key (`event.stopPropagation()`), preventing background dismissals.
  2. **WCAG 2.1 AA & Section 508 Contrast Standards**: Ensuring all non-decorative text meets a minimum 4.5:1 contrast ratio against dark backgrounds (`#121212`, `#18181b`), utilizing high-luminance tokens (`zinc-200`, `zinc-300`) and tabular numeral kerning (`font-mono tabular-nums`).
  3. **Progressive Disclosure (Nielsen Norman Group)**: Breaking high-density player biometrics (24+ ratings) into "Primary Positional Keys" (prominent primary cards) and an expandable "Full Athletic & Skill Breakdown" accordion.
  4. **Fitts's Law & Hitbox Physics**: Preserving touch/pointer drop zones (`min-h-[72px]`) on dynamic drag-and-drop slots in `@dnd-kit` and Framer Motion even on compact vertical viewports (<800px).

- **Future Potential:**
  Future franchise iterations (2026/2027) will support multi-touch tablet war boards in coach's boxes, live tablet sideline syncing, and audio-driven audible hotkeys. Hardening the UI architecture into an accessible, high-contrast, keyboard-navigable operational console establishes a rock-solid foundation for future tablet PWA and touch-surface deployments.

- **Constraints:**
  - **Zero Regression Invariant**: 578 backend unit/integration tests and 21 existing Playwright E2E tests must maintain 100% pass rates.
  - **No `any` Types**: Strict TypeScript 5.9 typings across all store hooks, modal stack interfaces, and component props.
  - **WCAG 2.1 AA Compliance**: Strict minimum contrast ratio of 4.5:1 for all analytical table data, legends, and column headers.
  - **Zero Bundle Bloat**: Zero unnecessary third-party packages; leverage existing Tailwind v4, Zustand v5, Lucide React, and Framer Motion v12.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
The "standard" solution approach is to address each of Coach Hank's 10 complaints in isolation: add a local `event.stopPropagation()` on individual modal components, sprinkle higher contrast hex codes directly into `StandingsTable.css`, hardcode expanded labels into `TradeAnalyzer.tsx`, and add a couple of conditional classes to depth chart cards.

### Powerful Antithesis
Addressing these issues through localized, ad-hoc patches will rapidly degrade architectural integrity:
1. **Modal Event Leakage**: Adding ad-hoc `stopPropagation` to individual modal components fails when third-party components (e.g. Radix dialogs or child overlays) attach their own `keydown` listeners to `window`. When multiple modals mount concurrently, race conditions determine which unmounts first, corrupting focus and returning users to arbitrary parent screens.
2. **CSS Token Drift**: Manually tweaking hex colors in individual CSS files (`#aaa` to `#ddd`) creates visual inconsistency across the 13 core views and breaks dark-theme token contracts.
3. **Information Density Regress**: Over-simplifying attribute displays by permanently deleting secondary attributes deprives analytical users (capologists, scouts) of critical scouting depth, while keeping all 24 attributes visible overwhelms tactical coaches.
4. **Hitbox Clamping Bugs**: Simply applying fixed CSS heights to depth chart cards causes layout overflow on mobile and iPad viewports without resolving drop-target intersection physics in `@dnd-kit` / Framer Motion.

### The Superior Synthesis
We architect a unified, production-grade 4-Stage Tactical Hardening System:
1. **Global Modal Stack Coordinator (`useModalStackStore`)**: A lightweight Zustand-based stack registry that registers every modal mounted in the application. Only the top-most modal (`stack[stack.length - 1]`) is designated `isTop: true`, captures `Escape`, and traps focus. Subordinate modals become inert (`aria-hidden={!isTop}`, `pointer-events-none`), guaranteeing deterministic single-layer dismissals and perfect focus restoration.
2. **Design Token Accessibility Unification**: Centralize high-contrast WCAG AA tokens (`--text-table-header: #e4e4e7`, `--text-table-body: #f4f4f5`, `--text-table-muted: #d4d4d8`) into shared CSS variables, and apply `tabular-nums font-mono` to all statistical columns.
3. **Progressive Disclosure Architecture**: Implement a two-tiered attribute presentation:
   - **Tier 1 (Core Tactical Keys)**: 4 position-critical attributes rendered in bold, high-contrast badges (e.g., CB -> Speed, Coverage, Press, Agility).
   - **Tier 2 (Full Athletic Breakdown)**: An accessible, animated disclosure accordion (`AnimatePresence`) for secondary traits.
4. **Accessible Micro-Tooltips & Natural Language Translation**: Replace financial jargon (`TNI`, `EV Decay`, `TVP`) with human-readable labels (`Team Need Fit`, `Draft Capital Drift`, `Trade Value Pts`), supported by an accessible, keyboard-focusable `<AccessibleTooltip>` wrapper.
5. **Spatial War Room Hardening**:
   - Enforce `min-h-[72px]` touch boundaries on depth slots with active drop-target glow indicators (`ring-2 ring-emerald-400`).
   - Add dynamic vacancy alerts (`count < targetCount` renders an amber alert ring).
   - Implement global keyboard hotkeys (`1-4` for master unit tabs: Offense, Defense, Special Teams, Specialists).
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frontend Stack:** React 19.2.0, Vite 7.2.4, TypeScript 5.9.3, Tailwind CSS v4.1.18.
- **Animation & Spatial:** Framer Motion 12.23.26, CSS 2.5D perspective transforms.
- **State Management:** Zustand 5.0.8 (Modal Stack & Tactical Settings), TanStack React Query 5.90.10.
- **Icons & Ergonomics:** Lucide React 0.554.0.
- **Testing:** Playwright 1.57.0 (Cross-browser Chromium, Firefox, WebKit), Pytest 8.x.

---

### 2. The Data Schema & Interfaces (Pre-Generation)

#### A. Modal Stack Registry (`frontend/src/store/useModalStackStore.ts`)
```typescript
export interface ModalInstance {
  id: string;
  depth: number;
  triggerElement: HTMLElement | null;
  onDismiss: () => void;
}

export interface ModalStackState {
  stack: ModalInstance[];
  pushModal: (id: string, onDismiss: () => void, triggerElement?: HTMLElement | null) => void;
  popModal: (id?: string) => void;
  isTopModal: (id: string) => boolean;
  clearStack: () => void;
}
```

#### B. Depth Chart Tactical & Scheme Metadata (`frontend/src/types/depthTactics.ts`)
```typescript
export interface SchemeFitMetadata {
  overallFitScore: number; // 0 - 100
  primaryScheme: string; // "Cover 3 Zone", "Man Press Heavy", "Wide Zone", "Air Raid"
  fitTier: "ELITE_FIT" | "SCHEME_COMPATIBLE" | "SCHEME_MISMATCH";
  tacticalNotes: string[];
}

export interface RosterCapSummary {
  activeCount: number;
  maxActiveLimit: number; // 46 for gameday active
  totalRosterCount: number; // 53 for active roster
  practiceSquadCount: number; // 16
  capSpaceUsd: number;
}
```

---

### 3. Step-by-Step Execution Roadmap

#### 🚀 STAGE 1: Critical Interaction & Modal Stack Hierarchy (Tickets 1 & 4)
*Goal: Eliminate multi-modal escape bubbling, trapped navigation, and collapsed drag-drop hitboxes.*

- [ ] **Step 1.1: Implement Global Modal Stack Store.**
  - Path: `frontend/src/store/useModalStackStore.ts`
  - Logic: Maintain reactive LIFO modal stack. Ensure only the head of the stack handles `Escape`. Capture and restore focus to `triggerElement` on pop.
- [ ] **Step 1.2: Create `<ModalShell>` Accessible Wrapper.**
  - Path: `frontend/src/components/ui/ModalShell.tsx`
  - Logic: Encapsulate focus trapping, W3C APG dialog roles (`role="dialog"`, `aria-modal="true"`), backdrop portal mounting, and `isTop` listener gating.
- [ ] **Step 1.3: Refactor Existing Modals to use `<ModalShell>`.**
  - Paths:
    - [`frontend/src/components/ui/PlayerModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/PlayerModal.tsx)
    - [`frontend/src/components/player/PlayerBackstoryModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/player/PlayerBackstoryModal.tsx)
    - [`frontend/src/components/medical/OrthopedicTriageModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/medical/OrthopedicTriageModal.tsx)
    - [`frontend/src/components/capology/CapLedgerAuditModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/capology/CapLedgerAuditModal.tsx)
- [ ] **Step 1.4: Harden Depth Chart Hitboxes & Drop Zones.**
  - Path: [`frontend/src/pages/DepthChartSpatial.css`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChartSpatial.css) & [`frontend/src/pages/DepthChart.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChart.tsx)
  - Logic: Enforce `min-h-[72px]` on all player magnet cards. Add active dragging state `.depth-drop-active` with `ring-2 ring-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.3)]` for unambiguous drop targets.

---

#### 🎨 STAGE 2: Accessibility, Typography & Trade Ergonomics (Tickets 2, 3 & 7)
*Goal: Ensure WCAG AA 4.5:1 contrast, eliminate cryptic acronyms, and enable instant conference filtering.*

- [ ] **Step 2.1: Elevate Standings & Stat Table Color Tokens.**
  - Paths:
    - [`frontend/src/components/season/StandingsTable.css`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/season/StandingsTable.css)
    - [`frontend/src/components/season/StandingsTable.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/season/StandingsTable.tsx)
  - Logic:
    - Replace `.standings-table th { color: #aaa; }` with `color: #e4e4e7` (zinc-200, 7.8:1 contrast).
    - Replace `.standings-legend { color: #888; }` with `color: #d4d4d8` (zinc-300).
    - Add `font-mono tabular-nums` to all record, PCT, and point differential cells.
- [ ] **Step 2.2: Add Standings Conference & Playoff Segmented Controls.**
  - Path: [`frontend/src/components/season/StandingsTable.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/season/StandingsTable.tsx)
  - Logic: Add segmented control buttons `[ALL | AFC | NFC | PLAYOFF PICTURE]` allowing instant one-click switching without dropdown menus.
- [ ] **Step 2.3: Humanize Trade Analyzer Metrics & Add Accessible Tooltips.**
  - Paths:
    - `frontend/src/components/ui/AccessibleTooltip.tsx`
    - [`frontend/src/components/trades/TradeAnalyzer.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/trades/TradeAnalyzer.tsx)
    - [`frontend/src/components/trades/TradeAnalyzer.css`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/trades/TradeAnalyzer.css)
  - Logic:
    - Fix corrupted unicode icon `dY'` -> clean Lucide icon `<FileText className="w-4 h-4 text-cyan-400" />`.
    - Change `TNI` to `Team Need Fit`, `EV Decay` to `Draft Value Drift`, `TVP` to `Trade Value Points`.
    - Attach `<AccessibleTooltip text="...">` explaining GM decision formula inputs.

---

#### 🏈 STAGE 3: Tactical Information Architecture & Progressive Disclosure (Tickets 5, 6, 8 & 10)
*Goal: Declutter attribute grids, add missing backup vacancy warnings, and show gameday active caps.*

- [ ] **Step 3.1: Progressive Disclosure Player Attributes Grid.**
  - Path: [`frontend/src/components/ui/PlayerModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/PlayerModal.tsx)
  - Logic:
    - Group attributes by position taxonomy: display top 4 "Key Positional Attributes" in large hero metric cards (`text-2xl font-black font-heading text-cyan-300`).
    - Move secondary athletic traits into an animated collapsible disclosure panel: `<details className="group">...<summary>View Complete 24-Trait Athletic Profile</summary></details>`.
- [ ] **Step 3.2: Positional Tab Underfilled Alert Badges.**
  - Path: [`frontend/src/pages/DepthChart.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChart.tsx)
  - Logic:
    - Compare `count` against `pos.targetCount`.
    - If `count < pos.targetCount`, render an amber warning pill: `border border-amber-500/50 bg-amber-500/10 text-amber-300` with an alert indicator icon.
- [ ] **Step 3.3: Scheme Fit Affinity Tagging.**
  - Paths:
    - [`frontend/src/components/ui/PlayerModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/PlayerModal.tsx)
    - `frontend/src/utils/schemeFit.ts`
  - Logic: Compute player scheme affinity percentage based on coordinator playbook style and render a concise chip (e.g. `Scheme Fit: 94% (Cover 3 Zone)`).
- [ ] **Step 3.4: Sticky Roster Limit & Active Gameday Cap Bar.**
  - Path: [`frontend/src/pages/DepthChart.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChart.tsx)
  - Logic: Implement a sticky HUD banner: `ACTIVE: 46/46 | INACTIVE: 7/7 | TOTAL: 53/53 | CAP ROOM: $18.4M`.

---

#### ⚡ STAGE 4: Pro-Coach Hotkeys & End-to-End Adversarial Verification (Ticket 9)
*Goal: Provide fast keyboard navigation and prove all 10 tickets pass in automated browser tests.*

- [ ] **Step 4.1: Depth Chart Master Unit Keyboard Navigation.**
  - Path: [`frontend/src/pages/DepthChart.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChart.tsx)
  - Logic:
    - Listen for `1` (Offense), `2` (Defense), `3` (Special Teams), `4` (Specialists) when no text input or modal is active.
    - Add visible `<kbd className="text-[10px] bg-white/10 px-1.5 py-0.5 rounded font-mono">1</kbd>` badges to unit tabs.
- [ ] **Step 4.2: Comprehensive Playwright Adversarial E2E Verification Suite.**
  - Path: `frontend/e2e/ux-remediation-gauntlet.spec.ts`
  - Assertions:
    1. Open nested modal -> press `Escape` -> verify only nested modal closes, parent modal remains open.
    2. Check contrast of table header text on Standings table meets minimum 4.5:1 ratio.
    3. Verify Trade Analyzer displays natural labels and tooltips on hover.
    4. Verify Depth Chart drop slots have minimum height >= 72px.
    5. Verify player attribute accordion toggle functions properly.
    6. Verify underfilled position tab displays amber alert badge.
    7. Verify Standings segmented control filters teams instantly.
    8. Verify Scheme Fit badge renders on player modal.
    9. Verify pressing `2` switches depth chart to Defense unit.
    10. Verify sticky roster active gameday cap bar is visible and formatted.
- [ ] **Step 4.3: Full Regression Test Execution.**
  - Backend unit tests (`pytest backend/tests/unit -q`).
  - Frontend TypeScript build (`tsc -b && vite build`).
  - Playwright E2E suite (`npx playwright test e2e/ux-remediation-gauntlet.spec.ts`).

---

### 4. Edge Cases & Error Handling
- **Case A: Rapid Multi-Modal Mounting** -> Zustand stack deduplicates by modal `id`. If a modal is mounted twice by duplicate clicks, the existing instance is focused rather than stacked.
- **Case B: Mobile / Small Viewport Overflow** -> Tables retain horizontal touch scrolling (`overflow-x-auto`) with sticky team name columns, ensuring numbers never clip.
- **Case C: Keyboard Conflict in Text Inputs** -> Hotkey listener ignores keystrokes when `document.activeElement` is `INPUT`, `TEXTAREA`, or `SELECT`.
- **Case D: Unfilled Positions on Save** -> If depth chart has underfilled mandatory slots, display a gentle warning confirmation dialog: *"2 required CB slots are currently vacant. Save anyway?"*

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Zero `any` types. Strict prop types and return types across all stores, hooks, and components.
- [ ] **Security:** All modal content, tooltips, and table statistics sanitized. No dynamic `dangerouslySetInnerHTML`.
- [ ] **Accessibility:** Full W3C WAI-APG compliance for modal focus trapping, WCAG 2.1 AA 4.5:1 contrast, and screen reader labels (`aria-pressed`, `aria-expanded`).
- [ ] **Performance:** Minimal re-renders via Zustand selectors; zero canvas layout thrashing during drag interactions; bundle size impact < 10 kB.
- [ ] **Self-Critique:** Does this satisfy Coach Hank without breaking the depth required by GM analytics? *Yes: high-level tactical clarity is front-and-center, while deep analytics remain one click away via progressive disclosure.*
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to Step 1.1 of Stage 1—implement the global modal stack store (`frontend/src/store/useModalStackStore.ts`) and create the accessible `<ModalShell>` wrapper to resolve Ticket 1.
</baton_handoff>

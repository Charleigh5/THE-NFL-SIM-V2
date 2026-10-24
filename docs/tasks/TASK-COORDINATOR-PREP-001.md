<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-COORDINATOR-PREP-001 (Coordinator Game-Week Prep & Laminated Call-Sheet Overhaul)

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - **Bill Walsh & Mike Shanahan ("The Opening 15"):** Scripting the first 12–15 offensive plays of the game to probe defensive reactions (personnel matching, motion adjustments, safety rotation) before situational play-calling begins.
  - **Brian Billick & Denny Green (Laminated Situational Call-Sheets):** Color-coded laminated matrices organized by down-and-distance and field zone (`1st & 10 Base`, `3rd & Med/Long "Money Down"`, `Red Zone / Low Red`, `2-Minute / 4-Minute`).
  - **Bill Belichick ("Erase Threat #1"):** Identifying the single opposing "Game-Wrecker" (e.g., an elite WR1, RB1, or EDGE rusher) and committing structural double-teams, bracket coverage, or chip protection at the calculated expense of leaving secondary threats in 1-on-1 matchups.
  - **NFL Coordinator Weekly Micro-Cycle:** Real NFL coordinators do not look at a generic "Season Progress %" bar. Their week flows chronologically: **Mon/Tue** (Self-Scout & Opponent Tape) $\rightarrow$ **Wed** (1st/2nd Down Base Install) $\rightarrow$ **Thu** (3rd Down & Blitz Protection) $\rightarrow$ **Fri** (Red Zone, Goal Line & 2-Minute) $\rightarrow$ **Sat** (Opening 15-Play Script Lock) $\rightarrow$ **Sun** (Kickoff).
- **Related Ideas:**
  - Existing `THE-NFL-SIM-V2` coaching and tactical primitives:
    - [`GameplanDashboard.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/coaching/GameplanDashboard.tsx) & `POST /api/gameplan/install` (`{ team_id, season_id, week, opponent_id, strategy: { offense, defense } }`).
    - [`Playbook.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/Playbook.tsx) (`PLAYBOOK_LIBRARY` plays with tags, win-rate vs. Cover-1/Cover-2/Cover-3/Blitz, and Explosive/EPA ratings).
    - [`narrator_facts_service.py`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/backend/app/services/narrator_facts_service.py) & [`NarratorBar.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/audio/NarratorBar.tsx) (Contextual "SportsCenter" Narrator).
- **Future Potential:**
  - Seamless handoff into `LiveSim.tsx`: Locking the coordinator call-sheet on `/season` pre-populates the opening drive play-caller suggestions and grants situational simulation modifiers during `Simulate Week`.
  - Contextual Narrator enrichment: The SportsCenter anchor reads the user's locked gameplan and opponent matchup ("Turning to Week 3 at Ford Field, the Lions' offensive staff is installing heavy Play-Action to attack Atlanta's single-high Cover-3...").
- **Constraints:**
  - **Zero Additional Page-Load Latency:** Must reuse the consolidated `seasonDashboardLoader` payload (`season`, `summary`, `standings`, `games`, `teams`) cached in `season_cache.py` (`TASK-PERF-001`) so `/season` P95 load latency stays `< 25ms`.
  - **Progressive Disclosure / Fast-Sim Ergonomics:** Users who want to rapidly simulate weeks in Dynasty Mode must be able to click **Auto-Install Coordinator Script** or **Simulate Week** in 1 click without mandatory multi-step friction.
  - **Strict Type Safety:** Zero `any` types in TypeScript (`npm --prefix frontend run build` & `lint`) and strict Pydantic/Mypy compliance on the backend.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Replace the passive 4-box macro counter strip in [`SeasonSummaryCard.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/season/SeasonSummaryCard.tsx) (`Games Played`, `Remaining`, `Total Weeks`, `Season Progress`) with one of the 5 visual Coordinator Prep concepts:
1. **Concept 1 (Monday–Sunday Coordinator Install Pipeline):** Chronological 6-stage weekly install stepper + 3-column tactical board.
2. **Concept 2 (Laminated 4-Quadrant Situational Call-Sheet):** Color-coded 2x2 situational matrix (`1st & 10`, `3rd & Med/Long`, `Red Zone`, `2-Minute`) + Opening-15 script sidebar.
3. **Concept 3 (NextGen Telemetry & Tendency War Room):** Opponent scheme tendency bars + counter-package selector with live win-probability delta.
4. **Concept 4 (Belichick Game-Wrecker & Matchup Chessboard):** Threat #1 bracket/erase card + OL/DL trench protection slide + injury mismatch exploits.
5. **Concept 5 (Primetime Broadcast "Keys to the Game" Desk):** Network television matchup hero card + 3 interactive Coordinator Keys to Victory.

### Powerful Antithesis

- **UX Bloating & Click-Fatigue Risk:** If a user simulating a 18-week season is forced to manually configure 5 days of practice or 4 quadrants of plays every single week before clicking `Simulate Week`, fast-sim players will experience severe click fatigue.
- **Data Starvation in `SeasonSummaryCard.tsx`:** Currently, [`SeasonDashboard.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/SeasonDashboard.tsx) only passes `season` and `summary` to `SeasonSummaryCard`—it does **not** pass `games`, `teams`, or `standings`, meaning `SeasonSummaryCard` doesn't even know who the user's Week $N$ opponent is or whether the user is on a Bye Week.
- **State Desynchronization with `/api/gameplan/install`:** If coordinator selections only live in ephemeral React state inside `SeasonSummaryCard`, navigating to `/playbook` or triggering the Contextual Narrator (`POST /api/broadcast/narrate`) won't reflect the locked coordinator script.

### The Superior Synthesis

Implement a **Modular Coordinator Prep Command Deck (`SeasonSummaryCard.tsx` v2)** that combines the strongest elements of the 5 concepts while preserving 1-click simulation ergonomics:
1. **Compact Macro League Ribbon (Top Bar):** Preserves the macro season metrics (`2026 Regular Season • Week N of 18 • X/272 Games • Progress %`) in a sleek top status strip so no existing macro information is lost, and keeps all existing `data-testid` hooks intact for E2E backwards compatibility.
2. **Matchup & Opponent Scouting Header (Concepts 1, 3 & 5):** Automatically resolves the user's active franchise (`selectedTeamId`) and current Week $N$ opponent from `games`, `teams`, and `standings` (with graceful **Bye Week Self-Scout** and **Playoff Bracket** states). Displays opponent record, division standing, offensive/defensive scheme tendencies, and primary "Game-Wrecker" threat.
3. **Interactive Coordinator Mode Switcher (Laminated Call-Sheet / Matchup Chessboard / Install Pipeline):**
   - **Situational Call-Sheet (Concept 2):** 4 color-coded situational quadrants (`1st & 10 Base`, `3rd Down Money`, `Red Zone`, `Game-Wrecker / Trench Rule`) with 1-click pill toggles and an **Auto-Scout Optimal Script** button.
   - **Mon–Sun Install Progress Bar (Concept 1):** Visualizes install readiness (`88% Staff Synergy`) and locks the week's gameplan via `POST /api/gameplan/install` (with optimistic local persistence in `localStorage` + backend sync).
   - **Direct Action Bar:** Prominent `Kickoff / Simulate Week N`, `Lock Call-Sheet`, `Auto-Scout`, and `Narrate Matchup` buttons.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** React 19, TypeScript 5.8, Vite 6, Tailwind CSS / Scoped Glassmorphic CSS, FastAPI + SQLAlchemy 2.0.
- **Language:** Strict TypeScript (`noImplicitAny`) and Python 3.12+ with strict Pydantic v2 schemas.
- **State Management:** React Router v7 `useLoaderData` (`seasonDashboardLoader`) + `useNarratorStore` (Zustand v5 with `useShallow`) + `/api/gameplan/install` persistence.

### 2. The Data Schema (Pre-Generation)

#### Frontend Type Definitions (`frontend/src/types/coordinatorPrep.ts`)
```typescript
export type SituationalQuadrantId =
  | "early_downs"
  | "third_down"
  | "red_zone"
  | "game_wrecker";

export interface CoordinatorCallOption {
  id: string;
  label: string;
  sublabel: string;
  modifierBadge: string;
  offenseStrategyKey?: string;
  defenseStrategyKey?: string;
}

export interface OpponentScoutingReport {
  opponentTeamId: number;
  opponentName: string;
  opponentAbbreviation: string;
  opponentRecord: string;
  isHomeGame: boolean;
  gameId: number;
  offensiveTendency: string;
  defensiveTendency: string;
  gameWreckerName: string;
  gameWreckerPosition: string;
  gameWreckerRating: number;
  recommendedCounterSummary: string;
}

export interface LockedCoordinatorGameplan {
  seasonId: number;
  week: number;
  teamId: number;
  opponentId: number | null;
  selections: Record<SituationalQuadrantId, string>;
  lockedAtIso: string;
  synergyScore: number;
}
```

#### Backend FactPacket Enrichment (`backend/app/services/narrator_facts_service.py`)
- Extend `_collect_team_facts` in `NarratorFactsService` to also inspect the **upcoming unplayed game** (`Game.is_played == False`, `Game.week == season.current_week`) for `team_id` so the Contextual SportsCenter Narrator can announce the upcoming Week $N$ opponent matchup alongside the last played game result.

### 3. Step-by-Step Execution

- [x] **Step 1: Opponent Scouting & Matchup Resolver (`frontend/src/utils/coordinatorScouting.ts`)**
  - Created deterministic helper functions that take `games: Game[]`, `teams: Team[]`, `standings: TeamStanding[]`, and `userTeamId: number` to compute `OpponentScoutingReport | null` (returning `null` on a Bye Week or offseason).
  - Derived authentic opponent tendencies (`11 Personnel Pass (64%)`, `Cover-3 Sky / 38% 3rd-Down Blitz`), primary Game-Wrecker threat alerts, and 4-quadrant situational options with synergy bonuses.
  - **Verified:** `npm --prefix frontend run build` & `lint` passed with 0 errors.

- [x] **Step 2: Upgrade `SeasonSummaryCard.tsx` & `SeasonSummaryCard.css` to the Coordinator Game-Week Prep Deck**
  - Updated `SeasonSummaryCardProps` in [`SeasonSummaryCard.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/season/SeasonSummaryCard.tsx) to accept `games`, `teams`, `standings`, and `userTeamId` props while preserving all existing props and test IDs (`season-summary-card`, `season-year`, `current-week`, `season-status`, `season-stats-grid`, `season-progress-section`, `champion-display`, `quick-actions-container`).
  - Rendered:
    1. **Top League Telemetry Strip:** Season Year, Current Week, Status Badge, Games Played, Remaining, and Season Progress bar.
    2. **Monday–Sunday Coordinator Install Pipeline Bar:** Interactive 6-stage install schedule (`Mon/Tue Film` $\rightarrow$ `Wed Base` $\rightarrow$ `Thu 3rd Down` $\rightarrow$ `Fri Red Zone` $\rightarrow$ `Sat Script Lock` $\rightarrow$ `Sun Kickoff`) with real-time staff readiness score (`95% Installed (+5 OVR Tactical Edge)`).
    3. **3-Column Tactical Command Deck:**
       - **Left Column:** Matchup Hero (`Opponent vs You`), opponent scheme tendencies, and Threat #1 Game-Wrecker Alert (with Bye Week recovery mode).
       - **Center Column:** Laminated Situational Call Matrix with 4 color-coded quadrants (`Q1 1st & 10 Base`, `Q2 3rd & Money`, `Q3 Red Zone`, `Q4 Neutralizer / Trench Rule`) and `⚡ Auto-Scout`.
       - **Right Column:** Staff Chemistry & Coaching Edge gauge, `🔒 Lock Weekly Call-Sheet` (persists to `localStorage` + `/api/gameplan/install`), `🎙️ Narrate Matchup & Keys` (triggers `useNarratorStore.getState().requestNarration`), and Quick Actions (`Simulate Week`, `Sim to Postseason`, `Bracket`, `Weekly Wrap-Up`).
  - Passed `games`, `teams`, `standings` from [`SeasonDashboard.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/SeasonDashboard.tsx) into `<SeasonSummaryCard />`.
  - **Verified:** `npm --prefix frontend run build` exited 0 in 9.31s with 0 errors.

- [x] **Step 3: Backend Upcoming-Matchup Fact Enrichment (`backend/app/services/narrator_facts_service.py`)**
  - Updated `NarratorFactsService._append_last_game_facts` to query all team season games in a single SQL query and extract both the last played game and upcoming unplayed game for `current_week`, adding an `upcoming_matchup` fact while preserving the `<= 6` SQL query budget.
  - **Verified:** `pytest backend/tests/services/test_narrator_facts_team.py backend/tests/services/test_narrator_facts_player.py -v` passed (`6 passed, 12 warnings in 8.08s`, including `test_build_fact_packet_sql_query_count_under_budget`).

- [x] **Step 4: Live Browser Screenshot & E2E Verification**
  - Inspected `/season` in Chrome DevTools MCP (`1440x900`), verified visual alignment, tested interactive quadrant toggles, auto-scouting, call-sheet locking, and live state updates.
  - Created dedicated Playwright E2E suite `frontend/e2e/coordinator-prep.spec.ts`.
  - **Verified:** `Set-Location frontend; npx playwright test e2e/coordinator-prep.spec.ts e2e/narrator.spec.ts e2e/season-dashboard-flow.spec.ts --project=chromium` passed verbatim: `9 passed (12.9s)`.

### 4. Edge Cases & Error Handling

- **Case A: Bye Week / No Scheduled Game in Week $N$:** Renders a dedicated **"BYE WEEK SELF-SCOUT & RECOVERY CLINIC"** card in place of the opponent matchup, allowing the user to select bye-week focus (`Veteran Rest & Rehab`, `Rookie Development Reps`, `Self-Scout Tendency Breaker`).
- **Case B: Offseason / Postseason Completed:** Displays Championship / Offseason transition status and disables weekly install toggles cleanly.
- **Case C: `/api/gameplan/install` Endpoint Unavailable or Offline:** Persists locked coordinator selections to `localStorage` (`nfl_sim_coordinator_prep_{seasonId}_{week}_{teamId}`) and displays a non-blocking confirmation badge so UX never breaks.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** `npm --prefix frontend run build`, `npm --prefix frontend run lint`, and `pytest` pass with 0 errors and zero `any` types.
- [x] **Security:** All user/DB inputs sanitized; no inline script injection; safe `localStorage` parsing.
- [x] **Performance:** Preserves `<= 6` SQL query ceiling in `NarratorFactsService` and `< 25ms` cached `/api/season/summary` response times.
- [x] **Self-Critique:** Preserved all existing `data-testid` attributes (`season-summary-card`, `season-year`, `current-week`, `season-status`, `season-stats-grid`, `season-progress-section`, `champion-display`, `quick-actions-container`, `simulate-btn`) guaranteeing 100% backwards compatibility with existing Playwright E2E suites while completely modernizing the coordinator experience.
</final_audit>

---

<baton_handoff>
All steps completed and verified. Terminal outputs:
- Pytest: `6 passed in 8.08s`
- Frontend Build: `tsc -b && vite build` built cleanly in 9.31s
- Frontend Lint: `eslint .` passed with 0 errors
- Playwright E2E: `9 passed (12.9s)`
</baton_handoff>

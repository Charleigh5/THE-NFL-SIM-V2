<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-006: NCAA 25 & Madden 25 Style Depth Chart Architecture & Dynamic Franchise Synchronization

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Modern depth chart hierarchy evolved from classic EA Sports NCAA Football and Madden franchise systems: categorizing rosters into distinct operational units (Offense, Defense, Special Teams, and Specialists / Sub-Packages) rather than flat 1-dimensional lists.
- **Related Ideas:**
  - Cross-position positional flexibility (e.g., slot wide receivers, 3rd down passing backs, rushing defensive ends, sub package linebackers/safeties, and offensive line versatility).
  - Dynamic franchise state management binding active franchise theme context, persisted settings, and real-time backend roster endpoints.
- **Future Potential:**
  - Dynamic in-game injury substitutions, formation-specific package audibles, stamina-based automated rotational fatigue sliders, and unit chemistry progression tracking.
- **Constraints:**
  - Zero `any` types in TypeScript implementations.
  - Full backward compatibility with existing Playwright E2E selectors (`.Reorder_Group`, `.bg-white\/5.p-4.rounded-lg`, button "Save Changes").
  - Seamless support for all 32 NFL franchises with instant reactive roster updates.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Hardcode or lazily fetch a single static team's roster with flat position pills (`QB`, `RB`, `WR`, etc.) and a basic list view.

### Powerful Antithesis
- Fails when the user selects their favorite team (e.g. Detroit Lions, Green Bay Packers, KC Chiefs) because the view remains locked to team ID 1.
- Incomplete categorization ignores modern football sub-packages (3DRB, PWHB, SLWR, SUBLB, SLCB, Kick/Punt Returners) and breaks immersion.
- Rigid position strings in the database (e.g. `OL`, `DL`, `S`) cause empty position lists if the front-end requests specific codes (`LT`, `DT`, `FS`).

### The Superior Synthesis
- Build a 4-Unit Master Architecture (**OFFENSE**, **DEFENSE**, **SPECIAL TEAMS**, **SPECIALISTS & SUB**) with intelligent cross-position compatibility matching.
- Bind the active franchise dynamically via `useTheme`, `useSettingsStore`, `localStorage`, and an interactive Top Franchise Selector.
- Provide glassmorphic EA Sports Madden 25 / NCAA 25 cards with metallic OVR badges, physical attributes (SPD, ACC, STR, AWR), development traits, promote/demote quick controls, drag-and-drop handles, auto-reorder by OVR, and detailed player dossier modals.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19, Vite, Tailwind CSS, Framer Motion, Lucide Icons, FastAPI, SQLAlchemy 2.0.
- **State Management:** Zustand (`useSettingsStore`), React Context (`useTheme`), React Router v7 data loaders.
- **Endpoints:**
  - `GET /api/teams/{team_id}/roster` -> Returns complete 53-man roster with physical attributes and traits.
  - `GET /api/teams/{team_id}/chemistry` -> Returns offensive line and unit chemistry ratings.
  - `PUT /api/teams/{team_id}/depth-chart` -> Persists updated position rank ordering.

### 2. The Data Schema (Pre-Generation)
```typescript
export type DepthUnit = "OFFENSE" | "DEFENSE" | "SPECIAL_TEAMS" | "SPECIALISTS";

export interface PositionConfig {
  code: string;
  name: string;
  unit: DepthUnit;
  targetCount: number;
  compatiblePositions: string[];
  description: string;
}

export interface PlayerSchema {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  jersey_number: number;
  overall_rating: number;
  depth_chart_rank?: number;
  age: number;
  experience: number;
  height?: number;
  weight?: number;
  college?: string;
  speed?: number;
  acceleration?: number;
  strength?: number;
  agility?: number;
  awareness?: number;
  injury_status?: string;
  development_trait?: string;
}
```

### 3. Step-by-Step Execution
- [x] **Step 1: Backend Endpoint Hardening.** Updated `backend/app/api/endpoints/teams.py` `PlayerSchema` and loosened strict position matching in `update_depth_chart` to support sub-packages.
- [x] **Step 2: Frontend Data Models & Types.** Added `college`, `injury_status`, `development_trait`, and `archetype` to `frontend/src/services/api.ts`.
- [x] **Step 3: Depth Chart Redesign.** Authored `frontend/src/pages/DepthChart.tsx` with 4-unit tabs, position pill bar, room average metrics, starter spotlight, Madden glassmorphic cards, and auto-sort/save controls.
- [x] **Step 4: Franchise Persistence Sync.** Synchronized `handleSelectTeam` in `TeamSelection.tsx` and `DepthChart.tsx` with `localStorage` and `useTheme`.

### 4. Edge Cases & Error Handling
- [Case A: Null Roster on New Team] -> Renders styled fallback notice prompting user to add athletes.
- [Case B: Cross-Positional Athletes] -> Displays `Nat: [Pos]` badge with calculated positional effectiveness.
- [Case C: Save Network Error] -> Displays graceful error notification without losing user's local reorder state.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** 100% type safety with zero `any` types (`npm run build` compiled in 12.43s).
- [x] **Backend Unit Tests:** 354/354 unit tests passing (`pytest backend/tests/unit`).
- [x] **Browser End-to-End Verification:**
  - Verified Green Bay Packers (GB) initial load with QB, DE, and OL chemistry.
  - Verified dynamic switch to Detroit Lions (DET) loading Jared Goff (#16, OVR 79), Richard Sanchez (#40, OVR 75), Sione Vaki, Jahmyr Gibbs, and David Montgomery.
  - Verified interactive unit tabs (**OFFENSE**, **DEFENSE**, **SPECIAL TEAMS**, **SPECIALISTS & SUB**).
  - Verified interactive Player Dossier modal opening on Richard Sanchez.
</final_audit>

---

<baton_handoff>
Next Immediate Step: System is ready for active gameplay simulation, roster management, or advancing the dynasty calendar.
</baton_handoff>

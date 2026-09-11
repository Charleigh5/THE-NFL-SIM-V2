<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK_011_LOCKER_ROOM_AND_CLOSED_DOOR_COUNCIL_UI

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Professional football locker rooms are fragile social ecosystems where massive egos, contract grievances, target share disputes, and coaching philosophies collide.
  - In `THE-NFL-SIM-V2`, the backend already possesses a sophisticated 3-Tier **Society Engine**:
    - *Tier 1*: Deterministic differential equation engine tracking weekly tension deltas and Big-Six Psychological DNA (`Ego`, `Greed`, `Loyalty`, `Resilience`, `Paranoia`, `Professionalism`).
    - *Tier 2*: Event activation gate triggering when any player's cumulative tension reaches $\ge 75.0$.
    - *Tier 3*: Multi-agent narrative council (`LockerRoomAgentService`) modeling closed-door confrontation dialogue between the Disgruntled Star, the Head Coach, and the Team Captain.
  - However, the frontend currently lacks an interactive interface to expose this system. The General Manager cannot observe roster tension, inspect psychological profiles, or intervene in high-stakes closed-door summits.

- **Related Ideas & Industry Parallels:**
  - *Crusader Kings III Small Council & Feud System*: Visual council table with competing faction demands, opinion meters, and high-consequence ultimatums.
  - *Football Manager Team Dynamics*: Hierarchy pyramid (Team Leaders, Highly Influential, Other Players), social groups, and volatile player promises.
  - *BioWare / Mass Effect Dialogue Wheel*: Branching moral/strategic choices with explicit consequence forecasting (Morale, Chemistry, Trade Urgency).

- **Future Potential (2026/2027):**
  - Anonymous press leaks to national beat reporters, locker room mutinies causing coach firing ultimatums, and contract renegotiation holdouts during training camp.

- **Constraints:**
  - Sub-100ms render latency for multi-speaker confrontation dialogues with instant fallback if LLM synthesis is offline.
  - 100% adherence to the Canonical 3-Gate Security Pattern: All dialogue inputs sanitized against prompt injection.
  - Strict typing in TypeScript (zero `any`) and Python Pydantic V2 schemas.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Render a simple notification banner on the Dashboard when tension $\ge 75.0$ stating "Player X has a grievance" with a modal showing a static paragraph and a single button to "Resolve".

### Powerful Antithesis
- **Zero Atmospheric Immersion**: A plain notification banner fails to convey the tension of an NFL franchise on the brink of revolt.
- **Hidden Underlying Dynamics**: If users only see an alert when tension reaches 75.0, they cannot proactively manage emerging grievances (e.g. at tension 50-65) through target share adjustments or contract extensions.
- **Unidimensional Flattening**: An NFL locker room incident is inherently a 3-way clash: The player fights for his career/money, the coach demands accountability and scheme discipline, and the captain seeks to preserve playoff focus. Collapsing this into a 1-on-1 popup destroys the narrative depth.
- **Unaccountable Consequences**: Users must clearly see the direct mathematical trade-offs of their decisions (e.g., siding with the star alienates the head coach; siding with the coach causes a public trade demand).

### The Superior Synthesis
Build a dedicated **Locker Room & Closed-Door Council Hub**:
1. **Front Office Locker Room Command Center**:
   - Live **Team Tension Barometer** (0-100) and **Locker Room Chemistry Grade** (A+ to F).
   - **Grievance Heatmap Grid**: Roster cards classified by status: *Calm* (0-49, emerald), *Simmering* (50-74, amber), and *Boiling / Incident Imminent* (75+, crimson).
   - **Big-Six Psychological DNA Hexagon**: Interactive radar graph visualizing a player's core personality traits alongside their narrative backstory anchors.
2. **Interactive 3-Way Closed-Door Confrontation Modal (`ClosedDoorCouncilModal.tsx`)**:
   - High-contrast visual staging: Disgruntled Star (Left), Head Coach (Center), Team Captain (Right) with dynamic audio-reactive avatar cards.
   - Cinematic conversation timeline: Sequenced dialogue bubbles rendering `LockerRoomDialogueTurn[]` with distinct role typography.
   - GM Decision Matrix: 5 strategic resolution choices (`promise_targets`, `bench_player`, `address_team`, `explore_trade`, `fine_conduct`) with live projected delta tags.
   - Aftermath Receipt: Animated summary modal showing morale updates, trust shifts, and press headline generation.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend:** FastAPI, SQLAlchemy, `backend/app/engine/society/locker_room_agent.py`, `backend/app/schemas/society.py`.
- **Frontend:** React 19, Framer Motion, Lucide React (`Flame`, `UserX`, `MessageSquare`, `ShieldAlert`, `Scale`), Tailwind CSS + Custom Dark Theme.
- **State Management:** `useSocietyStore.ts` synchronized with active team ID.

### 2. The Data Schema (Pre-Generation)

#### Backend Pydantic Schemas (`backend/app/schemas/society.py`)

```python
# Existing schemas to leverage:
# PsychologicalDNA, PlayerBackstory, TensionDelta, LockerRoomDialogueTurn,
# LockerRoomConsequences, LockerRoomActionOption, LockerRoomEventResponse,
# LockerRoomResolutionRequest, LockerRoomResolutionResponse

class TeamLockerRoomOverview(BaseModel):
    team_id: int
    overall_chemistry_score: float
    chemistry_grade: str  # "A+", "A", "B", "C", "D", "F"
    active_incidents_count: int
    high_tension_players_count: int
    roster_tension_summary: List[Dict[str, Any]]
```

#### Frontend TypeScript Interfaces (`frontend/src/types/society.ts`)

```typescript
export interface PsychologicalDNA {
  ego: number;
  greed: number;
  loyalty: number;
  resilience: number;
  paranoia: number;
  professionalism: number;
}

export interface LockerRoomDialogueTurn {
  speaker_name: string;
  speaker_role: "disgruntled_star" | "team_captain" | "head_coach" | "position_coach";
  speaker_id?: number;
  text: string;
}

export interface LockerRoomActionOption {
  id: "promise_targets" | "bench_player" | "address_team" | "explore_trade" | "fine_conduct";
  label: string;
  description: string;
  projected_impact: string;
}

export interface LockerRoomEventResponse {
  team_id: number;
  week: number;
  active_actors: number[];
  captain_id?: number;
  head_coach_name: string;
  incident_type: string;
  confrontation_dialogue: LockerRoomDialogueTurn[];
  consequences: {
    morale_deltas: Record<string, number>;
    trust_coach_deltas: Record<string, number>;
    trust_qb_deltas: Record<string, number>;
    trade_requested: boolean;
    team_chemistry_delta: number;
    drama_headline: string;
  };
  action_options: LockerRoomActionOption[];
}
```

### 3. Step-by-Step Execution

#### Step 1: Scaffolding
- [ ] Create endpoint `GET /society/teams/{team_id}/locker-room/overview` in `backend/app/api/endpoints/society.py`.
- [ ] Create TypeScript types in `frontend/src/types/society.ts`.
- [ ] Create API service `frontend/src/services/societyApi.ts`.
- [ ] Create Zustand store `frontend/src/store/useSocietyStore.ts`.
- [ ] Scaffold components directory `frontend/src/components/society/`.

#### Step 2: Core Logic Implementation
- [ ] **Subtask 2.1: Roster Tension & Chemistry Overview Aggregator**
  - Implement `get_team_locker_room_overview` in `backend/app/engine/society/locker_room_agent.py` computing team chemistry mean, standard deviation of grievances, and risk tiers.
- [ ] **Subtask 2.2: Automated Weekly Evaluation Hook**
  - Link `evaluate_team_locker_room` into the season week advancement orchestrator (`advance_week` in `season_service.py`), creating a persistent pending council incident if tension $\ge 75.0$.
- [ ] **Subtask 2.3: GM Action Resolution Pipeline**
  - Verify that `resolve_action` in `locker_room_agent.py` commits all mutations (`morale`, `chemistry`, `trade_requested`, and log entries) inside an atomic DB transaction.

#### Step 3: Interface & Experience
- [ ] **Subtask 3.1: Locker Room Tab in Front Office (`LockerRoomHub.tsx`)**
  - Build Team Chemistry Gauge with visual status bars and tension indicators.
  - Implement Roster Tension Heatmap showing player OVR, position, tension score, and primary driver (e.g. "Low Targets", "Contract Year", "Losing Streak").
- [ ] **Subtask 3.2: Psychological DNA Radar Visualizer (`PsychologicalHexagon.tsx`)**
  - Render SVG radar/spider chart showing Big-Six personality distribution for selected player.
- [ ] **Subtask 3.3: 3-Way Closed-Door Council Modal (`ClosedDoorCouncilModal.tsx`)**
  - Avatar cards for Star, Coach, and Captain with glowing status rings.
  - Sequenced Framer Motion dialogue bubbles with typing animation effect.
  - Action card selection buttons with clear impact badges.
- [ ] **Subtask 3.4: Resolution Aftermath & News Ticker**
  - Animate outcome cards showing chemistry shifts and auto-generated beat reporter headline ("Sources: Locker room meeting diffuses WR trade talk").

### 4. Edge Cases & Error Handling

- [Case A: No Active Grievances] -> Displays harmonious locker room state with "All Clear: Team Morale Optimal" and proactive leadership accolades.
- [Case B: The Disgruntled Player IS the Captain] -> System promotes the next highest leadership player as interim spokesperson for the confrontation.
- [Case C: Star Player Trade Request Triggered] -> Automatically surfaces player in the Trade Center block with trade demand badge.
- [Case D: Rapid Double Resolution Clicks] -> Frontend disables action buttons immediately upon selection and shows spinner until DB returns confirmation.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** TypeScript compilation with zero errors; no implicit `any`.
- [ ] **Security:** All dialogue generation verified against the Canonical 3-Gate Security Pattern.
- [ ] **Performance:** Modal dialogue transitions run at 60 FPS; API overview loads in $< 60$ms.
- [ ] **Self-Critique:** If the LLM call fails or times out, does the council gracefully fall back? Yes, `LockerRoomAgentService` contains 100% deterministic offline dialogue templates.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Scaffold `frontend/src/components/society/` and implement `GET /society/teams/{team_id}/locker-room/overview`.
</baton_handoff>

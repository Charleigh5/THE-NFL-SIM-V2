<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK_013_IN_GAME_PLAY_CALLING_HUD_DURING_LIVE_SIM

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - In pro football, the sideline head coach and coordinators orchestrate chess matches at breakneck speed. Every down presents strategic trade-offs: pass protections vs exotic blitz packages, clock management via timeouts, and critical 4th-down analytics calls (Go For It, Field Goal, Punt).
  - In `THE-NFL-SIM-V2`, the live simulation (`LiveSim.tsx` and `live_visualization.py`) currently operates primarily in "Spectator Mode": the backend simulates the game autonomously while the frontend renders field canvas animations and scoreboards.
  - Users lack interactive coaching control: they cannot call offensive play concepts (Inside Zone, Power, Play Action Deep Shot, Quick Slants) or defensive coverages (Cover 1, Cover 2 Man, Cover 3 Sky, Fire Zone Blitz), manage timeouts during two-minute drills, or make crucial 4th-down decisions based on expected value analytics.

- **Related Ideas & Industry Parallels:**
  - *Madden / College Football Coach Mode*: Interactive play-calling trays organized by Concept and Formation, with play-clock pressure.
  - *NFL Next Gen Stats & Baldwin 4th-Down Decision Bot*: Real-time Win Probability (WP) and Expected Points Added (EPA) calculators recommending high-leverage 4th-down decisions.
  - *Football Manager In-Game Touchline Shouts & Tactical Changes*: Real-time tactical shifts, tempo toggles (Normal, Chew Clock, No-Huddle), and timeout calls.

- **Future Potential (2026/2027):**
  - Defensive coordinators diagnosing user play-calling tendencies using pattern-matching AI, crowd noise audio disruption causing false starts in hostile road stadiums.

- **Constraints:**
  - Real-time synchronization over WebSocket (`/ws/simulation/live`) or rapid HTTP polling with $< 50$ms play injection latency.
  - Non-blocking pause mechanism: Simulation smoothly pauses on critical decision points without freezing the UI or breaking the WebSocket stream.
  - 100% deterministic physics resolution: User-called concepts feed directly into `play_resolver.py` and `trajectory_engine.py`.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Add three buttons (Run, Pass, Punt) at the bottom of `LiveSim.tsx` that fire an API request to `POST /api/simulation/play` during the live game.

### Powerful Antithesis
- **Live Stream Race Condition**: The live simulation loop runs asynchronously at 60 FPS or 1-second ticks. If the simulation does not halt when the user has possession, the game advances past 2nd and 3rd down before the user can even read the options, causing play-call desyncs.
- **Trivial Gameplay**: 3 generic buttons (Run/Pass/Punt) insult the tactical complexity of American football. Coaches do not call "Pass"; they call "PA Bootleg", "Mesh", or "Four Verticals" against specific defensive shell looks.
- **Blind 4th-Down Choices**: Forcing users to guess on 4th-and-2 from the opponent's 38-yard line without displaying Field Goal range, kick probability, or EPA leaves users frustrated.
- **Clock Mismanagement**: Without timeout controls and clock tempo toggles ("Chew Clock", "Hurry Up", "Spike"), endgame two-minute drills cannot be realistically executed.

### The Superior Synthesis
Architect a **Comprehensive Coach Play-Calling HUD**:
1. **Interactive Mode Switcher**:
   - Seamlessly toggle between **"Coach Mode"** (User commands plays for the user franchise) and **"Spectator Mode"** (Pure AI vs AI auto-simulation).
2. **Deterministic Play-Clock Pause Hook**:
   - When in Coach Mode and the user team is on offense or defense, the live engine pauses at the snap decision point, displaying the play-calling HUD with a 25-second play clock timer.
3. **Tactical Play-Call Drawer**:
   - **Offensive Concepts**: Run (Inside Zone, Outside Stretch, Counter), Pass (Quick Slants, Mesh, Flood, Four Verticals, Screen), Specialty (QB Sneak, Spike, Kneel).
   - **Defensive Schemes**: Base Front (Cover 3 Sky, Cover 2 Tampa, Cover 1 Man-Free), Blitzes (Nickel Overload, Corner Blitz, Fire Zone 3).
4. **Automated 4th-Down Analytics Modal (`FourthDownDecisionModal.tsx`)**:
   - Triggered automatically whenever facing 4th down in both Coach and Spectator modes.
   - Computes live Expected Points & Win Probability for each path:
     $$\text{Recommendation} = \arg\max_{a \in \{\text{Go}, \text{FG}, \text{Punt}\}} \text{WP}(a)$$
   - Displays kicker range, historical conversion rates, and instant execution buttons.
5. **Sideline Clock & Timeout Suite**:
   - 3 timeout pills per team with instant-call button, clock runoff controls, and hurry-up/chew-clock toggles.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend:** FastAPI, WebSockets (`/ws/simulation/live`), `backend/app/orchestrator/play_resolver.py`, `backend/app/engine/live_game.py`.
- **Frontend:** React 19, TypeScript, Framer Motion, Lucide React (`Play`, `Shield`, `Crosshair`, `Clock`, `Zap`), soundEffects engine.
- **State Management:** `useSimulationStore.ts` extended with `playCallingState` and `timeoutState`.

### 2. The Data Schema (Pre-Generation)

#### Backend Schemas (`backend/app/schemas/playcalling.py`)

```python
from typing import Optional, Literal
from pydantic import BaseModel, Field

class PlayCallRequest(BaseModel):
    game_id: int
    team_id: int
    play_type: Literal["RUN", "PASS", "FIELD_GOAL", "PUNT", "SPIKE", "KNEEL"]
    concept_id: str  # "inside_zone", "stretch_run", "slants", "four_verticals", "mesh", "cover_3", "cover_2_man", "fire_zone"
    tempo: Literal["NORMAL", "HURRY_UP", "CHEW_CLOCK"] = "NORMAL"

class FourthDownDecisionContext(BaseModel):
    game_id: int
    down: int = 4
    yards_to_go: int
    yard_line: int  # 1 to 99 (from own goal)
    quarter: int
    seconds_remaining: int
    score_differential: int  # Positive = leading, negative = trailing
    kicker_fg_probability: float
    recommended_action: Literal["GO_FOR_IT", "FIELD_GOAL", "PUNT"]
    go_for_it_wp: float
    field_goal_wp: float
    punt_wp: float

class TimeoutCallRequest(BaseModel):
    game_id: int
    team_id: int
```

#### Frontend TypeScript Interfaces (`frontend/src/types/playcalling.ts`)

```typescript
export type PlayCategory = "RUN" | "PASS" | "DEFENSE" | "SPECIAL_TEAMS";

export interface PlayConcept {
  id: string;
  name: string;
  category: PlayCategory;
  diagram: string;
  riskReward: "SAFE" | "BALANCED" | "AGGRESSIVE";
  description: string;
}

export interface FourthDownAnalytics {
  recommendedAction: "GO_FOR_IT" | "FIELD_GOAL" | "PUNT";
  goForItWp: number;
  fieldGoalWp: number;
  puntWp: number;
  fgDistance: number;
  fgProbability: number;
}
```

### 3. Step-by-Step Execution

#### Step 1: Scaffolding
- [ ] Create schema file `backend/app/schemas/playcalling.py`.
- [ ] Create frontend types `frontend/src/types/playcalling.ts`.
- [ ] Scaffold components:
  - `frontend/src/components/game/PlayCallingHUD.tsx`
  - `frontend/src/components/game/FourthDownModal.tsx`
  - `frontend/src/components/game/ClockManagementBar.tsx`
- [ ] Extend `frontend/src/store/useSimulationStore.ts` with coaching actions.

#### Step 2: Core Logic Implementation
- [ ] **Subtask 2.1: Live Engine Manual Play Injection**
  - Update `backend/app/engine/live_game.py` / `live_visualization.py` to support paused state waiting for `play_call` input over WebSocket or REST.
- [ ] **Subtask 2.2: 4th-Down Analytics Engine**
  - Implement `calculate_fourth_down_recommendation` in `backend/app/engine/fourth_down_calculator.py` using Baldwin formula weighting win probability, score differential, and field position.
- [ ] **Subtask 2.3: Timeout & Clock Stoppage Controller**
  - Implement `call_timeout` endpoint in `backend/app/api/endpoints/simulation.py` deducting timeouts and stopping game clock immediately.

#### Step 3: Interface & Experience
- [ ] **Subtask 3.1: Mount PlayCallingHUD in `LiveSim.tsx`**
  - Responsive collapsible bottom drawer featuring Run, Pass, and Defensive concept cards with custom tactical diagrams.
- [ ] **Subtask 3.2: 4th Down High-Leverage Prompt Modal (`FourthDownModal.tsx`)**
  - Cinematic modal popping up on 4th down with glowing recommendation badge, odds comparison bars, and audio heartbeat effect.
- [ ] **Subtask 3.3: Sideline Clock & Timeout Bar**
  - Display interactive timeout pills (3/3), 2-minute drill hurry-up toggle, and spike/kneel emergency buttons.
- [ ] **Subtask 3.4: Coach Mode vs Spectator Mode Toggle**
  - Clean top-bar switcher allowing user to hand over play-calling to AI coordinator at any moment.

### 4. Edge Cases & Error Handling

- [Case A: Play Clock Expiration (Delay of Game)] -> If user does not pick within 25 seconds, simulation assesses 5-yard penalty and automatically calls default play.
- [Case B: Zero Timeouts Remaining] -> Timeout button displays "0 Remaining" and disables with sound effect buzz.
- [Case C: Sudden-Death Overtime] -> 4th-down engine recalculates with overtime sudden-death win probability matrix.
- [Case D: WebSocket Disconnection during Play Call] -> Gracefully queues choice and submits via REST fallback endpoint.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Zero `any` types; verified via `tsc --noEmit` and `mypy` / `pyright`.
- [ ] **Security:** Client play call validated against authorized current possession team ID.
- [ ] **Performance:** Play-call to physics resolution latency $< 45$ms.
- [ ] **Self-Critique:** Can the user play defense as well as offense? Yes, when the opponent has possession, the HUD switches automatically to defensive coverages/blitzes.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Scaffold `backend/app/schemas/playcalling.py` and build `PlayCallingHUD.tsx` in `frontend/src/components/game/`.
</baton_handoff>

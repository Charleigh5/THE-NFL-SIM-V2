<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026 Production Standard
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification, strict types (no `any`).
</system_context>

# REQUIREMENT 4 (R4): IN-GAME PLAY-CALLING HUD DURING LIVE SIM
## Exhaustive File Extrapolation & 5 Tangential Feature Expansions

---

## 📂 SECTION 1: CORE FILE EXTRAPOLATION FOR R4

Every individual file required to deliver the real-time Play-Calling HUD, 4th-down decision analytics modal, and sideline clock/timeout controls is enumerated below with its architectural layer, explicit responsibilities, and complete data interfaces.

```
THE-NFL-SIM-V2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       └── simulation.py                  # [MODIFY] Add play injection, timeout & fourth-down endpoints
│   │   ├── schemas/
│   │   │   └── playcalling.py                     # [NEW] Strict Pydantic V2 models for calls & 4th-down context
│   │   ├── engine/
│   │   │   ├── fourth_down_calculator.py          # [NEW] Real-time Win Probability & Baldwin EPA decision model
│   │   │   ├── timeout_controller.py              # [NEW] Timeout deduction, clock stoppage & runoff logic
│   │   │   └── live_game.py                       # [MODIFY] Implement coach mode pause loop & user play resolution
│   │   └── orchestrator/
│   │       └── play_resolver.py                   # [MODIFY] Map user concepts (e.g. Mesh, Cover 3) into physics engine
│   └── tests/
│       └── unit/
│           ├── test_fourth_down_calculator.py     # [NEW] Unit tests verifying Baldwin model mathematical outputs
│           └── test_coach_mode_play_calling.py    # [NEW] Unit tests verifying user play resolution in live sim
└── frontend/
    └── src/
        ├── types/
        │   └── playcalling.ts                     # [NEW] TypeScript definitions for concepts, formations, analytics
        ├── services/
        │   └── playcallingApi.ts                  # [NEW] API client for submitting plays and calling timeouts
        ├── store/
        │   └── useSimulationStore.ts              # [MODIFY] Add coachMode, playCallingState, timeoutState
        ├── components/
        │   └── game/
        │       ├── PlayCallingHUD.tsx             # [NEW] Interactive bottom drawer with offensive & defensive cards
        │       ├── ConceptSelectorTray.tsx        # [NEW] Tactical diagrams showing route arrows & run lanes
        │       ├── FourthDownModal.tsx            # [NEW] Dramatic high-leverage 4th-down analytics prompt
        │       ├── SidelineClockControls.tsx      # [NEW] Timeout pills (3/3), hurry-up toggle, spike/kneel buttons
        │       ├── PlayClockTimer.tsx             # [NEW] Animated 25-second play clock with buzzer sound
        │       └── PlayCalling.module.css         # [NEW] High-contrast broadcast HUD styling
        ├── pages/
        │   └── LiveSim.tsx                        # [MODIFY] Mount PlayCallingHUD & FourthDownModal in live game view
        └── e2e/
            └── play-calling-live-sim.spec.ts      # [NEW] Playwright E2E test for coach mode play execution
```

---

### Detailed File Specifications (R4 Core)

#### 1. `backend/app/schemas/playcalling.py`
- **Purpose**: Strict validation schemas for user play calls, 4th-down decision prompts, and timeout controls.
```python
from typing import Optional, Literal
from pydantic import BaseModel, Field

class PlayCallRequest(BaseModel):
    game_id: int
    team_id: int
    play_type: Literal["RUN", "PASS", "FIELD_GOAL", "PUNT", "SPIKE", "KNEEL"]
    concept_id: str  # e.g. "inside_zone", "stretch_run", "slants", "four_verticals", "mesh", "cover_3", "cover_2_man", "fire_zone"
    tempo: Literal["NORMAL", "HURRY_UP", "CHEW_CLOCK"] = "NORMAL"

class FourthDownDecisionContext(BaseModel):
    game_id: int
    down: int = 4
    yards_to_go: int
    yard_line: int  # 1 to 99 (from own end zone)
    quarter: int
    seconds_remaining: int
    score_differential: int  # Positive = leading, negative = trailing
    kicker_fg_probability: float
    recommended_action: Literal["GO_FOR_IT", "FIELD_GOAL", "PUNT"]
    go_for_it_wp: float
    field_goal_wp: float
    punt_wp: float
    net_win_prob_delta: float

class TimeoutCallRequest(BaseModel):
    game_id: int
    team_id: int

class TimeoutCallResponse(BaseModel):
    game_id: int
    team_id: int
    timeouts_remaining: int
    clock_stopped_at: str
    charged_to_team: str
```

#### 2. `frontend/src/types/playcalling.ts`
- **Purpose**: Frontend TypeScript definitions for tactical plays, 4th-down analytics, and coach mode state.
```typescript
export type PlayType = "RUN" | "PASS" | "FIELD_GOAL" | "PUNT" | "SPIKE" | "KNEEL";

export interface TacticalConcept {
  id: string;
  name: string;
  category: "RUN" | "PASS" | "DEFENSE";
  formation: "SHOTGUN" | "UNDER_CENTER" | "PISTOL" | "NICKEL" | "DIME" | "BASE_43";
  diagramSvg: string; // SVG path string for animated route diagram
  targetPersonnel: string; // e.g. "11 Personnel", "12 Personnel"
  riskReward: "SAFE" | "BALANCED" | "AGGRESSIVE";
}

export interface FourthDownAnalytics {
  recommendedAction: "GO_FOR_IT" | "FIELD_GOAL" | "PUNT";
  goForItWp: number;
  fieldGoalWp: number;
  puntWp: number;
  fgDistance: number;
  fgSuccessProbability: number;
  historicalConversionRate: number;
}
```

---

## 🚀 SECTION 2: FIVE TANGENTIALLY RELATED FEATURE EXPANSIONS (R4)

### Expansion 4.1: Baldwin 4th-Down & 2-Point Conversion Real-Time Analytics HUD
- **Conceptual Rationale:** Modern NFL decision-making is anchored by public analytics models (such as Ben Baldwin's 4th down and 2-point conversion bot). Coaches require immediate visual clarity on whether attempting a 2-point conversion after a touchdown shifts win probability positively (e.g. going for 2 when trailing by 8 to tie, or trailing by 2 to win).
- **Concrete Technical Architecture & Mechanics:**
  - Real-Time Baldwin Conversion Matrix:
    - Down/Distance/Yardline converted into Expected Points Added (EPA) and Win Probability (WP) via logistic regression weights.
    - Post-Touchdown 2-Point Conversion Trigger: When score differential is $-8, -2, +1, +4$, HUD generates a glowing analytics recommendation box: *"Go for 2 (+3.2% WP)"*.
- **Files to Create / Modify:**
  - `backend/app/engine/analytics/baldwin_conversion_model.py`
  - `backend/app/schemas/two_point_analytics.py`
  - `frontend/src/components/game/TwoPointConversionModal.tsx`
- **Data Schemas:**
  ```python
  class TwoPointAnalytics(BaseModel):
      lead_after_one_point: int
      lead_after_two_points: int
      one_point_wp: float
      two_point_wp: float
      recommended_decision: Literal["KICK_PAT", "GO_FOR_TWO"]
      rationale: str
  ```
- **UI/UX Flow:** Following an offensive touchdown, the scoreboard halts briefly with a dual-card choice modal displaying animated win probability bars for "1-Point Kick (96% XP)" vs "2-Point Conversion (48% XP, +3.8% WP)".

---

### Expansion 4.2: Acoustic Decibel & Hostile Crowd Noise Interference Engine
- **Conceptual Rationale:** Hostile road venues (e.g. Seattle's Lumen Field, Kansas City's Arrowhead Stadium) generate over 135 decibels of crowd noise. This deafens visiting offensive lines, making verbal snap counts impossible, requiring silent snap counts, causing false starts, and preventing audibles at the line of scrimmage.
- **Concrete Technical Architecture & Mechanics:**
  - Stadium Decibel Level ($dB$) calculated dynamically based on Game Importance, Quarter, 3rd/4th down, and Stadium Acoustics.
  - Audible Failure Risk ($P_{\text{fail}}$):
    $$P_{\text{audible\_failure}} = \max\left(0.0, \frac{dB - 105}{40}\right) \times (1.0 - \text{QB\_Awareness} \times 0.01)$$
  - Audio Synthesis: Real-time Web Audio API pink-noise distortion and stadium roar that dynamically swells on critical 3rd and 4th down road plays.
- **Files to Create / Modify:**
  - `backend/app/engine/physics/crowd_noise_engine.py`
  - `frontend/src/services/audio/stadiumAcoustics.ts`
  - `frontend/src/components/game/DecibelMeterWidget.tsx`
- **Data Schemas:**
  ```typescript
  export interface CrowdNoiseState {
    currentDecibels: number;
    stadiumVibe: "CALM" | "LOUD" | "DEAFENING_DEATH_VALLEY";
    audibleCommunicationPenalty: number;
    falseStartRiskMultiplier: number;
  }
  ```
- **UI/UX Flow:** On critical road snaps, the screen edges vibrate with a shaking soundwave graphic, the crowd roar drowns out the field audio, and calling an audible requires passing an instant quick-time check.

---

### Expansion 4.3: Defensive Coordinator Tendency Recognition & Counter-Call Buffs
- **Conceptual Rationale:** Elite NFL defensive coordinators (e.g. Steve Spagnuolo, Vic Fangio) track offensive tendencies meticulously. If a human player becomes predictable (e.g., calling Inside Zone on 70% of 1st downs or Quick Slants on 3rd-and-short), the AI coordinator anticipates the play, audibles into a run blitz, and blows up the backfield.
- **Concrete Technical Architecture & Mechanics:**
  - Rolling 20-play Tendency Matrix tracking User Down/Distance concept distribution:
    $$\text{Predictability}(c) = \frac{\text{Count}(c \mid \text{Down}, \text{Distance})}{\sum \text{Plays}}$$
  - Counter-Call Trigger: When predictability of a concept exceeds $60\%$, the AI coordinator automatically audibles to the optimal counter (e.g. Run Blitz vs Inside Zone, Tampa 2 vs Deep Crossers), granting defenders a $+20\%$ reaction acceleration buff at the snap.
- **Files to Create / Modify:**
  - `backend/app/engine/ai/coordinator_tendency_engine.py`
  - `backend/app/schemas/play_tendency.py`
  - `frontend/src/components/game/CoordinatorTendencyBadge.tsx`
- **Data Schemas:**
  ```python
  class TendencyInsight(BaseModel):
      down_distance_category: str
      dominant_concept: str
      frequency_percentage: float
      opponent_has_recognized: bool
      defensive_counter_prepared: str
  ```
- **UI/UX Flow:** When selecting a play, if user is being predictable, a discreet coach note warns: *"Warning: Opponent DC has picked up on your 1st down run tendency (72% Run). Blitz expected."*

---

### Expansion 4.4: Two-Minute Drill No-Huddle Clock Control Matrix
- **Conceptual Rationale:** In the frantic final 2 minutes of each half, games are won or lost by clock mastery: knowing when to hurry to the line without a huddle, when to run out of bounds to stop the clock, and when to clock the ball via a spike.
- **Concrete Technical Architecture & Mechanics:**
  - Tempo Selector:
    - *No-Huddle Turbo*: Runs to line in 4 seconds; defenses cannot substitute; players suffer $+15\%$ gameday fatigue.
    - *Chew Clock*: Runs the play clock down to 3 seconds before snapping, burning up to 35 seconds of game clock.
    - *Spike Ball*: Immediate intentional grounded throw to stop the clock (costs 1 down and 1-2 seconds).
    - *Take a Knee*: Drains 40 seconds in victory formation.
- **Files to Create / Modify:**
  - `backend/app/engine/clock/tempo_controller.py`
  - `frontend/src/components/game/TwoMinuteHurryUpBar.tsx`
- **Data Schemas:**
  ```typescript
  export interface TempoState {
    activeTempo: "TURBO_NO_HUDDLE" | "NORMAL" | "CHEW_CLOCK";
    canSpike: boolean;
    canKneel: boolean;
    estimatedClockDrainPerPlay: number;
  }
  ```
- **UI/UX Flow:** Inside the final 2:00, a glowing golden HUD strip appears above the play caller with instant "Spike Ball", "Chew Clock", and "Turbo No-Huddle" toggle buttons.

---

### Expansion 4.5: Referee Challenge Flag & High-Leverage Booth Review Simulator
- **Conceptual Rationale:** When controversial plays occur near the sideline (toe-tap catches), goal line (ball breaking the plane), or disputed fumble recoveries, the head coach has the option to throw the Red Challenge Flag, triggering high-tension referee booth reviews.
- **Concrete Technical Architecture & Mechanics:**
  - Challenge Eligibility: Maximum 2 challenges per game (granted a 3rd if both previous win); must have at least 1 timeout remaining; cannot challenge inside the 2-minute warning (booth reviews only).
  - Review Probability Algorithm: Evaluates pixel coordinate variance in ball/foot placement against ground truth in `trajectory_engine.py`.
  - Reversal Outcome: Overturn grants successful call; upholding call costs the team 1 timeout.
- **Files to Create / Modify:**
  - `backend/app/engine/referee/challenge_review_engine.py`
  - `backend/app/schemas/referee_challenge.py`
  - `frontend/src/components/game/ChallengePromptModal.tsx`
  - `frontend/src/components/game/BoothReplayScrubber.tsx`
- **Data Schemas:**
  ```python
  class ChallengeReviewResult(BaseModel):
      game_id: int
      play_id: str
      play_description: str
      initial_call: str
      final_ruling: Literal["CALL_OVERTURNED", "CALL_STANDS", "CALL_CONFIRMED"]
      referee_announcement_text: str
      timeout_lost: bool
  ```
- **UI/UX Flow:** After a close sideline catch ruled incomplete, an animated red challenge flag icon flashes on the sideline with a 5-second countdown timer: *"Throw Challenge Flag? (Costs 1 Timeout if lost)"*. Clicking triggers zoomed slow-motion camera angles and referee microphone announcement.

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026 Production Standard
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification, strict types (no `any`).
</system_context>

# REQUIREMENT 2 (R2): LOCKER ROOM & CLOSED-DOOR COUNCIL UI
## Exhaustive File Extrapolation & 5 Tangential Feature Expansions

---

## 📂 SECTION 1: CORE FILE EXTRAPOLATION FOR R2

Every individual file required to deliver the Locker Room Command Center and 3-Way Closed-Door Confrontation Modal is enumerated below with its architectural layer, explicit responsibilities, and complete data interfaces.

```
THE-NFL-SIM-V2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       └── society.py                     # [MODIFY] Add roster tension overview & incident queue endpoints
│   │   ├── schemas/
│   │   │   └── society.py                         # [MODIFY] Add TeamLockerRoomOverview & CouncilIncident models
│   │   ├── engine/
│   │   │   └── society/
│   │   │       ├── locker_room_agent.py           # [MODIFY] Multi-agent confrontation generator & state commit
│   │   │       └── society_kernel.py              # [MODIFY] Big-Six DNA tension differential equations
│   │   └── services/
│   │       └── offseason_service.py               # [MODIFY] Hook weekly society evaluation into season loop
│   └── tests/
│       └── unit/
│           ├── test_locker_room_confrontation.py  # [NEW] Unit tests for 3-way council dialogue & actions
│           └── test_psychological_dna_radar.py    # [NEW] Unit tests for Big-Six math and bounds
└── frontend/
    └── src/
        ├── types/
        │   └── society.ts                         # [MODIFY] Add TeamOverview, TensionHotspot, DialogueBubble types
        ├── services/
        │   └── societyApi.ts                      # [NEW] REST API client for society & locker room endpoints
        ├── store/
        │   └── useSocietyStore.ts                 # [NEW] Zustand state store for team tension & active incident
        ├── components/
        │   └── society/
        │       ├── LockerRoomHub.tsx              # [NEW] Main locker room tab in Front Office
        │       ├── ChemistryBarometer.tsx         # [NEW] Team chemistry grade (A+ to F) & tension meter
        │       ├── GrievanceHeatmapGrid.tsx       # [NEW] Roster grid color-coded by tension status
        │       ├── PsychologicalHexagon.tsx       # [NEW] SVG radar chart displaying Big-Six traits
        │       ├── ClosedDoorCouncilModal.tsx     # [NEW] Cinematic 3-way confrontation dialogue modal
        │       ├── ConfrontationDialogueView.tsx  # [NEW] Sequenced animated speech bubbles with role icons
        │       ├── GMDecisionMatrix.tsx           # [NEW] Action option cards with projected consequence tags
        │       └── Society.module.css             # [NEW] Neon-ambient locker room dark theme styling
        ├── pages/
        │   └── FrontOffice.tsx                    # [MODIFY] Mount LockerRoomHub tab in Front Office navigation
        └── e2e/
            └── locker-room-council.spec.ts        # [NEW] Playwright E2E test for grievance confrontation flow
```

---

### Detailed File Specifications (R2 Core)

#### 1. `backend/app/schemas/society.py`
- **Purpose**: Strict validation schemas for locker room overviews, incident tickets, and decision consequences.
```python
from typing import List, Optional, Dict, Literal, Any
from pydantic import BaseModel, Field, ConfigDict

class PlayerTensionSummary(BaseModel):
    player_id: int
    full_name: str
    position: str
    overall_rating: number = Field(ge=50, le=99)
    current_tension: float = Field(ge=0.0, le=100.0)
    tension_status: Literal["CALM", "SIMMERING", "BOILING"]
    primary_driver: str  # e.g. "Low Target Share", "Bench Frustration", "Expiring Deal"
    ego: int
    greed: int
    loyalty: int

class TeamLockerRoomOverview(BaseModel):
    team_id: int
    overall_chemistry_score: float = Field(ge=0.0, le=100.0)
    chemistry_grade: Literal["A+", "A", "B", "C", "D", "F"]
    active_incidents_count: int
    boiling_players_count: int
    roster_tensions: List[PlayerTensionSummary]
    leadership_core: List[Dict[str, Any]]

class CouncilIncidentTicket(BaseModel):
    incident_id: str
    week: int
    team_id: int
    star_player_id: int
    captain_id: int
    head_coach_name: str
    trigger_tension: float
    headline: str
    dialogue_transcript: List[Dict[str, str]]
    action_options: List[Dict[str, str]]
    resolved: bool = False
```

#### 2. `frontend/src/types/society.ts`
- **Purpose**: Frontend TypeScript definitions for psychological DNA, dialogues, and resolution consequences.
```typescript
export interface PsychologicalDNA {
  ego: number;
  greed: number;
  loyalty: number;
  resilience: number;
  paranoia: number;
  professionalism: number;
}

export interface PlayerTensionCard {
  playerId: number;
  name: string;
  position: string;
  overallRating: number;
  currentTension: number;
  status: "CALM" | "SIMMERING" | "BOILING";
  primaryDriver: string;
  traits: string[];
}

export interface LockerRoomDialogueTurn {
  speakerName: string;
  speakerRole: "disgruntled_star" | "team_captain" | "head_coach" | "position_coach";
  speakerId?: number;
  text: string;
  emotion: "ANGRY" | "FIRM" | "CONCILIATORY" | "DEFIANT";
}

export interface GMResolutionChoice {
  id: "promise_targets" | "bench_player" | "address_team" | "explore_trade" | "fine_conduct";
  label: string;
  description: string;
  starMoraleDelta: number;
  coachTrustDelta: number;
  chemistryDelta: number;
  tradeDemandRisk: number; // 0-100%
}
```

---

## 🚀 SECTION 2: FIVE TANGENTIALLY RELATED FEATURE EXPANSIONS (R2)

### Expansion 2.1: Anonymous Press Leaks & Social Media Drama Feed ("Gridiron Insider")
- **Conceptual Rationale:** When NFL locker room tension boils over, players or agents rarely stay silent; they leak stories to national reporters (e.g. Adam Schefter, Ian Rapoport) or post cryptic messages on social media. This creates external pressure from the fanbase and ownership.
- **Concrete Technical Architecture & Mechanics:**
  - When an unresolved grievance reaches Tension $\ge 80.0$, a probabilistic roll ($P = \text{Paranoia} \times 0.01$) triggers an **Anonymous Press Leak**.
  - Creates a simulated tweet/insider report in the league news feed (`backend/app/api/endpoints/news.py`).
  - Fanbase Approval Delta ($-5\%$ to $-15\%$) and Owner Patience penalty.
- **Files to Create / Modify:**
  - `backend/app/engine/society/press_leak_generator.py`
  - `backend/app/schemas/press_leak.py`
  - `frontend/src/components/society/GridironInsiderTicker.tsx`
  - `frontend/src/components/society/SocialMediaLeakModal.tsx`
- **Data Schemas:**
  ```python
  class PressLeak(BaseModel):
      id: str
      source_player_id: int
      reporter_name: str  # e.g. "Adam Schefter"
      tweet_content: str
      leak_severity: Literal["MINOR_RUMOR", "ACTIVE_DISPUTE", "TRADE_DEMAND"]
      fan_sentiment_impact: int
      owner_pressure_delta: int
  ```
- **UI/UX Flow:** A simulated social media ticker bar slides into the Front Office with a glowing verified badge: *"Sources tell ESPN that star WR has officially requested a trade following heated sideline dispute with coaching staff."*

---

### Expansion 2.2: Positional Group Cliques & Leadership Mentorship Tree
- **Conceptual Rationale:** Football teams are collections of sub-tribes (the Offensive Line brotherhood, the Secondary "No Fly Zone", the Quarterback room). When leaders mentor younger players, rookies develop faster and absorb playbook mastery. Conversely, toxic veteran cliques can corrupt young talent.
- **Concrete Technical Architecture & Mechanics:**
  - Positional Chemistry Score computed across units (e.g., OL Unit Chemistry, DB Unit Chemistry).
  - Mentorship Linkage: Players with Professionalism $\ge 80$ can be assigned as "Mentors" to rookies at their position, accelerating rookie XP growth by $+25\%$ while buffering against rookie panic/fatigue.
  - Toxic Clique Hazard: If two starters at a position have low loyalty ($< 35$) and high paranoia ($> 75$), they form a toxic faction that resists coaching adjustments.
- **Files to Create / Modify:**
  - `backend/app/engine/society/position_cliques.py`
  - `backend/app/schemas/mentorship.py`
  - `frontend/src/components/society/MentorshipAssignmentModal.tsx`
  - `frontend/src/components/society/PositionalChemistryMatrix.tsx`
- **Data Schemas:**
  ```typescript
  export interface MentorshipPairing {
    mentorId: number;
    menteeId: number;
    position: string;
    xpBonusMultiplier: number;
    tensionShieldRating: number;
  }
  ```
- **UI/UX Flow:** In `LockerRoomHub.tsx`, a "Mentorship & Cliques" tab lets the GM drag and drop veteran captains onto promising rookies to forge formal leadership bonds.

---

### Expansion 2.3: Captain's Council Weekly Briefing & Locker Room Vote
- **Conceptual Rationale:** Prior to the regular season, NFL players hold a secret ballot to elect team captains (Offense, Defense, Special Teams). Every Tuesday during game planning, the captains meet with the Head Coach and GM to deliver a candid "Pulse of the Locker Room" debrief.
- **Concrete Technical Architecture & Mechanics:**
  - Preseason Training Camp Captain Vote: Players vote based on peer `professionalism` and `resilience` scores.
  - Weekly Captain's Debrief: Prior to game week simulation, the captains deliver a 3-bullet briefing highlighting fatigue concerns, scheme confusion, or simmering peer disputes.
  - Actionable Coach Directives: The user can adopt a captain recommendation (e.g., "Shorten Wednesday padded practice") granting $+10$ team energy at the cost of $-5\%$ game prep sharpness.
- **Files to Create / Modify:**
  - `backend/app/services/society/captain_election_service.py`
  - `backend/app/schemas/captain_briefing.py`
  - `frontend/src/components/society/CaptainBriefingCard.tsx`
  - `frontend/src/components/society/CaptainElectionModal.tsx`
- **Data Schemas:**
  ```python
  class CaptainWeeklyBriefing(BaseModel):
      team_id: int
      week: int
      offensive_captain_id: int
      defensive_captain_id: int
      locker_room_mood_summary: str
      top_concern: str
      recommended_practice_adjustment: str
  ```
- **UI/UX Flow:** A notification banner at the beginning of each sim week: *"Team Captains have requested a 5-minute meeting"*. Clicking opens a tactical briefing card with 1-click practice schedule toggles.

---

### Expansion 2.4: Owner Confidence Barometer & Coaching Hot Seat
- **Conceptual Rationale:** Locker room chaos does not occur in a vacuum. Franchise owners demand a return on investment and a disciplined organization. Sustained locker room drama coupled with losing records lands head coaches on the "Hot Seat", triggering owner intervention and coordinator firing mandates.
- **Concrete Technical Architecture & Mechanics:**
  - Owner Confidence Score ($0-100$):
    $$\text{OwnerConfidence} = w_w \cdot \text{WinPct} + w_c \cdot \text{CapHealth} + w_m \cdot \text{LockerRoomHarmony}$$
  - Hot Seat Triggers: When Owner Confidence drops below $35.0$, the owner schedules an emergency summons with the GM demanding the firing of an unpopular coordinator or a change at starting quarterback.
- **Files to Create / Modify:**
  - `backend/app/engine/society/owner_confidence_engine.py`
  - `backend/app/schemas/owner_relations.py`
  - `frontend/src/components/society/OwnerConfidenceGauge.tsx`
  - `frontend/src/components/society/OwnerUltimatumModal.tsx`
- **Data Schemas:**
  ```python
  class OwnerUltimatum(BaseModel):
      owner_name: str
      confidence_score: float
      is_hot_seat: bool
      mandate_type: Literal["FIRE_OFFENSIVE_COORDINATOR", "BENCH_STARTING_QB", "WIN_NEXT_GAME"]
      deadline_week: int
      penalty_on_failure: str
  ```
- **UI/UX Flow:** The Front Office displays a discreet "Ownership Status" card with a glowing amber/red badge: *"Hot Seat Warning: Owner demands decisive action regarding locker room discipline."*

---

### Expansion 2.5: Contract Renegotiation Holdout & "Hold-In" Simulator
- **Conceptual Rationale:** When star players with high `greed` outperform their contracts with 1-2 years remaining, they initiate training camp holdouts (skipping mandatory camp) or "hold-ins" (attending meetings but refusing to practice due to minor "tightness").
- **Concrete Technical Architecture & Mechanics:**
  - Holdout Eligibility: Player with $\text{OVR} \ge 86$, $AAV \le 60\%$ of current market value, and $\text{Greed} \ge 75$.
  - Daily Fines ($CBA standard \$50,000/day during camp).
  - Preseason Rust & Chemistry Decay: Holdout players suffer $-10\%$ agility and $-15\%$ play familiarity upon eventual return.
  - Holdout Resolution Workbench: Fast-track extension offer, restructure signing bonus, or call the player's bluff with daily fines.
- **Files to Create / Modify:**
  - `backend/app/engine/society/holdout_service.py`
  - `backend/app/schemas/holdout.py`
  - `frontend/src/components/society/HoldoutResolutionModal.tsx`
- **Data Schemas:**
  ```typescript
  export interface HoldoutState {
    playerId: number;
    daysHeldOut: number;
    accumulatedFines: number;
    demandedAav: number;
    holdoutType: "FULL_HOLDOUT" | "HOLD_IN";
    teamChemistryPenalty: number;
  }
  ```
- **UI/UX Flow:** In August preseason sim, an urgent popup alerts the GM: *"Star Edge Rusher has failed to report to Saint Vincent College for mandatory training camp"*.

---

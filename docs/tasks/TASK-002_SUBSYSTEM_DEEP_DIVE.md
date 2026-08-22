<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: EXPAND_SIMULATION_DEPTH_SUBSYSTEMS

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Professional sports simulation franchises (Football Manager, Out of the Park Baseball, Crusader Kings III, Madden Dynasty Mode) historically oscillate between shallow surface-level minigames and opaque statistical spreadsheets. Real NFL front offices operate through decentralized organizational departments: an intelligence-gathering scouting department prone to cognitive biases, a pedagogical coaching staff with scheme philosophy trees, and an orthopedic medical department balancing risk-weighted trauma recovery against competitive windows.
- **Related Ideas:** 
  1. *Bayesian Scouting & Dynamic Draft AI:* Bradley-Terry paired comparison models for prospect valuation, modified by Jimmy Johnson / Fitzgerald-Spielberger trade value charts with real-time positional scarcity multipliers.
  2. *Skill-Tree & Staff Chemistry DAGs:* Directed Acyclic Graphs (DAGs) representing hierarchical skill trees (HC, OC, DC, Position Coaches) with scheme alignment bonuses (e.g. West Coast + Zone Blocking synergy).
  3. *Cox Proportional Hazards & Medical Triage:* Survival analysis modeling of soft-tissue and structural ligament degradation under acute play load, with non-linear rehab risk/benefit curves (PRP vs. Arthroscopy vs. Cortisone stabilization).
- **Future Potential:** Extensibility to real-time multiplayer co-op front offices, neural network play-calling synthesis, and micro-wear kinematic tracking synchronized across multi-season dynasty saves.
- **Constraints:** 
  - Backend execution latency < 50ms for draft pick resolution and coaching bonus aggregation.
  - Zero `any` types in TypeScript interfaces; Pydantic V2 schemas on backend.
  - 100% deterministic state transitions across SQLite / PostgreSQL persistency layers.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Implement discrete independent feature modules for each subsystem: a static draft board with randomized scout errors, a simple linear talent tree with point purchases for coaches, and a 3-button modal for medical treatment (Rest, Surgery, Play).

### Powerful Antithesis
- **Draft AI Failure Mode:** Static boards with randomized noise lead to absurd AI draft picks (e.g., a team with Patrick Mahomes drafting three 1st-round QBs in a row) because the AI lacks situational roster-urgency models and trade-up/down dynamic game theory.
- **Coaching Tree Failure Mode:** Isolated point spending turns into an uninspired linear grind with "one optimal build" if bonuses are flat numerical modifiers devoid of scheme synergy and staff turnover risks (coordinators getting poached for HC jobs).
- **Medical Triage Failure Mode:** If treatment choice is a pure math check (Surgery = 4 wks, Rest = 6 wks), players will always pick the faster option unless non-linear complication risks, long-term attribute degradation, and player pain tolerance (Toughness / Ragknow traits) make the decision agonizingly contextual.

### The Superior Synthesis
Architect an interconnected triad of organizational intelligence:
1. **Dynamic Draft AI & Scouting Fog-of-War Engine:** 4 distinct scouting lenses (National Consensus, Regional Scout Bias, Analytics Department, Film Grader) with dynamic AI war room draft boards that react to positional runs, tier drops, and trade-up leverage.
2. **Dynasty Coaching Staff Ecosystem:** 3-branch skill trees (Tactical Playbook Mastery, Player Development Whisperer, Culture & Morale) with staff alignment chemistry multipliers and coordinator poaching logic.
3. **Trauma Bio-Matrix & Orthopedic Triage Protocols:** 7-zone anatomical wear tracking with Cox hazard re-injury curves, surgical complication dice-rolls, and PRP regenerative treatment paths influenced by player age and developmental traits.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend Framework:** FastAPI (Python 3.12+) with Pydantic V2 and SQLAlchemy 2.0.
- **Frontend Framework:** React 19 / Vite 7 with TypeScript strict mode, Tailwind CSS v4, Lucide Icons, and Framer Motion.
- **State Management & Communication:** Zustand stores with optimistic UI updates and resilient REST / WebSocket channels.

### 2. The Data Schema (Pre-Generation)

#### Backend Schemas (`backend/app/schemas/deep_dive.py` & `/services/`)
```python
class ScoutBiasLens(str, Enum):
    CONSENSUS = "CONSENSUS"
    FILM_TRADITIONALIST = "FILM_TRADITIONALIST"
    ANALYTICS_METRICS = "ANALYTICS_METRICS"
    REGIONAL_SCOUT = "REGIONAL_SCOUT"

class ProspectScoutingGrade(BaseModel):
    prospect_id: int
    true_ovr: int
    consensus_ovr: int
    scout_ovr: int
    analytics_ovr: int
    film_grade: str # A+, A, B, etc.
    s2_cognition_score: int # 0-100
    athletic_tier: str # Elite, Great, Good, Sub-par
    boom_bust_probability: float # 0.0 - 1.0

class CoachingSkillNode(BaseModel):
    id: str
    name: str
    tree: str # "SCHEME_TACTICS" | "DEVELOPMENT" | "PROGRAM_CULTURE"
    tier: int # 1, 2, 3, 4 (Mastery)
    unlocked: bool
    sp_cost: int
    bonus_description: str
    prerequisites: List[str]

class MedicalTriageDecision(BaseModel):
    player_id: int
    zone_key: str # "head" | "neck" | "torso" | "leftArm" | "rightArm" | "leftLeg" | "rightLeg"
    chosen_protocol: str # "REST" | "PRP_THERAPY" | "ARTHROSCOPIC_SURGERY" | "RECONSTRUCTIVE_SURGERY" | "CORTISONE_STABILIZATION"
    current_integrity: float
    projected_recovery_weeks: int
    complication_risk_pct: float
    re_injury_hazard_multiplier: float
    stat_suppression_pct: float
```

#### Frontend TypeScript Contracts (`frontend/src/types/deepDive.ts`)
```typescript
export type ScoutLens = 'CONSENSUS' | 'FILM' | 'ANALYTICS' | 'SCOUT';

export interface ProspectIntelligence {
  id: number;
  name: string;
  position: string;
  college: string;
  consensusOvr: number;
  perceivedOvr: Record<ScoutLens, number>;
  s2Score: number;
  gpsSpeedMph: number;
  bustFactor: number;
  schemeFitPercentage: number;
  medicalGrade: 'PASS' | 'CONCERN' | 'FAIL';
}

export interface CoachingTreeNode {
  id: string;
  name: string;
  branch: 'SCHEME' | 'DEV' | 'CULTURE';
  tier: number;
  unlocked: boolean;
  cost: number;
  bonusText: string;
  dependencies: string[];
}

export interface MedicalProtocolOption {
  protocol: 'REST' | 'PRP_THERAPY' | 'SURGERY_EXPEDITED' | 'CONSERVATIVE_RECON' | 'FIELD_STABILIZATION';
  name: string;
  weeksEstimate: number;
  complicationRisk: number;
  integrityRestoreTarget: number;
  description: string;
  dangerFlag?: string;
}
```

### 3. Step-by-Step Execution

- [ ] **Step 1: Scaffolding.**
  - `backend/app/services/draft/scouting_lens_service.py`
  - `backend/app/services/coaching/coaching_dynasty_service.py`
  - `backend/app/services/medical/orthopedic_triage_service.py`
  - `frontend/src/components/offseason/ScoutIntelligenceLens.tsx`
  - `frontend/src/components/coaching/CoachingDynastyTree.tsx`
  - `frontend/src/components/medical/OrthopedicTriageModal.tsx`
- [ ] **Step 2: Core Logic & Probabilistic Equations.**
  - Implement dynamic draft board trade-up pressure formula: P_trade = Urgency_pos * (1 - PickRemaining_tier).
  - Implement coaching synergy calculation combining HC + OC/DC scheme congruence.
  - Implement Cox hazard re-injury calculation: lambda(t) = lambda0(t) * exp(beta1 * MicroWear - beta2 * Toughness).
- [ ] **Step 3: Interface & Visual Immersion.**
  - Glassmorphic scout lens toggle (Consensus vs Film vs Analytics vs Scout view).
  - Interactive connected SVG tree with glowing unlock animations and staff synergy gauges.
  - Comprehensive orthopedic triage modal with PRP injections and surgical complication risk meters.

### 4. Edge Cases & Error Handling

- [Case A: Player with 0% Zone Integrity & Multiple Compound Injuries] -> Automatic surgical consultation prompt with career-threatening warning dialog.
- [Case B: AI War Room with No 1st Round Picks] -> Graceful fallthrough to trade-down baiting and 2nd-day diamond-in-the-rough scouting filters.
- [Case C: Fired Coordinator mid-season] -> Dynamic staff synergy recalculation with 2-week transitional familiarization penalty.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Strict TypeScript compilation with 0 `any` types.
- [ ] **Security:** Input validation with Pydantic V2 preventing unauthorized stat mutations.
- [ ] **Performance:** Sub-millisecond calculation for 256 draft prospect evaluations and 32 coaching staff synergies.
- [ ] **Self-Critique:** Verified edge-case robustness against rapid draft clock countdowns, multi-injury compounding, and coordinator churn.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Review and approve the execution of Step 1 (Scaffolding & Models), Step 2 (Core Logic), and Step 3 (Interactive Glassmorphic UI Components).
</baton_handoff>

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026 Production Standard
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification, strict types (no `any`).
</system_context>

# REQUIREMENT 3 (R3): MEDICAL CENTER LIVE ROSTER & SURGICAL TRIAGE INTEGRATION
## Exhaustive File Extrapolation & 5 Tangential Feature Expansions

---

## 📂 SECTION 1: CORE FILE EXTRAPOLATION FOR R3

Every individual file required to wire the live franchise injured roster into `MedicalCenter.tsx` and execute 7-zone surgical triage persistence is enumerated below with its architectural layer, explicit responsibilities, and complete data interfaces.

```
THE-NFL-SIM-V2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       └── medical.py                     # [MODIFY] Add live roster wear queries & triage persistence
│   │   ├── schemas/
│   │   │   └── deep_dive.py                       # [MODIFY] Add OrthopedicTriageRequest/Response models
│   │   ├── services/
│   │   │   ├── medical_service.py                 # [MODIFY] Connect 7-zone BodyHealth updates to injury lifecycle
│   │   │   └── medical/
│   │   │       └── orthopedic_triage_service.py   # [MODIFY] Implement complication probability rolls & DB writes
│   │   └── models/
│   │       ├── player.py                          # [MODIFY] Verify InjuryStatus enum & weeks_to_recovery columns
│   │       └── body_health.py                     # [MODIFY] Add 7-zone specific recovery rate modifiers
│   └── tests/
│       └── unit/
│           ├── test_medical_live_roster.py        # [NEW] Unit tests verifying real team injury ingestion
│           └── test_orthopedic_triage_db.py       # [NEW] Unit tests verifying DB persistence of surgical decisions
└── frontend/
    └── src/
        ├── types/
        │   └── medical.ts                         # [MODIFY] Add 7-zone BodyMapHealthData & live InjuredPlayer types
        ├── services/
        │   └── medicalApi.ts                      # [MODIFY] Add getTeamInjuries & applyOrthopedicTriage methods
        ├── store/
        │   └── useMedicalStore.ts                 # [NEW] Zustand store managing active injured player selection & triage state
        ├── components/
        │   └── medical/
        │       ├── BodyMap.tsx                    # [MODIFY] Connect SVG click events to zone triage modal triggers
        │       ├── OrthopedicTriageModal.tsx      # [MODIFY] Wire protocol submission to backend API & error handling
        │       ├── TreatmentModal.tsx             # [MODIFY] Wire Rest / Surgery / Play Through decisions to API
        │       ├── PreventiveMaintenanceCard.tsx  # [NEW] Starter fatigue & wear monitor when 0 players injured
        │       ├── BiometricRecoveryTimeline.tsx  # [NEW] Interactive slider showing surgery vs conservative recovery curves
        │       └── MedicalCenter.css              # [MODIFY] Refine neon anatomical scanning visuals
        ├── pages/
        │   └── MedicalCenter.tsx                  # [MODIFY] Remove all mock arrays; dynamically bind to useTeamStore
        └── e2e/
            └── medical-triage-live.spec.ts        # [NEW] Playwright E2E test for live injury triage & DB mutation
```

---

### Detailed File Specifications (R3 Core)

#### 1. `backend/app/schemas/deep_dive.py`
- **Purpose**: Strict validation schemas for orthopedic triage requests, body zone damages, and surgical outcomes.
```python
from typing import Optional, Dict, Literal
from pydantic import BaseModel, Field

class OrthopedicTriageRequest(BaseModel):
    player_id: int
    zone_key: Literal["head", "neck", "torso", "rightArm", "leftArm", "rightLeg", "leftLeg"]
    protocol: Literal["CONSERVATIVE_REST", "ARTHROSCOPIC_SURGERY", "PRP_INJECTION", "PLAY_THROUGH_BRACE"]

class OrthopedicTriageResponse(BaseModel):
    player_id: int
    zone_key: str
    previous_recovery_weeks: int
    new_recovery_weeks: int
    complication_occurred: bool
    complication_weeks_added: int = 0
    new_zone_health: float
    new_injury_status: str
    re_injury_recurrence_risk: float
    performance_penalties: Dict[str, int]
    clinical_narrative: str
```

#### 2. `frontend/src/types/medical.ts`
- **Purpose**: Frontend TypeScript interfaces for live roster injuries and 7-zone anatomical health matrices.
```typescript
export type BodyZoneKey = "head" | "neck" | "torso" | "rightArm" | "leftArm" | "rightLeg" | "leftLeg";

export interface LiveInjuredPlayer {
  playerId: number;
  firstName: string;
  lastName: string;
  position: string;
  injuryType: string;
  injuryStatus: "ACTIVE" | "QUESTIONABLE" | "DOUBTFUL" | "OUT" | "IR";
  severity: number; // 1-10
  weeksRemaining: number;
  affectedZone: BodyZoneKey;
  surgeryRecommended: boolean;
  complicationRisk: number; // 0.0 - 1.0
}

export interface BodyMapHealthData {
  head: number;
  neck: number;
  torso: number;
  rightArm: number;
  leftArm: number;
  rightLeg: number;
  leftLeg: number;
  generalWear: number;
}
```

---

## 🚀 SECTION 2: FIVE TANGENTIALLY RELATED FEATURE EXPANSIONS (R3)

### Expansion 3.1: Regenerative Orthobiologics (PRP & Stem Cell) vs Arthroscopy Studio
- **Conceptual Rationale:** Modern elite sports medicine frequently uses Platelet-Rich Plasma (PRP) therapy and autologous stem cell injections as non-surgical alternatives to arthroscopic surgery, trading a slightly longer recovery window for preservation of native tendon and ligament elasticity.
- **Concrete Technical Architecture & Mechanics:**
  - Clinical Protocol Comparison Matrix:
    - *Arthroscopic Surgery*: $-40\%$ recovery time, $+12\%$ surgical complication risk, $+5\%$ long-term joint stiffness.
    - *PRP / Orthobiologic Therapy*: $-15\%$ recovery time, $0\%$ surgical risk, $+10\%$ long-term cartilage resilience, requires 2-week total immobilization.
    - *Cortisone Shielding*: Zero time missed, $-15\%$ player fatigue, $+35\%$ catastrophic rupture risk if hit in gameday action.
- **Files to Create / Modify:**
  - `backend/app/services/medical/orthobiologics_service.py`
  - `backend/app/schemas/orthobiologics.py`
  - `frontend/src/components/medical/BiologicsProtocolSelector.tsx`
- **Data Schemas:**
  ```python
  class OrthobiologicDecision(BaseModel):
      player_id: int
      treatment_type: Literal["PRP_INJECTION", "CELLULAR_THERAPY", "ARTHROSCOPY", "CORTISONE_BLOCK"]
      recovery_days: int
      cartilage_preservation_score: float
      secondary_rupture_risk: float
  ```
- **UI/UX Flow:** Inside `OrthopedicTriageModal.tsx`, clicking on an injured knee opens a "Therapy Branch" toggle comparing MRI scans of Arthroscopy vs PRP therapy with recovery curve diagrams.

---

### Expansion 3.2: Turf vs Grass Biomechanical Load & Non-Contact Injury Risk Engine
- **Conceptual Rationale:** In the NFL, field surface quality is a massive health debate. Slit-film artificial turf creates extreme rotational traction, dramatically elevating non-contact ACL and Achilles tears compared to hybrid Bermuda grass during high-torque cuts.
- **Concrete Technical Architecture & Mechanics:**
  - Stadium Surface Lookup: Each NFL stadium categorized by surface type (`NATURAL_GRASS`, `HYBRID_GRASS`, `FIELD_TURF`, `SLIT_FILM_TURF`).
  - Biomechanical Load Factor ($\beta$):
    $$\text{TearRisk}_{\text{non-contact}} = \text{BaseRisk} \times \beta_{\text{surface}} \times \left(1.0 + \frac{\text{Fatigue} + \text{GeneralWear}}{50.0}\right)$$
    Where $\beta_{\text{grass}} = 1.0$, $\beta_{\text{turf}} = 1.45$.
- **Files to Create / Modify:**
  - `backend/app/engine/physics/surface_injury_risk.py`
  - `backend/app/schemas/surface_biometrics.py`
  - `frontend/src/components/medical/TurfRiskAlertBanner.tsx`
- **Data Schemas:**
  ```typescript
  export interface SurfaceInjuryRiskForecast {
    stadiumName: string;
    surfaceType: "NATURAL_GRASS" | "SYNTHETIC_TURF";
    rotationalTractionIndex: number;
    elevatedAclRiskPercentage: number;
    recommendedTapeProtocol: "STANDARD" | "HIGH_ANKLE_SPAT" | "BRACED";
  }
  ```
- **UI/UX Flow:** Before away games on turf venues (e.g. MetLife Stadium), the Medical Center displays a warning card: *"Elevated Lower Extremity Hazard: High-torque turf increases non-contact strain by +45%."*

---

### Expansion 3.3: Injured Reserve (IR) Designation to Return & Practice Window Tracker
- **Conceptual Rationale:** Managing the NFL Injured Reserve (IR) list requires meticulous adherence to league rules: a team may designate a maximum of 8 players to return per season, players on IR must sit out at least 4 games, and activating a player triggers a strict 21-day practice window before they must be placed on the 53-man roster or shut down for the year.
- **Concrete Technical Architecture & Mechanics:**
  - IR Eligibility: Minimum 4-week missed game lock.
  - Season Return Quota: 8 total designations tracked per franchise.
  - 21-Day Practice Window Clock: Activating a player for practice starts a 21-day timer; failure to promote to the active roster before day 21 places the player on Season-Ending IR.
- **Files to Create / Modify:**
  - `backend/app/services/medical/ir_management_service.py`
  - `backend/app/schemas/injured_reserve.py`
  - `frontend/src/components/medical/IRManagementDrawer.tsx`
  - `frontend/src/components/medical/PracticeWindowClock.tsx`
- **Data Schemas:**
  ```python
  class IRRosterStatus(BaseModel):
      player_id: int
      games_on_ir: int
      minimum_games_required: int = 4
      eligible_for_practice_window: bool
      practice_window_days_remaining: Optional[int]
      designations_remaining_for_team: int
  ```
- **UI/UX Flow:** A dedicated "IR & Roster Exemptions" tray in the Medical Center with countdown badges showing when injured stars become eligible to open their 21-day practice return windows.

---

### Expansion 3.4: Gameday "Toradol / Pain Block" Injection Trade-Off Matrix
- **Conceptual Rationale:** During critical playoff pushes, players frequently volunteer to take pain-masking gameday injections (e.g. Toradol or localized Marcaine) to play through bruised ribs or sprained ankles, trading immediate gameday numbness for exacerbated post-game trauma and elevated re-injury risks.
- **Concrete Technical Architecture & Mechanics:**
  - Injection Protocol: Temporarily elevates player Gameday Availability from `QUESTIONABLE` to `ACTIVE`.
  - In-Game Buff: Suppresses pain penalties on speed/strength for 4 quarters.
  - Post-Game Penalty: $+40\%$ chance the injury severity increases by 1 grade, and player suffers double fatigue in the subsequent week.
- **Files to Create / Modify:**
  - `backend/app/engine/medical/pain_management.py`
  - `backend/app/schemas/pain_management.py`
  - `frontend/src/components/medical/GamedayInjectionModal.tsx`
- **Data Schemas:**
  ```typescript
  export interface GamedayPainInjection {
    playerId: number;
    medicationType: "TORADOL_INJECTION" | "LOCAL_LIDOCAINE_BLOCK" | "REST_ONLY";
    temporaryPainSuppression: boolean;
    postGameSeverityInflationRisk: number; // e.g. 0.40
    playerConsentGiven: boolean;
  }
  ```
- **UI/UX Flow:** On Gameday Live Sim screen, questionable starters show a syringe icon. Clicking it allows the GM/Coach to authorize a pain injection with explicit risk disclosures.

---

### Expansion 3.5: Career-Threatening Trauma Review Board & Medical Settlements
- **Conceptual Rationale:** When catastrophic orthopedic injuries occur (cervical spine stenosis, recurrent concussions with CTE markers, complete multiligament knee dislocations), an independent medical panel evaluates the player's viability for continued competition, potentially mandating medical retirement and triggering CBA injury settlement buyout calculations.
- **Concrete Technical Architecture & Mechanics:**
  - Career Viability Index ($0-100$): Computed when repeat concussions $\ge 3$ or neck severity $\ge 8$.
  - Mandatory Medical Retirement: If viability drops below $15.0$, independent doctors declare player medically ineligible.
  - Injury Protection Benefit & Cap Relief: Team pays CBA standard injury settlement, and remaining contract bonus liabilities receive catastrophic cap insurance relief.
- **Files to Create / Modify:**
  - `backend/app/services/medical/catastrophic_trauma_service.py`
  - `backend/app/schemas/medical_settlement.py`
  - `frontend/src/components/medical/MedicalRetirementModal.tsx`
- **Data Schemas:**
  ```python
  class MedicalReviewVerdict(BaseModel):
      player_id: int
      concussion_count: int
      medical_board_recommendation: Literal["CLEARED_FOR_CONTACT", "PROLONGED_SHUTDOWN", "MANDATORY_RETIREMENT"]
      injury_settlement_cost: int
      cap_relief_granted: int
  ```
- **UI/UX Flow:** In extreme medical cases, a solemn "Medical Review Board Verdict" dossier modal renders with physician signatures and official retirement ceremonies.

---

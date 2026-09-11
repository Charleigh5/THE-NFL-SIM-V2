<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK_012_MEDICAL_CENTER_LIVE_ROSTER_AND_SURGICAL_TRIAGE_INTEGRATION

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - In pro football, player availability is the supreme currency. Injuries are not monolithic binary states; they are complex physiological conditions distributed across distinct anatomical regions (concussions, cervical strains, pectoral tears, ACL/MCL tears, high ankle sprains).
  - In `THE-NFL-SIM-V2`, a 7-Zone Anatomical Biometrics Engine exists (`head`, `neck`, `torso`, `right_arm`, `left_arm`, `right_leg`, `left_leg`) along with an orthopedic triage backend service (`orthopedic_triage_service.py` and `medical.py`).
  - However, the frontend `MedicalCenter.tsx` is currently disconnected from the live franchise database, operating with hardcoded mock player arrays (e.g. Kyler Murray, James Conner). Furthermore, treatment decisions made in the UI modals are not persistently committed to the backend database or reflected in subsequent game simulations.

- **Related Ideas & Industry Parallels:**
  - *Military Battlefield Triage & Orthopedic Surgery Protocols*: Rapid categorization of damage severity (Minor, Moderate, Severe, Catastrophic), risk-adjusted surgical interventions, and expedited return-to-play timelines.
  - *Madden Injury Reserve & Practice Management*: Designation to Return (IR-R), questionable tag game-time decisions, and re-injury probability multipliers.
  - *Anatomical Interactive Heatmaps*: Medical diagnostic applications with interactive SVG body zones and localized wear-and-tear degradation.

- **Future Potential (2026/2027):**
  - Biomechanical joint stress tracking, platelet-rich plasma (PRP) therapy vs arthroscopy branching decisions, and permanent athletic attribute degradation from repeat surgeries.

- **Constraints:**
  - Dynamic multi-team binding: Automatically binds to the user's selected franchise via `useTeamStore`.
  - Zero mock data in production builds.
  - Full relational persistence in SQLAlchemy (`Player.injury_status`, `Player.weeks_to_recovery`, `Player.injury_recurrence_risk`, `BodyHealth`).
  - Graceful fallback for teams with zero active injuries.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Swap out the static `injuredRoster` useState array in `MedicalCenter.tsx` with a simple `useEffect` fetching `GET /api/medical/team/{teamId}/injuries`.

### Powerful Antithesis
- **Zero-Injury Crash**: If a user's franchise has zero injuries (common during Week 1 or preseason), `injuredRoster[0]` resolves to `undefined`. `BodyMap` crashes with `TypeError: Cannot read properties of undefined (reading 'head')`, destroying the user experience.
- **Dangling UI State**: When a user clicks "Surgery" or "Play Through" in `TreatmentModal.tsx` or `OrthopedicTriageModal.tsx`, the modal closes, but if the endpoint call fails or is disconnected, the DB still marks the player as OUT for 8 weeks, creating a critical desync between UI and simulation state.
- **Anatomical Disconnect**: In the mock data, clicking on an injured player showed arbitrary hardcoded body map numbers regardless of what injury the player actually suffered (e.g. an "Ankle Sprain" showing a healthy leg and damaged arm).
- **Missing Proactive Triage**: In a real NFL franchise, the medical room is not just for players already out; it monitors fatigue and general wear on active starters to prevent catastrophic non-contact injuries.

### The Superior Synthesis
Architect a **Fully Integrated Live Medical Triage Suite**:
1. **Dynamic Roster Ingestion with Active Team Binding**:
   - Bind `MedicalCenter.tsx` to `useTeamStore.getState().userTeamId`.
   - Query live injured players via `GET /api/medical/team/{teamId}/injuries`.
   - When injuries are zero, gracefully transition to the **Preventive Biometrics & Maintenance Mode**, loading starters with high wear (`general_wear > 25%`) for proactive recovery sessions.
2. **Deterministic Anatomical Damage Mapping**:
   - Automatically derive the 7-zone `BodyMapHealthData` directly from the player's specific injury type, severity, and `BodyHealth` record:
     $$\text{ZoneHealth} = \max(10, 100 - (\text{Severity} \times 18))$$
3. **Two-Way Database Persistence Loop**:
   - Wire `TreatmentModal` and `OrthopedicTriageModal` directly to `POST /api/medical/treatment` and `POST /api/medical/orthopedic/triage`.
   - Update `Player.injury_status` (`QUESTIONABLE`, `DOUBTFUL`, `OUT`, `IR`), `weeks_to_recovery`, and performance penalties directly in the database.
   - Trigger instant cache re-validation, sound effects (`soundEffects.playWhistle()`), and notification banners displaying updated recovery timelines.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend:** FastAPI, SQLAlchemy 2.0, `backend/app/api/endpoints/medical.py`, `backend/app/services/medical_service.py`.
- **Frontend:** React 19, TypeScript, `BodyMap.tsx`, `FatigueMonitor.tsx`, `GenesisBiometricCard.tsx`, `TreatmentModal.tsx`, `OrthopedicTriageModal.tsx`.
- **State Management:** `useMedicalStore.ts` hooked into `useTeamStore.ts`.

### 2. The Data Schema (Pre-Generation)

#### Backend Schemas (`backend/app/api/endpoints/medical.py` & `schemas/deep_dive.py`)

```python
class OrthopedicTriageRequest(BaseModel):
    player_id: int
    zone_key: str  # "head", "neck", "torso", "rightArm", "leftArm", "rightLeg", "leftLeg"
    protocol: str  # "CONSERVATIVE_REST", "ARTHROSCOPIC_SURGERY", "PRP_INJECTION", "PLAY_THROUGH_BRACE"

class OrthopedicTriageResponse(BaseModel):
    player_id: int
    zone_key: str
    new_zone_health: float
    new_injury_status: str
    new_recovery_weeks: int
    complication_occurred: bool
    performance_penalties: Dict[str, int]
    triage_notes: str
```

#### Frontend TypeScript Interfaces (`frontend/src/types/medical.ts`)

```typescript
export interface InjuredPlayer {
  player_id: number;
  first_name: string;
  last_name: string;
  position: string;
  injury_type: string;
  injury_status: "ACTIVE" | "QUESTIONABLE" | "DOUBTFUL" | "OUT" | "IR";
  severity: number;
  weeks_remaining: number;
  body_part: "head" | "neck" | "torso" | "rightArm" | "leftArm" | "rightLeg" | "leftLeg";
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

### 3. Step-by-Step Execution

#### Step 1: Scaffolding
- [ ] Add `applyOrthopedicTriage` and `getTeamInjuries` to `frontend/src/services/medicalApi.ts`.
- [ ] Implement `frontend/src/store/useMedicalStore.ts` to manage active player selection, body map state, and live mutation caching.
- [ ] Verify endpoint routes in `backend/app/api/endpoints/medical.py`.

#### Step 2: Core Logic Implementation
- [ ] **Subtask 2.1: Live Injury Roster Aggregator**
  - Ensure `GET /api/medical/team/{team_id}/injuries` correctly returns body zone mapping based on `injury_type` string parsing (e.g. "Knee" $\rightarrow$ `rightLeg`/`leftLeg`).
- [ ] **Subtask 2.2: Orthopedic Triage DB Mutation Pipeline**
  - Implement `POST /api/medical/orthopedic/triage` in `medical.py` executing:
    - Prorated recovery weeks calculation.
    - Complication risk roll ($0.05 + 0.01 \times \text{severity} + \text{age\_risk}$).
    - Direct write to `BodyHealth` table updating zone health.
    - Direct write to `Player` table updating `injury_status` and `weeks_to_recovery`.
- [ ] **Subtask 2.3: Preventative Maintenance Starters Query**
  - Add `GET /api/medical/team/{team_id}/wear-overview` returning active healthy players with highest general wear ($> 20\%$) for proactive triage.

#### Step 3: Interface & Experience
- [ ] **Subtask 3.1: Clean Roster Ingestion in `MedicalCenter.tsx`**
  - Remove all hardcoded mock arrays (`Kyler Murray`, `James Conner`).
  - Hook into `useTeamStore` to dynamically fetch active team injuries on component mount or franchise change.
- [ ] **Subtask 3.2: Zero-Injury Preventive Maintenance View**
  - Render an inspiring "All Players Cleared for Game Day" banner when injury count is 0, switching the body map to display starter wear/fatigue.
- [ ] **Subtask 3.3: Interactive 7-Zone Click-to-Triage Flow**
  - Connect SVG clicks on `BodyMap.tsx` zones to open `OrthopedicTriageModal.tsx` filtered by the clicked zone.
- [ ] **Subtask 3.4: Treatment Modal DB Action Dispatch**
  - Wire `handleApplyTreatment` and `handleTriageDecision` to call backend APIs, display optimistic loading spinners, and re-fetch updated player health data upon completion.

### 4. Edge Cases & Error Handling

- [Case A: No Injured Players on Active Roster] -> Graceful fallback to "Preventative Maintenance" mode displaying starting QB/RB fatigue without crashing.
- [Case B: Surgery Complication Triggered] -> UI displays amber warning alert: "Surgical Complication: Minor setback adds 3 weeks to recovery timeline."
- [Case C: Network Failure during Triage Submission] -> Preserves user selection, rolls back optimistic UI state, and displays retry toast.
- [Case D: Player Cleared to Active Status] -> Instantly removes player from injured queue and plays celebratory recovery audio chime.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** TypeScript clean build (`npx tsc --noEmit`); strict typed Pydantic V2 responses.
- [ ] **Security:** SQL injection protection via SQLAlchemy ORM parameters; team ID validation against authorized franchise session.
- [ ] **Performance:** Live injury load $< 50$ms; body map SVG renders at 60 FPS without layout shift.
- [ ] **Self-Critique:** Does clearing a player properly update the depth chart? Yes, player becomes eligible for active roster insertion.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Refactor `frontend/src/pages/MedicalCenter.tsx` to remove mock data and integrate `frontend/src/services/medicalApi.ts`.
</baton_handoff>

# ADR-007: Clinical Orthopedic Trauma Triage, Body Health Forecasting, and Return-to-Play Synchronization

**Status**: Accepted
**Date**: 2026-09-06
**Decision Makers**: Medical Subsystem Architect, Sports Science Specialist, QA Engineer
**Supersedes**: N/A

---

## Context

In conventional sports video games, player injuries are treated as monolithic binary timers (e.g. "Injured: 4 Weeks"), where players are completely absent until the clock runs down and then return at 100% full health. In reality, NFL sports medicine involves complex orthopedic triage trade-offs:
1. **Conservative vs. Surgical Interventions**: Medical staff and players choose between conservative non-invasive rehabilitation, autologous biologic therapies (PRP), minimally invasive scope debridement, or full anatomical reconstructive surgery.
2. **Acute Wear vs. Long-Term Joint Integrity**: Aggressive interventions may accelerate a player's return to the field for a playoff push, but degrade baseline structural joint health and increase career-ending reinjury hazard rates.
3. **Anatomical Zone Health**: Player bodies are composed of distinct musculoskeletal units (`head`, `neck`, `torso`, `right_arm`, `left_arm`, `right_leg`, `left_leg`) that degrade and recover independently.
4. **Data Contract Defects Identified**:
   - Status checks previously compared `player.injury_status != "HEALTHY"`, but the database enum defines healthy players as `InjuryStatus.ACTIVE`, causing healthy athletes to be falsely classified as injured.
   - `Player.body_health` was erroneously accessed with list indexing (`player.body_health[0]`), raising runtime TypeErrors against the 1:1 scalar relationship.
   - Triage rehabilitation forecasts were computed in the endpoint but never persisted to `player.body_health`, and immutable `InjuryEvent` audit trails were not recorded.

---

## Decision

We overhauled the medical trauma and rehabilitation subsystem across backend models, triage engines, endpoints, and frontend UI:

### 1. The 5 Clinical Orthopedic Triage Pathways
We formalized five distinct clinical medical protocols in `orthopedic_triage_service.py` and `medical.py`:

| Protocol Pathway | Clinical Mechanism | Recovery Duration Modifier | Complication Risk | Structural Integrity Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **`REST`** | Conservative biological immobilization & physical therapy | Standard (1.0x baseline) | 0% | Full 100% tissue restoration; zero long-term degradation |
| **`PRP_THERAPY`** | Platelet-rich plasma autologous biotherapy | -30% (0.70x duration) | 5% | 90-95% integrity restoration; minor biological variance |
| **`ARTHROSCOPIC_SURGERY`** | Minimally invasive scope debridement & meniscus trim | -50% (0.50x duration) | 12% | 80-85% integrity restoration; slight cartilage sacrifice |
| **`RECONSTRUCTIVE_SURGERY`** | Complete graft reconstruction (e.g. ACL, labrum) | Season shutdown (+50% to +100%) | 20% | High structural stability for multi-year career longevity |
| **`CORTISONE_STABILIZATION`** | Field joint injection & structural bracing | Immediate (0 weeks / suit up) | 25% | 2.5x hazard multiplier; permanent -10% structural health drop |

### 2. Resolution of Enum & Scalar Subscript Defects
- Standardized `InjuryStatus` verification in `backend/app/api/endpoints/medical.py` to:
  ```python
  is_injured = player.injury_status not in (InjuryStatus.ACTIVE, "ACTIVE")
  ```
- Fixed all access to `player.body_health` as a scalar object (`bh = player.body_health`) in `medical_service.py`, eliminating list subscript TypeErrors.

### 3. Triage Forecast Persistence & Immutable Audit Trail
- In `apply_player_triage_protocol`, the endpoint maps the injured zone to the corresponding `BodyPart` attribute (e.g. `right_leg_health`, `left_knee_health`) and persists `final_integrity_forecast`.
- Inserts an immutable `InjuryEvent` record storing:
  - `player_id`, `season_id`, `week`
  - `injury_name`, `body_part`, `severity`
  - `duration_weeks`, `treatment_chosen=protocol`
- Synchronizes player roster status (`QUESTIONABLE`, `OUT`, or `IR`) dynamically based on projected recovery duration.

### 4. Live Medical Center UI Integration
- Connected `frontend/src/pages/MedicalCenter.tsx` to live backend endpoints:
  - `GET /api/medical/teams/{team_id}/injuries` (filtered to active rostered injuries).
  - `GET /api/medical/players/{player_id}/triage/protocols` (loading the 5 clinical options with risks and timelines).
  - `POST /api/medical/players/{player_id}/triage/apply` (transmitting selected protocol and updating UI state).

---

## Rationale

1. **Medical Depth**: Reflects real NFL front-office medical decisions (e.g., whether to shut down a franchise QB for surgery or administer stabilizing injections for a postseason run).
2. **Long-Term Career Consequences**: Players who repeatedly play through severe joint injuries without reconstructive surgery suffer accelerated physical attribute decline in their late 20s.
3. **Data Integrity**: Enforces strict schema and enum validation across the full stack with zero type mismatches.

---

## Consequences

### Positive Consequences
- **Diagnostic Realism**: GMs and medical staff must weigh immediate playoff contention against multi-year franchise asset preservation.
- **Flawless Type Parity**: Strict Pydantic models (`InjuredPlayerResponse`, `TriageProtocolOption`, `TriageApplicationRequest`) mirror frontend TypeScript definitions with 0 `any` types.
- **Persistent State**: Joint health degradation and treatments persist across weeks and seasons in the database.

### Negative Consequences / Trade-offs
- **High Consequence for User**: Choosing cortisone stabilization or rushing players back can trigger catastrophic season-ending or career-altering secondary tears.
- **Granular Database Tracking**: Every play and weekly recovery cycle evaluates individual body zone health metrics.

---

## Alternatives Considered

1. **Simple Weekly Injury Countdown**:
   - *Description*: Count down remaining weeks automatically with no treatment choices.
   - *Reason for Rejection*: Eliminates user agency and medical realism.
2. **Random Complication Rolls with No Medical Choices**:
   - *Description*: Automatic background rolls without exposing clinical pathways.
   - *Reason for Rejection*: Lacks transparency and denies GMs strategic decision-making.

---

## Validation Criteria

- `pytest backend/tests/unit/test_medical_hud_sprint.py`: 100% pass rate across medical triage tests, enum checks, and event persistence.
- `python scripts/test_domain_boundary_pipeline.py`: Step 4 verifies high-impact physics contact seamlessly transitioning into medical triage protocols.
- `npm --prefix frontend run build`: Clean build verifying `MedicalCenter.tsx` and `OrthopedicTriageModal.tsx`.

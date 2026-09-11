# Dispatch: Worker M3 (Track 3: Physics/HUD & Medical Specialist - TASK-012 & TASK-013)

## Mandatory Context
Read the authoritative user request at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`

Read the survey findings at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_5p_2\handoff.md`

Read the project scope and interface contracts at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_5pillar\PROJECT.md`

## Working Directory
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m3_medical_hud`
Maintain your `BRIEFING.md` and `progress.md` in this directory.

## Exclusive File Ownership
You exclusively own and modify:
- `backend/app/api/endpoints/medical.py`
- `backend/app/services/medical_service.py`
- `backend/app/engine/fourth_down_calculator.py`
- `backend/app/api/endpoints/playcalling.py`
- `backend/app/schemas/playcalling.py`
- `frontend/src/pages/MedicalCenter.tsx`
- `frontend/src/components/medical/OrthopedicTriageModal.tsx`
- `frontend/src/services/medicalApi.ts`
- `frontend/src/components/game/PlayCallingHUD.tsx`
- `frontend/src/components/game/FourthDownModal.tsx`
- `frontend/src/components/game/ClockManagementBar.tsx`
- `frontend/src/pages/LiveSim.tsx`
- `backend/tests/unit/test_medical_hud_sprint.py`

DO NOT modify any other files.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Requirements
1. **Medical Backend Defect Repairs (TASK-012)**:
   - Fix `backend/app/api/endpoints/medical.py:61`: change `is_injured=player.injury_status != "HEALTHY"` to `is_injured=player.injury_status != "ACTIVE"` (or compare against `InjuryStatus.ACTIVE`).
   - Fix `backend/app/services/medical_service.py:24, 70`: `health = player.body_health[0]` -> `health = player.body_health` (scalar 1:1 relationship).
   - In `backend/app/api/endpoints/medical.py` `apply_player_triage_protocol`: ensure `final_integrity_forecast` is saved to `player.body_health` and an `InjuryEvent` record is inserted into `injury_events`.
2. **Medical Frontend Live Integration (TASK-012)**:
   - In `frontend/src/pages/MedicalCenter.tsx`: eliminate the 3 hardcoded mock players (`Kyler Murray`, etc.). Fetch live team injuries on mount and franchise change using `medicalApi.getTeamInjuries(teamId)`.
   - In `frontend/src/services/medicalApi.ts`: add `getPlayerTriageProtocols(playerId: number)` and `applyOrthopedicTriage(playerId: number, protocol: string)`.
   - In `frontend/src/components/medical/OrthopedicTriageModal.tsx`: fetch live protocols from `GET /api/medical/players/{player_id}/triage/protocols`, display the 5 clinical pathways (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`), and submit to `POST /api/medical/players/{player_id}/triage/apply`.
3. **In-Game Play-Calling HUD & Ben Baldwin 4th-Down Model (TASK-013)**:
   - In `backend/app/engine/fourth_down_calculator.py`: implement Ben Baldwin 4th-down decision modeling (Go/Punt/FG) evaluating Expected Points (EP), Win Probability (WP), and conversion odds based on distance, yardline, score difference, time remaining, and timeouts. Guarantee lookup latency strictly $< 10$ms.
   - In `backend/app/schemas/playcalling.py` & `backend/app/api/endpoints/playcalling.py`: define Pydantic schemas and expose `POST /api/playcalling/fourth-down-recommendation` and `POST /api/playcalling/call-play`.
   - In `frontend/src/components/game/`: implement `PlayCallingHUD.tsx`, `FourthDownModal.tsx`, and `ClockManagementBar.tsx`.
   - In `frontend/src/pages/LiveSim.tsx`: mount `PlayCallingHUD` and `FourthDownModal` during live simulation with play selection controls and Baldwin 4th-down recommendation cards.
4. **Verification**:
   - Write unit tests in `backend/tests/unit/test_medical_hud_sprint.py` testing the medical status fix, triage application persistence, and Baldwin 4th-down decision calculation latency (<10ms).
   - Run tests: `pytest backend/tests/unit/test_medical_hud_sprint.py backend/tests/test_60hz_physics.py`.
   - Run: `npm --prefix frontend run build` to verify 0 TypeScript errors and 0 `any` types.

Deliver your report in `handoff.md` in your working directory and notify parent.

## 2026-09-06T03:37:19Z
Read your dispatch file at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m3_medical_hud\DISPATCH.md and the authoritative request at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md.

Your working directory is:
c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m3_medical_hud

You exclusively own and modify:
- backend/app/api/endpoints/medical.py
- backend/app/services/medical_service.py
- backend/app/engine/fourth_down_calculator.py
- backend/app/api/endpoints/playcalling.py
- backend/app/schemas/playcalling.py
- frontend/src/pages/MedicalCenter.tsx
- frontend/src/components/medical/OrthopedicTriageModal.tsx
- frontend/src/services/medicalApi.ts
- frontend/src/components/game/PlayCallingHUD.tsx
- frontend/src/components/game/FourthDownModal.tsx
- frontend/src/components/game/ClockManagementBar.tsx
- frontend/src/pages/LiveSim.tsx
- backend/tests/unit/test_medical_hud_sprint.py

Implement:
1. Fix backend medical bugs: is_injured status check (InjuryStatus.ACTIVE), scalar subscript player.body_health[0], and persist triage integrity forecast and InjuryEvent.
2. Wire MedicalCenter.tsx to live backend getTeamInjuries(teamId), wire OrthopedicTriageModal.tsx to live protocols and apply triage endpoints.
3. Implement Ben Baldwin 4th-down decision modeling in backend/app/engine/fourth_down_calculator.py (<10ms execution).
4. Implement PlayCallingHUD, FourthDownModal, ClockManagementBar, and integrate into LiveSim.tsx.
5. Author and run unit tests in backend/tests/unit/test_medical_hud_sprint.py, verify backend tests and frontend build (npm --prefix frontend run build).

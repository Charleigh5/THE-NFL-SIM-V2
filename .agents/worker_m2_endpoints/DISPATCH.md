## 2026-08-24T01:16:32Z
You are the Worker for Milestone 2: Live FastAPI Endpoint Implementation & Wire-up (R2) for THE-NFL-SIM-V2.
Your working directory is: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2_endpoints`
Create your working directory if needed. Maintain `progress.md` with timestamps.

MANDATORY: You MUST read `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md` and `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md` before starting work. Also review the backend survey report at `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_be\survey_backend.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE & TASKS:
1. Backend REST Endpoint Implementation:
   - `backend/app/api/endpoints/medical.py`: Add REST endpoints for 5-Pathway Orthopedic Triage:
     - `GET /api/medical/players/{player_id}/triage/protocols` -> returns `TriageProtocolsResponse`
     - `POST /api/medical/players/{player_id}/triage/apply` -> calls `OrthopedicTriageService.apply_triage_protocol` and returns `TriageDecisionResult`
     - Add `neck_health: float = 100.0` to `BodyHealthResponse`
   - `backend/app/api/endpoints/coaches.py`: Add REST endpoints for Coaching Dynasty Tree & Staff Synergy:
     - `GET /api/coaches/{coach_id}/tree` -> calls `CoachingDynastyService.get_coach_profile`
     - `POST /api/coaches/{coach_id}/unlock-node` -> calls `CoachingDynastyService.unlock_node`
     - `GET /api/coaches/staff/synergy/{team_id}` -> calls `CoachingDynastyService.calculate_staff_synergy`
   - `backend/app/api/endpoints/scouts.py`: Add REST endpoints for Multi-Lens Prospect Intelligence:
     - `GET /api/scouts/prospects/{prospect_id}/intelligence` -> calls `ScoutingLensService.evaluate_prospect`
     - `GET /api/scouts/trade-urgency/{team_id}` -> calls `ScoutingLensService.calculate_trade_urgency`
2. Frontend Service & URL Prefix Fixes:
   - `frontend/src/services/abilitiesApi.ts`: Fix all URL paths from `/abilities/...` to `/api/abilities/...`.
   - `frontend/src/services/physicsService.ts`: Fix all URL paths from `/physics/...` to `/api/physics/...` and WebSocket to `/api/physics/stream`.
   - `frontend/src/services/scouting.ts`: Replace `MOCK_SCOUTING_REPORT` & `MOCK_BACKSHIORY` with live API calls to `/api/scouts/report/${team_id}/${playerId}` and `/api/scouts/prospects/${playerId}/intelligence`.
   - `frontend/src/services/tradeApi.ts`: Wire `getIncomingOffers`, `respondToOffer`, `proposeTrade` to live `/api/trades` endpoints and eliminate mock generator functions.
   - `frontend/src/router.tsx`: In `draftRoomLoader()`, query live `/api/teams`, `/api/season/current`, and `/api/draft/board` endpoints.
   - `frontend/src/services/season.ts`: Wire live endpoints for draft picks, team needs, and free agency simulation.
   - `frontend/src/components/coaching/GameplanDashboard.tsx`: Query live coaching tree / gameplan API.
   - `frontend/src/components/history/LogoTimeline.tsx`: Connect live franchise historical data.
3. Verification:
   - Run `pytest backend/tests/unit` to ensure 100% backend unit test pass rate.
   - Run `cd frontend && npm run build` (`tsc -b && vite build`) to ensure 0 TypeScript compilation errors.
4. Document all changes and test outputs in `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2_endpoints\handoff.md`.
When done, message parent with your summary and report path.

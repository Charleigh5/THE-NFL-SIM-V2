# Handoff Report — Backend Survey Explorer

**Date:** 2026-08-23T21:08:00Z  
**Agent Role:** Survey Explorer (Backend Audit)  
**Working Directory:** `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_be`  
**Parent Agent:** `e2795446-c3c5-4e9f-8b68-8c7a1cd58475` (parent)  
**Deliverable File:** `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_be\survey_backend.md`  

---

## 1. Observation

Direct code inspections and terminal verification confirmed the following:

1. **Backend Unit Tests:** Ran `pytest backend/tests/unit` with output:
   `300 passed, 9 warnings in 9.96s` (48% total codebase coverage across unit tests).
2. **Endpoint Inventory:** Scanned `backend/app/api/endpoints/` and `backend/app/api/`. Found 27 router files with 134 total registered routes across system, simulation, data, teams, players, season, draft, scouts, medical, coaches, gameplans, traits, abilities, broadcast, news, trades, combine, physics, and training.
3. **Unexposed Backend Services:**
   - `backend/app/services/medical/orthopedic_triage_service.py` (lines 25-155) defines `get_protocol_options()` and `apply_triage_protocol()` for 5 clinical pathways (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`) returning `TriageDecisionResult`. However, `backend/app/api/endpoints/medical.py` (lines 74-167) only exposes a legacy 3-option string endpoint (`REST`, `SURGERY`, `PLAY_THROUGH`).
   - `backend/app/services/coaching/coaching_dynasty_service.py` (lines 150-255) defines `get_coach_profile()`, `unlock_node()`, and `calculate_staff_synergy()`. However, `backend/app/api/endpoints/coaches.py` only implements coach hiring/firing/carousel and has no endpoints for skill trees or staff synergy.
   - `backend/app/services/draft/scouting_lens_service.py` (lines 25-145) implements multi-lens prospect evaluation (`ProspectIntelligence`) across `ScoutBiasLens` (Consensus, Film, Analytics, Regional) and `calculate_trade_urgency()`. However, `backend/app/api/endpoints/draft.py` only exposes `/board` and `/suggest-pick`.
4. **URL Prefix Desynchronizations:**
   - `backend/app/core/setup.py` (line 98) mounts `abilities.router` with `prefix="/api"`, while `abilities.py` (line 23) has `prefix="/abilities"`, resulting in `/api/abilities/...`. However, `frontend/src/services/abilitiesApi.ts` (lines 15, 24, 34, 44, 55) issues HTTP requests to `/abilities/...` (without `/api`), causing 404 errors.
   - `backend/app/core/setup.py` (line 120) mounts `physics_api.router` with `prefix="/api"`, while `physics_api.py` (line 26) has `prefix="/physics"`, resulting in `/api/physics/...` and `ws://.../api/physics/stream`. However, `frontend/src/services/physicsService.ts` (lines 86, 103, 132) calls `/physics/...` and `ws://.../physics/stream` (without `/api`), causing 404 & WebSocket connection drops.
   - `backend/app/api/endpoints/scouts.py` (line 124) defines `@router.get("/report/{team_id}/{prospect_id}")`. However, `frontend/src/services/scouting.ts` (line 55) calls `api.get('/api/scouting/report/${playerId}')` omitting `team_id`, resulting in 404/422 errors and fallback to static mock `MOCK_SCOUTING_REPORT`.
5. **Duplicate Routers:**
   - `backend/app/api/training.py` vs `backend/app/api/endpoints/training.py`: `api/training.py` integrates `TrainingEngine`, whereas `endpoints/training.py` has mock stubs.
   - `backend/app/api/endpoints/news.py` vs `backend/app/api/news_router.py`: overlapping news routes registered in `setup.py`.
6. **Hardcoded Frontend Loaders & Stubs:**
   - `frontend/src/router.tsx` (lines 147-206): `draftRoomLoader` returns hardcoded mock teams, season, and current pick objects.
   - `frontend/src/services/season.ts` (lines 140-194): `getCurrentPick`, `makePick`, `tradeCurrentPick`, `simulateNextPick`, `simulateFreeAgency`, and `getTeamNeeds` return mock data instead of calling backend `/api/season/{id}/...` endpoints.
   - `frontend/src/services/tradeApi.ts` (lines 147-152, 246-253): `getIncomingOffers` and `respondToOffer` use mock data even though `backend/app/api/endpoints/trades.py` has live endpoints.
7. **Hardcoded File Path in Feedback:**
   - `backend/app/api/endpoints/feedback.py` (line 200): `output_dir = Path("c:/Users/cweir/Documents/GitHub/THE NFL SIM/docs/updates_and_enhancements")` is hardcoded.

---

## 2. Logic Chain

1. **Premise:** R1 and R2 of the mandate require 100% backend API coverage and 1:1 schema parity across all 13 core application views with zero mock fallbacks.
2. **Analysis:** The simulation engine, RPG kernels, and domain services already exist in Python (`backend/app/services/` and `backend/app/engine/`).
3. **Inference:** The primary causes of frontend mock dependencies and UI disconnects are:
   - Specific service methods (`OrthopedicTriageService`, `CoachingDynastyService`, `ScoutingLensService`) lack FastAPI route handlers in `backend/app/api/endpoints/`.
   - Frontend API clients in `frontend/src/services/` have mismatched URL prefixes (`/abilities` vs `/api/abilities`, `/physics` vs `/api/physics`) or outdated mock loaders.
4. **Resolution:** By implementing the 14 identified remediations in `survey_backend.md`, creating the 7 missing endpoint handlers, and updating the frontend service URLs and loaders, the system will achieve 100% contract parity, 0 mock dependencies, and live data rendering across all 13 views.

---

## 3. Caveats

- **Frontend Component Layouts:** Audit of frontend TypeScript components was conducted from an API/contract integration perspective; detailed CSS layout clipping or responsive styling audits will be finalized during Playwright browser automation.
- **External Network Access (MCP Sports News / Gemini API):** While backend handles offline mock fallbacks for AI research and news when API keys are absent, all primary simulation, physics, triage, draft, and dynasty features operate deterministically in offline/local mode.

---

## 4. Conclusion

The backend audit is complete and documented in `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_be\survey_backend.md`.

All 13 core views have been cataloged, existing FastAPI endpoints mapped, and 14 specific gaps/routing fixes identified for closed-loop remediation. The backend test suite currently passes 100% (`pytest backend/tests/unit` -> 300 passed).

---

## 5. Verification Method

1. **Verify Backend Unit Tests:**
   ```bash
   pytest backend/tests/unit
   ```
2. **Inspect Comprehensive Survey Report:**
   Read `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_be\survey_backend.md`.
3. **Verify Route Registrations:**
   Inspect `backend/app/core/setup.py` and endpoint routers in `backend/app/api/endpoints/`.

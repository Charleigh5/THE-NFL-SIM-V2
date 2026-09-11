# Dispatch: Worker M1 (Track 1: Contract & Capology Specialist - TASK-010)

## Mandatory Context
Read the authoritative user request at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`

Read the survey findings at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_5p_1\handoff.md`

Read the project scope and interface contracts at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_5pillar\PROJECT.md`

## Working Directory
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m1_capology`
Maintain your `BRIEFING.md` and `progress.md` in this directory.

## Exclusive File Ownership
You exclusively own and modify:
- `backend/app/services/empire/salary_cap.py`
- `backend/app/kernels/empire/capologist.py`
- `backend/app/services/salary_cap_service.py`
- `backend/app/services/free_agency_engine.py`
- `backend/app/api/endpoints/season.py`
- `backend/app/schemas/offseason.py`
- `frontend/src/types/offseason.ts`
- `backend/tests/unit/test_capology_sprint.py`

DO NOT modify any other files.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Requirements
1. **Post-June 1st Cap Splits**:
   - Implement post-June 1st contract release logic in `capologist.py` and `salary_cap.py`: when a player is designated as a post-June 1st cut, dead money from unamortized signing bonus is split across two league years:
     - Current league year takes only the current year's prorated signing bonus allocation.
     - Following league year absorbs the remaining unamortized signing bonus balance.
2. **Top-51 Offseason Rule**:
   - Implement the NFL CBA Top-51 rule in `salary_cap_service.py`: during the offseason period (e.g. when `season.status != "REGULAR_SEASON"`), team salary cap obligations are calculated using only the top 51 largest `contract_salary` amounts on the active roster.
3. **FreeAgencyEngine Market Overview & Parameter Alignment**:
   - In `backend/app/services/free_agency_engine.py`, fix `get_market_overview` where it instantiates `FreeAgentMarketPlayer`: ensure parameter names match `backend/app/schemas/offseason.py` (`player_name` and `projected_aav`, not `name` or `experience`), or update schema/engine to complete parity.
4. **Interactive Market Browsing & Bidding Endpoints**:
   - In `backend/app/api/endpoints/season.py`, expose:
     - `GET /api/seasons/{season_id}/free-agency/market`: returns `List[FreeAgentMarketPlayer]` for unassigned players.
     - `POST /api/seasons/{season_id}/free-agency/bid`: processes user GM bid and evaluates competitive AI GM counter-offers via `FreeAgencyEngine`.
5. **Contract Parity**:
   - Add `FreeAgentSigning` and `FreeAgentMarketPlayer` to `frontend/src/types/offseason.ts` with zero `any` types.
6. **Unit Tests & Verification**:
   - Write comprehensive unit tests in `backend/tests/unit/test_capology_sprint.py` testing post-June 1st dead money splitting, Top-51 cap calculation, and market overview querying.
   - Run tests: `pytest backend/tests/unit/test_capology_sprint.py backend/tests/test_free_agency_engine.py`.
   - Run: `python scripts/check_field_parity.py`.
   - Run: `npm --prefix frontend run build`.

Deliver your report in `handoff.md` in your working directory and notify parent.

## 2026-09-06T03:37:18Z
Read your dispatch file at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m1_capology\DISPATCH.md and the authoritative request at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md.

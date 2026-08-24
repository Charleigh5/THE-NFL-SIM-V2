## 2026-08-23T21:32:23Z
You are the Worker for Milestone 3: Duplicate Logic & Schema Deduplication (R3) for THE-NFL-SIM-V2.
Your working directory is: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m3_deduplication`
Create your working directory if needed. Maintain `progress.md` with timestamps.

MANDATORY: You MUST read `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md` and `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md` before starting work. Also review `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_qa\survey_qa.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE & TASKS:
1. Backend Logic & Router Deduplication:
   - OL Chemistry: Harmonize `backend/app/services/chemistry_service.py` with `backend/app/services/enhanced_chemistry_service.py` so simulation and API share unified chemistry formulas.
   - Player Archetypes: Harmonize `backend/app/engine/archetype_effects.py` to support the 7 canonical archetypes in `backend/app/rpg/player_archetypes.py`.
   - Traits: Ensure deprecated `backend/app/rpg/traits.py` delegates cleanly to canonical `backend/app/services/trait_service.py`.
   - Training Routers: Remove unmounted duplicate `backend/app/api/training.py` and consolidate into `backend/app/api/endpoints/training.py`.
   - News Routers: Consolidate `backend/app/api/news_router.py` into `backend/app/api/endpoints/news.py` and clean up `backend/app/core/setup.py` mountings.
   - Stats Schemas: Unify `backend/app/schemas/expanded_stats.py` into `backend/app/schemas/stats.py`.
   - Feedback Path: Fix hardcoded path in `backend/app/api/endpoints/feedback.py:200` to use relative directory `Path("docs/updates_and_enhancements")`.
2. Frontend Schema Parity & 0 `any` Types:
   - In `frontend/src/services/tradeApi.ts` and `frontend/src/types/trade.ts`: Eliminate `any` casts, align `TradeProposal`, `TradeOfferRequest`, `TradeOfferStatus` (add `WITHDRAWN`), and `gm_philosophy`.
   - In `frontend/src/types/offseason.ts` & `frontend/src/types/api/scouting.ts`: Deduplicate `ScoutingReport` interface.
   - In `frontend/src/services/`: Consolidate `traits.ts` and `traitService.ts`.
   - Delete orphaned `frontend/src/types/season.ts.backup`.
3. Verification:
   - Run `pytest backend/tests/unit` to ensure 100% pass rate.
   - Run `python scripts/batch_simulator.py --games 50` to confirm Monte Carlo calibration.
   - Run `cd frontend && npm run build` (`tsc -b && vite build`) to confirm 0 compilation errors.
4. Document all changes and test outputs in `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m3_deduplication\handoff.md`.
When done, message parent with your summary and report path.

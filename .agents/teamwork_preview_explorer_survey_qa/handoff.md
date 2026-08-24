# Handoff Report: Survey Explorer QA & Deduplication Audit

**Author:** QA Survey Explorer  
**Date:** 2026-08-24  
**Target:** Parent Orchestrator (`e2795446-c3c5-4e9f-8b68-8c7a1cd58475`)  
**Scope:** Full-Codebase Code Duplication, Schema/TypeScript Parity, and Test Infrastructure Audit  

---

## 1. Observation

### Direct Observations & Verbatim Commands
1. **Backend Unit Tests:**
   - Command: `pytest backend/tests/unit`
   - Result: `300 passed, 9 warnings in 11.99s`
   - Test files: 34 files in `backend/tests/unit/`, 89 files across `backend/tests/`.
2. **Monte Carlo Calibration Engine:**
   - Command: `python scripts/batch_simulator.py --games 50`
   - Result:
     - `sack_rate`: Observed `6.39%` (Target: `6.50% ± 1.50%`) -> `PASS`
     - `yards_per_carry`: Observed `4.03 yds` (Target: `4.20 ± 0.50 yds`) -> `PASS`
     - `completion_rate`: Observed `67.36%` (Target: `64.50% ± 4.50%`) -> `PASS`
     - `turnovers_per_game`: Observed `0.89 /gm` (Target: `1.30 ± 0.50 /gm`) -> `PASS`
     - `points_per_game`: Observed `24.64 pts` (Target: `21.80 ± 4.00 pts`) -> `PASS`
     - Status: `100% ALIGNED WITH NFL BASELINE` in `1.29s (38.6 games/sec)`.
3. **Frontend Production Compilation:**
   - Command: `cd frontend && npm run build` (`tsc -b && vite build`)
   - Result: Exit code `0` (built in 25.43s, `tsc -b` strictly passed without errors).
4. **Playwright E2E Setup:**
   - `frontend/playwright.config.ts`: `testDir: "./e2e"`, base URL `http://localhost:5199`, webServer `npx vite --port 5199`.
   - `frontend/e2e/`: 27 active test specs covering all 13 core views.
   - `frontend/tests/`: 12 legacy/component test specs outside the main Playwright test dir.
5. **Backend Code Duplication:**
   - **OL Chemistry:** `backend/app/services/chemistry_service.py` (sync `Session`, discrete threshold table 0/1/2/3/5) vs `backend/app/services/enhanced_chemistry_service.py` (async `AsyncSession`, logarithmic formula `0.6 + 0.4 * (1 - e^(-2.5x))`, caching, advanced perks).
   - **Player Archetypes:** `backend/app/rpg/player_archetypes.py` (7 canonical archetypes matching frontend `types/archetypes.ts`) vs `backend/app/engine/archetype_effects.py` (5 divergent legacy archetypes; only imported in `backend/tests/test_archetype_effects.py:9`).
   - **Traits:** `backend/app/rpg/traits.py` (deprecated 4-trait system with runtime warning) vs `backend/app/services/trait_service.py` (canonical 25-trait catalog) vs `trait_acquisition_service.py` / `trait_evolution_service.py`.
   - **Training Routers:** `backend/app/api/endpoints/training.py` (mounted at `/api/training`) vs `backend/app/api/training.py` (unmounted orphan router at `/training` with duplicate models).
   - **News Routers:** `backend/app/api/endpoints/news.py` (mounted at `/api/news`) vs `backend/app/api/news_router.py` (mounted at `/api/news` with route collisions on `/api/news/categories`).
   - **Stats Schemas:** `backend/app/schemas/stats.py` (`LeagueLeaders` with 6 categories) vs `backend/app/schemas/expanded_stats.py` (`LeagueLeaders` with 23 categories; only used in `test_expanded_stats.py`).
6. **Schema & TypeScript Contract Parity:**
   - `frontend/src/services/tradeApi.ts:151`: Uses explicit `as unknown as IncomingTradeOffer[]` with comment `// Casting to any to avoid strict type mismatch with legacy IncomingTradeOffer for now`.
   - `frontend/src/types/medical.ts:1-12`: `BodyHealth.neck_health: number` is declared mandatory, but `backend/app/api/endpoints/medical.py:11-20` `BodyHealthResponse` lacks `neck_health`.
   - `frontend/src/types/trade.ts:63`: `TradeEvaluation.gm_personality?: string` vs backend `TradeEvaluationResponse.gm_philosophy?: str`.
   - `frontend/src/types/trade.ts:106`: `TradeOfferStatus` misses `WITHDRAWN` enum member.
   - `frontend/src/types/trade.ts:41-51`: `TradeProposal` uses `offered_players: number[]` & `receiving_team_id: number` vs `TradeOfferRequest` in `backend/app/schemas/trade.py:73-98` (`offered_player_ids: List[int]` & `target_team_id: int`).
   - Duplicate interface name `ScoutingReport` in `frontend/src/types/offseason.ts:38-52` vs `frontend/src/types/api/scouting.ts:18-35`.
   - Duplicate trait services: `frontend/src/services/traits.ts` (`traitsApi` via Axios) vs `frontend/src/services/traitService.ts` (`traitService` via `fetch`).
   - Leftover artifact: `frontend/src/types/season.ts.backup`.

---

## 2. Logic Chain

1. **Test Infrastructure Health:**
   - Both backend unit tests (`pytest backend/tests/unit`) and frontend production build (`tsc -b && vite build`) pass with 100% success rate.
   - Monte Carlo simulation verifies that physical game math aligns within statistical tolerances of real-world NFL data (sack rates 6.39%, YPC 4.03, completions 67.36%, turnovers 0.89/gm, points 24.64/gm).
   - Therefore, the underlying core execution environment is stable and ready for targeted refactoring and visual verification.

2. **Backend Redundancy Root Causes:**
   - As the engine evolved through successive phases (e.g. Phase 1-12 enhancements, RPG expansion, living world director), new services were created (e.g., `enhanced_chemistry_service.py`, `news.py`, `trait_service.py`) alongside earlier prototype implementations (e.g., `chemistry_service.py`, `news_router.py`, `rpg/traits.py`, `archetype_effects.py`).
   - Because `play_resolver.py` still references `chemistry_service.py`, a functional fork exists where simulation runtime logic calculates chemistry differently from the API layer (`enhanced_chemistry_service.py`).
   - Similarly, duplicate API routers (`api/training.py` vs `api/endpoints/training.py`) and colliding news mounts (`endpoints/news.py` vs `news_router.py`) create unnecessary maintenance overhead and routing ambiguities.

3. **Frontend Contract Gaps:**
   - Field mismatch on `neck_health` in `BodyHealth` causes potential `undefined` values in medical views if accessed directly.
   - Type casting and mock methods in `tradeApi.ts` hide incomplete backend wiring for trade blocks and formal offer execution.
   - Interface name collisions between `types/offseason.ts` and `types/api/scouting.ts` risk accidental type cross-contamination during component imports.

---

## 3. Caveats

1. **Playwright Live Browser Automation Execution:** Headless browser execution against the live dev server (`npm run test:e2e`) was not executed in full during this survey turn to maintain explorer focus on code-level audit and test runner requirements; however, the configuration, mock interceptors, and 27 spec files were fully inspected.
2. **Database Migrations:** Database persistence models were surveyed for schema shape; actual SQLite/PostgreSQL migration rollbacks were not evaluated.
3. **No Code Written to Source Files:** In strict compliance with the Explorer archetype read-only mandate, no modifications were made to `backend/app/` or `frontend/src/`. All proposals are documented in `survey_qa.md`.

---

## 4. Conclusion

The NFL Sim V2 codebase possesses strong foundational test coverage (300 passing unit tests, verified Monte Carlo calibration, 0 build-time TypeScript errors), but suffers from **modular duplication, unmounted prototype routers, and minor contract drift** resulting from rapid iterative feature expansion.

Remediating the identified top 8 priorities (P0-P3 outlined in `survey_qa.md`) will cleanly eliminate legacy code paths, reconcile divergent chemistry/archetype math, unify API routing, and achieve 100% strict contract parity between backend Pydantic models and frontend TypeScript interfaces with 0 `any` types.

---

## 5. Verification Method

To independently reproduce and verify all findings:
1. **Verify Backend Unit Tests:**
   ```bash
   pytest backend/tests/unit
   ```
   *Expected:* 300 passed tests.
2. **Verify Monte Carlo Statistical Calibration:**
   ```bash
   python scripts/batch_simulator.py --games 50
   ```
   *Expected:* All 5 metrics PASS within NFL benchmark tolerances.
3. **Verify Frontend Build & Typecheck:**
   ```bash
   cd frontend && npm run build
   ```
   *Expected:* `tsc -b && vite build` completes with exit code 0.
4. **Inspect Audit Dossier:**
   - Full Report: `.agents/teamwork_preview_explorer_survey_qa/survey_qa.md`

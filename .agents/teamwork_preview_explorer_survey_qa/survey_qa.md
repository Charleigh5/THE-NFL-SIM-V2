# Comprehensive Survey & QA Audit Report: Code Duplication, Schema Parity, and Test Infrastructure

**Document ID:** QA-AUDIT-001  
**Author:** QA Survey Explorer  
**Date:** 2026-08-24  
**Project:** THE-NFL-SIM-V2 ("The Digital Gridiron")  
**Target Scope:** Backend (`backend/app/`), Frontend (`frontend/src/`), Test Suites (`backend/tests/`, `frontend/e2e/`, `scripts/`)  

---

## 1. Executive Summary

A comprehensive, deep-scan audit of THE-NFL-SIM-V2 was conducted across three primary axes:
1. **Backend Duplicate Logic & Redundant Implementations:** Identified 7 distinct areas of architectural divergence and duplicate modules across services, engines, orchestrators, and RPG layers.
2. **Schema & TypeScript Contract Parity:** Audited all Pydantic V2 models against TypeScript definitions, identifying naming collisions, interface collisions, unmounted/duplicate service classes, field discrepancies, and explicit `any`/casting usages.
3. **Test Infrastructure & Verification Gates:** Evaluated backend unit test suites, Monte Carlo calibration simulation, frontend production compilation, and Playwright E2E browser automation setup.

---

## 2. Pillar 1: Backend Duplicate Logic & Redundancy Audit

### 2.1 OL Chemistry Systems: `ChemistryService` vs `EnhancedChemistryService`
- **Locations:**
  - `backend/app/services/chemistry_service.py` (186 lines)
  - `backend/app/services/enhanced_chemistry_service.py` (415 lines)
- **Observations & Evidence:**
  - `ChemistryService` (`chemistry_service.py`): Synchronous SQLAlchemy `Session`, static discrete threshold table (0-2 games = +0/1, 3-5 = +2, 6-9 = +3, 10+ = +5), hashing based on `PlayerGameStarts.teammates_hash`. Directly imported in `backend/app/orchestrator/play_resolver.py:13` and tested in `backend/tests/unit/test_chemistry_service.py:1`.
  - `EnhancedChemistryService` (`enhanced_chemistry_service.py`): Asynchronous `AsyncSession`, logarithmic formula `0.6 + 0.4 * (1 - e^(-2.5x))`, caching via `chemistry_cache`, advanced effects (`stunt_pickup_bonus`, `penalty_reduction`, `communication_boost`, `blitz_pickup_improvement`). Directly imported in `backend/app/api/endpoints/teams.py:13`, `backend/app/services/pre_game_service.py:8`, and `backend/tests/integration/test_enhanced_chemistry.py:3`.
- **Architectural Risk:** Simulation engine (`play_resolver.py`) uses synchronous threshold math, while the UI endpoint (`teams.py`) and pre-game service use async logarithmic math. Player ratings and chemistry modifiers diverge between live play resolution and UI inspection.
- **Deduplication Recommendation:** Consolidate into a single canonical chemistry engine module that exposes a pure mathematical calculation core usable by both synchronous simulation loops and async FastAPI endpoints.

---

### 2.2 Player Archetype Divergence: `player_archetypes.py` vs `archetype_effects.py`
- **Locations:**
  - `backend/app/rpg/player_archetypes.py` (410 lines)
  - `backend/app/engine/archetype_effects.py` (232 lines)
  - `frontend/src/types/archetypes.ts` (83 lines)
- **Observations & Evidence:**
  - `player_archetypes.py`: Defines 7 canonical archetypes: `FIELD_GENERAL`, `SORCERER`, `ALPHA_DOG`, `WEAPON`, `FREAK`, `TECHNICIAN`, `WORKHORSE`. 100% matched to `frontend/src/types/archetypes.ts`.
  - `archetype_effects.py`: Defines 5 legacy archetypes: `FIELD_GENERAL`, `TRAILER_PARK_TERMINATOR`, `SPEED_MERCHANT`, `TRENCH_WARLORD`, `STANDARD` with string value mismatch (e.g., `"Trailer Park Terminator"` vs canonical enum keys).
  - Grep search confirms `archetype_effects.py` is ONLY imported in `backend/tests/test_archetype_effects.py:9` and nowhere in the main simulation or API.
- **Deduplication Recommendation:** Deprecate/delete `backend/app/engine/archetype_effects.py` or refactor its in-game trigger logic to use the canonical 7 archetypes from `app.rpg.player_archetypes`.

---

### 2.3 Trait System Fragmentation: Legacy RPG Traits vs Service Architecture
- **Locations:**
  - `backend/app/rpg/traits.py` (56 lines)
  - `backend/app/services/trait_service.py` (948 lines)
  - `backend/app/services/trait_acquisition_service.py` (128 lines)
  - `backend/app/services/trait_evolution_service.py` (265 lines)
- **Observations & Evidence:**
  - `backend/app/rpg/traits.py` explicitly issues `warnings.warn("TraitSystem is deprecated. Use TraitService from app.services.trait_service instead.")` with 4 legacy traits (`DeepBall`, `Clutch`, `BrickWall`, `BallHawk`). Only referenced by `backend/app/rpg/__init__.py`.
  - `trait_service.py` implements the full 25-trait catalog with database persistence, eligibility checking, and simulation modifiers.
  - `trait_acquisition_service.py` and `trait_evolution_service.py` re-wrap calls to `TraitService`.
- **Deduplication Recommendation:** Remove deprecated `backend/app/rpg/traits.py`, update `app.rpg.__init__.py` to export canonical `TraitService`, and encapsulate acquisition/evolution under `app.services.trait_service`.

---

### 2.4 Duplicate Training API Routers: `api/endpoints/training.py` vs `api/training.py`
- **Locations:**
  - `backend/app/api/endpoints/training.py` (127 lines)
  - `backend/app/api/training.py` (338 lines)
  - `backend/app/core/setup.py` (lines 72, 114)
- **Observations & Evidence:**
  - `backend/app/core/setup.py` imports `training` from `app.api.endpoints` and registers it via `app.include_router(training.router, prefix="/api/training", tags=["training"])`.
  - `backend/app/api/training.py` is an unmounted orphan router defining `prefix="/training"` with duplicate schemas (`ExecuteTrainingRequest`, `ExecuteTrainingResponse`, `ScheduleResponse`, `DrillResponse`) and calls `TrainingEngine` from `app.kernels.rpg.training`.
  - `backend/app/api/endpoints/training.py` uses `TrainingProgramsService` from `app.services.training.training_programs`.
- **Deduplication Recommendation:** Merge the rich kernel integration from `app/api/training.py` into `app/api/endpoints/training.py` and remove `app/api/training.py`.

---

### 2.5 News & Living World Route Collision: `endpoints/news.py` vs `api/news_router.py`
- **Locations:**
  - `backend/app/api/endpoints/news.py` (541 lines)
  - `backend/app/api/news_router.py` (246 lines)
  - `backend/app/core/setup.py` (lines 104, 129)
- **Observations & Evidence:**
  - `backend/app/core/setup.py` mounts `app.include_router(news.router, prefix="/api", tags=["news"])` (exposing `/api/news/league`, `/api/news/team/{name}`, `/api/news/player/{name}`, `/api/news/living/feed`, `/api/news/living/recap/...`, `/api/news/categories`).
  - `backend/app/core/setup.py` ALSO mounts `app.include_router(news_router.router)` where `news_router` has `prefix="/api/news"` (exposing `/api/news/feed`, `/api/news/recap/{season_id}/{week}`, `/api/news/categories`).
  - Both routers define colliding endpoints on `/api/news/categories` and `/api/news/recap`.
- **Deduplication Recommendation:** Unify all news endpoints into `backend/app/api/endpoints/news.py`, remove `backend/app/api/news_router.py`, and remove duplicate mount in `setup.py`.

---

### 2.6 Colliding Stats Schemas: `schemas/stats.py` vs `schemas/expanded_stats.py`
- **Locations:**
  - `backend/app/schemas/stats.py` (21 lines)
  - `backend/app/schemas/expanded_stats.py` (408 lines)
- **Observations & Evidence:**
  - `schemas/stats.py` defines `LeagueLeaders` (6 basic stat categories) with `PlayerLeader`. Used by `backend/app/api/endpoints/season.py:23` and `backend/app/services/stats_service.py:8`.
  - `schemas/expanded_stats.py` defines a colliding `LeagueLeaders` (23 expanded categories) using `PlayerStat` inheritance (`QuarterbackStat`, `RunningBackStat`, etc.). Only imported in `backend/tests/test_expanded_stats.py:3`.
- **Deduplication Recommendation:** Consolidate `stats.py` and `expanded_stats.py` into a unified schema hierarchy so production endpoints can benefit from expanded stats without class name collisions.

---

### 2.7 Medical & Orthopedic Wear Subsystems
- **Locations:**
  - `backend/app/services/medical_service.py` (82 lines)
  - `backend/app/services/medical/orthopedic_triage_service.py` (155 lines)
  - `backend/app/rpg/injury_system.py` (520 lines)
  - `backend/app/kernels/genesis/trauma_center.py`
- **Observations & Evidence:**
  - `medical_service.py` models 6 body parts (`head`, `torso`, `right_arm`, `left_arm`, `right_leg`, `left_leg`) on `BodyPart` model.
  - `orthopedic_triage_service.py` models 7 anatomical zones and 5 medical protocol options (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`).
  - `injury_system.py` calculates in-game injury probabilities based on position wear, weather, turf, and fatigue.
- **Deduplication Recommendation:** Unify the anatomical zone definitions across `BodyPart` model, `medical_service.py`, and `orthopedic_triage_service.py`.

---

## 3. Pillar 2: Schema & Type Parity Audit

### 3.1 Explicit `any` Types & Unsafe Casts
1. `frontend/src/services/tradeApi.ts:151`:
   - `return generateMockIncomingOffers(teamId) as unknown as IncomingTradeOffer[];`
   - Explicit comment on line 149 acknowledges type mismatch: `// Casting to any to avoid strict type mismatch with legacy IncomingTradeOffer for now`.
2. Mock / Placeholder Implementations in `tradeApi.ts`:
   - `executeTrade` (lines 135-142): Returns static `{ success: true, message: "Trade executed successfully!" }`.
   - `getTradeBlock` (lines 157-161): Returns static `[]`.
   - `addToTradeBlock` (lines 166-181): Returns static mock object with hardcoded `"Unknown Player"`.
   - `removeFromTradeBlock` (lines 186-190): No-op `console.log`.
   - `getTradeHistory` (lines 258-262): Returns static `[]`.

---

### 3.2 Field & Property Discrepancies
| Area / Contract | Backend Schema (`backend/app/schemas/`) | Frontend Interface (`frontend/src/types/`) | Severity & Impact |
| :--- | :--- | :--- | :--- |
| **Body Health** | `BodyHealthResponse` in `endpoints/medical.py:11-20` has 6 body zones (`head`, `torso`, `right_arm`, `left_arm`, `right_leg`, `left_leg`). | `BodyHealth` in `types/medical.ts:1-12` declares mandatory `neck_health: number`. | **High**: Frontend expects `neck_health`, which backend never sends (`undefined`). |
| **Trade Evaluation** | `TradeEvaluationResponse` in `schemas/trade.py:67` has `gm_philosophy: Optional[str]`. | `TradeEvaluation` in `types/trade.ts:63` has `gm_personality?: string` and `counter_offer?: ...`. | **Medium**: Renamed field leads to missing GM rationale in UI. |
| **Trade Offer Status** | `TradeOfferStatus` in `schemas/trade.py:124-131` includes `WITHDRAWN`. | `TradeOfferStatus` in `types/trade.ts:106` lacks `WITHDRAWN` (`"PENDING" \| "ACCEPTED" \| "REJECTED" \| "COUNTERED" \| "EXPIRED"`). | **Medium**: Deserialization gap when offer is withdrawn. |
| **Trade Proposal vs Offer** | `TradeOfferRequest` in `schemas/trade.py:73-98` uses `offered_player_ids: List[int]` and `target_team_id: int`. | `TradeProposal` in `types/trade.ts:41-51` uses `offered_players: number[]` and `receiving_team_id: number`. | **High**: Incompatible payload format if submitted directly. |

---

### 3.3 Duplicate Interface Names & Collisions in Frontend
1. **`ScoutingReport` Collision:**
   - `frontend/src/types/offseason.ts:38-52`:
     ```ts
     export interface ScoutingReport {
       prospect_id: string;
       completion: number;
       attributes: Record<string, { value: number | null; range: [number, number] | null; tier: string; display: string }>;
       strengths: string[];
       weaknesses: string[];
     }
     ```
   - `frontend/src/types/api/scouting.ts:18-35`:
     ```ts
     export interface ScoutingReport {
       player_id?: string | number;
       summary: string;
       strengths: string[];
       weaknesses: string[];
       nfl_comparison: string;
       ceiling_projection?: string;
       ...
     }
     ```
   - Two entirely different structures share the same interface name across two type files.

2. **`Trait` vs `TraitInfo` Collision:**
   - `frontend/src/types/trait.ts:19-27` defines `Trait` (`id`, `name`, `description`, `effect_type`, `effect_value`, `tier`, `position_groups`).
   - `frontend/src/services/api.ts:183-187` defines `TraitInfo` (`name`, `description`, `tier`).

3. **`PlayerStats` Collision:**
   - `frontend/src/services/api.ts:55-63` defines `PlayerStats` (`games_played`, `passing_yards`, `passing_tds`, `rushing_yards`, `rushing_tds`, `receiving_yards`, `receiving_tds`).
   - `frontend/src/types/stats.ts:1-8` defines `PlayerLeader` and `LeagueLeaders`.

---

### 3.4 Duplicate Frontend Service Modules
- `frontend/src/services/traits.ts`: Exports `traitsApi` using Axios `apiClient`. Used in `pages/SkillsPage.tsx` and `router.tsx`.
- `frontend/src/services/traitService.ts`: Exports `traitService` using native `fetch`. Used in `components/dev/TraitManager.tsx`.
- **Recommendation:** Merge `traitService.ts` into `traits.ts` using `apiClient`.

---

### 3.5 Leftover Artifact Files
- `frontend/src/types/season.ts.backup` (2,716 bytes): Leftover backup file in the source tree. Should be removed.

---

## 4. Pillar 3: Test Infrastructure Audit

### 4.1 Backend Unit Test Suite (`backend/tests/unit`)
- **Execution Command:** `pytest backend/tests/unit`
- **Result:** **300 passed, 9 warnings in 11.99s (100% Pass Rate)**
- **Coverage Areas Tested:**
  - `test_ability_service.py` (Ability unlocks, XP deductions, prerequisite checks)
  - `test_ai_services.py` (Gemini client integration and fallback logic)
  - `test_attribute_interaction.py` (Physics and rating interactions)
  - `test_audible_master.py` & `test_the_closer_trait.py` & `test_ragknow_trait.py` (RPG traits)
  - `test_broadcast_schemas.py` (Broadcast 7-phase state machine & transitions)
  - `test_coach_hierarchy.py` & `test_coaching_personality.py` (Staff chemistry & dynasty trees)
  - `test_injury_probability.py` & `test_injury_system.py` (Wear & tear, triage recovery)
  - `test_game_repository.py` & `test_game_state_manager.py` (State persistence & execution)
  - `test_s2_cognition_integration.py` & `test_turf_grid_integration.py` (Biometrics & field physics)

---

### 4.2 Monte Carlo Statistical Calibration Engine (`scripts/batch_simulator.py`)
- **Execution Command:** `python scripts/batch_simulator.py --games 50`
- **Result:** **100% Pass Rate across all 5 NFL Baseline Metrics (1.29s for 50 games / 6,000 plays)**
- **Calibration Telemetry Table:**

| Metric | Target Baseline | Observed Output | Allowed Tolerance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Sack Rate** | 6.50% | **6.39%** | ± 1.50% | **PASS** |
| **Yards Per Carry (YPC)** | 4.20 yds | **4.03 yds** | ± 0.50 yds | **PASS** |
| **Completion Rate** | 64.50% | **67.36%** | ± 4.50% | **PASS** |
| **Turnovers Per Game** | 1.30 /gm | **0.89 /gm** | ± 0.50 /gm | **PASS** |
| **Points Per Game** | 21.80 pts | **24.64 pts** | ± 4.00 pts | **PASS** |

---

### 4.3 Frontend Production Compilation & Typecheck Setup
- **Build Script:** `npm run build` (`tsc -b && vite build`)
- **TypeScript Configuration:** Strict type checking enabled (`"strict": true`, `"noUnusedLocals": true`, `"noUnusedParameters": true`, `"noEmit": true`) across `tsconfig.app.json` and `tsconfig.node.json`.
- **Execution Verification:** `tsc -b` compiles without errors.

---

### 4.4 Playwright E2E Test Suite
- **Configuration:** `frontend/playwright.config.ts`
  - Test Directory: `./e2e`
  - Base URL: `http://localhost:5199`
  - Auto Web Server: `npx vite --port 5199`
  - Multi-Browser Support: Chromium, Firefox, WebKit
- **Active E2E Specs (`frontend/e2e/` - 27 specs):**
  - `capture-dossier-screenshots.spec.ts`
  - `comprehensive-feature-verification.spec.ts` (13-view interactive verification suite)
  - `dashboard-flow.spec.ts`, `depth-chart-flow.spec.ts`, `draft-room.spec.ts`, `draft-genesis-flow.spec.ts`, `draft-assistant-widget.spec.ts`
  - `front-office.spec.ts`, `live-sim-flow.spec.ts`, `medical-center-flow.spec.ts`, `news-feed.spec.ts`
  - `offseason-flow.spec.ts`, `offseason-dashboard-flow.spec.ts`, `playbook-flow.spec.ts`, `player-profile-flow.spec.ts`
  - `scouting-flow.spec.ts`, `season-dashboard-flow.spec.ts`, `settings-flow.spec.ts`, `skills-page-flow.spec.ts`
  - `team-selection-flow.spec.ts`, `trade-center.spec.ts`, `training-center-flow.spec.ts`, `trophy-room-flow.spec.ts`
  - `visual-regression.spec.ts`
- **Legacy Spec Inventory (`frontend/tests/` - 12 specs):**
  - Contains older unit/component specs (`depth-chart.spec.ts`, `enhanced-dashboard.spec.ts`, `example.spec.ts`, `front_office.spec.ts`, `offseason.spec.ts`, `player-details.spec.ts`, `player_profile.spec.ts`, `schedule.spec.ts`, `season-start.spec.ts`, `season_progression.spec.ts`, `test-helpers.ts`).
  - Note: Not included in default `playwright.config.ts` (`testDir: "./e2e"`).

---

## 5. Prioritized Deduplication & QA Action Plan

| Priority | Action Item | Target Files | Remediation Description |
| :--- | :--- | :--- | :--- |
| **P0** | **Fix Medical BodyHealth Schema Mismatch** | `backend/app/api/endpoints/medical.py`<br>`frontend/src/types/medical.ts` | Add `neck_health` to `BodyHealthResponse` or make it optional in `BodyHealth` interface. |
| **P0** | **Unify News API Routers & Remove Collisions** | `backend/app/api/endpoints/news.py`<br>`backend/app/api/news_router.py`<br>`backend/app/core/setup.py` | Merge all living world and news routes into `endpoints/news.py` and remove duplicate `news_router.py`. |
| **P1** | **Consolidate Chemistry Engine** | `backend/app/services/chemistry_service.py`<br>`backend/app/services/enhanced_chemistry_service.py`<br>`backend/app/orchestrator/play_resolver.py` | Reconcile OL chemistry calculation formula into a shared kernel calculation used by both simulation and API. |
| **P1** | **Clean Up Duplicate Training Routers** | `backend/app/api/training.py`<br>`backend/app/api/endpoints/training.py` | Remove unmounted `backend/app/api/training.py` and ensure `endpoints/training.py` exposes all needed training endpoints. |
| **P1** | **Deduplicate Frontend Trait Services** | `frontend/src/services/traits.ts`<br>`frontend/src/services/traitService.ts` | Merge `traitService.ts` into `traits.ts` using `apiClient` Axios instance. |
| **P2** | **Reconcile Trade Contracts & Replace Mocks** | `frontend/src/services/tradeApi.ts`<br>`frontend/src/types/trade.ts`<br>`backend/app/schemas/trade.py` | Replace mock handlers in `tradeApi.ts` with real API endpoints, unify `TradeProposal`/`TradeOffer` types, and remove `any` casting. |
| **P2** | **Rename Ambiguous `ScoutingReport` Interfaces** | `frontend/src/types/offseason.ts`<br>`frontend/src/types/api/scouting.ts` | Rename `offseason.ts` `ScoutingReport` to `ProspectScoutingReport` to eliminate namespace collision with `api/scouting.ts`. |
| **P3** | **Remove Orphan Files** | `frontend/src/types/season.ts.backup` | Delete `.backup` file from version control. |

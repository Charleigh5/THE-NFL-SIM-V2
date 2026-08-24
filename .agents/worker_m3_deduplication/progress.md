# Progress: Milestone 3 - Duplicate Logic & Schema Deduplication

Last visited: 2026-08-23T21:32:23Z
Current Status: In Progress

## Tasks Checklist
- [ ] 0. Read mandatory documents (`ORIGINAL_REQUEST.md`, `PROJECT.md`, `survey_qa.md`).
- [ ] 1. Backend Deduplication:
  - [ ] OL Chemistry: Harmonize `chemistry_service.py` with `enhanced_chemistry_service.py`.
  - [ ] Player Archetypes: Harmonize `archetype_effects.py` with 7 canonical archetypes in `rpg/player_archetypes.py`.
  - [ ] Traits: Delegate `rpg/traits.py` to `services/trait_service.py`.
  - [ ] Training Routers: Consolidate `api/training.py` into `api/endpoints/training.py`.
  - [ ] News Routers: Consolidate `api/news_router.py` into `api/endpoints/news.py` & fix `core/setup.py`.
  - [ ] Stats Schemas: Unify `schemas/expanded_stats.py` into `schemas/stats.py`.
  - [ ] Feedback Path: Fix hardcoded path in `api/endpoints/feedback.py:200`.
- [ ] 2. Frontend Schema Parity & Zero `any`:
  - [ ] `tradeApi.ts` & `trade.ts`: Eliminate `any`, align `TradeProposal`, `TradeOfferRequest`, `TradeOfferStatus` (+`WITHDRAWN`), `gm_philosophy`.
  - [ ] `offseason.ts` & `api/scouting.ts`: Deduplicate `ScoutingReport`.
  - [ ] `services/`: Consolidate `traits.ts` and `traitService.ts`.
  - [ ] Delete `frontend/src/types/season.ts.backup`.
- [ ] 3. Verification:
  - [ ] `pytest backend/tests/unit`
  - [ ] `python scripts/batch_simulator.py --games 50`
  - [ ] `cd frontend && npm run build`
- [ ] 4. Handoff & Completion:
  - [ ] Write `handoff.md` with 5 required sections.
  - [ ] Send message to parent agent.

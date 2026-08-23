# BRIEFING — 2026-08-22T16:22:15Z

## Mission
Investigate and survey R2 (Core Football Simulation & Physics Engine Correction) and R3 (Season Lifecycle, Offseason & RPG Repair) across THE-NFL-SIM-V2 backend codebase.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, synthesizer
- Working directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_sim_season
- Original parent: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Milestone: Survey R2 (Simulation Engine) & R3 (Season Lifecycle & Offseason)

## 🔒 Key Constraints
- Read-only investigation — do NOT modify source code files.
- Document exact file paths, line numbers, root causes, and recommended surgical fix strategies in `handoff.md`.
- Send report path and status back to caller agent (`parent`).

## Current Parent
- Conversation ID: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Updated: 2026-08-22T16:22:15Z

## Investigation State
- **Explored paths**:
  - `app/engine/` (`sack_calculator.py`, `position_physics.py`, `quarterback.py`, `injury.py`, `probability_engine.py`, `core/deterministic_rng.py`)
  - `app/orchestrator/` (`simulation_orchestrator.py`, `play_resolver.py`, `play_commands.py`, `state_machine.py`)
  - `app/services/` (`standings_calculator.py`, `offseason_service.py`, `free_agency_engine.py`, `week_simulator.py`)
  - `app/api/endpoints/` (`season.py`, `trades.py`)
  - `app/models/` (`season.py`, `game.py`, `draft.py`, `trade_offer.py`)
  - `app/schemas/` (`play.py`, `offseason.py`)
- **Key findings**:
  - R2: Safety logic awards offensive TD due to `yard_line <= 0` in `simulation_orchestrator.py:817`; clock runoffs default to 40.0s in `schemas/play.py:13`; red zone TDs are missed because `play_resolver.py:923` checks `yards_gained > 80` rather than goal line; PAT/2-pt is hardcoded `+7` in `simulation_orchestrator.py:825`; global `random` leaks in `sack_calculator.py:98` and `position_physics.py`; continuous sim halts at Q1 end in `simulation_orchestrator.py:474`.
  - R3: `offseason_service.py:205` uses `x.win_pct` instead of `x.win_percentage` from `TeamStanding`; traded draft picks are ignored during pick creation and trade acceptance; `/free-agency/simulate` executes a dummy loop instead of `FreeAgencyEngine`; `WeekSimulator` creates duplicate `Game(season=2025, week=1)` rows and omits `await save_game_result()`; `StandingsCalculator:282` explicitly skips head-to-head tiebreakers; `OffseasonPhase` is missing state tracking and transition enforcement.
- **Unexplored areas**: None for R2/R3 survey scope.

## Key Decisions Made
- Fully documented all 13 targeted mechanisms with line numbers, code quotes, exact mechanics, root causes, and recommended surgical fix strategies.

## Artifact Index
- `.agents/explorer_survey_sim_season/DISPATCH.md` — Inbound prompts log
- `.agents/explorer_survey_sim_season/BRIEFING.md` — Persistent state and working memory
- `.agents/explorer_survey_sim_season/progress.md` — Heartbeat log
- `.agents/explorer_survey_sim_season/handoff.md` — Final structured 5-component report

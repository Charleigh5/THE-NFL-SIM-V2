# Progress — Explorer 2 (Simulation Engine & Season Lifecycle)

Last visited: 2026-08-22T16:22:15Z

- [x] Initialized DISPATCH.md and BRIEFING.md
- [x] Read ORIGINAL_REQUEST.md
- [x] Investigate R2: Core Football Simulation & Physics Engine (`app/engine/`, `app/orchestrator/`)
  - [x] Safety calculation on `yard_line <= 0`: Identified root causes in `simulation_orchestrator.py:817` and `play_resolver.py:668-677, 1434-1448`.
  - [x] Play clock runoffs: Identified 40.0s hardcoded default in `schemas/play.py:13` and missing runoff params in `play_resolver.py:547-1100`.
  - [x] Red zone TD stat attribution: Identified `yards_gained > 80` flaw in `play_resolver.py:923-927, 1328-1334` causing `is_touchdown=False` for red zone plays and zero stats in `_save_player_stats`.
  - [x] PAT & 2-point conversions: Identified hardcoded `+7` in `simulation_orchestrator.py:824-827` bypassing `TwoPointConversionCommand` and PAT logic.
  - [x] Deterministic seeded RNG vs unseeded random calls: Identified unseeded `import random` in `sack_calculator.py:98`, `position_physics.py:297, 303, 466, 594`, `quarterback.py:240`, `injury.py:411`.
  - [x] Quarter progression loop (Q1 -> Q4 + OT): Identified premature exit after Q1 in `simulation_orchestrator.py:474-477` and missing multi-quarter transition loop.
- [x] Investigate R3: Season Lifecycle, Offseason & RPG (`app/orchestrator/`, `app/rpg/`, `app/api/`, `app/services/`)
  - [x] Draft order calculation (`win_percentage` vs `win_pct`): Identified `standings.sort` in `offseason_service.py:205` referencing missing `x.win_pct` on `TeamStanding`.
  - [x] Traded draft pick ownership preservation (Rounds 1-7): Identified pick creation ignoring trades in `offseason_service.py:230-242` and `trades.py:346-367`.
  - [x] `/free-agency/simulate` route vs `FreeAgencyEngine` execution & salary cap: Identified primitive stub in `offseason_service.py:407-435` bypassing `FreeAgencyEngine.simulate_free_agency`.
  - [x] `WeekSimulator` duplicate `Game` row creation & missing `await save_game_result()`: Identified hardcoded `Game(season=2025, week=1)` in `simulation_orchestrator.py:81-93` and missing `save_game_result()` in `week_simulator.py:140-160`.
  - [x] `StandingsCalculator` head-to-head tiebreaker logic: Identified explicit omission of H2H in `standings_calculator.py:282-285`.
  - [x] `OffseasonPhase` state machine transitions & enforcement: Identified missing phase tracking on `Season` and missing sequential transition guards in `OffseasonService`.
- [ ] Synthesize findings and write `handoff.md`
- [ ] Send status message to orchestrator

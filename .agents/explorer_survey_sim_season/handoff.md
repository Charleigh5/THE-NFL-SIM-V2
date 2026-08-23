# Comprehensive Investigation Report: R2 (Simulation Engine & Physics) & R3 (Season Lifecycle & Offseason)

**Explorer Role**: Explorer 2 (Simulation Engine & Season Lifecycle Specialist)  
**Target Milestone**: Survey R2 & R3  
**Working Directory**: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_sim_season`  
**Date**: 2026-08-22  

---

## 1. Observation

Direct evidence gathered across the codebase:

### R2: Core Football Simulation & Physics Engine Correction

#### 1.1 Safety Calculation Bug (`yard_line <= 0` Awards Offensive Touchdown)
- **File**: `backend/app/orchestrator/simulation_orchestrator.py`
- **Lines 771–830 & 817**:
  ```python
  # Update yard line
  if self.possession == "home":
      self.yard_line += result.yards_gained
  else:
      self.yard_line -= result.yards_gained

  # Bounds check
  self.yard_line = max(0, min(100, self.yard_line))
  ...
  # Check for touchdown
  elif result.is_touchdown or self.yard_line >= 100 or self.yard_line <= 0:
      if self.possession == "home":
          self.home_score += 7
      else:
          self.away_score += 7
  ```
- **File**: `backend/app/orchestrator/play_resolver.py`
- **Lines 643–677**: On a sack, `_resolve_pass_play` returns:
  ```python
  return PlayResult(
      yards_gained=-loss_yards,
      is_touchdown=False,
      is_sack=True,
      description=f"SACKED! ...",
      headline=f"Sack! ...",
      is_highlight_worthy=True,
      injuries=injuries,
      passer_id=qb.id
  )
  ```
  `is_safety` is never calculated or set on sacks.
- **Lines 795–806** in `simulation_orchestrator.py`:
  ```python
  # Standard: Scored-upon team kicks off from 20
  # Flip possession first, then set yard line
  self.possession = "away" if self.possession == "home" else "home"
  self.yard_line = 35 # Should be 20 for safety kick, but using 35 (kickoff default) for now
  self.yard_line = 25
  ```

#### 1.2 Play Clock Runoffs Defaulting to 40.0s
- **File**: `backend/app/schemas/play.py`
- **Line 13**:
  ```python
  class PlayResult(BaseModel):
      yards_gained: int
      is_touchdown: bool = False
      is_turnover: bool = False
      is_sack: bool = False
      is_penalty: bool = False
      is_safety: bool = False
      penalty_yards: int = 0
      time_elapsed: float = 40.0  # seconds
  ```
- **File**: `backend/app/orchestrator/play_resolver.py`
- **Lines 1017–1028, 1064–1072, 1095–1100, 1452–1462**:
  When `PlayResult` is instantiated for completed passes, interceptions, incomplete passes, and runs, `time_elapsed` is never specified and always falls back to the `40.0`s default.
- **File**: `backend/app/orchestrator/play_commands.py`
- **Lines 112–115, 148–151, 218–221**:
  `KickoffCommand`, `PuntCommand`, and `FieldGoalCommand` instantiate `PlayResult` without specifying `time_elapsed`, thus consuming 40s per kick/punt.

#### 1.3 Red Zone Touchdown Player Stat Attribution
- **File**: `backend/app/orchestrator/play_resolver.py`
- **Lines 922–928**:
  ```python
  # Touchdown check
  is_touchdown = False
  if yards_gained > 80:
      is_touchdown = True
  elif yards_gained > 20 and ProbabilityEngine.resolve_outcome(self.rng, 0.1):
      is_touchdown = True
  ```
- **Lines 1328–1334**:
  ```python
  is_touchdown = False
  if yards_gained > 80:
      is_touchdown = True
  elif yards_gained > 15 and yards_gained >= (100 - 20):
       # Simplified red zone logic
       pass
  ```
- **File**: `backend/app/orchestrator/simulation_orchestrator.py`
- **Lines 312–343**:
  ```python
  for play in self.history:
      if play.passer_id:
          s = get_stats(play.passer_id)
          ...
          if play.is_touchdown:
              s["pass_tds"] += 1
      if play.rusher_id:
          s = get_stats(play.rusher_id)
          ...
          if play.is_touchdown:
              s["rush_tds"] += 1
      if play.receiver_id:
          s = get_stats(play.receiver_id)
          ...
          if play.is_touchdown:
              s["rec_tds"] += 1
  ```
  Because `play.is_touchdown` is `False` for red zone plays (e.g. 5-yard TD pass), `pass_tds`, `rush_tds`, and `rec_tds` are NEVER credited to the players.

#### 1.4 Hardcoded PAT & 2-Point Conversion Logic
- **File**: `backend/app/orchestrator/simulation_orchestrator.py`
- **Lines 824–837**:
  ```python
  if self.possession == "home":
      self.home_score += 7
  else:
      self.away_score += 7

  # 2-Point Conversion Logic (GAME-012)
  # Basic stub for decision making (Go for 1 vs 2)
  # In a real loop, we would insert a TwoPointConversionCommand here.
  ```
  Every touchdown automatically adds 7 points to the score, bypassing `TwoPointConversionCommand` and PAT execution.

#### 1.5 Deterministic Seeded RNG vs Unseeded Global `random` Calls
- **Files with unseeded `import random` calls during simulation**:
  1. `backend/app/engine/sack_calculator.py:3, 98`:
     ```python
     def resolve_sack_outcome(qb: Player, sack_prob: float) -> str:
         roll = random.random()
         if roll < sack_prob:
             return "SACK"
         return "PRESSURE_AVOIDED"
     ```
  2. `backend/app/engine/position_physics.py:297, 303, 466, 594`:
     ```python
     def _simulate_stiff_arm_battle(self, defender_tackle: int) -> bool:
         import random
         stiff_arm_chance = self.stiff_arm / (self.stiff_arm + defender_tackle)
         return random.random() < stiff_arm_chance

     def _check_fumble(self, force_ratio: float) -> bool:
         import random
         fumble_chance = 0.02 * force_ratio
         return random.random() < fumble_chance
     ```
  3. `backend/app/engine/position_physics/quarterback.py:240–243`:
     ```python
     if rng:
         angle = rng.next_float() * 360.0
         deviation = rng.next_float() * accuracy_radius
     else:
         import random
         angle = random.random() * 360.0
         deviation = random.random() * accuracy_radius
     ```
  4. `backend/app/engine/genesis/injury.py:411, 479`:
     ```python
     if self.rng:
         roll = self.rng.next_float()
     else:
         import random
         roll = random.random()
     ```
  5. Duplicated `DeterministicRNG` classes: `app/core/random_utils.py` (wraps `random.Random` with SHA-256 seeding) vs `app/engine/core/deterministic_rng.py` (HMAC-SHA256 CSPRNG).

#### 1.6 Quarter Progression & Simulation Loop (`Q1 -> Q4 + OT`)
- **File**: `backend/app/orchestrator/simulation_orchestrator.py`
- **Lines 454–479**:
  ```python
  for play_num in range(num_plays):
      if not self.is_running:
          break
      result = await self._execute_single_play()
      ...
      # Check if quarter/game is over
      if self._is_quarter_over():
          logger.info("Quarter complete", extra={"quarter": self.current_quarter})
          break

  self.is_running = False
  await self.save_game_result()
  ```
  When Q1 reaches `0:00`, `_is_quarter_over()` returns `True`, immediately breaking out of the loop and finalizing the game at Q1.

---

### R3: Season Lifecycle, Offseason & RPG Repair

#### 2.1 Draft Order Attribute Collision (`win_percentage` vs `win_pct`)
- **File**: `backend/app/services/offseason_service.py`
- **Line 205**:
  ```python
  standings.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential))
  ```
- **File**: `backend/app/services/standings_calculator.py`
- **Lines 9–25**:
  ```python
  class TeamStanding(BaseModel):
      model_config = ConfigDict(from_attributes=True)
      team_id: int
      team_name: str
      team_abbreviation: str
      conference: str
      division: str
      wins: int
      losses: int
      ties: int
      win_percentage: float  # <--- named win_percentage, not win_pct
      points_for: int
      points_against: int
      point_differential: int
  ```
  Causes `AttributeError: 'TeamStanding' object has no attribute 'win_pct'`.

#### 2.2 Traded Draft Pick Ownership Preservation (Rounds 1–7)
- **File**: `backend/app/services/offseason_service.py`
- **Lines 230–242**:
  ```python
  # Create Picks
  for round_num in range(1, 8):
      for i, team_id in enumerate(ordered_team_ids):
          pick = DraftPick(
              season_id=season_id,
              team_id=team_id,
              original_team_id=team_id,
              round=round_num,
              pick_number=(round_num - 1) * 32 + (i + 1),
              player_id=None
          )
          self.db.add(pick)
  ```
  `generate_draft_order` blindly creates new picks where `team_id = team_id` (original team) for all rounds 1–7.
- **File**: `backend/app/api/endpoints/trades.py`
- **Lines 346–367**:
  When a trade offer is accepted, only player team IDs are swapped (`player.team_id = ...`). `offer.offered_picks` and `offer.requested_picks` are completely ignored, and no pick ownership records are modified or created.

#### 2.3 `/free-agency/simulate` Route vs `FreeAgencyEngine`
- **File**: `backend/app/api/endpoints/season.py`
- **Lines 877–890**:
  ```python
  @router.post("/{season_id}/free-agency/simulate")
  @handle_errors
  async def simulate_free_agency(season_id: int, db: AsyncSession = Depends(get_async_db)):
      def fa_sync():
          with SessionLocal() as sync_db:
              service = OffseasonService(sync_db)
              return service.simulate_free_agency(season_id)

      result = await run_in_threadpool(fa_sync)
      return result
  ```
- **File**: `backend/app/services/offseason_service.py`
- **Lines 407–435**:
  ```python
  def simulate_free_agency(self, season_id: int) -> dict:
      """Fill rosters with free agents."""
      # Assigns unassigned players 1-year contracts with no salary cap calculations
      ...
      return {"message": "Free Agency simulated."}
  ```
  Bypasses `FreeAgencyEngine` in `app/services/free_agency_engine.py`, which implements full multi-wave market bidding, team interest valuation, salary cap tracking (`team.salary_cap_space`), `PlayerContract` creation, and returns `List[FreeAgentSigning]`.

#### 2.4 `WeekSimulator` Duplicate `Game` Rows & Missing `await save_game_result()`
- **File**: `backend/app/services/week_simulator.py`
- **Lines 131–151**:
  ```python
  # Start game session (this will create/update db entry)
  await orchestrator.start_new_game_session(
      home_team_id=game.home_team_id,
      away_team_id=game.away_team_id,
      config={"fast_sim": use_fast_sim, "weather": weather_config},
      db_session=self.db
  )

  # Run simulation asynchronously
  await self._run_simulation(orchestrator, play_count)

  # Update the original game record with the results
  game.is_played = True
  game.home_score = orchestrator.home_score
  game.away_score = orchestrator.away_score
  ...
  await self.db.commit()
  ```
- **File**: `backend/app/orchestrator/simulation_orchestrator.py`
- **Lines 80–93**:
  ```python
  if self.db_session:
      new_game = Game(
          home_team_id=home_team_id,
          away_team_id=away_team_id,
          date=datetime.datetime.now(datetime.UTC),
          season=2025,
          week=1,
          is_played=False,
          game_data={"config": config} if config else {}
      )
      self.db_session.add(new_game)
      await self.db_session.commit()
      await self.db_session.refresh(new_game)
      self.current_game_id = new_game.id
  ```
  `start_new_game_session` unconditionally creates and commits a duplicate `Game(season=2025, week=1)` row for every game simulated. Furthermore, `WeekSimulator` never calls `await orchestrator.save_game_result()`, which means `_save_player_stats()` and `_update_elo_ratings()` are NEVER executed during week simulations.

#### 2.5 `StandingsCalculator` Omission of Head-to-Head Tiebreaker
- **File**: `backend/app/services/standings_calculator.py`
- **Lines 277–306**:
  ```python
  def _make_sort_key(self, team: Dict, all_teams_in_group: List[Dict], group_type: str):
      # 1. Win Percentage
      win_pct = team['win_percentage']

      # 2. Head-to-Head (Simplified: win % against other tied teams)
      # This is hard to do in a single key because it depends on who you are tied with.
      # We will skip complex H2H in the key and rely on Division/Conf record.

      div_pct = team['division_win_pct'] if group_type == 'division' else 0
      conf_pct = team['conference_win_pct']
      sos = team['strength_of_schedule']
      diff = team['point_differential']

      if group_type == 'division':
          return (win_pct, div_pct, conf_pct, sos, diff)
      else:
          is_div_winner = 1 if team.get('division_rank') == 1 else 0
          return (is_div_winner, win_pct, conf_pct, sos, diff)
  ```
  Head-to-head is explicitly bypassed in the sort key, causing teams tied in win percentage to be sorted by division/conference record or point differential rather than head-to-head outcome.

#### 2.6 `OffseasonPhase` Missing State Tracking and Enforcement
- **File**: `backend/app/models/season.py`
- **Lines 6–32**: `SeasonStatus` enum only defines `PRE_SEASON`, `REGULAR_SEASON`, `POST_SEASON`, `OFF_SEASON`. There is no `offseason_phase` field or sub-state machine to prevent calling `simulate_draft` or `simulate_free_agency` out of order.

---

## 2. Logic Chain

```
[Observation 1.1: yard_line <= 0 in simulation_orchestrator.py:817]
  -> Home offense moves from 0 to 100.
  -> Sack/Tackle in home own endzone reduces yard_line to <= 0.
  -> Line 817 treats (self.yard_line <= 0) as an offensive Touchdown (+7 points to Home).
  -> Consequence: Sacking the offense in their own endzone gives the offense 7 points instead of awarding 2 points to the defense and a free kick from the 20.

[Observation 1.2: PlayResult.time_elapsed = 40.0s default in play.py:13]
  -> PlayResolver does not set time_elapsed for incomplete passes, completions, sacks, runs, or special teams.
  -> Every play consumes 40.0s.
  -> Consequence: Incomplete passes burn 40 seconds of game clock instead of stopping the clock after 4-7 seconds.

[Observation 1.3: play_resolver.py:924 checks yards_gained > 80 for Touchdown]
  -> Plays inside the red zone (e.g. 5-yard TD pass) have yards_gained < 80 and are flagged is_touchdown = False.
  -> SimulationOrchestrator._save_player_stats only increments pass_tds/rush_tds/rec_tds if play.is_touchdown is True.
  -> Consequence: Players receive 0 TD stats for all red zone touchdowns.

[Observation 1.4: simulation_orchestrator.py:825 does score += 7]
  -> PAT and 2-point conversions are skipped with a comment stub.
  -> Consequence: Scores only increment in increments of 7, never reflecting missed PATs or successful 2-point conversions.

[Observation 1.5: sack_calculator.py:98 & position_physics.py use random.random()]
  -> Calls to global random bypass the session DeterministicRNG instance.
  -> Consequence: Repeated runs with the exact same game seed yield divergent results.

[Observation 1.6: simulation_orchestrator.py:474 breaks out on _is_quarter_over()]
  -> run_continuous_simulation stops as soon as Quarter 1 reaches 0:00.
  -> Consequence: Games terminate after 1 quarter; Q2-Q4 and OT never simulate.

[Observation 2.1: offseason_service.py:205 sorts on x.win_pct]
  -> TeamStanding schema defines win_percentage, not win_pct.
  -> Consequence: generate_draft_order crashes with AttributeError.

[Observation 2.2: offseason_service.py:233 hardcodes DraftPick(team_id=team_id)]
  -> Trades accepted in trades.py:346 do not update DraftPick ownership.
  -> Consequence: Traded draft pick assets are completely lost when draft order is generated.

[Observation 2.3: season.py:877 calls OffseasonService.simulate_free_agency]
  -> OffseasonService has a dummy stub that assigns 1-year contracts with no cap tracking.
  -> Consequence: FreeAgencyEngine (which has multi-wave bidding, interest calculation, salary cap updates) is never executed.

[Observation 2.4: simulation_orchestrator.py:81 creates Game(season=2025, week=1)]
  -> start_new_game_session does not accept an existing game_id.
  -> WeekSimulator simulates scheduled games by calling start_new_game_session, creating duplicate dummy rows for every game, and never calls save_game_result().
  -> Consequence: Database bloat with orphan 2025 Week 1 games, and player stats/Elo are never saved.

[Observation 2.5: standings_calculator.py:282 explicitly skips H2H in sort key]
  -> Teams with equal win percentage are ranked by division/conference record and point differential.
  -> Consequence: A team that won the head-to-head matchup can be ranked behind the team it defeated.

[Observation 2.6: Season model lacks OffseasonPhase tracking]
  -> No guard exists to ensure retirements -> free agency -> draft -> rookie signings occur in sequence.
  -> Consequence: Offseason steps can be called out of order.
```

---

## 3. Caveats

1. **Deterministic RNG Implementation**: Two classes named `DeterministicRNG` exist (`app/core/random_utils.py` and `app/engine/core/deterministic_rng.py`). `SimulationOrchestrator` uses `app.core.random_utils.DeterministicRNG` which wraps `random.Random(sha256(seed))`. All subcomponents (`PlayResolver`, `SackCalculator`, `PositionPhysics`, `InjurySystem`) should consistently accept and use this instance.
2. **Database Migrations for OffseasonPhase**: Adding an `offseason_phase` column to `Season` will require registering the field in Alembic metadata or using the existing `Season.game_data` JSON field / state machine if schema changes are constrained.
3. **Async vs Sync Sessions**: `OffseasonService`, `FreeAgencyEngine`, and `StandingsCalculator` currently use synchronous `Session`, while endpoints run them via `run_in_threadpool(sync_func)`. When refactoring, ensure sessions are cleanly opened and closed in worker threads.

---

## 4. Conclusion & Recommended Surgical Fix Strategies

### Summary of Targeted Fixes

| Topic | File(s) | Root Cause | Surgical Fix Strategy |
|---|---|---|---|
| **Safety Calculation** | `simulation_orchestrator.py:771–830`, `play_resolver.py:643–677` | `yard_line <= 0` lumped into TD check; sacks don't compute `is_safety` | Separate safety check: for home offense, `yard_line <= 0` or `result.is_safety` gives away team 2 points and sets field position at 35 (free kick from 20). For away offense, `yard_line >= 100` gives home team 2 points. Sacks in endzone set `is_safety = True`. |
| **Play Clock Runoffs** | `schemas/play.py:13`, `play_resolver.py:547–1463`, `play_commands.py` | Default `time_elapsed = 40.0s` used everywhere | Explicitly set `time_elapsed`: incomplete pass 4–7s, out of bounds 5–8s, in-bounds 25–38s, sacks 6–9s, special teams 5–8s. |
| **Red Zone TD Stat Attribution** | `play_resolver.py:922–942, 1328–1380`, `simulation_orchestrator.py:276–380` | `is_touchdown` only checks `yards_gained > 80`, ignoring goal line inside red zone | Compute `is_touchdown = (yards_gained >= distance_to_goal)` in resolver; ensure `result.is_touchdown = True` on all scoring plays so `_save_player_stats` increments `pass_tds`, `rush_tds`, and `rec_tds`. |
| **PAT / 2-Pt Conversions** | `simulation_orchestrator.py:824–837` | Touchdowns hardcode `+7` points directly | TD awards +6 points; execute PAT (1 pt with ~94-95% probability or kicker rating) or 2-pt conversion (2 pts with ~45% probability); adjust scoreboard accordingly. |
| **Deterministic Seeded RNG** | `sack_calculator.py:98`, `position_physics.py:297, 303`, `quarterback.py:240`, `injury.py:411` | Unseeded global `random` calls in sub-calculators | Pass `rng: DeterministicRNG` into `SackCalculator.resolve_sack_outcome` and position physics methods; eliminate unseeded `random.random()`. |
| **Quarter Progression (Q1–Q4 + OT)** | `simulation_orchestrator.py:429–480` | `run_continuous_simulation` breaks out on Q1 end | Loop quarters 1 through 4. Reset clock to 15:00 between quarters; handle halftime kickoff; if tied after Q4, enter Overtime (Q5, 10:00 clock, NFL regular season OT rules). |
| **Draft Order Win % Attribute** | `offseason_service.py:205`, `standings_calculator.py:9–34` | `x.win_pct` used instead of `x.win_percentage` | Change `x.win_pct` to `x.win_percentage` in `offseason_service.py:205`; add `win_pct` property on `TeamStanding` for safety. |
| **Traded Draft Picks** | `offseason_service.py:230–242`, `trades.py:346–367` | Traded picks ignored on trade accept and during draft generation | In `trades.py`, record draft pick ownership transfer on trade accept; in `generate_draft_order`, preserve traded pick assignments (`team_id != original_team_id`). |
| **Free Agency Engine Execution** | `season.py:877–890`, `offseason_service.py:407–435` | Route calls dummy stub instead of `FreeAgencyEngine` | Delegate `simulate_free_agency` to `FreeAgencyEngine(self.db).simulate_free_agency(season_id)`, updating player contracts and team salary cap spaces. |
| **Duplicate Game Rows in Week Sim** | `week_simulator.py:131–151`, `simulation_orchestrator.py:80–93` | `start_new_game_session` unconditionally inserts dummy `Game(season=2025, week=1)` | Allow `start_new_game_session` to attach to an existing `game_id`; in `WeekSimulator`, pass existing `game.id` and call `await orchestrator.save_game_result()`. |
| **Head-to-Head Tiebreakers** | `standings_calculator.py:277–306` | Head-to-head explicitly skipped in `_make_sort_key` | Implement head-to-head tiebreaker logic in `_rank_group` (evaluating wins among tied teams before division/conference record and point differential). |
| **OffseasonPhase State Machine** | `models/season.py`, `offseason_service.py:25–56` | No phase tracking or transition guards | Add `OffseasonPhase` enum (`RETIREMENTS`, `RESIGNINGS`, `FREE_AGENCY`, `DRAFT`, `ROOKIE_SIGNINGS`, `TRAINING_CAMP`, `COMPLETED`) with state transition enforcement. |

---

## 5. Verification Method

### Test Suite Execution Commands

1. **Football Engine & Physics Verification**:
   - Run existing and new test suites:
     ```powershell
     cd backend
     pytest tests/test_advanced_simulation_features.py -v
     pytest tests/test_engines.py -v
     pytest tests/integration/test_orchestrator_integration.py -v
     ```
   - **Safety Assertion**: Test with offense starting at own 5-yard line; sack for 7-yard loss -> assert defense awarded 2 points, possession flips, yard line becomes 35.
   - **Clock Runoff Assertion**: Simulate incomplete pass -> assert `result.time_elapsed >= 4.0` and `result.time_elapsed <= 7.0`.
   - **Red Zone TD Assertion**: Simulate pass from opponent's 5-yard line -> assert `result.is_touchdown == True`, `passer` receives +1 `pass_tds`, `receiver` receives +1 `rec_tds`.
   - **Deterministic Seed Assertion**: Run `SimulationOrchestrator` twice with seed `42` -> assert identical play history checksums across all 100 plays.
   - **Full Game Simulation Assertion**: Run continuous simulation -> assert game completes all 4 quarters with `current_quarter >= 4`.

2. **Season Lifecycle & Offseason Verification**:
   - Run offseason tests:
     ```powershell
     cd backend
     pytest tests/test_draft_logic.py -v
     pytest tests/test_season_api.py -v
     ```
   - **Draft Order Assertion**: Call `generate_draft_order(season_id)` -> assert no `AttributeError` on `win_pct`.
   - **Free Agency Engine Assertion**: Call `POST /api/season/{id}/free-agency/simulate` -> assert returned list contains `FreeAgentSigning` objects with valid salaries and `team.salary_cap_space` updated.
   - **Week Simulator Game Row Assertion**: Run `WeekSimulator.simulate_week(season_id, 1)` -> assert query for `Game.season == 2025, Game.week == 1` does not contain duplicate phantom rows, and `PlayerGameStats` rows exist for the week's games.
   - **Standings Tiebreaker Assertion**: Create 2 teams with identical 10-7 records where Team A beat Team B head-to-head -> assert Team A is ranked higher than Team B regardless of point differential.

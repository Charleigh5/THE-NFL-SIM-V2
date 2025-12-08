# Phase 7: Deep Engine Integration - Masterclass Task List

**Objective:** Connect the "Macro" Simulation (League, Standings, Schedules) with the "Micro" Simulation (Physics, Biology, AI) by hydrating the Engine with real database data.

**Current Problem:** The simulation runs with placeholder data - random outcomes instead of attribute-based calculations, empty player lists, and hardcoded player IDs.

**Success Criteria:**
- A "Fast WR" (99 Speed) beats a "Slow CB" (80 Speed) on deep balls >80% of the time
- A "Tired RB" (High Fatigue) fumbles more often than a fresh RB
- Teams call "Hail Mary" when losing with <10 seconds left (Cortex AI)
- All 22 players on field use their real attributes in every play outcome

---

## Task 7.1: Match Context & Roster Loading System

### 7.1.1: Design Match Context Architecture
- [x] Review current `SimulationOrchestrator` implementation
- [x] Design `MatchContext` class structure with these components:
  - [x] Home team roster dictionary (player_id → Player object)
  - [x] Away team roster dictionary (player_id → Player object)
  - [x] Active fatigue system (GenesisKernel instance)
  - [x] Active AI system (CortexSystem instance)
  - [x] Current formation data (offense/defense)
  - [x] Substitution tracking (starters vs backups)
- [x] Document class diagram and data flow
- [x] Create interface specifications for other systems

### 7.1.2: Create Match Context Class
**File:** `backend/app/orchestrator/match_context.py` (NEW)

- [ ] Create `MatchContext` class with constructor accepting home/away teams
- [ ] Implement `load_roster(team_id: int) -> Dict[int, Player]` method
  - [ ] Query database for all players on team
  - [ ] Convert to dictionary indexed by player_id
  - [ ] Include all relevant player attributes (speed, strength, fatigue, etc.)
- [ ] Implement `initialize_systems()` method
  - [ ] Create GenesisKernel instance with all players
  - [ ] Create CortexSystem instance with team coaches
  - [ ] Set initial fatigue states to zero
- [ ] Implement `get_fielded_players(side: str, formation: str) -> List[Player]`
  - [ ] Pull 11 starters based on depth chart
  - [ ] Handle special teams formations
  - [ ] Return Player objects with current fatigue levels
- [ ] Add error handling for missing players or incomplete rosters
- [ ] Write unit tests for MatchContext class

### 7.1.3: Create Depth Chart Service
**File:** `backend/app/services/depth_chart_service.py` (NEW)

- [x] Create `DepthChartService` class
- [x] Implement `get_starting_offense(team_id: int, formation: str) -> Dict[str, Player]`
  - [x] Query depth chart for offensive positions
  - [x] Return dict with positions: QB, RB, WR1, WR2, WR3, TE, LT, LG, C, RG, RT
  - [x] Handle different formations (I-Formation, Shotgun, etc.)
- [x] Implement `get_starting_defense(team_id: int, formation: str) -> Dict[str, Player]`
  - [x] Query depth chart for defensive positions
  - [x] Return dict with positions: DE, DT, LB, CB, S
  - [x] Handle different schemes (4-3, 3-4, Nickel, Dime)
- [x] Implement `get_backup(position: str, depth: int) -> Player`
  - [x] Handle injuries and substitutions
  - [x] Return next player on depth chart
- [x] Add fallback logic for missing depth chart entries
- [x] Write unit tests for depth chart retrieval

### 7.1.4: Integrate Match Context with Orchestrator
**File:** `backend/app/orchestrator/simulation_orchestrator.py` (MODIFY)

- [ ] Import `MatchContext` class
- [ ] Modify `start_new_game_session()` method:
  - [ ] Create MatchContext instance with home/away teams
  - [ ] Call `initialize_systems()` on MatchContext
  - [ ] Store MatchContext as instance variable
- [ ] Modify `_execute_single_play()` method:
  - [ ] Get fielded players from MatchContext
  - [ ] Pass player lists to PlayResolver
  - [ ] Remove empty list `[]` placeholders
- [ ] Update `_handle_play_result()` to update fatigue in MatchContext
- [ ] Add cleanup method to release MatchContext after game ends
- [ ] Write integration tests for orchestrator with MatchContext

### 7.1.5: Update Database Models (if needed)
**Files:** `backend/app/models/depth_chart.py`, `backend/app/models/player.py`

- [ ] Check if `DepthChart` model exists
  - [ ] If not, create model with: team_id, position, player_id, depth_order
- [ ] Verify `Player` model has all required attributes:
  - [ ] Physical: speed, strength, agility, stamina
  - [ ] Mental: awareness, play_recognition
  - [ ] Position-specific: throw_power, route_running, man_coverage, etc.
- [ ] Create Alembic migration if schema changes needed
- [ ] Run migration on test database
- [ ] Seed depth charts for all 32 teams

---

## Task 7.2: Kernel Registration & Fatigue System

### 7.2.1: Enhance Genesis Kernel for Multi-Player Tracking
**File:** `backend/app/engine/kernels/genesis.py` (MODIFY)

- [ ] Review current GenesisKernel implementation
- [ ] Modify `register_player()` to accept Player object
- [ ] Update internal state to track fatigue per player_id:
  - [ ] Replace single fatigue value with `Dict[int, float]`
  - [ ] Initialize all players at 0.0 fatigue
- [ ] Implement `get_player_fatigue(player_id: int) -> float`
- [ ] Implement `update_fatigue(player_id: int, delta: float)`
- [ ] Implement `reset_all_fatigue()` for halftime/end of game
- [ ] Add fatigue recovery during timeouts and between plays
- [ ] Write unit tests for multi-player fatigue tracking

### 7.2.2: Integrate Genesis Kernel with PlayResolver
**File:** `backend/app/orchestrator/play_resolver.py` (MODIFY)

- [ ] Remove hardcoded `player_id=1` references
- [ ] Accept `genesis_kernel` instance in constructor or method params
- [ ] Modify `_resolve_run_play()`:
  - [ ] Accept RB and defensive players as parameters
  - [ ] Get RB fatigue from GenesisKernel
  - [ ] Apply fatigue penalty to RB effectiveness
  - [ ] Update RB fatigue after play
- [ ] Modify `_resolve_pass_play()`:
  - [ ] Accept QB, WR, CB as parameters
  - [ ] Get QB fatigue from GenesisKernel
  - [ ] Apply fatigue penalty to throw accuracy
  - [ ] Update QB fatigue after play
- [ ] Implement position group fatigue (entire O-Line fatigues together)
- [ ] Write integration tests with GenesisKernel

### 7.2.3: Add Fatigue Visualization (Optional)
**File:** `frontend/src/components/game/FatigueIndicator.tsx` (NEW)

- [ ] Create React component to display player fatigue levels
- [ ] Show color-coded fatigue bars (green → yellow → red)
- [ ] Display during live simulation
- [ ] Add to player profile pages
- [ ] Style component for visual clarity

---

## Task 7.3: Attribute-Based Play Resolution

### 7.3.1: Design Probability Engine
**File:** `backend/app/engine/probability_engine.py` (NEW)

- [ ] Create `ProbabilityEngine` class
- [ ] Implement `calculate_success_chance(attacker_attrs, defender_attrs, context) -> float`
  - [ ] Compare relevant attributes (speed vs speed, strength vs strength)
  - [ ] Apply contextual modifiers (weather, fatigue, field position)
  - [ ] Return probability between 0.0 and 1.0
- [ ] Implement attribute comparison formulas:
  - [ ] Speed differential: `(attacker.speed - defender.speed) / 100`
  - [ ] Strength differential: `(attacker.strength - defender.strength) / 100`
  - [ ] Skill differential: position-specific comparisons
- [ ] Add randomness with controlled variance
- [ ] Write unit tests for probability calculations

### 7.3.2: Refactor Pass Play Resolution
**File:** `backend/app/orchestrator/play_resolver.py` (MODIFY)

- [ ] Import `ProbabilityEngine`
- [ ] Modify `_resolve_pass_play(qb, receiver, defenders, context)`:
  - [ ] Remove `random.random() < 0.6` logic
  - [ ] Get QB attributes: throw_power, throw_accuracy, current_fatigue
  - [ ] Get WR attributes: speed, route_running, catch_rating
  - [ ] Get CB attributes: speed, man_coverage, zone_coverage
  - [ ] Calculate base completion chance using ProbabilityEngine
  - [ ] Apply modifiers:
    - [ ] Weather impact (wind reduces accuracy)
    - [ ] Pressure impact (defenders near QB)
    - [ ] Fatigue penalty (QB and WR)
  - [ ] Determine outcome based on final probability
  - [ ] Calculate yards gained using player attributes vs defenders
- [ ] Add logging for attribute comparisons (debug mode)
- [ ] Write unit tests for attribute-based pass resolution

### 7.3.3: Refactor Run Play Resolution
**File:** `backend/app/orchestrator/play_resolver.py` (MODIFY)

- [ ] Modify `_resolve_run_play(rb, offensive_line, defenders, context)`:
  - [ ] Remove random logic
  - [ ] Get RB attributes: speed, elusiveness, power, vision
  - [ ] Get O-Line attributes: run_blocking (average of all linemen)
  - [ ] Get defensive front attributes: run_defense, tackling
  - [ ] Calculate success using ProbabilityEngine:
    - [ ] O-Line blocking vs D-Line penetration
    - [ ] RB speed/power vs LB tackling
    - [ ] RB elusiveness vs CB pursuit angles
  - [ ] Determine yards gained based on attribute matchups
  - [ ] Apply fatigue effects to RB and O-Line
- [ ] Add fumble chance based on RB ball security vs defender hit power
- [ ] Write unit tests for run play outcomes

### 7.3.4: Add Advanced Play Outcomes
**Files:** `backend/app/orchestrator/play_resolver.py` (MODIFY)

- [ ] Implement `calculate_yards_after_catch(wr, defenders)`:
  - [ ] Compare WR speed to pursuing defenders
  - [ ] Apply breaking tackles logic (WR strength vs tacklers)
  - [ ] Add elusiveness bonus for open field
- [ ] Implement `calculate_sack_outcome(qb, pass_rushers, pocket_time)`:
  - [ ] Compare pass rush vs O-Line pass blocking
  - [ ] Apply QB awareness to escape pressure
  - [ ] Add QB scrambling ability
- [ ] Implement `calculate_interception_chance(qb, cb, throw_difficulty)`:
  - [ ] Poor throws (low accuracy) increase INT chance
  - [ ] CB play_recognition affects reaction time
  - [ ] CB catch_rating affects securing INT
- [ ] Write comprehensive tests for all outcome types

### 7.3.5: Create Verification Script
**File:** `backend/verify_attribute_impact.py` (MODIFY/ENHANCE)

- [ ] Enhance existing script to test Phase 7 changes
- [ ] Test fast WR vs slow CB matchup (should win 80%+)
- [ ] Test strong RB vs weak defense (should gain more yards)
- [ ] Test tired QB vs fresh QB (completion % should drop)
- [ ] Generate detailed report with statistics
- [ ] Run script and document results

---

## Task 7.4: Cortex (AI) Integration

### 7.4.1: Enhance Cortex System
**File:** `backend/app/engine/kernels/cortex.py` (MODIFY)

- [ ] Review current Cortex implementation
- [ ] Create `GameSituation` dataclass:
  - [ ] down: int
  - [ ] distance: int
  - [ ] field_position: int
  - [ ] time_remaining: int
  - [ ] score_differential: int
  - [ ] quarter: int
- [ ] Implement `call_play(situation: GameSituation, coach_style: str) -> str`
  - [ ] Load coach tendencies from database or config
  - [ ] Analyze situation context
  - [ ] Return play type: "RUN", "PASS_SHORT", "PASS_DEEP", "FG", "PUNT"
- [ ] Add play-calling logic for common situations:
  - [ ] 3rd & Long → Pass likely (70%+ chance)
  - [ ] 3rd & Short → Run or short pass (balanced)
  - [ ] 4th & inches → Go for it if aggressive coach
  - [ ] 4th & long → Punt unless desperate
  - [ ] Red zone → Higher run percentage
  - [ ] 2-minute drill → Pass-heavy, sideline routes
- [ ] Write unit tests for play-calling logic

### 7.4.2: Add Coach Attributes and Philosophies
**Files:** `backend/app/models/coach.py`, Database schema

- [ ] Check if `Coach` model exists
  - [ ] If not, create model with: name, team_id, philosophy attributes
- [ ] Add coach attributes:
  - [ ] aggressiveness: int (0-100) - 4th down decisions
  - [ ] pass_tendency: int (0-100) - pass vs run ratio
  - [ ] risk_tolerance: int (0-100) - trick plays, deep balls
  - [ ] clock_management: int (0-100) - timeout usage, hurry-up
- [ ] Create migration to add Coach table
- [ ] Seed database with 32 coaches (one per team)
- [ ] Assign varied philosophies (conservative, balanced, aggressive)

### 7.4.3: Integrate Cortex with Orchestrator
**File:** `backend/app/orchestrator/simulation_orchestrator.py` (MODIFY)

- [ ] Import Cortex system
- [ ] Modify `_execute_single_play()`:
  - [ ] Remove random play type selection
  - [ ] Build GameSituation from current game state
  - [ ] Get home coach and away coach from database
  - [ ] Call `cortex.call_play()` for offensive team
  - [ ] Use returned play type for PlayResolver
- [ ] Add logging for AI decisions (debug mode)
- [ ] Verify play-calling makes sense in context
- [ ] Write integration tests

### 7.4.4: Add Special Situation Logic
**File:** `backend/app/engine/kernels/cortex.py` (MODIFY)

- [ ] Implement `should_go_for_it(situation, coach) -> bool`:
  - [ ] Consider field position (own 40 vs opponent 40)
  - [ ] Consider score differential (losing = more aggressive)
  - [ ] Consider time remaining (desperate situations)
  - [ ] Apply coach aggressiveness modifier
- [ ] Implement `should_use_timeout(situation, timeouts_left) -> bool`:
  - [ ] 2-minute drill situations
  - [ ] Prevent delay of game
  - [ ] Ice the kicker (defensive timeout)
- [ ] Implement `select_play_after_turnover(situation) -> str`:
  - [ ] Conservative if good field position
  - [ ] Aggressive if near end zone
- [ ] Write tests for special situation logic

### 7.4.5: Create AI Verification Script
**File:** `backend/verify_ai_decisions.py` (NEW)

- [ ] Create script to test Cortex decision-making
- [ ] Test scenario: 4th & 1 at midfield, tied game, 2:00 left
  - [ ] Aggressive coach: Goes for it
  - [ ] Conservative coach: Punts
- [ ] Test scenario: 4th & 10 at opponent 35, down by 3, 0:10 left
  - [ ] Should attempt field goal
- [ ] Test scenario: 4th & 15 at own 20, down by 7, 0:05 left
  - [ ] Should attempt Hail Mary
- [ ] Generate report with AI decision accuracy
- [ ] Run and document results

---

## Task 7.5: Integration & End-to-End Testing

### 7.5.1: Create Full Integration Test
**File:** `backend/tests/test_phase7_integration.py` (NEW)

- [ ] Write test that simulates full game with Phase 7 features:
  - [ ] Initialize two teams with full rosters
  - [ ] Create MatchContext
  - [ ] Run 10+ plays with real player data
  - [ ] Verify player fatigue accumulates
  - [ ] Verify AI makes sensible play calls
  - [ ] Verify attribute-based outcomes
- [ ] Add assertions for expected behavior:
  - [ ] Fast players should gain more yards
  - [ ] Tired players should perform worse
  - [ ] Play calls should match game situation
- [ ] Run test and ensure it passes

### 7.5.2: Performance Testing
**File:** `backend/tests/test_phase7_performance.py` (NEW)

- [ ] Test simulation speed with full player data:
  - [ ] Measure time to simulate single play
  - [ ] Measure time to simulate full quarter
  - [ ] Measure time to simulate full game
- [ ] Set performance benchmarks:
  - [ ] Single play: <100ms
  - [ ] Full quarter: <10 seconds
  - [ ] Full game: <60 seconds
- [ ] Identify performance bottlenecks if targets not met
- [ ] Optimize slow queries or calculations

### 7.5.3: Run All Verification Scripts
- [ ] Run `verify_gameplay_mechanics.py` - verify attributes matter
- [ ] Run `verify_fatigue_impact.py` - verify fatigue affects performance
- [ ] Run `verify_play_calling.py` - verify AI makes smart decisions
- [ ] Run `verify_attribute_impact.py` - verify specific matchups work
- [ ] Run `verify_ai_decisions.py` - verify special situations
- [ ] Run `simulate_full_game.py` - verify complete game works
- [ ] Document all results in `PHASE_7_VERIFICATION.md`

### 7.5.4: Update Documentation
- [ ] Update `docs/ARCHITECTURE.md` with Phase 7 changes
- [ ] Document MatchContext system
- [ ] Document Cortex AI decision-making
- [ ] Add diagrams showing data flow
- [ ] Update API documentation if endpoints changed
- [ ] Create Phase 7 completion report

---

## Task 7.6: Frontend Integration (Optional)

### 7.6.1: Enhance Live Simulation Display
**File:** `frontend/src/pages/LiveSim.tsx` (MODIFY)

- [ ] Display specific player names in play results
  - [ ] Show "K. Murray passes to D. Hopkins for 12 yards"
  - [ ] Instead of "Pass complete for 12 yards"
- [ ] Add player matchup preview before plays
- [ ] Show fatigue indicators during game
- [ ] Display AI reasoning for play calls (debug mode)

### 7.6.2: Add Advanced Statistics
**Files:** `frontend/src/components/stats/*` (NEW/MODIFY)

- [ ] Show player-specific game stats
- [ ] Track WR vs CB matchup statistics
- [ ] Display fatigue charts over time
- [ ] Add "key matchups" section highlighting speed differentials

---

## Estimated Timeline

- **Task 7.1**: 8-12 hours (Match Context & Roster Loading)
- **Task 7.2**: 4-6 hours (Kernel Registration & Fatigue)
- **Task 7.3**: 10-14 hours (Attribute-Based Play Resolution)
- **Task 7.4**: 6-8 hours (Cortex AI Integration)
- **Task 7.5**: 4-6 hours (Integration & Testing)
- **Task 7.6**: 4-6 hours (Frontend - Optional)

**Total Estimated Time:** 36-52 hours

---

## Success Metrics

After completion, verify:
- ✅ All plays use real player attributes (no more random outcomes)
- ✅ All 22 players on field are tracked with individual fatigue
- ✅ Fast players consistently outperform slow players
- ✅ Tired players show measurable performance degradation
- ✅ AI makes context-appropriate play calls (>90% sensible)
- ✅ Full game simulation completes without errors
- ✅ Performance targets met (<60s per full game)

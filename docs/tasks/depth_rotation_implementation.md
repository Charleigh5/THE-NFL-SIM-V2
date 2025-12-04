# Depth & Rotation System - Implementation Tasks

**Epic:** Multiple Elite Players at Same Position
**Based On:** NFL Depth & Rotation Research (Dec 2024)
**Priority:** HIGH - Core gameplay feature

---

## Overview

Implement a comprehensive depth chart and rotation system that moves beyond "starter/backup" to realistically simulate how modern NFL teams deploy multiple skilled players at the same position through personnel packages, situational usage, and fatigue management.

---

## Task Breakdown

### ✅ Phase 1: Foundation (Week 1-2)

#### Task 1.1: Database Schema Extensions

**Effort:** 2 days
**Dependencies:** None

- [ ] Create `personnel_package_catalog` table
- [ ] Create `player_role_assignments` table
- [ ] Create `game_rotation_states` table
- [ ] Create `player_snap_logs` table
- [ ] Create `coaching_schemes` table
- [ ] Write Alembic migration scripts
- [ ] Test migrations on dev database

**Files to Create:**

- `backend/app/models/personnel_package.py`
- `backend/app/models/rotation_state.py`
- `backend/alembic/versions/xxx_add_rotation_system.py`

---

#### Task 1.2: Core Data Models

**Effort:** 3 days
**Dependencies:** Task 1.1

- [ ] Implement `PersonnelPackage` Pydantic schema
- [ ] Implement `PlayerRole` Pydantic schema
- [ ] Implement `RotationState` Pydantic schema
- [ ] Implement `SnapLog` Pydantic schema
- [ ] Add validation logic for all models
- [ ] Write unit tests for model validation

**Files to Create:**

- `backend/app/schemas/personnel.py`
- `backend/app/schemas/rotation.py`

---

#### Task 1.3: Fatigue Calculation Engine

**Effort:** 3 days
**Dependencies:** Task 1.2

- [ ] Implement base fatigue calculation algorithm
- [ ] Add position-specific fatigue rates
- [ ] Implement consecutive snap penalty logic
- [ ] Add environmental factors (weather, altitude)
- [ ] Create fatigue recovery system (when player rests)
- [ ] Implement fatigue performance penalty calculation
- [ ] Write comprehensive unit tests

**Formula to Implement:**

```python
fatigue = (snap_percentage * 100 + consecutive_penalty) * stamina_modifier * position_modifier * environment_modifier
performance = base_rating * (1 - fatigue_penalty_curve(fatigue))
```

**Files to Create:**

- `backend/app/engine/fatigue_engine.py`
- `backend/tests/engine/test_fatigue_engine.py`

**Key Constants:**

```python
POSITION_FATIGUE_RATES = {
    "DL": 3.5, "EDGE": 3.0, "RB": 2.5, "TE": 2.2, "LB": 2.0,
    "CB": 1.8, "WR": 1.5, "S": 1.5, "OL": 1.0, "QB": 0.5
}
```

---

#### Task 1.4: Personnel Package Catalog

**Effort:** 2 days
**Dependencies:** Task 1.2

- [ ] Define all offensive personnel packages (11, 12, 10, 00, 21, 22, 13)
- [ ] Define all defensive personnel packages (base, nickel, dime, goal line)
- [ ] Set base frequencies from NFL research
- [ ] Configure down/distance modifiers
- [ ] Configure situational modifiers (score, time, field position)
- [ ] Write seed script to populate database
- [ ] Create API endpoint to retrieve package catalog

**Packages to Define:**

**Offense:**

- 11 Personnel (1 RB, 1 TE, 3 WR) - 65% frequency
- 12 Personnel (1 RB, 2 TE, 2 WR) - 20% frequency
- 10 Personnel (1 RB, 0 TE, 4 WR) - 10% frequency
- 21 Personnel (2 RB, 1 TE, 2 WR) - 3% frequency
- 00 Personnel (0 RB, 0 TE, 5 WR) - 2% frequency

**Defense:**

- Base (4-3 or 3-4) - 33% frequency
- Nickel (4-2-5) - 60% frequency
- Dime (4-1-6) - 7% frequency

**Files to Create:**

- `backend/app/data/personnel_packages.py`
- `backend/app/scripts/seed_personnel_packages.py`
- `backend/app/api/endpoints/personnel.py`

---

### ✅ Phase 2: Position-Specific Rotation Logic (Week 3-4)

#### Task 2.1: Running Back RBBC System

**Effort:** 4 days
**Dependencies:** Task 1.3, 1.4

- [ ] Implement RB role classification (Early Down, 3rd Down, Goal Line, Change of Pace)
- [ ] Create RB selection algorithm based on situation
- [ ] Implement carry-based fatigue (after 3-4 consecutive carries, force rotation)
- [ ] Add "hot hand" bonus (if RB averaging 5+ YPC, increase usage)
- [ ] Implement snap count distribution (target: RB1 55-65%, RB2 30-40%)
- [ ] Write integration tests for RBBC scenarios

**Key Algorithm:**

```python
def select_rb_for_play(game_state, depth_chart, rotation_state):
    if field_position <= 5:
        return best_goal_line_rb
    elif down == 3 and distance > 5:
        return best_third_down_rb
    elif consecutive_carries(current_rb) >= 4:
        return change_of_pace_rb
    else:
        return best_early_down_rb
```

**Files to Create:**

- `backend/app/engine/rotation/rb_rotation.py`
- `backend/tests/engine/rotation/test_rb_rotation.py`

---

#### Task 2.2: Wide Receiver Personnel Sets

**Effort:** 3 days
**Dependencies:** Task 1.4

- [ ] Implement WR role assignment (X, Z, Slot)
- [ ] Create package-based WR selection (11, 10, 12 personnel)
- [ ] Implement WR rotation logic (top 3 rarely rotate, WR4/5 in 4+ WR sets)
- [ ] Add skill-based role fit scoring (speed for X, agility for Slot)
- [ ] Target snap distribution (WR1/2/3: 85-95%, WR4: 20-30%)
- [ ] Write tests for different personnel package scenarios

**Files to Create:**

- `backend/app/engine/rotation/wr_rotation.py`
- `backend/tests/engine/rotation/test_wr_rotation.py`

---

#### Task 2.3: Defensive Line Heavy Rotation

**Effort:** 4 days
**Dependencies:** Task 1.3, 1.4

- [ ] Implement 8-man DL rotation system
- [ ] Force rotation after 6 consecutive snaps (aggressive fatigue)
- [ ] Target snap distribution (no DL over 65%)
- [ ] Prioritize fresh legs for 3rd downs
- [ ] Implement package-based DL deployment (base vs nickel vs dime)
- [ ] Add performance penalty for tired DL (reduced pass rush win rate)
- [ ] Write tests validating rotation keeps all DL fresh

**Key Logic:**

```python
# After every 5-8 snaps, rotate at least one DL
if consecutive_snaps(any_dl) >= 6:
    force_rotation()

# On 3rd down, ensure best pass rushers are fresh
if down == 3:
    deploy_best_fresh_pass_rushers()
```

**Files to Create:**

- `backend/app/engine/rotation/dl_rotation.py`
- `backend/tests/engine/rotation/test_dl_rotation.py`

---

#### Task 2.4: Edge Rusher Snap Cap

**Effort:** 2 days
**Dependencies:** Task 2.3

- [ ] Implement hard cap at 70% snap count for EDGE
- [ ] Force rest after 8 consecutive snaps
- [ ] Prioritize elite EDGE for 3rd downs
- [ ] Target snap distribution (Elite: 55-60%, Secondary: 45-50%)
- [ ] Add fatigue penalty threshold at 65% snaps
- [ ] Write tests ensuring no EDGE exceeds thresholds

**Files to Create:**

- `backend/app/engine/rotation/edge_rotation.py`
- `backend/tests/engine/rotation/test_edge_rotation.py`

---

#### Task 2.5: Cornerback Nickel/Dime Packages

**Effort:** 3 days
**Dependencies:** Task 1.4

- [ ] Implement nickel package (5 DBs) as primary defense
- [ ] Create CB role assignment (Outside CB1/CB2, Nickel CB, Dime CB)
- [ ] Package frequency: Nickel 60-67%, Base 30-33%, Dime 5-10%
- [ ] Allow Safety to play nickel role ("big nickel")
- [ ] Target snap distribution (CB1/2: 90-95%, Nickel CB: 65-70%)
- [ ] Write tests for package selection logic

**Files to Create:**

- `backend/app/engine/rotation/cb_rotation.py`
- `backend/tests/engine/rotation/test_cb_rotation.py`

---

#### Task 2.6: Linebacker Sub Package System

**Effort:** 3 days
**Dependencies:** Task 1.4

- [ ] Implement base defense (3 LB: Mike, Will, Sam) - 33% usage
- [ ] Implement nickel defense (2 LB: Mike, Will) - 60% usage
- [ ] Implement dime defense (1 LB: Mike only) - 7% usage
- [ ] Require coverage skills for Mike to stay on field in nickel
- [ ] Sam LB becomes situational (only in base defense)
- [ ] Target snap distribution (Mike: 85-90%, Will: 70-75%, Sam: 40-45%)
- [ ] Write tests for LB package transitions

**Files to Create:**

- `backend/app/engine/rotation/lb_rotation.py`
- `backend/tests/engine/rotation/test_lb_rotation.py`

---

#### Task 2.7: Tight End Y/F Roles

**Effort:** 2 days
**Dependencies:** Task 1.4

- [ ] Implement Y TE role (receiving specialist)
- [ ] Implement F TE role (blocking specialist)
- [ ] Y TE plays 80-90% of snaps (almost always on field)
- [ ] F TE plays 40-50% of snaps (12 personnel, goal line, max protect)
- [ ] Skill-based role fit (Y: route running, F: blocking)
- [ ] Write tests for TE deployment in different personnel

**Files to Create:**

- `backend/app/engine/rotation/te_rotation.py`
- `backend/tests/engine/rotation/test_te_rotation.py`

---

### ✅ Phase 3: Core Rotation Engine (Week 5-6)

#### Task 3.1: Rotation Engine Orchestrator

**Effort:** 5 days
**Dependencies:** All Task 2.x

- [ ] Implement `RotationEngine` class to manage all position rotations
- [ ] Create `select_personnel_package()` algorithm
- [ ] Implement `assign_players_to_package()` logic
- [ ] Create `calculate_role_fit_score()` for player-role matching
- [ ] Integrate all position-specific rotation modules
- [ ] Manage rotation state (snap counts, fatigue, package history)
- [ ] Write comprehensive integration tests

**Core Algorithm:**

```python
class RotationEngine:
    def select_active_players(self, game_state, team):
        # 1. Determine personnel package based on situation
        package = self.select_personnel_package(game_state)

        # 2. Assign players to each role in package
        assignments = self.assign_players_to_package(package, team.depth_chart)

        # 3. Update rotation state (snap counts, fatigue)
        self.update_rotation_state(assignments)

        # 4. Return active players for this snap
        return assignments
```

**Files to Create:**

- `backend/app/engine/rotation_engine.py`
- `backend/tests/engine/test_rotation_engine.py`

---

#### Task 3.2: Integration with PlayResolver

**Effort:** 3 days
**Dependencies:** Task 3.1

- [ ] Integrate `RotationEngine` into `PlayResolver`
- [ ] Call rotation engine before each play to determine active players
- [ ] Pass active players to play execution logic
- [ ] Apply fatigue penalties to player ratings during play resolution
- [ ] Log snap data to `player_snap_logs` table
- [ ] Update rotation state after each play
- [ ] Write integration tests with full game simulations

**Integration Points:**

```python
# In PlayResolver.resolve_play()
active_players = self.rotation_engine.select_active_players(game_state, offense)
active_defenders = self.rotation_engine.select_active_players(game_state, defense)

# Apply fatigue penalties
for player in active_players:
    fatigue = rotation_state.get_fatigue(player.id)
    player.effective_rating = apply_fatigue_penalty(player.rating, fatigue)
```

**Files to Modify:**

- `backend/app/engine/play_resolver.py`

---

#### Task 3.3: Snap Count Logging System

**Effort:** 2 days
**Dependencies:** Task 3.2

- [ ] Log every snap to `player_snap_logs` table
- [ ] Track package used, player role, fatigue level
- [ ] Calculate per-snap performance grade
- [ ] Create aggregation queries for post-game snap reports
- [ ] Implement API endpoint for snap count analytics
- [ ] Write tests for logging accuracy

**Data to Log:**

```python
{
    "game_id": 12345,
    "snap_number": 42,
    "player_id": 789,
    "package_used": "11_personnel",
    "role": "slot_wr",
    "fatigue_level": 38.5,
    "performance_grade": 82.3
}
```

**Files to Create:**

- `backend/app/services/snap_logging_service.py`
- `backend/app/api/endpoints/snap_analytics.py`

---

### ✅ Phase 4: Advanced Features (Week 7-8)

#### Task 4.1: Matchup-Based Adjustments

**Effort:** 4 days
**Dependencies:** Task 3.2

- [ ] Implement opponent weakness detection
- [ ] Adjust package frequencies based on matchups
- [ ] Select specific players for favorable matchups (speed WR vs slow CB)
- [ ] Calculate matchup advantage scores
- [ ] Integrate with coaching scheme preferences
- [ ] Write tests for matchup exploitation scenarios

**Example Logic:**

```python
# If opponent ranks 28th vs slot WRs, increase 11 personnel usage
if opponent.slot_coverage_rank > 25:
    package_frequencies["11_personnel"] *= 1.25

# Deploy fastest WR when opponent has slow CBs
if our_wr.speed > opponent_cb.speed + 5:
    matchup_bonus = 20  # Big advantage
```

**Files to Create:**

- `backend/app/engine/matchup_analyzer.py`
- `backend/tests/engine/test_matchup_analyzer.py`

---

#### Task 4.2: Coaching Scheme Integration

**Effort:** 3 days
**Dependencies:** Task 4.1

- [ ] Define offensive scheme types (Air Raid, West Coast, Power Run, Spread Option)
- [ ] Define defensive scheme types (Exotic Blitz, Tampa 2, 46 Bear, Cover 3)
- [ ] Implement scheme-specific package preferences
- [ ] Implement scheme-specific rotation philosophies
- [ ] Allow teams to set their coaching scheme
- [ ] Adjust rotation logic based on team's scheme
- [ ] Write tests for different scheme behaviors

**Schemes to Implement:**

**Offense:**

- Air Raid: 75% 11 personnel, heavy RBBC
- West Coast: Balanced, feature back
- Power Run: 45% 12 personnel, dual TE
- Spread Option: 70% 11 personnel, feature + change of pace RB

**Defense:**

- Exotic Blitz: 70% nickel, 8-man DL rotation
- Tampa 2: 40% base, minimal rotations
- Cover 3 Seattle: 55% nickel, heavy rotations

**Files to Create:**

- `backend/app/models/coaching_scheme.py`
- `backend/app/engine/scheme_integration.py`

---

#### Task 4.3: Playing Time Morale System

**Effort:** 4 days
**Dependencies:** Task 3.3

- [ ] Calculate expected snap % for each player (based on rating, contract, age)
- [ ] Track actual snap % throughout season
- [ ] Calculate morale impact from playing time delta
- [ ] Implement position-specific expectation modifiers (RB/DL expect less, QB/OL expect more)
- [ ] Generate narrative events (trade requests, contract demands)
- [ ] Integrate with existing morale system
- [ ] Write tests for morale scenarios

**Morale Tiers:**

```python
if actual_snaps > expected_snaps + 15%:
    morale = "Very Happy" (Loyalty +10)
elif actual_snaps > expected_snaps + 5%:
    morale = "Happy" (Loyalty +5)
elif actual_snaps > expected_snaps - 5%:
    morale = "Neutral"
elif actual_snaps > expected_snaps - 15%:
    morale = "Unhappy" (Loyalty -5, request more PT)
else:
    morale = "Very Unhappy" (Loyalty -10, request trade)
```

**Files to Create:**

- `backend/app/rpg/playing_time_morale.py`
- `backend/tests/rpg/test_playing_time_morale.py`

---

#### Task 4.4: Snap-Based Player Development

**Effort:** 3 days
**Dependencies:** Task 3.3, Task 4.3

- [ ] Calculate development based on snap count
- [ ] Weight high-leverage snaps (3rd down, red zone) more heavily
- [ ] Apply performance multiplier (excelling = faster development)
- [ ] Implement age curve (young players develop faster)
- [ ] Apply bench penalty for players under 15% snaps
- [ ] Integrate with existing progression system
- [ ] Write tests for development scenarios

**Development Formula:**

```python
snap_development = snap_count * 0.01
quality_bonus = high_leverage_snaps * 0.02
total = (snap_development + quality_bonus) * performance_mult * age_mult

# Bench penalty
if snap_percentage < 0.15:
    total -= 2.0  # Lose 2 OVR points per year on bench
```

**Files to Create:**

- `backend/app/rpg/snap_based_development.py`
- `backend/tests/rpg/test_snap_development.py`

---

#### Task 4.5: Workload Injury Risk

**Effort:** 3 days
**Dependencies:** Task 3.2

- [ ] Calculate injury risk based on snap percentage
- [ ] Increase risk for consecutive snaps without rest
- [ ] Add position-specific workload risks (RB/DL highest)
- [ ] Implement fatigue multiplier on injury risk
- [ ] Create load management system (limit stars in blowouts)
- [ ] Rest players in meaningless games
- [ ] Write tests for injury risk scenarios

**Injury Risk Formula:**

```python
base_risk = 0.01  # 1% per snap
if snap_percentage > 80%:
    snap_risk = 1.5
if consecutive_snaps > 12:
    consecutive_risk = 1.8
if fatigue > 80:
    fatigue_risk = 2.0

injury_chance = base_risk * snap_risk * consecutive_risk * position_risk * fatigue_risk
```

**Files to Create:**

- `backend/app/engine/workload_injury.py`
- `backend/tests/engine/test_workload_injury.py`

---

### ✅ Phase 5: Frontend Integration (Week 9-10)

#### Task 5.1: Depth Chart Management UI

**Effort:** 5 days
**Dependencies:** Task 1.4

- [ ] Create drag-and-drop depth chart interface
- [ ] Add role assignment dropdowns (X/Z/Slot for WR, etc.)
- [ ] Implement snap count target sliders (user can set desired % for each player)
- [ ] Display player skill fit for each role (color-coded)
- [ ] Show fatigue indicators
- [ ] Show morale from playing time
- [ ] Display projected injury risk from workload
- [ ] Write E2E tests for depth chart management

**UI Components:**

- `DepthChartEditor.tsx`
- `PlayerRoleAssignment.tsx`
- `SnapTargetSlider.tsx`
- `RoleFitIndicator.tsx`

---

#### Task 5.2: In-Game Rotation Display

**Effort:** 3 days
**Dependencies:** Task 5.1

- [ ] Display current personnel package in live sim
- [ ] Show active players for current snap
- [ ] Display snap count % and fatigue for each player
- [ ] Highlight matchup advantages
- [ ] Show "hot hand" indicators
- [ ] Add rotation event notifications ("Johnson resting after 5 straight carries")
- [ ] Write E2E tests for live sim rotation display

**Live Sim Addition:**

```text
Current Package: 11 Personnel (3 WR)

Active Players:
RB: #28 Johnson (64% snaps, 35% fatigue) ⚡ Hot Hand
WR (X): #81 Davis (88% snaps, 45% fatigue)
WR (Z): #10 Moore (85% snaps, 42% fatigue) 🎯 Matchup Advantage
WR (Slot): #15 Wilson (72% snaps, 38% fatigue)
TE: #87 Thompson (80% snaps, 40% fatigue)
```

---

#### Task 5.3: Post-Game Snap Report

**Effort:** 3 days
**Dependencies:** Task 3.3

- [ ] Create snap count analytics page
- [ ] Display snap % for all players
- [ ] Break down by personnel package
- [ ] Show situational usage (3rd down %, red zone %, etc.)
- [ ] Compare to snap count targets
- [ ] Display player performance grades
- [ ] Export to CSV functionality
- [ ] Write tests for analytics page

**Report Format:**

```text
Player Snap Count Report - Week 12 vs Patriots

Running Backs:
- #28 M. Johnson: 45 snaps (64%)
  └─ Early Down: 30 | 3rd Down: 8 | Goal Line: 7
  └─ 18 carries, 3 catches, 78.5 PFF grade

- #33 D. Williams: 22 snaps (31%)
  └─ Early Down: 5 | 3rd Down: 15 | Goal Line: 2
  └─ 6 carries, 5 catches, 72.1 PFF grade

Personnel Packages:
- 11 Personnel: 47 plays (67%)
- 12 Personnel: 15 plays (21%)
- 21 Personnel: 8 plays (11%)
```

---

#### Task 5.4: Coaching Scheme UI

**Effort:** 2 days
**Dependencies:** Task 4.2

- [ ] Create scheme selection interface in team settings
- [ ] Display scheme impact on package frequencies
- [ ] Show rotation philosophy for each scheme
- [ ] Allow customization of scheme preferences
- [ ] Display visual representation of scheme (formation diagrams)
- [ ] Write tests for scheme selection

---

### ✅ Phase 6: Testing & Validation (Week 11-12)

#### Task 6.1: Statistical Validation

**Effort:** 4 days
**Dependencies:** All previous tasks

- [ ] Run 100+ full season simulations
- [ ] Validate snap count distributions match NFL data:
  - RB1: 55-75% of snaps ✓
  - Nickel usage: 60-67% of defensive snaps ✓
  - DL rotation: No player over 65% ✓
- [ ] Validate fatigue impacts on performance
- [ ] Validate injury rates match expected workload correlation
- [ ] Create statistical validation report
- [ ] Tune parameters based on results

**Validation Targets:**

```python
VALIDATION_METRICS = {
    "rb_lead_snaps": (0.55, 0.75),
    "nickel_frequency": (0.60, 0.70),
    "dl_max_snaps": 0.65,
    "edge_max_snaps": 0.70,
    "fatigue_performance_correlation": -0.7,  # Negative correlation
}
```

---

#### Task 6.2: Performance Testing

**Effort:** 2 days
**Dependencies:** Task 6.1

- [ ] Profile rotation engine performance
- [ ] Optimize database queries for snap logging
- [ ] Ensure < 50ms overhead per play resolution
- [ ] Add caching for package selection logic
- [ ] Optimize role fit score calculations
- [ ] Write performance benchmarks

**Performance Targets:**

- Rotation selection: < 20ms per play
- Fatigue calculation: < 5ms per player
- Snap logging: < 10ms per snap

---

#### Task 6.3: User Acceptance Testing

**Effort:** 3 days
**Dependencies:** Task 5.4

- [ ] Create UAT test scenarios (RBBC teams, DL rotation, etc.)
- [ ] Recruit beta testers familiar with NFL
- [ ] Gather feedback on realism
- [ ] Identify edge cases and bugs
- [ ] Iterate based on feedback
- [ ] Document known issues

---

## Acceptance Criteria

### Must Have (MVP)

- ✅ Running back committee with realistic snap distribution
- ✅ Defensive line 8-man rotation keeping all players under 65% snaps
- ✅ Nickel defense as primary package (60-67% usage)
- ✅ Fatigue system impacting player performance
- ✅ Depth chart management UI with role assignments
- ✅ Post-game snap count analytics

### Should Have (V1.1)

- ✅ Edge rusher snap cap at 70%
- ✅ Cornerback nickel/dime package deployment
- ✅ Linebacker sub package system
- ✅ Wide receiver personnel sets (11/10/12)
- ✅ Tight end Y/F role differentiation
- ✅ Matchup-based adjustments
- ✅ Coaching scheme integration

### Could Have (V2.0)

- ✅ Playing time morale system
- ✅ Snap-based player development
- ✅ Workload injury risk
- ✅ Load management in blowouts
- ✅ Advanced matchup exploitation

---

## Definition of Done

Each task is considered "done" when:

1. **Code Complete:** All code written and peer reviewed
2. **Tests Pass:** Unit tests, integration tests, and E2E tests all passing
3. **Documentation:** API docs, code comments, and user docs updated
4. **Performance:** Meets performance benchmarks (<50ms overhead per play)
5. **Validation:** Statistical validation shows realistic NFL distributions
6. **UI Complete:** (For frontend tasks) UI implemented, responsive, accessible
7. **Merged:** Code merged to main branch and deployed to staging

---

## Risk Assessment

### High Risk

- **Integration Complexity:** Rotation engine touches play resolution, which is core to simulation
  - Mitigation: Extensive integration testing, feature flag for rollback
- **Performance Impact:** Logging every snap could slow simulation
  - Mitigation: Batch inserts, async logging, caching

### Medium Risk

- **Stat Validation:** Might not match NFL distributions on first attempt

  - Mitigation: Tuning parameters, multiple simulation runs

- **User Confusion:** Depth chart management could be complex
  - Mitigation: Tooltips, tutorial, sensible defaults

### Low Risk

- **Database Migrations:** Standard Alembic migrations, well-tested
- **Model Validation:** Pydantic makes this straightforward

---

## Dependencies

### External

- None (all internal to NFL SIM)

### Internal

- ✅ Existing PlayResolver (extend, don't replace)
- ✅ Existing Player/Team models (add relationships)
- ✅ Existing Progression system (integrate development)
- ✅ Existing Morale system (integrate playing time morale)

---

## Success Metrics

### Technical Metrics

- All tests passing (target: 95%+ coverage for new code)
- Performance: <50ms overhead per play
- Database: <1GB snap log growth per simulated season
- Zero P0/P1 bugs in production

### Product Metrics

- Snap count distributions within 5% of NFL averages
- User engagement: 80%+ of users interact with depth chart feature
- Positive feedback: 85%+ users find rotation system realistic
- Feature usage: 70%+ of games use advanced rotations

---

**TOTAL ESTIMATED EFFORT:** 80-90 developer days (~4 months for 1 developer, 2 months for 2 developers)

**RECOMMENDED STAFFING:** 2 full-stack developers (1 backend-focused, 1 frontend-focused)

---

## END OF TASK BREAKDOWN

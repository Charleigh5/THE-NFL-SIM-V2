# Phase 7: Deep Engine Integration & Data Hydration

**Status:** PLANNED
**Objective:** Connect the "Macro" Simulation (League, Standings, Schedules) with the "Micro" Simulation (Physics, Biology, AI) by hydrating the Engine with real database data.

---

## 1. The "Data Hydration" Problem

Currently, the `SimulationOrchestrator` runs a "hollow" simulation:
- It creates `Game` and `PlayResult` records correctly.
- It manages the clock, score, and field position.
- **HOWEVER**, the actual play outcome is random (`random.random() < 0.6`).
- It sends empty lists (`[]`) for offense/defense players to the `PlayResolver`.
- The `PlayResolver` hardcodes `player_id=1` for fatigue calculations.

**Goal:** When a play runs, the engine must know *exactly* which 22 players are on the field and use their specific attributes (Speed, Strength, Fatigue) to determine the outcome.

## 2. Architecture: The "Match Context"

We will introduce a `MatchContext` object that persists in memory during a game simulation.

```python
class MatchContext:
    def __init__(self, home_team, away_team):
        self.home_roster: Dict[int, Player] = ...
        self.away_roster: Dict[int, Player] = ...
        
        # Kernels State for this match
        self.fatigue_system = GenesisSystem(all_players)
        self.ai_system = CortexSystem(home_coach, away_coach)
        
    def get_fielded_players(self, side: str, formation: str) -> List[Player]:
        # Logic to pull 11 starters based on depth chart
        ...
```

## 3. Implementation Tasks

### Task 7.1: The Match Context & Roster Loading
- [ ] Modify `SimulationOrchestrator` to fetch full rosters for Home/Away teams upon `start_new_game_session`.
- [ ] Create `MatchContext` class to hold these player objects in memory.
- [ ] Implement `DepthChartService` to select the "Starting 11" for Offense/Defense.

### Task 7.2: Kernel Registration
- [ ] Update `PlayResolver` to register all active players with the `GenesisKernel` at game start.
- [ ] Ensure `GenesisKernel` tracks fatigue for *all* players individually during the game loop.

### Task 7.3: Attribute-Based Play Resolution
- [ ] Modify `PlayResolver._resolve_pass_play` to:
    1. Receive the specific `Quarterback`, `Receiver`, and `Defender` objects.
    2. Compare `QB.throw_accuracy` vs `Weather.wind`.
    3. Compare `WR.route_running` vs `CB.man_coverage`.
    4. Compare `WR.speed` vs `CB.speed` (Physics Kernel).
- [ ] Remove `random.randint` logic and replace with `ProbabilityEngine` outcomes.

### Task 7.4: The Cortex (AI) Integration
- [ ] Replace random play-calling in `_execute_single_play`.
- [ ] Implement `Cortex.call_play(situation)` which looks at Down, Distance, Time, and Score.
- [ ] Connect `Coach` attributes (Aggressiveness) to the `Cortex` decision making.

## 4. Execution Strategy

1. **Refactor Orchestrator**: Get the data IN.
2. **Refactor Resolver**: Pass the data DOWN.
3. **Refactor Kernels**: Use the data to CALCULATE.

## 5. Success Criteria

- A "Fast WR" (99 Speed) wins a deep ball against a "Slow CB" (80 Speed) > 80% of the time.
- A "Tired RB" (High Fatigue in Genesis) fumbles more often.
- Teams call "Hail Mary" when losing with 10 seconds left (Cortex AI).

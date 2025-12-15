# AI-002: Player AI State Machines

**Feature ID:** AI-002
**Status:** SPEC_COMPLETE
**Implementation Status:** PARTIAL (Stateless decision trees exist in `ai.py`)

## 1. Overview

This specification details the architecture for Player AI, defining how individual players (QB, RB, Defender) make decisions during a play. The current implementation uses stateless utility classes (`QuarterbackAI`, `VisionAI`), while the target architecture moves towards stateful entities (State Machines) to handle complex, multi-phase behaviors.

## 2. Current Implementation (`backend/app/engine/ai.py`)

The current system operates on a **tick-based stateless** model. Logic is encapsulated in static methods that are called every simulation tick or event.

### 2.1 Quarterback AI

The `QuarterbackAI` class determines reactions to pressure.

- **Input:** QB Position, List of Defenders (coordinates, pass rush power).
- **Pressure Calculation:** Weighted sum of Defender Proximity and Pass Rush Power. (`(Power / 50) * (10 / (Dist + 1))`).
- **Reaction Logic (`check_pressure_response`):**
  1. **Sense Check:** Uses `pocket_presence` to determine if QB notices pressure.
  2. **Decision:** If pressure felt, checks `scramble_willingness`.
  3. **Output:** Returns enum/string: `NORMAL`, `SCRAMBLE`, `THROW_AWAY`, `OBLIVIOUS`.

### 2.2 Vision AI (Running Backs)

The `VisionAI` class calculates optimal running lanes.

- **Input:** Lane Vectors, Defenders, Blockers.
- **Scoring:** `(GoalDist * Wa) - (DefProximity * Wb) + (BlockerLev * Wc)`.
- **Output:** Safety score for a given vector.

### 2.3 Collision System

Physics-based interaction using Momentum (`p = mv`).

- Calculates `Impact Force`.
- Determines `broken_tackle` if Force > Threshold (50).

## 3. Proposed Architecture: State Machines

To support more complex behaviors (e.g., a WR seeing a blitz and changing their route, or a LB reading a play action), we will transition to a State Machine model.

### 3.1 Base Player State

Every active player on field will have a `PlayerState` enum.

```python
class PlayerState(Enum):
    PRE_SNAP = "PRE_SNAP"
    IDLE = "IDLE"
    MOVING = "MOVING"
    ENGAGED = "ENGAGED" (Blocking/Shedding)
    PURSUIT = "PURSUIT" (Defender chasing)
    COVERAGE = "COVERAGE" (DB covering)
    ROUTE_RUNNING = "ROUTE_RUNNING"
    TACKLING = "TACKLING"
    CARRYING = "CARRYING" (Ball carrier)
    CELEBRATING = "CELEBRATING"
```

### 3.2 State Transitions (The "Brain")

Each tick, `Player.update()` calls its specific State Machine logic.

#### Example: Linebacker Logic

1. **PRE_SNAP**: Read offensive formation.
2. **SNAP**: Transition to **READ_STEP**.
3. **READ_STEP**:
   - If Run detected -> Transition to **PURSUIT**.
   - If Pass detected -> Transition to **COVERAGE**.
4. **PURSUIT**: Calculate path to ball carrier. If distance < 1yd -> **TACKLING**.
5. **TACKLING**: Call `CollisionSystem`. If success -> **IDLE** (Play Over). If broken -> **PURSUIT** (Recover).

## 4. Gap Analysis & Next Steps

- [x] **Physics Core**: `CollisionSystem` exists.
- [x] **Decision Utilities**: `VisionAI` and `QuarterbackAI` exist.
- [ ] **State Storage**: `Player` objects need a temporary `current_state` field during game simulation.
- [ ] **Transition Logic**: Move static calls from `PlayResolver` into `Player.update()` methods.

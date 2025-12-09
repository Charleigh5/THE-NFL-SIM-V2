# AI Decision Making Specification

**Source:** `backend/app/engine/ai.py`, `backend/app/services/playbook/defensive_ai.py`
**Status:** Reverse-Engineered / Current Implementation

## 1. Overview

The AI system is divided into two distinct layers:

1.  **Macro AI (Coaching)**: Strategic decision-making such as play calling, coverage selection, and blitz packages.
2.  **Micro AI (Player)**: Real-time on-field decision making such as quarterback pressure response and ball carrier vision.

## 2. Low-Level Player AI (`engine/ai.py`)

### 2.1 Quarterback AI

Handles how the QB reacts to the pocket collapsing.

**Pressure Score Calculation:**

- Aggregates pressure from all unblocked defenders.
- **Formula:** `(PassRushPower / 50) * (10 / (Distance + 1))`
- Only counts defenders within 7 yards.

**Pressure Response Logic:**

1.  **Sense Check**:
    - Does the QB realize pressure is coming?
    - Based on `Pocket Presence` attribute.
    - If failed: **OBLIVIOUS** (High Sack Risk).
2.  **Reaction Decision**:
    - If Sensed: Check `Scramble Willingness`.
    - **SCRAMBLE**: Attempt to run.
    - **THROW_AWAY**: Incomplete pass to avoid sack.
    - **NORMAL**: Stand tall and deliver.

### 2.2 Vision AI (Ball Carrier)

Calculates the optimal path for runs.

**Safety Score Formula:**

```python
Score = (GoalDist * W) - (DefProximity * W) + (BlockerLev * W)
```

- **Defender Penalty**: Inverse distance function (closer = much worse).
- **Blocker Bonus**: Flat bonus if a blocker is nearby.

### 2.3 Physics / Collision System

Resolves tackles using momentum physics.

**Momentum Formula:** `p = mass * velocity`
**Impact Force:** `p_runner - (p_defender * cos(angle))`

- **Broken Tackle**: If `impact_force > 50`.
- **Outcome**: If broken, runner maintains residual momentum.

## 3. Defensive Coordinator AI (`playbook/defensive_ai.py`)

Handles situational play calling based on Gameplan settings.

### 3.1 Decision Hierarchy

1.  **Blitz Decision (`_should_blitz`)**

    - Base probability defined in `Gameplan`.
    - **Modifier**: 1.5x frequency on 3rd & Long (>7 yds).
    - Result: Boolean.

2.  **Coverage Selection (`_select_coverage`)**

    - **Blitzing?** -> Force `COVER_1` (Man).
    - **Long Yardage (>= 15)** -> Force `COVER_2` (Deep Safety help).
    - **Short Yardage (<= 3)** -> Force `COVER_1` (Press).
    - **Standard**: Default to `base_coverage` (usually `COVER_3`).

3.  **Blitz Package Selection**
    - **Critical Down (3rd & >10)**: `ALL_OUT` Blitz.
    - **Standard**: Random choice between `LB_BLITZ`, `CB_BLITZ`, `SAFETY_BLITZ`.

### 3.2 Supported Schemes

- **Coverages**: Cover 0, 1, 2, 3, 4, 6.
- **Blitzes**: LB, CB, Safety, All-Out.

# Player System Technical Guide

This document serves as the technical reference for the Player Model in the Nano Banana Football Simulation Engine. It details the schema, attributes, statistical tracking, and RPG elements for every player position.

## Overview

The Player system is the core of the simulation. It combines:
1.  **Physical Attributes**: Used for physics-based calculations (momentum, tackling).
2.  **Skill Ratings**: Used for probability-based outcomes (catching, coverage).
3.  **RPG Elements**: Traits, XP, and progression logic.
4.  **Dynasty Mechanics**: Morale, contracts, and aging.

---

## Global Attributes
These attributes apply to every player regardless of position.

### Physical & Mental
| Attribute | Type | Description | System Usage |
|-----------|------|-------------|--------------|
| `speed` | 0-100 | Top speed potential. | Movement engine, pursuit angles. |
| `acceleration` | 0-100 | Rate of reaching top speed. | Burst off line, closing speed. |
| `strength` | 0-100 | Physical power. | Blocking, tackling force, shed block. |
| `agility` | 0-100 | Ability to change direction. | Juking, route cutting, coverage reaction. |
| `awareness` | 0-100 | AI decision making. | Reaction time to plays, reading defenses. |
| `stamina` | 0-100 | Energy pool. | fatigue accumulation, sub logic. |
| `injury_resistance` | 0-100 | Durability. | Injury probability roll after contact. |
| `morale` | 0-100 | Player happiness. | **Critical**: Affects team chemistry. Low morale triggers "Mutiny Cascades" in `SocialGraph`. |

### Contract & Status
| Attribute | Description |
|-----------|-------------|
| `contract_salary` | Annual cost in dollars. |
| `contract_years` | Remaining seasons. |
| `development_trait` | Growth potential (`NORMAL`, `STAR`, `SUPERSTAR`, `XFACTOR`). Affects XP multipliers in `OffseasonService`. |

---

## Offensive Positions

### Quarterback (QB)
The primary ball handler and decision maker.

**Key Attributes:**
*   **`throw_power`**: Maximum distance and velocity of throws.
    *   *Link*: Used in `PlayResolver` to determine if a deep pass is physically possible.
*   **`throw_accuracy_short/mid/deep`**: Probability modifiers for pass success at varying ranges.
    *   *Link*: `PlayResolver` selects the specific attribute based on target distance.
*   **`awareness`**: Speed of reading the defense.
*   **`arm_slot`**: Visual/Physics attribute (`OverTop`, `Sidearm`).
*   **`release_point_height`**: Height in feet. Affects ball trajectory start point.

**Progression Logic:**
*   Gains XP heavily from **Passing TDs** (50 XP) and **Yards** (0.5 XP).
*   Loses XP for **Interceptions** (-20 XP).

### Running Back (RB)
Ball carriers focused on evasion and power.

**Key Attributes:**
*   **`vision_cone_angle`**: (Degrees) The field of view where the AI can "see" defenders to react. Narrower cones mean missing open lanes.
*   **`break_tackle_threshold`**: (Float) The force (Newtons approx.) required to bring this player down.
    *   *Link*: Used in `AI.resolve_tackle` against defender's momentum.
*   **`carrying`**: (Implied via `strength`/`agility`) Ability to hold onto the ball.
*   **`catching`**: Ability to act as a receiver out of the backfield.

**Progression Logic:**
*   Gains XP from **Rush TDs** (40 XP) and **Rush Yards** (0.8 XP).

### Wide Receiver (WR) & Tight End (TE)
Pass catchers.

**Key Attributes:**
*   **`catching`**: Base probability to catch a clean pass.
*   **`route_running`**: Ability to create separation from defenders.
    *   *Link*: Used in `PlayResolver` vs. Defender's Coverage.
*   **`pass_block` / `run_block`**: TE specifically relies on these for dual-threat utility.

**Progression Logic:**
*   Gains XP from **Receptions**, **Yards**, and **TDs**.

### Offensive Line (OT, OG, C)
The protectors.

**Key Attributes:**
*   **`pass_block`**: Rating vs. Pass Rush.
    *   *Link*: `BlockingEngine.resolve_pass_block` compares this vs. Defender's `pass_rush_power`.
*   **`run_block`**: Rating vs. Block Shedding.
*   **`strength`**: Critical to avoid "Bull Rush" moves.

**Stats Tracked:**
*   **`pancakes`**: Times they flattened a defender.
*   **`sacks_allowed`**: Negative stat.

---

## Defensive Positions

### Defensive Line (DE, DT)
Pass rushers and run stuffers.

**Key Attributes:**
*   **`pass_rush_power`**: Ability to push the pocket (Bull Rush).
*   **`pass_rush_finesse`**: Ability to swim/spin past blockers.
*   **`block_shed`**: Ability to disengage from a block to make a tackle.
*   **`tackle`**: Ability to wrap up the ball carrier.

**Progression Logic:**
*   Huge XP bonuses for **Sacks** (100 XP) and **Tackles for Loss** (30 XP).

### Linebacker (LB)
Hybrid defenders.

**Key Attributes:**
*   **`play_recognition`**: Ability to distinguish Run vs. Pass early.
*   **`man_coverage` / `zone_coverage`**: Coverage skills.
*   **`tackle`** & **`hit_power`**: Stopping power. `hit_power` increases fumble chance.

### Defensive Back (CB, S)
Pass defenders.

**Key Attributes:**
*   **`man_coverage`**: Ability to stick to a receiver 1-on-1.
*   **`zone_coverage`**: Effectiveness in a designated area.
    *   *Link*: `DefenseEngine.resolve_zone_coverage` uses this + `awareness` to determine reaction speed.
*   **`catching`**: Ability to make Interceptions.

**Stats Tracked:**
*   **`interceptions`**, **`pass_deflections`**.

---

## Special Teams

### Kicker (K) & Punter (P)
**Key Attributes:**
*   **`kick_power`**: Max distance.
*   **`kick_accuracy`**: Probability of straight flight.

---

## System Interconnections

### 1. The Physics Engine (`backend/app/engine/ai.py`)
Unlike simple dice rolls, the game often uses physics.
*   **Tackling**: Uses `strength` and speed to calculate Momentum (`p = mv`).
*   **Break Tackle**: The runner's `break_tackle_threshold` is compared against the defender's effective momentum.

### 2. The RPG Engine (`backend/app/rpg`)
*   **Traits**: Special flags like `"DeepBall"` or `"BrickWall"` provide conditional boosts.
    *   *Example*: `"BrickWall"` adds +10 `pass_block` specifically when facing a Bull Rush.
*   **Progression**: `ProgressionEngine` calculates XP weekly. `DevelopmentTrait` (Star, XFactor) acts as a multiplier for how fast players grow.

### 3. The Society Engine (`backend/app/kernels/society`)
*   **Morale**: This is not just a cosmetic number. A low-morale player can trigger a **Mutiny Cascade** in the social graph, lowering the morale of teammates connected to them.

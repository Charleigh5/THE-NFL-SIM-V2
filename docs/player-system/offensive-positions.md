# Offensive Positions

## Quarterback (QB)

The primary ball handler and decision maker.

### QB Key Attributes

- **`throw_power`**

  - Maximum distance and velocity of throws.
  - _Link_: Used in `PlayResolver` to determine if a deep pass is physically
    possible.

- **`throw_accuracy_short/mid/deep`**

  - Probability modifiers for pass success at varying ranges.
  - _Link_: `PlayResolver` selects the specific attribute based on target
    distance.

- **`awareness`**

  - Speed of reading the defense.

- **`arm_slot`**

  - Visual/Physics attribute (`OverTop`, `Sidearm`).

- **`release_point_height`**
  - Height in feet. Affects ball trajectory start point.

### QB Progression Logic

- Gains XP heavily from **Passing TDs** (50 XP) and **Yards** (0.5 XP).
- Loses XP for **Interceptions** (-20 XP).

## Running Back (RB)

Ball carriers focused on evasion and power.

### RB Key Attributes

- **`vision_cone_angle`**

  - (Degrees) The field of view where the AI can "see" defenders to react.
    Narrower cones mean missing open lanes.

- **`break_tackle_threshold`**

  - (Float) The force (Newtons approx.) required to bring this player down.
  - _Link_: Used in `AI.resolve_tackle` against defender's momentum.

- **`carrying`**

  - (Implied via `strength`/`agility`) Ability to hold onto the ball.

- **`catching`**
  - Ability to act as a receiver out of the backfield.

### RB Progression Logic

- Gains XP from **Rush TDs** (40 XP) and **Rush Yards** (0.8 XP).

## Wide Receiver (WR) & Tight End (TE)

Pass catchers.

### WR/TE Key Attributes

- **`catching`**

  - Base probability to catch a clean pass.

- **`route_running`**

  - Ability to create separation from defenders.
  - _Link_: Used in `PlayResolver` vs. Defender's Coverage.

- **`pass_block` / `run_block`**
  - TE specifically relies on these for dual-threat utility.

### WR/TE Progression Logic

- Gains XP from **Receptions**, **Yards**, and **TDs**.

## Offensive Line (OT, OG, C)

The protectors.

### OL Key Attributes

- **`pass_block`**

  - Rating vs. Pass Rush.
  - _Link_: `BlockingEngine.resolve_pass_block` compares this vs. Defender's
    `pass_rush_power`.

- **`run_block`**

  - Rating vs. Block Shedding.

- **`strength`**
  - Critical to avoid "Bull Rush" moves.

### OL Stats Tracked

- **`pancakes`**: Times they flattened a defender.
- **`sacks_allowed`**: Negative stat.

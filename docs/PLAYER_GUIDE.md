# Player System Technical Guide

This document serves as the technical reference for the Player Model in the Nano
Banana Football Simulation Engine. It details the schema, attributes,
statistical tracking, and RPG elements for every player position.

## Overview

The Player system is the core of the simulation. It combines:

1. **Physical Attributes**: Used for physics-based calculations (momentum,
   tackling).
2. **Skill Ratings**: Used for probability-based outcomes (catching, coverage).
3. **RPG Elements**: Traits, XP, and progression logic.
4. **Dynasty Mechanics**: Morale, contracts, and aging.

## Contents

- [Global Attributes](player-system/attributes.md)

  - Physical & Mental
  - Contract & Status

- [Offensive Positions](player-system/offensive-positions.md)

  - Quarterback (QB)
  - Running Back (RB)
  - Wide Receiver (WR) & Tight End (TE)
  - Offensive Line (OT, OG, C)

- [Defensive Positions](player-system/defensive-positions.md)

  - Defensive Line (DE, DT)
  - Linebacker (LB)
  - Defensive Back (CB, S)

- [Special Teams](player-system/special-teams.md)

  - Kicker (K) & Punter (P)
  - Enhancements & Identity

- [Proposed RPG & Leveling Overhaul](player-system/rpg-progression.md)

  - Offensive Positions
  - Defensive Positions
  - Special Teams Positions

- [Proposed Feature Enhancements](player-system/proposed-features.md)
  - Offensive Enhancements
  - Defensive Enhancements

## System Interconnections

### 1. The Physics Engine (`backend/app/engine/ai.py`)

Unlike simple dice rolls, the game often uses physics.

- **Tackling**: Uses `strength` and speed to calculate Momentum (`p = mv`).
- **Break Tackle**: The runner's `break_tackle_threshold` is compared against
  the defender's effective momentum.

### 2. The RPG Engine (`backend/app/rpg`)

- **Traits**: Special flags like `"DeepBall"` or `"BrickWall"` provide
  conditional boosts.
  - _Example_: `"BrickWall"` adds +10 `pass_block` specifically when facing a
    Bull Rush.
- **Progression**: `ProgressionEngine` calculates XP weekly. `DevelopmentTrait`
  (Star, XFactor) acts as a multiplier for how fast players grow.

### 3. The Society Engine (`backend/app/kernels/society`)

- **Morale**: This is not just a cosmetic number. A low-morale player can
  trigger a **Mutiny Cascade** in the social graph, lowering the morale of
  teammates connected to them.

# Defensive Positions

## Defensive Line (DE, DT)

Pass rushers and run stuffers.

### Defensive Line Key Attributes

- **`pass_rush_power`**

  - Ability to push the pocket (Bull Rush).

- **`pass_rush_finesse`**

  - Ability to swim/spin past blockers.

- **`block_shed`**

  - Ability to disengage from a block to make a tackle.

- **`tackle`**
  - Ability to wrap up the ball carrier.

### Progression Logic

- Huge XP bonuses for **Sacks** (100 XP) and **Tackles for Loss** (30 XP).

## Linebacker (LB)

Hybrid defenders.

### Linebacker Key Attributes

- **`play_recognition`**

  - Ability to distinguish Run vs. Pass early.

- **`man_coverage` / `zone_coverage`**

  - Coverage skills.

- **`tackle`** & **`hit_power`**
  - Stopping power. `hit_power` increases fumble chance.

## Defensive Back (CB, S)

Pass defenders.

### Defensive Back Key Attributes

- **`man_coverage`**

  - Ability to stick to a receiver 1-on-1.

- **`zone_coverage`**

  - Effectiveness in a designated area.
  - _Link_: `DefenseEngine.resolve_zone_coverage` uses this + `awareness` to determine reaction speed.

- **`catching`**
  - Ability to make Interceptions.

### Stats Tracked

- **`interceptions`**, **`pass_deflections`**.

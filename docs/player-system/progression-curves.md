# Progression Curves Specification

**Source:** `backend/app/services/training/progression.py`, `backend/app/services/offseason_service.py`, `backend/app/kernels/rpg/progression.py`
**Status:** Reverse-Engineered / Current Implementation

## 1. Overview

The progression system manages player development throughout their careers, including XP-based leveling, age-based regression, and development trait multipliers.

## 2. Career Phases

Players move through distinct career phases based on age and position:

| Phase        | Description                     |
| ------------ | ------------------------------- |
| `ROOKIE`     | Before peak age - Rapid growth  |
| `PRIME`      | Peak performance years          |
| `POST_PRIME` | Physical plateau, mental growth |
| `DECLINE`    | Physical regression             |
| `RETIREMENT` | End of career                   |

### Peak Ages by Position

```python
PEAK_AGES = {
    "QB": (26, 32),
    "RB": (23, 27),
    "WR": (25, 29),
    "TE": (26, 30),
    "OL": (26, 31),
    "DL": (25, 29),
    "LB": (24, 28),
    "DB": (24, 28),
    "K": (27, 35),
    "P": (27, 35),
}
```

## 3. XP and Leveling

### XP Thresholds

```python
def calculate_xp_threshold(current_level):
    if current_level > 70:
        return int(1000 * (1.1 ** (current_level - 70)))
    return 1000
```

- Base: 1000 XP per level
- Above 70 OVR: Exponential scaling (harder to improve elite players)

### Development Trait Multipliers

| Trait     | XP Multiplier |
| --------- | ------------- |
| NORMAL    | 1.0x          |
| STAR      | 1.25x         |
| SUPERSTAR | 1.5x          |
| X_FACTOR  | 2.0x          |

### Work Ethic Modifier

From `kernels/rpg/progression.py`:

- Range: 0.5 (Lazy) to 1.5 (Gym Rat)
- Multiplies all XP gains

## 4. Annual Progression (Offseason)

Located in `simulate_player_progression()`:

### Age-Based Changes

| Age Range | Rating Change |
| --------- | ------------- |
| ≤ 24      | +1 to +3      |
| 25-28     | -1 to +2      |
| 29-32     | -2 to +1      |
| 33+       | -3 to -1      |

### Experience Modifier

| Experience | Modifier |
| ---------- | -------- |
| ≤ 2 years  | +0 to +2 |
| 8+ years   | -2 to 0  |

### Coach Impact

- Coach `development_rating > 70`: +1 bonus
- Coach `development_rating < 30`: -1 penalty

### Final Formula

```python
total_change = age_change + exp_modifier + variance + dev_trait_mod + coach_mod
new_rating = clamp(old_rating + total_change, 40, 99)
```

## 5. Regression System

Triggered during `DECLINE` phase:

### Physical Attributes (Fast Decay)

Attributes: `speed`, `acceleration`, `agility`, `jumping`

```python
loss_chance = 0.5 + (years_past_prime * 0.1)
loss_amount = random(1, 1 + years_past_prime)
```

### Power Attributes (Moderate Decay)

Attributes: `strength`, `throw_power`

```python
loss_chance = base_chance * 0.6
loss_amount = random(1, 2)
```

### Mental Attributes (Protected)

Attributes: `awareness`, `play_recognition`

- Rarely regress
- May continue to improve

## 6. Retirement Logic

Located in `process_retirements()`:

| Age   | Condition | Retirement Chance |
| ----- | --------- | ----------------- |
| 40+   | Any       | 100%              |
| 35-39 | OVR < 75  | 50%               |
| 35-39 | OVR ≥ 75  | 10%               |
| 30-34 | OVR < 65  | 20%               |

### Hall of Fame Criteria

Upon retirement, players are evaluated:

- Overall Rating ≥ 90: Inducted
- Legacy Score ≥ 1000: Inducted

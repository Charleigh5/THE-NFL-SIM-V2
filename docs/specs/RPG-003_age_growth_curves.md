# RPG-003: Age-Based Growth & Regression Curves Specification

**Feature ID:** RPG-003
**Status:** 🟢 SPEC_COMPLETE
**Priority:** P1
**Last Updated:** 2025-12-20

---

## 1. Overview

The Age-Based Growth & Regression system implements position-specific "Aging Curves" derived from NFL data. This replaces linear progression with bio-realistic curves, ensuring players peak at appropriate ages and decline realistically, creating a dynamic and evolving league ecosystem.

## 2. Core Concepts

### 2.1 The "Curve" Function

Progression is no longer linear. It follows a multi-stage function:

1. **Ascension (Rookie - Peak)**: High XP gains, rapid attribute growth.
2. **Peak Plateau**: XP maintains attributes, mental attributes grow, physicals hold.
3. **The Cliff (Decline)**: Negative XP modifiers, physical attribute decay.

### 2.2 Position-Specific Epochs

| Position | Breakout Age | Peak Band | Decline Start | The Cliff |
| :------- | :----------- | :-------- | :------------ | :-------- |
| **RB**   | 22           | 24-26     | 27            | 29        |
| **WR**   | 23           | 26-29     | 30            | 32        |
| **TE**   | 24           | 26-30     | 31            | 33        |
| **QB**   | 24           | 28-32     | 34            | 36        |
| **OL**   | 24           | 26-30     | 31            | 33        |
| **DL**   | 23           | 25-29     | 30            | 32        |
| **LB**   | 23           | 25-28     | 29            | 31        |
| **DB**   | 22           | 24-28     | 29            | 31        |
| **K/P**  | 24           | 27-32     | 34            | 36        |

---

## 3. Implementation Logic

### 3.1 Attribute Decay Categories

Regression hits attributes differently based on their biological nature.

- **Tier 1: Physical (Fast Decay)**

  - Speed, Acceleration, Agility, Jumping, Change of Direction.
  - _Decay Rate_: High (loss of 1-3 pts/year in decline).

- **Tier 2: Technical (Slow Decay)**

  - Strength, Throw Power, Break Tackle, Route Running.
  - _Decay Rate_: Low (loss of 0-1 pts/year).

- **Tier 3: Mental (No Decay / Growth)**
  - Awareness, Play Recognition, Vision.
  - _Decay Rate_: None (Often grows until retirement).

### 3.2 Regression Algo (`offseason_service.py`)

```python
def calculate_regression(player):
    curve = get_curve(player.position)
    years_past_peak = player.age - curve.peak_end

    if years_past_peak <= 0:
        return # Safe

    # The Cliff logic
    decline_factor = 1.0 + (years_past_peak * 0.25) # Accelerates over time

    if player.position == "RB" and years_past_peak > 2:
        decline_factor *= 1.5 # RBs fall off hard

    for attr in player.attributes:
         if attr.is_physical:
             roll = random()
             if roll < (0.3 * decline_factor):
                 decrement(attr, 1-2 pts)
```

---

## 4. Verification Plan

1. **Test: RB Shelf Life**: Verify that <10% of generated RBs remain starters (OVR > 80) past age 30.
2. **Test: QB Longevity**: Verify QBs consistently maintain OVR > 85 into their early 30s.
3. **Test: Speed Kills**: Verify that Speed is the first attribute to drop in 90% of regressions.

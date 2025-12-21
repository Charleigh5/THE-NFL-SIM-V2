# GAME-010: Venue-Specific Effects Specification

**Feature ID:** GAME-010
**Status:** 🟢 SPEC_COMPLETE
**Priority:** P2
**Last Updated:** 2025-12-20

---

## 1. Overview

The Venue-Specific Effects system models the unique characteristics of each NFL stadium, influencing gameplay through crowd noise, altitude, surface type, and weather interaction. This system replaces generic home-field advantage with physics-based and psychological modifiers.

## 2. Core Mechanics

### 2.1 Crowd Influence (The "12th Man")

Crowd noise is dynamic, calculated per play based on:

1. **Attendance %**: Base volume.
2. **Situation**: 3rd/4th down, Red Zone increases volume.
3. **Momentum**: Big plays spike volume.
4. **Stadium Architecture**: Domes and specific open-air stadiums (Seattle, KC) have multipliers.

**Impacts:**

- **False Start Chance**: Increases non-linearly with decibels > 90dB.
- **Hot Route Failures**: Away QBs with low awareness fail to check audibles.
- **Snap Count Jumps**: Defense gets a jump on the snap (pass rush bonus).

### 2.2 Altitude Physics (Denver Effect)

At high altitudes (>4000ft):

- **Kick Distance**: +5-8% max distance for FGs and Punts.
- **Stamina Drain**: Away players (unless acclimated) lose fatigue 10-15% faster in the 2nd half.

### 2.3 Surface Interaction

| Surface               | Injury Modifier | Speed Modifier | Cut/Agility Modifier |
| :-------------------- | :-------------- | :------------- | :------------------- |
| **Grass (Natural)**   | 1.0 (Base)      | 1.0 (Base)     | 1.0 (Base)           |
| **Turf (Artificial)** | 1.15 (+15%)     | 1.02 (+2%)     | 1.03 (+3%)           |
| **Hybrid**            | 1.05 (+5%)      | 1.01 (+1%)     | 1.01 (+1%)           |

_Note: Rain/Snow effects (GAME-009) interact differently. Grass becomes mud (slow), Turf becomes slick (no speed loss, high fumble)._

---

## 3. Implementation Data

### 3.1 Known Loud Stadiums

_(Configuration for `StadiumConfig`)_

| Stadium Code | Name              | Base Noise Bonus | Architecture  |
| :----------- | :---------------- | :--------------- | :------------ |
| **KC**       | Arrowhead         | +15              | Open (Bowl)   |
| **SEA**      | Lumen Field       | +15              | Open (Canopy) |
| **NO**       | Caesars Superdome | +12              | Dome          |
| **MIN**      | US Bank Stadium   | +10              | Dome          |
| **BUF**      | Highmark          | +8               | Open (Windy)  |

### 3.2 Altitude List

- **DEN** (Empower Field): 5280ft -> Tier 2 Altitude Effect
- **ARI** (State Farm): 1100ft -> Negligible
- **ATL**: 1000ft -> Negligible

---

## 4. Integration Logic

### `calculate_home_field_bonus(crowd_state, stadium_config)`

```python
# Noise Calculation
noise_db = base_noise + (attendance_pct * 20) + (momentum * 10)
if stadium.is_dome or stadium.id in ["KC", "SEA"]:
    noise_db += 10

# False Start Probability
# Sigmoid function centered at 95dB
false_start_prob = base_prob * (1 + (noise_db - 85) * 0.05)

# Fatigue (Altitude)
fatigue_mult = 1.0
if stadium.altitude > 4000 and team.is_away:
    fatigue_mult = 1.15
```

---

## 5. Verification Plan

1. **Test: The "Seattle Test"**: Verify that an away team's false start rate is >2x higher in SEA/KC vs a quiet stadium (e.g., LAC).
2. **Test: The "Prater Test"**: Verify that a kicker with 55yd range can hit 59yd field goals with generated wind in DEN.
3. **Test: Turf Monster**: Verify injury rates are statistically higher on Turf surfaces over 1000 simulations.

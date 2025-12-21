# GAME-009: Environmental Weather Effects Specification

**Feature ID:** GAME-009
**Status:** 🟢 SPEC_COMPLETE
**Priority:** P1
**Last Updated:** 2025-12-20

---

## 1. Overview

The Environmental Weather Effects system models how weather conditions affect game outcomes, including passing, kicking, running, and ball security.

## 2. NFL Statistical Baselines

### Wind Impact

| Wind Speed | Pass Yards Impact | Completion % | FG Accuracy |
| :--------- | :---------------- | :----------- | :---------- |
| 0-10 mph   | Baseline          | Baseline     | ~89%        |
| 10-15 mph  | -5%               | -3%          | ~83%        |
| 15-20 mph  | -12%              | -7%          | ~80%        |
| 20+ mph    | -20%              | -12%         | ~77%        |

### Precipitation Impact

| Condition  | Fumble Rate | Pass Yards | Total Points |
| :--------- | :---------- | :--------- | :----------- |
| Clear      | Baseline    | Baseline   | Baseline     |
| Light Rain | +10%        | -5%        | -3 pts       |
| Heavy Rain | +20%        | -12%       | -7 pts       |
| Snow       | +15%        | -15%       | -25%         |

### Temperature Impact

| Temperature | Passing Accuracy | Ball Grip | Fatigue  |
| :---------- | :--------------- | :-------- | :------- |
| 70-85°F     | Baseline         | Baseline  | Baseline |
| 50-70°F     | +2% (optimal)    | Baseline  | -5%      |
| 32-50°F     | -3%              | -5%       | Baseline |
| <32°F       | -5%              | -10%      | +5%      |
| >85°F       | -2%              | Baseline  | +10-20%  |

---

## 3. Implementation Details

### Current Implementation (`weather_effects.py`)

```python
# PASSING MODIFIERS
if wind_speed > 10:
    accuracy -= (wind_speed - 10) * 0.01   # -1% per mph over 10
    distance -= (wind_speed - 10) * 0.005  # -0.5% per mph

if precipitation == RAIN:
    accuracy *= 0.90  # -10%
elif precipitation == SNOW:
    accuracy *= 0.85  # -15%
    distance *= 0.95

if temperature < 32:
    accuracy *= 0.95  # -5% for freezing

# KICKING MODIFIERS
if wind_speed > 5:
    accuracy -= (wind_speed - 5) * 0.02   # -2% per mph over 5
    distance -= (wind_speed - 5) * 0.01   # -1% per mph

if temperature < 40:
    distance -= (40 - temp) * 0.005  # Dense cold air

# FUMBLE MODIFIERS
WET: 1.2x (20% increase)
MUDDY: 1.3x (30% increase)
SNOWY: 1.15x (15% increase)
COLD (<20°F): Additional 1.1x
```

### Recommended Calibration Updates

| Parameter                 | Current | Recommended   | Rationale             |
| :------------------------ | :------ | :------------ | :-------------------- |
| Wind threshold            | 10 mph  | **10 mph**    | ✅ Correct            |
| Wind accuracy penalty     | -1%/mph | **-0.8%/mph** | Slightly generous     |
| Rain accuracy             | 0.90    | **0.88**      | -12% matches NFL data |
| Snow accuracy             | 0.85    | **0.85**      | ✅ Correct            |
| Cold threshold            | 32°F    | **32°F**      | ✅ Correct            |
| Fumble multiplier (wet)   | 1.2     | **1.2**       | ✅ Correct            |
| Fumble multiplier (muddy) | 1.3     | **1.25**      | Slightly reduce       |

---

## 4. Field Conditions

### Surface Type Effects

| Surface             | Speed Modifier | Injury Risk | Traction  |
| :------------------ | :------------- | :---------- | :-------- |
| Natural Grass (Dry) | 1.0            | 1.0         | High      |
| Natural Grass (Wet) | 0.95           | 1.1         | Medium    |
| Field Turf (Dry)    | 1.02           | 0.95        | Very High |
| Field Turf (Wet)    | 0.98           | 1.0         | High      |
| Muddy               | 0.85           | 1.2         | Low       |
| Snowy               | 0.90           | 1.15        | Medium    |

### Special Considerations

| Venue                | Effect                  | Modifier          |
| :------------------- | :---------------------- | :---------------- |
| Dome                 | No weather effects      | N/A               |
| Retractable (Closed) | No weather effects      | N/A               |
| Denver (Altitude)    | Ball travels farther    | +3% kick distance |
| Green Bay (Cold)     | Higher cold probability | Environmental     |

---

## 5. Integration Points

### Play Resolver Integration

```python
# Before pass resolution
weather_effects = WeatherEffects(game_weather)
acc_mod, dist_mod = weather_effects.get_passing_modifiers()

# Apply to completion calculation
completion_prob *= acc_mod
max_air_yards *= dist_mod

# Before kick resolution
kick_acc, kick_dist = weather_effects.get_kicking_modifiers()
```

### Fumble Check Integration

```python
fumble_multiplier = weather_effects.get_fumble_probability_modifier()
base_fumble_prob *= fumble_multiplier
```

---

## 6. Verification

### Unit Tests Required

- [ ] Test wind >15 mph reduces pass accuracy by ~10%
- [ ] Test rain increases fumble rate by 20%
- [ ] Test snow reduces passing yards by 15%
- [ ] Test cold (<32°F) reduces accuracy by 5%
- [ ] Test FG accuracy drops to ~77% at 20+ mph wind

### Statistical Validation

Simulate 1,000 games per condition and validate:

- Passing yard distributions match NFL weather data
- Fumble rates increase appropriately
- Dome games average ~4 points higher than outdoor cold games

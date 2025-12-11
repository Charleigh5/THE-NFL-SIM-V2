# Environmental Effects Specification

**Document ID:** GAME-009
**Status:** IMPLEMENTED
**Last Updated:** 2024-12-10

---

## Overview

Environmental effects modify gameplay based on weather conditions, temperature, field state, and venue characteristics. Weather can combine (e.g., heavy rain + high wind) with effects stacking.

## Architecture

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ GameWeather     │────▶│ WeatherEffects   │────▶│ PlayResolver    │
│ (Model)         │     │ (Engine)         │     │ (Applies mods)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## Weather Severity Levels

| Severity     | Description              | Multiplier |
| ------------ | ------------------------ | ---------- |
| **LIGHT**    | Minimal impact           | 0.5x       |
| **MODERATE** | Standard weather effects | 1.0x       |
| **HEAVY**    | Severe conditions        | 1.5x       |
| **EXTREME**  | Dangerous conditions     | 2.0x       |

---

## Precipitation Types

| Type      | Severity | Pass Accuracy | Fumble Risk | Kicking |
| --------- | -------- | ------------- | ----------- | ------- |
| **Rain**  | LIGHT    | -5%           | +10%        | -3%     |
| **Rain**  | MODERATE | -10%          | +20%        | -8%     |
| **Rain**  | HEAVY    | -20%          | +35%        | -15%    |
| **Snow**  | LIGHT    | -8%           | +10%        | -5%     |
| **Snow**  | MODERATE | -15%          | +20%        | -12%    |
| **Snow**  | HEAVY    | -25%          | +40%        | -25%    |
| **Sleet** | MODERATE | -18%          | +30%        | -15%    |

---

## Wind Effects

| Speed (mph) | Category  | Pass Distance | Kick Distance | Pass Accuracy |
| ----------- | --------- | ------------- | ------------- | ------------- |
| 0-10        | Calm      | 0%            | 0%            | 0%            |
| 11-15       | Breezy    | -3%           | -5%           | -2%           |
| 16-25       | Windy     | -8%           | -12%          | -5%           |
| 26-35       | High Wind | -15%          | -25%          | -10%          |
| 36+         | Gusts     | -25%          | -40%          | -20%          |

### Wind Direction Impact

| Direction          | Effect                               |
| ------------------ | ------------------------------------ |
| **Headwind**       | Full negative modifier on distance   |
| **Tailwind**       | +50% of modifier as bonus            |
| **Crosswind**      | Full negative modifier on accuracy   |
| **Diagonal (45°)** | 70% effect on both distance/accuracy |

---

## Combined Weather (Wind + Precipitation)

Effects **stack multiplicatively** when conditions combine:

```python
# Example: Heavy Rain + High Wind (26 mph)
base_accuracy = 1.0
rain_penalty = 0.80  # Heavy rain: -20%
wind_penalty = 0.90  # High wind: -10%
combined_accuracy = 1.0 * 0.80 * 0.90  # = 0.72 (-28% total)
```

### Common Combinations

| Combination            | Pass Accuracy | Fumble | Notes                   |
| ---------------------- | ------------- | ------ | ----------------------- |
| Light Rain + Breezy    | -7%           | +12%   | Typical game day        |
| Moderate Rain + Windy  | -15%          | +25%   | Challenging conditions  |
| Heavy Rain + High Wind | -28%          | +45%   | Running game advantage  |
| Light Snow + Windy     | -13%          | +15%   | Cold-weather classic    |
| Heavy Snow + Gusts     | -42%          | +55%   | Near-unplayable passing |

---

## Temperature Effects

| Range   | Category     | Pass | Fumble | Fatigue | Notes            |
| ------- | ------------ | ---- | ------ | ------- | ---------------- |
| < 0°F   | Extreme Cold | -10% | +25%   | +10%    | Ball like a rock |
| 0-20°F  | Frigid       | -7%  | +15%   | +5%     | Cold hands       |
| 21-32°F | Cold         | -5%  | +10%   | 0%      | Standard cold    |
| 33-50°F | Cool         | 0%   | 0%     | 0%      | Ideal            |
| 51-75°F | Mild         | 0%   | 0%     | 0%      | Ideal            |
| 76-85°F | Warm         | 0%   | 0%     | +5%     | Slight fatigue   |
| 86-95°F | Hot          | 0%   | -5%    | +15%    | Sweaty ball      |
| > 95°F  | Extreme Heat | -3%  | -8%    | +30%    | Dangerous        |

---

## Field Conditions

| Condition  | Cause                      | Fumble | Fatigue | Speed |
| ---------- | -------------------------- | ------ | ------- | ----- |
| **DRY**    | Clear weather              | 0%     | 0%      | 0%    |
| **WET**    | Light-Moderate rain        | +20%   | +5%     | -3%   |
| **SOAKED** | Heavy/prolonged rain       | +35%   | +10%    | -8%   |
| **MUDDY**  | Heavy rain + poor drainage | +40%   | +25%    | -15%  |
| **SNOWY**  | Accumulated snow           | +25%   | +15%    | -10%  |
| **ICY**    | Frozen precipitation       | +50%   | +10%    | -20%  |

---

## Modifier Formulas (Updated)

### Passing Accuracy

```python
def get_passing_accuracy(weather: GameWeather) -> float:
    accuracy = 1.0
    severity_mult = SEVERITY_MULTIPLIERS[weather.severity]

    # Precipitation
    if weather.precipitation == RAIN:
        base_penalty = {LIGHT: 0.05, MODERATE: 0.10, HEAVY: 0.20}
        accuracy -= base_penalty[weather.severity]
    elif weather.precipitation == SNOW:
        base_penalty = {LIGHT: 0.08, MODERATE: 0.15, HEAVY: 0.25}
        accuracy -= base_penalty[weather.severity]

    # Wind (stacks with precipitation)
    if weather.wind_speed > 10:
        wind_penalty = min(0.25, (weather.wind_speed - 10) * 0.01)
        accuracy *= (1 - wind_penalty)

    # Temperature
    if weather.temperature < 32:
        cold_penalty = min(0.10, (32 - weather.temperature) * 0.003)
        accuracy -= cold_penalty

    return max(0.50, accuracy)
```

### Fumble Probability

```python
def get_fumble_multiplier(weather: GameWeather) -> float:
    multiplier = 1.0

    # Field condition
    field_mods = {DRY: 1.0, WET: 1.2, SOAKED: 1.35, MUDDY: 1.4, SNOWY: 1.25, ICY: 1.5}
    multiplier *= field_mods[weather.field_condition]

    # Precipitation (additional)
    if weather.precipitation in [RAIN, SNOW]:
        precip_mod = {LIGHT: 1.05, MODERATE: 1.10, HEAVY: 1.20}
        multiplier *= precip_mod[weather.severity]

    # Cold temperature
    if weather.temperature < 20:
        multiplier *= 1.15

    return min(2.5, multiplier)  # Cap at 2.5x
```

---

## Venue-Specific Effects

| Venue Type                    | Weather Override            |
| ----------------------------- | --------------------------- |
| **Dome**                      | Always clear, 72°F, no wind |
| **Retractable Roof (Closed)** | Same as dome                |
| **Retractable Roof (Open)**   | Normal weather applies      |
| **Outdoor - Northern**        | Higher cold/snow chance     |
| **Outdoor - Southern**        | Higher heat/humidity chance |
| **Outdoor - Coastal**         | Higher wind chance          |

---

## Implementation Files

| Component              | Path                                 | Status |
| ---------------------- | ------------------------------------ | ------ |
| Weather Model          | `models/weather.py`                  | ✅     |
| Weather Effects Engine | `engine/weather_effects.py`          | ✅     |
| Weather Service        | `services/weather_service.py`        | ✅     |
| Weather Schema         | `schemas/weather.py`                 | ✅     |
| Frontend Widget        | `components/game/WeatherWidget.tsx`  | ✅     |
| Unit Tests             | `tests/unit/test_weather_effects.py` | ✅     |

---

END OF DOCUMENT

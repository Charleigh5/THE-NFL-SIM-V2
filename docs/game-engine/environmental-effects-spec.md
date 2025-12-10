# Environmental Effects Specification

**Document ID:** GAME-009
**Status:** IMPLEMENTED
**Last Updated:** 2024-12-10

---

## Overview

Environmental effects modify gameplay based on weather conditions, temperature, field state, and venue characteristics. The system is designed to add realism and strategic depth to the simulation.

## Architecture

```text
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ GameWeather     │────▶│ WeatherEffects   │────▶│ PlayResolver    │
│ (Model)         │     │ (Engine)         │     │ (Applies mods)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        ▼                        ▼
┌─────────────────┐     ┌──────────────────┐
│ WeatherService  │     │ WeatherWidget    │
│ (Backend)       │     │ (Frontend)       │
└─────────────────┘     └──────────────────┘
```

## Weather Conditions

| Condition                | Impact                                      | Modifier               |
| ------------------------ | ------------------------------------------- | ---------------------- |
| **Clear**                | No effect                                   | 1.0x                   |
| **Rain**                 | Reduced passing accuracy, increased fumbles | -10% pass, +20% fumble |
| **Snow**                 | Reduced passing/kicking, slippery field     | -15% pass, +15% fumble |
| **Wind (>10 mph)**       | Reduced passing/kicking distance            | -1% per mph over 10    |
| **Extreme Cold (<32°F)** | Reduced grip, ball hardness                 | -5% pass, +10% fumble  |
| **Extreme Heat (>85°F)** | Increased fatigue                           | +2% fatigue per degree |

## Field Conditions

| Condition | Effect                        |
| --------- | ----------------------------- |
| **DRY**   | Normal play (1.0x multiplier) |
| **WET**   | +20% fumble probability       |
| **MUDDY** | +30% fumble, +20% fatigue     |
| **SNOWY** | +15% fumble, +20% fatigue     |

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

## Modifier Formulas

### Passing Accuracy

```python
accuracy = 1.0
if wind_speed > 10:
    accuracy -= (wind_speed - 10) * 0.01  # -1% per mph
if precipitation == RAIN:
    accuracy *= 0.90
elif precipitation == SNOW:
    accuracy *= 0.85
if temperature < 32:
    accuracy *= 0.95
return max(0.5, accuracy)
```

### Fumble Probability

```python
multiplier = 1.0
if field == WET: multiplier *= 1.2
elif field == MUDDY: multiplier *= 1.3
elif field == SNOWY: multiplier *= 1.15
if temperature < 20: multiplier *= 1.1
return multiplier
```

### Fatigue Accumulation

```python
multiplier = 1.0
if temperature > 85:
    multiplier += (temperature - 85) * 0.02
if humidity > 0.7:
    multiplier += (humidity - 0.7) * 0.5
if field in [MUDDY, SNOWY]:
    multiplier *= 1.2
return multiplier
```

---

## Venue-Specific Effects

| Venue Type                    | Weather Override            |
| ----------------------------- | --------------------------- |
| **Dome**                      | Always clear, 72°F, no wind |
| **Retractable Roof (Closed)** | Same as dome                |
| **Retractable Roof (Open)**   | Normal weather applies      |
| **Outdoor**                   | Full weather effects        |

---

## Integration Points

1. **MatchContext** - Weather loaded at game start
2. **PlayResolver** - Modifiers applied to play outcomes
3. **WeatherWidget** - Visual display to user
4. **Game Summary** - Weather noted in results

---

## Testing

- Unit tests: `pytest tests/unit/test_weather_effects.py`
- Integration: Weather MCP server tests

---

END OF DOCUMENT

# AI-005: 2-Minute Drill AI Specification

**Feature ID:** AI-005
**Status:** ✅ IMPLEMENTED
**Priority:** P1
**Author:** Gemini
**Date:** 2025-12-17

---

## Overview

The 2-Minute Drill AI enhances late-game decision making by providing granular urgency levels and play selection adjustments. This enables the simulation to make smarter, more realistic choices when time is critical.

## Components

### 1. UrgencyLevel Enum

Granular urgency levels based on time, score, and timeouts:

| Level      | Condition                     | Behavior                    |
| ---------- | ----------------------------- | --------------------------- |
| `LOW`      | >4 min or winning comfortably | Normal play                 |
| `MEDIUM`   | 2-4 min, need efficiency      | Slightly faster tempo       |
| `HIGH`     | 1-2 min, hurry-up needed      | Fast tempo, sideline routes |
| `CRITICAL` | <1 min, desperation           | Maximum urgency, avoid deep |

### 2. TwoMinuteDrillContext Dataclass

```python
@dataclass
class TwoMinuteDrillContext:
    urgency_level: UrgencyLevel
    clock_strategy: ClockStrategy
    timeouts_remaining: int
    score_deficit: int
    time_remaining: int
    field_position: int
    down: int
    distance: int
    favor_sideline_routes: bool
    avoid_middle_field: bool
    max_pass_depth: str
    spike_recommended: bool
    timeout_recommended: bool
```

### 3. Key Methods

#### `get_urgency_level(situation, timeouts)`

Calculates urgency based on:

- Quarter (only 2nd and 4th matter)
- Time remaining + timeout value (~40s each)
- Score differential

#### `get_two_minute_drill_context(situation, timeouts)`

Builds comprehensive context with recommendations.

#### `get_play_adjustments(situation, timeouts)`

Returns dict with:

- `pass_probability_boost`: 0.0 to 0.35
- `run_penalty`: 0.0 to 0.4
- `deep_pass_penalty`: 0.0 to 0.3
- `sideline_route_boost`: 0.0 to 0.25
- `max_play_clock_usage`: 8 to 40 seconds

## Integration Points

### PlayCaller

- `PlayCallingContext.two_minute_adjustments` receives adjustments
- `_decide_run_vs_pass()` uses `pass_probability_boost` and `run_penalty`
- `_create_pass_play()` uses `deep_pass_penalty` and `sideline_route_boost`

### SimulationOrchestrator

- Should call `get_play_adjustments()` before play selection
- Should pass adjustments to PlayCaller via context

## Files Modified

- [clock_management.py](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/backend/app/services/playbook/clock_management.py)
- [play_caller.py](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/backend/app/orchestrator/play_caller.py)
- [test_clock_management.py](file:///c:/Users/cweir/Documents/GitHub/THE%20NFL%20SIM/backend/tests/unit/test_clock_management.py)

## Test Coverage

9 unit tests covering:

- Urgency level detection (CRITICAL, HIGH, LOW scenarios)
- Context generation
- Play adjustment calculations

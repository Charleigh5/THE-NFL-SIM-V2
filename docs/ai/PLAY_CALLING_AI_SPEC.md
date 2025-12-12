# Play Calling AI Specification

**Document ID:** AI-001
**Status:** SPEC_COMPLETE
**Last Updated:** 2025-12-12

---

## 1. Design Philosophy

### Core Principles

1. **Authenticity First**: Decisions must "feel" like real NFL coaching
2. **Analytics-Informed**: Use verified NFL statistics as decision basis
3. **Personality-Driven**: Different coaches make different calls
4. **Context-Aware**: Game situation drives every decision
5. **Unpredictability Balance**: Not robotic, but not random

### Immersion Critical Points

From user feedback, these break immersion:

- ❌ Running out the clock when behind
- ❌ Punting on 4th-and-1 at midfield
- ❌ Passing 80% when leading by 21
- ❌ Never using timeouts strategically
- ❌ Ignoring personnel mismatches

---

## 2. Coach Personality Archetypes

### 2.1 Personality Attributes

| Attribute         | Range   | Description             |
| ----------------- | ------- | ----------------------- |
| `aggression`      | 0.0-1.0 | 4th down/2-pt decisions |
| `pass_tendency`   | 0.0-1.0 | Base run/pass ratio     |
| `analytics_trust` | 0.0-1.0 | Follow optimal vs gut   |
| `blitz_rate`      | 0.0-1.0 | Defensive aggression    |
| `risk_tolerance`  | 0.0-1.0 | Deep shots, trick plays |

### 2.2 Archetype Definitions

| Archetype          | Aggression | Pass | Analytics | Model            |
| ------------------ | ---------- | ---- | --------- | ---------------- |
| **Conservative**   | 0.25       | 0.45 | 0.3       | Old school       |
| **Balanced**       | 0.50       | 0.55 | 0.6       | Modern average   |
| **Aggressive**     | 0.75       | 0.60 | 0.8       | Analytics-driven |
| **Air Raid**       | 0.65       | 0.70 | 0.5       | Pass-heavy       |
| **Ground Control** | 0.40       | 0.35 | 0.4       | Run-first        |

### 2.3 Real Coach Mappings

| Coach          | Archetype    | Notes                                   |
| -------------- | ------------ | --------------------------------------- |
| Andy Reid      | Air Raid     | 0.7 pass, experiments in regular season |
| Sean McVay     | Aggressive   | Uses AI/analytics, play sequencing      |
| Kyle Shanahan  | Balanced     | Strategic deception, condensed sets     |
| Bill Belichick | Conservative | Situational adaptation                  |
| Doug Pederson  | Aggressive   | High 4th down conversion rates          |

---

## 3. Situation Assessment

### 3.1 Game State Variables

```python
@dataclass
class GameState:
    quarter: int              # 1-4 (5+ = OT)
    time_remaining: int       # Seconds in quarter
    down: int                 # 1-4
    distance: int             # Yards to first down
    yard_line: int           # 1-99 (own 1 to opp 1)
    score_diff: int          # +/- from offense perspective
    timeouts_offense: int    # 0-3
    timeouts_defense: int    # 0-3
    possession: str          # "home" / "away"
```

### 3.2 Priority Calculation

```python
def calculate_situation_priority(state: GameState) -> str:
    """Determine primary strategic mode."""
    time_pressure = state.time_remaining < 120 and state.quarter in [2, 4]

    if state.score_diff <= -16 and state.quarter >= 4:
        return "DESPERATION"
    elif state.score_diff <= -8 and time_pressure:
        return "CATCH_UP"
    elif state.score_diff >= 14 and state.quarter >= 3:
        return "PROTECT_LEAD"
    elif state.score_diff >= 8:
        return "MAINTAIN"
    elif time_pressure:
        return "TWO_MINUTE"
    elif state.yard_line <= 20:
        return "RED_ZONE"
    else:
        return "NORMAL"
```

---

## 4. Play Selection Algorithm

### 4.1 Base Pass Rate Formula

```python
def calculate_pass_rate(coach, state: GameState) -> float:
    """Calculate pass probability based on situation."""
    base = coach.pass_tendency  # 0.35-0.70 typically

    # Down adjustments (verified NFL data)
    if state.down == 1:
        adjustment = 0.0
    elif state.down == 2 and state.distance >= 7:
        adjustment = 0.15
    elif state.down == 3:
        if state.distance >= 7:
            adjustment = 0.35  # 3rd and long = pass heavy
        elif state.distance <= 2:
            adjustment = -0.10  # 3rd and short = run viable
        else:
            adjustment = 0.15
    else:  # 4th down (if going for it)
        if state.distance <= 2:
            adjustment = -0.15
        else:
            adjustment = 0.20

    # Score differential (NFL data: trailing = more pass)
    if state.score_diff <= -8:
        score_adj = 0.25 + (min(abs(state.score_diff), 24) / 100)
    elif state.score_diff >= 8:
        score_adj = -0.20 - (min(state.score_diff, 24) / 100)
    else:
        score_adj = state.score_diff * -0.02

    # Time pressure
    if state.time_remaining < 120 and state.quarter in [2, 4]:
        if state.score_diff < 0:
            time_adj = 0.30  # Trailing: pass to save clock
        else:
            time_adj = -0.25  # Leading: run to kill clock
    else:
        time_adj = 0.0

    return clamp(base + adjustment + score_adj + time_adj, 0.15, 0.90)
```

### 4.2 Play Type Selection

```python
def select_play_type(coach, state: GameState, pass_rate: float) -> str:
    """Select specific play type based on situation."""
    roll = random.random()

    if roll < pass_rate:
        # Pass play selection
        if state.priority == "TWO_MINUTE":
            return select_hurry_up_pass(state)
        elif state.priority == "RED_ZONE":
            return select_red_zone_pass(state)
        elif state.distance >= 15:
            return select_deep_pass(coach)
        else:
            return select_standard_pass(coach, state)
    else:
        # Run play selection
        if state.yard_line <= 5:
            return select_goal_line_run()
        elif state.distance <= 2:
            return select_short_yardage_run()
        else:
            return select_standard_run(coach)
```

---

## 5. 4th Down Decision Logic

### 5.1 Conversion Rate Data (NFL Verified)

| Distance   | Success Rate | Go Threshold  |
| ---------- | ------------ | ------------- |
| 4th-and-1  | 68.6%        | Almost always |
| 4th-and-2  | 57.8%        | Often         |
| 4th-and-3  | 51%          | Situational   |
| 4th-and-4+ | 40-45%       | Rarely        |

### 5.2 Decision Tree

```python
def decide_4th_down(coach, state: GameState) -> str:
    """Returns: 'GO', 'PUNT', 'FG'"""

    # Field goal range check (yard_line = distance to goal)
    fg_range = state.yard_line <= 40
    fg_probability = calculate_fg_probability(state.yard_line)

    # Go-for-it win probability gain
    conversion_prob = CONVERSION_RATES.get(state.distance, 0.40)
    go_wp_gain = calculate_go_wp_gain(state, conversion_prob)

    # Desperation overrides
    if state.priority == "DESPERATION":
        return "GO"

    # Analytics threshold: go if WP gain >= 3% (verified NFL standard)
    if go_wp_gain >= 0.03 and coach.analytics_trust > 0.5:
        return "GO"

    # Aggression-based decisions
    aggression_threshold = 2 + (1 - coach.aggression) * 3  # 2-5 yards

    if state.distance <= 1:
        # 4th-and-1: most coaches go
        if state.yard_line > 40:  # Not in own territory
            return "GO"

    if state.distance <= aggression_threshold:
        if state.yard_line >= 35 and state.yard_line <= 60:
            # "No man's land" - often go for it
            if coach.aggression > 0.5:
                return "GO"

    # Goal line (inside 3)
    if state.yard_line <= 3:
        return "GO"

    # Field goal decision
    if fg_range and fg_probability > 0.70:
        return "FG"

    return "PUNT"
```

---

## 6. Clock Management

### 6.1 Two-Minute Drill

```python
def two_minute_drill_logic(coach, state: GameState) -> dict:
    """Manage end-of-half/game scenarios."""

    adjustments = {
        "tempo": "HURRY_UP",
        "play_calls": [],
        "timeout_strategy": None
    }

    if state.score_diff < 0:
        # Trailing: maximize plays
        adjustments["pass_rate"] = 0.85
        adjustments["target_sidelines"] = True
        adjustments["avoid_sacks"] = True

        # Timeout usage
        if state.time_remaining < 45 and state.timeouts_offense > 0:
            adjustments["use_timeout"] = True
    else:
        # Leading: kill clock
        adjustments["pass_rate"] = 0.25
        adjustments["tempo"] = "SLOW"
        adjustments["run_out_of_bounds"] = False

    return adjustments
```

### 6.2 Timeout Strategy

| Situation            | Timeout Decision     | Rationale             |
| -------------------- | -------------------- | --------------------- |
| Trailing, <2 min Q4  | Use aggressively     | Maximize plays        |
| Before 2-min warning | Never call D timeout | Free pass for offense |
| Leading, <2 min Q4   | Preserve             | For emergency         |
| Goal line stand      | Consider             | Ice kicker / adjust D |

---

## 7. Red Zone Logic

### 7.1 Tendencies (Verified NFL Data)

| Metric            | Value              |
| ----------------- | ------------------ |
| Pass/Run Ratio    | 1.15 (55% pass)    |
| Rush Success Rate | 45%                |
| Pass Success Rate | 37%                |
| Optimal Strategy  | Slightly run-heavy |

### 7.2 Red Zone Adjustments

```python
def red_zone_adjustments(coach, state: GameState) -> dict:
    """Adjust play calling inside the 20."""

    # Increase run rate (more efficient per NFL data)
    run_bonus = 0.08

    if state.yard_line <= 5:
        # Goal line: run heavy
        run_bonus = 0.15

    if state.down == 3:
        # 3rd down: revert to passing
        run_bonus = -0.05

    return {
        "run_rate_adjustment": run_bonus,
        "prefer_play_action": state.yard_line > 10,
        "short_routes": True
    }
```

---

## 8. Defensive Play Calling

### 8.1 Coverage Selection

```python
def select_coverage(coach, offense_tendency, state: GameState) -> str:
    """Select coverage based on situation."""

    # Base tendencies (NFL 2024 data)
    coverages = {
        "cover_3": 0.35,
        "cover_1": 0.20,
        "cover_2": 0.15,
        "cover_4": 0.15,
        "cover_6": 0.10,
        "cover_0": 0.05
    }

    # Adjust for down/distance
    if state.distance >= 10:
        coverages["cover_4"] += 0.15
        coverages["cover_3"] -= 0.10
    elif state.distance <= 2:
        coverages["cover_1"] += 0.15
        coverages["cover_0"] += 0.05

    # Red zone: more man coverage
    if state.yard_line <= 20:
        coverages["cover_1"] += 0.10
        coverages["cover_0"] += 0.05

    return weighted_random_choice(coverages)
```

### 8.2 Blitz Logic

```python
def should_blitz(coach, state: GameState) -> bool:
    """Determine if blitz is appropriate."""

    base_rate = coach.blitz_rate  # 0.20-0.35 typically

    # 3rd and long: more blitz
    if state.down == 3 and state.distance >= 7:
        base_rate += 0.15

    # Red zone: more aggressive
    if state.yard_line <= 20:
        base_rate += 0.10

    # Behind late: increase pressure
    if state.score_diff < -8 and state.quarter >= 4:
        base_rate += 0.10

    return random.random() < clamp(base_rate, 0.05, 0.45)
```

---

## 9. Adaptation System

### 9.1 In-Game Learning

```python
class GameAdaptation:
    def __init__(self):
        self.opponent_tendencies = {}
        self.success_tracking = {}

    def record_play(self, play_type, result, context):
        """Track what's working and what isn't."""
        key = (play_type, context.down, context.distance_bucket)
        if key not in self.success_tracking:
            self.success_tracking[key] = {"attempts": 0, "success": 0}
        self.success_tracking[key]["attempts"] += 1
        if result.success:
            self.success_tracking[key]["success"] += 1

    def get_adjustment(self, play_type, context) -> float:
        """Adjust play calling based on game success."""
        key = (play_type, context.down, context.distance_bucket)
        if key in self.success_tracking:
            data = self.success_tracking[key]
            if data["attempts"] >= 3:
                success_rate = data["success"] / data["attempts"]
                expected = 0.50
                return (success_rate - expected) * 0.10  # ±5% adj
        return 0.0
```

### 9.2 Halftime Adjustments

```python
def halftime_adjustments(offense_stats, defense_stats) -> dict:
    """Make strategic adjustments at halftime."""
    adjustments = {}

    # If run game working, increase
    if offense_stats.yards_per_rush > 5.0:
        adjustments["run_rate"] = +0.10
    elif offense_stats.yards_per_rush < 3.0:
        adjustments["run_rate"] = -0.10

    # If getting pressured, adjust
    if offense_stats.sack_rate > 0.08:
        adjustments["quick_game"] = +0.15
        adjustments["max_protect"] = +0.10

    # If coverage is getting beat
    if defense_stats.yards_per_pass > 8.0:
        adjustments["two_high"] = +0.15

    return adjustments
```

---

## 10. Validation Metrics

### 10.1 Distribution Targets

Over 1000 simulated games:

| Metric           | NFL Target | Tolerance |
| ---------------- | ---------- | --------- |
| League Pass Rate | 55-58%     | ±3%       |
| 4th Down Go Rate | 25-30%     | ±5%       |
| 4th Down Success | 55-60%     | ±5%       |
| Blitz Rate       | 25-28%     | ±3%       |
| Red Zone TD %    | 55-60%     | ±5%       |

### 10.2 Immersion Tests

- [ ] Trailing teams pass more late
- [ ] Leading teams run more late
- [ ] 4th-and-1 almost always go
- [ ] Timeouts used logically
- [ ] Coach personalities feel distinct

---

## Changelog

| Date       | Change                                       |
| ---------- | -------------------------------------------- |
| 2025-12-12 | Initial creation with verified NFL analytics |

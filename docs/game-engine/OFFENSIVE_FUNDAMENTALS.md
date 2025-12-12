# NFL Offensive Fundamentals Analysis (2020-2024)

**Document ID:** GAME-001a
**Status:** SPEC_COMPLETE
**Last Updated:** 2025-12-12

---

## 1. League-Wide Offensive Trends

### Run/Pass Ratios by Team (2020-2024)

| Season | Highest Run % | Lowest Run %   | Trend              |
| ------ | ------------- | -------------- | ------------------ |
| 2020   | Ravens 57.8%  | Falcons 39.4%  | Pass-heavy peak    |
| 2021   | Eagles 52.7%  | Falcons 40.7%  | Slight shift       |
| 2022   | Bears 59.7%   | Cardinals 39%  | Run emerging       |
| 2023   | Ravens 52.3%  | Chiefs 39.6%   | Balance returns    |
| 2024   | Eagles 58.1%  | Seahawks 39.2% | **Run resurgence** |

### Key Metrics

- **Rushing Success Rate:** 30.13% (2024), up from 28.84% (2023)
- **Passing EPA/play:** ~0.06 average
- **Rushing EPA/play:** ~-0.09 average
- **Net EPA advantage for passing:** ~0.15 per play

---

## 2. Situational Play Calling

### Score Differential Impact

| Score State        | 1st Down Pass Rate | Behavior                    |
| ------------------ | ------------------ | --------------------------- |
| Leading 8+         | 40-50%             | Run-heavy, clock management |
| Trailing 8+ (late) | ~90%               | Desperation passing         |
| Tied/1-score       | 55-60%             | Balanced approach           |

**Implementation Formula:**

```python
def adjust_pass_rate(base_rate, score_diff, minutes_remaining):
    if score_diff <= -8:
        if minutes_remaining < 10:
            return min(0.90, base_rate + 0.30)  # Catch-up mode
        return base_rate + 0.15
    elif score_diff >= 8:
        if minutes_remaining < 10:
            return max(0.35, base_rate - 0.25)  # Kill clock
        return base_rate - 0.10
    return base_rate  # Neutral game
```

### Down and Distance Patterns

| Situation          | Pass Rate | Notes                          |
| ------------------ | --------- | ------------------------------ |
| 1st & 10           | 50-55%    | Balanced, establish run threat |
| 2nd & Long (7+)    | 65-70%    | Must move chains               |
| 2nd & Short (1-3)  | 45%       | Run-heavy                      |
| 3rd & Long (7+)    | 85-90%    | Passing critical               |
| 3rd & Short (1-3)  | 50-55%    | Mixed; run can work            |
| 3rd & Medium (4-6) | 70-75%    | Passing favored                |

### 3rd Down Conversion Rates

- **League Average:** 39-45%
- **Top Teams:** ~50% (Green Bay 2024: 50.6%)
- **Bottom Teams:** ~30% (Tennessee 2024: 29.9%)

---

## 3. Red Zone Tendencies

### Play Type Distribution

| Season | Pass/Run Ratio  | Rush Success | Pass Success           |
| ------ | --------------- | ------------ | ---------------------- |
| 2020   | 1.04 (49% pass) | 46%          | 42%                    |
| 2021   | 1.09            | 46%          | 42%                    |
| 2022   | 1.15            | 46%          | 40%                    |
| 2023   | 1.09            | 46%          | 39%                    |
| 2024   | 1.15            | 45.3%        | **37.3%** (decade low) |

**Key Insight:** Rushing is more efficient in red zone despite teams passing more.

### TD Conversion Rates

- **Top Teams:** 65-70% TD rate (PHI: 71%, GB: 68%)
- **Average Teams:** 55-60%
- **Poor Teams:** 44-50%

---

## 4. 2-Minute Drill Efficiency

### Critical Metrics

| Metric              | Value                     | Source           |
| ------------------- | ------------------------- | ---------------- |
| FG Range Success    | ~70%                      | Reddit 2025 data |
| Timeout Usage       | Strategic importance high | N/A              |
| No-Huddle Advantage | +1-2 yards/play           | Sharp Football   |

### Implementation Behavior

```python
def two_minute_drill_adjustments(game_state):
    if game_state.time_remaining < 120:  # 2 minutes
        return {
            "pass_rate_boost": 0.25,
            "target_sideline_routes": True,
            "hurry_up_tempo": True,
            "avoid_sacks_priority": "HIGH",
            "clock_awareness": True
        }
```

---

## 5. Offensive Schemes

### Scheme Distribution (2024)

| Scheme           | Teams | Characteristics                            |
| ---------------- | ----- | ------------------------------------------ |
| **West Coast**   | 23    | Short passes, YAC focus, high completion % |
| **Spread**       | 2     | Shotgun, multiple WRs, horizontal stretch  |
| **Hybrid/Other** | 7     | Custom blends                              |

### West Coast Offense

**Philosophy:** "Take what the defense gives you"

| Attribute         | Value                           |
| ----------------- | ------------------------------- |
| Pass Depth        | 3-15 yards (short/intermediate) |
| Completion Target | 65-70%                          |
| YAC Emphasis      | High                            |
| Run/Pass Balance  | 45-55% run                      |
| Key Routes        | Slants, outs, crosses           |

**Notable Practitioners:** Andy Reid, Kyle Shanahan

### Formation Trends

| Formation Type | 2020 | 2024 | Pass % | YPA     |
| -------------- | ---- | ---- | ------ | ------- |
| Spread         | 46%  | 40%  | 79%    | 6.7     |
| Condensed      | 38%  | 44%  | 49%    | **7.7** |

**Key Finding:** Condensed formations gain a full yard more per pass attempt.

---

## 6. Play Action Effectiveness

### Performance Data

| Metric                 | Value | Context               |
| ---------------------- | ----- | --------------------- |
| Play-Action Rate (top) | 46.6% | Ravens scripted plays |
| PA EPA Leader          | +56.9 | Stafford 2024         |
| PA Success Rate        | 55.8% | Rams (4th in NFL)     |
| PA Yards/Play          | 9.0   | When effective        |
| PA TD:INT Ratio        | 10:0  | Stafford 2024         |
| PA Pressure Rate       | 27.1% | Lower than dropback   |

### Simulation Formula

```python
def calculate_play_action_bonus(qb, rb_rushing_success):
    """Play action is more effective with credible run threat."""
    base_bonus = 0.10  # Always some deception value
    run_credibility = rb_rushing_success * 0.15  # 0-15% bonus

    return {
        "completion_bonus": base_bonus + run_credibility,
        "yac_bonus": 0.08,  # Defenders slow to react
        "sack_reduction": 0.05  # LBs bite on run fake
    }
```

---

## 7. Statistical Benchmarks for Simulation

### Expected Yards Per Play

| Play Type   | Mean | Std Dev | Notes               |
| ----------- | ---- | ------- | ------------------- |
| All Plays   | 5.4  | 8.0     | High variance       |
| Rush        | 4.2  | 5.5     | Lower ceiling       |
| Pass        | 6.8  | 12.0    | Explosive potential |
| Play-Action | 8.5  | 10.0    | Premium efficiency  |
| Screen      | 5.0  | 7.0     | Safe, moderate gain |

### Success Rate Thresholds

- **1st Down:** 40% of needed yards (4+ yards)
- **2nd Down:** 50% of remaining
- **3rd/4th Down:** 100% (move chains)

### Explosive Play Frequency

| Type           | Threshold | Frequency      |
| -------------- | --------- | -------------- |
| Big Run        | 10+ yards | ~12% of rushes |
| Explosive Run  | 20+ yards | ~2%            |
| Big Pass       | 15+ yards | ~20%           |
| Explosive Pass | 40+ yards | ~3%            |

---

## 8. Calibration Targets

For simulation validation, target these league averages:

| Metric          | Target | Tolerance |
| --------------- | ------ | --------- |
| Points/Game     | 22.5   | ±2.0      |
| Yards/Game      | 340    | ±20       |
| Pass Yards/Game | 215    | ±15       |
| Rush Yards/Game | 115    | ±10       |
| 3rd Down %      | 42%    | ±3%       |
| Red Zone TD%    | 58%    | ±5%       |
| Turnovers/Game  | 1.3    | ±0.3      |

---

## Changelog

| Date       | Change                               |
| ---------- | ------------------------------------ |
| 2025-12-12 | Initial creation with 2020-2024 data |

# NFL Defensive Fundamentals Analysis (2020-2024)

**Document ID:** GAME-001b
**Status:** SPEC_COMPLETE
**Last Updated:** 2025-12-12

---

## 1. Defensive Scheme Distribution

### Base Fronts (2024)

| Front   | Teams | Characteristics                     |
| ------- | ----- | ----------------------------------- |
| **3-4** | 17    | 3 DL, 4 LB; flexible blitz packages |
| **4-3** | 15    | 4 DL, 3 LB; one-on-one pass rush    |

**Notable 3-4 Teams:** Eagles, Ravens, Steelers, Broncos
**Notable 4-3 Teams:** Cowboys, Colts, Lions

### Hybrid Trend

Most teams now blend fronts based on personnel packages:

- Nickel (5 DB) is effectively the base defense
- Pure 3-4 or 4-3 only on early downs vs 21/22 personnel

---

## 2. Coverage Schemes

### Coverage Type Distribution

| Coverage         | 2020 | 2023  | 2024 | Trend        |
| ---------------- | ---- | ----- | ---- | ------------ |
| Cover 3          | 38%  | 36.1% | 34%  | ⬇️ Declining |
| Cover 1 (Man)    | 26%  | 18.7% | 21%  | ⬆️ Returning |
| Cover 2          | 11%  | 13%   | 14%  | ⬆️ Rising    |
| Cover 4/Quarters | 11%  | 14.2% | 15%  | ⬆️ Rising    |
| Cover 0          | 2.7% | 4.0%  | 4%   | Stable       |
| Cover 6          | 8%   | 10%   | 12%  | ⬆️ Rising    |

### Man vs Zone Trends

| Metric             | 2020  | 2023 | Change    |
| ------------------ | ----- | ---- | --------- |
| Man Coverage Rate  | 30.8% | 24%  | **-6.8%** |
| Zone Coverage Rate | 69.2% | 76%  | +6.8%     |

**Key Finding:** NFL becoming a "zone league" - man coverage declining.

### Two-High Safety Revolution

| Year | Two-High % on Pass Plays |
| ---- | ------------------------ |
| 2019 | 44%                      |
| 2024 | **63%**                  |

This is the biggest defensive shift since 2018.

---

## 3. Coverage Effectiveness (EPA)

### Zone vs Man Performance

| Metric           | Zone   | Man    | Advantage         |
| ---------------- | ------ | ------ | ----------------- |
| EPA Allowed/Play | Lower  | Higher | Zone 10.4% better |
| WPA Allowed/Play | Lower  | Higher | Zone 22.8% better |
| Success Rate     | Higher | Lower  | Zone preferred    |

### Implementation Formula

```python
def calculate_coverage_success(coverage_type, receiver, defender):
    """Base success rates by coverage type."""
    base_rates = {
        "cover_0": 0.55,  # High risk/reward
        "cover_1": 0.60,  # Solid man
        "cover_2": 0.65,  # Zone shell
        "cover_3": 0.63,  # Most common
        "cover_4": 0.68,  # Deep prevention
        "cover_6": 0.65   # Split coverage
    }

    base = base_rates.get(coverage_type, 0.60)

    # Adjust for matchup
    matchup_diff = (defender.coverage - receiver.route_running) / 100

    return clamp(base + matchup_diff * 0.15, 0.30, 0.85)
```

---

## 4. Pass Rush Statistics

### Pressure Trends

| Metric             | 2020 | 2024      | Trend                 |
| ------------------ | ---- | --------- | --------------------- |
| QB Under Pressure  | 28%  | **31%**   | ⬆️ Highest since 2020 |
| 5+ Rushers (Blitz) | 24%  | **26.8%** | ⬆️ Rising             |
| 6+ Rushers         | 5%   | **6.6%**  | ⬆️ Rising             |

### 4-Man Rush Effectiveness

| Team (2024) | 4-Man Pressure Rate | Notes         |
| ----------- | ------------------- | ------------- |
| Vikings     | 44.4%               | Elite         |
| Broncos     | 39.3%               | Top tier      |
| Browns      | 38.2%               | Strong        |
| Seahawks    | 36.6%               | Above average |
| Eagles      | 35.5%               | Solid         |
| Lions       | 35.2%               | Solid         |

**Key Insight:** Teams generating 35%+ pressure with 4-man rush win more games.

### Blitz Effectiveness

| Rushers | DVOA (2024) | Interpretation      |
| ------- | ----------- | ------------------- |
| 4       | 6.8%        | Baseline            |
| 5       | **4.2%**    | Most effective      |
| 6+      | 7.0%        | Diminishing returns |

**Strategy:** 5-man rush is optimal balance of pressure and coverage.

---

## 5. Run Defense

### Gap Responsibility

```
3-4 Defense:
NT (0-tech): A-Gap control
DE (5-tech): B-Gap/C-Gap
OLB: Edge containment
ILB: Fill downhill

4-3 Defense:
DT (3-tech): B-Gap penetration
DT (1-tech): A-Gap anchor
DE: C-Gap/Edge
LB: Read and react
```

### Run Defense Success Rate

- **League Average:** 70% stop rate (< 4 yards)
- **Top Defenses:** 75%+ stop rate
- **Gap Integrity:** Critical for run stuffing

---

## 6. Defensive Situational Adjustments

### By Down and Distance

| Situation   | Typical Coverage | Blitz Rate |
| ----------- | ---------------- | ---------- |
| 1st & 10    | Cover 3/4        | 20%        |
| 2nd & Long  | Cover 2/4        | 25%        |
| 3rd & Short | Cover 1/0        | 35%        |
| 3rd & Long  | Cover 2/4        | 30%        |
| Red Zone    | Cover 1/3        | 40%        |

### Implementation

```python
def select_defensive_call(down, distance, field_position):
    if down == 3:
        if distance <= 2:
            return {"coverage": "cover_1", "blitz_rate": 0.35}
        elif distance >= 8:
            return {"coverage": "cover_4", "blitz_rate": 0.25}
        else:
            return {"coverage": "cover_3", "blitz_rate": 0.30}
    elif field_position <= 20:  # Red zone
        return {"coverage": "cover_1", "blitz_rate": 0.40}
    else:
        return {"coverage": "cover_3", "blitz_rate": 0.22}
```

---

## 7. Key Matchup Resolution

### Pass Coverage Interactions

| Offensive Concept | Weak Against     | Strong Against   |
| ----------------- | ---------------- | ---------------- |
| Deep routes       | Cover 1, Cover 0 | Cover 4, Cover 2 |
| Slants/Crosses    | Cover 3          | Cover 2, Cover 1 |
| Out routes        | Cover 3          | Cover 2          |
| Seams             | Cover 2, Cover 4 | Cover 3          |
| Screens           | All zone         | Man              |

### Pass Rush Interactions

| Rush Type      | Effective Against   | Countered By         |
| -------------- | ------------------- | -------------------- |
| 4-man          | Standard protection | Slide protection     |
| Zone blitz     | Play-action         | Quick game           |
| Edge blitz     | 7-step drops        | Roll-outs, screens   |
| Interior blitz | Heavy sets          | Spread, quick slants |

---

## 8. Calibration Targets

For simulation validation:

| Metric              | Target | Tolerance |
| ------------------- | ------ | --------- |
| Points Allowed/Game | 22.5   | ±2.0      |
| Yards Allowed/Game  | 340    | ±20       |
| Sacks/Game          | 2.5    | ±0.5      |
| INTs/Game           | 0.8    | ±0.2      |
| 3rd Down Stop %     | 58%    | ±3%       |
| Red Zone Stop %     | 42%    | ±5%       |
| Pressure Rate       | 30%    | ±3%       |

---

## Changelog

| Date       | Change                               |
| ---------- | ------------------------------------ |
| 2025-12-12 | Initial creation with 2020-2024 data |

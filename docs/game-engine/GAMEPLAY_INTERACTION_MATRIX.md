# Gameplay Interaction Matrix

**Document ID:** GAME-001c
**Status:** SPEC_COMPLETE
**Last Updated:** 2025-12-12

---

## 1. Pass Play Resolution Model

### 1.1 Protection vs Pass Rush

#### Line Battle Resolution

```python
def resolve_line_battle(ol_player, dl_player, scheme_bonus=0):
    """
    Returns: BlockingResult (WIN, STALEMATE, LOSS, PANCAKE)
    """
    ol_rating = ol_player.pass_block + scheme_bonus
    dl_rating = (dl_player.pass_rush_power + dl_player.pass_rush_finesse) / 2

    differential = ol_rating - dl_rating
    roll = random.randint(0, 100)

    # Thresholds based on NFL data
    if differential > 15:
        if roll < 10: return "PANCAKE"  # OL dominates
        if roll < 80: return "WIN"
        return "STALEMATE"
    elif differential > 0:
        if roll < 5: return "PANCAKE"
        if roll < 55: return "WIN"
        if roll < 85: return "STALEMATE"
        return "LOSS"
    elif differential > -15:
        if roll < 35: return "WIN"
        if roll < 70: return "STALEMATE"
        if roll < 95: return "LOSS"
        return "PANCAKE"  # DL pancakes OL
    else:
        if roll < 20: return "STALEMATE"
        if roll < 60: return "LOSS"
        return "PANCAKE"
```

#### Pressure Timeline

| OL Result    | Time to Pressure | Sack Risk |
| ------------ | ---------------- | --------- |
| PANCAKE (DL) | Immediate        | 75%       |
| LOSS         | 1.5-2.0 sec      | 25-40%    |
| STALEMATE    | 2.5-3.0 sec      | 10%       |
| WIN          | 3.5+ sec         | 5%        |
| PANCAKE (OL) | Clean pocket     | 2%        |

### 1.2 Sack Probability Formula

```python
def calculate_sack_probability(pressure_level, qb, ol_chemistry):
    """
    Based on NFL data: ~6.7% of dropbacks result in sacks.
    Pressure ~31% of dropbacks.
    Sack given pressure: ~22%
    """
    initial_prob = 0.15 * pressure_level

    # QB Pocket Presence mitigation (99 rating = 49.5% reduction)
    presence_factor = qb.pocket_presence * 0.005

    # OL Chemistry bonus (max 15% reduction)
    chemistry_factor = ol_chemistry * 0.003

    # Athletic escape (speed, agility, accel)
    escape_rating = (qb.speed + qb.agility + qb.acceleration) / 3
    escape_factor = escape_rating / 100 * 0.15

    final_prob = initial_prob * (1 - presence_factor) * (1 - chemistry_factor) * (1 - escape_factor)
    return clamp(final_prob, 0.02, 0.75)
```

---

## 2. Route vs Coverage Matchups

### 2.1 Separation Probability Matrix

| Route Type | vs Man | vs Cover 2 | vs Cover 3 | vs Cover 4 |
| ---------- | ------ | ---------- | ---------- | ---------- |
| Go/Fade    | 0.35   | 0.30       | 0.40       | 0.25       |
| Post       | 0.40   | 0.35       | 0.50       | 0.30       |
| Corner     | 0.40   | 0.60       | 0.35       | 0.30       |
| Out        | 0.50   | 0.65       | 0.45       | 0.50       |
| Slant      | 0.55   | 0.50       | 0.65       | 0.55       |
| Curl       | 0.50   | 0.55       | 0.60       | 0.50       |
| Flat       | 0.60   | 0.40       | 0.50       | 0.55       |
| Seam       | 0.45   | 0.70       | 0.40       | 0.65       |
| Cross      | 0.55   | 0.45       | 0.70       | 0.50       |

### 2.2 Completion Probability Formula

```python
def calculate_completion_probability(
    qb, receiver, defender, route, coverage,
    weather_modifier=1.0, fatigue_modifier=1.0
):
    # Base from route vs coverage matrix
    base_separation = ROUTE_COVERAGE_MATRIX[route][coverage]

    # WR skill adjustment
    route_skill = receiver.route_running / 100
    separation_bonus = (route_skill - 0.75) * 0.20  # ±10%

    # Defender skill adjustment
    coverage_skill = defender.man_coverage if coverage == "man" else defender.zone_coverage
    coverage_penalty = (coverage_skill / 100 - 0.75) * 0.15  # ±7.5%

    # Speed differential for deep routes
    if route in ["go", "post", "corner"]:
        speed_diff = (receiver.speed - defender.speed) / 100
        separation_bonus += speed_diff * 0.10

    # QB accuracy by depth
    if route in ["go", "post", "corner"]:
        accuracy = qb.throw_accuracy_deep
    elif route in ["curl", "out", "seam"]:
        accuracy = qb.throw_accuracy_mid
    else:
        accuracy = qb.throw_accuracy_short

    accuracy_factor = accuracy / 100

    # Final calculation
    raw_prob = base_separation + separation_bonus - coverage_penalty
    final_prob = raw_prob * accuracy_factor * weather_modifier * fatigue_modifier

    return clamp(final_prob, 0.10, 0.95)
```

---

## 3. Run Play Resolution Model

### 3.1 Blocking Scheme Effectiveness

| Scheme       | vs 4-3 Under | vs 4-3 Over | vs 3-4 | vs Nickel |
| ------------ | ------------ | ----------- | ------ | --------- |
| Inside Zone  | 0.55         | 0.50        | 0.45   | 0.60      |
| Outside Zone | 0.50         | 0.55        | 0.50   | 0.65      |
| Power        | 0.60         | 0.55        | 0.60   | 0.50      |
| Counter      | 0.55         | 0.60        | 0.55   | 0.55      |
| Stretch      | 0.45         | 0.50        | 0.45   | 0.70      |

### 3.2 Run Yards Formula

```python
def calculate_run_yards(rb, blockers, defenders, play_type, game_context):
    # Base yards by RB tribe
    TRIBE_STATS = {
        "POWER": {"base": 4.0, "std": 1.5, "breakaway": 0.8, "fumble": 0.8},
        "SCAT": {"base": 3.0, "std": 2.5, "breakaway": 1.5, "fumble": 1.2},
        "BALANCED": {"base": 3.5, "std": 2.0, "breakaway": 1.0, "fumble": 1.0}
    }

    tribe = classify_rb_tribe(rb)
    stats = TRIBE_STATS[tribe]

    # Blocking success (average of OL grades)
    block_quality = calculate_blocking_quality(blockers, defenders)

    # Base yardage with variance
    base_yards = random.gauss(stats["base"], stats["std"])
    blocking_modifier = (block_quality - 0.5) * 4.0  # ±2 yards

    yards = base_yards + blocking_modifier

    # Breakaway check (10% base chance for 10+ yard run)
    breakaway_roll = random.random()
    breakaway_threshold = 0.12 * stats["breakaway"] * (rb.speed / 80)
    if breakaway_roll < breakaway_threshold:
        yards += random.randint(10, 40)

    return max(yards, -2)  # Minimum -2 yard loss
```

---

## 4. Turnover Probabilities

### 4.1 Interception Model

| Situation       | Base Rate | Modifier Sources      |
| --------------- | --------- | --------------------- |
| Standard pass   | 1.5%      | QB decision, coverage |
| Contested catch | 4.0%      | Defender ball skills  |
| Pressure throw  | 3.0%      | QB under pressure     |
| Tipped ball     | 8.0%      | After deflection      |
| Weather (rain)  | +0.5%     | Wet ball              |

```python
def calculate_int_probability(qb, receiver, defender, is_contested, under_pressure):
    base = 0.015

    if is_contested:
        base = 0.04
        base += (defender.catching / 100) * 0.02
        base -= (receiver.catching / 100) * 0.015

    if under_pressure:
        base += 0.015
        base -= (qb.throw_under_pressure / 100) * 0.01

    # QB decision-making
    base -= (qb.awareness / 100) * 0.01

    return clamp(base, 0.005, 0.15)
```

### 4.2 Fumble Model

| Situation          | Base Rate | Risk Factors          |
| ------------------ | --------- | --------------------- |
| Standard carry     | 1.0%      | Carrier ball security |
| High-powered hit   | 2.5%      | Defender hit power    |
| Gang tackle        | 1.8%      | Multiple defenders    |
| Fatigued carrier   | +0.5%     | Stamina < 50          |
| Weather (rain/mud) | +0.8%     | Field conditions      |

---

## 5. Yards After Catch (YAC)

### 5.1 YAC by Route Type

| Route  | Avg YAC | Variance |
| ------ | ------- | -------- |
| Screen | 6.5     | 5.0      |
| Flat   | 5.0     | 4.0      |
| Slant  | 4.5     | 3.5      |
| Cross  | 4.0     | 3.0      |
| Out    | 2.5     | 2.0      |
| Curl   | 2.0     | 1.5      |
| Deep   | 3.0     | 4.0      |

### 5.2 YAC Formula

```python
def calculate_yac(receiver, defender, route, separation_level):
    base_yac = YAC_BY_ROUTE[route]["avg"]
    variance = YAC_BY_ROUTE[route]["var"]

    # Speed advantage
    speed_diff = receiver.speed - defender.speed
    speed_bonus = speed_diff / 10  # ±3 yards

    # Elusiveness
    elusiveness_bonus = (receiver.agility / 100) * 2.0

    # Separation level (0-1)
    space_bonus = separation_level * 3.0

    # Tackle ability reduction
    tackle_penalty = (defender.tackle / 100) * 2.0

    yac = random.gauss(base_yac + speed_bonus + elusiveness_bonus + space_bonus - tackle_penalty, variance)
    return max(yac, 0)
```

---

## 6. Play Type Interaction Summary

### Offensive Play → Defensive Counter

| Offensive Play | Best Counter     | Weak Against   |
| -------------- | ---------------- | -------------- |
| Inside Run     | 4-3 Under, 3-4   | Nickel, Spread |
| Outside Run    | 4-3 Over, Edge   | Light box      |
| Quick Pass     | Man Blitz        | Zone           |
| Play-Action    | Disciplined Zone | Aggressive LB  |
| Deep Pass      | Cover 4, 2-Deep  | Single High    |
| Screen         | Man Coverage     | Zone           |
| RPO            | Disciplined DE   | Aggressive DE  |

### Defensive Call → Offensive Exploit

| Defense | Exploited By    | Strong Against |
| ------- | --------------- | -------------- |
| Cover 0 | Quick slants    | Deep routes    |
| Cover 1 | Rub routes      | Most           |
| Cover 2 | Seams, corners  | Underneath     |
| Cover 3 | Flats, curls    | Deep middle    |
| Cover 4 | Underneath, run | Deep passes    |
| Blitz   | Quick game      | 7-step drops   |

---

## 7. Validation Metrics

Run 1000 simulated games and compare to NFL averages:

| Metric            | NFL Target | Acceptable Range |
| ----------------- | ---------- | ---------------- |
| Pass Completion % | 65%        | 62-68%           |
| Yards/Attempt     | 7.0        | 6.5-7.5          |
| Yards/Rush        | 4.3        | 4.0-4.6          |
| Sack Rate         | 6.7%       | 5.5-8.0%         |
| Turnover Rate     | 2.5/game   | 2.0-3.0          |
| 3rd Down Conv     | 42%        | 39-45%           |
| Red Zone TD       | 58%        | 54-62%           |

---

## Changelog

| Date       | Change                                     |
| ---------- | ------------------------------------------ |
| 2025-12-12 | Initial creation with interaction matrices |

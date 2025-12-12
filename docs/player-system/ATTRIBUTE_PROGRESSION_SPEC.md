# Attribute Progression System Specification

**Document ID:** RPG-002
**Status:** SPEC_COMPLETE
**Last Updated:** 2025-12-12

---

## 1. Core Philosophy

### Design Principles

1. **Emergent Narratives**: Player development creates stories (late bloomers, busts, comeback years)
2. **Strategic Coaching**: User decisions genuinely impact player growth
3. **Hidden Uncertainty**: Not all potential is immediately known (fog of war)
4. **Realistic Curves**: Physical decline is inevitable; mental growth can continue
5. **Rewarding Investment**: Time spent on development yields tangible results

### Community-Validated Priorities

Based on Reddit/forum research:

- ✅ Separate development speed from trait tier
- ✅ Hidden potential revealed over time
- ✅ Realistic age-based regression
- ✅ Coaching staff influence
- ✅ "Breakout game" mechanics
- ✅ Scheme fit bonuses

---

## 2. Player Rating System

### 2.1 Core Ratings (Visible)

| Rating     | Range | Description                          |
| ---------- | ----- | ------------------------------------ |
| Overall    | 40-99 | Weighted average of attributes       |
| Attributes | 40-99 | Individual skills (50+ per position) |
| Age        | 21-42 | Current age                          |
| Experience | 0-20  | Years in league                      |

### 2.2 Hidden Ratings (Partially Revealed)

| Rating                | Range   | Reveal Mechanic                 |
| --------------------- | ------- | ------------------------------- |
| **Potential**         | 60-99   | Scouting accuracy reveals range |
| **Development Speed** | 0.5-2.0 | Revealed after 500 snaps        |
| **Durability**        | 0.5-1.5 | Revealed via injury history     |
| **Consistency**       | 0.6-1.2 | Revealed after 16 games         |

### 2.3 Development Traits

| Trait     | XP Multiplier | Description          | Acquisition       |
| --------- | ------------- | -------------------- | ----------------- |
| NORMAL    | 1.0x          | Standard progression | Default           |
| STAR      | 1.25x         | Above-average growth | Performance/Draft |
| SUPERSTAR | 1.5x          | Elite development    | Awards/Draft      |
| XFACTOR   | 2.0x          | Generational talent  | Draft only (rare) |

---

## 3. Progression System

### 3.1 XP Sources

| Source             | XP/Week  | Notes                    |
| ------------------ | -------- | ------------------------ |
| Game snaps         | 0.5/snap | Max ~35 XP/game          |
| Practice (light)   | 25       | Low injury risk          |
| Practice (intense) | 40       | Medium injury risk       |
| Film study         | 20       | Mental attributes only   |
| Focus player       | +50%     | One player/week          |
| Scheme fit         | +25%     | Matching playbook        |
| Coaching bonus     | ±20%     | Coach development rating |

### 3.2 XP to Skill Point Formula

```python
def calculate_xp_requirement(player):
    """
    Based on Madden research: younger + lower rated = cheaper.
    """
    base_xp = 500

    # Age factor (exponential after 28)
    if player.age <= 24:
        age_mult = 0.7
    elif player.age <= 27:
        age_mult = 1.0
    elif player.age <= 30:
        age_mult = 1.5
    else:
        age_mult = 2.0 + (player.age - 30) * 0.3

    # Overall factor (harder to improve elites)
    ovr_mult = 1.0 + (player.overall - 70) * 0.02

    # Development trait
    dev_divider = {
        "NORMAL": 1.0,
        "STAR": 0.80,
        "SUPERSTAR": 0.65,
        "XFACTOR": 0.50
    }[player.dev_trait]

    return int(base_xp * age_mult * ovr_mult * dev_divider)
```

### 3.3 Weekly Progression

```python
def process_weekly_progression(player, game_snaps, practice_type, is_focus):
    # Base XP
    xp = game_snaps * 0.5
    xp += PRACTICE_XP[practice_type]

    # Bonuses
    if is_focus:
        xp *= 1.5
    if player.scheme_fit:
        xp *= 1.25
    xp *= player.coach.development_bonus

    # Apply to player
    player.xp_current += xp

    # Check for level up
    required = calculate_xp_requirement(player)
    while player.xp_current >= required:
        player.xp_current -= required
        award_skill_point(player)
        required = calculate_xp_requirement(player)
```

---

## 4. Age Curves by Position

### 4.1 Peak Age Windows

| Position | Peak Start | Peak End | Decline Start |
| -------- | ---------- | -------- | ------------- |
| QB       | 26         | 34       | 37            |
| RB       | 23         | 27       | 28            |
| WR       | 25         | 30       | 31            |
| TE       | 26         | 31       | 32            |
| OL       | 26         | 32       | 33            |
| DL       | 25         | 30       | 31            |
| LB       | 24         | 29       | 30            |
| DB       | 24         | 29       | 30            |
| K/P      | 27         | 38       | 40            |

### 4.2 Attribute Decay Rates

| Attribute Type  | Examples                    | Decay Rate (Post-Peak) |
| --------------- | --------------------------- | ---------------------- |
| Speed/Explosion | Speed, Accel, Agility       | -1 to -3 per year      |
| Power           | Strength, Throw Power       | -0.5 to -1.5 per year  |
| Mental          | Awareness, Play Recognition | 0 to +1 per year       |
| Durability      | Injury Resistance           | -1 to -2 per year      |

### 4.3 Regression Formula

```python
def apply_offseason_regression(player):
    age_past_peak = player.age - PEAK_END[player.position]

    if age_past_peak <= 0:
        return  # Still in prime, no regression

    for attr in player.attributes:
        category = get_attribute_category(attr)
        base_decay = DECAY_RATES[category]

        # Variance for unpredictability
        decay = random.gauss(base_decay * age_past_peak, 0.5)

        # Durability modifier
        decay *= player.durability_rating

        # Apply
        player.set_attribute(attr, player.get_attribute(attr) - decay)
```

---

## 5. Hidden Potential System

### 5.1 Scouting Accuracy

| Scout Level | Potential Range Shown | Example           |
| ----------- | --------------------- | ----------------- |
| Rookie      | ±15 points            | "75-99 potential" |
| Veteran     | ±8 points             | "82-94 potential" |
| Elite       | ±4 points             | "86-92 potential" |

### 5.2 Potential Revelation

```python
def reveal_potential(player, snaps_played):
    if snaps_played >= 1500:  # ~Full season
        player.potential_revealed = True
        player.show_true_potential()
    elif snaps_played >= 500:  # Half season
        player.dev_trait_revealed = True
    # Else: only scouting range shown
```

### 5.3 Bust/Boom Mechanics

| Category    | Potential | Dev Speed | Outcome              |
| ----------- | --------- | --------- | -------------------- |
| **Boom**    | 90+       | 1.5+      | Superstar trajectory |
| **Solid**   | 80-89     | 1.0-1.4   | Reliable starter     |
| **Project** | 75-84     | 0.7-0.9   | Needs time           |
| **Bust**    | <75       | <0.7      | Never develops       |

---

## 6. Trait Acquisition

### 6.1 Acquisition Sources

| Source        | Trigger               | Example                       |
| ------------- | --------------------- | ----------------------------- |
| **Draft**     | Random at generation  | 5% X-Factor, 15% SS, 30% Star |
| **Milestone** | Statistical threshold | 200 carries → "Workhorse"     |
| **Award**     | Season awards         | MVP → Upgrade dev trait       |
| **Breakout**  | Exceptional game      | 3 TD game → "Clutch" check    |

### 6.2 Milestone Triggers

| Trait       | Position | Requirement                     |
| ----------- | -------- | ------------------------------- |
| Workhorse   | RB       | 200+ carries in season          |
| Ironman     | OL       | 48+ games started consecutively |
| Deep Threat | WR       | 10+ catches of 40+ yards        |
| Sack Artist | DL       | 10+ sacks in season             |
| Ball Hawk   | DB       | 5+ interceptions in season      |
| Clutch      | Any      | 3+ game-winning drives          |

### 6.3 Trait Upgrade Thresholds

| Current              | Upgrade To | Performance Required             |
| -------------------- | ---------- | -------------------------------- |
| Normal → Star        | Star       | Top 15 at position in stats      |
| Star → Superstar     | Superstar  | Top 5 at position OR major award |
| Superstar → X-Factor | X-Factor   | MVP/OPOY/DPOY only               |

---

## 7. Coaching Influence

### 7.1 Position Coach Impact

| Coach Rating | XP Modifier   | Trait Unlock Bonus              |
| ------------ | ------------- | ------------------------------- |
| 40-59        | -10%          | None                            |
| 60-74        | 0% (baseline) | None                            |
| 75-84        | +10%          | Small milestone reduction       |
| 85-94        | +20%          | Medium milestone reduction      |
| 95-99        | +30%          | Large + unique traits available |

### 7.2 Coaching Philosophies

| Philosophy             | Effect                                     |
| ---------------------- | ------------------------------------------ |
| **Player Development** | +25% XP gain, faster trait reveals         |
| **Veteran Focused**    | Slower regression for 30+ players          |
| **Youth Movement**     | +50% rookie XP, hidden dev revealed faster |
| **Scheme Mastery**     | +40% scheme fit bonus                      |

---

## 8. Training System Integration

### 8.1 Seasonal Periodization

| Phase          | Duration | Focus          | XP Rate |
| -------------- | -------- | -------------- | ------- |
| Offseason      | 8 weeks  | Heavy training | 150%    |
| Preseason      | 4 weeks  | Conditioning   | 100%    |
| Regular Season | 18 weeks | Maintenance    | 75%     |
| Playoffs       | 4 weeks  | Recovery focus | 50%     |

### 8.2 Training Drill Effects

| Drill Type       | Target       | XP Mult | Injury Risk |
| ---------------- | ------------ | ------- | ----------- |
| Film Study       | Mental       | 0.8x    | 0%          |
| Light Practice   | General      | 1.0x    | 2%          |
| Position Drills  | Primary stat | 1.3x    | 4%          |
| Intense Training | Physical     | 1.5x    | 8%          |
| Game Simulation  | All          | 1.6x    | 12%         |

---

## 9. User Interface Requirements

### 9.1 Visibility Levels

| Stage     | Visible                 | Hidden                           |
| --------- | ----------------------- | -------------------------------- |
| Pre-Draft | Scout estimate, combine | True potential, dev speed        |
| Year 1    | Performance stats       | True potential (until 500 snaps) |
| Year 2+   | All core ratings        | Long-term durability             |

### 9.2 Progress Indicators

```
Player Card Display:
┌─────────────────────────────────┐
│ John Smith - QB                 │
│ OVR: 78 → 81 (+3 this season)   │
│ Dev: ⭐⭐⭐ (Superstar)           │
│ Age: 24 (↑ Prime in 2 years)    │
│ XP: ████████░░ 847/1,200        │
│ Potential: 88-94 (Scouted)      │
└─────────────────────────────────┘
```

---

## 10. Validation Metrics

Over 10 simulated seasons, verify:

| Metric                   | Target      | Tolerance |
| ------------------------ | ----------- | --------- |
| Rookie OVR gain (Year 1) | +3 to +5    | ±2        |
| Prime player OVR change  | -1 to +2    | ±1        |
| Post-prime decline/year  | -2 to -4    | ±1        |
| X-Factor % in league     | 3-5%        | ±1%       |
| Bust rate (draft)        | 20-30%      | ±5%       |
| Star emergence/year      | 2-4 players | ±1        |

---

## Changelog

| Date       | Change                                              |
| ---------- | --------------------------------------------------- |
| 2025-12-12 | Initial creation with community-validated mechanics |

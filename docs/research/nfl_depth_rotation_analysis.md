# NFL Depth & Rotation Research Summary

**Research Date:** December 4, 2024
**Purpose:** Analyze real NFL usage patterns for multiple skilled players at same position

---

## Executive Summary

Modern NFL offenses and defenses have evolved far beyond simple "starter/backup" depth charts. The research reveals that **7 primary positions** are significantly impacted by multi-player rotation systems, with some positions (like defensive line) using 8+ player rotations as standard practice.

### Key Finding: The Nickel Defense is the "New Base"

The most dramatic shift: **Nickel defense (5 DBs) is now used ~67% of snaps**, compared to traditional base defense (4 DBs) at only ~33%. This fundamentally changes linebacker usage patterns.

---

## Position-by-Position Analysis

### 🏃 1. Running Back - Most Affected by RBBC

**Finding:** ~70% of NFL teams use a Running Back By Committee (RBBC) approach

**Snap Distribution Pattern:**

- **Lead Back:** 55-65% of snaps
- **Secondary Back:** 30-40% of snaps
- **3rd Back (if any):** 5-15% of snaps

**Role Differentiation:**

- **Early Down Back:** Power runner, between the tackles (50-60% rush snaps)
- **Third Down Back:** Pass-catching specialist, pass protection (40-50% pass snaps)
- **Change of Pace:** Speed back for fresh legs (15-25% rush snaps)
- **Goal Line:** Power back inside the 5-yard line (50-70% of goal line snaps)

**Real Examples (2024):**

- Detroit Lions: Jahmyr Gibbs / David Montgomery (both 10+ TDs)
- Atlanta Falcons: Bijan Robinson / Tyler Allgeier
- Miami Dolphins: Raheem Mostert / De'Von Achane / Jaylen Wright (fearsome trio)

**Simulation Impact:**

- Must model different RB skills (power vs. speed vs. receiving)
- Snap distribution based on down/distance/field position
- Fatigue management after 3-4 consecutive carries

---

### 🎯 2. Wide Receiver - Personnel Package Revolution

**Finding:** 11 Personnel (3 WR sets) used on **60-70% of offensive snaps**

**The Modern WR Room:**

- **Top 3 WRs:** All play 85-95% of snaps (when healthy)
- **WR4:** Enters in 4-WR sets or to spell tired players (20-30% snaps)
- **WR5:** Mostly special teams, garbage time (5-10% snaps)

**Role Specialization:**

- **X Receiver:** Outside, deep threat, beats press coverage
- **Z Receiver:** Outside, versatile route runner
- **Slot Receiver:** Inside, quick routes, finds zone seams

**Personnel Package Distribution:**

```
11 Personnel (3 WR): 65% of snaps
12 Personnel (2 WR): 20% of snaps
10 Personnel (4 WR): 10% of snaps
00 Personnel (5 WR): 2% of snaps
13/21 Personnel (1-0 WR): 3% of snaps
```

**Real Examples (2024):**

- Houston Texans: Stefon Diggs / Nico Collins / Tank Dell (crowded but productive)
- Chicago Bears: DJ Moore / Keenan Allen / Rome Odunze (rookie Odunze already major contributor)
- Miami Dolphins: Tyreek Hill / Jaylen Waddle / OBJ

**Simulation Impact:**

- 3 WRs should all see significant playing time
- Different WR types (speed vs. possession vs. slot specialist)
- Matchup-based deployment (slot WR vs. weak LBs in coverage)

---

### 🛡️ 3. Defensive Line - Heaviest Rotation in NFL

**Finding:** Standard DL rotation is **6-8 players**, with **no individual exceeding 65% snaps**

**Why Heavy Rotation?**

- Defensive linemen fatigue **3-4x faster** than offensive linemen
- Must react to offense (vs. knowing the play call)
- Constant physical battle with 300+ lb blockers
- Fresh legs critical for pass rush effectiveness

**Rotation Pattern:**

- **Starter DEs/DTs:** 50-60% of snaps
- **Rotational Rushers:** 35-45% of snaps
- **Situational Rushers:** 20-30% of snaps

**Scheme-Specific:**

- **Jim Schwartz (Browns 2024):** Used **8-man DL rotation** explicitly
- Most teams aim for 6-8 capable DL to maintain freshness

**Simulation Impact:**

- Aggressive fatigue accumulation for DL
- Automatic rotation every 5-8 snaps
- Performance penalty after 65% snap share
- Fresh legs bonus on 3rd downs

---

### ⚡ 4. Edge Rusher - Snap Count Ceiling

**Finding:** Elite edge rushers target **50-65% max snap count** to stay effective

**The Fatigue Problem:**

- Edge rushing is explosive, high-effort every snap
- Performance drops significantly above 70% snap count
- Risk of injury increases with overuse

**Target Distribution:**

- **Elite Starter EDGE:** 55-60% of snaps
- **Secondary EDGE:** 45-50% of snaps
- **Rotational EDGE:** 30-40% of snaps
- **Pure Pass Rush Specialist:** 20-25% of snaps (3rd downs only)

**Critical Thresholds:**

```
< 55% snaps: Optimal freshness zone
55-65% snaps: Standard starter workload
65-70% snaps: Fatigue begins impacting performance
> 70% snaps: Significant performance drop + injury risk
```

**Simulation Impact:**

- Hard cap at 70% snap share for EDGE
- Force rotation after 8 consecutive snaps
- Elite pass rushers prioritized for 3rd downs
- Fresh legs = better pass rush win rate

---

### 🎯 5. Cornerback - The Nickel Revolution

**Finding:** Nickel defense (5 DBs) now used on **67% of defensive snaps**

**Package Distribution:**

```
Nickel Defense (5 DBs): 60-67% of snaps
Base Defense (4 DBs): 30-33% of snaps
Dime Defense (6 DBs): 5-10% of snaps
```

**What This Means:**

- The **Nickel CB (3rd CB)** is essentially a starter
- Many teams use a Safety in the nickel role ("big nickel")
- CB depth is critical - need 3+ quality corners

**Role Specialization:**

- **CB1/CB2 (Outside):** Man coverage, press at line, shadow top WRs (90-95% snaps)
- **Nickel CB (Slot):** Zone coverage, tackling, cover slot WRs (65-70% snaps)
- **Dime CB (6th DB):** Often a safety, coverage specialist (5-10% snaps)

**Simulation Impact:**

- CB3 should play 60-70% of snaps
- Different skills: Outside CBs need press coverage, Slot CBs need tackling
- Personnel package based on opponent WR count

---

### 💪 6. Linebacker - The Disappearing Position

**Finding:** Base defense only **33% of snaps** means LBs play far less than before

**The New Reality:**

```
Base Defense (3 LBs): 33% of snaps
Nickel Defense (2 LBs): 60% of snaps - SAM comes out
Dime Defense (1 LB): 7% of snaps - Only MIKE remains
```

**What This Means:**

- **Mike LB:** Must be elite in coverage to stay on field (85-90% snaps)
- **Will LB:** Fast, coverage-oriented (70-75% snaps)
- **Sam LB:** Often removed for nickel DB (40-45% snaps)

**Hybrid "Nickel LB" Role:**

- Modern NFL features LB/S hybrids
- Size of LB, speed of S
- Can cover slot WRs and still tackle

**Simulation Impact:**

- Don't assume 3 LBs will all play equal snaps
- Mike must have coverage skills or sit in nickel
- Sam LB is essentially a rotational player now

---

### 🏈 7. Tight End - Y vs F Tight End

**Finding:** Teams with 2 quality TEs use **12 Personnel ~20-25% of snaps**

**Role Differentiation:**

**Y Tight End (Receiving TE):**

- Primary pass catcher
- Lines up on the line
- Plays 80-90% of snaps
- Skills: Route running, hands, release

**F Tight End (Blocking TE / H-Back):**

- Primary blocker
- Lines up varied (backfield, wing, etc.)
- Plays 40-50% of snaps
- Skills: Run blocking, pass blocking, power

**Personnel Package Usage:**

```
11 Personnel (1 TE): Y TE plays ~90% of these snaps
12 Personnel (2 TE): Both Y and F play ~95% of these snaps
13 Personnel (3 TE): Rare, but both Y/F plus 3rd TE
```

**Simulation Impact:**

- Y TE is essentially a WR in terms of snap count
- F TE is situational (run-heavy, goal line, max protect)
- 2-TE sets should be based on team offensive scheme

---

## Cross-Position Insights

### Fatigue Rates by Position Group

**Fastest Fatigue (Need Heavy Rotation):**

1. Defensive Line (3.5/10 fatigue rate)
2. Edge Rusher (3.0/10)
3. Running Back (2.5/10)

**Moderate Fatigue:** 4. Tight End (2.2/10) 5. Linebacker (2.0/10) 6. Cornerback (1.8/10)

**Slowest Fatigue (Can Play 90%+ Snaps):** 7. Wide Receiver (1.5/10) 8. Safety (1.5/10) 9. Offensive Line (1.0/10) 10. Quarterback (0.5/10)

### Snap Count Expectations by Position

| Position | Starter Range | Rotational Range | Backup Range |
| -------- | ------------- | ---------------- | ------------ |
| QB       | 98-100%       | N/A              | 0-2%         |
| OL       | 95-100%       | 40-60%           | 0-5%         |
| WR       | 85-95%        | 60-75%           | 20-35%       |
| TE       | 80-90%        | 40-55%           | 10-20%       |
| RB       | 55-65%        | 30-45%           | 5-15%        |
| DL       | 50-60%        | 35-45%           | 20-30%       |
| EDGE     | 55-65%        | 40-50%           | 25-35%       |
| LB       | 85-90% (Mike) | 40-50% (Sam)     | 10-20%       |
| CB       | 90-95%        | 65-75% (Nickel)  | 5-15%        |
| S        | 90-95%        | 70-80%           | 5-10%        |

---

## Implementation Priorities

### Phase 1: High Impact Positions

1. **Running Back RBBC System** - Most visible to users
2. **Defensive Line Rotation** - Biggest gameplay impact
3. **Nickel Defense Package** - Reflects modern NFL

### Phase 2: Medium Impact

4. **Edge Rusher Management** - Prevents unrealistic snap counts
5. **Cornerback Packages** - Adds depth to secondary
6. **WR Personnel Sets** - 11/10/12 personnel variation

### Phase 3: Advanced Features

7. **Linebacker Sub Packages** - Realistic modern usage
8. **Tight End Y/F Roles** - Adds strategic depth
9. **Matchup-Based Adjustments** - Coordinator AI

---

## Real NFL Examples to Model

### RBBC Done Right

- **Detroit Lions:** Gibbs (speed/receiving) & Montgomery (power) both elite
- **Pittsburgh Steelers:** Harris & Warren effective committee

### DL Rotation Excellence

- **Cleveland Browns:** 8-man rotation under Jim Schwartz
- **San Francisco 49ers:** Deep DL room, constant fresh legs

### Nickel Defense as Base

- **Baltimore Ravens:** Use dime more due to secondary depth
- Most teams: 60-67% nickel usage standard

### WR Room Depth

- **Houston Texans:** 3 WRs all highly productive despite shared targets
- **Chicago Bears:** Rookie Odunze immediately integrated into 3-WR sets

---

## Key Takeaways for Simulation

1. **Rotation ≠ Lack of Talent:** Multiple skilled players at a position is now the norm, not the exception

2. **Position-Specific Logic Required:** Can't use same rotation logic for RB (heavy rotation) and WR (minimal rotation)

3. **Personnel Packages Matter:** Modern NFL is about 11 personnel, nickel, and dime - not traditional base offense/defense

4. **Fatigue is Everything:** For DL/EDGE, rotation is mandatory for performance maintenance

5. **Morale Considerations:** 85 OVR player getting 35% snaps will be unhappy unless it's a position that naturally rotates heavily

6. **Coaching Schemes:** Different coordinators have different rotation philosophies (Andy Reid vs. Kyle Shanahan)

7. **Matchup Exploitation:** Smart teams adjust package frequency based on opponent weaknesses

---

**END OF RESEARCH SUMMARY**

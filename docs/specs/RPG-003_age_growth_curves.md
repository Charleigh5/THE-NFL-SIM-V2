# RPG-003: Age-Based Growth & Regression Curves

**Objective**: Simulate realistic NFL career arcs where players evolve based on position-specific aging curves. Front-load XP for young players, stabilize in prime, and apply regression penalties in decline phase.

## 1. Aging Curve Archetypes

We define 4 primary curve shapes based on PFF research:

### A. The "Running Back" Curve (Early Peak, Sharp Decline)

- **Positions**: RB, CB, WR (Speed)
- **Ascension**: Ages 21-24 (Rapid Growth)
- **Prime**: Ages 25-27
- **Decline**: Age 28+ (Sharp Regression, especially physicals)

### B. The "Skill" Curve (Standard)

- **Positions**: WR (Route/Possession), LB, S, TE
- **Ascension**: Ages 21-25
- **Prime**: Ages 26-29
- **Decline**: Age 30+ (Moderate Regression)

### C. The "Trench" Curve (Late Peak, Slow Decline)

- **Positions**: OL, DL
- **Ascension**: Ages 21-26 (Slower Mastery)
- **Prime**: Ages 27-31
- **Decline**: Age 32+ (Gradual Regression)

### D. The "Quarterback" Curve (Longevity)

- **Positions**: QB, K, P
- **Ascension**: Ages 21-26
- **Prime**: Ages 27-33
- **Decline**: Age 35+ (Slowest Regression)

---

## 2. Mechanics

### XP Multiplier (Growth)

Applied to `ProgressionService` when awarding XP.

| Age Phase       | Age Range       | Multiplier | Notes                    |
| :-------------- | :-------------- | :--------- | :----------------------- |
| **Rookie/Soph** | 21-22           | **1.5x**   | "Rookie Bump"            |
| **Ascension**   | 23-25           | **1.2x**   | Developing               |
| **Prime**       | (Pos Dependent) | **1.0x**   | Baseline                 |
| **Veteran**     | Post-Prime      | **0.5x**   | Hard to learn new tricks |

### Regression Logic

Applied during `OffseasonService`.

**Regression Severity Formula**:
`Regression Score = (Current Age - Decline Start Age) * Severity Factor`

**Attribute decay priority:**

1. **Physicals** (Speed, Agility, Acceleration) - Decay FIRST and FASTEST.
2. **Skills** (Throw Power, Catching, Tackling) - Decay MODERATELY.
3. **Mental** (Awareness, Play Rec) - Decay SLOWEST (or even grow).

---

## 3. Implementation Plan

### Phase A: `GrowthCurveEngine` (`app/services/training/growth_curves.py`)

- Define `POSITION_CURVES` dictionary mapping positions to curve types.
- Implement `get_xp_multiplier(age, position)`
- Implement `get_regression_factors(age, position)`

### Phase B: Integrate with `ProgressionService`

- In `apply_xp`: `xp_to_add = raw_xp * GrowthCurveEngine.get_xp_multiplier(...)`

### Phase C: Integrate with `OffseasonService`

- In `process_regression`:
  - Fetch `regression_factors`.
  - Apply decay to attributes based on type.

## 4. Verification

- **Test A**: RB at age 29 should gain virtually no Speed XP and lose ~2-3 points of Speed in offseason.
- **Test B**: QB at age 32 should still be stable.
- **Test C**: Rookie (21) should gain XP 50% faster than vet.

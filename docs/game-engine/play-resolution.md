# Play Resolution Specification

**Source:** `backend/app/orchestrator/play_resolver.py`
**Status:** Reverse-Engineered / Current Implementation

## 1. Overview

The `PlayResolver` is the core engine component responsible for simulating the outcome of a single football play. It takes a `PlayCommand` (Run or Pass) and the current `MatchContext` as input, and returns a `PlayResult`.

It orchestrates interactions between several sub-systems:

- **Genesis Kernel**: Fatigue and Injury calculations.
- **Blocking Engine**: OL vs DL interaction resolution.
- **Attribute Interaction Engine**: Complex cross-attribute modifiers.
- **Probability Engine**: Final statistical determination of success/failure and yardage.
- **Weather Service**: Environmental impact application.

## 2. Pass Play Resolution

### 2.1 Process Flow

1.  **Identify Key Players**: QB, Targeted Receiver (WR/TE), Primary Defender (CB/S).
2.  **Genesis Check**: Calculate current fatigue for QB (affects accuracy) and checking for potential injury events.
3.  **Line Battle & Sack Logic**:
    - Simulates 1-on-1 matchups (LT vs RE, etc.) using `BlockingEngine`.
    - **Pancake**: Immediate Sack.
    - **Loss (Pressure)**: Calculates `Sack Probability` based on pressure level and QB attributes.
    - **Outcome**: Sack, Pressure Avoided, or Clean Pocket.
4.  **Attribute Interactions**:
    - Applies `WR Release vs CB Press` (Line of Scrimmage).
    - Applies `Route Running vs Man Coverage` (Post-Snap).
    - Applies `Ball Tracking vs Throw Placement` (Catch Point).
5.  **Probability Calculation**:
    - **Base Probability**: Derived from QB's specific accuracy rating (Short/Mid/Deep) configured by `command.depth`.
    - **Modifiers**:
      - Speed Differential (Target Speed vs Defender Speed).
      - Matchup Skill (Route Running vs Man Coverage).
      - Weather Penalty (Rain/Snow/Wind).
      - Fatigue Penalty (10% max at 100 fatigue).
      - Pressure Penalty (-25% for Heavy Pressure, -10% for Mild).
      - Trait Bonuses (e.g., "Possession Receiver" in contested catches).
    - **Final Success Chance**: Calculated by `ProbabilityEngine`.
6.  **Outcome Resolution**:
    - **Completion**: Yards calculated based on depth (Short ~5yds, Mid ~12yds, Deep ~25yds) + Variance + YAC (Speed Diff Bonus).
    - **Touchdown**: Automatic if yards > 80, or 10% chance if yards > 20.
    - **Incomplete**: 0 yards.

### 2.2 Key Formulas

**Accuracy Base:**

```python
base_prob = (accuracy_rating / 100.0) * weather_accuracy_mod
```

**Success Chance:**

```python
success_chance = base_prob + attribute_modifiers - context_modifiers - fatigue_penalty
```

## 3. Run Play Resolution

### 3.1 Process Flow

1.  **Identify Key Players**: Ball Carrier (RB), Primary Defender (DT for middle, DE/LB for outside).
2.  **Fatigue Check**: Impact on fumble chance and total yardage.
3.  **Attribute Logic**:
    - **Power Run**: Compares `RB Strength` vs `Defender Tackle`.
    - **Outside Run**: Compares `RB Speed` vs `Defender Speed`.
4.  **Yardage Calculation**:
    - Uses a Normal Distribution via `ProbabilityEngine`.
    - **Mean**: Base Value (3.5 middle / 2.5 outside) + Attribute Diff Bonus - Fatigue Penalty.
    - **Std Dev**: Higher variance for outside runs (3.0 vs 1.5).
5.  **Breakaway System**:
    - Check for "Breakaway" outcome (20% threshold).
    - **Critical Success**: Big bonus yards (Mean 25).
6.  **Fumble Logic**:
    - Base chance: 1%.
    - Modifiers: Fatigue (>70), Big Hit (Hit Power > 85), Low Ball Security, Weather (Rain/Cold).

### 3.2 Key Formulas

**Base Yards (Middle):**

```python
base_yards = 3.5 + (strength_diff * 10.0)
```

**Base Yards (Outside):**

```python
base_yards = 2.5 + (speed_diff * 20.0)
```

## 4. Environmental Effects

Integration with `WeatherService`.

- **Rain**: -15% Passing Accuracy, +10% Fumble Chance.
- **Snow**: -25% Passing Accuracy, +5% Rushing Effectiveness (TBD).
- **Wind**: -20% Passing Accuracy (>15mph), -10% FG Accuracy.
- **Cold**: +15% Fumble Chance (<20F).

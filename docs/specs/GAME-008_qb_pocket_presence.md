# GAME-008: QB Pocket Presence Specification

**Feature ID:** GAME-008
**Status:** 🟢 SPEC_COMPLETE
**Priority:** P1
**Last Updated:** 2025-12-20

---

## 1. Overview

The QB Pocket Presence system models how quarterbacks handle pass rush pressure, affecting sack outcomes, throwaway decisions, and scramble escapes.

## 2. NFL Statistical Baselines

| Metric                    | NFL Average     | Source                   |
| :------------------------ | :-------------- | :----------------------- |
| Sack Rate (per pass play) | **6.5%**        | Historical avg 2020-2024 |
| Pressure Rate             | **25-30%**      | Next Gen Stats           |
| Sacks per Pressure        | **~22%**        | Derived (6.5% / 28%)     |
| Time to Throw             | **2.6 seconds** | Next Gen Stats           |
| Elite QB Sack Rate        | **4.5-5.0%**    | Top 5 QBs                |
| Poor QB Sack Rate         | **8.5-10%**     | Bottom 5 QBs             |

### QB Tiers by Pocket Presence

| Tier              | Example QBs        | Pocket Awareness | Sack Rate |
| :---------------- | :----------------- | :--------------- | :-------- |
| Elite (90+)       | Mahomes, Burrow    | 90-99            | 4.5%      |
| Good (75-89)      | Stafford, Prescott | 75-89            | 5.5%      |
| Average (60-74)   | Goff, Cousins      | 60-74            | 6.5%      |
| Below Avg (45-59) | Young QBs          | 45-59            | 7.5%      |
| Poor (<45)        | Rookies, Backups   | 30-44            | 9.0%      |

---

## 3. Implementation Formula

### Current Implementation (`sack_calculator.py`)

```python
BASE_SACK_PROBABILITY = 0.07  # 7% base - CALIBRATED

# Presence Factor: 0.0 to 0.5 reduction
presence_factor = pocket_presence * 0.005  # 50 rating = 25% reduction

# Chemistry Factor: 0.0 to 0.1 reduction
chemistry_factor = ol_chemistry_bonus * 0.02  # 5 pts = 10% reduction

# Escape Factor: Up to 30% reduction for elite mobility
mobility_score = (speed + accel + agility) / 300.0
escape_factor = mobility_score * 0.3

# Final calculation
initial_prob = BASE * (1 + pressure_level)
final_prob = initial_prob * (1 - presence) * (1 - chemistry) * (1 - escape)
```

### Recommended Calibration Updates

| Parameter               | Current | Recommended | Rationale                   |
| :---------------------- | :------ | :---------- | :-------------------------- |
| `BASE_SACK_PROBABILITY` | 0.07    | **0.065**   | Align with 6.5% NFL avg     |
| `presence_factor` max   | 0.495   | **0.45**    | 90+ rating = ~45% reduction |
| `escape_factor` max     | 0.30    | **0.25**    | Cap scramble benefit        |

---

## 4. Attribute Interactions

### Primary Attributes

| Attribute         | Impact                   | Source       |
| :---------------- | :----------------------- | :----------- |
| `pocket_presence` | Reduces sack probability | Player model |
| `awareness`       | Affects pre-snap read    | Player model |
| `throw_on_run`    | Scramble completion rate | Player model |

### Secondary Factors

| Factor             | Effect            | Multiplier    |
| :----------------- | :---------------- | :------------ |
| OL Chemistry (0-5) | Reduces sack rate | -2% per point |
| Blitz Pickup Trait | Blocks blitzer    | -5% on blitz  |
| QB Quick Release   | Reduces TtT       | -0.1s avg     |

---

## 5. Outcome Resolution

When pressure is detected:

```python
Roll < sack_prob → SACK (-7 yards avg)
Roll < sack_prob + 0.15 → THROW_AWAY (incomplete, no INT risk)
Roll < sack_prob + 0.30 → SCRAMBLE (gain yards if mobile)
Else → PASS_COMPLETED (normal resolution)
```

---

## 6. Verification

### Unit Tests Required

- [ ] Verify elite QB (Mahomes) sack rate ~4.5-5%
- [ ] Verify average QB sack rate ~6.5%
- [ ] Verify poor QB sack rate ~9%
- [ ] Verify OL chemistry reduces rate correctly

### Statistical Validation

Run 10,000 simulated pass plays per QB tier and validate:

- Mean sack rate within ±0.5% of target
- Pressure-to-sack conversion ~22%

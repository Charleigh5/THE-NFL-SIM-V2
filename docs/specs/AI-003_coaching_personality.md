# AI-003: Coaching AI Personality Specification

**Feature ID:** AI-003
**Status:** 🟢 SPEC_COMPLETE
**Priority:** P1
**Last Updated:** 2025-12-20

---

## 1. Overview

The Coaching AI Personality system defines unique behavioral archetypes for head coaches, moving beyond simple "Aggressive/Conservative" sliders. It models decision-making tendencies for 4th downs, play-calling ratios, and adaptivity to game states (leading vs. trailing).

## 2. Coaching Archetypes

We define 7 distinct "Personas" derived from NFL analytics clusters.

| ID             | Persona                | Description                                                     | Real-Life Analog  | 4th Down Aggression | Pass/Run Bias |
| :------------- | :--------------------- | :-------------------------------------------------------------- | :---------------- | :------------------ | :------------ |
| **CEO**        | **The CEO**            | Leader, culture-first, delegates, balanced conservative.        | Tomlin, Carroll   | Low-Med             | Balanced      |
| **GURU_OFF**   | **Offensive Guru**     | Scheme-heavy, efficient, aggressive in plus territory.          | Shanahan, McVay   | High                | Pass Lean     |
| **GURU_DEF**   | **Defensive Schemer**  | Field position focus, conservative offense, plays for turnover. | Fangio, Belichick | Low                 | Run Lean      |
| **ANALYTICS**  | **Analytics Disciple** | Strict adherence to EPA models, aggressive on 4th down.         | Sirianni, Staley  | Very High           | Efficiency    |
| **OLD_SCHOOL** | **Old School**         | Establish the run, punt for field position, risk averse.        | Rivera, Fox       | Very Low            | Run Heavy     |
| **RIVERBOAT**  | **The Gambler**        | High variance, "gut feeling" risks, emotional momentum.         | Campbell, Arians  | High (Random)       | Deep Pass     |
| **ROOKIE**     | **The Clipboard**      | Basic, predictable, low adaptation, safe choices.               | New Hires         | Average             | Balanced      |

---

## 3. Decision Matrices

### 3.1 Fourth Down Logic (Go For It %)

| Situation               | Analytics/Gambler | Off Guru | CEO/Defensive | Old School |
| :---------------------- | :---------------- | :------- | :------------ | :--------- |
| **4th & 1 (Own 40-50)** | 95%               | 80%      | 50%           | 20%        |
| **4th & 2 (Opp 35-45)** | 85%               | 65%      | 30%           | 10%        |
| **4th & Goal (from 2)** | 90%               | 75%      | 40%           | 15%        |
| **Trailing late (Any)** | 100%              | 100%     | 100%          | 100%       |

### 3.2 Adaptive Logic (Game Script)

- **Old School / Defensive**: If leading by 7+ in 2nd half -> Run Rate increases by +20%.
- **Offensive Guru / Analytics**: "Gas Pedal". If leading -> Keep passing to maintain efficiency (Run Rate only +5%).
- **CEO**: "Protect the Lead". If leading -> Defense becomes "Bend Don't Break" (Prevent).

---

## 4. Implementation Details

### `PersonalityProfile` Class Updates

Each archetype maps to specific float modifiers:

```python
@dataclass
class PersonalityProfile:
    name: str
    pass_heavy_ratio: float      # >0.5 = Pass heavy
    fourth_down_aggression: float # 0.0 - 1.0 (Multiplier for Go probability)
    adaptive_score: float        # 0.0 - 1.0 (How fast they change plans)
    run_clock_urgency: float     # When to start chewing clock (0=never, 1=early 3rd)
```

### Integration in `CoachingAIService`

```python
def should_go_for_it(situation):
    base_prob = analytics_model.get_win_probability_added()

    # Personality Modifier
    if base_prob > 0.0 and base_prob < 0.15:  # Marginal decision
        if philosophy.aggression > 0.8: # Analytics/Gambler
            return True
        elif philosophy.aggression < 0.4: # Old School
            return False

    return base_prob > threshold
```

---

## 5. Verification Plan

1. **Test: The "Staley Scenario"**: Verify `ANALYTICS` coach goes for it on 4th & 1 from own 25 more than 60% of the time, while `OLD_SCHOOL` punts 99%.
2. **Test: Lead Protection**: Verify `OLD_SCHOOL` coaches run the ball >70% of the time when up by 10 in the 3rd quarter.

# AI-004: 4th Down Decision AI

**Feature ID:** AI-004
**Status:** SPEC_COMPLETE
**Implementation Status:** MANUAL / BASIC (Currently implicit in Playbook selection)

## 1. Overview

This specification monitors the logic for the "Head Coach" AI when facing critical 4th down situations. It parses game state (Score, Time remaining, Field Position, Momentum) to decide between three actions: **Punt**, **Field Goal**, or **Go For It**.

## 2. Current Implementation

The current logic resides partly in `services/playbook/play_caller.py` but is essentially **Playbook Driven** rather than **Decision Driven**.

- The `PlayCallerAI` requests plays for `Down=4`.
- The Playbook returns a list of plays valid for that situation.
  - If 4th & Long in own territory -> Playbook returns Punt.
  - If 4th & Short in Red Zone -> Playbook might return FG or Run.
- **Deficiency:** The AI does not explicitly weigh probabilities (Win Probability Added). It relies on static playbook assignments.

## 3. Specification: Situational Decision Engine

The new logic will intercept the play call process _before_ querying the playbook.

### 3.1 The Decision Matrix

The AI evaluates a `GoStrength` score (0-100) based on:

1. **Field Position:**
   - Own 0-40: Strong Punt bias.
   - 40-Opp 40: "No Man's Land" (Go or Punt).
   - Opp 40-Opp 10: FG Range (FG bias).
   - Opp 10-Goal: FG or Go (depending on score).
2. **Distance to First Down:**
   - < 1 yard: High Go bias (+40).
   - > 5 yards: High Punt/FG bias.
3. **Score Differential:**
   - Trailing by > 8 late: Must Go.
   - Trailing by < 3 late: FG priority.
4. **Coach Aggression:**
   - `Aggressive`: +15 to Go score.
   - `Conservative`: -15 to Go score.

### 3.2 Decision Logic Pseudo-Code

```python
def make_4th_down_decision(situation, coach_traits):
    # 1. Mandatory Kicks
    if score_diff < -3 and time_remaining < 30s and in_fg_range:
        return ACTION_FIELD_GOAL

    # 2. Desperation Mode
    if score_diff < -8 and time_remaining < 180s:
        return ACTION_GO_FOR_IT

    # 3. Standard Logic (NYT Bot Style)
    go_prob = calculate_win_prob_if_go(situation)
    kick_prob = calculate_win_prob_if_kick(situation)
    punt_prob = calculate_win_prob_if_punt(situation)

    actions = [
        ("GO", go_prob),
        ("FG", kick_prob),
        ("PUNT", punt_prob)
    ]

    best_action = max(actions, key=lambda x: x[1])

    # Apply Coach Personality Variance
    # ...

    return best_action
```

## 4. Implementation Plan

1. Create `CoachingDecisionService` in `backend/app/services/playbook/`.
2. Implement `should_go_for_it(situation)` method using the matrix above.
3. Update `PlayCallerAI.call_play`:
   - Check `if down == 4`.
   - Call `should_go_for_it`.
   - If `GO`: Filter playbook for Run/Pass.
   - If `PUNT`: Filter playbook for Special Teams > Punt.
   - If `FG`: Filter playbook for Special Teams > Field Goal.

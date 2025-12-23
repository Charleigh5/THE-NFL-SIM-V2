# RPG-003: Age-Based Growth & Regression Curves

**Status:** Implemented
**Owner:** RPG Mechanics Team
**Last Updated:** 2025-12-22

## 1. Overview

This feature simulates the biological and career lifecycle of NFL players. It replaces linear progression with position-specific "Aging Curves," ensuring that Running Backs decline early (the "RB Cliff"), Quarterbacks can play into their late 30s, and physical attributes decay faster than mental skills.

## 2. Core Mechanics

### 2.1 Growth Curve Archetypes

We define four distinct aging archetypes based on PFF data:

| Archetype     | Positions     | Prime Window | Decline Start | Description                                     |
| :------------ | :------------ | :----------- | :------------ | :---------------------------------------------- |
| **RB_SPEED**  | RB, CB        | 23-26        | 27            | Relies on athleticism. Hard wall at 28.         |
| **SKILL_POS** | WR, TE, LB, S | 25-29        | 30            | Balanced physical/technical. Moderate decline.  |
| **TRENCHES**  | OL, DL        | 26-30        | 31            | Strength profiles peak later and last longer.   |
| **QB_KICKER** | QB, K, P      | 27-33        | 35            | Relies on mental processing. Very slow decline. |

### 2.2 XP Acquisition Efficiency (Neuroplasticity)

Players earn XP at different rates depending on their age phase:

| Phase          | Age Range  | XP Multiplier             |
| :------------- | :--------- | :------------------------ |
| **Rookie/Dev** | < 22       | **1.5x** (Rapid Growth)   |
| **Pre-Prime**  | 23-24      | **1.2x**                  |
| **Prime**      | (Variable) | **1.0x**                  |
| **Post-Prime** | (Variable) | **0.8x**                  |
| **Decline**    | (Variable) | **0.5x** (Stalled Growth) |

### 2.3 Regression Physics

Regression is **probabilistic** and **attribute-specific**.

#### The Regression Score (0-100)

Calculated annually: `Score = (Current Age - Decline Age) * Severity Factor`

- **RB Severity**: 12 (Very High)
- **Skill Severity**: 6 (Medium)
- **Trenches Severity**: 4 (Low)
- **QB Severity**: 3 (Very Low)

#### Attribute Decay Tiers

1.  **Physicals (Speed, Agility, Jump)**:
    - _Vulnerability_: High (Score / 100 chance to lose point).
    - _Impact_: Can lose 1-3 points per year in deep decline.
2.  **Skills (Catch, Block, Throw Power)**:
    - _Vulnerability_: Moderate (Score / 200 chance).
    - _Impact_: Typically lose 0-1 point.
3.  **Mentals (Awareness, Play Rec)**:
    - _Vulnerability_: None. Players do not get "dumber" with age.

## 3. Implementation Details

- **Engine**: `app.services.training.growth_curves.GrowthCurveEngine`
- **Logic**: `app.services.training.progression.ProgressionEngine`
- **Verification**: `backend/tests/unit/test_growth_curves.py`

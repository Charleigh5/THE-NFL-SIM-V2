# GAME-010: Venue-Specific Effects & Home Field Advantage

**Status:** Implemented
**Owner:** Core Simulation Team
**Last Updated:** 2025-12-22

## 1. Overview

The "Venue Effects" system models the impact of stadium atmosphere, crowd noise, and environmental factors on gameplay. The goal is to replicate the tangible "Home Field Advantage" (HFA) seen in the NFL, where home teams win ~57% of games and loud stadiums significantly disrupt opposing offensives.

## 2. Core Mechanics

### 2.1 noise_level Calculation

Crowd noise is dynamic, calculated on every play based on:
`Total Noise = Base Rating + Attendance Mod + Situation Mod + Energy Mod + Dome Bonus`

| Component           | Range   | Description                                              |
| :------------------ | :------ | :------------------------------------------------------- |
| **Base Rating**     | 60-100  | Intrinsic loudness of the stadium design.                |
| **Attendance Mod**  | 0-20    | Percentage of seats filled (e.g., 95% = +19).            |
| **Situation Mod**   | 0-25    | "CRITICAL" (3rd Down/Redzone = +15) or "BIG_PLAY" (+25). |
| **Energy Mod**      | 0-10    | Momentum of the crowd (0.0 - 1.0 scale).                 |
| **Dome/Loud Bonus** | 0 or 10 | +10 for Domes or "Known Loud" open-air stadiums.         |

**Noise Tiers:**

- **QUIET (< 70)**: No impact.
- **MODERATE (70-84)**: Minor impact.
- **LOUD (85-94)**: Significant communication issues.
- **DEAFENING (95+)**: Severe disruption (False Start risk).

### 2.2 Crowd Energy

Crowd energy fluctuates based on game events:

- **Touchdown (Home)**: +0.25
- **Turnover (Home Defense)**: +0.20
- **Touchdown (Away)**: -0.15
- **Silence**: Gradual decay if home team performs poorly.

### 2.3 Altitude Physics

Stadiums at high elevation (e.g., Denver) apply unique physics modifiers:

- **Fatigue Drain**: Accelerates stamina loss for visiting teams.
- **Kicking Distance**: Air density reduction increases max kick distance by ~3% per 1000ft > 4000ft.

## 3. Gameplay Impact (Home Field Bonus)

The `StadiumEngine` translates environmental state into direct gameplay modifiers:

### 3.1 Pre-Snap Penalties (False Start)

The most visible impact of HFA. Loud crowds cause miscommunication for the visiting offense.

- **Trigger**: `possession == "away"` AND `noise_level >= LOUD`.
- **Mechanic**: Checks `rng.random() < false_start_modifier`.
- **Modifier**: Up to 10% probability per play in DEAFENING conditions.
- **Result**: 5-yard penalty, repeat down.

### 3.2 Fatigue Acceleration

- **Trigger**: `altitude > 4000`.
- **Mechanic**: Visiting players lose stamina 2.5% faster per 1000ft elevation.
- **Target**: Denver (5280ft) applies ~3.2% fatigue penalty to visitors.

### 3.3 Kicking Boost

- **Trigger**: High altitude.
- **Mechanic**: Increases `max_distance` for Field Goals and Punts.
- **Magnitude**: +1% (3000ft+), +3% (Denver).

## 4. Reference Data

### Known Loud Stadiums

These stadiums receive an intrinsic +10 Noise Bonus:

- **KC** (Arrowhead)
- **SEA** (Lumen Field)
- **NO** (Superdome)
- **MIN** (US Bank Stadium)
- **BAL** (M&T Bank)
- **BUF** (Highmark)
- **DEN** (Mile High) - _Also applies Altitude Physics_

## 5. Implementation Details

- **Engine**: `app.services.stadium.stadium.StadiumEngine`
- **Orchestrator Hook**: `SimulationOrchestrator._execute_single_play` (Pre-snap check).
- **Verification**: `backend/scripts/verify_home_field_advantage.py` confirms ~3.0 point home margin increase in hostile environments.

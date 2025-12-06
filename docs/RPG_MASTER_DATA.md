# RPG Master Data & Progression System

This document serves as the single source of truth for the Player, Coach, and GM RPG systems. It consolidates currently implemented features with the approved design proposals.

---

## 1. Global Progression Systems

### Leveling & XP
*   **XP Threshold**: `1000 * Current Level * 1.2` (Source: `progression.py`)
*   **Skill Points**: Gained upon leveling up.
    *   **Logic**: `1000 XP = 1 Skill Point` (Source: `player_development_service.py`)
    *   **Usage**: Currently auto-spent by the `PlayerDevelopmentService` to upgrade random relevant attributes or Overall Rating.
*   **Weekly Training**:
    *   **Base Gain**: 50 XP per week.
    *   **Multipliers**:
        *   **Dev Trait**: Star (1.25x), Superstar (1.5x), X-Factor (2.0x).
        *   **Coach Bonus**: +/- based on Head Coach Development Rating.
        *   **Age**: <24 (1.2x), >30 (0.8x).

### Regression
*   **Trigger Age**: 29 years old.
*   **Formula**: `-0.5` per attribute per year after age 28.
*   **Affected Attributes**: Speed, Acceleration, Agility.
*   **Source**: `backend/app/rpg/progression.py`

---

## 2. Position Analysis (Ordered by Data Density)

### 1. Quarterback (QB)
*   **XP Sources (Gameplay)**:
    *   **Pass TD**: +50 XP
    *   **Pass Yards**: +0.5 XP per yard
    *   **Interceptions**: -20 XP
    *   **Playtime**: +50 XP
*   **Abilities & Perks**:
    *   **Implemented (`traits.py`)**:
        *   `DeepBall`: Increases deep accuracy (+5) & reduces drag (0.1).
        *   `Clutch`: Boosts all stats (+5) in 4th Quarter.
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Film Study Master` (Lvl 10): Reveals coverage shell pre-snap.
        *   `The Architect` (Lvl 15): Custom hot routes.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `QBWhisperer` skill (Coach) grants **1.2x XP Gain**.
    *   **Strategy Advantage**: **1.25x** multiplier when offense scheme counters defense (e.g., Vertical vs Cover 3).
    *   **Market Value**: **1.2x** multiplier on contract demands (Inflation logic).

### 2. Wide Receiver (WR) / Tight End (TE)
*   **XP Sources (Gameplay)**:
    *   **Playtime**: +50 XP
    *   **Receiving**: (Generic stat tracking in `player_development_service`, currently standard XP).
*   **Abilities & Perks**:
    *   **Implemented**:
        *   `DeepBall`: (Relevant for WRs on deep routes).
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Route Artist` (WR, Lvl 5): Elite cut animations.
        *   `Security Blanket` (WR): +10% Catch Rate on 3rd down if QB Chemistry > 80.
        *   `Seam Buster` (TE, Lvl 12): Bonus speed up hash marks.
        *   `Sixth Lineman` (TE, Lvl 5): Toggle Blocking vs Receiving stance.
*   **Boosts & Multipliers**:
    *   **Chemistry**: Catch rate modifiers based on QB relationship (Proposed).
    *   **Separation Bonus**: Speed differential * 50.0 = YAC Bonus chance.
    *   **Schematic**: Seam routes vs Cover 3 = **1.25x** Effectiveness.

### 3. Running Back (RB)
*   **XP Sources (Gameplay)**:
    *   **Rush TD**: +40 XP
    *   **Rush Yards**: +0.8 XP per yard
    *   **Playtime**: +50 XP
*   **Abilities & Perks**:
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Combo Breaker` (Lvl 8): Reduced stamina cost for consecutive moves.
        *   `Bell Cow Certification`: Injury resistance boost in 4th quarter.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `ZoneRunMaster` (Coach) grants +5 Run Block Zone.
    *   **Weather**: Rain/Snow increases fumble chance (implied friction physics).

### 4. Defensive Line (DE / DT)
*   **XP Sources (Gameplay)**:
    *   **Sacks**: +100 XP
    *   **Tackles for Loss**: +30 XP
*   **Abilities & Perks**:
    *   **Implemented**:
        *   `BrickWall`: +10 Pass Block (Countered by DL moves).
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Edge Threat` (DE, Lvl 10): "Wide 9" stance for speed rush bonus.
        *   `Spin Cycle` (DE, Lvl 8): Faster spin move.
        *   `Grave Digger` (DT, Lvl 12): Increased pile-up radius.
        *   `Interior Disruptor` (DT, Lvl 15): Block shed chance when QB steps up.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `BlitzHappy` (Coach) grants +5 Pass Rush Power.
    *   **Strategy**: "Hard Counter" defensive calls = **0.75x** multiplier for Offense.

### 5. Linebacker (LB)
*   **XP Sources (Gameplay)**:
    *   **Playtime**: +50 XP
    *   **Tackles/Sacks**: Standard defensive XP logic.
*   **Abilities & Perks**:
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Field Commander` (Lvl 18): Expands "Fog of War" reveal radius.
        *   `Lurker` (Lvl 10): "Super Jump" for interceptions.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `ZoneCoverageSpecialist` (Coach) grants +5 Zone Coverage.

### 6. Defensive Back (CB / S)
*   **XP Sources (Gameplay)**:
    *   **Playtime**: +50 XP
    *   **Interceptions/Deflections**: (Standard XP logic).
*   **Abilities & Perks**:
    *   **Implemented**:
        *   `BallHawk`: +10 Catch in Traffic, 1.2x Interception Rate.
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Island King` (CB, Lvl 20): +5 Stats when isolated (no safety help).
        *   `Route Jumper` (CB, Lvl 12): +50% Jump Route bonus on 4th repeat route.
        *   `Hit Stick Master` (S, Lvl 8): +20% Incompletion chance on impact.
        *   `Robber Role` (S, Lvl 14): Unlocks "Robber" zone assignment.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `ManPressExpert` (Coach) grants +5 Man Coverage.

### 7. Offensive Line (OT / OG / C)
*   **XP Sources**:
    *   **Playtime**: +50 XP
*   **Abilities & Perks**:
    *   **Implemented**:
        *   `BrickWall`: +10 Pass Block vs Bull Rush.
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Island Survivor` (OT, Lvl 20): Negates edge rusher bonus in 1-on-1.
        *   `Technique Doctor` (OT, Lvl 10): +5 Pass Block to adjacent Guard.
        *   `Pull Train` (OG, Lvl 8): +20% Impact Force when pulling.
        *   `Pocket Anchor` (OG, Lvl 12): Prevents push-back > 1 yard.
        *   `Line General` (C, Lvl 15): Identifies Mike LB (Counter to Blitz).
        *   `Snap Perfection` (C, Lvl 5): 0% Shotgun fumble chance.
*   **Boosts & Multipliers**:
    *   **Coach Synergy**: `TrenchWarfare` (Coach) grants **1.2x XP Gain** for OL/DL.

### 8. Special Teams (K / P)
*   **XP Sources**:
    *   **Playtime**: +50 XP
*   **Abilities & Perks**:
    *   **Proposed (`PLAYER_GUIDE.md`)**:
        *   `Clutch Kicker` (K, Lvl 10): Accuracy zone doesn't shrink in 4th Qtr.
        *   `Calibration` (K, Lvl 5): Sideline warm-up (+5% Accuracy).
        *   `Pin Point` (P, Lvl 12): Trajectory preview.
        *   `Fake Specialist` (P, Lvl 8): Boosted stats on fake punts.
*   **Boosts & Multipliers**:
    *   **Environment**:
        *   **Wind**: `Wind Speed * 0.5` affects kick trajectory.
        *   **Altitude**: Boosts kick range.
        *   **Moisture**: **2.0x** Turf Degradation (affects footing).

---

## 3. Management RPG (Coach & GM)

### Coach Skill Trees (`backend/app/rpg/coach.py`)
1.  **Offense**:
    *   `WestCoastGuru` (Lvl 1): +5 Short Pass Accuracy.
    *   `VerticalThreat` (Lvl 1): +5 Deep Pass Accuracy.
    *   `ZoneRunMaster` (Lvl 1): +5 Run Block Zone.
2.  **Defense**:
    *   `BlitzHappy` (Lvl 1): +5 Pass Rush Power.
    *   `ZoneCoverageSpecialist` (Lvl 1): +5 Zone Coverage.
    *   `ManPressExpert` (Lvl 1): +5 Man Coverage.
3.  **Development**:
    *   `QBWhisperer` (Lvl 1): **1.2x** XP Gain for QBs.
    *   `TrenchWarfare` (Lvl 1): **1.2x** XP Gain for OL/DL.

### GM Skill Trees (`backend/app/rpg/gm.py`)
1.  **Scouting**:
    *   `TalentSpotter` (Lvl 1): +10 Scouting Accuracy.
    *   `GemFinder` (Lvl 1): Reveals Late Round Potential.
2.  **Negotiation**:
    *   `CapWizard` (Lvl 1): **-10%** Contract Demands (Multiplier 0.9).
    *   `Charismatic` (Lvl 1): **1.2x** Free Agent Interest.

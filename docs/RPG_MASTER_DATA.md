# RPG Master Data & Reference Guide

**Status:** Active Reference
**Maintainer:** Lead Game Designer / Lead Engineer
**Last Updated:** Phase 7

## 1. Maintenance Instructions
This document serves as the **Authoritative Source of Truth** for all Role-Playing Game (RPG) elements in the Nano Banana simulation engine. It bridges the gap between high-level design (`docs/PLAYER_GUIDE.md`) and actual code implementation (`backend/app/rpg/`).

**When to Update:**
1.  **New Feature:** When a new trait, skill, or ability is added to the codebase.
2.  **Balancing:** When XP formulas or attribute modifiers are tweaked.
3.  **Refactoring:** When the location of RPG logic (e.g., `progression.py`) changes.

**Format:**
*   **Feature Name**: The public name.
*   **Gameplay Description**: What the user sees/feels.
*   **Technical Implementation**: Specific files, classes, and logic governing the feature.

---

## 2. Quarterback (QB) RPG Features

### A. Progression & XP (Leveling)
The core loop of player growth.

*   **Feature:** **Experience Points (XP)**
    *   **Gameplay Description:** QBs earn XP based on their game performance. Performing well (TDs, Yards) grants XP, while mistakes (Interceptions) deduct it. Accumulating XP leads to Level Ups.
    *   **Technical Implementation:**
        *   **File:** `backend/app/rpg/progression.py`
        *   **Class:** `ProgressionEngine`
        *   **Formula:**
            ```python
            XP = Base_Playtime (50)
               + (Pass_TDs * 50)
               + (Pass_Yards * 0.5)
               - (Pass_Ints * 20)
            ```
        *   **Example:** A QB with 300 yards, 3 TDs, and 1 INT earns: $50 + (3 \times 50) + (300 \times 0.5) - (1 \times 20) = 50 + 150 + 150 - 20 = 330 \text{ XP}$.

*   **Feature:** **Level Up**
    *   **Gameplay Description:** Reaching an XP threshold increases the Player Level, granting Skill Points (future implementation).
    *   **Technical Implementation:**
        *   **File:** `backend/app/rpg/progression.py`
        *   **Method:** `check_level_up`
        *   **Threshold Formula:** `Threshold = 1000 * Level * 1.2`
        *   **Data Model:** Stores `xp` and `level` on the `Player` model (`backend/app/models/player.py`).

### B. Traits (Passive Modifiers)
Permanent or semi-permanent buffs defined in the system.

*   **Feature:** **Deep Ball Specialist** (`DeepBall`)
    *   **Gameplay Description:** Increases accuracy on throws over 20 yards and allows the ball to travel further in the air with less velocity decay.
    *   **Technical Implementation:**
        *   **Definition:** `backend/app/rpg/traits.py` -> `TraitSystem.TRAITS["DeepBall"]`
        *   **Modifiers:**
            *   `throw_accuracy_deep`: +5
            *   `drag_reduction`: 0.1 (Physics engine modifier)
        *   **Integration Gap:** Currently, `backend/app/engine/probability_engine.py` does not automatically fetch these modifiers.
        *   **Required Fix:** The `calculate_success_chance` method needs to query `TraitSystem.get_trait_effect` for the active player and add the returned values to `attribute_modifiers`.

*   **Feature:** **Clutch** (`Clutch`)
    *   **Gameplay Description:** Player performs significantly better in the 4th Quarter or Overtime.
    *   **Technical Implementation:**
        *   **Definition:** `backend/app/rpg/traits.py` -> `TraitSystem.TRAITS["Clutch"]`
        *   **Modifiers:**
            *   `all_stats`: +5
        *   **Condition:** `{"condition": "4th_quarter"}`
        *   **Logic:** The simulation engine (`SimulationOrchestrator`) must check `game_clock.quarter >= 4` before applying this bonus.

### C. Abilities (Active/Unlockable - Proposed)
High-level RPG mechanics currently in design/prototyping.

*   **Feature:** **Film Study Master**
    *   **Gameplay Description:** (Unlockable Ability) Reveals the defensive coverage shell (Man vs. Zone) pre-snap if the QB stands in the pocket for 2 seconds.
    *   **Technical Design:**
        *   **Requirement:** Level 10 + 5000 XP cost.
        *   **Frontend (UI):**
            *   Component: `GameStream.tsx`
            *   Visual: A "Film Room" icon lights up 2 seconds after the `SNAP_READY` state.
            *   Action: Displays text "READ: ZONE COVERAGE" above the defensive formation.
        *   **Backend (API):**
            *   Endpoint: `GET /match/insight?player_id={id}`
            *   Logic: Checks `player.abilities` for "FilmStudyMaster". If present, returns the `defensive_scheme` from the `Cortex` kernel (AI).
        *   **Simulation Impact:** Increases `awareness` roll by +15 for the subsequent play decision.

*   **Feature:** **The Architect**
    *   **Gameplay Description:** (Skill Tree) Allows the QB to define custom "Hot Routes" (e.g., a "Smart Post" that breaks earlier) and save them to the playbook.
    *   **Technical Design:**
        *   **Requirement:** Level 15 + "High IQ" Trait.
        *   **Data Structure:**
            *   New Column: `Player.custom_routes` (JSON).
            *   Schema: `{ "name": "Smart Post", "nodes": [(0,0), (0, 10), (5, 15)] }` (Vector path).
        *   **Simulation Logic:**
            *   The `Hive` (Physics Kernel) translates these vector nodes into movement instructions for the WR.
            *   The QB receives a specific `synergy_bonus` when throwing to a WR running an "Architect" route.

---

## 3. Running Back (RB) RPG Features

### A. Progression & XP
*   **Feature:** **Performance XP**
    *   **Technical Implementation:**
        *   **File:** `backend/app/rpg/progression.py`
        *   **Formula:** `XP = 50 + (Rush_TDs * 40) + (Rush_Yards * 0.8)`
        *   **Note:** RBs are one of the few positions with explicit stat tracking in the current XP engine.

### B. Abilities (Proposed)

*   **Feature:** **Combo Breaker**
    *   **Gameplay Description:** Consecutive jukes/spins cost 50% less stamina, allowing for extended runs.
    *   **Technical Design:**
        *   **Requirement:** Level 8 + Agility > 90.
        *   **Simulation Logic:**
            *   In `Genesis` (Biology Kernel), track `moves_performed_this_play`.
            *   If `moves > 0` and ability is active, reduce `stamina_cost` of subsequent move by 0.5.

*   **Feature:** **Bell Cow Certification**
    *   **Gameplay Description:** Increases injury resistance and stamina recovery in the 4th Quarter.
    *   **Technical Design:**
        *   **Requirement:** 200 Carries in a single season.
        *   **Simulation Logic:**
            *   In `Genesis`, check `game_clock.quarter == 4`.
            *   Apply modifier: `injury_roll_threshold += 20` (harder to get injured).
            *   Apply modifier: `fatigue_recovery_rate *= 1.5`.

---

## 4. Receivers (WR, TE) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP**
    *   **Current State:** Currently, WRs and TEs receive only the base **50 XP** per game.
    *   **Gap:** Code in `progression.py` does not explicitly reward Receptions, Yards, or TDs for these positions yet.
    *   **Required Fix:** Update `calculate_xp_gain` to include: `xp += (rec_yards * 0.8) + (rec_tds * 40) + (receptions * 5)`.

### B. Abilities (Proposed)

*   **Feature:** **Route Artist** (WR)
    *   **Gameplay Description:** Unlocks elite animations for specific cuts (e.g., Whip, Comeback).
    *   **Technical Design:**
        *   **Requirement:** Level 5 per route type.
        *   **Simulation Logic:**
            *   In `ProbabilityEngine.compare_skill`: If `route_type` matches unlocked art, grant `separation_bonus += 0.15`.
            *   Frontend: Trigger specific `animation_id` (e.g., `WR_CUT_ELITE_01`) instead of generic.

*   **Feature:** **Security Blanket** (WR)
    *   **Gameplay Description:** +10% Catch Rate on 3rd Down if QB Chemistry > 80.
    *   **Technical Design:**
        *   **Requirement:** 3 Seasons with same QB.
        *   **Simulation Logic:**
            *   Check `match_context.down == 3`.
            *   Check `RelationshipManager.get_chemistry(qb_id, wr_id) > 80`.
            *   Apply `catch_probability += 0.10`.

*   **Feature:** **Seam Buster** (TE)
    *   **Gameplay Description:** Bonus speed for 2s when releasing vertically.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Speed > 80.
        *   **Simulation Logic:**
            *   If route is "Go", "Seam", or "Post": Apply `speed_modifier = 1.1` for first 2.0 seconds of play clock in `Hive` kernel.

*   **Feature:** **Sixth Lineman** (TE)
    *   **Gameplay Description:** Toggle between Receiver Stance (Agility) and Blocking Stance (Strength).
    *   **Technical Design:**
        *   **Requirement:** Level 5.
        *   **Data:** New `Player.active_stance` (Enum).
        *   **Logic:** Pre-snap modifier application. `BLOCKING`: +5 Str, -5 Agi. `RECEIVER`: -5 Str, +5 Agi.

---

## 5. Offensive Line (OT, OG, C) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP**
    *   **Current State:** OL receive only the base **50 XP**.
    *   **Gap:** No reward for Pancakes or Sacks Allowed prevented.
    *   **Required Fix:** Implement tracking for "Pancakes" in `SeasonStats` and award XP (e.g., +10 per Pancake).

### B. Traits (Implemented)
*   **Feature:** **Brick Wall** (`BrickWall`)
    *   **Gameplay Description:** Increases pass block rating against Bull Rush moves.
    *   **Technical Implementation:**
        *   **Definition:** `TraitSystem.TRAITS["BrickWall"]`.
        *   **Effect:** `pass_block +10` when `defender_move == "BULL_RUSH"`.

### C. Abilities (Proposed)

*   **Feature:** **Island Survivor** (OT)
    *   **Gameplay Description:** Negates edge rusher bonuses in 1-on-1 situations.
    *   **Technical Design:**
        *   **Requirement:** Level 20 + Pass Block > 90.
        *   **Simulation Logic:**
            *   Scan `defensive_front`: If no defender is in adjacent gap (isolated), force defender `pass_rush_move_bonus = 0`.

*   **Feature:** **Pull Train** (OG)
    *   **Gameplay Description:** +20% Impact Force when pulling.
    *   **Technical Design:**
        *   **Requirement:** Level 8 + Strength > 85.
        *   **Simulation Logic:**
            *   If `play_type == "POWER"` and guard is `pulling`: `impact_force *= 1.2` in collision physics.

*   **Feature:** **Line General** (C)
    *   **Gameplay Description:** Identifies "Mike" LB to reset blocking assignments.
    *   **Technical Design:**
        *   **Requirement:** Level 15 + Awareness > 90.
        *   **Simulation Logic:**
            *   AI Logic (`Cortex`): If Center has ability, `blocking_intelligence` set to Max. Eliminates "blown assignment" RNG events.

---

## 6. Defensive Front (DE, DT, LB) RPG Features

### A. Progression & XP
*   **Feature:** **Sack Master XP**
    *   **Technical Implementation:**
        *   **File:** `backend/app/rpg/progression.py`
        *   **Formula:** `XP = 50 + (Sacks * 100) + (TFL * 30)`
        *   **Scope:** Applies to DE and DT.
        *   **Gap:** LBs currently fall to default XP unless manually tagged as DE/DT in logic. Needs to include `position == "LB"`.

### B. Abilities (Proposed)

*   **Feature:** **Edge Threat** (DE)
    *   **Gameplay Description:** "Wide 9" alignment for speed rush bonus.
    *   **Technical Design:**
        *   **Requirement:** Level 10.
        *   **Logic:** Trade-off: `pass_rush_speed += 10`, `run_block_shed -= 15`.

*   **Feature:** **Grave Digger** (DT)
    *   **Gameplay Description:** Increased "Pile Up" radius, clogging gaps.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Weight > 320.
        *   **Logic:** In `Hive` (Physics): `collision_radius *= 1.25`. Any ball carrier touching this radius is slowed.

*   **Feature:** **Field Commander** (LB)
    *   **Gameplay Description:** Expands "Fog of War" reveal radius.
    *   **Technical Design:**
        *   **Requirement:** Level 18 + Awareness > 95.
        *   **Logic:** `MatchContext.visibility_radius` increased by 5 yards for the defense user.

---

## 7. Secondary (CB, S) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP**
    *   **Gap:** No XP for Interceptions or Deflections in current code.
    *   **Required Fix:** Add `XP += (Ints * 50) + (Deflections * 10)`.

### B. Traits (Implemented)
*   **Feature:** **Ball Hawk** (`BallHawk`)
    *   **Gameplay Description:** Increases interception chance.
    *   **Technical Implementation:**
        *   **Definition:** `TraitSystem.TRAITS["BallHawk"]`.
        *   **Effect:** `catch_in_traffic +10`, `interception_rate * 1.2`.

### C. Abilities (Proposed)

*   **Feature:** **Island King** (CB)
    *   **Gameplay Description:** +5 Stats when no Safety help is visible.
    *   **Technical Design:**
        *   **Requirement:** Level 20 + Man Cov > 95.
        *   **Logic:** Check `defensive_shell`. If `safety_depth > 20` or `safety_side != cb_side`: Apply `man_coverage += 5`.

*   **Feature:** **Robber Role** (S)
    *   **Gameplay Description:** Unlocks "Robber" zone (short middle trap).
    *   **Technical Design:**
        *   **Requirement:** Level 14.
        *   **AI Logic:** Unlocks a specific node in the AI decision tree (`Cortex`) allowing the Safety to abandon deep zone for an intermediate intercept path.

---

## 8. Special Teams (K, P) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP**
    *   **Gap:** No XP for FG Made or Punt Yards.
    *   **Required Fix:** Add specific ST formulas.

### B. Abilities (Proposed)

*   **Feature:** **Clutch Kicker** (K)
    *   **Gameplay Description:** Accuracy Zone does not shrink in 4th Qtr.
    *   **Technical Design:**
        *   **Requirement:** Level 10.
        *   **Frontend (UI):** In `KickMeter.tsx`, ignore the `pressure_modifier` that usually shrinks the green zone if `game_clock.quarter >= 4`.

*   **Feature:** **Pin Point** (P)
    *   **Gameplay Description:** Shows exact trajectory for Coffin Corner punts.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Accuracy > 90.
        *   **Frontend (UI):** Render a `TrajectoryLine` component on the field visualization showing the bounce path.

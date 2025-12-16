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
        *   **Example:** A RB with 100 yards and 1 TD earns: $50 + (1 \times 40) + (100 \times 0.8) = 170 \text{ XP}$.
        *   **Note:** RBs are one of the few positions with explicit stat tracking in the current XP engine.

### B. Abilities (Proposed)

*   **Feature:** **Combo Breaker**
    *   **Gameplay Description:** Consecutive jukes/spins cost 50% less stamina, allowing for extended runs.
    *   **Technical Design:**
        *   **Requirement:** Level 8 + Agility > 90.
        *   **Kernel:** `backend/app/kernels/genesis/progression_bio.py` (Fatigue).
        *   **Simulation Logic:**
            *   Track `moves_performed_this_play` in the `MatchContext`.
            *   If `moves > 0` and ability is active, set `stamina_drain_multiplier = 0.5`.
        *   **Frontend Impact:** The stamina bar (under player nameplate) flashes blue instead of red during the second move.

*   **Feature:** **Bell Cow Certification**
    *   **Gameplay Description:** Increases injury resistance and stamina recovery in the 4th Quarter.
    *   **Technical Design:**
        *   **Requirement:** 200 Carries in a single season.
        *   **Kernel:** `Genesis` (Biology).
        *   **Simulation Logic:**
            *   If `game_clock.quarter == 4`:
            *   Set `injury_roll_threshold += 20` (Effective injury chance drops from ~2% to ~0.5%).
            *   Set `fatigue_recovery_rate *= 1.5` (Recovers faster on sideline).

---

## 4. Receivers (WR, TE) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP (Current Gap)**
    *   **Current State:** WRs/TEs currently receive only base **50 XP**.
    *   **Gap:** Code in `progression.py` does not explicitly reward Receptions, Yards, or TDs for these positions yet.
    *   **Required Fix:** Update `calculate_xp_gain` to include: `xp += (rec_yards * 0.8) + (rec_tds * 40) + (receptions * 5)`.
    *   **Example (Post-Fix):** 5 catches, 80 yards, 1 TD = $50 + (25) + (64) + (40) = 179 \text{ XP}$.

### B. Abilities (Proposed)

*   **Feature:** **Route Artist** (WR)
    *   **Gameplay Description:** Unlocks elite animations for specific cuts (e.g., Whip, Comeback) creating instant separation.
    *   **Technical Design:**
        *   **Requirement:** Level 5 per route type.
        *   **Data:** `Player.unlocked_animations` list.
        *   **Simulation Logic (`ProbabilityEngine`):**
            *   If `route_type` in unlocked list: `separation_bonus += 0.15`.
        *   **Frontend (Visualization):**
            *   Instead of standard `WR_CUT_GENERIC`, trigger `WR_CUT_ELITE_WHIP`.
            *   Requires `frontend/src/assets/animations/elite_routes.json`.

*   **Feature:** **Security Blanket** (WR)
    *   **Gameplay Description:** +10% Catch Rate on 3rd Down if QB Chemistry > 80.
    *   **Technical Design:**
        *   **Requirement:** 3 Seasons with same QB.
        *   **Kernel:** `Cortex` (Strategy) & `Core` (Orchestration).
        *   **Simulation Logic:**
            *   Check `match_context.down == 3`.
            *   Query `RelationshipManager.get_chemistry(qb_id, wr_id)`.
            *   If > 80: `catch_probability_modifier = 1.10`.
        *   **API:** `GET /player/{id}/synergy?partner_id={qb_id}`.

*   **Feature:** **Seam Buster** (TE)
    *   **Gameplay Description:** Bonus speed for 2s when releasing vertically.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Speed > 80.
        *   **Kernel:** `Hive` (Physics).
        *   **Simulation Logic:**
            *   Detect Route Type: "Go", "Seam", "Post".
            *   Apply `speed_burst = 1.1` for `t < 2.0s`.
            *   After 2s, revert to base speed.

*   **Feature:** **Sixth Lineman** (TE)
    *   **Gameplay Description:** Toggle between Receiver Stance (Agility) and Blocking Stance (Strength).
    *   **Technical Design:**
        *   **Requirement:** Level 5.
        *   **Data:** New `Player.active_stance` (Enum: `RECEIVER` | `BLOCKING`).
        *   **UI:** Pre-game toggle in `DepthChart` or `GamePlan`.
        *   **Logic:**
            *   `BLOCKING`: +5 STR, -5 AGI, +10 Run Block.
            *   `RECEIVER`: -5 STR, +5 AGI, +10 Release.

---

## 5. Offensive Line (OT, OG, C) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP (Current Gap)**
    *   **Current State:** OL receive only the base **50 XP**.
    *   **Required Fix:** Implement "Pancakes" tracking.
    *   **Formula:** `XP = 50 + (Pancakes * 10) + (Sacks_Allowed * -10)`.

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
        *   **Kernel:** `Hive` (Physics/Collision).
        *   **Simulation Logic:**
            *   Detect alignment: If `abs(OT.x - DE.x) < 2.0` AND no TE/RB within 3 yards.
            *   Set `defender_special_move_chance = 0`.
            *   Force standard "Engagement" physics logic instead of "Special Move" logic.

*   **Feature:** **Pull Train** (OG)
    *   **Gameplay Description:** +20% Impact Force when pulling.
    *   **Technical Design:**
        *   **Requirement:** Level 8 + Strength > 85.
        *   **Simulation Logic:**
            *   If `play_assignment == "PULL"`:
            *   `momentum_transfer_coefficient *= 1.2`.
            *   Increases chance of `KNOCKDOWN` event on defender.

*   **Feature:** **Line General** (C)
    *   **Gameplay Description:** Identifies "Mike" LB to reset blocking assignments.
    *   **Technical Design:**
        *   **Requirement:** Level 15 + Awareness > 90.
        *   **Kernel:** `Cortex` (AI).
        *   **Simulation Logic:**
            *   Effectively sets `blocking_intelligence = 1.0` (Max).
            *   Prevents `BLOWN_ASSIGNMENT` events (where two linemen block one guy and leave one free).
        *   **UI:** Shows a "Target" icon over the designated Mike LB in pre-snap view.

---

## 6. Defensive Front (DE, DT, LB) RPG Features

### A. Progression & XP
*   **Feature:** **Sack Master XP**
    *   **Technical Implementation:**
        *   **File:** `backend/app/rpg/progression.py`
        *   **Formula:** `XP = 50 + (Sacks * 100) + (TFL * 30)`
        *   **Example:** 2 Sacks, 1 TFL = $50 + 200 + 30 = 280 \text{ XP}$.
        *   **Gap:** LB position string needs to be added to the `if` check.

### B. Abilities (Proposed)

*   **Feature:** **Edge Threat** (DE)
    *   **Gameplay Description:** "Wide 9" alignment for speed rush bonus.
    *   **Technical Design:**
        *   **Requirement:** Level 10.
        *   **Data:** `Player.alignment_preference`.
        *   **Logic:**
            *   Widens starting coordinate `x`.
            *   `pass_rush_speed += 10`.
            *   `run_block_shed -= 15` (Vulnerable to Inside Zone).

*   **Feature:** **Grave Digger** (DT)
    *   **Gameplay Description:** Increased "Pile Up" radius, clogging gaps.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Weight > 320.
        *   **Kernel:** `Hive`.
        *   **Logic:**
            *   `collision_radius *= 1.25`.
            *   Any ball carrier entering this radius suffers `speed *= 0.7` (The "Mud" effect).

*   **Feature:** **Field Commander** (LB)
    *   **Gameplay Description:** Expands "Fog of War" reveal radius.
    *   **Technical Design:**
        *   **Requirement:** Level 18 + Awareness > 95.
        *   **Kernel:** `Cortex` (Vision System).
        *   **Logic:**
            *   `MatchContext.visibility_radius` typically 15 yards.
            *   With ability: `visibility_radius = 20 yards`.
        *   **UI:** The "Darkened" area of the field is smaller for the defensive user.

---

## 7. Secondary (CB, S) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP (Current Gap)**
    *   **Gap:** No XP for Interceptions or Deflections.
    *   **Required Fix:** `XP += (Ints * 50) + (Deflections * 10)`.
    *   **Example:** 1 INT, 3 PDs = $50 + 50 + 30 = 130 \text{ XP}$.

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
        *   **Simulation Logic:**
            *   Scan `defensive_shell`: Calculate distance to nearest Safety.
            *   If `distance > 20 yards`: `man_coverage_rating += 5`.
            *   Visible notification "ISLAND MODE ACTIVE".

*   **Feature:** **Robber Role** (S)
    *   **Gameplay Description:** Unlocks "Robber" zone (short middle trap).
    *   **Technical Design:**
        *   **Requirement:** Level 14.
        *   **Kernel:** `Cortex` (AI Behavior Tree).
        *   **Logic:**
            *   Unlocks `ZoneAssignment.ROBBER`.
            *   Behavior: Drop to 10 yards depth, then read QB eyes.
            *   Triggers generic "Cut Route" logic on crossing patterns entering zone.

---

## 8. Special Teams (K, P) RPG Features

### A. Progression & XP
*   **Feature:** **Standard Playtime XP (Current Gap)**
    *   **Required Fix:** Add specific ST formulas.
    *   **Formula:** `XP = 20 + (FG_Made * 20) + (FG_Long * 0.5)`.

### B. Abilities (Proposed)

*   **Feature:** **Clutch Kicker** (K)
    *   **Gameplay Description:** Accuracy Zone does not shrink in 4th Qtr.
    *   **Technical Design:**
        *   **Requirement:** Level 10.
        *   **Frontend (UI):** `KickMeter.tsx`.
        *   **Logic:**
            *   Standard: `green_zone_width = base_width - (pressure * 2)`.
            *   With Ability: `green_zone_width = base_width`.
            *   Visual: The meter glows gold to indicate immunity to pressure.

*   **Feature:** **Pin Point** (P)
    *   **Gameplay Description:** Shows exact trajectory for Coffin Corner punts.
    *   **Technical Design:**
        *   **Requirement:** Level 12 + Accuracy > 90.
        *   **Frontend (UI):** `FieldRenderer.tsx`.
        *   **Logic:**
            *   Calculate physics arc using `ball_velocity` and `angle`.
            *   Render `TrajectoryLine` component (dotted line) showing landing spot + bounce roll.
            *   Standard view only shows landing area circle (uncertainty). This shows precise point.

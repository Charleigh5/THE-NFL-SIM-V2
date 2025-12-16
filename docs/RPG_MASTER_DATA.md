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

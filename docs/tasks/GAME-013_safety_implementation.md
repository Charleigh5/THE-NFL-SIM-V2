# TASK: GAME-013 Safety Scenarios Implementation

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** The Safety (2 points) is one of the rarest scoring plays in football, punishing offenses for retreating into their own end zone. It requires precise field position logic (checking < 0 or > 100).
- **Related Ideas:** Touchbacks (similar boundary condition but different outcome), Turnovers (possession change), Sacks (negative yardage leading to safety).
- **Future Potential:** Safety logic establishes the "hard boundaries" of the field. This foundation is critical for future features like "momentum swings" (a safety is a massive momentum killer) and specialized "safety kick" returns (different from standard kickoffs).
- **Constraints:** - Must handle both "Home" and "Away" possession directions correctly. - Must account for negative yardage plays (Sacks, TFLs). - Must trigger specific "Free Kick" logic (kick from 20), not standard kickoff (from 35). - Must be detected _after_ yardage calculation but _before_ possession flipping.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Implement a boolean flag `is_safety` in `PlayResult`. In `PlayResolver`, check if `start_yard - loss <= 0` (or >= 100). In `Orchestrator`, if `is_safety` is true, award 2 points and set up a free kick state.

### Powerful Antithesis

- **Race Condition/Order of Operations:** If the Orchestrator flips possession _before_ checking for safety, the "own end zone" logic flips. A safety for Home could be misinterpreted as a Touchback for Away if possession changes first.
- **Double Counting:** If a sack causes a safety, does it count as a Sack statistic AND a Safety? Yes. But if we aren't careful, we might double-decrement yardage or stats.
- **The "Safety Kick" Edge Case:** Users might expect a standard kickoff. A safety kick is a punt or placekick from the 20. If we use standard kickoff logic, the field position math will be wrong (receiving team starts too far back).
- **Fumble Safeties:** What if a player fumbles into the end zone and the offense recovers? Or defense bats it out? (Edge case: Simply treating "tackled in end zone" covers 95% of cases, fumble recovery location needs to be precise).

### The Superior Synthesis

- **State Logic:** The `PlayResolver` is the authority on _what happened_. It must return `is_safety=True` explicitly. The `Orchestrator` handles the _consequences_ (points, possession change).
- **Order of Ops:** Orchestrator must process score -> stats -> possession change in that strict order.
- **Specific Kick Logic:** We will explicitly set the yard line to 20 for the post-safety free kick, differentiating it from the standard 35-yard line kickoff.
- **Unified Detection:** Create a helper `_check_for_safety()` in `PlayResolver` used by both Run and Pass resolvers to ensure consistent boundary logic (Home vs Away directions).
  </adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** Python 3.11+ (FastAPI/Pydantic)
- **Framework:** Backend Orchestrator Pattern
- **State Management:** `SimulationOrchestrator` (Async)

### 2. The Data Schema (Pre-Generation)

- **EventType:** Add `SAFETY` to Enum.
- **PlayResult:** Field `is_safety: bool` (Already exists, enforce usage).
- **MomentumEvent:** Ensure `SAFETY` momentum event exists/is utilized.

### 3. Step-by-Step Execution

- [ ] **Step 1: Event Bus Update.**

  - Modify `backend/app/engine/event_bus.py` to include `SAFETY` in `EventType`.

- [ ] **Step 2: Core Logic (PlayResolver).**

  - Create helper `_check_for_safety(possession, start_yard, yards_gained) -> bool`.
  - Function `_resolve_pass_play`: Add safety check after sack logic.
  - Function `_resolve_run_play`: Refactor to use new helper.

- [ ] **Step 3: Orchestrator Handling.**

  - Modify `backend/app/orchestrator/simulation_orchestrator.py`.
  - In `_update_game_state`: Verify point award (2 pts).
  - **CRITICAL:** Fix free kick yard line. Set `self.yard_line = 20`.

- [ ] **Step 4: Verification Tests.**
  - Create `backend/tests/unit/test_safety_scenarios.py`.
  - Test Home Safety, Away Safety, Pass Sack Safety, Run TFL Safety.

### 4. Edge Cases & Error Handling

- [Case A: 0 Yard Line Exact] -> Treated as Safety.
- [Case B: 100 Yard Line Exact] -> Treated as Safety.
- [Case C: Momentum Error] -> Ensure Momentum Engine doesn't crash if event type missing (handled by Enum update).

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** No `any` types allowed.
- [ ] **Security:** N/A (Internal Logic).
- [ ] **Performance:** No heavy computations added.
- [ ] **Self-Critique:** Did I remember to update the player stats? A safety sack is still a sack. Ensure `is_sack` remains True even if `is_safety` is True.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Execute Step 1 (Event Bus Update) and Step 2 (PlayResolver Logic).
</baton_handoff>

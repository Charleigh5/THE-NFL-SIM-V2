# TASK: AI-003 (Coaching AI Personality)

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Classic sports sims (Madden, Football Manager) model coaches as bundles of tendecies.
  - The goal is to move beyond simple "Run/Pass Ratio" to semantic behaviors ("The Gambler", "The Defensive Mastermind").
- **Related Ideas:**
  - _Utility Theory:_ Making decisions based on expected value (Analytics Coach).
  - _Bounded Rationality:_ Making sub-optimal decisions based on personality flaws (Conservative Coach playing too safe).
- **Future Potential:**
  - 2026/2027 Scaling: "Learning" Coaches that adapt their personality over a career based on wins/losses.
  - Multi-Agent Orchestration: Coordinators having different personalities than Head Coaches, causing internal friction.
- **Constraints:**
  - **Deterministic Execution:** Same seed + same state = same decision.
  - **Performance:** Decision logic must be O(1) inside the `resolve_play` loop (~16ms budget).
  - **Data Compatibility:** Must use existing `CoachingPhilosophy` models from `backend/app/data/coaches.py`.
    </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Implement a `CoachingPhilosophy` injection into `PlayCaller`. Contextual decision-making (e.g., "Go for it on 4th down") is biased by scalar values (`aggressiveness`, `pass_heavy`). Simple, linear weights.

### Powerful Antithesis

**The Critic Attacks:**

1. **Linear Predictability:** A simple scalar (`aggression=0.8`) is boring. It just means they blitz 80% of the time. Real coaches vary by context (Aggressive on 4th down, Conservative on 3rd & long?).
2. **State Friction:** If a "Run Heavy" coach is down by 20 points, do they still run? A rigid system creates "stupid AI" resulting in user frustration.
3. **Confliction:** What happens if `run_pass_ratio` says "Pass" but `clock_management` says "Burn Clock"? Priority conflicts leads to undefined behavior.

### The Superior Synthesis

**The Definitive Architecture:**
We will implement a **Context-Aware Weighting System with Priority Overrides**.

1. **Situational Scalars:** `Aggression` isn't a static check. It's a modifier applied `should_go_for_it(context)`. Meaning even a conservative coach has a threshold where they _must_ pass.
2. **Badges & Archetypes:** Beyond sliders, we use boolean flags (e.g., `Badge.RIVERBOAT_GAMBLER`) that unlock specific overrides (e.g., "Always go for it on 4th & <2 inside 50").
3. **Fluid Logic layer:** `_decide_run_vs_pass` calculates a Base Weight logic, then applies Personality Modifiers, _then_ applies Situational Overrides (Score/Time).

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** Python 3.12 (Strict Types)
- **Framework:** Pydantic (Models), FastAPI (Orchestrator)
- **State Management:** `GameStateManager` providing readonly context.

### 2. The Data Schema (Pre-Generation)

- **Model:** `CoachingPhilosophy` (Existing in `app/data/coaches.py`)
  - `run_pass_ratio: int` (0-100)
  - `aggressiveness: int` (0-100)
  - `fourth_down_aggression: int` (0-100) [NEW]
  - `trick_play_frequency: int` (0-100) [NEW]

### 3. Step-by-Step Execution

- [ ] **Step 1: Scaffolding.**

  - [ ] Verify `backend/app/data/coaches.py` has the new fields (`fourth_down_aggression`, etc).
  - [ ] Create `backend/app/services/playbook/personality_profiles.py` to hold "Archetype" definitions if needed.

- [ ] **Step 2: Core Logic (`play_caller.py`).**

  - [ ] Update `PlayCaller.__init__` to accept `CoachingPhilosophy`.
  - [ ] Implement `_get_effective_aggression(context)` to blend base trait with score/time urgency.
  - [ ] Update `_handle_fourth_down` to use the effective aggression score.
  - [ ] Update `_decide_run_vs_pass` to use `run_pass_ratio` + context scalars.

- [ ] **Step 3: Interface & Verification.**
  - [ ] Add `CoachPersonality` display to the Frontend "Staff" page.
  - [ ] Unit Test `PlayCaller` with extreme personas (0 Aggression vs 100 Aggression) and verify statistically significant difference in outputs.

### 4. Edge Cases & Error Handling

- [Case A: No Coach Assigned] -> Fallback to `DEFAULT_PHILOSOPHY` (Balanced 50/50).
- [Case B: Conflicting Signals] -> Urgency (Time/Score) always trumps Personality (e.g., Losing team MUST Hail Mary even if "Run Heavy").

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy --strict` on `play_caller.py`.
- [ ] **Security:** Ensure `rng` is thread-safe/deterministic.
- [ ] **Performance:** No database calls inside `select_play`. All attributes must be in-memory.
- [ ] **Balance Check:** Simulate 100 4th Down decisions. Ensure "Riverboat" archetype attempts >80% vs "Conservative" <20%.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: **Step 2: Core Logic** -> Update `backend/app/orchestrator/play_caller.py` with `CoachingPhilosophy` injection.
</baton_handoff>

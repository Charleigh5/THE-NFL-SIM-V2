# TASK: RPG-003 (Age-Based Growth & Regression)

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - "The Rookie Wall", "Sophomore Slump", "Father Time Remaining Undefeated".
  - Simulating the lifecycle of an athlete is critical for Dynasty Mode longevity.
- **Related Ideas:**
  - _Survival Analysis:_ Predicting career length based on position and usage (RBs burn out fast).
  - _RPG Leveling:_ Experience Points (XP) curve typically gets steeper; here, the "Ability to Gain XP" decays.
- **Future Potential:**
  - 2026+: DNA/Genetics system where "freak athletes" age slower (LeBron/Brady trait).
  - Injury History compounding regression (ACL tear speeds up speed decay).
- **Constraints:**
  - **Population Stability:** The league cannot become all 99 OVRs (Inflation) or all 60 OVRs (Depression) after 10 years.
  - **Fun Factor:** Regression sucks for the user. It must be communicated clearly ("He's losing a step") rather than just silent stat drops.
    </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Implement deterministic Age Curves per position.

- RB: Peak 24-27. Hard decline at 29.
- QB: Peak 28-32. Slow decline till 38.
- Logic: `AttributeChange = BaseXP * AgeMultiplier`.

### Powerful Antithesis

**The Critic Attacks:**

1. **The "Cliff" Problem:** If every RB drops 5 speed points at age 29, users will trade every RB at age 28. It becomes a spreadsheet exploit.
2. **Lack of Narrative:** Real players defy curves. Frank Gore played forever. RG3 burned out instantly. Rigid curves kill stories.
3. **Attribute Homogenization:** If everyone follows the same curve, unique player identities are lost over time.

### The Superior Synthesis

**The Definitive Architecture:**
We will implement a **Stochastic Trajectory System**.

1. **Archetype Curves:** A "Power Back" ages differently than a "Speed Back" (Speed dies fast, Power lingers).
2. **Variance Roll:** Every offseason, players roll for their "Aging Factor". Most follow the curve, but 5% defy it (Positive or Negative).
3. **Usage Toll:** It's not just age; it's `Carries`. 2000 career carries triggers a "Wear and Tear" regression modifier, punishing overuse.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** Python 3.12
- **Framework:** `scipy` (for curve interpolation if needed, or simple linear lerp).
- **Service:** `ProgressionService` (Growth) and `RegressionService` (Decay).

### 2. The Data Schema (Pre-Generation)

- **Model:** `GrowthCurve` (JSON config or Python Class)
  - `position: str`
  - `peak_start: int`
  - `peak_end: int`
  - `decline_rate: float`
- **Player Field:** `biological_age: float` (Can be distinct from calendar age for "Wear and Tear").

### 3. Step-by-Step Execution

- [ ] **Step 1: Curve Definition.**

  - [ ] Create `backend/app/services/rpg/growth_curves.py`.
  - [ ] Define dictionaries for `POSITION_CURVES` (Start, Peak, End).

- [ ] **Step 2: Core Logic (`offseason_service.py`).**

  - [ ] Implement `apply_progression()`: Multiply XP by `AgeFactor` (Rookies 1.5x, Vets 0.5x).
  - [ ] Implement `apply_regression()`: Check Age > PeakEnd. If true, roll for attribute loss.
  - [ ] Implement `UsageTax`: If Snaps > Threshold, apply temp penalty or permanent decay.

- [ ] **Step 3: Interface.**
  - [ ] "Career Phase" indicator on Player Card (Rising Star, Prime, Veteran, Decline).
  - [ ] End-of-Season Report: "Notable Regressions" list.

### 4. Edge Cases & Error Handling

- [Case A: Un-retirement] -> If we implement Brett Favre scenarios, age curve resumes.
- [Case B: Late Bloomer] -> Procedually generated rookies entering league at 24 instead of 21.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Strict floats for multipliers.
- [ ] **Simulation Test:** Run 10-year sim. specific check: "Do 35+ year old RBs exist?" (Should be < 1%). "Do 40 year old QBs exist?" (Should be ~2-3%).
- [ ] **Eco-System:** Verify League-wide Average OVR stays between 75-78.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: **Step 1: Curve Definition** -> Create `backend/app/services/rpg/growth_curves.py`.
</baton_handoff>

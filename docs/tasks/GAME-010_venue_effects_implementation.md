# TASK: GAME-010 (Venue-Specific Effects)

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - "The 12th Man" (Seattle), "Lambeau Leap" (Green Bay).
  - Home field advantage is statistically proven (approx +2.5 points in NFL).
  - Elements: Crowd Noise (Communication disruption), Weather (Wind/Cold), Physics (Altitude).
- **Related Ideas:**
  - _Dynamic Audio Engines:_ Sound affecting gameplay mechanics (not just cosmetic).
  - _Environmental Physics:_ Projectile motion changes based on air density (Denver vs Miami).
- **Future Potential:**
  - 2027 Scaling: RT crowd rendering where individual fans react to plays.
  - Dynamic Momentum: Crowd gets quieter if the home team is losing badly (-Decibels).
- **Constraints:**
  - **Fairness:** Must not make the game unplayable for the Away team (e.g., 50% False Start rate is bad UX).
  - **Clarity:** User must know WHY their kick fell short (Visual indicator for Altitude/Wind).
    </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Implement modifiers in `StadiumEngine`.

- `noise_level` -> increases `FalseStart` probability.
- `altitude` -> increases `MaxKickDistance` and `FatigueRate`.
- `dome` -> eliminates `Wind/Rain` effects.

### Powerful Antithesis

**The Critic Attacks:**

1. **Metric Abuse:** If Denver gives +5 yards to kicks, everyone will pick Denver for H2H. It breaks competitive balance.
2. **Invisible Walls:** Increasing `FatigueRate` because of "Altitude" feels like a bug if not communicated. "Why is my RB tired after 2 runs?"
3. **Audio Frustration:** If "Loudness" just means screen shake and inability to audible, it can be annoying, not immersive.

### The Superior Synthesis

**The Definitive Architecture:**
We will implement a **Transparent Environmental Layer**.

1. **Visual Feedback:** Altitude/Weather must have specific UI icons (e.g., "Thin Air: +5% Kick Range, +10% Fatigue").
2. **Momentum Coupling:** Noise isn't static. It scales with `Momentum`. A silent 4th quarter in Green Bay if they are down by 21.
3. **Attribute Counter-Play:** `StadiumVolume` vs `QB.Leadership`. A veteran QB ignores the noise; a rookie crumbles.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** Python 3.12 (Strict Types)
- **Framework:** Pydantic (Stadium Models)
- **Pattern:** Decorator Pattern (Modifiers applied to Physics results).

### 2. The Data Schema (Pre-Generation)

- **Model:** `Stadium` (Enriched)
  - `altitude_ft: int` (0-5280+)
  - `is_dome: bool`
  - `base_decibels: float` (Typical noise floor)
  - `max_decibels: float` (Peak noise)

### 3. Step-by-Step Execution

- [ ] **Step 1: Data Enrichment.**

  - [ ] Update `backend/app/data/stadiums.py` with real-world altitude and decibel data.
  - [ ] Implement `StadiumEngine.get_current_conditions(weather, momentum)`.

- [ ] **Step 2: Core Logic.**

  - [ ] **Kicking:** Update `SpecialTeamsEngine` to multiply distance by `1 + (altitude / 10000)`.
  - [ ] **Penalties:** Update `PlayResolver` pre-snap check. `FalseStartChance = Base + (Decibels - QB.Leadership)`.
  - [ ] **Fatigue:** Update `FatigueSystem`. `StaminaDrain *= 1.1` at high altitude.

- [ ] **Step 3: Interface.**
  - [ ] Add "Environment Monitor" to the Pre-Game Hub.
  - [ ] Trigger "Crowd Roar" event in Frontend when decibels peak.

### 4. Edge Cases & Error Handling

- [Case A: Neutral Site] -> Super Bowl / London games have `home_field_advantage = 0`.
- [Case B: Empty Stadium] -> Covid/Practice mode sets `decibels = 0`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** No magic numbers. Use `constants.py` for multipliers.
- [ ] **Balance Check:** Simulate 1000 Kicks at Denver vs Miami. Confirm ~5 yard difference.
- [ ] **UX Check:** Verify that users can see _why_ a penalty occurred ("Crowd Noise caused False Start").
      </final_audit>

---

<baton_handoff>
Next Immediate Step: **Step 1: Data Enrichment** -> Update `backend/app/data/stadiums.py`.
</baton_handoff>

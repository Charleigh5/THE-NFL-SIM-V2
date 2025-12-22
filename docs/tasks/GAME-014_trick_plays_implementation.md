# TASK: GAME-014 (Trick Plays)

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Trick plays are the "wildcards" of football history (e.g., The Boise State Statue of Liberty, The Philly Special). They rely on deception, misdirection, and breaking the opponent's mental model of the play.
- **Related Ideas:**
  - _Fog of War:_ The defense doesn't know the play type until specific "tells" are revealed.
  - _Momentum Mechanics:_ A successful trick play is a massive momentum booster; a failure is a morale crusher.
- **Future Potential:**
  - 2026/2027 Scaling: Complex multi-stage animation blending (e.g., WR pass option).
  - AI learning to _bait_ trick plays by showing specific defensive looks.
- **Constraints:** - Must function within the 60Hz physics engine or cleanly abstract it. - AI must not spam these (Anti-Cheese logic required). - Data usage: Must use real player attributes (e.g., Punter throwing power), not generic values.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Implement simple probabilistic resolution for "Fake Punt Run/Pass" and "Fake FG". If `Random < SuccessChance`, give First Down. Simple, effective, reliable.

### Powerful Antithesis

**The Critic Attacks:**

1. **"RNG-fest":** Pure probability feels cheap. If I have a freak athlete at Punter, I want his speed to matter, not a dice roll.
2. **Logic Gaps:** What if the defense is in "Safe Special Teams" formation? A fake punt should almost _never_ work against a safe defense.
3. **Exploits:** If the success rate is > 50%, players will run Fake Punt every 4th down. The AI is too stupid to counter it.
4. **Physics Disconnect:** If the play is a "Flea Flicker", the engine needs to handle the ball transfer `RB -> QB` without glitching the `Possession` mechanics.

### The Superior Synthesis

**The Definitive Architecture:**
We will implement a **Context-Aware Deception System**.

1. **Formation Matchups:** Success is heavily weighted by the defensive formation. (e.g., `Punt Block` = High Vulnerability to Pass, `Punt Return` = High Vulnerability to Run, `Safe` = Near Zero Success).
2. **Attribute Injection:** We use the _actual_ attributes of the specific players involved. `Punter.throwing_accuracy`, `Holder.speed`.
3. **"Confusion" Mechanic:** We calculate a `ConfusionScore` for the defense based on `(DeceptionAttr + CoachingTrickery) - (DefensiveAwareness + PrepTime)`. High confusion = delayed defender reaction times in the physics engine.
4. **Dynamic Cooldowns:** The "Surprise Factor" decays rapidly. Calling a trick play twice in a game applies a massive cumulative penalty to the confusion score.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Language:** Python 3.12 (Strict Typing)
- **Framework:** FastAPI / SQLAlchemy
- **Pattern:** Command Pattern for Play Execution, Strategy Pattern for Resolution.

### 2. The Data Schema

- **New Enums (`constants.py`):**
  - `PlayType.FAKE_PUNT_RUN`
  - `PlayType.FAKE_PUNT_PASS`
  - `PlayType.FAKE_FG_RUN`
  - `PlayType.FAKE_FG_PASS`
  - `PlayType.FLEA_FLICKER`
  - `PlayType.PHILLY_SPECIAL`
- **Config (`nfl_reference_data.py`):**
  - `TRICK_PLAY_TABLE`: Base success rates, counter-formations, and risk multipliers.

### 3. Step-by-Step Execution

#### Step 1: Foundation & Data Structures

- [ ] **1.1 Update Constants:** Define all new `PlayType` enums.
- [ ] **1.2 Reference Data:** Create the `TrickPlayConfiguration` class and populating `TRICK_PLAY_TABLE` with NFL-calibrated baselines (e.g., Fake Punt success ~40% vs Base, ~10% vs Safe).
- [ ] **1.3 Schema Checkbox:** Ensure `Player` model has accessors for out-of-position skills (e.g., `.throwing` for a Punter).

#### Step 2: The Core Resolution Logic (`play_resolver.py`)

- [ ] **2.1 The Dispatcher:** Add routing in `resolve_play()` to capture trick types.
- [ ] **2.2 The Confusion Engine:** Implement `_calculate_trick_play_confusion(offense, defense)`.
  - Formula: `(Coach.aggressiveness * 0.5 + Play.deception) - (Def.awareness * 1.2)`
- [ ] **2.3 Flea Flicker / Philly Special Logic:**
  - Implement multi-stage transfer logic. (Snap -> Hand -> Pitch -> Throw).
  - _Critical:_ Utilize existing `PassPlayPhysics` but with a modifier for "Defender Reaction Time" based on the Confusion Score.
- [ ] **2.4 Special Teams Fakes:**
  - `_resolve_fake_punt_run()`: Use Punter speed vs ST Tackling.
  - `_resolve_fake_punt_pass()`: Use Punter throw vs ST Coverage.

#### Step 3: AI & Decision Making (`coaching_ai.py`)

- [ ] **3.1 The Gambler's Logic:** Update `get_play_call` to check for "High Leverage" moments.
- [ ] **3.2 Context Limits:** Ensure AI _never_ calls Fake Punt inside their own 30 (unless losing late) and _never_ calls it if they are winning by 14+.
- [ ] **3.3 Anti-Cheese:** Implement `Team.trick_play_history` to track usage and apply the `DiminishingReturns` penalty.

#### Step 4: Narrative & Feedback

- [ ] **4.1 Play-by-Play Logs:** specialized commentary strings. "The Punter takes the snap... HE THROWS IT!"
- [ ] **4.2 Stat Tracking:** Ensure the Punter gets passing stats and the Holder gets rushing stats correctly.

### 4. Edge Cases & Error Handling

- [Case A: Null Attacker] -> Fallback to generic "Replacement Level" stats (Prevent crash if Punter object missing).
- [Case B: Physics Timeout] -> If multi-stage play takes too long (>10s), force "Sack" or "Tackle for Loss" to prevent infinite loop.
- [Case C: Attribute Missing] -> If Punter has no `throwing_accuracy`, default to `25` (very poor).

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** all new methods strictly typed.
- [ ] **Security:** N/A (Internal Logic), but ensure no negative stat overflows.
- [ ] **Performance:** Confusion calculation must be O(1), not O(N) recursion.
- [ ] **Balance Check:** Run 1,000 simulations of Fake Punts. Success rate should converge to Real-World NFL Average (~38-42%).
- [ ] **Logic Trap:** Ensure Flea Flicker doesn't count as _two_ plays or two passes in stats.

</final_audit>

---

<baton_handoff>
Next Immediate Step: **Implementation of Step 1: Foundation & Data Structures** -> Update `constants.py` and `nfl_reference_data.py`.
</baton_handoff>

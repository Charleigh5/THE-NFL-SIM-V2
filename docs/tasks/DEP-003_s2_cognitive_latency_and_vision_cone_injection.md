<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-003] S2 Cognitive Latency & Vision Cone Injection in PlayResolver

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** S2 Cognition testing in the NFL measures an athlete's visual processing speed, spatial awareness, and decision reaction latency under pressure.
- **Related Ideas:** OODA Loop (Observe, Orient, Decide, Act) time-slice modeling, Boydian fighter pilot reaction kinetics, behavior tree execution throttling.
- **Future Potential:** Real-time VR gaze tracking and 3D vision cone visualization in gridiron broadcasts.
- **Constraints:** Must integrate directly into `backend/app/orchestrator/play_resolver.py` without breaking deterministic 60Hz tick budget (<16ms per play resolution).
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Use a static random die roll or single rating threshold check (e.g. `if qb.football_iq > 80: complete_pass()`).

### Powerful Antithesis
Static threshold checks treat player cognition as a binary coin flip, ignoring pocket collapse timing, progressive read degradation, panic checkdowns, and defensive disguised coverages.

### The Superior Synthesis
Implement the continuous **S2 OODA Pipeline**:
1. Calculate quarterback base read latency:
   $$\Delta t_{read} = 150\text{ms} + (99 - \text{processing\_speed}) \cdot 3.5\text{ms}$$
2. Under pocket pressure ($\text{PressureLevel} > 0.6$), transition `CognitiveState` (`RELAXED` $\rightarrow$ `FOCUSED` $\rightarrow$ `STRESSED` $\rightarrow$ `PANICKED`).
3. Contract vision cone angle $\theta_{cone}$ from $120^\circ \rightarrow 45^\circ$, forcing tunnel vision and delayed progression from primary to secondary receivers.
4. Defensive DB/LB break-on-ball latency $\Delta t_{break}$ dynamically contests the window based on their respective S2 reaction times.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** FastAPI, Python 3.14 Dataclasses, Position Physics Vector2
- **Language:** Strict Python typing (100% type annotations)
- **State Management:** Immutable `OODAState` and `CognitiveProfile`

### 2. The Data Schema (Pre-Generation)
```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class CognitiveState(str, Enum):
    RELAXED = "RELAXED"
    FOCUSED = "FOCUSED"
    STRESSED = "STRESSED"
    PANICKED = "PANICKED"
    FLOW = "FLOW"

@dataclass(frozen=True)
class S2CognitionResult:
    qb_latency_ms: float
    vision_cone_degrees: float
    reads_completed: int
    forced_checkdown: bool
    db_break_latency_ms: float
    contested_window: bool
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Create `backend/app/engine/genesis/s2_evaluator.py` and unit test harness `backend/tests/unit/test_s2_cognition_integration.py`.
- [ ] **Step 2: Core Logic.** Hook `S2Evaluator.evaluate_pass_play_cognition()` into `PlayResolver._resolve_pass_play()`.
- [ ] **Step 3: Interface.** Include cognitive state metrics in `PlayResult` schema telemetry.

### 4. Edge Cases & Error Handling
- **Case A: Missing Player Cognitive Attributes** -> Derive graceful defaults from `awareness` and `football_iq`.
- **Case B: Pocket Collapses in < 1.2s** -> Force immediate `PANICKED` state and trigger scramble or throwaway evaluation.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Zero `Any` types, 100% type annotated signatures.
- [ ] **Security:** Pure function calculations, zero global side-effects.
- [ ] **Performance:** Execution latency < 0.5ms per play resolution step.
- [ ] **Self-Critique:** Verify that low-S2 QBs throw 25-35% more hurried interceptions under heavy blitzes without breaking baseline completion rates.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-004] 10x10 Turf Degradation Grid & Contact Physics.
</baton_handoff>

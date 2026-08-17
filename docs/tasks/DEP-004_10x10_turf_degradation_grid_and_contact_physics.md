<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-004] 10x10 Turf Degradation Grid & Contact Physics Loop

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Playing surfaces (Bermuda grass, FieldTurf, frozen dirt) wear unevenly over a 60-minute game, especially in the red zone and between the numbers, significantly altering traction and injury risk.
- **Related Ideas:** Micro-friction surface grids, finite-element terrain wear modeling, biomechanical shoe-surface traction studies.
- **Future Potential:** Real-time visual wear decals on 3D stadium meshes and dynamic cleat-changing halftime adjustments.
- **Constraints:** Grid resolution 10x10 zones across 100 yards, memory footprint < 100KB per game state, deterministic wear tracking.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Apply a static, stadium-wide weather penalty to all plays (e.g. `if rain: friction = 0.7`).

### Powerful Antithesis
Uniform stadium penalties fail to model why running inside the tackles in the 4th quarter on chewed-up grass creates slips and blown blocks, while outside boundary runs retain pristine turf grip.

### The Superior Synthesis
Implement the **10x10 Dynamic Turf Grid**:
1. Field partitioned into $10 \times 10$ coordinate zones $(X \in [0..9], Y \in [0..9])$.
2. Track cumulative mechanical work $W_{zone} += \sum \frac{1}{2} m v^2$ deposited by offensive/defensive linemen and ball carriers.
3. Compute dynamic friction coefficient:
   $$\mu_{effective} = \mu_{base} \cdot \left(1 - \alpha \cdot \frac{W_{zone}}{W_{max}}\right) \cdot \text{WeatherModifier}$$
4. Inject $\mu_{effective}$ into running back cut moves, wide receiver route breaks, and non-contact ligament strain equations.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** Python 3.14, NumPy / Pure Dataclass Matrix, Position Physics Vector2
- **Language:** Strict Python typing
- **State Management:** `TurfGridState` attached to `MatchContext`

### 2. The Data Schema (Pre-Generation)
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class TurfZone:
    zone_x: int  # 0-9 (longitudinal 10-yard buckets)
    zone_y: int  # 0-9 (lateral 5.33-yard buckets)
    wear_level: float = 0.0  # 0.0 (pristine) to 1.0 (destroyed)
    traction_coefficient: float = 0.85
    slip_risk_multiplier: float = 1.0
    divot_count: int = 0

@dataclass
class TurfGridState:
    stadium_id: str
    surface_type: str  # "NATURAL_GRASS", "FIELDTURF", etc.
    zones: List[List[TurfZone]] = field(default_factory=list)
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Connect `backend/app/engine/hive/turf_grid.py` with `backend/app/engine/position_physics.py`.
- [ ] **Step 2: Core Logic.** Update `PlayResolver` to register contact location $(X, Y)$, apply zone wear, and fetch localized $\mu_{effective}$ for route cuts and tackle collisions.
- [ ] **Step 3: Interface.** Expose 10x10 wear matrix in game telemetry API payload for frontend heatmap rendering.

### 4. Edge Cases & Error Handling
- **Case A: Out of bounds plays** -> Clamp coordinate lookups safely to zone boundary $[0..9]$.
- **Case B: Extreme mud/frozen turf** -> Impose a hard minimum friction floor ($\mu_{min} = 0.40$) to prevent game engine deadlock.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Zero `Any` types, strict bounds validation.
- [ ] **Security:** In-memory grid mutation scoped purely to active game instance.
- [ ] **Performance:** Zone lookup and wear update < 0.1ms per play.
- [ ] **Self-Critique:** Verify that high-traffic hash marks exhibit 3x faster wear degradation than sideline zones across 100 simulated offensive plays.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-005] Cryptographic Replay Verification API.
</baton_handoff>

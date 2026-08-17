<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-005] Cryptographic Replay Verification API

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Provably fair cryptographic algorithms (used in high-stakes online gaming and blockchain oracles) enable client-side mathematical verification of server-simulated outcomes.
- **Related Ideas:** HMAC-SHA256 seed commit-reveal schemes, deterministic state-machine replication, esports anti-cheat verifiers.
- **Future Potential:** Competitive online multi-franchise leagues with immutable match dispute arbitration and zero-knowledge replay proofs.
- **Constraints:** Python `hashlib` HMAC-SHA256 CSPRNG, sub-millisecond seed hashing, 100% deterministic bit-for-bit replay replication.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Rely on standard Python `random.seed(x)` or trust server-side database logs without client-side cryptographic verification.

### Powerful Antithesis
`random.seed()` is non-cryptographic, varies across Python versions / platforms, and lacks commit-reveal tamper resistance, allowing rogue client/server tampering.

### The Superior Synthesis
Implement the **Provably Fair Commit-Reveal Harness**:
1. **Pre-Game**: Server generates `server_seed` (32 cryptographically random bytes) and publishes commitment $H = \text{SHA256}(\text{server\_seed})$.
2. **Game Play**: Simulation runs driven by HMAC-SHA256:
   $$\text{Entropy}_{\text{nonce}} = \text{HMAC-SHA256}(\text{server\_seed}, \text{client\_seed} \,\|\, \text{nonce})$$
3. **Post-Game**: Server reveals `server_seed`. Client or third-party verifier hits `POST /api/v1/simulation/verify-replay`, re-running the exact play trajectory in an isolated sandbox to confirm $H$ and match outcome match 100%.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** FastAPI, Pydantic v2, Python `hashlib` & `struct`
- **Language:** Strict Python typing
- **State Management:** `DeterministicRNG` from `backend/app/engine/core/deterministic_rng.py`

### 2. The Data Schema (Pre-Generation)
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ReplayVerificationRequest(BaseModel):
    game_id: str
    server_seed: str = Field(..., description="Hex-encoded revealed server seed")
    server_seed_hash: str = Field(..., description="Original published SHA256 commitment")
    client_seed: str = Field(..., description="Client seed string")
    total_plays: int
    expected_final_score: Dict[str, int]
    action_log: List[Dict[str, Any]]

class ReplayVerificationResponse(BaseModel):
    is_valid: bool
    server_seed_matched: bool
    simulation_diverged_at_play: int | None = None
    replay_final_score: Dict[str, int]
    verification_hash: str
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Create `backend/tests/unit/test_replay_verification_api.py`.
- [ ] **Step 2: Core Logic.** Implement `ReplayVerificationService` invoking `DeterministicRNG` replay loop.
- [ ] **Step 3: Interface.** Add route `POST /api/v1/simulation/verify-replay` in `backend/app/api/endpoints/simulation.py`.

### 4. Edge Cases & Error Handling
- **Case A: Corrupted Server Seed Hash** -> Return `is_valid: False` with `ERR_COMMITMENT_MISMATCH`.
- **Case B: Mid-game Nonce Desynchronization** -> Isolate first play index where floating-point RNG diverged.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Verified Pydantic v2 schemas and exact return types.
- [ ] **Security:** Sandbox execution prevents arbitrary code execution; rate-limited endpoint.
- [ ] **Performance:** 100-play game replay verification completes in < 25ms.
- [ ] **Self-Critique:** Ensure floating-point rounding is clamped to 6 decimal precision across platforms.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-006] Monte Carlo Statistical Calibration Engine.
</baton_handoff>

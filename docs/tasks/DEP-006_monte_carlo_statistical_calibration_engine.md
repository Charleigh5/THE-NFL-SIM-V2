<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: [DEP-006] Monte Carlo Statistical Calibration Engine & Benchmark Suite

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** Sports simulation game design requires empirical validation against real-world statistical benchmarks (NextGenStats, Pro-Football-Reference) to ensure emergent physics match reality.
- **Related Ideas:** Monte Carlo batch runs, Chi-Square goodness-of-fit tests, automated regression calibration harnesses.
- **Future Potential:** Self-calibrating physics hyperparameters using Bayesian optimization over 100,000 game runs.
- **Constraints:** Must benchmark against `NFL Simulation Engine Implementation Data Table - Table 1.csv` within 95% confidence intervals.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Manually eyeball individual game box scores or run 1-2 test games to check if scoring looks reasonable.

### Powerful Antithesis
Small sample sizes hide massive systemic biases (e.g. sack rate creeping up to 12%, explosive run rate dropping to 0.5%, or completion percentages drifting above 75%).

### The Superior Synthesis
Build an automated **1,000-Game Monte Carlo Calibration Engine**:
1. Run headless multi-threaded batches of 1,000 full NFL games.
2. Aggregate league-wide macro statistics and evaluate against ground truth:
   - **Sack Rate**: Ground Truth $6.5\%$ (Tolerance $\pm 0.6\%$)
   - **Yards Per Carry**: Ground Truth $4.2$ (Tolerance $\pm 0.3$)
   - **Pass Completion %**: Ground Truth $64.5\%$ (Tolerance $\pm 2.5\%$)
   - **Turnovers Per Game**: Ground Truth $1.3$ (Tolerance $\pm 0.3$)
   - **Points Per Game**: Ground Truth $21.8$ (Tolerance $\pm 2.0$)
3. Automatically fail the CI build if any macro distribution drifts outside the 95% confidence bounds.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** Python 3.14, Polars / Pandas, SciPy Statistical Tests
- **Language:** Strict Python typing
- **State Management:** Isolated in-memory `SimulationOrchestrator` instances

### 2. The Data Schema (Pre-Generation)
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class MetricCalibrationResult:
    metric_name: str
    target_value: float
    observed_mean: float
    standard_deviation: float
    p_value: float
    is_calibrated: bool

@dataclass
class CalibrationReport:
    total_games: int
    total_plays: int
    elapsed_seconds: float
    metrics: Dict[str, MetricCalibrationResult]
    passed_all_gates: bool
```

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Create `scripts/batch_simulator.py` and `tests/benchmarks/test_nfl_statistical_calibration.py`.
- [ ] **Step 2: Core Logic.** Implement multi-threaded headless runner with aggregate metric accumulator.
- [ ] **Step 3: Interface.** Output Markdown summary report and ASCII distribution histogram.

### 4. Edge Cases & Error Handling
- **Case A: Outlier Blowout Game (e.g. 70-0 score)** -> Validate that extreme tails occur at realistic NFL frequencies (< 0.1%).
- **Case B: Thread Race Condition** -> Use thread-local RNG states and lock-free metric accumulators.
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Verified clean type signatures and Polars aggregation queries.
- [ ] **Security:** Benchmarks run fully offline in sandbox mode.
- [ ] **Performance:** 1,000 game simulation batch completes in < 30 seconds on local multi-core CPU.
- [ ] **Self-Critique:** Confirm all calibration thresholds match `NFL Simulation Engine Implementation Data Table - Table 1.csv`.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to [DEP-007] Frontend Gridiron Heatmap & Playwright E2E Suite.
</baton_handoff>

# Master Full-Scope Implementation Task List: The Digital Gridiron (V2)

**PROJECT:** THE-NFL-SIM-V2 (The Digital Gridiron / Cortex NFL Sim)  
**STATUS:** ACTIVE EXECUTION  
**GOVERNANCE:** Conforms to `.agent/rules/app-master.md`, `.agent/rules/task-list-template.md`, and `.agent/rules/frontend-backend-task-gen.md`.

---

## 🗺️ Master Dependency Index

| Task ID | Task Title | Subsystem | Target Files | Specification File |
| :--- | :--- | :--- | :--- | :--- |
| **DEP-001** | Operator Registry & Codex Ingestion | Codex Governance | `~/.codex/skills/cweir-operator-preferences/` | [DEP-001 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-001_operator_registry_and_codex_ingestion.md) |
| **DEP-002** | Agent Workflow Integration (`/codex-pipeline`) | Workflow Engine | `.agent/workflows/codex-pipeline.md` | [DEP-002 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-002_agent_workflow_integration.md) |
| **DEP-003** | S2 Cognitive Latency & Vision Cone Injection | `GENESIS` Engine | `backend/app/orchestrator/play_resolver.py` | [DEP-003 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-003_s2_cognitive_latency_and_vision_cone_injection.md) |
| **DEP-004** | 10x10 Turf Degradation Grid & Contact Physics | `HIVE` Engine | `backend/app/engine/hive/turf_grid.py` | [DEP-004 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-004_10x10_turf_degradation_grid_and_contact_physics.md) |
| **DEP-005** | Cryptographic Replay Verification API | `CORE` Engine | `backend/app/api/endpoints/simulation.py` | [DEP-005 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-005_cryptographic_replay_verification_api.md) |
| **DEP-006** | Monte Carlo Statistical Calibration Engine | Telemetry & QA | `scripts/batch_simulator.py` | [DEP-006 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-006_monte_carlo_statistical_calibration_engine.md) |
| **DEP-007** | Frontend Gridiron Heatmap & Playwright E2E Suite | UI / Presentation | `frontend/src/components/GridironVisualizer.tsx` | [DEP-007 Spec](file:///C:/Users/cweir/.gemini/antigravity/worktrees/THE-NFL-SIM-V2/codex_integration_research_plan/docs/tasks/DEP-007_frontend_gridiron_heatmap_and_playwright_e2e_suite.md) |

---

## Task Specifications (Consolidated Archive)

### [DEP-001] Operator Registry & Codex Ingestion
- **Conceptual Mapping:** Ingests the 6-stage lifecycle into global operator registers.
- **Superior Synthesis:** Locks persistent memory and avoids context drift during autonomous multi-agent sessions.
- **Verification:** Fast <5ms load time with zero credential exposure.

### [DEP-002] Agent Workflow Integration
- **Conceptual Mapping:** Maps slash command `/codex-pipeline` to `scripts/codex_pipeline_runner.py`.
- **Superior Synthesis:** Enables single-command autonomous task generation, testing, and dossier updating.
- **Verification:** Non-interactive execution with automatic error stack trace capture.

### [DEP-003] S2 Cognitive Latency & Vision Cone Injection
- **Conceptual Mapping:** Models OODA-loop visual processing speed and decision latency under pass rush pressure.
- **Superior Synthesis:** Mathematical OODA progression pipeline ($\Delta t_{read} = 150\text{ms} + (99 - \text{processing\_speed}) \cdot 3.5\text{ms}$) with dynamic vision cone contraction ($120^\circ \rightarrow 45^\circ$).
- **Verification:** Low-S2 QBs exhibit 25-35% higher hurried INTs under heavy pressure.

### [DEP-004] 10x10 Turf Degradation Grid & Contact Physics
- **Conceptual Mapping:** Tracks surface wear across 10x10 field coordinate zones.
- **Superior Synthesis:** Cumulative kinetic energy wear reduces localized friction $\mu \in [0.45, 0.85]$, dynamically driving cut slips and non-contact injury risks.
- **Verification:** High-traffic hash marks exhibit 3x higher wear than sideline boundaries.

### [DEP-005] Cryptographic Replay Verification API
- **Conceptual Mapping:** Client-side mathematical verification of match outcomes.
- **Superior Synthesis:** HMAC-SHA256 commit-reveal CSPRNG architecture with bit-for-bit replay replication.
- **Verification:** `POST /api/v1/simulation/verify-replay` executes in < 25ms.

### [DEP-006] Monte Carlo Statistical Calibration Engine
- **Conceptual Mapping:** Empirical statistical calibration against real-world NFL distributions.
- **Superior Synthesis:** 1,000-game headless batches validating sack rates (~6.5%), YPC (~4.2), and completion rates (~64.5%) against `NFL Simulation Engine Implementation Data Table - Table 1.csv`.
- **Verification:** 1,000 game simulation completes in < 30 seconds.

### [DEP-007] Frontend Gridiron Heatmap & Playwright E2E Suite
- **Conceptual Mapping:** Live gridiron visual telemetry and full browser end-to-end testing.
- **Superior Synthesis:** CAD-grade high-density monograph UI canvas with live turf wear heatmaps and automated Playwright test suite for Draft, Medical, and Simulation user flows.
- **Verification:** 100% passing Playwright journeys with 60fps canvas performance.

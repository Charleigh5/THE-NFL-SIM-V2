# Original User Request

## Follow-up — 2026-08-24T23:47:08-04:00

Architect and implement a production-grade, 3-tier hybrid intelligence system for THE-NFL-SIM-V2 ("The Digital Gridiron") that unifies deterministic physics/mathematical engines (Tier 0), low-latency edge/Flash-tier narrative generators (Tier 1), and deep strategic multi-agent reasoning models (Tier 2) with zero-cost offline fallbacks.

Working directory: backend/app/services/ai

## Requirements

### R1. Deterministic Core Enforcement & Boundary Hardening (Tier 0)
Formalize strict non-LLM boundaries for trench physics, S2 reaction timing, salary cap amortization, Jimmy Johnson pick valuation, and 18-week schedule/playoff tiebreaker logic. Guarantee sub-millisecond execution and exact mathematical invariants with zero external API calls.

### R2. Low-Latency Narrative & Broadcast Generation Engine (Tier 1)
Implement async, structured JSON generators for live play-by-play color commentary across 4 broadcast styles (ESPN, CBS, FOX, NFL Network), draft prospect scouting profiles with pro comparisons, weekly news wire wrap-up recaps, and dynamic locker room storyline events. Support both cloud Flash models and local SLMs (e.g. Qwen2.5/Llama-3.2) with deterministic offline fallback templates.

### R3. Autonomous Multi-Agent Strategy & GM Game-Theoretic Negotiation (Tier 2)
Build deep reasoning services for autonomous AI General Managers to evaluate multi-player/pick trades across 3-year cap horizons, formulate opponent-specific tactical gameplans from box score tape, and dynamically steer Draft War Room panic/reach logic under imperfect information.

### R4. Provider-Agnostic LLM Adapter & Resilient Fallback Harness
Construct a unified AI provider interface supporting Google GenAI / Vertex AI, OpenAI/Anthropic-compatible endpoints, and local Ollama/vLLM backends with automated Pydantic V2 schema validation, in-memory caching, and seamless offline degradation when no API keys are present.

## Acceptance Criteria

### Engine Integrity & Performance
- [ ] 100% of core simulation plays resolve in <1.0ms without external network or LLM dependencies.
- [ ] Tier 1 narrative requests complete in <200ms (cloud) or with instant offline cached template fallbacks.
- [ ] Full backend test suite passes with 100% success rate (`pytest backend/tests/unit`).
- [ ] Frontend production build compiles with 0 errors (`npm run build`).

### Strategic & Contract Quality
- [ ] AI GM trade evaluation correctly factors 3-year cap projections, draft capital equity, and franchise rebuild status.
- [ ] Pydantic V2 schemas enforce strict structured output with zero raw unformatted string leaks.
- [ ] Comprehensive documentation and task specification authored in `docs/tasks/TASK-005_HYBRID_INTELLIGENCE_ARCHITECTURE.md`.

## Follow-up — 2026-09-06T03:27:53Z

Execute the 5-Pillar Architectural Review & Optimization Framework across four core subsystems in THE-NFL-SIM-V2: Free Agency Market & Contract Bidding Hub (TASK-010), Locker Room & Closed-Door Council UI (TASK-011), Medical Center Live Roster & Surgical Triage Integration (TASK-012), and In-Game Play-Calling HUD (TASK-013). Verify system health through automated static contract gates, operational latency benchmarks, domain boundary continuity, and empirical NFL statistical validation.

Requested team: Full Team: Decompose into parallel specialist tracks (Contract/Capology, Frontend UI Virtualization, Physics/HUD Telemetry, QA/Validation)

Working directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2
Integrity mode: demo

## Requirements

### R1. Type and Contract Parity Gate
Eliminate schema and naming drift between the FastAPI/Pydantic V2 backend and the React/TypeScript frontend. Disallow `any` types in TypeScript code. Validate that all API payloads and WebSocket frame schemas share strict 1:1 parity and discriminated unions across boundaries.

### R2. Subsystem Delivery and Integration
Implement and wire the full-stack features for the four target sprint modules:
1. **Interactive Free Agency Market (TASK-010)**: Real-time contract negotiations with NFL CBA-compliant signing bonus proration, post-June 1st cap splits, top-51 offseason rule, and multi-team concurrent AI GM bidding.
2. **Locker Room & Closed-Door Council UI (TASK-011)**: Deterministic Tier 1 locker-room morale/chemistry differential equations, council narrative events, and team dynamic telemetry.
3. **Medical Center & Surgical Triage (TASK-012)**: Anatomical injury triage, surgery vs. rehab decision paths, body health state transitions, and roster status synchronization.
4. **In-Game Play-Calling HUD (TASK-013)**: Interactive play-calling interface operational during 60Hz live physics simulation, integrated with Ben Baldwin 4th-down decision modeling (Go/Punt/FG).

### R3. Latency Budgets & UI Rendering Performance
Maintain strict operational performance thresholds:
- Live physics and telemetry frame delivery: <16ms (60 FPS)
- Capology multi-year proration and AI GM bidding resolution: <40ms
- Table and roster rendering for 1,500+ free agents and 53-man rosters: 60 FPS without frame drops, using virtualized list rendering
- 4th-down decision recommendation lookups: <10ms
- Locker room society chemistry evaluation: <2ms per team

### R4. Domain Boundary Continuity and Statistical Calibration
Ensure state mutations in one domain (e.g. physics injury, contract signing, morale shift) propagate through broadcast, dynasty, and medical layers to the UI without loss or desynchronization. Ensure Monte Carlo simulation outputs align with official NFL statistical distributions (yards per carry, pass completion rate, sack rate, and injury incidence).

### R5. Architecture Records & Living System Dossiers
Document architectural trade-offs in formal Architecture Decision Records (ADRs) within `docs/decisions/`. Update `docs/FEATURE_STATUS_MATRIX.md` to reflect production readiness, and synchronize `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` with all player mechanic and injury state updates.

## Verification Resources

- Type & Schema Parity: `python scripts/verify_blueprint_contracts.py` and `python scripts/check_field_parity.py`
- Frontend Compilation & Typecheck: `npm --prefix frontend run build`
- Cross-Domain Pipeline Continuity: `python scripts/test_domain_boundary_pipeline.py`
- Statistical Calibration Suite: `python scripts/batch_simulator.py --games 100 --calibrate` and `python backend/scripts/run_statistical_validation.py`
- Performance & Latency Harness: `python backend/scripts/benchmark_mcp.py` and `python backend/scripts/load_test.py`
- End-to-End User Flow Tests: `npx playwright test`

## Acceptance Criteria

### Contract & Compilation
- [ ] `python scripts/verify_blueprint_contracts.py` passes with zero contract mismatches or schema discrepancies.
- [ ] `npm --prefix frontend run build` compiles with zero TypeScript errors under strict mode.

### Domain Boundary Continuity
- [ ] `python scripts/test_domain_boundary_pipeline.py` succeeds across all domain boundaries (Physics -> Broadcast -> Medical -> WebSocket Frame).

### Latency Budgets
- [ ] `python backend/scripts/benchmark_mcp.py` passes with all tested subsystems operating strictly within latency ceilings (<16ms telemetry, <40ms capology, <2ms society math).
- [ ] Roster and Free Agency views render with virtualized scrolling at a stable 60 FPS with >1,000 player records.

### Statistical Realism
- [ ] `python scripts/batch_simulator.py --games 100 --calibrate` produces game stats conforming to NFL reference distribution bounds (YPC 4.1-4.4, Pass Completion 63.5-66.0%, Sack Rate 6.0-7.2%).

### Documentation & Dossier Sync
- [ ] New ADRs are recorded in `docs/decisions/` covering major architectural design choices.
- [ ] `docs/FEATURE_STATUS_MATRIX.md` reflects updated status for TASK-010 through TASK-013.
- [ ] `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` is updated and synchronized with implemented mechanics.

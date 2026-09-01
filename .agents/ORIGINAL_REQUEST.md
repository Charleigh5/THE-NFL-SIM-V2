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

## 2026-08-25T03:47:40Z

You are the Project Orchestrator for THE-NFL-SIM-V2 ("The Digital Gridiron").

Your working directory is:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_hybrid_ai`

Please initialize and maintain your `BRIEFING.md` and `progress.md` inside your working directory.

The original user request is recorded in:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md` and `.agents\ORIGINAL_REQUEST.md`

## Mission & Requirements

Architect and implement a production-grade, 3-tier hybrid intelligence system for THE-NFL-SIM-V2 ("The Digital Gridiron") that unifies deterministic physics/mathematical engines (Tier 0), low-latency edge/Flash-tier narrative generators (Tier 1), and deep strategic multi-agent reasoning models (Tier 2) with zero-cost offline fallbacks.

Working directory for feature implementation: `backend/app/services/ai`

### R1. Deterministic Core Enforcement & Boundary Hardening (Tier 0)
Formalize strict non-LLM boundaries for trench physics, S2 reaction timing, salary cap amortization, Jimmy Johnson pick valuation, and 18-week schedule/playoff tiebreaker logic. Guarantee sub-millisecond execution and exact mathematical invariants with zero external API calls.

### R2. Low-Latency Narrative & Broadcast Generation Engine (Tier 1)
Implement async, structured JSON generators for live play-by-play color commentary across 4 broadcast styles (ESPN, CBS, FOX, NFL Network), draft prospect scouting profiles with pro comparisons, weekly news wire wrap-up recaps, and dynamic locker room storyline events. Support both cloud Flash models and local SLMs (e.g. Qwen2.5/Llama-3.2) with deterministic offline fallback templates.

### R3. Autonomous Multi-Agent Strategy & GM Game-Theoretic Negotiation (Tier 2)
Build deep reasoning services for autonomous AI General Managers to evaluate multi-player/pick trades across 3-year cap horizons, formulate opponent-specific tactical gameplans from box score tape, and dynamically steer Draft War Room panic/reach logic under imperfect information.

### R4. Provider-Agnostic LLM Adapter & Resilient Fallback Harness
Construct a unified AI provider interface supporting Google GenAI / Vertex AI, OpenAI/Anthropic-compatible endpoints, and local Ollama/vLLM backends with automated Pydantic V2 schema validation, in-memory caching, and seamless offline degradation when no API keys are present.

## Acceptance Criteria
- [ ] 100% of core simulation plays resolve in <1.0ms without external network or LLM dependencies.
- [ ] Tier 1 narrative requests complete in <200ms (cloud) or with instant offline cached template fallbacks.
- [ ] Full backend test suite passes with 100% success rate (`pytest backend/tests/unit`).
- [ ] Frontend production build compiles with 0 errors (`npm run build`).
- [ ] AI GM trade evaluation correctly factors 3-year cap projections, draft capital equity, and franchise rebuild status.
- [ ] Pydantic V2 schemas enforce strict structured output with zero raw unformatted string leaks.
- [ ] Comprehensive documentation and task specification authored in `docs/tasks/TASK-005_HYBRID_INTELLIGENCE_ARCHITECTURE.md` complying strictly with `.agent/rules/task-list-template.md`.

## Execution Standards
- Decompose the work into logical milestones and dispatch to specialized worker subagents.
- Verify every milestone with tests and adversarial verification.
- Adhere strictly to user governance rules (app-master.md, AGENTS.md, task-list-template.md).
- When all requirements and acceptance criteria are completely satisfied and verified, report completion back to the Sentinel.

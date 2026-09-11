# ADR-006: Locker Room Society Engine & 3-Tier Multi-Agent Council Synthesis

**Status**: Accepted
**Date**: 2026-09-06
**Decision Makers**: Society Engine Architect, AI Systems Lead, QA Specialist
**Supersedes**: N/A

---

## Context

Professional football teams are fragile human ecosystems. Interpersonal friction, play-calling dissatisfaction, contract disputes, losing streaks, and ego clashes directly influence team performance. In sports simulation engines, modeling this dynamic has historically suffered from two extremes:
1. **Shallow Static Morale**: A single integer morale slider that fluctuates trivially with wins/losses, offering zero narrative immersion or behavioral nuance.
2. **Costly Unbounded LLM Calls**: Invoking large language models for 53 players every week generates unacceptably high API latency (>10 seconds per team), exorbitant cloud inference costs, and frequent rate-limiting failures during background season simulation.

We required an architecture that delivers **instantaneous deterministic calculations** for weekly roster evaluations (<2.0ms per team) while generating **cinematic, high-stakes narrative drama** only when critical psychological breaking points are reached, backed by 100% resilient offline fallback templates.

---

## Decision

We designed and implemented a **3-Tier Hierarchical Society Engine Architecture**:

```
[ Tier 1: Deterministic Differential Equations ] -> Evaluates 53-man roster weekly (<2ms)
                    |
                    v (Tension >= 75.0 Threshold Gate)
[ Tier 2: Event Activation Gating ] -------------> Triggers Closed-Door Council Incident
                    |
                    v
[ Tier 3: Agentic Council Synthesis ] -----------> 3-Way Confrontation Dialogue (LLM / SLM)
                    |                              (With 100% Deterministic Offline Fallback)
                    v
[ User Executive Resolution ] -------------------> Mutates Morale, Coach Trust, & Team Chemistry
```

### 1. Tier 1: Deterministic Differential Equations (`TensionEngine`)
- Evaluates individual player psychological state deltas each week using the **Big Six Psychological DNA**:
  - `ego` (0-100): Amplifies snap share frustration and target demands.
  - `greed` (0-100): Drives contract dispute escalation when outplaying salary.
  - `loyalty` (0-100): Buffers coach trust erosion during losing streaks.
  - `resilience` (0-100): Dampens negative tension accumulation from adverse game events.
  - `paranoia` (0-100): Magnifies panic from benching or trade rumors.
  - `professionalism` (0-100): Accelerates natural weekly tension decay toward baseline.
- Calculates weekly tension drivers:
  - `BENCHED_STAR_RESENTMENT`: Star players ($OVR \ge 80$) playing $<25\%$ snaps.
  - `PASS_RUSH_CRITIQUE` & `TURNOVER_BLAME`: Offensive linemen and skill players reacting to QB sacks taken and turnovers.
  - `LOSING_STREAK_APATHY`: Compounding friction scaled by loss streak and paranoia.
  - `VICTORY_DECAY`: Weekly tension relief and morale recovery on wins.
- Sub-2ms execution guarantee: Roster batch evaluation (`evaluate_roster_weekly`) executes in ~0.35ms for all 53 players.

### 2. Tier 2: Activation Gating Threshold
- A dramatic locker room crisis is triggered **only** when a player's calculated `tension_score` meets or exceeds **75.0**.
- Filters out non-critical fluctuations, ensuring that heavy narrative generation is invoked only when genuine structural conflict exists.

### 3. Tier 3: Multi-Agent Closed-Door Council & Offline Fallback
- Orchestrated in `locker_room_agent.py` and visualised in `ClosedDoorCouncilModal.tsx`.
- Generates an authentic 3-way multi-agent confrontation between:
  1. `disgruntled_star`: The aggrieved player demanding immediate accountability or usage.
  2. `team_captain`: The veteran locker room leader defending team unity and culture.
  3. `head_coach`: The authority figure managing team discipline and strategic balance.
- **Resilient Offline Fallback**: If external LLM APIs are unavailable, disabled, or unconfigured, the system immediately falls back to structured, deterministic scenario templates ensuring zero downtime and 100% offline functionality.
- **4 Executive Resolution Pathways**:
  1. `promise_usage`: Commit to scripted early touches (+Usage, +Player Morale, slight HC Authority drop).
  2. `demand_accountability`: Enforce coaching discipline (+HC Authority, risk of trade request if player ego is high).
  3. `players_meeting`: Mandate a closed-door players-only summit (Captain resolves, +Team Chemistry).
  4. `explore_trade`: Authorize the Front Office to field trade calls (Player removed from conflict, tension reset).

---

## Rationale

1. **Strict Operational Efficiency**: Evaluating 32 NFL teams (1,696 players) takes less than 15ms total, allowing rapid multi-week simulation without CPU bottlenecks.
2. **Emergent Storytelling**: High-ego wide receivers demand targets; aging veterans resent benchings; struggling quarterbacks lose offensive line trust. Stories emerge naturally from the simulation math.
3. **Player Agency**: The user is placed in the coach/GM hot seat to make difficult cultural and strategic decisions that have lasting gameplay consequences.
4. **Zero-Failure Architecture**: The offline deterministic fallback ensures that gameplay, tests, and CI/CD never break due to network or third-party AI outages.

---

## Consequences

### Positive Consequences
- **Ultra-Low Latency**: Roster evaluation averages 0.358ms (well beneath the 2.00ms budget).
- **Immersion & Drama**: Cinematic 3-way dialogue with rich character archetypes and dynamic tension gauges.
- **Reliability**: 100% offline fallback guarantees system operates in any environment.
- **Data Integrity**: State mutations cleanly propagate to `Player.tension_score`, `Player.morale`, `trust_in_coach`, and `trust_in_qb`.

### Negative Consequences / Trade-offs
- **State Complexity**: Requires tracking psychological DNA and rolling weekly snap/target stats across all rostered athletes.
- **Balancing Requirements**: Tension accumulation and decay rates must be calibrated to avoid perpetual locker room revolts or complete apathy.

---

## Alternatives Considered

1. **Pure LLM Prompts on Every Game Week**:
   - *Description*: Ask an LLM to evaluate every player's feelings after each game.
   - *Reason for Rejection*: Infeasible latency (>30s per week) and thousands of dollars in token costs.
2. **Static Morale Points (+/- 2 on win/loss)**:
   - *Description*: Traditional simplistic sports video game morale system.
   - *Reason for Rejection*: Fails to deliver emergent narratives or reflect real NFL locker room dynamics.

---

## Validation Criteria

- `python backend/scripts/benchmark_operational_latencies.py`: Subsystem 4 (Society Chemistry 53-Man Evaluation) executes in ~0.36ms (ceiling <2.00ms).
- `pytest backend/tests/unit/test_tension_engine.py backend/tests/unit/test_locker_room_agent.py`: 100% pass rate across 35 unit tests.
- `npm --prefix frontend run build`: Zero TypeScript errors in `LockerRoom.tsx`, `ClosedDoorCouncilModal.tsx`, and `LockerRoomTelemetry.tsx`.

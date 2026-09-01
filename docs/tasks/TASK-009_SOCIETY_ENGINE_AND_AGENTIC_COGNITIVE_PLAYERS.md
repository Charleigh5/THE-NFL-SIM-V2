<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
Guidelines: Karpathy simplicity-first, surgical containment, zero speculative abstractions.
</system_context>

# TASK: TASK-009: Society Engine Tier 1-3 (Psychological DNA, Mathematical Tension Engine & Agentic Locker Room Service)

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Traditional sports simulations (Football Manager, Madden Franchise, Dwarf Fortress) often reduce locker rooms to static "morale" integer counters from 0 to 100.
  - In real NFL dynamics, players possess complex psychological profiles: undrafted players play with a chip on their shoulder, veteran wide receivers demand target volume in contract years, and locker rooms fracture along social clique and position group fault lines.
- **Related Ideas:**
  - **Cognitive Vector Modeling:** Big-Five personality traits adapted for elite professional athletics (`Ego`, `Greed`, `Loyalty`, `Resilience`, `Paranoia`, `Professionalism`).
  - **Stress-Accumulation Differential Equations:** State-based tension growth driven by playing time, target share, contract year status, and team winning percentage.
  - **Single-Turn Multi-Agent Dialogue Synthesis:** Batched LLM orchestration where 2-5 active agents with opposing motivations interact in a single structured prompt (HBO *Hard Knocks* dynamic).
- **Future Potential (2026/2027):**
  - Continuous long-term memory integration via vector memory stores (Mem0 / SQLite-vec).
  - Autonomous dynamic social media sentiment engine simulating beat reporter leaks, podcast clips, and fan reaction.
- **Constraints:**
  - Zero `any` types across Python and TypeScript contracts.
  - 0ms inference overhead for standard weekly game resolution (Tier 1 is 100% deterministic math).
  - Max 1 LLM call per team per week, triggered ONLY if active agent tension exceeds the activation threshold ($\text{Tension} \ge 75.0$).
  - Zero disruption to existing 1,482 passing backend tests and 21 domain parity models.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Create a separate autonomous AI agent instance for all 53 players on the active roster, calling an LLM endpoint sequentially for each player every week to determine their thoughts, media statements, and trade desires.

### Powerful Antithesis
- **Catastrophic Failure Modes:**
  1. **Latency Explosion:** 53 LLM calls $\times$ 32 teams = 1,696 LLM calls per week. Advancing a single week would take 5 to 10 minutes and blow past rate limits.
  2. **Hallucination & Personality Drift:** Without strict mathematical anchor states, independent LLM instances hallucinate contradictory events (e.g., claiming they played when benched).
  3. **Loss of Determinism:** Random LLM outputs break reproducible season simulation benchmarks and replay verification.
  4. **Cost & Infrastructure Overhead:** Thousands of unnecessary tokens spent on third-string special teamers who had uneventful weeks.

### The Superior Synthesis
- **The 3-Tier Cognitive Hierarchical Engine:**
  1. **Tier 1 (Deterministic Micro-State Accumulator - 0ms):** Evaluates all 1,696 players league-wide using pure mathematical differential equations. Updates `tension_score`, `morale`, `trust_in_coach`, and `trust_in_qb` based on game stats, target share, snap counts, and psychological DNA.
  2. **Tier 2 (Event-Driven Activation Gate):** Filters the roster to identify only the top 1–3 "Active Grievance Actors" whose tension crosses the threshold ($\text{Tension} \ge 75$).
  3. **Tier 3 (Batched Locker Room Council Agent):** When (and only when) active actors exist, passes the active players + team captain + head coach context into a single structured prompt (using Gemini Flash / local SLM) to generate realistic dialogue, locker room consequences, and actionable choices for the user in $<500\text{ms}$.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend:** Python 3.11+ / FastAPI / SQLAlchemy 2.0 (Mapped Column typing) / Pydantic v2
- **Simulation Engine:** `backend/app/engine/society/`
- **Testing:** `pytest` unit test suite with deterministic seed fixtures

### 2. The Data Schema (Pre-Generation)

#### 2.1 Database Model Modifications (`backend/app/models/player.py`)
```python
# Added to Player class:
psychological_dna: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
backstory: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)
tension_score: Mapped[float] = mapped_column(Float, default=0.0)
morale: Mapped[int] = mapped_column(Integer, default=80)
trust_in_coach: Mapped[int] = mapped_column(Integer, default=80)
trust_in_qb: Mapped[int] = mapped_column(Integer, default=80)
```

#### 2.2 Domain Contracts & Pydantic Types (`backend/app/engine/domain_contracts.py` & `schemas`)
```python
class PsychologicalDNA(BaseModel):
    ego: int = Field(default=50, ge=0, le=100)
    greed: int = Field(default=50, ge=0, le=100)
    loyalty: int = Field(default=50, ge=0, le=100)
    resilience: int = Field(default=50, ge=0, le=100)
    paranoia: int = Field(default=50, ge=0, le=100)
    professionalism: int = Field(default=50, ge=0, le=100)

class PlayerBackstory(BaseModel):
    origin: str = ""
    financial_motive: str = ""
    career_milestone: str = ""
    draft_narrative: str = ""
    mentor_id: Optional[int] = None
    rival_id: Optional[int] = None

class TensionDelta(BaseModel):
    player_id: int
    prior_tension: float
    new_tension: float
    primary_driver: str
    morale_delta: int
    is_active_grievance: bool
```

### 3. Step-by-Step Execution

- [ ] **Step 1: Database Model & Migration Scaffolding**
  - Update `backend/app/models/player.py` with typed columns and hybrid properties.
  - Provide fallback default generators for existing players lacking `psychological_dna` or `backstory`.
- [ ] **Step 2: Tier 1 Mathematical Tension Engine (`backend/app/engine/society/tension_engine.py`)**
  - Implement `TensionEngine.calculate_weekly_tension(player, game_stats, team_record, team_context)`.
  - Implement target share penalty for high-ego WRs/TEs.
  - Implement benching penalty for high-ego starters.
  - Implement contract leverage escalation for high-greed players in contract years.
  - Implement offensive line trust degradation if QB takes $\ge 4$ sacks or turns over ball.
- [ ] **Step 3: Tier 2 & 3 Locker Room Agent Service (`backend/app/engine/society/locker_room_agent.py`)**
  - Implement `LockerRoomAgentService.evaluate_team_locker_room(team_id, db_session)`.
  - Gather active grievance actors ($\text{Tension} \ge 75$) and identify team captains.
  - Construct structured prompt payload and invoke model with deterministic fallback logic.
  - Apply consequence mutations (morale updates, trust edges, public drama flags).
- [ ] **Step 4: Unit & Integration Verification Suite**
  - Create `backend/tests/unit/test_tension_engine.py` (Validating all mathematical edge cases).
  - Create `backend/tests/unit/test_locker_room_agent.py` (Validating agent evaluation and fallback parsing).

### 4. Edge Cases & Error Handling

- **[Case A: Missing/Null `psychological_dna` or `backstory`]:** -> `TensionEngine` defaults to neutral baseline ($50$ for all psychological traits).
- **[Case B: Offline / LLM Timeout or API Error]:** -> `LockerRoomAgentService` falls back to deterministic rule-based template dialogue without halting simulation.
- **[Case C: Zero Active Grievances in a Week]:** -> Tier 3 skips LLM invocation completely ($0\text{ms}$ execution, $0$ tokens consumed).

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** No `any` types in Python models, Pydantic schemas, or TypeScript contracts.
- [ ] **Security:** Prompt sanitization implemented to prevent prompt injection from player name strings.
- [ ] **Performance:** Tier 1 tension calculations execute in $<2\text{ms}$ for all 53 roster players.
- [ ] **Karpathy Simplicity-First Audit:** Zero speculative wrapper abstractions; pure functions and direct SQLAlchemy models.
- [ ] **Verification Stop:** Verbatim test execution output generated for `test_tension_engine.py` and `test_locker_room_agent.py`.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Execute Step 1 (Modify `Player` model in `backend/app/models/player.py`) and Step 2 (Implement `TensionEngine` in `backend/app/engine/society/tension_engine.py`).
</baton_handoff>

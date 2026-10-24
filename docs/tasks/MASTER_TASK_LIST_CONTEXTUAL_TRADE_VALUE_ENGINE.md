# Contextual Trade Value Engine (CTVE) Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Replace the legacy single-formula trade evaluator with a 3-layer Contextual Trade Value Engine (CTVE) on a unified Fitzgerald-Spielberger Trade Value Point (TVP) currency (`#1 pick = 3,000 TVP`), incorporating positional market APY% curves, position-specific aging, projected-slot future draft pick valuation, two-sided Team Need Index (TNI), 4-year CBA cap & dead-money projection, Monte-Carlo Draft-Class Fit, 5 hyper-realism modifiers, and ratio-based grading (`A+` to `F`) with knapsack counter-offers.

**Architecture:** A modular backend domain service package (`backend/app/services/trade_engine/`) organized into three layers—**Market Layer** (`market.py`, `picks.py`), **Context Layer** (`context.py`, `cap.py`, `class_fit.py`, `modifiers.py`), and **Decision Layer** (`decision.py`)—invoked by [`GMAgent.evaluate_trade`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/backend/app/services/gm_agent.py#L43-L150) and exposed via [`POST /api/trades/evaluate`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/backend/app/api/endpoints/trades.py#L85-L177). The React frontend consumes backend-computed TVP and dual-team grade breakdowns directly, eliminating client-side valuation drift.

**Tech Stack:** Python 3.11+, FastAPI, SQLAlchemy 2.0 (Mapped ORM), Alembic, Pydantic v2, Pytest, React 19, TypeScript 5.5+ (strict, 0 `any`), Vitest / Playwright.

---

## 🗺️ Master Dependency & Phase Index

| Task ID | Phase | Task Name | Primary Files Created / Modified |
| :--- | :--- | :--- | :--- |
| **TASK-CTVE-000** | Phase 0 | Foundational Bug Fixes & Contract Alignment | `backend/app/core/trade_config.py`, `backend/app/services/gm_agent.py`, `backend/app/api/endpoints/trades.py`, `frontend/src/components/trades/TradeAnalyzer.tsx`, `frontend/src/services/tradeApi.ts` |
| **TASK-CTVE-001** | Phase 1 | Market Layer — Positional APY, Aging Curves & Surplus TVP | `backend/app/services/trade_engine/market.py`, `backend/tests/unit/test_ctve_market.py` |
| **TASK-CTVE-002** | Phase 2 | Draft Pick Ledger, Projected-Slot EV & Conditional Picks | `backend/alembic/versions/xxxx_expand_draft_pick_trade_ledger.py`, `backend/app/models/draft.py`, `backend/app/services/trade_engine/picks.py`, `backend/tests/unit/test_ctve_picks.py` |
| **TASK-CTVE-003** | Phase 3 | Team Context Layer — Two-Sided TNI, Youth Pipeline & Window | `backend/app/services/trade_engine/context.py`, `backend/tests/unit/test_ctve_context.py` |
| **TASK-CTVE-004** | Phase 4 | CBA Salary Cap Layer — Dead Money Acceleration & 4-Yr Projection | `backend/app/services/trade_engine/cap.py`, `backend/tests/unit/test_ctve_cap.py` |
| **TASK-CTVE-005** | Phase 5 | Draft-Class Fit — Seeded Monte-Carlo Availability & Run Risk | `backend/app/services/trade_engine/class_fit.py`, `backend/tests/unit/test_ctve_class_fit.py` |
| **TASK-CTVE-006** | Phase 6 | The 5 Hyper-Realism Modifiers (Injury, Scheme, Morale, Market, Rivalry) | `backend/app/services/trade_engine/modifiers.py`, `backend/tests/unit/test_ctve_modifiers.py` |
| **TASK-CTVE-007** | Phase 7 | Ratio Grading, Knapsack Counter-Offers & Frontend Dual-Grade UI | `backend/app/services/trade_engine/decision.py`, `backend/app/schemas/trade.py`, `frontend/src/components/trades/TradeAnalyzer.tsx`, `backend/tests/integration/test_ctve_end_to_end.py` |

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-000 — Phase 0: Foundational Bug Fixes & Contract Alignment

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Domain-Driven Design (Bounded Contexts & Ubiquitous Language). When enum identifiers drift between configuration tables (`EDGE/LT/RT/OL/DL`) and ORM entities (`DE/OT/OG/C/DT`), silent fallbacks corrupt downstream valuations.
- **Related Ideas:** Idempotent HTTP read semantics (RFC 9110: evaluation/analysis endpoints must not mutate audit tables), Single Source of Truth (SSOT) between backend contracts and frontend DTOs.
- **Future Potential:** Establishes clean, bug-free interfaces so Phases 1–7 can plug into `GMAgent` and `/api/trades/*` without fighting legacy key mismatches or dropped pick payloads.
- **Constraints:** Zero breaking changes to existing passing API tests; `Position` enum keys strictly enforced; `/api/trades/evaluate` must be side-effect free (`log_decision=False` on dry-run evaluation); scores rounded to 1 decimal place.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Leave the existing `trade_config.py`, `gm_agent.py`, and `trades.py` untouched while building the new engine alongside them, then swap everything at the very end.

### Powerful Antithesis
Leaving broken key mappings (`EDGE/LT/RT/OL/DL`), unrounded floats (`-204.28023350526902`), dropped pick arrays (`offered_picks: null` in `TradeAnalyzer.tsx`), and un-transferred draft picks on trade acceptance means any incremental testing of Phases 1–6 will still fail on basic plumbing bugs. Worse, `submit_trade_offer` currently crashes with `HTTP 400` on pick-only trades because it infers `offering_team_id` from `offered_player_ids[0]`.

### The Superior Synthesis
Execute a surgical Phase 0 hygiene sweep first:
1. Map all 14 `Position` enum values (`QB, RB, WR, TE, OT, OG, C, DE, DT, LB, CB, S, K, P`) in `trade_config.py` and `gm_agent.py` (retaining aliases for `EDGE/LT/RT` backward compatibility).
2. Add optional `offering_team_id: int | None = None` to `TradeEvaluationRequest` and `TradeOfferRequest` so pick-only trades work deterministically.
3. Transfer `DraftPick.team_id` ownership when an offer is accepted in `trades.py`.
4. Make `GMAgent.evaluate_trade(..., log_decision: bool = False)` side-effect free during dry-run `/evaluate` calls while logging formal offer responses.
5. Pass real player contract `salary` and `years_remaining` and `trade_value` from the backend roster payload instead of hardcoding `$5M / 2 yrs` in `tradeApi.ts`.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** FastAPI, SQLAlchemy 2.0, Pydantic v2, React 19, TypeScript 5.5+.
- **Language:** Python 3.11+ & TypeScript (strict mode, zero `any`).
- **State Management:** Stateless REST evaluation + transactional SQLAlchemy session commit on formal trade acceptance.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/schemas/trade.py additions
class DraftPickInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | None = Field(default=None, description="Specific DraftPick DB row ID if known")
    round: int = Field(ge=1, le=7, description="Draft round (1-7)")
    year: int = Field(ge=2024, le=2035, description="Draft year")
    original_team_id: int | None = Field(default=None, description="Original team ID")

class TradeEvaluationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    offering_team_id: int | None = Field(default=None, description="Team offering assets")
    target_team_id: int = Field(description="Team ID evaluating the trade")
    offered_player_ids: list[int] = Field(default_factory=list)
    requested_player_ids: list[int] = Field(default_factory=list)
    offered_picks: list[DraftPickInfo] | None = Field(default=None)
    requested_picks: list[DraftPickInfo] | None = Field(default=None)
```

### 3. Step-by-Step Execution

#### Task 0.1: Align `Position` Enum Keys in `trade_config.py` & `gm_agent.py`

**Objective:** Ensure `DE`, `OT`, `OG`, `C`, `DT` match `Position` enum values in `trade_config.py` and `gm_agent._get_position_need`.

**Files:**
- Modify: `backend/app/core/trade_config.py:24-50`
- Modify: `backend/app/services/gm_agent.py:158-161,387-415`
- Test: `backend/tests/unit/test_trade_phase0_fixes.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_trade_phase0_fixes.py
from app.core.trade_config import trade_config
from app.models.player import Position


def test_all_position_enum_members_have_explicit_tier():
    """Every Position enum value must map to its intended tier, never falling through by accident."""
    assert trade_config.get_position_tier(Position.QB) == "ELITE"
    assert trade_config.get_position_tier(Position.DE) == "PREMIUM"
    assert trade_config.get_position_tier(Position.OT) == "PREMIUM"
    assert trade_config.get_position_tier(Position.WR) == "PREMIUM"
    assert trade_config.get_position_tier(Position.CB) == "PREMIUM"
    assert trade_config.get_position_tier(Position.DT) == "HIGH"
    assert trade_config.get_position_tier(Position.S) == "HIGH"
    assert trade_config.get_position_multiplier(Position.DE) == 1.25
    assert trade_config.get_position_multiplier(Position.OT) == 1.25
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_trade_phase0_fixes.py::test_all_position_enum_members_have_explicit_tier -v`
Expected: FAIL — `AssertionError: assert 'STANDARD' == 'PREMIUM'` for `Position.DE` and `Position.OT`.

- [ ] **Step 3: Write minimal implementation**
```python
# In backend/app/core/trade_config.py (lines 24-50)
    POSITION_VALUE_TIERS: dict[str, dict[str, Any]] = {
        "ELITE": {
            "positions": ["QB"],
            "multiplier": 1.45,
            "description": "Franchise cornerstones. Hardest to acquire.",
        },
        "PREMIUM": {
            "positions": ["DE", "OT", "WR", "CB", "EDGE", "LT"],
            "multiplier": 1.25,
            "description": "High-impact positions paid at top of market.",
        },
        "HIGH": {
            "positions": ["DT", "S", "RT"],
            "multiplier": 1.15,
            "description": "Core starters, increasing in modern value.",
        },
        "STANDARD": {
            "positions": ["TE", "LB", "C", "OG", "RB"],
            "multiplier": 1.00,
            "description": "Dependent on scheme. Value flattened by market.",
        },
        "DEPTH": {
            "positions": ["FB", "K", "P", "LS"],
            "multiplier": 0.65,
            "description": "Specialists and niche roles.",
        },
    }
```
And in `backend/app/services/gm_agent.py` (`_get_position_need` and `generate_trade_proposal`), replace `["OL", "DL"]` checks with `["OT", "OG", "C"]` (starters threshold `< 5`) and `["DE", "DT"]` (threshold `< 4`), and round `score` in `evaluate_trade` via `round(modified_score, 1)`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_trade_phase0_fixes.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/core/trade_config.py backend/app/services/gm_agent.py backend/tests/unit/test_trade_phase0_fixes.py
git commit -m "fix(trades): align Position enum keys in trade_config and GMAgent"
```

#### Task 0.2: Support Pick-Only Trades, Transfer Picks on Accept & Side-Effect-Free Evaluate

**Objective:** Allow `offering_team_id` on trade requests, transfer `DraftPick.team_id` when offers are accepted, and prevent `/api/trades/evaluate` from polluting `GMDecision` audit logs on dry-run previews unless requested.

**Files:**
- Modify: `backend/app/schemas/trade.py:16-90`
- Modify: `backend/app/api/endpoints/trades.py:206-235,328-360`
- Test: `backend/tests/unit/test_trade_phase0_fixes.py`

- [ ] **Step 1: Write failing test**
```python
# Append to backend/tests/unit/test_trade_phase0_fixes.py
import pytest
from app.models.draft import DraftPick
from app.models.season import Season
from app.models.team import Team
from app.models.trade_offer import TradeOffer, TradeOfferStatus


@pytest.mark.asyncio
async def test_accept_offer_transfers_draft_pick_ownership(async_client, db_session):
    t1 = Team(id=10, name="Lions", city="Detroit", abbreviation="DET", conference="NFC", division="North")
    t2 = Team(id=11, name="Raiders", city="Las Vegas", abbreviation="LV", conference="AFC", division="West")
    season = Season(id=1, year=2025, current_week=1, is_active=True)
    pick = DraftPick(id=501, season_id=1, team_id=10, original_team_id=10, round=1, pick_number=15)
    db_session.add_all([t1, t2, season, pick])
    db_session.commit()

    offer = TradeOffer(
        id=900,
        offering_team_id=10,
        receiving_team_id=11,
        offered_player_ids=[],
        requested_player_ids=[],
        offered_picks=[{"id": 501, "round": 1, "year": 2025}],
        requested_picks=[{"round": 2, "year": 2025}],
        status=TradeOfferStatus.PENDING,
    )
    db_session.add(offer)
    db_session.commit()

    resp = await async_client.post("/api/trades/respond/900", json={"action": "accept"})
    assert resp.status_code == 200
    db_session.expire_all()
    updated_pick = db_session.get(DraftPick, 501)
    assert updated_pick.team_id == 11
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_trade_phase0_fixes.py::test_accept_offer_transfers_draft_pick_ownership -v`
Expected: FAIL — `assert updated_pick.team_id == 11` (remains `10`).

- [ ] **Step 3: Write minimal implementation**
In `backend/app/api/endpoints/trades.py`:
1. In `submit_trade_offer`, use `request.offering_team_id` first before falling back to `offered_player_ids[0]`.
2. In `respond_to_offer` under `if action == "accept":`, iterate over `offer.offered_picks or []` and `offer.requested_picks or []`; locate matching `DraftPick` by `id` (or by `(season.year == pick["year"], round == pick["round"], team_id == from_team_id)`) and update `pick.team_id = to_team_id`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_trade_phase0_fixes.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/schemas/trade.py backend/app/api/endpoints/trades.py backend/tests/unit/test_trade_phase0_fixes.py
git commit -m "fix(trades): transfer DraftPick ownership on trade acceptance and support pick-only offers"
```

#### Task 0.3: Pass Picks & Real Contract Data in Frontend `TradeAnalyzer.tsx` & `tradeApi.ts`

**Objective:** Forward selected draft picks to `/api/trades/evaluate` in `TradeAnalyzer.tsx` and use real player salary/contract years in `tradeApi.ts`.

**Files:**
- Modify: `frontend/src/components/trades/TradeAnalyzer.tsx:10-55`
- Modify: `frontend/src/services/tradeApi.ts:45-68`
- Test: `frontend/src/components/trades/__tests__/TradeAnalyzer.test.tsx`

- [ ] **Step 1: Write failing test**
Create unit test verifying `TradeAnalyzer` passes `offeredPicks` and `requestedPicks` in the `POST /api/trades/evaluate` request body and formats the score to 1 decimal place.
- [ ] **Step 2: Run test to verify failure**
Run: `npm --prefix frontend test -- TradeAnalyzer`
Expected: FAIL — `offered_picks` is hardcoded to `null`.
- [ ] **Step 3: Write minimal implementation**
Add optional `offeredPicks?: DraftPickInfo[]` and `requestedPicks?: DraftPickInfo[]` props to `TradeAnalyzerProps`, pass them in `JSON.stringify(...)`, and format `evaluation.score.toFixed(1)`. In `tradeApi.ts`, map `salary: p.contract_salary ?? 1_000_000` and `years_remaining: p.contract_years ?? 1`.
- [ ] **Step 4: Run test to verify pass**
Run: `npm --prefix frontend test -- TradeAnalyzer`
Expected: PASS
- [ ] **Step 5: Commit**
```bash
git add frontend/src/components/trades/TradeAnalyzer.tsx frontend/src/services/tradeApi.ts
git commit -m "fix(ui): pass draft picks to TradeAnalyzer and use real player contract fields"
```

### 4. Edge Cases & Error Handling

- **Pick-only trade without `offering_team_id` or `offered_picks`:** Return `HTTP 400` with explicit detail `"offering_team_id is required when no offered players are provided"`.
- **Player missing `contract` relationship:** Fallback to `$1,000,000` 1-year contract without throwing `AttributeError`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/core/trade_config.py backend/app/api/endpoints/trades.py` and `npm --prefix frontend run typecheck` pass with 0 `any`.
- [ ] **Security:** Verify `requested_player_ids` ownership check (`player.team_id == request.target_team_id`) cannot be bypassed.
- [ ] **Performance:** Single DB transaction on trade execution (`< 15ms`).
- [ ] **Self-Critique:** Retaining `EDGE/LT/RT` aliases in `POSITION_VALUE_TIERS` guarantees legacy tests that pass `"EDGE"` or `"LT"` continue to pass while all real `Position` enum rows hit the proper tier.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-001` to build the Market Layer (`backend/app/services/trade_engine/market.py`) on the unified Fitzgerald-Spielberger TVP currency.
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-001 — Phase 1: Market Layer — Positional APY, Aging Curves & Surplus TVP

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** OverTheCap (OTC) Fitzgerald-Spielberger trade chart (`#1 = 3,000 TVP`, `#32 = 1,244 TVP`, `#64 = 892 TVP`), PFF WAR (Wins Above Replacement) aging clusters, and NFL front-office **Surplus Value Theory** (on-field market value minus cap hit across remaining years of team control).
- **Related Ideas:** Option pricing theory (5th-year rookie options and Franchise Tag control years), 2025 NFL positional market APY ceilings (`$279.2M` cap: QB `21.5%`, DE `14.3%`, WR `14.0%`, DT `13.0%`, OT `10.1%`, CB `9.3%`, OG `8.9%`, C `9.5%`, LB `9.0%`, S `8.2%`, RB `7.8%`, TE `6.8%`, K/P `2.5%`).
- **Future Potential:** Automatically scales to any future league year (2026–2035+) because market value is expressed as a **percentage of the active league salary cap** (`Cap_y` growing at `SALARY_CAP_CAGR = 6.97%`), eliminating hardcoded dollar bands.
- **Constraints:** Deterministic pure functions (`< 1ms` per player valuation), strictly typed `PositionValueProfile`, calibrated against pre-registered real NFL trades (Adams, Ramsey, McCaffrey, Diggs, Wilson).
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Value a player using `((OVR - 50) ** 1.6) / 2.0 * pos_mult * age_mult` and multiply by a flat contract ratio bucket (`1.20` for cheap, `0.60` for expensive).

### Powerful Antithesis
1. **Flat age curves distort positional reality:** A 28-year-old RB is at the edge of a steep physical cliff, whereas a 28-year-old QB or OT is entering his statistical prime.
2. **Pure surplus (`MV - CapHit`) under-values stars on market deals:** If $\lambda = 1.0$, a 96-OVR WR paid full market APY would have `0` surplus and trade for nothing, contradicting the Davante Adams and Tyreek Hill blockbusters (elite talent is scarce and cannot be freely bought in FA).
3. **Ignoring control options:** A 1st-round rookie in Year 2 has 2 cheap base years + a 5th-year option + potential Franchise Tag control.

### The Superior Synthesis
Implement `market.py` using **Scarcity-Weighted Multi-Year Surplus TVP**:
$$TVP_{player} = \kappa \sum_{y=0}^{Y_{ctrl}-1} \delta^{y} \cdot \max\Big(0,\ MV_y - \lambda \cdot CapHit_y\Big) \cdot R_{risk}$$
With $\lambda = 0.60$ (cap-cost discount reflecting star scarcity in free agency) and $\kappa$ calibrated so that the 5 pre-registered NFL trade archetypes land inside their target TVP bands on the 3,000-point FS chart.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+ dataclasses & Pydantic v2.
- **Language:** Strict type annotations (`mypy --strict` clean).
- **State Management:** Pure functional calculation in `backend/app/services/trade_engine/market.py`.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/services/trade_engine/market.py
from dataclasses import dataclass
from app.models.player import DevelopmentTrait, Position

@dataclass(frozen=True)
class PositionValueProfile:
    position: Position
    top_apy_pct_cap: float      # Top-of-market APY as fraction of league cap
    starters_required: int      # Standard starting slots per team
    peak_start: int             # Age where prime plateau begins
    peak_end: int               # Age where prime plateau ends
    decline_per_year: float     # Annual OVR drop rate after peak_end
    cliff_age: int              # Age where decline rate doubles

@dataclass(frozen=True)
class PlayerValuationBreakdown:
    player_id: int
    base_market_tvp: float
    projected_ovrs: list[float]
    annual_market_values: list[int]
    annual_cap_hits: list[int]
    years_of_control: int
    includes_fifth_year_option: bool
    includes_franchise_tag_window: bool
```

### 3. Step-by-Step Execution

#### Task 1.1: Create `PositionValueProfile` Registry & Per-Position Aging Projection

**Objective:** Define the 14 position profiles and project player OVR across future control years using age, `peak_start`/`peak_end`, `decline_per_year`, `cliff_age`, and `development_trait`.

**Files:**
- Create: `backend/app/services/trade_engine/__init__.py`
- Create: `backend/app/services/trade_engine/market.py`
- Test: `backend/tests/unit/test_ctve_market.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_market.py
from app.models.player import DevelopmentTrait, Position
from app.services.trade_engine.market import POSITION_PROFILES, project_player_ovr_curve


def test_position_profiles_cover_all_positions():
    for pos in Position:
        assert pos in POSITION_PROFILES
    assert POSITION_PROFILES[Position.QB].top_apy_pct_cap > POSITION_PROFILES[Position.DE].top_apy_pct_cap
    assert POSITION_PROFILES[Position.DE].top_apy_pct_cap > POSITION_PROFILES[Position.RB].top_apy_pct_cap


def test_rb_ages_faster_than_qb():
    rb_curve = project_player_ovr_curve(
        ovr=90, age=27, position=Position.RB, dev_trait=DevelopmentTrait.STAR, years=4
    )
    qb_curve = project_player_ovr_curve(
        ovr=90, age=27, position=Position.QB, dev_trait=DevelopmentTrait.STAR, years=4
    )
    # By year 3 (age 30), RB must have declined significantly more than QB
    assert rb_curve[-1] < qb_curve[-1] - 6.0
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_market.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine'`

- [ ] **Step 3: Write minimal implementation**
Create `backend/app/services/trade_engine/__init__.py` and `backend/app/services/trade_engine/market.py` with `POSITION_PROFILES` for all 14 `Position` enum values and `project_player_ovr_curve(...)` implementing pre-peak growth (`NORMAL=0.8`, `STAR=1.5`, `SUPERSTAR=2.2`, `XFACTOR=3.0` OVR/yr tapered to `peak_start`) and post-`peak_end` decline (doubling past `cliff_age`).

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_market.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/__init__.py backend/app/services/trade_engine/market.py backend/tests/unit/test_ctve_market.py
git commit -m "feat(trade-engine): add PositionValueProfile registry and per-position aging curves"
```

#### Task 1.2: Implement Surplus TVP Calculator & Pre-Registered Benchmark Calibration

**Objective:** Compute `calculate_player_market_tvp` in `market.py` and verify it satisfies all 5 pre-registered NFL trade benchmarks plus monotonicity invariants.

**Files:**
- Modify: `backend/app/services/trade_engine/market.py`
- Modify: `backend/tests/unit/test_ctve_market.py`

- [ ] **Step 1: Write failing test**
```python
# Append to backend/tests/unit/test_ctve_market.py
from app.services.trade_engine.market import PlayerSnapshot, calculate_player_market_tvp


def test_preregistered_nfl_trade_benchmarks():
    cap = 279_200_000
    # 1. Davante Adams archetype: 29-yr 95 WR on new market deal ($35M, 4 yrs) -> 2,200 - 2,800 TVP
    adams = PlayerSnapshot(
        id=1, position=Position.WR, overall_rating=95, age=29,
        contract_years=4, annual_base_salary=35_000_000, is_rookie=False,
        development_trait=DevelopmentTrait.SUPERSTAR,
    )
    assert 2200 <= calculate_player_market_tvp(adams, cap).base_market_tvp <= 2800

    # 2. Jalen Ramsey archetype: 24-yr 92 CB on cheap rookie deal ($4M, 2 yrs + 5th yr option) -> 2,800 - 3,600 TVP
    ramsey = PlayerSnapshot(
        id=2, position=Position.CB, overall_rating=92, age=24,
        contract_years=2, annual_base_salary=4_000_000, is_rookie=True, draft_round=1,
        development_trait=DevelopmentTrait.XFACTOR,
    )
    assert 2800 <= calculate_player_market_tvp(ramsey, cap).base_market_tvp <= 3600

    # 3. Christian McCaffrey archetype: 26-yr 95 RB on market deal ($16M, 3 yrs) -> 1,600 - 2,400 TVP
    cmc = PlayerSnapshot(
        id=3, position=Position.RB, overall_rating=95, age=26,
        contract_years=3, annual_base_salary=16_000_000, is_rookie=False,
        development_trait=DevelopmentTrait.XFACTOR,
    )
    assert 1600 <= calculate_player_market_tvp(cmc, cap).base_market_tvp <= 2400

    # 4. Stefon Diggs archetype: 30-yr 85 WR on market deal ($22M, 2 yrs) -> 800 - 1,200 TVP
    diggs = PlayerSnapshot(
        id=4, position=Position.WR, overall_rating=85, age=30,
        contract_years=2, annual_base_salary=22_000_000, is_rookie=False,
        development_trait=DevelopmentTrait.STAR,
    )
    assert 800 <= calculate_player_market_tvp(diggs, cap).base_market_tvp <= 1200

    # 5. Russell Wilson archetype: 33-yr 88 QB on $40M deal, 3 yrs -> 3,500 - 4,500 TVP
    wilson = PlayerSnapshot(
        id=5, position=Position.QB, overall_rating=88, age=33,
        contract_years=3, annual_base_salary=40_000_000, is_rookie=False,
        development_trait=DevelopmentTrait.STAR,
    )
    assert 3500 <= calculate_player_market_tvp(wilson, cap).base_market_tvp <= 4500
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_market.py::test_preregistered_nfl_trade_benchmarks -v`
Expected: FAIL — `ImportError: cannot import name 'PlayerSnapshot'`

- [ ] **Step 3: Write minimal implementation**
Implement `PlayerSnapshot`, `ovr_to_market_tier(ovr)`, `calculate_player_market_tvp(player, current_cap, discount_factor=0.85, cap_weight_lambda=0.60)` in `backend/app/services/trade_engine/market.py`, including 5th-year option control for 1st-round rookies (`is_rookie and draft_round == 1`) and 1 Franchise Tag control year (weighted at `0.5`) for elite players (`ovr >= 88`).

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_market.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/market.py backend/tests/unit/test_ctve_market.py
git commit -m "feat(trade-engine): implement surplus TVP player valuation calibrated to NFL benchmarks"
```

### 4. Edge Cases & Error Handling

- **Sub-replacement players (`OVR < 65`) with bloated contracts (`> $10M`):** `MV_y - lambda * CapHit_y` becomes negative, producing a **negative TVP** (an explicit salary-dump liability requiring draft pick sweeteners to move, like the Brock Osweiler trade).
- **Zero remaining contract years:** Clamp `contract_years` to `1` with rental discount `0.75`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/market.py` passes with 0 errors.
- [ ] **Security:** Pure deterministic mathematical functions; no DB or network side effects.
- [ ] **Performance:** `< 0.05ms` per player valuation.
- [ ] **Self-Critique:** Allowing negative TVP on overpaid low-OVR veterans naturally enables NBA/NFL-style salary dump trades in Phase 4 without special-case hacks.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-002` to build the Draft Pick Ledger migration and Projected-Slot Expected Value engine (`picks.py`).
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-002 — Phase 2: Draft Pick Ledger, Projected-Slot EV & Conditional Picks

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** NFL rules permit trading draft picks up to 3 drafts into the future (`current_year + 2`). In NFL front offices, a future 1st from a projected 3-14 bottom-feeder is prized as a potential top-5 lottery ticket, whereas a future 1st from a 14-3 Super Bowl contender is valued like a late-2nd-round pick (`~1,000–1,100 TVP`).
- **Related Ideas:** Gaussian slot distribution over convex payoff functions ($E[f(X)] > f(E[X])$ by Jensen's Inequality on the steep top-10 Fitzgerald-Spielberger curve), conditional pick probability trees.
- **Future Potential:** Pre-allocating `DraftPick` rows for `year in [current_year, current_year+1, current_year+2]` enables multi-year pick tracking, pick-swap rights, and live draft-order projection throughout the regular season.
- **Constraints:** `DraftPick.pick_number` must be nullable until draft order is finalized; `OffseasonService.generate_draft_order` must **update** existing `DraftPick` rows in place so traded ownership (`team_id != original_team_id`) is never overwritten.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Keep `DraftValueChart.get_future_pick_value` as a static `round_num + years_in_future` lookup at pick 16 of the round, and only create `DraftPick` DB rows at the end of the season.

### Powerful Antithesis
1. Creating `DraftPick` rows at the end of the season with `team_id=team_id, original_team_id=team_id` wipes out any future picks traded during the season or previous offseason!
2. Furthermore, `draft_value_chart.py` currently applies an extra `TOP_10_PICK_PREMIUM = 1.20` on top of the Fitzgerald-Spielberger chart, which *already* embeds the top-10 curve (`#1 = 3,000`), double-counting top-10 value to `3,600`.
3. Treating every team's future 1st as pick `#48` (`1,047` points) lets users fleece bottom-feeding AI teams for their future `#1` overall pick at a 65% discount.

### The Superior Synthesis
1. Add `year: Mapped[int]`, `is_compensatory: Mapped[bool]`, `conditions: Mapped[dict | None]`, and nullable `pick_number: Mapped[int | None]` to `DraftPick`.
2. Add `ensure_future_picks_ledger(db, current_year, horizon=2)` to idempotently seed rounds 1–7 for all 32 teams across `current_year .. current_year + 2`, and update `OffseasonService` to assign `pick_number` in-place via `original_team_id` order.
3. Value future picks in `picks.py` by taking the Gaussian expected value over `DraftValueChart` centered on the **original team's projected draft slot** ($\mu_{\text{slot}}$ derived from team Elo + win pct + roster strength, $\sigma \in \{4, 9, 11\}$ by years out), multiplied by time discount $D^{\text{years}}$ ($D = 0.78$).
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** SQLAlchemy 2.0, Alembic, Python `math.erf` / Gaussian quadrature over discrete slots `1..32`.
- **Language:** Python 3.11+ (strict typing).
- **State Management:** Persistent `DraftPick` ownership ledger in SQLite/PostgreSQL.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/models/draft.py updates
class DraftPick(Base):
    __tablename__ = "draft_pick"
    __table_args__ = (Index("ix_draft_pick_season_round", "season_id", "round"),)

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=True, index=True)
    year = Column(Integer, nullable=False, default=2025, index=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False, index=True)
    original_team_id = Column(Integer, ForeignKey("team.id"), nullable=False, index=True)
    round = Column(Integer, nullable=False, index=True)
    pick_number = Column(Integer, nullable=True, index=True)  # Nullable until draft order finalized
    is_compensatory = Column(Boolean, default=False, nullable=False)
    conditions = Column(JSON, nullable=True)  # e.g. {"upgrade_to_round": 2, "probability": 0.65}
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
```

### 3. Step-by-Step Execution

#### Task 2.1: Remove Double-Counted Top-10 Tax & Implement Projected-Slot Future Pick EV (`picks.py`)

**Objective:** Fix `DraftValueChart.get_pick_value(1) == 3000` (exact FS anchor) and create `backend/app/services/trade_engine/picks.py` to value current, future, and conditional picks using the original team's projected draft slot distribution.

**Files:**
- Modify: `backend/app/data/draft_value_chart.py:91-108`
- Create: `backend/app/services/trade_engine/picks.py`
- Test: `backend/tests/unit/test_ctve_picks.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_picks.py
from app.data.draft_value_chart import DraftValueChart
from app.services.trade_engine.picks import PickValuationInput, evaluate_draft_pick_tvp


def test_fitzgerald_spielberger_exact_anchors():
    assert DraftValueChart.get_pick_value(1) == 3000
    assert DraftValueChart.get_pick_value(32) == 1244
    assert DraftValueChart.get_pick_value(64) == 895


def test_future_first_scales_with_original_team_strength():
    # Bottom-feeder (projected slot 2) vs Average (slot 16) vs Contender (slot 30)
    bottom_pick = PickValuationInput(round=1, year=2026, current_year=2025, projected_slot_in_round=2)
    avg_pick = PickValuationInput(round=1, year=2026, current_year=2025, projected_slot_in_round=16)
    contender_pick = PickValuationInput(round=1, year=2026, current_year=2025, projected_slot_in_round=30)

    v_bottom = evaluate_draft_pick_tvp(bottom_pick).market_tvp
    v_avg = evaluate_draft_pick_tvp(avg_pick).market_tvp
    v_contender = evaluate_draft_pick_tvp(contender_pick).market_tvp

    assert v_bottom > v_avg > v_contender
    # Pre-registered benchmark: average team's future 1st = 1,100 - 1,350 TVP
    assert 1100 <= v_avg <= 1350
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_picks.py -v`
Expected: FAIL — `DraftValueChart.get_pick_value(1)` returns `3600` instead of `3000`, and `app.services.trade_engine.picks` does not exist.

- [ ] **Step 3: Write minimal implementation**
1. In `backend/app/data/draft_value_chart.py`, return `base_value` directly in `get_pick_value` without multiplying by `TOP_10_PICK_PREMIUM`.
2. Create `backend/app/services/trade_engine/picks.py` with discrete Gaussian slot weighting over `slot in 1..32` around `projected_slot_in_round`, time discount `D = 0.78 ** years_out`, and conditional pick probability summation.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_picks.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/data/draft_value_chart.py backend/app/services/trade_engine/picks.py backend/tests/unit/test_ctve_picks.py
git commit -m "feat(trade-engine): add projected-slot EV draft pick valuation and fix FS top-10 anchor"
```

#### Task 2.2: Expand `DraftPick` Model & Preserve Traded Ownership Across Offseason Order Generation

**Objective:** Add `year`, `is_compensatory`, `conditions`, and nullable `pick_number` to `DraftPick`, plus `ensure_future_picks_ledger` and non-destructive draft order assignment in `OffseasonService`.

**Files:**
- Modify: `backend/app/models/draft.py`
- Modify: `backend/app/services/offseason_service.py:438-455`
- Test: `backend/tests/unit/test_ctve_picks.py`

- [ ] **Step 1: Write failing test**
```python
# Append to backend/tests/unit/test_ctve_picks.py
from app.services.trade_engine.picks import ensure_future_picks_ledger, assign_draft_order_preserving_trades
from app.models.team import Team
from app.models.season import Season


def test_draft_order_generation_preserves_traded_pick_owner(db_session):
    t1 = Team(id=1, name="Bears", city="Chicago", abbreviation="CHI", conference="NFC", division="North")
    t2 = Team(id=2, name="Panthers", city="Carolina", abbreviation="CAR", conference="NFC", division="South")
    season = Season(id=10, year=2025, current_week=18, is_active=True)
    db_session.add_all([t1, t2, season])
    db_session.commit()

    ensure_future_picks_ledger(db_session, current_year=2025, season_id=10, horizon=2)
    # Trade Carolina's (id=2) 2025 Round 1 pick to Chicago (id=1)
    car_r1 = (
        db_session.query(DraftPick)
        .filter_by(year=2025, round=1, original_team_id=2)
        .one()
    )
    car_r1.team_id = 1
    db_session.commit()

    # Carolina finishes worst (1st in draft order), Chicago finishes 2nd
    assign_draft_order_preserving_trades(db_session, season_id=10, year=2025, ordered_team_ids=[2, 1])

    db_session.refresh(car_r1)
    assert car_r1.pick_number == 1
    assert car_r1.team_id == 1  # Still owned by Chicago!
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_picks.py::test_draft_order_generation_preserves_traded_pick_owner -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**
Update `backend/app/models/draft.py`, implement `ensure_future_picks_ledger` and `assign_draft_order_preserving_trades` in `backend/app/services/trade_engine/picks.py`, and call it from `OffseasonService`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_picks.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/models/draft.py backend/app/services/offseason_service.py backend/app/services/trade_engine/picks.py backend/tests/unit/test_ctve_picks.py
git commit -m "feat(draft): seed 3-year DraftPick ledger and preserve traded ownership on order generation"
```

### 4. Edge Cases & Error Handling

- **Compensatory picks (`is_compensatory=True`):** Eligible to be traded under modern NFL CBA rules (since 2017), slotted at the end of rounds 3–7.
- **Picks > 3 years out:** Raise `ValueError("Cannot trade draft picks more than 3 years in the future")` and map to `HTTP 400` in `/api/trades/*`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/picks.py` passes cleanly.
- [ ] **Security:** Verify a team cannot include a `DraftPick` in `offered_picks` unless `pick.team_id == offering_team_id`.
- [ ] **Performance:** Discrete 32-slot Gaussian EV runs in `< 0.02ms` per pick.
- [ ] **Self-Critique:** Updating existing `DraftPick` rows via `original_team_id` instead of recreating them eliminates the classic franchise-mode bug where off-season transitions erase mid-season pick trades.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-003` to implement the Team Context Layer (`context.py`): Two-Sided Team Need Index (TNI), Youth Pipeline Offset, and Competitive Window classifier.
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-003 — Phase 3: Team Context Layer — Two-Sided TNI, Youth Pipeline & Window

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** NFL personnel departments grade positional need along two axes: **Immediate Starter/Depth Deficit (`NeedNow`)** and **2-Year Horizon Risk (`NeedFuture` — age cliffs + contract expirations minus young developmental pipeline)**.
- **Related Ideas:** Marginal Utility Diminishing Returns (acquiring a 2nd pocket QB when you already have a 25-year-old 92-OVR QB yields near-zero marginal utility; trading away your *only* starting QB creates a catastrophic chasm).
- **Future Potential:** The exact same `TeamNeedIndex` (TNI) object can power Draft AI, Free Agency bidding priorities, and Trade Block automation across the entire simulation.
- **Constraints:** TNI bounded strictly to `[0.0, 1.0]`; applied symmetrically to **both** incoming acquisitions (`TNI_before`) and outgoing departures (`TNI_after_removal`).
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Compute need from `avg_rating = sum(p.overall_rating for p in players_at_pos) / count` and apply it only when `is_acquiring=True`.

### Powerful Antithesis
1. **The Backup Dilution Bug:** A team with Patrick Mahomes (99 OVR) and two 58-OVR camp arms has an average QB rating of `71.6`, fooling the old engine into thinking the Chiefs have a mediocre QB room!
2. **One-Sided Blindness:** Because need was only multiplied when `is_acquiring=True`, a team would happily trade away its only starting Left Tackle (`OT1`) for face value without pricing in the hole left behind.
3. **Youth Pipeline Ignorance:** A team with a 31-year-old starter (`82 OVR`) AND a 22-year-old `SUPERSTAR` rookie (`77 OVR`) waiting in the wings does *not* have a future need at that position.

### The Superior Synthesis
Implement `backend/app/services/trade_engine/context.py`:
1. Sort players at each position by effective starter value; evaluate the top `K = starters_required` starters separately from depth backups.
2. Compute `NeedNow` from starter gap (`(84 - starter_avg_ovr) / 18`) + depth gap.
3. Compute `NeedFuture` from starter age proximity to `peak_end` and expiring contracts (`contract_years <= 1`), **offset by the Youth Pipeline score** (any non-starter age $\le 24$ with `STAR/SUPERSTAR/XFACTOR` or projected 2-year OVR $\ge 80$).
4. Blend `TNI = (1 - h) * NeedNow + h * NeedFuture` using the team's `CompetitiveWindow` (`CONTENDER`, `BUBBLE`, `RETOOL`, `REBUILD`), and apply context multipliers to both incoming and outgoing players.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+ dataclasses.
- **Language:** Strict Python typing.
- **State Management:** Pure roster evaluation functions operating on in-memory `list[PlayerSnapshot]` rosters.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/services/trade_engine/context.py
from dataclasses import dataclass
from enum import StrEnum
from app.models.player import Position

class CompetitiveWindow(StrEnum):
    CONTENDER = "CONTENDER"  # delta = 0.70, h = 0.25
    BUBBLE = "BUBBLE"        # delta = 0.80, h = 0.40
    RETOOL = "RETOOL"        # delta = 0.88, h = 0.55
    REBUILD = "REBUILD"      # delta = 0.95, h = 0.70

@dataclass(frozen=True)
class PositionNeedDetail:
    position: Position
    need_now: float           # 0.0 - 1.0
    need_future: float        # 0.0 - 1.0
    youth_pipeline_offset: float
    tni: float                # Blended 0.0 - 1.0
    starter_ovr: float
```

### 3. Step-by-Step Execution

#### Task 3.1: Implement `classify_competitive_window` and `calculate_team_need_index`

**Objective:** Classify a team's competitive window and compute per-position `PositionNeedDetail` factoring in starters, depth, age cliffs, contract expirations, and youth pipeline offset.

**Files:**
- Create: `backend/app/services/trade_engine/context.py`
- Test: `backend/tests/unit/test_ctve_context.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_context.py
from app.models.player import DevelopmentTrait, Position
from app.services.trade_engine.context import (
    CompetitiveWindow,
    calculate_position_need,
    classify_competitive_window,
    evaluate_roster_context_multiplier,
)
from app.services.trade_engine.market import PlayerSnapshot


def test_youth_pipeline_reduces_future_need():
    aging_vet = PlayerSnapshot(
        id=1, position=Position.OT, overall_rating=83, age=32,
        contract_years=1, annual_base_salary=18_000_000,
    )
    young_heir = PlayerSnapshot(
        id=2, position=Position.OT, overall_rating=77, age=22,
        contract_years=3, annual_base_salary=2_000_000,
        development_trait=DevelopmentTrait.SUPERSTAR,
    )
    need_without_heir = calculate_position_need(
        Position.OT, [aging_vet], window=CompetitiveWindow.RETOOL
    )
    need_with_heir = calculate_position_need(
        Position.OT, [aging_vet, young_heir], window=CompetitiveWindow.RETOOL
    )
    assert need_with_heir.youth_pipeline_offset > 0.3
    assert need_with_heir.tni < need_without_heir.tni - 0.15


def test_trading_away_lone_starting_qb_has_high_departure_multiplier():
    qb1 = PlayerSnapshot(
        id=10, position=Position.QB, overall_rating=86, age=26,
        contract_years=3, annual_base_salary=35_000_000,
    )
    mult = evaluate_roster_context_multiplier(
        player=qb1, roster=[qb1], window=CompetitiveWindow.CONTENDER, is_acquiring=False
    )
    assert mult >= 1.30
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_context.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine.context'`

- [ ] **Step 3: Write minimal implementation**
Create `backend/app/services/trade_engine/context.py` implementing `CompetitiveWindow`, `classify_competitive_window`, `calculate_position_need`, and `evaluate_roster_context_multiplier` (including the incumbent-blocker cap `<= 0.70` when acquiring an older/lower-rated player behind a young entrenched starter, and `need_after_removal` when `is_acquiring=False`).

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_context.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/context.py backend/tests/unit/test_ctve_context.py
git commit -m "feat(trade-engine): add CompetitiveWindow, two-sided TeamNeedIndex, and youth pipeline offset"
```

### 4. Edge Cases & Error Handling

- **Empty position group on roster (`len == 0`):** `need_now = 1.0`, `tni = 1.0`, incoming starter multiplier `= 1.40`.
- **Early-season record (`games_played < 4`):** Weight Elo (`team.elo_rating`) and starter OVR `80%` over raw win percentage so a 0-1 powerhouse isn't misclassified as `REBUILD`.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/context.py` passes with 0 errors.
- [ ] **Security:** Read-only roster snapshot evaluation.
- [ ] **Performance:** Full 53-man roster TNI calculation completes in `< 0.5ms`.
- [ ] **Self-Critique:** Separating starter slots (`K = starters_required`) from backup depth solves the "Mahomes + two 58-OVR backups = 71 average" bug permanently.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-004` to implement the CBA Salary Cap & Dead Money 4-Year Projection Layer (`cap.py`).
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-004 — Phase 4: CBA Salary Cap Layer — Dead Money Acceleration & 4-Yr Projection

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** NFL Collective Bargaining Agreement (CBA) Article 13, Section 6 (Valuation of Traded Contracts):
  1. **Seller (Trading Team):** All remaining unamortized signing bonus proration (`signing_bonus_proration * min(5, contract_years + void_years)`) **immediately accelerates** onto the trading team's current-year salary cap as **Dead Money** (unless traded post-June 1, where years `1..N` defer to `year + 1`).
  2. **Buyer (Acquiring Team):** Absorbs **only** the remaining `annual_base_salary` (and future un-prorated base guarantees), with **zero** signing bonus proration from the prior team.
- **Related Ideas:** Double-entry cap accounting (`CapLedgerService`), multi-year cap horizon stress testing (`CapologyEngine`), and NBA/NFL "Brock Osweiler" salary-dump trades (buying draft picks with unused cap room).
- **Future Potential:** Connects trade execution directly to `CapLedgerService` (`TRADE_ACQUISITION` and `TRADE_OUTGOING` journal entries) so the Front Office Capology Heatmap updates in real time.
- **Constraints:** Hard rejection gate if Year-0 post-trade cap space `< 0` for either team; 4-year horizon (`y = 0..3`) projection with `SALARY_CAP_CAGR = 0.0697`.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Check `salary_cap_space < incoming_salary - outgoing_salary` for the current season only.

### Powerful Antithesis
1. **Violates the NFL CBA:** In the current code, if a player has a `$10M` base salary and `$15M` in remaining signing bonus proration (`$5M/yr` over 3 years), trading him away *frees* `$15M` in cap space in the current code, whereas in the real NFL it triggers `$15M` of accelerated dead money (`$0` net cap savings)!
2. **Multi-Year Cap Cliff Blindness:** A team with `$15M` in Year-0 cap space might acquire a player with backloaded `$35M` base salaries in Years 1–2 while its own rookie QB is due a `$55M` extension in Year 2.

### The Superior Synthesis
Build `backend/app/services/trade_engine/cap.py`:
1. Compute exact seller `dead_money_Immediate` (and Post-June-1 split when `is_post_june_1=True`) from `signing_bonus_proration`, `contract_years`, and `void_years`.
2. Project 4 years (`y = 0..3`) of `CapYearProjection` (`cap_before`, `cap_after`, `dead_money_delta`, `reserved_extensions`, `rookie_pool_reserve`) for **both** teams.
3. Enforce the Year-0 hard compliance gate (`cap_after[0] >= 0`) and compute a TVP-denominated `cap_stress_tvp` penalty for Year 1–3 shortfalls below a safety buffer (`$7.5M`).
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+, integrates with `app.core.nfl_reference_data.SALARY_CAP_CAGR` and `CapLedgerService`.
- **Language:** Python 3.11+ (strict typing, integer dollar math).
- **State Management:** Pure simulation during `/evaluate`; atomic ledger commit during `/respond/{offer_id}` accept.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/services/trade_engine/cap.py
from dataclasses import dataclass

@dataclass(frozen=True)
class CapYearProjection:
    year_offset: int          # 0, 1, 2, 3
    projected_league_cap: int
    space_before: int
    space_after: int
    net_cap_delta: int
    accelerated_dead_money: int
    reserved_extensions: int

@dataclass(frozen=True)
class TeamCapTradeImpact:
    team_id: int
    is_compliant_year0: bool
    dead_money_tvp_cost: float
    cap_stress_tvp_delta: float
    yearly_projections: list[CapYearProjection]
    rejection_reason: str | None = None
```

### 3. Step-by-Step Execution

#### Task 4.1: Implement CBA Signing Bonus Acceleration & 4-Year Cap Projection (`cap.py`)

**Objective:** Calculate seller dead-money acceleration, buyer base-salary absorption, extension reservations for young stars (`age <= 25, ovr >= 85, contract_years <= 2`), and 4-year cap stress in TVP.

**Files:**
- Create: `backend/app/services/trade_engine/cap.py`
- Test: `backend/tests/unit/test_ctve_cap.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_cap.py
from app.models.player import Position
from app.services.trade_engine.cap import evaluate_team_cap_impact
from app.services.trade_engine.market import PlayerSnapshot


def test_seller_absorbs_accelerated_signing_bonus_dead_money():
    # Player has $10M base salary + $6M/yr signing bonus proration for 3 years ($16M current cap hit)
    # When traded pre-June 1:
    # - Seller saves $10M base salary, but $18M total bonus accelerates ($12M extra beyond this year's $6M)
    # - Net Year-0 cap change for seller = -$2M (loses $2M cap space!)
    # - Buyer takes only $10M base salary (0 bonus proration)
    traded_star = PlayerSnapshot(
        id=50,
        position=Position.WR,
        overall_rating=90,
        age=27,
        contract_years=3,
        annual_base_salary=10_000_000,
        signing_bonus_proration=6_000_000,
        void_years=0,
    )
    seller_impact = evaluate_team_cap_impact(
        team_id=1,
        current_cap_space=20_000_000,
        incoming_players=[],
        outgoing_players=[traded_star],
        roster=[traded_star],
    )
    buyer_impact = evaluate_team_cap_impact(
        team_id=2,
        current_cap_space=20_000_000,
        incoming_players=[traded_star],
        outgoing_players=[],
        roster=[],
    )
    assert seller_impact.yearly_projections[0].accelerated_dead_money == 18_000_000
    assert seller_impact.yearly_projections[0].space_after == 18_000_000  # 20M + 10M base saved - 12M extra accel
    assert buyer_impact.yearly_projections[0].space_after == 10_000_000   # 20M - 10M base only
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_cap.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine.cap'`

- [ ] **Step 3: Write minimal implementation**
Create `backend/app/services/trade_engine/cap.py` with `calculate_trade_dead_money(player, is_post_june_1=False)` and `evaluate_team_cap_impact(...)`. When `space_after[0] < 0`, set `is_compliant_year0 = False` and populate `rejection_reason`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_cap.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/cap.py backend/tests/unit/test_ctve_cap.py
git commit -m "feat(trade-engine): add CBA signing bonus dead-money acceleration and 4-year cap projection"
```

### 4. Edge Cases & Error Handling

- **Player with `void_years > 0`:** Unamortized signing bonus in void years (`signing_bonus_proration * void_years`) also accelerates into the seller's dead money upon trade.
- **Legacy `Player` mock in unit tests with only `contract_salary` and no `annual_base_salary`:** Default `annual_base_salary = contract_salary` and `signing_bonus_proration = 0` so existing unit tests stay 100% compatible.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/cap.py` passes with 0 errors.
- [ ] **Security:** Integer arithmetic prevents floating-point rounding drift in cap checks.
- [ ] **Performance:** 4-year projection runs in `< 0.2ms`.
- [ ] **Self-Critique:** Accurately modeling dead-money acceleration stops the #1 exploit in football management games (signing free agents with massive signing bonuses and immediately flipping them for draft picks at zero cap cost).
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-005` to implement the Draft-Class Fit & Seeded Monte-Carlo Availability engine (`class_fit.py`).
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-005 — Phase 5: Draft-Class Fit — Seeded Monte-Carlo Availability & Run Risk

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** NFL War Room draft boards (e.g., Ravens/Eagles tier-drop probability models). A draft pick's value is not static across years or teams: Pick `#8` in a draft class with 4 blue-chip QBs is worth a fortune to a QB-needy team, whereas Pick `#8` when the top tier ends at Pick `#6` is a prime trade-down candidate.
- **Related Ideas:** Seeded Monte-Carlo simulation (`DeterministicRNG`), Order Statistics over noisy prospect boards, Positional Run Risk (probability that all Tier-1 prospects at a team's top need are drafted before their next pick).
- **Future Potential:** Powers both Trade Center pick valuations and live Draft Day trade-up / trade-down phone offers (`TradePhone.tsx`).
- **Constraints:** Must stay well under the `< 200ms` total trade evaluation budget via LRU caching keyed by `(season_id, remaining_prospect_ids_hash)` (`N = 100` fast vector trials, `< 15ms` cold, `< 0.05ms` cached).
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Use a static chart value for every pick regardless of who is in the draft class or what positions the picking team needs.

### Powerful Antithesis
If a draft class has zero 1st-round QBs, a QB-desperate team shouldn't pay a 3,000-point ransom to trade up to `#2`. Conversely, if a team needs `OT` and there are 5 starting-caliber OTs projected between picks `#25` and `#45`, trading *back* from `#24` to `#38` preserves almost 100% of their expected positional value while netting an extra 3rd-round pick.

### The Superior Synthesis
Implement `backend/app/services/trade_engine/class_fit.py`:
1. Run a seeded Monte-Carlo simulation (`N = 100` trials via `DeterministicRNG`) of picks `1..slot`, where each team ahead of `slot` selects from available prospects weighted by `prospect.overall_rating * (0.7 + 0.6 * team_tni[pos]) + N(0, sigma_board)`.
2. Compute `ClassFit_T(slot) = clamp(E[best_need_weighted_val_at_slot] / E[best_unweighted_val_at_slot], 0.85, 1.25)`.
3. Compute `PositionalRunRisk` (probability that the top tier at Team `T`'s #1 need position vanishes between `slot_A` and `slot_B`), driving trade-up urgency.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+, `DeterministicRNG` from `app.core.random_utils`, `functools.lru_cache`.
- **Language:** Python 3.11+ (strict typing).
- **State Management:** Cached availability probability matrix per draft state.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/services/trade_engine/class_fit.py
from dataclasses import dataclass
from app.models.player import Position

@dataclass(frozen=True)
class ProspectBoardEntry:
    prospect_id: int
    position: Position
    grade: float              # Scouting / overall grade (50 - 99)

@dataclass(frozen=True)
class PickClassFitResult:
    slot: int
    class_fit_multiplier: float       # [0.85, 1.25]
    expected_best_position: Position | None
    positional_run_risk: float        # [0.0, 1.0]
```

### 3. Step-by-Step Execution

#### Task 5.1: Build Seeded Monte-Carlo Draft Availability & `ClassFit` Calculator (`class_fit.py`)

**Objective:** Compute `evaluate_pick_class_fit` and `calculate_positional_run_risk` deterministically with `< 15ms` cold execution.

**Files:**
- Create: `backend/app/services/trade_engine/class_fit.py`
- Test: `backend/tests/unit/test_ctve_class_fit.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_class_fit.py
from app.models.player import Position
from app.services.trade_engine.class_fit import (
    ProspectBoardEntry,
    evaluate_pick_class_fit,
)


def test_qb_rich_top5_boosts_pick_value_for_qb_needy_team():
    prospects = [
        ProspectBoardEntry(1, Position.QB, 94.0),
        ProspectBoardEntry(2, Position.QB, 92.0),
        ProspectBoardEntry(3, Position.QB, 90.0),
        ProspectBoardEntry(4, Position.WR, 82.0),
        ProspectBoardEntry(5, Position.OT, 81.0),
        ProspectBoardEntry(6, Position.CB, 80.0),
    ]
    qb_needy_tni = {pos: (1.0 if pos == Position.QB else 0.2) for pos in Position}
    qb_set_tni = {pos: (0.05 if pos == Position.QB else 0.5) for pos in Position}

    fit_needy = evaluate_pick_class_fit(
        slot=2, prospects=prospects, evaluating_team_tni=qb_needy_tni, seed=42
    )
    fit_set = evaluate_pick_class_fit(
        slot=2, prospects=prospects, evaluating_team_tni=qb_set_tni, seed=42
    )
    assert fit_needy.class_fit_multiplier > 1.10
    assert fit_needy.class_fit_multiplier > fit_set.class_fit_multiplier + 0.15
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_class_fit.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine.class_fit'`

- [ ] **Step 3: Write minimal implementation**
Implement `ProspectBoardEntry`, `PickClassFitResult`, and `evaluate_pick_class_fit` in `backend/app/services/trade_engine/class_fit.py`. When `prospects` is empty (e.g., future draft classes not yet generated), return neutral `class_fit_multiplier = 1.0`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_class_fit.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/class_fit.py backend/tests/unit/test_ctve_class_fit.py
git commit -m "feat(trade-engine): add seeded Monte-Carlo draft class fit and positional run risk"
```

### 4. Edge Cases & Error Handling

- **Future draft years with no generated prospects (`len(prospects) == 0`):** Return `PickClassFitResult(slot=slot, class_fit_multiplier=1.0, expected_best_position=None, positional_run_risk=0.0)`.
- **Late-round picks (`slot > len(prospects)`):** Return `class_fit_multiplier = 1.0` gracefully.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/class_fit.py` passes with 0 errors.
- [ ] **Security:** Seeded `DeterministicRNG` ensures identical inputs always produce identical trade evaluations.
- [ ] **Performance:** Cached by prospect board tuple hash; cold run `< 12ms`, cached run `< 0.05ms`.
- [ ] **Self-Critique:** Bounding `class_fit_multiplier` to `[0.85, 1.25]` prevents extreme draft-board outliers from breaking overall pick market hierarchy.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-006` to implement the 5 Hyper-Realism Modifiers (`modifiers.py`).
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-006 — Phase 6: The 5 Hyper-Realism Modifiers

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Real-world NFL front office dynamics that pure stat charts miss:
  1. **Injury & Durability Risk (`R_risk`):** Active `InjuryStatus` (`OUT`/`IR`), chronic wear/tear, and team `medical_rating` risk tolerance.
  2. **Scheme & Coaching Fit (`M_scheme`):** Alignment between player skill attributes (`man_coverage` vs `zone_coverage`, 3-4 OLB vs 4-3 DE) and the acquiring team's `gameplan` / `Coach` scheme.
  3. **Locker Room Morale & Trade Requests (`M_morale`):** Disgruntled stars (`morale < 30` or `tension_score > 75`) force their way out at a `-12%` to `-20%` seller leverage discount (Stefon Diggs / Haason Reddick / Davante Adams precedent).
  4. **Market Leverage, Deadline Urgency & Comp-Pick Floor (`M_market`):** An expiring star will never be traded by a seller for less than the **Compensatory Pick TVP** (`CapologyEngine.evaluate_comp_pick_formula`) they would receive by letting him walk in free agency; trade deadline proximity increases contender urgency.
  5. **GM Relationship Graph & Division Rivalry Tax (`M_rivalry`):** Intra-division trades carry a `+12%` acceptance threshold tax (`same conference + same division`), plus historical trade memory from `GMDecision` logs and GM hot-seat panic (`owner_trust < 35`).
- **Related Ideas:** Behavioral Game Theory, Reservation Price (BATNA = Compensatory Pick value), Bilateral Monopoly Bargaining.
- **Future Potential:** Emits rich, emergent narrative explanations in `reasoning` (e.g., *"Division Rival Tax (+12%): Green Bay refuses to help an NFC North rival without a premium"*, *"Compensatory Pick Floor: Seller projects a 3rd-round comp pick (668 TVP) if player walks"*).
- **Constraints:** All 5 modifiers must use fields that already exist on `Player`, `Team`, `GM`, and `CapologyEngine` (with safe defaults when optional relationships are unloaded).
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Use a random LLM/news text check (`_get_llm_trade_opinion`) that adds `+5` for a 90+ OVR player and `-5` if the word `"injury"` appears in a headline.

### Powerful Antithesis
A flat `±5` point modifier on a 3,000-point scale is `0.16%`—completely imperceptible! Worse, ignoring division rivalries lets the user trade stars freely inside their own division at zero markup, and ignoring the Compensatory Pick floor lets users buy expiring 88-OVR rental players at the trade deadline for a 7th-round pick (`100 TVP`) when the seller would get a 3rd-round comp pick (`~670 TVP`) by keeping him.

### The Superior Synthesis
Implement `backend/app/services/trade_engine/modifiers.py` with multiplicative, bounded, explainable modifiers for all 5 realism dimensions, returning both numeric adjustments (`player_multiplier`, `threshold_delta`, `comp_pick_floor_tvp`) and human-readable narrative tags.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** Python 3.11+ dataclasses, `CapologyEngine.evaluate_comp_pick_formula`.
- **Language:** Python 3.11+ (strict typing).
- **State Management:** Pure functions consuming `PlayerSnapshot` and `TeamContextSnapshot`.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/services/trade_engine/modifiers.py
from dataclasses import dataclass, field

@dataclass(frozen=True)
class RealismEvaluation:
    injury_risk_mult: float = 1.0           # [0.60, 1.00]
    scheme_fit_mult: float = 1.0            # [0.85, 1.12]
    morale_leverage_mult: float = 1.0       # [0.80, 1.08]
    comp_pick_floor_tvp: float = 0.0        # Reservation price for expiring FAs
    rivalry_threshold_delta: float = 0.0    # +0.12 intra-division, +0.04 intra-conference
    urgency_threshold_delta: float = 0.0    # Negative when deadline/hot-seat/QB panic active
    narrative_notes: list[str] = field(default_factory=list)
```

### 3. Step-by-Step Execution

#### Task 6.1: Implement the 5 Realism Modifiers in `modifiers.py`

**Objective:** Implement injury durability discount, scheme fit, morale/holdout discount, compensatory pick reservation floor, and division rivalry / hot-seat GM threshold adjustments.

**Files:**
- Create: `backend/app/services/trade_engine/modifiers.py`
- Test: `backend/tests/unit/test_ctve_modifiers.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_modifiers.py
from app.models.player import InjuryStatus, Position
from app.services.trade_engine.market import PlayerSnapshot
from app.services.trade_engine.modifiers import (
    TeamContextProfile,
    evaluate_player_realism_modifiers,
    evaluate_trade_relationship_modifiers,
)


def test_division_rivalry_adds_12_percent_threshold_tax():
    t1 = TeamContextProfile(team_id=1, conference="NFC", division="East", owner_trust=60)
    t2 = TeamContextProfile(team_id=2, conference="NFC", division="East", owner_trust=60)
    rel = evaluate_trade_relationship_modifiers(offering_team=t1, receiving_team=t2)
    assert rel.rivalry_threshold_delta >= 0.12
    assert any("Division" in note for note in rel.narrative_notes)


def test_expiring_star_enforces_compensatory_pick_floor():
    expiring_star = PlayerSnapshot(
        id=77, position=Position.DE, overall_rating=89, age=27,
        contract_years=1, annual_base_salary=22_000_000,
    )
    seller = TeamContextProfile(team_id=2, conference="AFC", division="North")
    buyer = TeamContextProfile(team_id=1, conference="NFC", division="West")
    mod = evaluate_player_realism_modifiers(
        player=expiring_star, acquiring_team=buyer, selling_team=seller, is_acquiring=False
    )
    # 89 OVR DE commands top-tier FA deal -> 3rd-round comp pick floor (~450+ TVP after 1-yr discount)
    assert mod.comp_pick_floor_tvp >= 450.0


def test_disgruntled_holdout_player_reduces_seller_leverage():
    holdout_wr = PlayerSnapshot(
        id=88, position=Position.WR, overall_rating=91, age=27,
        contract_years=2, annual_base_salary=24_000_000,
        morale=20, tension_score=85.0,
    )
    seller = TeamContextProfile(team_id=2, conference="AFC", division="North")
    buyer = TeamContextProfile(team_id=1, conference="NFC", division="West")
    mod = evaluate_player_realism_modifiers(
        player=holdout_wr, acquiring_team=buyer, selling_team=seller, is_acquiring=False
    )
    assert mod.morale_leverage_mult <= 0.85
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_modifiers.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine.modifiers'`

- [ ] **Step 3: Write minimal implementation**
Create `backend/app/services/trade_engine/modifiers.py` implementing `TeamContextProfile`, `RealismEvaluation`, `evaluate_player_realism_modifiers`, and `evaluate_trade_relationship_modifiers`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_modifiers.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/modifiers.py backend/tests/unit/test_ctve_modifiers.py
git commit -m "feat(trade-engine): add 5 hyper-realism modifiers (injury, scheme, morale, comp floor, rivalry)"
```

### 4. Edge Cases & Error Handling

- **Player on `IR` or `OUT`:** `injury_risk_mult` scales down to `0.65 - 0.80` depending on acquiring team's `medical_rating`, and adds an explicit `"Medical Flag"` note in `narrative_notes`.
- **Missing `conference` or `division` on mocked teams:** Treat as non-rival (`rivalry_threshold_delta = 0.0`).

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** `mypy backend/app/services/trade_engine/modifiers.py` passes cleanly.
- [ ] **Security:** All modifiers are deterministic and side-effect free.
- [ ] **Performance:** `< 0.1ms` per trade evaluation.
- [ ] **Self-Critique:** Pricing the Compensatory Pick floor directly from `CapologyEngine` unifies the Free Agency and Trade subsystems so AI GMs never give away expiring stars for less than their compensatory return.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to `TASK-CTVE-007` to implement the Ratio Decision Layer, Knapsack Counter-Offer generator (`decision.py`), wire into `GMAgent`, and upgrade the React UI (`TradeAnalyzer.tsx`).
</baton_handoff>

---

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-CTVE-007 — Phase 7: Ratio Grading, Knapsack Counter-Offers & Frontend Dual-Grade UI

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Relative Ratio Valuation ($R_T = V_{\text{in}} / V_{\text{out}}$) rather than absolute difference ($V_{\text{in}} - V_{\text{out}}$). A 50-TVP gap on a 3,500-TVP blockbuster is a `1.4%` rounding error (an `A-/B+` win-win), whereas a 50-TVP gap on a 120-TVP 6th-round swap is a `42%` fleece (`F`).
- **Related Ideas:** Bounded Knapsack optimization for automated counter-proposals (finding the smallest sweetener from the user's picks or surplus depth at AI top-3 needs that brings $R_{\text{AI}} \ge \tau_{\text{AI}}$).
- **Future Potential:** Dual-side grading (`user_side` and `ai_side`) powers post-trade media report cards in `WeeklyRecapService` and draft-day trade grades.
- **Constraints:** Backward-compatible `TradeEvaluationResponse` (retaining `decision`, `score`, `reasoning`, `offered_value`, `requested_value`, `gm_philosophy` while adding `user_grade`, `ai_grade`, `factor_breakdown`, `cap_projections`, and `counter_offer`); zero `any` in TypeScript.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Replace `TradeEvaluationResponse` with an incompatible schema and only return `ACCEPT` or `REJECT`.

### Powerful Antithesis
1. Breaking `decision`, `score`, or `reasoning` on `TradeEvaluationResponse` would break existing integration tests (`test_trade_evaluation.py`, `test_gm_agent.py`, `test_trade_api.py`).
2. Returning only `REJECT` without a concrete `counter_offer` forces the user to play a frustrating guessing game of clicking "Analyze" 20 times to find what the AI wants.

### The Superior Synthesis
1. Implement `decision.py` computing:
   - `ratio = value_in / max(1.0, value_out + dead_money_tvp_cost + cap_stress_tvp_delta)`
   - Letter grade mapping (`A+` for $\ge 1.25$ down to `F` for $< 0.75$) for **both** teams.
   - Normalized `score = round((ai_ratio - tau) * 100.0, 1)` (where `0.0` is the exact acceptance line, `+12.5` means `+12.5%` surplus above the GM's threshold, and `-8.0` means `8%` short—ending the confusing `-204.28023350526902` mystery!).
   - When `0.80 <= ai_ratio < tau`, run the knapsack sweetener search over the offering team's draft picks and tradable players at the AI team's top-3 TNI positions to populate `counter_offer`.
2. Wire `ContextualTradeEngine` into `GMAgent.evaluate_trade` and `/api/trades/evaluate`, and update `TradeAnalyzer.tsx` & `tradeApi.ts` to display TVP totals, dual `A+..F` grades, 7-factor breakdown bars, 4-year cap delta summary, and a 1-click **"Apply Counter-Offer"** button.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** FastAPI, Pydantic v2, React 19, TypeScript 5.5+, TailwindCSS / CSS modules.
- **Language:** Python 3.11+ & TypeScript 5.5+ (strict, 0 `any`).
- **State Management:** Unified backend TVP calculation served via `/api/trades/evaluate` and `/api/teams/{team_id}/roster`.

### 2. The Data Schema (Pre-Generation)

```python
# backend/app/schemas/trade.py additions (backward-compatible extension)
from typing import Literal

TradeLetterGrade = Literal["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]

class FactorBreakdownSchema(BaseModel):
    market_tvp: float
    need_fit_delta: float
    cap_impact_delta: float
    window_fit_delta: float
    class_fit_delta: float
    realism_modifiers_delta: float
    gm_threshold: float

class TeamSideGradeSchema(BaseModel):
    team_id: int
    competitive_window: str
    value_in_tvp: float
    value_out_tvp: float
    ratio: float
    grade: TradeLetterGrade
    factors: FactorBreakdownSchema

class CounterOfferSuggestion(BaseModel):
    add_player_ids: list[int] = Field(default_factory=list)
    add_picks: list[DraftPickInfo] = Field(default_factory=list)
    summary: str
```

### 3. Step-by-Step Execution

#### Task 7.1: Implement Ratio Grading & Knapsack Counter-Offer Engine (`decision.py`)

**Objective:** Build `backend/app/services/trade_engine/decision.py` orchestrating Market, Pick, Context, Cap, ClassFit, and Realism layers into a complete `TradeDecisionResult` with knapsack counter-offers.

**Files:**
- Create: `backend/app/services/trade_engine/decision.py`
- Test: `backend/tests/unit/test_ctve_decision.py`

- [ ] **Step 1: Write failing test**
```python
# backend/tests/unit/test_ctve_decision.py
from app.models.player import Position
from app.services.trade_engine.decision import (
    evaluate_trade_package,
    ratio_to_letter_grade,
)
from app.services.trade_engine.market import PlayerSnapshot
from app.services.trade_engine.picks import PickValuationInput


def test_ratio_to_letter_grade_scale():
    assert ratio_to_letter_grade(1.30) == "A+"
    assert ratio_to_letter_grade(1.00) == "B"
    assert ratio_to_letter_grade(0.70) == "F"


def test_close_trade_generates_knapsack_counter_offer():
    # User offers an 83 OVR WR for AI's 86 OVR WR (close, ~0.86 ratio -> triggers counter-offer)
    offered = [PlayerSnapshot(id=1, position=Position.WR, overall_rating=83, age=26, contract_years=2, annual_base_salary=10_000_000)]
    requested = [PlayerSnapshot(id=2, position=Position.WR, overall_rating=86, age=26, contract_years=2, annual_base_salary=12_000_000)]
    available_user_picks = [
        PickValuationInput(round=3, year=2025, current_year=2025, projected_slot_in_round=16),
        PickValuationInput(round=5, year=2025, current_year=2025, projected_slot_in_round=16),
    ]
    res = evaluate_trade_package(
        offered_players=offered,
        requested_players=requested,
        offered_picks=[],
        requested_picks=[],
        available_counter_picks=available_user_picks,
    )
    assert res.ai_side.ratio < res.ai_threshold
    assert res.counter_offer is not None
    assert len(res.counter_offer.add_picks) >= 1
```

- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/unit/test_ctve_decision.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.trade_engine.decision'`

- [ ] **Step 3: Write minimal implementation**
Create `backend/app/services/trade_engine/decision.py` with `ratio_to_letter_grade`, `find_minimal_counter_offer`, and `evaluate_trade_package`.

- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/unit/test_ctve_decision.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add backend/app/services/trade_engine/decision.py backend/tests/unit/test_ctve_decision.py
git commit -m "feat(trade-engine): add ratio letter grading and knapsack counter-offer generator"
```

#### Task 7.2: Wire `ContextualTradeEngine` into `GMAgent` & `/api/trades/evaluate`

**Objective:** Connect `GMAgent.evaluate_trade` and `/api/trades/evaluate` to `trade_engine/decision.py`, returning both legacy fields and rich V2 breakdown fields.

**Files:**
- Modify: `backend/app/schemas/trade.py:48-68`
- Modify: `backend/app/services/gm_agent.py:43-150`
- Modify: `backend/app/api/endpoints/trades.py:85-178`
- Test: `backend/tests/integration/test_trade_evaluation.py`, `backend/tests/test_gm_agent.py`

- [ ] **Step 1: Write failing test**
Add assertion in `backend/tests/integration/test_trade_evaluation.py` checking that `/api/trades/evaluate` returns `offered_value`, `requested_value`, `ai_side.grade`, `user_side.grade`, and rounded `score`.
- [ ] **Step 2: Run test to verify failure**
Run: `pytest backend/tests/integration/test_trade_evaluation.py backend/tests/test_gm_agent.py backend/tests/test_trade_api.py -v`
Expected: FAIL — `ai_side` not present on response.
- [ ] **Step 3: Write minimal implementation**
Update `TradeEvaluationResponse` in `backend/app/schemas/trade.py`, wire `GMAgent.evaluate_trade` to `evaluate_trade_package`, and populate the extended response fields in `backend/app/api/endpoints/trades.py`.
- [ ] **Step 4: Run test to verify pass**
Run: `pytest backend/tests/integration/test_trade_evaluation.py backend/tests/test_gm_agent.py backend/tests/test_trade_api.py -v`
Expected: PASS
- [ ] **Step 5: Commit**
```bash
git add backend/app/schemas/trade.py backend/app/services/gm_agent.py backend/app/api/endpoints/trades.py backend/tests/integration/test_trade_evaluation.py
git commit -m "feat(api): wire Contextual Trade Value Engine into GMAgent and /api/trades/evaluate"
```

#### Task 7.3: Upgrade Frontend `TradeAnalyzer.tsx`, `trade.ts` & `tradeApi.ts`

**Objective:** Replace the frontend's dummy `OVR + age` calculation with the TVP curve, render dual-team letter grades (`Your Grade` / `Their GM Grade`), factor breakdown pills, and counter-offer display in `TradeAnalyzer.tsx`.

**Files:**
- Modify: `frontend/src/types/trade.ts`
- Modify: `frontend/src/services/tradeApi.ts`
- Modify: `frontend/src/components/trades/TradeAnalyzer.tsx`
- Test: `frontend/src/components/trades/__tests__/TradeAnalyzer.test.tsx`

- [ ] **Step 1: Write failing test**
Write Vitest test asserting `TradeAnalyzer` renders `ai_side.grade`, `user_side.grade`, rounded fairness percentage score, and counter-offer suggestion when returned by `/api/trades/evaluate`.
- [ ] **Step 2: Run test to verify failure**
Run: `npm --prefix frontend test -- TradeAnalyzer`
Expected: FAIL
- [ ] **Step 3: Write minimal implementation**
Update `TradeEvaluation` interface in `frontend/src/types/trade.ts`, update `calculateTradeValue` in `frontend/src/services/tradeApi.ts` to match the backend TVP scale, and render the dual-grade badges, factor breakdown, and counter-offer banner in `frontend/src/components/trades/TradeAnalyzer.tsx`.
- [ ] **Step 4: Run test to verify pass**
Run: `npm --prefix frontend test -- TradeAnalyzer`
Expected: PASS
- [ ] **Step 5: Commit**
```bash
git add frontend/src/types/trade.ts frontend/src/services/tradeApi.ts frontend/src/components/trades/TradeAnalyzer.tsx
git commit -m "feat(ui): display TVP currency, dual-team trade grades, factor breakdown, and counter-offers"
```

### 4. Edge Cases & Error Handling

- **Division by zero when `value_out <= 0` (e.g., acquiring a salary-dump player with negative TVP):** Floor the denominator at `max(50.0, value_out + dead_money_tvp_cost + cap_stress_tvp_delta)` and add negative outgoing TVP to the numerator as a liability-relief credit.
- **No viable 1-or-2-asset knapsack counter-offer found:** Return `counter_offer = None` and explain in `reasoning` that the value gap is too wide for a simple sweetener.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Zero `any` types in `frontend/src/types/trade.ts`, `frontend/src/services/tradeApi.ts`, and `frontend/src/components/trades/TradeAnalyzer.tsx`; `mypy` clean across `backend/app/services/trade_engine/`.
- [ ] **Security:** All player and pick IDs validated against team ownership before execution.
- [ ] **Performance:** End-to-end `POST /api/trades/evaluate` latency `< 50ms` (well below the `< 200ms` SLA).
- [ ] **Self-Critique:** Retaining `decision` (`ACCEPT`/`REJECT`) on `TradeEvaluationResponse` while surfacing `counter_offer` as a structured object keeps 100% of existing API consumers working while giving the UI full counter-offer power.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: Execute `TASK-CTVE-000` through `TASK-CTVE-007` sequentially using TDD verification after each task.
</baton_handoff>

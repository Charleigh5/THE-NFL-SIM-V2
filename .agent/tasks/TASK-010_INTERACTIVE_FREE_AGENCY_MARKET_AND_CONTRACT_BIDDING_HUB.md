<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK_010_INTERACTIVE_FREE_AGENCY_MARKET_AND_CONTRACT_BIDDING_HUB

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Modern NFL free agency is an intricate multi-round marketplace defined by the NFL Collective Bargaining Agreement (CBA), hard salary caps, signing bonus proration (spread evenly up to 5 contract years), guaranteed money risk, and the "Rule of 51" offseason cap accounting.
  - In `THE-NFL-SIM-V2 ("The Digital Gridiron")`, free agency was previously confined to a monolithic batch simulation (`simulate_free_agency`) that executed all signings in a single synchronous backend sweep.
  - The franchise General Manager requires an interactive, real-time war room where they can actively scout free agents by position, overall rating (OVR), scheme fit, and age, architect nuanced multi-year contract offers, monitor real-time cap health, and engage in high-stakes bidding battles against aggressive AI General Managers.

- **Related Ideas & Industry Parallels:**
  - *Spotrac / OverTheCap*: Contract capology, annual average value (AAV), rolling guarantee mechanisms, and dead cap liability models.
  - *Football Manager Contract Negotiation Loop*: Multi-clause agent negotiations with live player interest meters, patience bars, and rival club poaching alerts.
  - *Madden Franchise Free Agency Hub*: 3-stage bidding period with points-based player evaluation (Cash, Role, Contender, Scheme Fit).

- **Future Potential (2026/2027):**
  - Void years, rolling option bonuses, performance escalators, franchise tag tenders, and compensatory draft pick forecasting algorithms.

- **Constraints:**
  - Strict Rule of 51 salary cap verification: A team cannot exceed the NFL hard cap ($255.4M standard).
  - Sub-150ms evaluation latency for contract adjustments.
  - Zero `any` types across backend Pydantic models and frontend TypeScript interfaces.
  - Deterministic AI counter-bidding logic with no unbounded infinite bidding loops.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Expose a single CRUD endpoint `POST /api/free-agency/sign` where the user selects a free agent, fills in APY and Years, and the backend verifies `team.salary_cap_space >= offer.aav` before immediately assigning the player to the user's roster.

### Powerful Antithesis
- **Financial Naivety**: Comparing raw AAV to cap space violates NFL capology. A $30M AAV deal with a $20M signing bonus over 5 years has a Year 1 cap hit of only $14M ($10M base + $4M prorated bonus). Naive AAV validation needlessly blocks legitimate cap management maneuvers.
- **Sterile Experience**: Instant signings eliminate the competitive pressure and drama of the NFL offseason. In reality, elite free agents receive simultaneous bids from 3-5 contending teams.
- **Concurrency & Double-Spend**: Without database transaction locking, a user could submit offers to multiple players simultaneously that exceed total available cap space.
- **Roster Overflow**: Fails to enforce the standard 53-man (or 90-man offseason) roster limits.

### The Superior Synthesis
Architect a **Reactive 4-Stage Asynchronous Bidding Engine**:
1. **Interactive Market Browser**: Full-text, multi-facet filtering (Position, Age, OVR, Scheme Fit, Demanded AAV) with server-side pagination and real-time scheme compatibility scoring.
2. **Contract Structuring Studio**: Dual-input slider/stepper workbench computing Year 1 Cap Hit, Total Value, Prorated Bonus, Guaranteed Money, and dynamic Rule of 51 impact before submission.
3. **Player Interest & Sentiment Algorithm**: Multi-factor evaluation function:
   $$\text{Interest} = w_m \cdot \text{MoneyScore} + w_s \cdot \text{SchemeFit} + w_c \cdot \text{ContenderScore} + w_r \cdot \text{StarterRoleGuarantee}$$
   Returning transparent agent feedback ("Demanding higher guaranteed percentage", "Excited by championship potential", "Insulting lowball offer").
4. **AI GM Counter-Bidding Federation**: When the user places a high-interest bid, rival teams with positional need ($> 35.0$) and cap space submit counter-bids across 3 simulated bidding rounds, forcing the user to raise, hold, or concede.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Backend:** FastAPI (Python 3.11+), SQLAlchemy 2.0 Async/Sync, Pydantic V2.
- **Frontend:** React 19, TypeScript 5+, Vite, Lucide Icons, Framer Motion, Zustand.
- **State Management:** `useFreeAgencyStore.ts` synchronized with active franchise ID from `useTeamStore.ts`.
- **Styling:** Tailwind CSS + Vanilla CSS Modules adhering to Madden/NCAA gridiron dark-mode aesthetics (`#0a0f1d`, neon cyan `#00e5ff`, gold `#f59e0b`).

### 2. The Data Schema (Pre-Generation)

#### Backend Pydantic Schemas (`backend/app/schemas/free_agency.py`)

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class FreeAgentQueryFilters(BaseModel):
    position: Optional[str] = None
    min_ovr: int = Field(default=60, ge=50, le=99)
    max_ovr: int = Field(default=99, ge=50, le=99)
    max_age: Optional[int] = Field(default=None, ge=20, le=45)
    scheme: Optional[str] = None
    sort_by: str = Field(default="overall_rating", pattern="^(overall_rating|age|demanded_aav)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

class ContractOfferRequest(BaseModel):
    player_id: int
    team_id: int
    years: int = Field(ge=1, le=7)
    base_salary_annual: int = Field(ge=950_000, le=60_000_000)
    signing_bonus_total: int = Field(default=0, ge=0, le=120_000_000)
    guaranteed_total: int = Field(default=0, ge=0)

class YearByYearCapBreakdown(BaseModel):
    year: int
    base_salary: int
    prorated_bonus: int
    total_cap_hit: int
    dead_cap_if_cut: int

class ContractEvaluationResponse(BaseModel):
    player_id: int
    team_id: int
    total_value: int
    aav: int
    year_one_cap_hit: int
    current_team_cap_space: int
    projected_remaining_cap: int
    is_cap_compliant: bool
    cap_violation_amount: int = 0
    player_interest_score: float = Field(ge=0.0, le=100.0)
    likelihood: str = Field(description="'VERY_HIGH', 'HIGH', 'MODERATE', 'LOW', 'UNLIKELY'")
    agent_feedback: str
    breakdown: List[YearByYearCapBreakdown]

class AIBidResponse(BaseModel):
    round_number: int
    bids: List[Dict[str, Any]]
    user_status: str  # "LEADING", "OUTBID", "ACCEPTED", "REJECTED"
    top_bid_team_name: str
    top_bid_aav: int
    top_bid_years: int
```

#### Frontend TypeScript Interfaces (`frontend/src/types/freeAgency.ts`)

```typescript
export interface FreeAgentPlayer {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  overall_rating: number;
  age: number;
  demanded_aav: number;
  demanded_years: number;
  demanded_guaranteed: number;
  scheme_fit_score: number; // 0-100
  scheme_fit_label: "ELITE" | "GOOD" | "AVERAGE" | "POOR";
  interested_teams_count: number;
  status: "AVAILABLE" | "OFFER_PENDING" | "SIGNED";
}

export interface ContractOffer {
  playerId: number;
  teamId: number;
  years: number;
  baseSalaryAnnual: number;
  signingBonusTotal: number;
  guaranteedTotal: number;
}
```

### 3. Step-by-Step Execution

#### Step 1: Scaffolding
- [ ] Create schema file `backend/app/schemas/free_agency.py` with strict Pydantic V2 models.
- [ ] Create endpoint router `backend/app/api/endpoints/free_agency.py` and register in `backend/app/main.py`.
- [ ] Create TypeScript types `frontend/src/types/freeAgency.ts`.
- [ ] Create frontend API client `frontend/src/services/freeAgencyApi.ts`.
- [ ] Create Zustand store `frontend/src/store/useFreeAgencyStore.ts`.

#### Step 2: Core Logic Implementation
- [ ] **Subtask 2.1: Free Agent Query Engine**
  - Implement `get_free_agents_paginated` in `backend/app/services/free_agency_engine.py` with dynamic filters (OVR, Position, Age, Scheme Fit).
- [ ] **Subtask 2.2: NFL Capology & Proration Calculator**
  - Implement `calculate_contract_breakdown(years, base_salary, signing_bonus, guaranteed)` adhering to the 5-year bonus proration limit.
  - Implement real-time Rule of 51 cap space audit comparing Year 1 cap hit against team current effective cap.
- [ ] **Subtask 2.3: Player Valuation & Agent Feedback Synthesizer**
  - Implement `evaluate_user_offer` calculating multidimensional interest score factoring in market AAV delta, guarantee ratio, contender status, and depth chart vacancy.
- [ ] **Subtask 2.4: Multi-Team AI Counter-Bidding Engine**
  - Implement `simulate_bidding_round(player_id, user_offer)`: GMs identify high-need rivals, compute escalation bids (+5% to +15% AAV), and return active bidding board state.
- [ ] **Subtask 2.5: Atomic Contract Execution & Roster Signing**
  - Implement `execute_free_agent_signing` using SQLAlchemy transaction isolation: inserts `PlayerContract`, updates `Player.team_id`, creates contract transaction log, and deducts team cap space.

#### Step 3: Interface & Experience
- [ ] **Subtask 3.1: Free Agency Market View (`FreeAgencyHub.tsx`)**
  - Build responsive grid/table with position badges, OVR color coding (90+ Teal, 80+ Green, 70+ Yellow), scheme fit meters, and search bar.
- [ ] **Subtask 3.2: Contract Builder Studio Modal (`ContractBuilderModal.tsx`)**
  - Build tactile sliders for Contract Length (1-7 Years), Annual Base Salary ($1M-$50M), Signing Bonus ($0M-$60M), and Total Guaranteed.
  - Integrate live Year-by-Year Cap Hit table with animated SVG cap impact bar.
- [ ] **Subtask 3.3: Live Agent Sentiment & Interest Gauge**
  - Animated semicircular gauge (0-100%) displaying player willingness with instant agent quote bubble.
- [ ] **Subtask 3.4: Bidding War War-Room Feed (`BiddingWarTicker.tsx`)**
  - Staggered Framer Motion feed displaying rival AI GM bids ("Chiefs offer 3yr/$48M", "Cowboys drop out").

### 4. Edge Cases & Error Handling

- [Case A: Negative or Insufficient Cap Space] -> Contract builder disables "Submit Offer" button, highlights deficit in crimson (`#ef4444`), and suggests bonus restructuring.
- [Case B: Roster Limit Exceeded (53/53)] -> Modal prompts GM that signing requires waiving/cutting a player before contract finalization.
- [Case C: AI Outbids at Deadline] -> User receives visual high-priority alert with 30-second timer to submit counter-offer or withdraw.
- [Case D: Zero Free Agents Available] -> Renders high-fidelity "Offseason Market Closed" empty state.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Zero `any` types in `free_agency.py` and `freeAgency.ts`. Validated via `pyright` and `tsc --noEmit`.
- [ ] **Security:** Team ID authenticated against user session; contract values validated against integer overflow and negative limits.
- [ ] **Performance:** Market browsing query response time $< 80$ms using composite SQL index `(team_id, is_rookie, is_retired, overall_rating)`.
- [ ] **Self-Critique:** Are AI counter-bids deterministic? Yes, random seeds tied to `(season_id, player_id, round_number)` guarantee replay consistency.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Execute Task Scaffolding and build backend `backend/app/api/endpoints/free_agency.py` with associated test suite.
</baton_handoff>

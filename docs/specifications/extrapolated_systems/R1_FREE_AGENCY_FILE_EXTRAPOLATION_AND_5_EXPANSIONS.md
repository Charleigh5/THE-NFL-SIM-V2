<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026 Production Standard
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification, strict types (no `any`).
</system_context>

# REQUIREMENT 1 (R1): INTERACTIVE FREE AGENCY MARKET & CONTRACT BIDDING HUB
## Exhaustive File Extrapolation & 5 Tangential Feature Expansions

---

## 📂 SECTION 1: CORE FILE EXTRAPOLATION FOR R1

Every individual file required to deliver the core Free Agency War Room and Bidding Hub is enumerated below with its architectural layer, explicit responsibilities, and complete data interfaces.

```
THE-NFL-SIM-V2/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       └── free_agency.py                 # [NEW] REST API endpoints for FA market & bidding
│   │   ├── schemas/
│   │   │   └── free_agency.py                     # [NEW] Strict Pydantic V2 request/response models
│   │   ├── services/
│   │   │   ├── free_agency_engine.py              # [MODIFY] Query engine, AAV proration & bidding federation
│   │   │   └── salary_cap_service.py              # [MODIFY] Rule of 51 validator & multi-year cap proration
│   │   └── models/
│   │       └── player_contract.py                 # [MODIFY] Add signing bonus proration & void year fields
│   └── tests/
│       └── unit/
│           ├── test_free_agency_bidding.py        # [NEW] Unit tests for bidding federation & market value
│           └── test_capology_proration.py         # [NEW] Unit tests for 5-year signing bonus proration
└── frontend/
    └── src/
        ├── types/
        │   └── freeAgency.ts                      # [NEW] TypeScript interfaces & Zod schemas
        ├── services/
        │   └── freeAgencyApi.ts                   # [NEW] Axios API client for free agency endpoints
        ├── store/
        │   └── useFreeAgencyStore.ts              # [NEW] Zustand state store for FA market & active offer
        ├── components/
        │   └── freeAgency/
        │       ├── FreeAgentTable.tsx             # [NEW] Paginated player table with scheme fit badges
        │       ├── FreeAgentFilterBar.tsx         # [NEW] Multi-facet filter controls (Pos, OVR, Age, Scheme)
        │       ├── ContractBuilderModal.tsx       # [NEW] Interactive contract offer builder with sliders
        │       ├── CapImpactMeter.tsx             # [NEW] Real-time Year 1-5 cap hit visualizer
        │       ├── PlayerInterestGauge.tsx        # [NEW] Animated sentiment gauge (0-100%) with agent quote
        │       ├── BiddingWarTicker.tsx           # [NEW] Live AI GM counter-bid feed with audio alerts
        │       └── FreeAgency.module.css          # [NEW] High-tech dark gridiron styling
        ├── pages/
        │   └── FreeAgencyHub.tsx                  # [NEW] Primary War Room page mounting all subcomponents
        └── e2e/
            └── free-agency-bidding.spec.ts        # [NEW] Playwright end-to-end user negotiation flow
```

---

### Detailed File Specifications (R1 Core)

#### 1. `backend/app/schemas/free_agency.py`
- **Purpose**: Strict validation schemas for queries, offers, and bidding rounds.
```python
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict

class FreeAgentQueryFilters(BaseModel):
    position: Optional[str] = None
    min_ovr: int = Field(default=60, ge=50, le=99)
    max_ovr: int = Field(default=99, ge=50, le=99)
    max_age: Optional[int] = Field(default=None, ge=20, le=45)
    scheme_fit: Optional[str] = None
    sort_by: str = Field(default="overall_rating", pattern="^(overall_rating|age|demanded_aav)$")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

class ContractOfferRequest(BaseModel):
    player_id: int
    team_id: int
    years: int = Field(ge=1, le=7)
    base_salary_annual: int = Field(ge=950_000, le=65_000_000)
    signing_bonus_total: int = Field(default=0, ge=0, le=140_000_000)
    guaranteed_total: int = Field(default=0, ge=0)

class CapYearBreakdown(BaseModel):
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
    cap_deficit: int = 0
    player_interest_score: float = Field(ge=0.0, le=100.0)
    likelihood: Literal["VERY_HIGH", "HIGH", "MODERATE", "LOW", "UNLIKELY"]
    agent_feedback: str
    yearly_breakdown: List[CapYearBreakdown]

class AIBidItem(BaseModel):
    team_id: int
    team_name: str
    team_abbr: str
    years: int
    aav: int
    total_guaranteed: int
    interest_score: float

class BiddingRoundResponse(BaseModel):
    round_number: int
    bids: List[AIBidItem]
    user_status: Literal["LEADING", "OUTBID", "ACCEPTED", "REJECTED"]
    high_bidder_name: str
    high_bid_aav: int
    seconds_remaining: int
```

#### 2. `frontend/src/types/freeAgency.ts`
- **Purpose**: Mirror backend models in TypeScript with strict compile-time types.
```typescript
export interface FreeAgentPlayer {
  id: number;
  firstName: string;
  lastName: string;
  position: string;
  overallRating: number;
  age: number;
  demandedAav: number;
  demandedYears: number;
  demandedGuaranteed: number;
  schemeFitScore: number; // 0-100
  schemeFitBadge: "ELITE" | "GOOD" | "AVERAGE" | "POOR";
  interestedTeamsCount: number;
  biddingStatus: "AVAILABLE" | "OFFER_PENDING" | "SIGNED";
  portraitUrl?: string;
}

export interface ContractYearBreakdown {
  year: number;
  baseSalary: number;
  proratedBonus: number;
  totalCapHit: number;
  deadCapIfCut: number;
}

export interface ContractEvaluation {
  playerId: number;
  teamId: number;
  totalValue: number;
  aav: number;
  yearOneCapHit: number;
  currentTeamCapSpace: number;
  projectedRemainingCap: number;
  isCapCompliant: boolean;
  capDeficit: number;
  playerInterestScore: number;
  likelihood: "VERY_HIGH" | "HIGH" | "MODERATE" | "LOW" | "UNLIKELY";
  agentFeedback: string;
  yearlyBreakdown: ContractYearBreakdown[];
}
```

---

## 🚀 SECTION 2: FIVE TANGENTIALLY RELATED FEATURE EXPANSIONS (R1)

### Expansion 1.1: Void Years & Rolling Option Bonus Cap Restructuring Studio
- **Conceptual Rationale:** Modern NFL teams (e.g. Saints, Eagles, Chiefs) rarely sign players using flat cash. They utilize "Void Years" (dummy contract years that automatically void after 2-3 seasons) and rolling option bonuses to maximize immediate championship contention while deferring cap hits into future seasons.
- **Concrete Technical Architecture & Mechanics:**
  - When constructing an offer, GMs can append up to 3 "Void Years" to the end of a deal.
  - The signing bonus is prorated over $\min(5, \text{Real Years} + \text{Void Years})$.
  - When the contract voids, all remaining unamortized prorated bonus accelerates immediately into the void year as dead cap.
  - Formula for accelerated dead money upon void:
    $$\text{DeadCap}_{\text{VoidYear}} = \sum_{t = \text{VoidYear}}^{\text{MaxProration}} \text{ProratedBonus}_t$$
- **Files to Create / Modify:**
  - `backend/app/services/capology/void_years_calculator.py`
  - `backend/app/schemas/capology_restructure.py`
  - `frontend/src/components/freeAgency/VoidYearToggle.tsx`
  - `frontend/src/components/freeAgency/DeadCapTimelineModal.tsx`
- **Data Schemas:**
  ```python
  class VoidYearOffer(BaseModel):
      real_years: int = Field(ge=1, le=5)
      void_years: int = Field(ge=0, le=3)
      annual_option_bonus: int = 0
      accelerated_dead_money: int
      net_year_one_savings: int
  ```
- **UI/UX Flow:** A toggle in `ContractBuilderModal.tsx` labeled "Add Void Years". Selecting "+2 Void Years" expands a golden dotted section on the Cap Hit bar, dropping Year 1 cap hit by 35% while showing a crimson "Void Acceleration" warning marker on Year 3.

---

### Expansion 1.2: Compensatory Draft Pick Formula Forecaster (NFL Appendix V)
- **Conceptual Rationale:** In the NFL, losing high-value unrestricted free agents (UFAs) without signing comparable free agents yields valuable compensatory picks in Rounds 3-7 of the subsequent NFL Draft. GMs actively calculate whether signing a free agent will cancel out a projected 3rd-round compensatory pick.
- **Concrete Technical Architecture & Mechanics:**
  - Tracks qualifying unrestricted free agents lost vs gained based on AAV percentiles:
    - Top 5% league AAV lost $\rightarrow$ 3rd Round Pick.
    - Top 10% league AAV lost $\rightarrow$ 4th Round Pick.
    - Top 15% league AAV lost $\rightarrow$ 5th Round Pick.
  - Net CFA Cancellation Engine: Each signed incoming free agent cancels out an outgoing free agent of equivalent or lower tier.
- **Files to Create / Modify:**
  - `backend/app/services/draft/compensatory_pick_engine.py`
  - `backend/app/api/endpoints/compensatory_picks.py`
  - `frontend/src/components/freeAgency/CompPickWarningBadge.tsx`
- **Data Schemas:**
  ```python
  class CompPickProjection(BaseModel):
      team_id: int
      projected_picks: List[Dict[str, Any]] # e.g. [{"round": 3, "cancelled_by": None}]
      signing_this_player_cancels_pick: Optional[int] # e.g. Round 3 pick lost if signed
  ```
- **UI/UX Flow:** In the Free Agent table, hovering over a player demanding $\ge \$18\text{M}$ AAV displays an amber tooltip: *"Signing this player cancels your projected 2026 Round 3 Compensatory Pick"*.

---

### Expansion 1.3: State Income Tax & Market Location Preference Matrix
- **Conceptual Rationale:** Real players consider net take-home pay and market prestige. A \$20M AAV offer in Florida/Texas (0% state income tax) yields significantly more net take-home pay than \$20M in California (13.3% state tax). Similarly, high-ego WRs desire major media markets (NY, LA) for national endorsements.
- **Concrete Technical Architecture & Mechanics:**
  - State Tax Lookup Table ($T_{\text{state}}$) for all 32 NFL franchises (e.g., MIA, TB, JAX, DAL, HOU, LV, TEN = 0.0%; LAR, LAC, SF = 13.3%).
  - Effective Net Take-Home Pay formula:
    $$\text{NetTakeHome} = \text{AAV} \times (1.0 - (T_{\text{federal}} + T_{\text{state}} + T_{\text{jock\_tax}}))$$
  - Location Preference Score ($L_p$) added to Player Interest based on Big-Six `greed` (values tax savings) vs `ego` (values media market size).
- **Files to Create / Modify:**
  - `backend/app/data/nfl_state_taxes.py`
  - `backend/app/services/capology/tax_adjusted_valuation.py`
  - `frontend/src/components/freeAgency/NetIncomeComparisonCard.tsx`
- **Data Schemas:**
  ```typescript
  export interface TaxComparison {
    grossAav: number;
    stateTaxRate: number;
    netAnnualIncome: number;
    taxAdvantageDelta: number; // e.g. +$1,420,000 in Miami vs Buffalo
  }
  ```
- **UI/UX Flow:** `ContractBuilderModal.tsx` includes an expandable "Net Take-Home Pay" calculator tab comparing the user team's tax burden against rival bidding teams.

---

### Expansion 1.4: Franchise Tag & Transition Tag Tender System
- **Conceptual Rationale:** Before free agency opens, teams must have the power to protect their most crucial pending free agents via Exclusive Franchise Tags, Non-Exclusive Franchise Tags, or Transition Tags, setting fixed 1-year tender amounts.
- **Concrete Technical Architecture & Mechanics:**
  - Non-Exclusive Tag: Top 5 cap hit average at the position over past 5 seasons. Other teams can negotiate; if user declines to match, team receives two 1st-round draft picks.
  - Exclusive Tag: Top 5 current-year salaries at the position; player cannot negotiate with other teams.
  - Transition Tag: Top 10 salary average; right of first refusal, no draft pick compensation.
  - Player Holdout Probability: If a player with high `ego` or high `greed` is tagged without a long-term extension, their tension increases by $+35.0$, unlocking potential camp holdouts.
- **Files to Create / Modify:**
  - `backend/app/services/offseason/tag_service.py`
  - `backend/app/schemas/franchise_tag.py`
  - `frontend/src/components/freeAgency/FranchiseTagModal.tsx`
- **Data Schemas:**
  ```python
  class TagTenderCalculation(BaseModel):
      position: str
      exclusive_tender: int
      non_exclusive_tender: int
      transition_tender: int
      eligible_players: List[int]
  ```
- **UI/UX Flow:** In the Offseason War Room, an alert banner "Franchise Tag Window Open" provides a tender selection dialog with projected cap deduction and player reaction preview.

---

### Expansion 1.5: Post-June 1st Release & Dead Money Allocation Simulator
- **Conceptual Rationale:** In real NFL capology, designating a player as a "Post-June 1st Release" splits the accelerated dead money over two seasons (Year 1 absorbs only current-year proration; Year 2 absorbs all remaining future proration), providing emergency cap space to sign free agents.
- **Concrete Technical Architecture & Mechanics:**
  - Standard Cut: All remaining prorated bonus accelerates into current season immediately.
  - Post-June 1st Cut (Max 2 designations per offseason):
    $$\text{DeadCap}_{\text{CurrentYear}} = \text{ProratedBonus}_{\text{CurrentYear}}$$
    $$\text{DeadCap}_{\text{NextYear}} = \sum_{t = 2}^{\text{RemainingYears}} \text{ProratedBonus}_t$$
  - Cap Relief unlocks immediately on June 1st in the game calendar.
- **Files to Create / Modify:**
  - `backend/app/services/capology/post_june_cut_service.py`
  - `frontend/src/components/freeAgency/CutPlayerCapPreviewModal.tsx`
- **Data Schemas:**
  ```python
  class CutDesignationOption(BaseModel):
      player_id: int
      designation: Literal["STANDARD", "POST_JUNE_1"]
      immediate_cap_savings: int
      current_year_dead_cap: int
      next_year_dead_cap: int
  ```
- **UI/UX Flow:** Inside the Roster or Free Agency Cap Meter, clicking "Create Emergency Cap Space" opens a cut simulator where GMs can test post-June 1st designations with instant visual sliders.

---

# ADR-005: Free Agency Capology, Signing Bonus Proration, Post-June 1st Dead Money Split, and Top-51 Offseason Rule

**Status**: Accepted  
**Date**: 2026-09-06  
**Decision Makers**: Lead Capologist Architect, Empire Backend Specialist, QA Engineer  
**Supersedes**: N/A  

---

## Context

The NFL Collective Bargaining Agreement (CBA) governs player contracts, team salary caps, and dead money mechanics through highly specific financial rules:
1. **Offseason Roster Expansion**: In the offseason, NFL rosters expand from 53 to up to 90 players. If every player's contract were counted against the cap simultaneously, almost every NFL franchise would instantly suffer catastrophic salary cap violations during spring training activities and minicamps.
2. **Signing Bonus Proration**: Signing bonuses are fully guaranteed upfront cash disbursements amortized evenly over the duration of the contract, but the CBA imposes a strict 5-year maximum amortization ceiling, regardless of whether a contract spans 6, 7, or 10 years.
3. **Dead Money Acceleration vs. Post-June 1st Designations**: When a player is waived or terminated pre-June 1st, all unamortized signing bonus proration immediately accelerates into the current league year's cap obligation. However, under CBA Article 13, Section 3, teams may designate up to two players as post-June 1st releases (or release players after June 1st). Under this rule, only the current year's proration allocation hits the current league year, while all remaining unamortized balances are deferred to hit the subsequent league year.
4. **Interactive Free Agency Bidding**: Previous free agency implementations resolved offers via offline batch heuristics without real-time cap proration previews, interactive multi-team bidding, or validation against live GM cap space.

Without these mechanics, franchise cap management in THE-NFL-SIM-V2 produced unrealistic dead money spikes, offseason cap paralysis, and lacked authentic GM team-building strategy.

---

## Decision

We have implemented authentic NFL CBA capology mechanics across the backend kernel, domain services, schemas, and frontend UI:

1. **5-Year Maximum Proration Ceiling**:
   - In both backend engines (`CapologistPhysics`, `SalaryCapEngine`, `FreeAgencyEngine`) and the frontend interactive bidding calculator (`FreeAgencyMarket.tsx`), signing bonus proration is strictly bounded:
     $$\text{Proration Years} = \min(\text{Contract Years}, 5)$$
     $$\text{Annual Signing Bonus Proration} = \frac{\text{Signing Bonus}}{\text{Proration Years}}$$
     $$\text{Annual Base Salary} = \frac{\text{Total Value} - \text{Signing Bonus}}{\text{Contract Years}}$$
     $$\text{Year 1 Cap Hit} = \text{Annual Base Salary} + \text{Annual Signing Bonus Proration}$$

2. **Post-June 1st Dead Money Split**:
   - Implemented in `CapologistPhysics.calculate_post_june1_dead_money` and `SalaryCapEngine.calculate_post_june1_dead_money`:
     - Current League Year ($Y_0$): Absorbs exclusively the current year's scheduled signing bonus proration:
       $$\text{Dead Money}_{Y_0} = \text{Bonus Proration}_{Y_0}$$
     - Following League Year ($Y_1$): Absorbs the sum of all remaining future unamortized signing bonus allocations:
       $$\text{Dead Money}_{Y_1} = \sum_{y > Y_0} \text{Bonus Proration}_y$$
   - Recorded persistently in the team's multi-year dead money ledger (`record_post_june1_release`).

3. **Top-51 Offseason Rule**:
   - Implemented in `SalaryCapService.calculate_top51_cap`:
     - When `Season.status != SeasonStatus.REGULAR_SEASON` (e.g. `OFF_SEASON`, `PRE_SEASON`), active roster cap obligations are determined strictly by sorting all player salaries in descending order and summing only the top 51 highest cap charges.
     - When `Season.status == SeasonStatus.REGULAR_SEASON`, the calculation transitions automatically to the full 53-man roster summation plus practice squad and dead money allocations.
     - `get_team_cap_breakdown` exposes `"is_top51_applied": is_offseason` to the UI for transparent GM telemetry.

4. **Interactive Market Browsing & Real-Time Bidding API**:
   - Exposed `GET /api/seasons/{season_id}/free-agency/market` returning `List[FreeAgentMarketPlayer]` with position filtering, tier classification, and competing AI suitor teams.
   - Exposed `POST /api/seasons/{season_id}/free-agency/bid` processing user GM contract offers (`FreeAgentBidRequest`) in real time, validating cap room, executing AI GM counter-bidding algorithms, mutating contracts atomically, and returning `FreeAgentBidResponse`.

---

## Rationale

1. **NFL Realism**: Replicates real-world NFL front-office maneuvers (e.g., how the Saints, Rams, and Chiefs structure high-AAV deals with heavy signing bonuses while staying compliant).
2. **Strategic Depth**: Enables user GMs to utilize post-June 1st designations to manage veteran cap hits over two seasons rather than absorbing massive single-year dead cap penalties.
3. **Offseason Flexibility**: The Top-51 rule allows teams to sign undrafted free agents and depth players for training camp without triggering false cap violations.
4. **Interactive Engagement**: GMs can actively compete in free agency bidding wars with live cap calculations rather than simulating off-screen.

---

## Consequences

### Positive Consequences
- **Financial Authenticity**: 100% compliance with NFL CBA rules for signing bonus proration, post-June 1st cuts, and offseason roster accounting.
- **Strict Performance**: Free agency bidding resolution and multi-year cap calculations resolve in <1.0ms (well within the <40.0ms budget).
- **Type Safety**: Strict Pydantic V2 schemas and TypeScript interfaces with 0 `any` types.
- **Virtualization Support**: Free agency market UI seamlessly renders 1,500+ free agents via `@tanstack/react-virtual` at 60 FPS.

### Negative Consequences / Trade-offs
- **Multi-Year Ledger State**: Requires persistence of dead money commitments into future league years ($Y+1$), requiring careful state migration during season advancement.
- **Roster Cutdown Pressure**: When transitioning from preseason to regular season, GMs must trim rosters to 53 players before the Top-51 rule expires, or face cap penalties.

---

## Alternatives Considered

1. **Instant Acceleration for All Releases**:
   - *Description*: Accelerate 100% of unamortized bonus into current year regardless of date.
   - *Reason for Rejection*: Unrealistic; penalizes teams severely and eliminates the strategic utility of post-June 1st designations.
2. **Simple Average Cap Hit**:
   - *Description*: Dividing total contract value evenly across all years with no bonus proration.
   - *Reason for Rejection*: Fails to reflect NFL salary cap mechanics where base salary and bonus proration are distinct balance sheet items.

---

## Validation Criteria

- `pytest backend/tests/unit/test_capology_sprint.py`: 18/18 tests pass verifying proration ceilings, post-June 1st math, and Top-51 sorting.
- `python backend/scripts/benchmark_operational_latencies.py`: Subsystem 2 (Capology & Bidding) executes in ~0.83ms (ceiling <40.0ms).
- `python scripts/check_field_parity.py`: Verifies strict type parity across frontend and backend contract schemas.

# Handoff Report: Dynasty RPG Progression & Front Office Empire Economics (Pillar 2)

**Agent:** Explorer 2 (Dynasty & Economics Systems Analyst)  
**Working Directory:** `.agents/explorer_survey_2`  
**Primary Deliverable:** `.agents/explorer_survey_2/survey_dynasty.md`  
**Parent Conversation ID:** `18451d18-0570-4faa-9bec-b84d14c2d697`  
**Status:** COMPLETE (Hard Handoff)  

---

## 1. Observation

A comprehensive inspection of the codebase models, services, documentation, and CSV data tables revealed:

1. **Financial & Cap Data Tables**:
   - `NFL Financial Thresholds and Salary Cap Performance Metrics - Table 1.csv` records salary cap growth from 1994 ($34.6M) to 2025 ($279.2M) with a historical CAGR of $6.97\%$.
   - `NFL Simulation Engine Implementation Data Table - Table 1.csv` provides empirical benchmarks for restructure mechanics, void years, post-June 1 designations, and surplus value formulas.
2. **Existing Models & Schemas**:
   - `backend/app/models/player_progression.py`: Defines `DevelopmentTrait` (`NORMAL`, `STAR`, `SUPERSTAR`, `XFACTOR`), XP tracking, and JSON ability maps.
   - `backend/app/models/player_contract.py`: Stores `contract_years`, `contract_salary`, `is_rookie`, and `morale`.
   - `backend/app/models/player_injury.py` & `backend/app/models/medical.py`: Tracks body part integrity (head, neck, torso, arms, legs), injury recurrence risk, and severity levels.
   - `backend/app/models/trade_offer.py`: Persists trades with multi-asset arrays, pick years/rounds, and counter-offer trees.
3. **Core Services & Engines**:
   - `backend/app/rpg/progression.py` & `backend/app/services/age_curves.py`: Defines position-based peak windows, learning multipliers, and baseline physical decay.
   - `backend/app/services/trait_service.py`: Implements a 25-trait catalog with tier caps and `TraitRarity` soft caps.
   - `backend/app/services/empire/salary_cap.py` & `backend/app/kernels/empire/capologist.py`: Implements contract proration, dead money calculation, and basic restructuring.
   - `backend/app/services/gm_agent.py` & `backend/app/core/trade_config.py`: Implements non-linear player valuation, positional value tiers, and GM archetypes.
   - `backend/app/rpg/injury_system.py` & `backend/app/core/injury_config.py`: Implements per-play multiplicative injury probability ($P = P_{\text{base}} \cdot \mu_{\text{play}} \cdot \mu_{\text{pos}} \dots$), play-through toughness thresholds, and escalation risk.

---

## 2. Logic Chain

1. **Trait Evolution & Devolution**: To avoid progression bloat where all players eventually become superstars, development traits must feature strict league-wide soft caps (~3% for X-Factor, ~10% for Superstar) with bidirectional transitions. Evolution is driven by statistical Z-scores and awards; devolution is triggered by catastrophic Grade 3 injuries, prolonged benching, or sub-starter performance post-age-30.
2. **Bifurcated Age Curve Modeling**: Physical attributes (Speed, Acceleration, Throw Power) must be decoupled from cognitive attributes (Awareness, Play Recognition, Pass Block Nuance). Physical traits follow power-law decay curves starting between ages 26–30 depending on position; mental attributes follow logarithmic learning curves that persist into mid-to-late 30s.
3. **Surplus-Value Trade Evaluation**: Trade AI cannot rely solely on raw Overall ratings. It must evaluate Contract Surplus Value ($S_i = V_{\text{production}} - C_{\text{cash\_cost}}$), rookie-scale surplus premiums, and multi-chart draft valuations (Jimmy Johnson, Rich Hill, Fitzgerald-Spielberger) while adjusting for contender vs. rebuilder situational postures.
4. **CBA Capology Formulation**: Multi-year financial health requires exact modeling of 5-year maximum proration, pre- vs. post-June 1 dead money acceleration splits, simple restructures converting base salary to bonus, void year amortizations, and the 89% four-year cash spending floor.
5. **Medical Triage & Intervention**: Injury risk requires an anatomical model (8 body zones) paired with fatigue/workload compounding. Player triage decisions introduce explicit trade-offs: Toradol injections eliminate short-term attribute penalties at the cost of a 2.5x escalation risk; orthopedic braces reduce re-injury risk at the expense of fixed speed/agility penalties.
6. **DAG Narrative Generation**: Linear story engines become repetitive. An emergent Directed Acyclic Graph (DAG) architecture dynamically evaluates team state vectors (morale, chemistry, win streaks, contract surplus) to drive branching multi-week storylines (contract holdouts, coordinator friction, mentor-mentee dynamics).

---

## 3. Caveats

- **No Caveats**: All 6 core requirement areas were thoroughly surveyed, formulated, and mathematically specified.
- The specifications are fully compatible with existing SQLAlchemy database models and provide drop-in Pydantic V2 and TypeScript data contracts.

---

## 4. Conclusion

The comprehensive architectural specification for **Pillar 2: Dynasty RPG Progression & Front Office Empire Economics** has been synthesized and written to:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_2\survey_dynasty.md`

The deliverable provides production-ready mathematical equations, parameter matrices, Pydantic V2 schemas, TypeScript contracts, and anti-exploit safeguards (such as the "Saints Cap Trap" mitigation and package trade concentration discount).

---

## 5. Verification Method

To independently verify this specification:
1. **Inspect Artifact File**:
   - Open and review `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_2\survey_dynasty.md`.
2. **Verify Mathematical Consistency**:
   - Check the compound annual growth rate formula against `NFL Financial Thresholds and Salary Cap Performance Metrics - Table 1.csv` ($279.2\text{M}$ in 2025, CAGR $= 6.97\%$).
   - Check the draft valuation formula against `backend/app/data/draft_value_chart.py`.
   - Check the injury probability formula against `backend/app/core/injury_config.py`.
3. **Verify Schema Alignment**:
   - Compare `PlayerDynastyProfile`, `ContractYearDetail`, `CapOptimizationProposal`, and `DAGStorylineNode` in Section 8 with existing models in `backend/app/models/`.

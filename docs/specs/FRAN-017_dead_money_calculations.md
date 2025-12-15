# FRAN-017: Dead Money Calculations

**Feature ID:** FRAN-017
**Status:** SPEC_COMPLETE
**Implementation Status:** PARTIAL / PLANNED

## 1. Overview

Dead Money represents the salary cap charge for a player who is no longer on the roster. It typically comes from unamortized signing bonuses that accelerate onto the current year's cap when a player is cut or traded.

## 2. Current Implementation

### 2.1 SalaryCapService (`services/salary_cap_service.py`)

Currently, `SalaryCapService` calculates **Used Cap** by summing the `contract_salary` of _active_ players.

```python
used_cap = sum(p.contract_salary for p in players)
```

**Gap:** It currently does not query a `DeadMoneyAdjustment` table or similar, meaning the cap hit of a cut player usually disappears instantly (incorrect behavior) or isn't tracked.

### 2.2 Capologist Kernel (`kernels/empire/capologist.py`)

Experimental code exists for risk assessment:

```python
def check_financial_risk(self, dead_cap_hit: float) -> float:
    risk_ratio = dead_cap_hit / self.salary_cap
```

This implies the concept exists in the design but isn't fully wired into the main `SalaryCapService`.

## 3. Specification

To fully implement Dead Money:

### 3.1 Data Model

A new entity `DeadCapCharge` is required:

- `team_id` (FK)
- `player_id` (FK, nullable if player deleted)
- `amount` (Integer)
- `year` (Integer)
- `reason` (Enum: CUT, TRADE)

### 3.2 Calculation Logic

When a player is released:

1. **Remaining Guarantee:** Calculate unpaid guaranteed money.
2. **Acceleration:** If cut pre-June 1st, all remaining guarantees hit current year.
3. **Persist:** Create `DeadCapCharge` record.

### 3.3 Dashboard Integration

The `SalaryCapService.get_team_cap_breakdown` response must include:

```json
{
  "used_cap": <ActiveContracts + DeadMoney>,
  "dead_money": <Sum of DeadCapCharges>,
  "active_cap": <Sum of ActiveContracts>
}
```

## 4. Workaround

Until the full `DeadCapCharge` table is migrated, Dead Money is currently **abstracted** or treated as 0 in the main UI, meaning teams have slightly more flexibility than in real life.

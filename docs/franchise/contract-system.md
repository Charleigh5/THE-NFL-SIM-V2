# Contract System Specification

**Source:** `backend/app/models/player.py`, `backend/app/services/offseason_service.py`
**Status:** Reverse-Engineered / Current Implementation

## 1. Overview

The contract system tracks player contract status and manages the offseason transition between seasons. It is a simplified model focused on years remaining rather than complex salary structures.

## 2. Data Model

### Player Contract Fields

Located in `models/player.py`:

| Field             | Type    | Default   | Description                 |
| ----------------- | ------- | --------- | --------------------------- |
| `contract_years`  | Integer | 1         | Years remaining on contract |
| `contract_salary` | Integer | 1,000,000 | Annual salary in dollars    |
| `is_rookie`       | Boolean | False     | First year player flag      |

## 3. Contract Lifecycle

### 3.1 Contract Expiration

Triggered annually during offseason via `process_contract_expirations()`:

```python
for player in active_players:
    player.contract_years -= 1
    if player.contract_years <= 0:
        player.team_id = None  # Released to Free Agency
        player.contract_years = 0
```

### 3.2 Rookie Contracts

When a player is drafted:

- `contract_years = 4` (4-year rookie deal)
- `is_rookie = False` (flag cleared after draft)

### 3.3 Free Agency Contracts

When a free agent is signed:

- `contract_years = 1` (1-year deal)
- `team_id` set to signing team

## 4. Free Agency Simulation

Located in `offseason_service.py`:

1. Query all teams
2. For each team, calculate roster size (target: 53)
3. Sign top available free agents until roster is full
4. All free agent signings are 1-year contracts

## 5. Future Enhancements (Proposed)

- Salary cap enforcement
- Multi-year contract negotiations
- Franchise tag system
- Contract restructuring
- Signing bonus proration

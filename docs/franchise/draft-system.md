# Draft System Specification

**Source:** `backend/app/models/draft.py`, `backend/app/services/offseason_service.py`, `backend/app/services/rookie_generator.py`
**Status:** Reverse-Engineered / Current Implementation

## 1. Overview

The draft system manages the annual NFL Draft, including draft order generation, pick trading, and AI-driven player selection.

## 2. Data Model

### DraftPick Model

Located in `models/draft.py`:

| Field              | Type    | Description                         |
| ------------------ | ------- | ----------------------------------- |
| `id`               | Integer | Primary key                         |
| `season_id`        | Integer | FK to Season                        |
| `team_id`          | Integer | Current owner of pick               |
| `original_team_id` | Integer | Original owner (for trades)         |
| `round`            | Integer | Draft round (1-7)                   |
| `pick_number`      | Integer | Overall pick number                 |
| `player_id`        | Integer | Selected player (null until picked) |

### Indexes

- Composite index on `(season_id, round)` for efficient round queries
- Individual indexes on `season_id`, `team_id`, `round`, `pick_number`

## 3. Draft Order Generation

Located in `generate_draft_order()`:

### Process

1. Calculate standings from completed season
2. Sort teams by record (worst to best)
3. Adjust for playoff results:
   - Super Bowl winner picks last
   - Super Bowl loser picks second-to-last
4. Generate 7 rounds × 32 picks = 224 total picks

### Pick Numbering

```python
pick_number = (round_num - 1) * 32 + (position + 1)
```

## 4. Draft Pick Trading

Via `trade_current_pick()`:

- Changes `team_id` while preserving `original_team_id`
- Allows tracking of pick provenance

## 5. Draft Simulation

### AI Pick Logic (`simulate_next_pick`)

1. Get top 20 available prospects by overall rating
2. Analyze team needs against target roster composition
3. Selection priority:
   - **Need-Based**: If top prospect fills a team need, select them
   - **Best Player Available (BPA)**: Otherwise, take highest-rated player

### Target Roster Composition

```python
TARGET_COUNTS = {
    "QB": 3, "RB": 4, "WR": 6, "TE": 3,
    "OT": 4, "OG": 4, "C": 2,
    "DE": 4, "DT": 4, "LB": 6,
    "CB": 6, "S": 4, "K": 1, "P": 1
}
```

## 6. Post-Draft Processing

When a player is selected:

- `player.team_id = pick.team_id`
- `player.contract_years = 4` (rookie contract)
- `player.is_rookie = False`
- `pick.player_id = player.id`

## 7. Rookie Class Generation

Handled by `RookieGenerator` service:

- Generates 224 prospects per draft class
- Distribution across all positions
- Overall ratings typically range 50-85
- Includes combine metrics and Genesis data

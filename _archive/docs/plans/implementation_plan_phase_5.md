# Implementation Plan - Phase 5: Season & Franchise Mode

## Goal Description

Implement the core infrastructure for running a full NFL season, including schedule generation, standings calculation, and franchise management features. This builds upon the simulation engine to allow for long-term gameplay loops.

## User Review Required

> [!IMPORTANT]
> This phase introduces significant new database models and API endpoints. Ensure that the `Season` and `Schedule` models are reviewed for completeness before running migrations.

## Proposed Changes

### Backend

#### [NEW] `backend/app/models/season.py`

- Define `Season` model:

  - `id`: Integer, Primary Key
  - `year`: Integer
  - `current_week`: Integer
  - `is_active`: Boolean
  - `status`: Enum (PRE_SEASON, REGULAR_SEASON, POST_SEASON, OFF_SEASON)

- Define `Schedule` model (or `Game` updates):
  - Link `Game` to `Season` via `season_id`.
  - Add `week`: Integer to `Game` model.

#### [NEW] `backend/app/services/schedule_generator.py`

- Implement `generate_schedule(teams: List[Team]) -> List[Game]`:
  - Use a round-robin or similar algorithm to generate matchups for a 17-week season (or configurable length).
  - Ensure balanced home/away games.

#### [NEW] `backend/app/services/standings_calculator.py`

- Implement `calculate_standings(season_id: int) -> List[TeamStandings]`:
  - Aggregate `Game` results for the given season.
  - Calculate Wins, Losses, Ties, Points For, Points Against, Point Differential.
  - Sort by Win Percentage, then tie-breakers.

#### [NEW] `backend/app/api/endpoints/season.py`

- `POST /init`:
  - Accepts `year` and `team_ids`.
  - Calls `schedule_generator`.
  - Creates `Season` and `Game` records.
- `GET /schedule`:
  - Returns games filtered by `season_id` and optional `week`.
- `GET /standings`:
  - Returns calculated standings for the active season.

### Frontend

#### [NEW] `frontend/src/pages/SeasonDashboard.tsx`

- Main hub for Franchise mode.
- Displays:
  - Current Week info.
  - "Simulate Week" button.
  - Top headlines (optional).

#### [NEW] `frontend/src/components/season/StandingsTable.tsx`

- Table displaying team records.
- Columns: Rank, Team, W, L, T, PCT, PF, PA, DIFF.

#### [NEW] `frontend/src/components/season/ScheduleView.tsx`

- List of games for the selected week.
- Shows status (Scheduled, In Progress, Final) and scores.
- Allows clicking a game to view details or "Watch" (Live Sim).

## Verification Plan

### Automated Tests

- **Schedule Generation**:
  - Verify correct number of games per team.
  - Verify no duplicate matchups in the same week.
- **Standings**:
  - Create mock game results.
  - Verify standings calculation matches expected W-L records.

### Manual Verification

1. **Initialize Season**:
   - Use the API or UI to start a new season.
   - Verify `Season` and `Game` records in DB.
2. **Check Schedule**:
   - Navigate to Schedule View.
   - Verify all weeks are populated.
3. **Simulate Games**:
   - Run a few games (using existing simulation logic).
   - Check Standings update correctly.

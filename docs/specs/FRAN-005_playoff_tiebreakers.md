# FRAN-005: Playoff Tiebreakers

**Feature ID:** FRAN-005
**Status:** SPEC_COMPLETE
**Implementation Status:** IMPLEMENTED

## 1. Overview

This specification details the logic used to seed playoff teams, particularly when multiple teams end the season with the same win-loss record. It ensures the correct teams reach the post-season according to determined rules.

## 2. Current Implementation (`backend/app/services/playoff_service.py`)

The `PlayoffService` calculates seeds dynamically at the end of the regular season (Week 18).

### 2.1 The Algorithm

The logic resides in `_calculate_conference_seeds`.

1. **Group by Division:** Identify the winner of each division first.
2. **Sort Division Winners (Seeds 1-4):**
   - Primary Sort: **Win Percentage** (which accounts for Ties).
   - Secondary Sort: **Total Wins**.
   - Tertiary Sort: **Point Differential**.
3. **Sort Wild Cards (Seeds 5-7):**
   - Pool all non-division-winners.
   - Sort using the same criteria (Win% > Wins > Point Diff).
   - Take top 3.

### 2.2 Difference from NFL Rules

The real NFL has a complex 12-step tiebreaker including Head-to-Head, Conference Record, Common Games, and Strength of Victory.
**Current Simplification:**

- **Missing:** Head-to-Head record is not currently checked.
- **Missing:** Conference Record is not specifically weighted (though `StandingsCalculator` tracks it, the sorting key uses global Win%).
- **Used:** Point Differential is the primary "strength" metric used after record.

## 3. Data Flow

1. `Season` advances to `POST_SEASON`.
2. `PlayoffService.generate_playoffs(season_id)` is called.
3. `_calculate_conference_seeds` fetches `TeamStats`.
4. Seeds are assigned.
5. Matchups created (e.g., Seed 2 vs Seed 7).

## 4. Future Enhancements

To achieve 100% simulation accuracy:

- [ ] Implement `HeadToHeadService` to check historical game results between tied teams.
- [ ] Modify sorting lambda to specific `conference_win_percentage` before Point Differential.

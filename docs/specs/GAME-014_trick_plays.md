# GAME-014: Trick Plays Specification

**Feature ID:** GAME-014
**Status:** PROPOSED
**Priority:** P2

## 1. Overview

Trick plays add an element of high-risk, high-reward strategy to the NFL Sim Engine. They allow coaches to catch the defense off-guard, potentially turning the tide of a game. This feature introduces specific logic for resolving non-standard plays like fake kicks and gadget plays.

## 2. Play Types

### 2.1 Special Teams Trick Plays

These plays replace standard special teams plays (Punt, Field Goal).

- **Fake Punt Run:** The punter or up-back takes the snap and attempts to run for a first down.
- **Fake Punt Pass:** The punter or protector attempts to throw a pass to a gunner or wing.
- **Fake Field Goal Run:** The holder receives the snap and runs, or pitches to the kicker/wing.
- **Fake Field Goal Pass:** The holder receives the snap and throws a pass.
- **Surprise Onside Kick:** An onside kick attempted when not expected (e.g., typically before the 4th quarter).

### 2.2 Offensive Trick Plays

These plays are run from standard offensive formations but involve deceptive mechanics.

- **Flea Flicker:** RB takes a handoff, turns, and pitches back to the QB, who throws deep. High boom/bust potential.
- **Philly Special:** QB initiates a fake audible/protection call, ball is snapped to RB/TE who pitches to WR, who throws to QB.

## 3. Resolution Logic mechanics

### 3.1 Surprise Factor

- **Base Chance:** Every trick play has a base success probability derived from NFL analytics.
- **Defensive Awareness:** The defending team's "Awareness" or specific "Special Teams Recognition" attribute lowers the success rate.
- **Frequency Penalty:** Calling trick plays too often drastically reduces their success rate (diminishing returns).

### 3.2 Attribute Dependencies

- **Fake Punt Pass:** Uses Punter's `ThrowingAccuracy` (if available) or raw attribute, vs Defense `ZoneCoverage`.
- **Fake Punt Run:** Uses Punter/Up-back `Speed`/`Agility` vs Defense `Tackling`.
- **Flea Flicker:** Success depends on Offensive Line holding up longer (block shed time interaction) and DBs biting on the run fake (Play Action effectiveness).

### 3.3 Coaching AI

- **Aggressiveness:** Coaches with high "Aggressiveness" or "Riverboat Gambler" trait are more likely to call these.
- **Desperation:** Probability increases when losing in the 4th quarter or in "do-or-die" situations.

## 4. Data Requirements

- New `PlayType` enums: `FAKE_PUNT_RUN`, `FAKE_PUNT_PASS`, `FAKE_FG_RUN`, `FAKE_FG_PASS`, `FLEA_FLICKER`, `PHILLY_SPECIAL`.
- Configuration in `nfl_reference_data.py` for success rates and penalties.

## 5. UI/Animation (Future)

- Specific logs in the play-by-play (e.g., "It's a fake! The punter takes the snap...").

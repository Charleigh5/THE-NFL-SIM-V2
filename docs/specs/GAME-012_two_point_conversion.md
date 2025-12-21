# GAME-012: 2-Point Conversion Specification

## 1. Overview

This specification details the logic for 2-Point Conversions, replacing the legacy flat-percentage RNG command. It covers the decision-making process (when to go for 2) and the execution mechanics (simulating a real play from the 2-yard line).

## 2. Decision Logic (AI)

The decision to kick an Extra Point (PAT) or go for 2 is driven by the **Coaching AI** and game situation.

### 2.1 The Chart

The engine will implement a standard "Go for 2" chart logic:

- **Down by 2**: Go for 2 (to tie).
- **Down by 5**: Go for 1 (to be down 4).
- **Down by 8**: Go for 2 (to be down 6 - generally accepted analytics play, or classic Go for 1 to be down 7). _Configurable by Coach Personality_.
- **Down by 9**: Go for 2 (to be down 7).
- **Up by 1**: Go for 2 (to be up 3).
- **Up by 4**: Go for 2 (to be up 6).
- **Up by 5**: Go for 2 (to be up 7).
- **Up by 12**: Go for 2 (to be up 14).

### 2.2 Coach Personality Modifiers

- **Reliability Preference**: `CoachingPersonality.old_school` prefers kicking PATs unless forced.
- **Analytics Preference**: `CoachingPersonality.analytics_disciple` follows the strict analytics chart (e.g., Go for 2 when down 8).
- **Aggression**: `CoachingPersonality.riverboat_gambler` may go for 2 unexpectedly to extend a lead.

## 3. Execution Mechanics

Instead of a `TwoPointConversionCommand` with a flat % chance, the 2-point attempt is resolved as a specific **Game Play**.

### 3.1 Setup

- **Field Position**: Ball placed at the **2-yard line** (defensive territory).
- **Down/Distance**: Goal line scenario (Distance = 2).
- **Timer**: Clock does NOT run during the attempt (untimed down).

### 3.2 Command Translation

The `TwoPointConversionCommand` should act as a wrapper that:

1. Selects a play (Run or Pass) via `PlayCaller`.
2. Creates a `PassPlayCommand` (depth="short") or `RunPlayCommand`.
3. Modifies the command context: `is_two_point_attempt = True`.
4. Executes via `PlayResolver`.

### 3.3 Resolution

- **Success**: If `PlayResult.is_touchdown` is True OR `PlayResult.yards_gained >= 2`.
- **Scoring**: Award **2 points** to the offense.
- **Failure**: Any other result (Turnover, Stopped short, Incomplete). Award 0 points.
- **Stats**: 2-point attempts do **not** count towards player Passing/Rushing stats (Yards/TDs) in official NFL records, but are tracked as "2Pt Conversions". (Implementation note: Ensure `_update_player_stats` filters these out or tracks them separately).

## 4. Playbook Integration

- The `PlayCaller` needs a subset of plays tagged as "Goal Line" or "Short Yardage" for these attempts.
- Using a "Goal Line" formation is typical.

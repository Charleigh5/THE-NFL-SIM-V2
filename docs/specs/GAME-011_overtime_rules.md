# GAME-011: Overtime Rules Specification

## 1. Overview

This specification defines the logic for handling Overtime (OT) in the NFL Sim Engine. It covers the transition from Regulation to OT, the Coin Toss, applicable scoring rules (Modified Sudden Death), and game termination conditions.

## 2. Ruleset (NFL Modified Sudden Death)

The engine generally follows current NFL regular season overtime rules:

1. **Period**: A timed 10-minute period (Q5).
2. **Possession**: Determined by a coin toss.
3. **Winning Conditions**:
   - **Touchdown (First Possession)**: If the receiving team scores a touchdown on the opening drive, the game ends immediately. The receiving team wins.
   - **Safety (First Possession)**: If the defensive team scores a safety on the opening drive, games ends. Defense wins.
   - **Field Goal (First Possession)**: If the receiving team scores a field goal on the opening drive, the game continues. The kicking team gets one possession to score.
     - If they score a **Touchdown**, they win.
     - If they score a **Field Goal**, the game continues in Sudden Death (next score wins).
     - If they fail to score (Punt, Turnover, Missed FG), the first team wins.
   - **Sudden Death**: If, after the initial possessions (or if the first team punts/turnover), the score is tied, the next score of any kind wins the game.
4. **Ties**: If the 10-minute clock expires and the score is tied, the game ends in a Tie (Regular Season).

_Note: Playoff rules (both teams guaranteed possession unless first score is defensive TD/Safety) can be a future extension._

## 3. Implementation Requirements

### 3.1 Game State Manager

- **Quarter**: Add support for `quarter = 5` (OT).
- **Time**: Reset to "10:00" for OT.
- **Possession Tracking**:
  - Track `ot_possessions` (int).
  - Track `first_possession_score_type` (None, "FG", "TD").

### 3.2 Coin Toss

- Logic to execute `start_overtime()` which performs a random coin toss.
- Winner chooses to Receive/Kick (AI usually receives).
- Loser chooses definitive goal (handled by field position setup).

### 3.3 Scoring Logic Updates

- **Touchdown**: Check `is_overtime`.
  - If `ot_possessions == 0`: Game Over (Win).
  - If `ot_possessions == 1` and `first_possession_score_type == "FG"`: Game Over (Win).
  - If `ot_possessions >= 1` (Sudden Death): Game Over (Win).
- **Field Goal**: Check `is_overtime`.
  - If `ot_possessions == 0`: Set `first_possession_score_type = "FG"`. Kickoff.
  - If `ot_possessions == 1` and `first_possession_score_type == "FG"`: Sudden Death active. Tie Game. Next score wins.
  - If `ot_possessions >= 2`: Game Over (Win). (Assuming Sudden Death is active).

### 3.4 Game Loop Integration

- `is_game_over()` must check:
  - Standard: `quarter >= 4` AND `time_left == 0` AND `home_score != away_score`.
  - OT transition: If `quarter == 4` AND `time_left == 0` AND `home_score == away_score` -> Trigger `start_overtime()`.
  - OT End: `quarter == 5` AND (`time_left == 0` OR `win_condition_met`).

## 4. UI Implications

- Display "OT" instead of "4th".
- Explicitly notify user of "Modified Sudden Death" rules via commentary log.

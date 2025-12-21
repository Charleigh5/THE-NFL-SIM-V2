# GAME-013: Safety Scenarios Specification

## 1. Overview

This specification defines the logic for detecting and handling Safeties (scoring 2 points for the defense). A safety occurs when an offensive player is tackled with the ball in their own end zone, or commits a foul in their own end zone.

## 2. Detection Logic

A safety is detected during the **Play Resolution** phase or **Post-Play State Update**.

### 2.1 Criteria

1. **Tackle in End Zone**:

   - `possession == "home"` AND `new_yard_line <= 0` (Home defending left endzone 0).
   - `possession == "away"` AND `new_yard_line >= 100` (Away defending right endzone 100).
   - Condition: The ball carrier was tackled (not a forward progress stop outside).
   - _Implementation_: `PlayResult.yards_gained` results in field position crossing the defending goal line.

2. **Penalty in End Zone** (Phase 3/4):

   - Holding by offense in their own end zone.
   - Intentional Grounding by QB in own end zone.

3. **Fumble Out of Bounds in End Zone**:
   - Offensive player fumbles, ball goes out of bounds through their own end zone.

### 2.2 Orchestrator Logic

In `_update_game_state`:

```python
# Home has ball, driving right (0 -> 100)
# If they lose yards and cross 0
if self.possession == "home" and self.yard_line < 0:
    is_safety = True

# Away has ball, driving left (100 -> 0)
# If they lose yards and cross 100 (?) [Note: Coordinate system needs to be consistent]
# Standard Sim Convention: 0-100 absolute coordinates.
# If Home is at their own 5 (pos=5) and loses 6 yards -> pos = -1. SAFETY.
# If Away is at their own 5 (pos=95 relative to field? Or pos=95 absolute?)
# Let's assume absolute: 0 = Home Endzone, 100 = Away Endzone.
# Home offense drives 0->100. Safety at <= 0.
# Away offense drives 100->0. Safety at >= 100.
```

## 3. Resolution & Scoring

### 3.1 Scoring

- Award **2 Points** to the **Defense** (Score of the Non-Possessing team increases).
- Log Event: `EventType.SAFETY`.

### 3.2 Subsequent Action (Free Kick)

- After a safety, the team that was scored upon (original offense) must kick off.
- **Free Kick Line**: The **20-yard line** (not the 35 like normal kickoff).
- Use `PuntCommand` or `KickoffCommand` logic (players can choose, usually Punt style or Drop Kick) from the 20.

## 4. Stats Impact

- **Sack-Safety**: If caused by a sack, the QB receives a Sack stat AND the team receives a Safety stat.
- **TFL-Safety**: RB receives TFL.

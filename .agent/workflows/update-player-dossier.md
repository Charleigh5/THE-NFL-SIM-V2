---
description: Update the Player System Dossier when player mechanics change
---

# Update Player System Dossier Workflow

Use this workflow whenever you modify player-related systems to keep the `PLAYER_SYSTEM_DOSSIER.md` up to date.

## When to Run This Workflow

Execute this workflow after changes to any of these files:

- `backend/app/models/player.py` - Player attributes
- `backend/app/orchestrator/play_resolver.py` - Play triggers
- `backend/app/engine/sack_calculator.py` - Sack mechanics
- `backend/app/engine/blocking.py` - Blocking engine
- `backend/app/services/training/drills.py` - Training drills
- `backend/app/services/player_development_service.py` - Development
- `backend/app/services/offseason_service.py` - Progression
- `backend/app/services/rookie_generator.py` - Rookie generation
- `backend/app/rpg/injury_system.py` - Injury system
- `backend/app/models/trait.py` - Trait system
- `backend/app/services/salary_cap_service.py` - Contracts
- `backend/app/engine/rb_tribes.py` - RB tribes

## Steps

1. **Identify Changed Section**

   Determine which section(s) of the dossier are affected:

   - Section 1: Core Player Model → `player.py` changes
   - Section 2: Offense Positions → QB/RB/WR/TE/OL changes
   - Section 3: Defense Positions → DL/LB/DB changes
   - Section 4: Special Teams → K/P changes
   - Section 5: Play Triggers → `play_resolver.py` changes
   - Section 6: Progression → `offseason_service.py` changes
   - Section 7: Training → `drills.py` changes
   - Section 8: Traits → `trait.py` changes
   - Section 9: Contracts → `salary_cap_service.py` changes
   - Section 10: Injury → `injury_system.py` changes
   - Section 11: Rookies → `rookie_generator.py` changes

2. **Update the Dossier**

   Open `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` and:

   a. Update the "Last Updated" date at the top
   b. Modify the relevant section(s)
   c. Add a new entry to Section 13 (Changelog)

3. **Changelog Entry Format**

   ```markdown
   | YYYY-MM-DD | Brief description of change | affected_file.py |
   ```

4. **Verify Links**

   If you added new files or renamed existing ones, update the File Linkage Map in Section 12.

## Example

If you added a new attribute `pocket_awareness` to QBs:

1. Update Section 2 → Quarterback → Key Attributes table
2. Add to Section 1 if it's a global attribute
3. Update Section 13 Changelog:

   ```markdown
   | 2025-12-15 | Added pocket_awareness attribute for QBs | player.py, play_resolver.py |
   ```

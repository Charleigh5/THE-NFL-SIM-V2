# Code Review Report

**To:** cweir45@gmail.com
**Subject:** Code Review Findings and Fixes

---

### File: `backend/app/orchestrator/play_commands.py`
**Line Number(s):** 46, 68
**Error Description:** `PassPlayCommand` and `RunPlayCommand` constructors do not accept `possession`, `start_yard_line`, `down`, `distance`, `yard_line`, `is_home_team` arguments, causing the parent `PlayCommand` to use incorrect default values (e.g. `possession="home"` regardless of actual game state).
**Solution:**
Updated the `__init__` methods to accept these arguments and pass them to `super().__init__`.

```python
class RunPlayCommand(PlayCommand):
    """Command for running plays"""

    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 run_direction: str = "middle", modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, is_home_team: bool = True, possession: str = "home", start_yard_line: int = 20):
        super().__init__(offense_players, defense_players, modifiers, play_id, distance, down, yard_line, is_home_team, possession, start_yard_line)
        self.run_direction = run_direction
```

---

### File: `backend/app/orchestrator/play_caller.py`
**Line Number(s):** 216, 233
**Error Description:** `_create_pass_play` and `_create_run_play` methods instantiate commands without passing the current game context (`down`, `distance`, `possession`, etc.), resulting in the use of incorrect defaults.
**Solution:**
Updated methods to calculate absolute `yard_line` and pass all context variables to the command constructors.

```python
    def _create_run_play(self, context: PlayCallingContext) -> RunPlayCommand:
        # ... logic ...
        # Calculate absolute yard line
        yard_line = 0
        if context.possession == "home":
             yard_line = 100 - context.distance_to_goal
        else:
             yard_line = context.distance_to_goal

        return RunPlayCommand(
            # ...
            distance=context.distance,
            down=context.down,
            yard_line=yard_line,
            is_home_team=(context.possession == "home"),
            possession=context.possession,
            start_yard_line=yard_line
        )
```

---

### File: `backend/app/models/player.py`
**Line Number(s):** 19-21
**Error Description:** `NameError` for `Team`, `PlayerSeasonStats` and `BodyPart` due to missing or commented-out imports in the `TYPE_CHECKING` block.
**Solution:**
Uncommented and added the necessary imports.

```python
if TYPE_CHECKING:
    # ...
    from app.models.team import Team
    from app.models.stats import PlayerSeasonStats
    from app.models.medical import BodyPart
```

---

### File: `backend/app/orchestrator/simulation_orchestrator.py`
**Line Number(s):** 307 (approx) in `_save_player_stats`
**Error Description:** Potential `AttributeError` if `self.db_session` is `None` when `_save_player_stats` is called.
**Solution:**
Added a safety check at the beginning of the method.

```python
    async def _save_player_stats(self, game: Game = None) -> None:
        if not self.history:
            return

        if not self.db_session:
            logger.warning("No DB session available to save player stats")
            return
        # ...
```

---

### File: `frontend/src/services/api.ts`
**Line Number(s):** Entire file (all methods)
**Error Description:** Missing error handling logic. API methods would throw unhandled exceptions on failure.
**Solution:**
Added a global response interceptor for logging and `try/catch` blocks to all API methods.

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Request Failed:", { ... });
    return Promise.reject(error);
  }
);

// Example method wrapper
getTeams: async (page: number = 1, pageSize: number = 100): Promise<Team[]> => {
  try {
    const response = await apiClient.get<PaginatedResponse<Team>>(...);
    return response.data.items;
  } catch (error) {
    console.error("Failed to fetch teams", error);
    throw error;
  }
},
```

---

### File: `apts/models/base_model.py`
**Line Number(s):** 4-6
**Error Description:** Missing type hints for class attributes.
**Solution:**
Added type hints.

```python
class BaseModel:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # ...
```

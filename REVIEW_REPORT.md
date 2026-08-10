# Code Review Report

**To:** cweir45@gmail.com

This report outlines bugs, errors, TypeScript issues, missing files, and lack of documentation found across the repository based on manual inspection and static analysis.

---

## Missing Files & Directories
The following files and directories were requested or expected but are currently missing from the repository structure:
- `AGENTS.md`
- `docs/architecture/`
- `docs/data/`
- `scripts/check_docs.py`

## Bugs and Errors

### 1. `backend/app/models/player.py`
**Error:** Missing `BodyPart` import within the `TYPE_CHECKING` block. This causes static analysis tools like `mypy` to fail when evaluating `Mapped["BodyPart"]`.
**Line:** 11-21
**Proposed Solve:** Add `from app.models.medical import BodyPart` inside the `if TYPE_CHECKING:` block.

```python
<<<<<<< SEARCH
if TYPE_CHECKING:
    from app.models.trait import PlayerTrait
    from app.models.player_game_starts import PlayerGameStarts
    from app.models.player_attributes import PlayerAttributes
    from app.models.player_contract import PlayerContract
    from app.models.player_physics import PlayerPhysics
    from app.models.player_injury import PlayerInjury
    from app.models.player_progression import PlayerProgression
    # from app.models.team import Team # Circular import handling if needed, or string reference
    # from app.models.stats import PlayerSeasonStats
=======
if TYPE_CHECKING:
    from app.models.trait import PlayerTrait
    from app.models.player_game_starts import PlayerGameStarts
    from app.models.player_attributes import PlayerAttributes
    from app.models.player_contract import PlayerContract
    from app.models.player_physics import PlayerPhysics
    from app.models.player_injury import PlayerInjury
    from app.models.player_progression import PlayerProgression
    from app.models.medical import BodyPart
    # from app.models.team import Team # Circular import handling if needed, or string reference
    # from app.models.stats import PlayerSeasonStats
>>>>>>> REPLACE
```

### 2. `backend/app/api/endpoints/players.py`
**Error:** Potential `AttributeError` when accessing `stats.games_played`. The result `stats` can be `None` if the query returns nothing.
**Line:** 79-84
**Proposed Solve:** Check if `stats` is not `None` before accessing attributes.

```python
<<<<<<< SEARCH
    stats = result.first()

    return {
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
=======
    stats = result.first()

    return {
        "games_played": stats.games_played or 0 if stats else 0,
        "passing_yards": stats.passing_yards or 0 if stats else 0,
        "passing_tds": stats.passing_tds or 0 if stats else 0,
        "rushing_yards": stats.rushing_yards or 0 if stats else 0,
        "rushing_tds": stats.rushing_tds or 0 if stats else 0,
        "receiving_yards": stats.receiving_yards or 0 if stats else 0,
>>>>>>> REPLACE
```

### 3. `backend/app/services/standings_calculator.py`
**Error:** Type safety errors due to missing type annotations for dictionary variables `divisions` and `conferences`.
**Lines:** 226, 239
**Proposed Solve:** Add type hints for `divisions` and `conferences`.

```python
<<<<<<< SEARCH
        # 1. Group by Division and Rank
        divisions = {}
        for data in standings_data:
=======
        # 1. Group by Division and Rank
        divisions: dict[str, list[dict]] = {}
        for data in standings_data:
>>>>>>> REPLACE
```
```python
<<<<<<< SEARCH
        # 2. Group by Conference and Rank
        conferences = {}
        for data in standings_data:
=======
        # 2. Group by Conference and Rank
        conferences: dict[str, list[dict]] = {}
        for data in standings_data:
>>>>>>> REPLACE
```

### 4. `backend/app/services/depth_chart_service.py`
**Error:** Missing type annotations for dictionary variables like `chart` and `lineup`, causing `mypy` errors.
**Lines:** 16, 39, 115, 191
**Proposed Solve:** Add explicit type hints.

```python
<<<<<<< SEARCH
        chart = {}
        for p in players:
=======
        chart: Dict[str, List[Player]] = {}
        for p in players:
>>>>>>> REPLACE
```
```python
<<<<<<< SEARCH
        chart = DepthChartService.organize_roster(players)
        lineup = {}

        # Helper to safely get player
=======
        chart = DepthChartService.organize_roster(players)
        lineup: Dict[str, Optional[Player]] = {}

        # Helper to safely get player
>>>>>>> REPLACE
```
```python
<<<<<<< SEARCH
        chart = DepthChartService.organize_roster(players)
        lineup = {}

        def get_player(pos: str, rank: int) -> Optional[Player]:
=======
        chart = DepthChartService.organize_roster(players)
        lineup: Dict[str, Optional[Player]] = {}

        def get_player(pos: str, rank: int) -> Optional[Player]:
>>>>>>> REPLACE
```
```python
<<<<<<< SEARCH
        chart = DepthChartService.organize_roster(players)
        lineup = {}

        def get_player(pos: str, rank: int) -> Optional[Player]:
=======
        chart = DepthChartService.organize_roster(players)
        lineup: Dict[str, Optional[Player]] = {}

        def get_player(pos: str, rank: int) -> Optional[Player]:
>>>>>>> REPLACE
```

### 5. `frontend/src/services/season.ts`
**Error:** The method `simulateFreeAgency` and others return hardcoded mock data.
**Line:** 165-167
**Proposed Solve:** Acknowledge in the comments that this should be integrated with the real API, or implement the API call. Since the file notes "Will be used when real API is integrated", we will leave it as is or add a TODO.

### 6. `frontend/src/router.tsx`
**Error:** `draftRoomLoader` function uses hardcoded mock data instead of retrieving data from the API.
**Line:** 136-157
**Proposed Solve:** Use API service to fetch the draft room data instead of mocking it.

### 7. `backend/tests/verify_play_calling.py`
**Error:** `NameError` due to an undefined reference to `Player`. The script does not import `Player`.
**Line:** 39-40
**Proposed Solve:** Add `from app.models.player import Player` at the top of the file, and instantiate `Player` mock objects if needed.

```python
<<<<<<< SEARCH
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import (
=======
from app.models.player import Player
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.orchestrator.play_commands import (
>>>>>>> REPLACE
```

### 8. `backend/app/core/redis_cache.py`
**Error:** Usage of weak hashing algorithm `hashlib.md5` triggers Bandit security warning B324.
**Line:** 5, 56
**Proposed Solve:** Replace `hashlib.md5` with `hashlib.sha256`.

```python
<<<<<<< SEARCH
        return hashlib.md5(lineup_str.encode()).hexdigest()[:12]
=======
        return hashlib.sha256(lineup_str.encode()).hexdigest()[:12]
>>>>>>> REPLACE
```

### 9. `backend/app/services/enhanced_chemistry_service.py`
**Error:** Usage of weak hashing algorithm `hashlib.md5` triggers Bandit security warning B324.
**Line:** 9, 49
**Proposed Solve:** Replace `hashlib.md5` with `hashlib.sha256`.

```python
<<<<<<< SEARCH
        return hashlib.md5(lineup_string.encode()).hexdigest()[:12]
=======
        return hashlib.sha256(lineup_string.encode()).hexdigest()[:12]
>>>>>>> REPLACE
```

### 10. `frontend/src/services/api.ts`
**Error:** Missing JSDoc comments for exported methods, lacking documentation for parameters and return types.
**Proposed Solve:** Add standard JSDoc block comments to all exported API functions to ensure better documentation and IDE support.

---

**Note:** Raw static analysis output files (`ruff_output.txt`, `mypy_output.txt`, `tsc_output.txt`, `eslint_output.txt`, `bandit_output.txt`) have been generated and retained in the repository root for further review.
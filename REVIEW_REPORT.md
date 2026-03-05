To: cweir45@gmail.com
Subject: Comprehensive Code Review Report

# Comprehensive Code Review Report

The following is a list of bugs, errors, typescipt issues, and missing files/documentation found in the repository.


## File: app/api/endpoints/abilities.py
- **Line**: 41
  - **Error**: Name "AbilityStatus" already defined (possibly by an import)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "AbilityStatus" already defined (possibly by an import)
      - class AbilityStatus(BaseModel):
      ```


## File: app/api/endpoints/coaches.py
- **Line**: 58
  - **Error**: Argument "id" to "CoachResponse" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "id" to "CoachResponse" has incompatible type "Column[Any]"; expected "int"
      -         id=coach.id,
      ```

- **Line**: 59
  - **Error**: Argument "first_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "first_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
      -         first_name=coach.first_name,
      ```

- **Line**: 60
  - **Error**: Argument "last_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "last_name" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
      -         last_name=coach.last_name,
      ```

- **Line**: 61
  - **Error**: Argument "role" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "role" to "CoachResponse" has incompatible type "Column[str]"; expected "str"
      -         role=coach.role,
      ```

- **Line**: 63
  - **Error**: Argument "team_id" to "CoachResponse" has incompatible type "Column[int]"; expected "int | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "team_id" to "CoachResponse" has incompatible type "Column[int]"; expected "int | None"
      -         team_id=coach.team_id,
      ```

- **Line**: 65
  - **Error**: Argument "offense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
      -         offense_rating=coach.offense_rating,
      ```

- **Line**: 66
  - **Error**: Argument "defense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "defense_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
      -         defense_rating=coach.defense_rating,
      ```

- **Line**: 67
  - **Error**: Argument "development_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "development_rating" to "CoachResponse" has incompatible type "Column[int]"; expected "int"
      -         development_rating=coach.development_rating,
      ```

- **Line**: 68
  - **Error**: Argument "playbook_offense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "playbook_offense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"
      -         playbook_offense=coach.playbook_offense,
      ```

- **Line**: 69
  - **Error**: Argument "playbook_defense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "playbook_defense" to "CoachResponse" has incompatible type "Column[str]"; expected "str | None"
      -         playbook_defense=coach.playbook_defense
      ```

- **Line**: 129
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -     team = db.query(Team).filter(Team.id == request.team_id).first()
      ```

- **Line**: 165
  - **Error**: Incompatible types in assignment (expression has type "None", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     coach.team_id = None
      ```

- **Line**: 208
  - **Error**: Incompatible types in assignment (expression has type "None", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             current_hc.team_id = None  # Fire
      ```

- **Line**: 210
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         coach.role = "Head Coach"
      ```


## File: app/api/endpoints/data.py
- **Line**: 26
  - **Error**: Need type annotation for "state"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     state = game.game_data or {}
      +     state = game.game_data or {}
      ```

- **Line**: 37
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[Any] | Any", variable has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         possession = state["possession"]
      ```

- **Line**: 125
  - **Error**: No overload variant of "get" of "dict" matches argument types "str", "list[Never]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "get" of "dict" matches argument types "str", "list[Never]"
      -     logs = (game.game_data or {}).get("plays", [])
      ```


## File: app/api/endpoints/draft.py
- **Line**: 30
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
      -         .where(Player.is_rookie == True)
      ```

- **Line**: 30
  - **Error**: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -         .where(Player.is_rookie == True)
      ```


## File: app/api/endpoints/medical.py
- **Line**: 44
  - **Error**: Argument "head_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "head_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         head_health=health.head_health,
      ```

- **Line**: 45
  - **Error**: Argument "torso_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "torso_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         torso_health=health.torso_health,
      ```

- **Line**: 46
  - **Error**: Argument "right_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "right_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         right_arm_health=health.right_arm_health,
      ```

- **Line**: 47
  - **Error**: Argument "left_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "left_arm_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         left_arm_health=health.left_arm_health,
      ```

- **Line**: 48
  - **Error**: Argument "right_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "right_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         right_leg_health=health.right_leg_health,
      ```

- **Line**: 49
  - **Error**: Argument "left_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "left_leg_health" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         left_leg_health=health.left_leg_health,
      ```

- **Line**: 50
  - **Error**: Argument "general_wear" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "general_wear" to "BodyHealthResponse" has incompatible type "Column[float]"; expected "float"
      -         general_wear=health.general_wear,
      ```

- **Line**: 126
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_recurrence_risk += 0.10
      ```

- **Line**: 132
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.weeks_to_recovery = recovery_weeks
      ```

- **Line**: 153
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.QUESTIONABLE
      ```

- **Line**: 157
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.OUT
      ```

- **Line**: 191
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[InjuryStatus.ACTIVE]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[InjuryStatus.ACTIVE]")
      -         Player.injury_status != InjuryStatus.ACTIVE
      ```

- **Line**: 191
  - **Error**: Argument 2 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -         Player.injury_status != InjuryStatus.ACTIVE
      ```


## File: app/api/endpoints/playbook.py
- **Line**: 223
  - **Error**: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, object]], object]"; expected "Callable[[dict[str, object]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, object]], object]"; expected "Callable[[dict[str, object]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
      -     player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)
      ```

- **Line**: 223
  - **Error**: Incompatible return value type (got "object", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "object", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
      -     player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)
      ```

- **Line**: 225
  - **Error**: Generator has incompatible item type "object"; expected "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Generator has incompatible item type "object"; expected "bool"
      -     total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)
      ```


## File: app/api/endpoints/players.py
- **Line**: 79
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"
      -         "games_played": stats.games_played or 0,
      ```

- **Line**: 80
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_yards"
      -         "passing_yards": stats.passing_yards or 0,
      ```

- **Line**: 81
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "passing_tds"
      -         "passing_tds": stats.passing_tds or 0,
      ```

- **Line**: 82
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_yards"
      -         "rushing_yards": stats.rushing_yards or 0,
      ```

- **Line**: 83
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rushing_tds"
      -         "rushing_tds": stats.rushing_tds or 0,
      ```

- **Line**: 84
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_yards"
      -         "receiving_yards": stats.receiving_yards or 0,
      ```

- **Line**: 85
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "receiving_tds"
      -         "receiving_tds": stats.receiving_tds or 0,
      ```

- **Line**: 271
  - **Error**: "type[Player]" has no attribute "traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "type[Player]" has no attribute "traits"
      -     stmt = select(Player).options(selectinload(Player.traits)).where(Player.id == player_id)
      ```

- **Line**: 279
  - **Error**: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"
      -     trait_service = TraitService(db)
      ```

- **Line**: 280
  - **Error**: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")
      -     traits_data = await trait_service.get_player_traits(player_id)
      ```

- **Line**: 280
  - **Error**: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"
      -     traits_data = await trait_service.get_player_traits(player_id)
      ```

- **Line**: 280
  - **Error**: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"
      -     traits_data = await trait_service.get_player_traits(player_id)
      ```


## File: app/api/endpoints/scouts.py
- **Line**: 82
  - **Error**: Argument "scout_id" to "ScoutInfo" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "scout_id" to "ScoutInfo" has incompatible type "Column[Any]"; expected "int"
      -             scout_id=s.id,
      ```

- **Line**: 83
  - **Error**: Argument "name" to "ScoutInfo" has incompatible type "Column[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "name" to "ScoutInfo" has incompatible type "Column[str]"; expected "str"
      -             name=s.name,
      ```

- **Line**: 84
  - **Error**: Argument "region" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "region" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
      -             region=s.region or "NATIONAL",
      ```

- **Line**: 85
  - **Error**: Argument "specialty" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "specialty" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
      -             specialty=s.position_specialty or "GENERALIST",
      ```

- **Line**: 86
  - **Error**: Argument "bias" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "bias" to "ScoutInfo" has incompatible type "Column[str] | str"; expected "str"
      -             bias=s.bias or "NEUTRAL",
      ```

- **Line**: 87
  - **Error**: Argument "efficiency" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "efficiency" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"
      -             efficiency=s.efficiency,
      ```

- **Line**: 88
  - **Error**: Argument "accuracy" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "accuracy" to "ScoutInfo" has incompatible type "Column[int]"; expected "int"
      -             accuracy=s.evaluation_ability
      ```


## File: app/api/endpoints/season.py
- **Line**: 132
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     stmt = select(func.count(Game.id)).where(Game.season_id == season.id)
      ```

- **Line**: 136
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[int]]", variable has type "Select[tuple[Season]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     stmt = select(func.count(Game.id)).where(
      ```

- **Line**: 144
  - **Error**: Unsupported operand types for < ("int" and "Season")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for < ("int" and "Season")
      -     if total_games > 0:
      ```

- **Line**: 145
  - **Error**: Unsupported left operand type for / ("Season")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for / ("Season")
      -         completion = (games_played / total_games) * 100
      ```

- **Line**: 145
  - **Error**: Unsupported operand types for / ("Season" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("Season" and "int")
      -         completion = (games_played / total_games) * 100
      ```

- **Line**: 145
  - **Error**: Unsupported operand types for / ("int" and "Season")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("int" and "Season")
      -         completion = (games_played / total_games) * 100
      ```

- **Line**: 160
  - **Error**: Argument 1 to "get_bracket" of "PlayoffService" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "get_bracket" of "PlayoffService" has incompatible type "Column[Any]"; expected "int"
      -                     return playoff_service.get_bracket(season.id)
      ```

- **Line**: 237
  - **Error**: Argument 1 to "calculate_standings" of "StandingsCalculator" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "calculate_standings" of "StandingsCalculator" has incompatible type "Column[Any]"; expected "int"
      -                 return calculator.calculate_standings(season.id)
      ```

- **Line**: 243
  - **Error**: Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         conferences = {}
      +         conferences: dict = {}
      ```

- **Line**: 302
  - **Error**: Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         stmt = update(Season).values(is_active=False)
      ```

- **Line**: 306
  - **Error**: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         existing.is_active = True
      ```

- **Line**: 317
  - **Error**: Incompatible types in assignment (expression has type "Update", variable has type "Select[tuple[Season]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     stmt = update(Season).values(is_active=False)
      ```

- **Line**: 366
  - **Error**: Name "timedelta" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "timedelta" is not defined
      -             regular_start_date = start_date_val + timedelta(weeks=preseason_weeks_count)
      ```

- **Line**: 377
  - **Error**: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 game.is_preseason = False
      ```

- **Line**: 392
  - **Error**: Name "timedelta" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "timedelta" is not defined
      -         start_date = (today + timedelta(days=days_until_sunday)).replace(hour=13, minute=0, second=0, microsecond=0)
      ```

- **Line**: 476
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Game]]", variable has type "Select[tuple[Season]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     stmt = select(Game).options(
      ```

- **Line**: 547
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.status = SeasonStatus.REGULAR_SEASON
      ```

- **Line**: 548
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = 1
      ```

- **Line**: 551
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week += 1
      ```

- **Line**: 555
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.status = SeasonStatus.POST_SEASON
      ```

- **Line**: 556
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = 1
      ```

- **Line**: 558
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.status = SeasonStatus.OFF_SEASON
      ```

- **Line**: 560
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season.current_week += 1
      ```

- **Line**: 604
  - **Error**: Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         week = season.current_week
      ```

- **Line**: 611
  - **Error**: Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "int | None"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "int | None"; expected "int"
      -         week=week,
      ```

- **Line**: 620
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season.current_week += 1
      ```

- **Line**: 670
  - **Error**: Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "week" to "simulate_week" of "WeekSimulator" has incompatible type "Column[int]"; expected "int"
      -             week=season.current_week,
      ```

- **Line**: 677
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -              season.status = SeasonStatus.POST_SEASON
      ```

- **Line**: 678
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -              season.current_week = 1
      ```

- **Line**: 686
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int]", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -              season.current_week += 1
      ```

- **Line**: 905
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
      -             Player.is_rookie == True,
      ```

- **Line**: 905
  - **Error**: Argument 1 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "filter" of "Query" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -             Player.is_rookie == True,
      ```

- **Line**: 909
  - **Error**: Too many arguments for "DraftAssistant"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Too many arguments for "DraftAssistant"
      -         assistant = DraftAssistant(sync_db)
      ```

- **Line**: 910
  - **Error**: Missing positional arguments "available_players", "db" in call to "suggest_pick" of "DraftAssistant"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing positional arguments "available_players", "db" in call to "suggest_pick" of "DraftAssistant"
      -         suggestion = await assistant.suggest_pick(team_id, available_players)
      ```

- **Line**: 910
  - **Error**: Argument 2 to "suggest_pick" of "DraftAssistant" has incompatible type "list[Player]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "suggest_pick" of "DraftAssistant" has incompatible type "list[Player]"; expected "int"
      -         suggestion = await assistant.suggest_pick(team_id, available_players)
      ```

- **Line**: 1030
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
      -             stmt = stmt.where(Player.is_rookie == True)
      ```

- **Line**: 1030
  - **Error**: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -             stmt = stmt.where(Player.is_rookie == True)
      ```

- **Line**: 1048
  - **Error**: Incompatible types in assignment (expression has type "Any | float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 score = (p.pass_yards or 0)/10 + (p.pass_tds or 0)*6 - (p.pass_ints or 0)*3 + (p.rush_yards or 0)/10 + (p.rush_tds or 0)*6
      ```

- **Line**: 1093
  - **Error**: Incompatible types in assignment (expression has type "Column[Any] | int", variable has type "int | None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season_id = season.id if season else 0
      ```

- **Line**: 1096
  - **Error**: Argument 2 to "get_team_cap_breakdown" of "SalaryCapService" has incompatible type "int | None"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "get_team_cap_breakdown" of "SalaryCapService" has incompatible type "int | None"; expected "int"
      -     return service.get_team_cap_breakdown(team_id, season_id)
      ```

- **Line**: 1172
  - **Error**: Name "suggest_draft_pick" already defined on line 893
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "suggest_draft_pick" already defined on line 893
      - @router.post("/draft/suggest-pick", response_model=draft_schemas.DraftSuggestionResponse)
      ```


## File: app/api/endpoints/settings.py
- **Line**: 43
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         settings.user_team_id = update.user_team_id
      ```

- **Line**: 45
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         settings.difficulty_level = update.difficulty_level
      ```


## File: app/api/endpoints/simulation.py
- **Line**: 71
  - **Error**: Value of type "Coroutine[Any, Any, None]" must be used
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Value of type "Coroutine[Any, Any, None]" must be used
      -     orchestrator.start_new_game_session(home_team_id=1, away_team_id=2, config=request.config)
      ```


## File: app/api/endpoints/teams.py
- **Line**: 213
  - **Error**: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     head_coach.philosophy = current_philosophy
      ```


## File: app/api/endpoints/trades.py
- **Line**: 47
  - **Error**: Argument "team_id" to "TradeAssetRead" has incompatible type "int | None"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "team_id" to "TradeAssetRead" has incompatible type "int | None"; expected "int"
      -                 team_id=player.team_id,
      ```

- **Line**: 55
  - **Error**: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"
      -     offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
      ```

- **Line**: 55
  - **Error**: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"
      -     offered_assets = await _build_asset_list(db, offer.offered_player_ids or [], offer.offering_team_id)
      ```

- **Line**: 56
  - **Error**: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_build_asset_list" has incompatible type "Column[Any] | list[Never]"; expected "list[Any]"
      -     requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)
      ```

- **Line**: 56
  - **Error**: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 3 to "_build_asset_list" has incompatible type "Column[int]"; expected "int"
      -     requested_assets = await _build_asset_list(db, offer.requested_player_ids or [], offer.receiving_team_id)
      ```

- **Line**: 59
  - **Error**: Argument "id" to "TradeOfferRead" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "id" to "TradeOfferRead" has incompatible type "Column[Any]"; expected "int"
      -         id=offer.id,
      ```

- **Line**: 60
  - **Error**: Argument "offering_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offering_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"
      -         offering_team_id=offer.offering_team_id,
      ```

- **Line**: 61
  - **Error**: Argument "receiving_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "receiving_team_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int"
      -         receiving_team_id=offer.receiving_team_id,
      ```

- **Line**: 65
  - **Error**: Argument "message" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "message" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"
      -         message=offer.message,
      ```

- **Line**: 66
  - **Error**: Argument "gm_response" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "gm_response" to "TradeOfferRead" has incompatible type "Column[str]"; expected "str | None"
      -         gm_response=offer.gm_response,
      ```

- **Line**: 69
  - **Error**: Argument "parent_offer_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "parent_offer_id" to "TradeOfferRead" has incompatible type "Column[int]"; expected "int | None"
      -         parent_offer_id=offer.parent_offer_id
      ```

- **Line**: 109
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(Player).where(Player.id == player_id)
      ```

- **Line**: 121
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(Player).where(Player.id == player_id)
      ```

- **Line**: 129
  - **Error**: "Team" has no attribute "team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "team_id"
      -             if player.team_id != request.target_team_id:
      ```

- **Line**: 223
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[Team]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         stmt = select(Player).where(Player.id == request.offered_player_ids[0])
      ```

- **Line**: 227
  - **Error**: "Team" has no attribute "team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "team_id"
      -             offering_team_id = player.team_id
      ```

- **Line**: 255
  - **Error**: Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"
      -         offer_id=trade_offer.id,
      ```

- **Line**: 330
  - **Error**: Argument "team_id" to "GMAgent" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "team_id" to "GMAgent" has incompatible type "Column[int]"; expected "int"
      -                 gm_agent = GMAgent(db=sync_db, team_id=offer.receiving_team_id)
      ```

- **Line**: 335
  - **Error**: Argument "offered_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offered_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"
      -                     offered_players_ids=offer.offered_player_ids or [],
      ```

- **Line**: 336
  - **Error**: Argument "requested_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "requested_players_ids" to "evaluate_trade" of "GMAgent" has incompatible type "Column[Any] | list[Never]"; expected "list[int]"
      -                     requested_players_ids=offer.requested_player_ids or [],
      ```

- **Line**: 337
  - **Error**: Argument "offered_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offered_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"
      -                     offered_picks=offered_picks,
      ```

- **Line**: 338
  - **Error**: Argument "requested_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "requested_picks" to "evaluate_trade" of "GMAgent" has incompatible type "Reversible[Any]"; expected "list[dict[Any, Any]]"
      -                     requested_picks=requested_picks
      ```

- **Line**: 349
  - **Error**: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)
      -         for pid in offer.offered_player_ids or []:
      ```

- **Line**: 350
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(Player).where(Player.id == pid)
      ```

- **Line**: 354
  - **Error**: "TradeOffer" has no attribute "team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "TradeOffer" has no attribute "team_id"
      -                 player.team_id = offer.receiving_team_id
      ```

- **Line**: 357
  - **Error**: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "Column[Any]" of "Column[Any] | list[Never]" has no attribute "__iter__" (not iterable)
      -         for pid in offer.requested_player_ids or []:
      ```

- **Line**: 358
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[Player]]", variable has type "Select[tuple[TradeOffer]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(Player).where(Player.id == pid)
      ```

- **Line**: 362
  - **Error**: "TradeOffer" has no attribute "team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "TradeOffer" has no attribute "team_id"
      -                 player.team_id = offer.offering_team_id
      ```

- **Line**: 364
  - **Error**: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         offer.status = DBTradeOfferStatus.ACCEPTED
      ```

- **Line**: 365
  - **Error**: Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         offer.gm_response = gm_reasoning or request.message or "Trade accepted!"
      ```

- **Line**: 369
  - **Error**: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         offer.status = DBTradeOfferStatus.REJECTED
      ```

- **Line**: 370
  - **Error**: Incompatible types in assignment (expression has type "Any | str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         offer.gm_response = gm_reasoning or request.message or "Trade rejected."
      ```

- **Line**: 405
  - **Error**: Incompatible types in assignment (expression has type "TradeOfferStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     original_offer.status = DBTradeOfferStatus.COUNTERED
      ```

- **Line**: 406
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     original_offer.gm_response = "Counter-offer submitted."
      ```

- **Line**: 433
  - **Error**: Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "offer_id" to "TradeOfferResponse" has incompatible type "Column[Any]"; expected "int"
      -         offer_id=counter_offer.id,
      ```


## File: app/core/auth.py
- **Line**: 10
  - **Error**: Cannot find implementation or library stub for module named "firebase_admin"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot find implementation or library stub for module named "firebase_admin"
      - import firebase_admin
      ```

- **Line**: 83
  - **Error**: Returning Any from function declared to return "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "dict[Any, Any]"
      -         return decoded_token
      ```


## File: app/core/database.py
- **Line**: 22
  - **Error**: Dict entry 0 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 0 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
      -         "pool_size": settings.DB_POOL_SIZE,
      ```

- **Line**: 23
  - **Error**: Dict entry 1 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 1 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
      -         "max_overflow": settings.DB_MAX_OVERFLOW,
      ```

- **Line**: 24
  - **Error**: Dict entry 2 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 2 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
      -         "pool_timeout": settings.DB_POOL_TIMEOUT,
      ```

- **Line**: 25
  - **Error**: Dict entry 3 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 3 has incompatible type "str": "int"; expected "str": "bool | dict[str, bool] | type[StaticPool] | type[QueuePool]"
      -         "pool_recycle": settings.DB_POOL_RECYCLE,
      ```


## File: app/core/db_helpers.py
- **Line**: 9
  - **Error**: Incompatible default for argument "detail" (default has type "None", argument has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      - def get_object_or_404(db: Session, model: Type[T], object_id: Any, detail: str = None) -> T:
      ```

- **Line**: 13
  - **Error**: "type[T]" has no attribute "id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "type[T]" has no attribute "id"
      -     stmt = select(model).where(model.id == object_id)
      ```

- **Line**: 23
  - **Error**: Incompatible default for argument "detail" (default has type "None", argument has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      - async def get_object_or_404_async(db: AsyncSession, model: Type[T], object_id: Any, detail: str = None) -> T:
      ```

- **Line**: 27
  - **Error**: "type[T]" has no attribute "id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "type[T]" has no attribute "id"
      -     stmt = select(model).where(model.id == object_id)
      ```


## File: app/core/error_handlers.py
- **Line**: 16
  - **Error**: Incompatible return value type (got "Any | None", expected "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Any | None", expected "str")
      -     return getattr(request.state, "request_id", None)
      ```

- **Line**: 22
  - **Error**: Missing named argument "details" for "ErrorResponse"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "details" for "ErrorResponse"
      -     error_response = ErrorResponse(
      ```

- **Line**: 24
  - **Error**: Missing named argument "field" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "field" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 42
  - **Error**: Missing named argument "details" for "ErrorResponse"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "details" for "ErrorResponse"
      -     error_response = ErrorResponse(
      ```

- **Line**: 44
  - **Error**: Missing named argument "field" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "field" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 73
  - **Error**: Missing named argument "field" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "field" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 73
  - **Error**: Missing named argument "value" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "value" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 102
  - **Error**: Missing named argument "field" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "field" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 102
  - **Error**: Missing named argument "value" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "value" for "ErrorDetail"
      -         error=ErrorDetail(
      ```

- **Line**: 120
  - **Error**: Missing named argument "details" for "ErrorResponse"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "details" for "ErrorResponse"
      -     error_response = ErrorResponse(
      ```

- **Line**: 122
  - **Error**: Missing named argument "field" for "ErrorDetail"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing named argument "field" for "ErrorDetail"
      -         error=ErrorDetail(
      ```


## File: app/core/logging_config.py
- **Line**: 36
  - **Error**: Cannot find implementation or library stub for module named "structlog"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot find implementation or library stub for module named "structlog"
      - import structlog
      ```

- **Line**: 37
  - **Error**: Cannot find implementation or library stub for module named "structlog.types"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot find implementation or library stub for module named "structlog.types"
      - from structlog.types import EventDict, WrappedLogger
      ```

- **Line**: 369
  - **Error**: Returning Any from function declared to return "Response"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "Response"
      -             return response
      ```


## File: app/core/mcp_cache.py
- **Line**: 9
  - **Error**: Incompatible types in assignment (expression has type "None", variable has type Module)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     redis = None
      ```

- **Line**: 48
  - **Error**: Argument 1 to "loads" has incompatible type "Awaitable[Any] | Any"; expected "str | bytes | bytearray"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "loads" has incompatible type "Awaitable[Any] | Any"; expected "str | bytes | bytearray"
      -                     return json.loads(data)
      ```


## File: app/core/mcp_client.py
- **Line**: 40
  - **Error**: Item "None" of "ClientSession | None" has no attribute "initialize"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "ClientSession | None" has no attribute "initialize"
      -             await self.session.initialize()
      ```

- **Line**: 44
  - **Error**: Item "None" of "ClientSession | None" has no attribute "list_tools"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "ClientSession | None" has no attribute "list_tools"
      -             result = await self.session.list_tools()
      ```

- **Line**: 121
  - **Error**: Subclass of "CallToolResult" and "dict[Any, Any]" cannot exist: would have incompatible method signatures
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Subclass of "CallToolResult" and "dict[Any, Any]" cannot exist: would have incompatible method signatures
      -             sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
      ```

- **Line**: 121
  - **Error**: Subclass of "CallToolResult" and "list[Any]" cannot exist: would have incompatible method signatures
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Subclass of "CallToolResult" and "list[Any]" cannot exist: would have incompatible method signatures
      -             sanitized_result = self._sanitize(result) if isinstance(result, (dict, list)) else str(result)
      ```


## File: app/core/redis_cache.py
- **Line**: 33
  - **Error**: "Settings" has no attribute "REDIS_URL"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Settings" has no attribute "REDIS_URL"
      -                 settings.REDIS_URL,
      ```

- **Line**: 37
  - **Error**: Incompatible types in "await" (actual type "Awaitable[bool] | bool | Any", expected type "Awaitable[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible types in "await" (actual type "Awaitable[bool] | bool | Any", expected type "Awaitable[Any]")
      -             await self.redis.ping()
      ```

- **Line**: 81
  - **Error**: Returning Any from function declared to return "dict[Any, Any] | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "dict[Any, Any] | None"
      -                 return json.loads(cached)
      ```


## File: app/core/seed.py
- **Line**: 144
  - **Error**: Argument 2 to "generate_player" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "generate_player" has incompatible type "Column[Any]"; expected "int"
      -                 player = generate_player(pos, team.id)
      ```

- **Line**: 294
  - **Error**: Argument 1 to "calculate_overall_rating_modifier" has incompatible type "float | int"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "calculate_overall_rating_modifier" has incompatible type "float | int"; expected "int"
      -         final_overall = calculate_overall_rating_modifier(base_rating, p_data, accolades)
      ```

- **Line**: 383
  - **Error**: No overload variant of "get" of "dict" matches argument type "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "get" of "dict" matches argument type "str"
      -         team_id = team_lookup.get(fa.new_team)
      ```

- **Line**: 397
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             existing.contract_years = fa.contract_years
      ```

- **Line**: 398
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             existing.contract_salary = fa.apy
      ```

- **Line**: 401
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 existing.speed = fa.speed
      ```

- **Line**: 403
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 existing.strength = fa.strength
      ```

- **Line**: 405
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 existing.awareness = fa.awareness
      ```


## File: app/core/setup.py
- **Line**: 33
  - **Error**: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RateLimitExceeded], Response]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RateLimitExceeded], Response]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
      -     app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
      ```

- **Line**: 58
  - **Error**: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], IntegrityError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], IntegrityError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
      -     app.add_exception_handler(IntegrityError, database_exception_handler)
      ```

- **Line**: 59
  - **Error**: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], OperationalError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], OperationalError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
      -     app.add_exception_handler(OperationalError, database_operational_error_handler)
      ```

- **Line**: 60
  - **Error**: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RequestValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], RequestValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
      -     app.add_exception_handler(RequestValidationError, validation_exception_handler)
      ```

- **Line**: 61
  - **Error**: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], ValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "add_exception_handler" of "Starlette" has incompatible type "Callable[[Request[State], ValidationError], Coroutine[Any, Any, Any]]"; expected "Callable[[Request[State], Exception], Response | Awaitable[Response]] | Callable[[WebSocket, Exception], Awaitable[None]]"
      -     app.add_exception_handler(ValidationError, pydantic_validation_handler)
      ```


## File: app/core/trade_config.py
- **Line**: 106
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return self.POSITION_VALUE_TIERS[tier]["multiplier"]
      ```


## File: app/data/scouts.py
- **Line**: 28
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("BUF", "Marcus Williamson", Region.EAST, ScoutBias.ANALYTICS, None, 75, 70, 65),
      ```

- **Line**: 30
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("BUF", "Derek Sharpley", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 60),
      ```

- **Line**: 33
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("MIA", "Frank Johnson", Region.NATIONAL, ScoutBias.NEUTRAL, None, 72, 78, 68),
      ```

- **Line**: 36
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("NE", "Bill Langford", Region.EAST, ScoutBias.CHARACTER, None, 88, 55, 85),
      ```

- **Line**: 41
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("NYJ", "Sam Decker", Region.NATIONAL, ScoutBias.NEUTRAL, None, 70, 75, 65),
      ```

- **Line**: 46
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("BAL", "Eric DeCosta Jr", Region.SOUTH, ScoutBias.ANALYTICS, None, 85, 72, 82),
      ```

- **Line**: 47
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("BAL", "Keith Williams", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 75),
      ```

- **Line**: 50
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("CIN", "Paul Brown IV", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
      ```

- **Line**: 54
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("CLE", "Kevin Stefanski Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 72),
      ```

- **Line**: 58
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("PIT", "Omar Khan Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 78),
      ```

- **Line**: 63
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("HOU", "Devon Still", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 78, 70),
      ```

- **Line**: 67
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("IND", "Ed Dodds Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 75),
      ```

- **Line**: 71
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("JAX", "Tony Khan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 75, 75, 72),
      ```

- **Line**: 76
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("TEN", "David Caldwell", Region.EAST, ScoutBias.NEUTRAL, None, 75, 75, 70),
      ```

- **Line**: 80
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("DEN", "John Elway III", Region.NATIONAL, ScoutBias.CHARACTER, None, 78, 68, 82),
      ```

- **Line**: 84
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("KC", "Clark Hunt III", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 78, 80),
      ```

- **Line**: 92
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("LAC", "John Spanos", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 72),
      ```

- **Line**: 97
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("DAL", "Jerry Jones IV", Region.NATIONAL, ScoutBias.RAS_LOVER, None, 70, 75, 78),
      ```

- **Line**: 101
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("NYG", "Brian Daboll Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 75, 75),
      ```

- **Line**: 105
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("PHI", "Nick Sirianni Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
      ```

- **Line**: 109
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("WAS", "Adam Peters Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 80, 75, 75),
      ```

- **Line**: 118
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("DET", "Dan Campbell Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 72, 82),
      ```

- **Line**: 122
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("GB", "Matt LaFleur Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
      ```

- **Line**: 126
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("MIN", "Kevin O'Connell Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 78),
      ```

- **Line**: 135
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("CAR", "Dave Canales Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 75, 75, 70),
      ```

- **Line**: 139
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("NO", "Dennis Allen Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 78, 72, 75),
      ```

- **Line**: 152
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("LAR", "Sean McVay Jr", Region.NATIONAL, ScoutBias.NEUTRAL, None, 80, 75, 80),
      ```

- **Line**: 156
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("SF", "Kyle Shanahan Jr", Region.NATIONAL, ScoutBias.ANALYTICS, None, 85, 78, 85),
      ```

- **Line**: 160
  - **Error**: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 5 to "ScoutData" has incompatible type "None"; expected "str"
      -     ScoutData("SEA", "Pete Carroll Jr", Region.NATIONAL, ScoutBias.CHARACTER, None, 82, 70, 85),
      ```


## File: app/data/special_jerseys.py
- **Line**: 124
  - **Error**: Incompatible default for argument "year" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      - def get_thanksgiving_jersey(team_abbr: str, year: int = None) -> Dict[str, Any]:
      ```

- **Line**: 137
  - **Error**: Incompatible return value type (got "None", expected "dict[str, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "None", expected "dict[str, Any]")
      -     return None
      ```

- **Line**: 148
  - **Error**: Incompatible return value type (got "object", expected "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "object", expected "float")
      -         return THANKSGIVING_HOSTS[team_abbr]["home_field_boost"]
      ```


## File: app/engine/attribute_interaction.py
- **Line**: 671
  - **Error**: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
      -                     narrative = narrative.replace(f"{{{pos}}}", attacker_name)
      ```

- **Line**: 673
  - **Error**: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
      -                     narrative = narrative.replace(f"{{{pos}}}", defender_name)
      ```

- **Line**: 676
  - **Error**: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
      -         narrative = narrative.replace("{attacker}", attacker_name)
      ```

- **Line**: 677
  - **Error**: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "replace" of "str" has incompatible type "Any | None"; expected "str"
      -         narrative = narrative.replace("{defender}", defender_name)
      ```

- **Line**: 810
  - **Error**: Unsupported operand types for + ("object" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("object" and "float")
      -             aggregate["total_offense_boost"] += result.winner_boost
      ```

- **Line**: 813
  - **Error**: Unsupported operand types for + ("object" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("object" and "float")
      -             aggregate["total_defense_boost"] += result.loser_penalty
      ```

- **Line**: 815
  - **Error**: "object" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "object" has no attribute "append"
      -         aggregate["narratives"].append(result.narrative)
      ```

- **Line**: 816
  - **Error**: "object" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "object" has no attribute "append"
      -         aggregate["all_events"].append(result.to_dict())
      ```

- **Line**: 819
  - **Error**: "object" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "object" has no attribute "append"
      -             aggregate["dominant_events"].append(result.to_dict())
      ```


## File: app/engine/core/enhanced_event_bus.py
- **Line**: 249
  - **Error**: Argument 1 to "create_task" of "AbstractEventLoop" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "create_task" of "AbstractEventLoop" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"
      -                         loop.create_task(reg.handler(event))
      ```

- **Line**: 290
  - **Error**: Need type annotation for "task"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -                     task = asyncio.create_task(reg.handler(event))
      +                     task = asyncio.create_task(reg.handler(event))
      ```

- **Line**: 290
  - **Error**: Argument 1 to "create_task" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "create_task" has incompatible type "Future[None] | None"; expected "Generator[Any, None, Never] | Coroutine[Any, Any, Never]"
      -                     task = asyncio.create_task(reg.handler(event))
      ```


## File: app/engine/defense.py
- **Line**: 70
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -             return rng.randint(0, 100) < awareness
      ```


## File: app/engine/genesis/biometrics.py
- **Line**: 314
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return low + (high - low) * biased
      ```


## File: app/engine/offensive_line_ai.py
- **Line**: 34
  - **Error**: Returning Any from function declared to return "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "int"
      -             return self.active_debuffs[player_id]["pass_block_modifier"]
      ```


## File: app/engine/physics.py
- **Line**: 55
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -             x += vx * dt
      +             x += vx * dt  # Wrap expression in int()
      ```

- **Line**: 56
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -             y += vy * dt
      +             y += vy * dt  # Wrap expression in int()
      ```

- **Line**: 58
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -             t += dt
      +             t += dt  # Wrap expression in int()
      ```


## File: app/engine/position_physics/offensive_line.py
- **Line**: 177
  - **Error**: Need type annotation for "assignments" (hint: "assignments: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         assignments = {}
      +         assignments: dict = {}
      ```

- **Line**: 185
  - **Error**: Incompatible types in assignment (expression has type "None", target has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 assignments[blocker_id] = None
      ```

- **Line**: 205
  - **Error**: Incompatible types in assignment (expression has type "None", target has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 assignments[blocker_id] = None
      ```

- **Line**: 207
  - **Error**: Incompatible return value type (got "dict[str, str]", expected "dict[str, str | None]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "dict[str, str]", expected "dict[str, str | None]")
      -         return assignments
      ```

- **Line**: 267
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return roll < prob
      ```


## File: app/engine/position_physics/pass_rush.py
- **Line**: 174
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -             cumulative += weight
      +             cumulative += weight  # Wrap expression in int()
      ```


## File: app/engine/position_physics/running_back.py
- **Line**: 325
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return roll < fumble_prob
      ```


## File: app/engine/probability_engine.py
- **Line**: 162
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return rng.random() < probability
      ```

- **Line**: 211
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return base_value + random_factor + modifiers
      ```

- **Line**: 226
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return max(min_val, min(max_val, val))
      ```


## File: app/engine/rb_tribes.py
- **Line**: 145
  - **Error**: Dict entry 0 has incompatible type "str": "str"; expected "str": "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 0 has incompatible type "str": "str"; expected "str": "float"
      -         "tribe": tribe.value,
      ```

- **Line**: 150
  - **Error**: Dict entry 5 has incompatible type "str": "str"; expected "str": "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 5 has incompatible type "str": "str"; expected "str": "float"
      -         "description": profile.description
      ```


## File: app/engine/venue_effects.py
- **Line**: 45
  - **Error**: Unsupported operand types for + ("float" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "object")
      -             modifier += THANKSGIVING_HOSTS[self.home_team]["home_field_boost"]
      ```

- **Line**: 115
  - **Error**: Incompatible types in assignment (expression has type "object", target has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         atmosphere["tradition_started"] = host_data["tradition_started"]
      ```

- **Line**: 116
  - **Error**: Incompatible types in assignment (expression has type "object", target has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         atmosphere["game_slot"] = host_data["game_slot"]
      ```


## File: app/engine/weather_effects.py
- **Line**: 35
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             accuracy -= wind_over * 0.008   # -0.8% per mph over 10 (calibrated)
      ```

- **Line**: 36
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             distance -= wind_over * 0.005   # -0.5% per mph over 10
      ```

- **Line**: 66
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             accuracy -= wind_over * 0.015   # -1.5% per mph over 5
      ```

- **Line**: 67
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             distance -= wind_over * 0.008   # -0.8% per mph over 5
      ```

- **Line**: 71
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             distance -= (40 - self.weather.temperature) * 0.004  # -0.4% per degree under 40
      ```

- **Line**: 106
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             multiplier += (self.weather.temperature - 85) * 0.02
      ```

- **Line**: 110
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             multiplier += (self.weather.humidity - 0.7) * 0.5
      ```


## File: app/kernels/core/sim_engine.py
- **Line**: 17
  - **Error**: Incompatible return value type (got "Component | None", expected "Component")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Component | None", expected "Component")
      -         return self.components.get(comp_type, {}).get(entity_id)
      ```

- **Line**: 25
  - **Error**: Name "PhysicsKernel" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "PhysicsKernel" is not defined
      -     physics_kernel: 'PhysicsKernel' = None
      ```

- **Line**: 26
  - **Error**: Name "AIKernel" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "AIKernel" is not defined
      -     ai_kernel: 'AIKernel' = None
      ```


## File: app/kernels/cortex/behavior_tree.py
- **Line**: 16
  - **Error**: Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         self.context = {}
      +         self.context: dict = {}
      ```

- **Line**: 29
  - **Error**: Returning Any from function declared to return "NodeStatus"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "NodeStatus"
      -                 return status
      ```

- **Line**: 40
  - **Error**: Returning Any from function declared to return "NodeStatus"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "NodeStatus"
      -                 return status
      ```


## File: app/kernels/cortex/coverage_net.py
- **Line**: 29
  - **Error**: Incompatible return value type (got "Any | None", expected "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Any | None", expected "str")
      -         return closest_defender
      ```


## File: app/kernels/empire/econ_dynamics.py
- **Line**: 11
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return bonus_per_year * years_remaining
      ```


## File: app/kernels/genesis/trauma_center.py
- **Line**: 21
  - **Error**: Name "AnatomyModel" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "AnatomyModel" is not defined
      -     def administer_shot(self, anatomy: 'AnatomyModel'):
      ```


## File: app/kernels/hive/weather.py
- **Line**: 39
  - **Error**: Missing return statement
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing return statement
      -     def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
      ```

- **Line**: 63
  - **Error**: Name "get_ballistic_modifiers" already defined on line 20
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "get_ballistic_modifiers" already defined on line 20
      -     def get_ballistic_modifiers(self) -> Tuple[float, float, float]:
      ```

- **Line**: 78
  - **Error**: Name "get_visibility_penalty" already defined on line 31
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "get_visibility_penalty" already defined on line 31
      -     def get_visibility_penalty(self) -> float:
      ```

- **Line**: 91
  - **Error**: Name "get_sun_glare_vector" already defined on line 39
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "get_sun_glare_vector" already defined on line 39
      -     def get_sun_glare_vector(self, time_of_day: str, stadium_orientation: float) -> float:
      ```


## File: app/kernels/society/social_graph.py
- **Line**: 4
  - **Error**: Library stubs not installed for "networkx"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Library stubs not installed for "networkx"
      - import networkx as nx
      ```

- **Line**: 20
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -             return self.graph[p1][p2]['weight']
      ```


## File: app/models/base.py
- **Line**: 7
  - **Error**: Cannot override class variable (previously declared on base class "DeclarativeBase") with instance variable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot override class variable (previously declared on base class "DeclarativeBase") with instance variable
      -     __name__: str
      ```


## File: app/models/coach.py
- **Line**: 21
  - **Error**: Need type annotation for "tier"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     tier = Column(SQLEnum(CoachTier), default=CoachTier.DEVELOPING, nullable=False)
      +     tier = Column(SQLEnum(CoachTier), default=CoachTier.DEVELOPING, nullable=False)
      ```


## File: app/models/game.py
- **Line**: 33
  - **Error**: Need type annotation for "game_type"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     game_type = Column(SQLEnum(GameType), default=GameType.REGULAR, nullable=False)
      +     game_type = Column(SQLEnum(GameType), default=GameType.REGULAR, nullable=False)
      ```


## File: app/models/player.py
- **Line**: 73
  - **Error**: Name "Team" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "Team" is not defined
      -     team: Mapped[Optional["Team"]] = relationship("Team", back_populates="players")
      ```

- **Line**: 79
  - **Error**: Name "speed" already defined on line 76
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "speed" already defined on line 76
      -     @speed.setter
      ```

- **Line**: 86
  - **Error**: Name "acceleration" already defined on line 83
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "acceleration" already defined on line 83
      -     @acceleration.setter
      ```

- **Line**: 93
  - **Error**: Name "strength" already defined on line 90
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "strength" already defined on line 90
      -     @strength.setter
      ```

- **Line**: 100
  - **Error**: Name "agility" already defined on line 97
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "agility" already defined on line 97
      -     @agility.setter
      ```

- **Line**: 107
  - **Error**: Name "awareness" already defined on line 104
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "awareness" already defined on line 104
      -     @awareness.setter
      ```

- **Line**: 114
  - **Error**: Name "stamina" already defined on line 111
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "stamina" already defined on line 111
      -     @stamina.setter
      ```

- **Line**: 121
  - **Error**: Name "injury_resistance" already defined on line 118
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "injury_resistance" already defined on line 118
      -     @injury_resistance.setter
      ```

- **Line**: 129
  - **Error**: Name "forty_yard_dash" already defined on line 126
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "forty_yard_dash" already defined on line 126
      -     @forty_yard_dash.setter
      ```

- **Line**: 136
  - **Error**: Name "bench_press" already defined on line 133
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "bench_press" already defined on line 133
      -     @bench_press.setter
      ```

- **Line**: 143
  - **Error**: Name "vertical_jump" already defined on line 140
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "vertical_jump" already defined on line 140
      -     @vertical_jump.setter
      ```

- **Line**: 150
  - **Error**: Name "broad_jump" already defined on line 147
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "broad_jump" already defined on line 147
      -     @broad_jump.setter
      ```

- **Line**: 157
  - **Error**: Name "three_cone_drill" already defined on line 154
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "three_cone_drill" already defined on line 154
      -     @three_cone_drill.setter
      ```

- **Line**: 164
  - **Error**: Name "twenty_yard_shuttle" already defined on line 161
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "twenty_yard_shuttle" already defined on line 161
      -     @twenty_yard_shuttle.setter
      ```

- **Line**: 172
  - **Error**: Name "power_clean_max" already defined on line 169
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "power_clean_max" already defined on line 169
      -     @power_clean_max.setter
      ```

- **Line**: 179
  - **Error**: Name "gps_speed_max" already defined on line 176
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "gps_speed_max" already defined on line 176
      -     @gps_speed_max.setter
      ```

- **Line**: 186
  - **Error**: Name "s2_cognition_score" already defined on line 183
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "s2_cognition_score" already defined on line 183
      -     @s2_cognition_score.setter
      ```

- **Line**: 193
  - **Error**: Name "medical_flags" already defined on line 190
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "medical_flags" already defined on line 190
      -     @medical_flags.setter
      ```

- **Line**: 200
  - **Error**: Name "genesis_revealed" already defined on line 197
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "genesis_revealed" already defined on line 197
      -     @genesis_revealed.setter
      ```

- **Line**: 208
  - **Error**: Name "throw_power" already defined on line 205
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "throw_power" already defined on line 205
      -     @throw_power.setter
      ```

- **Line**: 215
  - **Error**: Name "throw_accuracy_short" already defined on line 212
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "throw_accuracy_short" already defined on line 212
      -     @throw_accuracy_short.setter
      ```

- **Line**: 222
  - **Error**: Name "throw_accuracy_mid" already defined on line 219
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "throw_accuracy_mid" already defined on line 219
      -     @throw_accuracy_mid.setter
      ```

- **Line**: 229
  - **Error**: Name "throw_accuracy_deep" already defined on line 226
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "throw_accuracy_deep" already defined on line 226
      -     @throw_accuracy_deep.setter
      ```

- **Line**: 236
  - **Error**: Name "catching" already defined on line 233
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "catching" already defined on line 233
      -     @catching.setter
      ```

- **Line**: 243
  - **Error**: Name "route_running" already defined on line 240
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "route_running" already defined on line 240
      -     @route_running.setter
      ```

- **Line**: 250
  - **Error**: Name "pass_block" already defined on line 247
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pass_block" already defined on line 247
      -     @pass_block.setter
      ```

- **Line**: 257
  - **Error**: Name "run_block" already defined on line 254
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "run_block" already defined on line 254
      -     @run_block.setter
      ```

- **Line**: 264
  - **Error**: Name "tackle" already defined on line 261
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "tackle" already defined on line 261
      -     @tackle.setter
      ```

- **Line**: 271
  - **Error**: Name "hit_power" already defined on line 268
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "hit_power" already defined on line 268
      -     @hit_power.setter
      ```

- **Line**: 278
  - **Error**: Name "block_shed" already defined on line 275
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "block_shed" already defined on line 275
      -     @block_shed.setter
      ```

- **Line**: 285
  - **Error**: Name "man_coverage" already defined on line 282
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "man_coverage" already defined on line 282
      -     @man_coverage.setter
      ```

- **Line**: 292
  - **Error**: Name "zone_coverage" already defined on line 289
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "zone_coverage" already defined on line 289
      -     @zone_coverage.setter
      ```

- **Line**: 299
  - **Error**: Name "pass_rush_power" already defined on line 296
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pass_rush_power" already defined on line 296
      -     @pass_rush_power.setter
      ```

- **Line**: 306
  - **Error**: Name "pass_rush_finesse" already defined on line 303
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pass_rush_finesse" already defined on line 303
      -     @pass_rush_finesse.setter
      ```

- **Line**: 313
  - **Error**: Name "play_recognition" already defined on line 310
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "play_recognition" already defined on line 310
      -     @play_recognition.setter
      ```

- **Line**: 320
  - **Error**: Name "kick_power" already defined on line 317
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "kick_power" already defined on line 317
      -     @kick_power.setter
      ```

- **Line**: 327
  - **Error**: Name "kick_accuracy" already defined on line 324
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "kick_accuracy" already defined on line 324
      -     @kick_accuracy.setter
      ```

- **Line**: 335
  - **Error**: Name "pocket_presence" already defined on line 332
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pocket_presence" already defined on line 332
      -     @pocket_presence.setter
      ```

- **Line**: 342
  - **Error**: Name "quick_release" already defined on line 339
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "quick_release" already defined on line 339
      -     @quick_release.setter
      ```

- **Line**: 349
  - **Error**: Name "scramble_willingness" already defined on line 346
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "scramble_willingness" already defined on line 346
      -     @scramble_willingness.setter
      ```

- **Line**: 356
  - **Error**: Name "throw_on_run" already defined on line 353
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "throw_on_run" already defined on line 353
      -     @throw_on_run.setter
      ```

- **Line**: 363
  - **Error**: Name "patience" already defined on line 360
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "patience" already defined on line 360
      -     @patience.setter
      ```

- **Line**: 370
  - **Error**: Name "pass_pro_rating" already defined on line 367
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pass_pro_rating" already defined on line 367
      -     @pass_pro_rating.setter
      ```

- **Line**: 377
  - **Error**: Name "juke_efficiency" already defined on line 374
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "juke_efficiency" already defined on line 374
      -     @juke_efficiency.setter
      ```

- **Line**: 384
  - **Error**: Name "release" already defined on line 381
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "release" already defined on line 381
      -     @release.setter
      ```

- **Line**: 391
  - **Error**: Name "blocking_tenacity" already defined on line 388
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "blocking_tenacity" already defined on line 388
      -     @blocking_tenacity.setter
      ```

- **Line**: 398
  - **Error**: Name "pull_speed" already defined on line 395
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "pull_speed" already defined on line 395
      -     @pull_speed.setter
      ```

- **Line**: 405
  - **Error**: Name "anchor" already defined on line 402
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "anchor" already defined on line 402
      -     @anchor.setter
      ```

- **Line**: 412
  - **Error**: Name "discipline" already defined on line 409
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "discipline" already defined on line 409
      -     @discipline.setter
      ```

- **Line**: 419
  - **Error**: Name "first_step" already defined on line 416
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "first_step" already defined on line 416
      -     @first_step.setter
      ```

- **Line**: 426
  - **Error**: Name "gap_integrity" already defined on line 423
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "gap_integrity" already defined on line 423
      -     @gap_integrity.setter
      ```

- **Line**: 433
  - **Error**: Name "coverage_disguise" already defined on line 430
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "coverage_disguise" already defined on line 430
      -     @coverage_disguise.setter
      ```

- **Line**: 440
  - **Error**: Name "blitz_timing" already defined on line 437
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "blitz_timing" already defined on line 437
      -     @blitz_timing.setter
      ```

- **Line**: 447
  - **Error**: Name "run_fit" already defined on line 444
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "run_fit" already defined on line 444
      -     @run_fit.setter
      ```

- **Line**: 454
  - **Error**: Name "press" already defined on line 451
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "press" already defined on line 451
      -     @press.setter
      ```

- **Line**: 461
  - **Error**: Name "ball_tracking" already defined on line 458
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "ball_tracking" already defined on line 458
      -     @ball_tracking.setter
      ```

- **Line**: 468
  - **Error**: Name "run_support" already defined on line 465
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "run_support" already defined on line 465
      -     @run_support.setter
      ```

- **Line**: 475
  - **Error**: Name "hang_time" already defined on line 472
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "hang_time" already defined on line 472
      -     @hang_time.setter
      ```

- **Line**: 482
  - **Error**: Name "coffin_corner" already defined on line 479
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "coffin_corner" already defined on line 479
      -     @coffin_corner.setter
      ```

- **Line**: 489
  - **Error**: Name "return_vision" already defined on line 486
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "return_vision" already defined on line 486
      -     @return_vision.setter
      ```

- **Line**: 497
  - **Error**: Name "arm_slot" already defined on line 494
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "arm_slot" already defined on line 494
      -     @arm_slot.setter
      ```

- **Line**: 504
  - **Error**: Name "release_point_height" already defined on line 501
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "release_point_height" already defined on line 501
      -     @release_point_height.setter
      ```

- **Line**: 511
  - **Error**: Name "vision_cone_angle" already defined on line 508
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "vision_cone_angle" already defined on line 508
      -     @vision_cone_angle.setter
      ```

- **Line**: 518
  - **Error**: Name "break_tackle_threshold" already defined on line 515
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "break_tackle_threshold" already defined on line 515
      -     @break_tackle_threshold.setter
      ```

- **Line**: 526
  - **Error**: Name "xp" already defined on line 523
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "xp" already defined on line 523
      -     @xp.setter
      ```

- **Line**: 533
  - **Error**: Name "level" already defined on line 530
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "level" already defined on line 530
      -     @level.setter
      ```

- **Line**: 540
  - **Error**: Name "skill_points" already defined on line 537
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "skill_points" already defined on line 537
      -     @skill_points.setter
      ```

- **Line**: 547
  - **Error**: Name "development_trait" already defined on line 544
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "development_trait" already defined on line 544
      -     @development_trait.setter
      ```

- **Line**: 558
  - **Error**: Name "abilities" already defined on line 555
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "abilities" already defined on line 555
      -     @abilities.setter
      ```

- **Line**: 566
  - **Error**: Name "attribute_xp" already defined on line 563
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "attribute_xp" already defined on line 563
      -     @attribute_xp.setter
      ```

- **Line**: 574
  - **Error**: Name "morale" already defined on line 571
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "morale" already defined on line 571
      -     @morale.setter
      ```

- **Line**: 582
  - **Error**: Name "injury_status" already defined on line 579
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "injury_status" already defined on line 579
      -     @injury_status.setter
      ```

- **Line**: 589
  - **Error**: Name "injury_type" already defined on line 586
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "injury_type" already defined on line 586
      -     @injury_type.setter
      ```

- **Line**: 596
  - **Error**: Name "weeks_to_recovery" already defined on line 593
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "weeks_to_recovery" already defined on line 593
      -     @weeks_to_recovery.setter
      ```

- **Line**: 603
  - **Error**: Name "injury_severity" already defined on line 600
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "injury_severity" already defined on line 600
      -     @injury_severity.setter
      ```

- **Line**: 610
  - **Error**: Name "injury_recurrence_risk" already defined on line 607
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "injury_recurrence_risk" already defined on line 607
      -     @injury_recurrence_risk.setter
      ```

- **Line**: 622
  - **Error**: Name "contract_years" already defined on line 619
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "contract_years" already defined on line 619
      -     @contract_years.setter
      ```

- **Line**: 629
  - **Error**: Name "contract_salary" already defined on line 626
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "contract_salary" already defined on line 626
      -     @contract_salary.setter
      ```

- **Line**: 636
  - **Error**: Name "is_rookie" already defined on line 633
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "is_rookie" already defined on line 633
      -     @is_rookie.setter
      ```

- **Line**: 643
  - **Error**: Name "is_retired" already defined on line 640
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "is_retired" already defined on line 640
      -     @is_retired.setter
      ```

- **Line**: 650
  - **Error**: Name "retirement_year" already defined on line 647
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "retirement_year" already defined on line 647
      -     @retirement_year.setter
      ```

- **Line**: 657
  - **Error**: Name "legacy_score" already defined on line 654
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "legacy_score" already defined on line 654
      -     @legacy_score.setter
      ```

- **Line**: 662
  - **Error**: Name "PlayerSeasonStats" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "PlayerSeasonStats" is not defined
      -     season_stats: Mapped[List["PlayerSeasonStats"]] = relationship("PlayerSeasonStats", back_populates="player")
      ```

- **Line**: 668
  - **Error**: Name "BodyPart" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "BodyPart" is not defined
      -     body_health: Mapped["BodyPart"] = relationship("BodyPart", back_populates="player", uselist=False)
      ```


## File: app/models/player_game_starts.py
- **Line**: 27
  - **Error**: Name "Player" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "Player" is not defined
      -     player: Mapped["Player"] = relationship(back_populates="game_starts")
      ```

- **Line**: 28
  - **Error**: Name "Game" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "Game" is not defined
      -     game: Mapped["Game"] = relationship(back_populates="player_starts")
      ```


## File: app/models/playoff.py
- **Line**: 27
  - **Error**: Need type annotation for "round"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     round = Column(SQLEnum(PlayoffRound), nullable=False)
      +     round = Column(SQLEnum(PlayoffRound), nullable=False)
      ```

- **Line**: 28
  - **Error**: Need type annotation for "conference"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     conference = Column(SQLEnum(PlayoffConference), nullable=False)
      +     conference = Column(SQLEnum(PlayoffConference), nullable=False)
      ```


## File: app/models/season.py
- **Line**: 26
  - **Error**: Need type annotation for "status"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     status = Column(SQLEnum(SeasonStatus), default=SeasonStatus.REGULAR_SEASON, nullable=False)
      +     status = Column(SQLEnum(SeasonStatus), default=SeasonStatus.REGULAR_SEASON, nullable=False)
      ```


## File: app/models/trade_offer.py
- **Line**: 45
  - **Error**: Need type annotation for "status"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -     status = Column(
      +     status = Column(
      ```

- **Line**: 82
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             return False
      ```

- **Line**: 83
  - **Error**: Incompatible return value type (got "ColumnElement[bool]", expected "bool")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "ColumnElement[bool]", expected "bool")
      -         return datetime.utcnow() > self.expires_at
      ```


## File: app/models/trait.py
- **Line**: 63
  - **Error**: Name "Player" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "Player" is not defined
      -     player: Mapped["Player"] = relationship(back_populates="player_traits")
      ```


## File: app/orchestrator/game_repository.py
- **Line**: 60
  - **Error**: "Game" has no attribute "current_quarter"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Game" has no attribute "current_quarter"
      -                 game.current_quarter = state.get("quarter", 1)
      ```

- **Line**: 61
  - **Error**: "Game" has no attribute "time_left"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Game" has no attribute "time_left"
      -                 game.time_left = state.get("time_left", "15:00")
      ```

- **Line**: 67
  - **Error**: Incompatible types in assignment (expression has type "dict[Any, Any]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 game.game_data = current_data
      ```

- **Line**: 91
  - **Error**: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 game.is_played = True
      ```


## File: app/orchestrator/kernels/genesis_kernel.py
- **Line**: 30
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return state.lactic_acid
      ```

- **Line**: 41
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -         return state.lactic_acid
      ```


## File: app/orchestrator/match_context.py
- **Line**: 25
  - **Error**: Incompatible default for argument "weather_config" (default has type "None", argument has type "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, home_team_id: int, away_team_id: int, db: AsyncSession, weather_config: Dict = None):
      ```

- **Line**: 77
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -             p.active_traits = [pt.trait.name for pt in p.player_traits if pt.trait]
      ```


## File: app/orchestrator/play_caller.py
- **Line**: 148
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return self.rng.random() < pass_prob
      ```

- **Line**: 152
  - **Error**: Name "Player" is not defined
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "Player" is not defined
      -         qb: "Player",
      ```


## File: app/orchestrator/play_resolver.py
- **Line**: 130
  - **Error**: Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -             context = {}
      +             context: dict = {}
      ```

- **Line**: 131
  - **Error**: Right operand of "and" is never evaluated
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Right operand of "and" is never evaluated
      -             if self.current_match_context and self.current_match_context.weather_config:
      ```

- **Line**: 132
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -                 context["weather"] = self.current_match_context.weather_config
      ```

- **Line**: 138
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             play_context = self._build_injury_play_context(command, result)
      ```

- **Line**: 173
  - **Error**: Right operand of "and" is never evaluated
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Right operand of "and" is never evaluated
      -         if self.current_match_context and self.current_match_context.weather_config:
      ```

- **Line**: 174
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             return self.current_match_context.weather_config.get("temperature", 75.0)
      ```

- **Line**: 198
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             medical_rating = getattr(self.current_match_context, "medical_staff_rating", 50)
      ```

- **Line**: 221
  - **Error**: Right operand of "or" is never evaluated
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Right operand of "or" is never evaluated
      -         if not self.current_match_context or not self.current_match_context.weather_config:
      ```

- **Line**: 224
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         config = self.current_match_context.weather_config
      ```

- **Line**: 309
  - **Error**: Unexpected keyword argument "ratings" for "WideReceiverPhysics"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unexpected keyword argument "ratings" for "WideReceiverPhysics"
      -         return WideReceiverPhysics(
      ```

- **Line**: 309
  - **Error**: Unexpected keyword argument "hand_size" for "WideReceiverPhysics"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unexpected keyword argument "hand_size" for "WideReceiverPhysics"
      -         return WideReceiverPhysics(
      ```

- **Line**: 331
  - **Error**: Unexpected keyword argument "ratings" for "RunningBackPhysics"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unexpected keyword argument "ratings" for "RunningBackPhysics"
      -         return RunningBackPhysics(
      ```

- **Line**: 333
  - **Error**: Argument "weight" to "RunningBackPhysics" has incompatible type "float"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "weight" to "RunningBackPhysics" has incompatible type "float"; expected "int"
      -             weight=float(getattr(rb, "weight", 210)),
      ```

- **Line**: 352
  - **Error**: Unexpected keyword argument "ratings" for "DefensiveBackPhysics"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unexpected keyword argument "ratings" for "DefensiveBackPhysics"
      -         return DefensiveBackPhysics(ratings=ratings)
      ```

- **Line**: 441
  - **Error**: Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         context = {}
      +         context: dict = {}
      ```

- **Line**: 446
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             context = {
      ```

- **Line**: 507
  - **Error**: Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         context = {}
      +         context: dict = {}
      ```

- **Line**: 511
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             context = {
      ```

- **Line**: 656
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -                  if getattr(command, "is_home_team", True):
      ```

- **Line**: 724
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             interaction_results = {
      ```

- **Line**: 861
  - **Error**: Need type annotation for "crunch_context" (hint: "crunch_context: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -             crunch_context = {}
      +             crunch_context: dict = {}
      ```

- **Line**: 863
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -                 crunch_context = {
      ```

- **Line**: 919
  - **Error**: Right operand of "and" is never evaluated
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Right operand of "and" is never evaluated
      -         if self.momentum_engine and self.current_match_context:
      ```

- **Line**: 921
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
      ```

- **Line**: 1184
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             interaction_results = {
      ```

- **Line**: 1310
  - **Error**: Right operand of "and" is never evaluated
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Right operand of "and" is never evaluated
      -         if self.momentum_engine and self.current_match_context:
      ```

- **Line**: 1311
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             offense_team_id = str(getattr(self.current_match_context, 'home_team_id', 'home'))
      ```


## File: app/orchestrator/simulation_orchestrator.py
- **Line**: 66
  - **Error**: Need type annotation for "game_config" (hint: "game_config: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         self.game_config = {}
      +         self.game_config: dict = {}
      ```

- **Line**: 93
  - **Error**: Incompatible types in assignment (expression has type "Column[Any]", variable has type "None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             self.current_game_id = new_game.id
      ```

- **Line**: 123
  - **Error**: Argument 1 to "record_starters" of "PreGameService" has incompatible type "Column[Any]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "record_starters" of "PreGameService" has incompatible type "Column[Any]"; expected "int"
      -                 await pre_game_service.record_starters(new_game.id, home_team_id, away_team_id)
      ```

- **Line**: 133
  - **Error**: Incompatible types in assignment (expression has type "MomentumEngine", variable has type "None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             self.play_resolver.momentum_engine = self.momentum_engine
      ```

- **Line**: 156
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         try:
      ```

- **Line**: 183
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         try:
      ```

- **Line**: 219
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "execute"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "execute"
      -             home_result = await self.db_session.execute(home_stmt)
      ```

- **Line**: 220
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "execute"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "execute"
      -             away_result = await self.db_session.execute(away_stmt)
      ```

- **Line**: 238
  - **Error**: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     home_team.elo_rating or 1500.0,
      ```

- **Line**: 239
  - **Error**: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     away_team.elo_rating or 1500.0,
      ```

- **Line**: 245
  - **Error**: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     home_team.elo_rating or 1500.0,
      ```

- **Line**: 246
  - **Error**: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     away_team.elo_rating or 1500.0,
      ```

- **Line**: 252
  - **Error**: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     away_team.elo_rating or 1500.0,
      ```

- **Line**: 253
  - **Error**: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "update_ratings" of "EloService" has incompatible type "Column[float] | Any | float"; expected "float"
      -                     home_team.elo_rating or 1500.0,
      ```

- **Line**: 261
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "commit"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "commit"
      -             await self.db_session.commit()
      ```

- **Line**: 276
  - **Error**: Incompatible default for argument "game" (default has type "None", argument has type "Game")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     async def _save_player_stats(self, game: Game = None) -> None:
      ```

- **Line**: 283
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -              stmt = select(Game).where(Game.id == self.current_game_id)
      ```

- **Line**: 351
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "execute"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "execute"
      -                 result = await self.db_session.execute(stmt)
      ```

- **Line**: 354
  - **Error**: Incompatible types in assignment (expression has type "int | Any | None", variable has type "Column[int] | None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     team_id = player.team_id
      ```

- **Line**: 360
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStats]]", variable has type "Select[tuple[Player]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(PlayerGameStats).where(
      ```

- **Line**: 364
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "execute"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "execute"
      -             result = await self.db_session.execute(stmt)
      ```

- **Line**: 375
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "add"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "add"
      -                 self.db_session.add(pgs)
      ```

- **Line**: 383
  - **Error**: Item "None" of "AsyncSession | None" has no attribute "commit"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "AsyncSession | None" has no attribute "commit"
      -         await self.db_session.commit()
      ```

- **Line**: 395
  - **Error**: Need type annotation for "offense_players" (hint: "offense_players: list[<type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         offense_players = []
      +         offense_players: list = []
      ```

- **Line**: 396
  - **Error**: Need type annotation for "defense_players" (hint: "defense_players: list[<type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         defense_players = []
      +         defense_players: list = []
      ```

- **Line**: 425
  - **Error**: Value of type "Coroutine[Any, Any, None]" must be used
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Value of type "Coroutine[Any, Any, None]" must be used
      -         self._save_progress()
      ```

- **Line**: 605
  - **Error**: Incompatible types in assignment (expression has type "dict[str, int]", variable has type "CoachingPhilosophy")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             coach_philosophy = {
      ```

- **Line**: 640
  - **Error**: "PlayResult" has no attribute "player_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "PlayResult" has no attribute "player_modifiers"
      -             result.player_modifiers = result.player_modifiers or {}
      ```

- **Line**: 641
  - **Error**: "PlayResult" has no attribute "player_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "PlayResult" has no attribute "player_modifiers"
      -             result.player_modifiers["quarterback_read"] = qb_read
      ```

- **Line**: 928
  - **Error**: Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"
      -                     time_remaining=post_play_time,
      ```

- **Line**: 952
  - **Error**: Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "time_remaining" to "GameSituation" has incompatible type "float"; expected "int"
      -                         time_remaining=post_play_time,
      ```


## File: app/rpg/injury_system.py
- **Line**: 12
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, seed: int = None):
      ```

- **Line**: 37
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_type = "Minor Sprain" # Placeholder, could be more specific
      ```

- **Line**: 38
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_status = InjuryStatus.QUESTIONABLE
      ```

- **Line**: 41
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_type = "Muscle Tear"
      ```

- **Line**: 42
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_status = InjuryStatus.OUT
      ```

- **Line**: 45
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_type = "Major Fracture" # or Ligament Tear
      ```

- **Line**: 46
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_status = InjuryStatus.IR
      ```

- **Line**: 48
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_severity = severity
      ```

- **Line**: 52
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.weeks_to_recovery = weeks
      ```

- **Line**: 56
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_recurrence_risk = severity * 0.02 # 2% per severity point initially (e.g. 20% for severity 10)
      ```

- **Line**: 111
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.weeks_to_recovery += added_weeks
      ```

- **Line**: 113
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_recurrence_risk += 0.05
      ```

- **Line**: 119
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.weeks_to_recovery -= 1
      ```

- **Line**: 132
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return roll < (player.injury_recurrence_risk * risk_modifier)
      ```

- **Line**: 141
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.ACTIVE
      ```

- **Line**: 142
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_type = None
      ```

- **Line**: 143
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_severity = 0
      ```

- **Line**: 144
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_recurrence_risk = 0.0
      ```

- **Line**: 177
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 player.injury_resistance = max(0, player.injury_resistance - 5)
      ```

- **Line**: 287
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.injury_severity = min(10, severity + increase)
      ```

- **Line**: 322
  - **Error**: Incompatible types in assignment (expression has type "None", variable has type "dict[str, int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -     performance_penalties: Dict[str, int] = None
      ```

- **Line**: 326
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             self.performance_penalties = {}
      ```

- **Line**: 336
  - **Error**: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     rng: DeterministicRNG = None
      ```

- **Line**: 479
  - **Error**: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     rng: DeterministicRNG = None
      ```

- **Line**: 519
  - **Error**: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     rng: DeterministicRNG = None
      ```

- **Line**: 536
  - **Error**: Argument "seed" to "InjurySystem" has incompatible type "int | None"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "seed" to "InjurySystem" has incompatible type "int | None"; expected "int"
      -     injury_system = InjurySystem(seed=rng.randint(0, 1000000) if rng else None)
      ```

- **Line**: 591
  - **Error**: Incompatible default for argument "rng" (default has type "None", argument has type "DeterministicRNG")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     rng: DeterministicRNG = None
      ```

- **Line**: 626
  - **Error**: Incompatible default for argument "injury_system" (default has type "None", argument has type "InjurySystem")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      - def apply_injury_event_to_player(player: Player, event: InjuryEvent, injury_system: InjurySystem = None):
      ```

- **Line**: 635
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -     player.injury_severity = event.severity
      ```

- **Line**: 636
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -     player.injury_type = event.injury_type
      ```

- **Line**: 637
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -     player.weeks_to_recovery = event.weeks_to_recovery
      ```

- **Line**: 641
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.QUESTIONABLE
      ```

- **Line**: 643
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.QUESTIONABLE
      ```

- **Line**: 645
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.OUT
      ```

- **Line**: 647
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.injury_status = InjuryStatus.IR
      ```

- **Line**: 650
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -     player.injury_recurrence_risk = event.severity * 0.02
      ```


## File: app/rpg/narrative.py
- **Line**: 37
  - **Error**: Incompatible return value type (got "None", expected "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "None", expected "dict[Any, Any]")
      -         return None
      ```


## File: app/rpg/traits.py
- **Line**: 54
  - **Error**: Incompatible return value type (got "Collection[str]", expected "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Collection[str]", expected "dict[Any, Any]")
      -         return TraitSystem.TRAITS.get(trait_name, {}).get("effect", {})
      ```


## File: app/scripts/seed_coaches.py
- **Line**: 66
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     existing.first_name = coach_data.first_name
      ```

- **Line**: 67
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     existing.last_name = coach_data.last_name
      ```

- **Line**: 69
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         existing.playbook_offense = off_scheme
      ```

- **Line**: 71
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         existing.playbook_defense = def_scheme
      ```

- **Line**: 73
  - **Error**: Incompatible types in assignment (expression has type "dict[str, int]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         existing.philosophy = philosophy_dict
      ```


## File: app/scripts/seed_teams.py
- **Line**: 42
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 team.logo_url = logo_url
      ```

- **Line**: 43
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 team.primary_color = data.colors.primary_hex
      ```

- **Line**: 44
  - **Error**: Incompatible types in assignment (expression has type "str", variable has type "Column[str]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 team.secondary_color = data.colors.secondary_hex
      ```


## File: app/services/ability_service.py
- **Line**: 143
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.xp -= ability_def.xp_cost
      ```

- **Line**: 148
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.abilities = abilities_dict
      ```

- **Line**: 165
  - **Error**: "type[ErrorCategory]" has no attribute "SERVICE_ERROR"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "type[ErrorCategory]" has no attribute "SERVICE_ERROR"
      -             log_error(logger, ErrorCategory.SERVICE_ERROR, "Failed to unlock ability", exc_info=e)
      ```

- **Line**: 184
  - **Error**: Returning Any from function declared to return "bool"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "bool"
      -         return abilities_dict.get(ability_key, False)
      ```


## File: app/services/ai/__init__.py
- **Line**: 7
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      - from app.services.ai.gemini_client import GeminiClient, get_gemini_client  # type: ignore[import-not-found]
      ```


## File: app/services/ai/gemini_client.py
- **Line**: 67
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      -             from google.genai.types import HttpOptions  # type: ignore[import-not-found]
      ```

- **Line**: 113
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      -             from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]
      ```

- **Line**: 115
  - **Error**: Item "None" of "Any | None" has no attribute "models"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Any | None" has no attribute "models"
      -             response = self._client.models.generate_content(
      ```

- **Line**: 123
  - **Error**: Returning Any from function declared to return "str | None"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "str | None"
      -             return response.text
      ```

- **Line**: 154
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      -             from google.genai.types import GenerateContentConfig  # type: ignore[import-not-found]
      ```

- **Line**: 159
  - **Error**: Item "None" of "Any | None" has no attribute "models"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Any | None" has no attribute "models"
      -             response = self._client.models.generate_content(
      ```

- **Line**: 205
  - **Error**: Incompatible types in assignment (expression has type "str | None", variable has type "T | None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     result = await self.generate_text(prompt, temperature)
      ```


## File: app/services/ai/scouting_ai.py
- **Line**: 16
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      - from app.schemas.scouting import ScoutingReportAI, PlayerBackstory  # type: ignore[import-not-found]
      ```

- **Line**: 17
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      - from app.services.ai.gemini_client import get_gemini_client  # type: ignore[import-not-found]
      ```

- **Line**: 89
  - **Error**: Returning Any from function declared to return "ScoutingReportAI"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "ScoutingReportAI"
      -                 return result
      ```

- **Line**: 288
  - **Error**: Returning Any from function declared to return "PlayerBackstory"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "PlayerBackstory"
      -                 return result
      ```


## File: app/services/ai_research_service.py
- **Line**: 141
  - **Error**: Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
      -                     summary=research["summary"],
      ```

- **Line**: 142
  - **Error**: Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
      -                     recommended_approach=research["approach"],
      ```

- **Line**: 143
  - **Error**: Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
      -                     code_examples=research.get("examples", []),
      ```

- **Line**: 144
  - **Error**: Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"
      -                     complexity=research["complexity"],
      ```

- **Line**: 145
  - **Error**: Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
      -                     sources=research.get("sources", []),
      ```

- **Line**: 151
  - **Error**: Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
      -             summary=self.DEFAULT_RESEARCH["summary"],
      ```

- **Line**: 152
  - **Error**: Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"
      -             recommended_approach=self.DEFAULT_RESEARCH["approach"],
      ```

- **Line**: 153
  - **Error**: Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
      -             code_examples=self.DEFAULT_RESEARCH["examples"],
      ```

- **Line**: 154
  - **Error**: Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"
      -             complexity=self.DEFAULT_RESEARCH["complexity"],
      ```

- **Line**: 155
  - **Error**: Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"
      -             sources=self.DEFAULT_RESEARCH["sources"],
      ```


## File: app/services/broadcasting_service.py
- **Line**: 194
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, style: BroadcastStyle = BroadcastStyle.ESPN, seed: int = None):
      ```


## File: app/services/data_sync_service.py
- **Line**: 31
  - **Error**: Unused "type: ignore" comment
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unused "type: ignore" comment
      -     import nflreadpy  # type: ignore[import-not-found]
      ```

- **Line**: 31
  - **Error**: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker
      -     import nflreadpy  # type: ignore[import-not-found]
      ```

- **Line**: 321
  - **Error**: Unsupported target for indexed assignment ("object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported target for indexed assignment ("object")
      -             report["sources"][source.value] = {
      ```


## File: app/services/database/optimizer.py
- **Line**: 81
  - **Error**: Incompatible default for argument "pattern" (default has type "None", argument has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def invalidate(self, pattern: str = None):
      ```

- **Line**: 88
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             self.cache.clear()
      ```


## File: app/services/depth_chart_service.py
- **Line**: 16
  - **Error**: Need type annotation for "chart" (hint: "chart: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         chart = {}
      +         chart: dict = {}
      ```


## File: app/services/draft_assistant.py
- **Line**: 70
  - **Error**: No overload variant of "select" matches argument types "InstrumentedAttribute[int]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[int]", overloaded function, overloaded function, overloaded function
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "select" matches argument types "InstrumentedAttribute[int]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[str]", "InstrumentedAttribute[int]", overloaded function, overloaded function, overloaded function
      -         players_stmt = select(
      ```


## File: app/services/elo_service.py
- **Line**: 84
  - **Error**: Incompatible default for argument "k_factor" (default has type "None", argument has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -         k_factor: float = None,
      ```

- **Line**: 152
  - **Error**: Argument "winner_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "winner_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"
      -             winner_elo=winner.elo_rating or 1500.0,
      ```

- **Line**: 153
  - **Error**: Argument "loser_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "loser_elo" to "update_ratings" of "EloService" has incompatible type "Column[float] | float"; expected "float"
      -             loser_elo=loser.elo_rating or 1500.0,
      ```

- **Line**: 159
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         winner.elo_rating = new_winner_elo
      ```

- **Line**: 160
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         loser.elo_rating = new_loser_elo
      ```


## File: app/services/empire/gm_ai.py
- **Line**: 254
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -             return max(0, base_value)
      ```

- **Line**: 289
  - **Error**: Returning Any from function declared to return "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "float"
      -             return base
      ```


## File: app/services/enhanced_chemistry_service.py
- **Line**: 261
  - **Error**: Need type annotation for "games_data" (hint: "games_data: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         games_data = {}
      +         games_data: dict = {}
      ```

- **Line**: 357
  - **Error**: Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         match_context.home_ol_chemistry = home_chemistry
      ```

- **Line**: 358
  - **Error**: Incompatible types in assignment (expression has type "ChemistryMetadata | None", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         match_context.away_ol_chemistry = away_chemistry
      ```

- **Line**: 400
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                         player.active_modifiers = {}
      ```

- **Line**: 404
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                         player.active_modifiers[attr] = (
      ```

- **Line**: 405
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                             player.active_modifiers.get(attr, 0) + bonus
      ```

- **Line**: 410
  - **Error**: "Player" has no attribute "chemistry_effects"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "chemistry_effects"
      -                         player.chemistry_effects = {}
      ```

- **Line**: 412
  - **Error**: "Player" has no attribute "chemistry_effects"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "chemistry_effects"
      -                     player.chemistry_effects = chemistry.advanced_effects
      ```


## File: app/services/gm_agent.py
- **Line**: 14
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: Session, team_id: int, seed: int = None):
      ```

- **Line**: 87
  - **Error**: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -             offered_value = self._calculate_package_value(offered_players, offered_picks, is_acquiring=True)
      ```

- **Line**: 88
  - **Error**: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "_calculate_package_value" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -             requested_value = self._calculate_package_value(requested_players, requested_picks, is_acquiring=False)
      ```

- **Line**: 94
  - **Error**: Argument 2 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -             modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)
      ```

- **Line**: 94
  - **Error**: Argument 3 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 3 to "_apply_gm_traits" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -             modified_score = self._apply_gm_traits(raw_score, offered_players, requested_players, offered_picks, requested_picks)
      ```

- **Line**: 98
  - **Error**: Argument 1 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -                 llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
      ```

- **Line**: 98
  - **Error**: Argument 2 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_get_llm_trade_opinion" of "GMAgent" has incompatible type "list[Player | None]"; expected "list[Player]"
      -                 llm_adjustment = await self._get_llm_trade_opinion(offered_players, requested_players)
      ```

- **Line**: 107
  - **Error**: Unsupported operand types for - ("object" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("object" and "int")
      -             acceptance_threshold = 0 - (self.gm_traits["aggression"] - 50) * 0.5
      ```

- **Line**: 133
  - **Error**: Incompatible default for argument "target_position" (default has type "None", argument has type "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def generate_trade_proposal(self, target_position: str = None) -> Dict[str, Any]:
      ```

- **Line**: 182
  - **Error**: Unsupported operand types for / ("object" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("object" and "int")
      -         skill_factor = 1.2 - (negotiation_skill / 250)
      ```

- **Line**: 355
  - **Error**: Item "None" of "Team | None" has no attribute "players"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Team | None" has no attribute "players"
      -         players_at_pos = [p for p in self.team.players if p.position == position]
      ```


## File: app/services/issue_logger.py
- **Line**: 42
  - **Error**: Item "None" of "datetime | None" has no attribute "strftime"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "datetime | None" has no attribute "strftime"
      -     timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
      ```

- **Line**: 109
  - **Error**: Library stubs not installed for "aiofiles"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Library stubs not installed for "aiofiles"
      -             import aiofiles
      ```


## File: app/services/medical_service.py
- **Line**: 54
  - **Error**: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
      -             health.head_health = max(0, health.head_health - damage)
      ```

- **Line**: 54
  - **Error**: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
      -             health.head_health = max(0, health.head_health - damage)
      ```

- **Line**: 56
  - **Error**: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
      -             health.torso_health = max(0, health.torso_health - damage)
      ```

- **Line**: 56
  - **Error**: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
      -             health.torso_health = max(0, health.torso_health - damage)
      ```

- **Line**: 58
  - **Error**: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
      -             health.right_arm_health = max(0, health.right_arm_health - damage)
      ```

- **Line**: 58
  - **Error**: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
      -             health.right_arm_health = max(0, health.right_arm_health - damage)
      ```

- **Line**: 60
  - **Error**: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "max" has incompatible type "int"; expected "Column[float]"
      -             health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty
      ```

- **Line**: 60
  - **Error**: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "max" has incompatible type "ColumnElement[float]"; expected "Column[float]"
      -             health.right_leg_health = max(0, health.right_leg_health - damage * 1.5) # Legs take more penalty
      ```


## File: app/services/nflverse_service.py
- **Line**: 12
  - **Error**: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Skipping analyzing "nflreadpy": module is installed, but missing library stubs or py.typed marker
      -     import nflreadpy as nfl
      ```

- **Line**: 120
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -         return df
      ```

- **Line**: 137
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -             return df
      ```

- **Line**: 157
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -             return df
      ```

- **Line**: 177
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -             return df
      ```

- **Line**: 197
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -             return df
      ```

- **Line**: 217
  - **Error**: Returning Any from function declared to return "DataFrame"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Returning Any from function declared to return "DataFrame"
      -             return df
      ```


## File: app/services/offseason_service.py
- **Line**: 19
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: Session, seed: int = None):
      ```

- **Line**: 31
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season.status = SeasonStatus.OFF_SEASON
      ```

- **Line**: 172
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.contract_years -= 1
      ```

- **Line**: 175
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 player.contract_years = 0
      ```

- **Line**: 205
  - **Error**: "TeamStanding" has no attribute "win_pct"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "TeamStanding" has no attribute "win_pct"
      -         standings.sort(key=lambda x: (x.win_pct, x.wins, x.point_differential))
      ```

- **Line**: 208
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[PlayoffMatchup]]", variable has type "Select[tuple[Team]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         stmt = select(PlayoffMatchup).where(
      ```

- **Line**: 216
  - **Error**: "Team" has no attribute "winner_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "winner_id"
      -         if sb_matchup and sb_matchup.winner_id:
      ```

- **Line**: 217
  - **Error**: "Team" has no attribute "winner_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "winner_id"
      -             winner_id = sb_matchup.winner_id
      ```

- **Line**: 218
  - **Error**: "Team" has no attribute "home_team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "home_team_id"
      -             loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
      ```

- **Line**: 218
  - **Error**: "Team" has no attribute "winner_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "winner_id"
      -             loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
      ```

- **Line**: 218
  - **Error**: "Team" has no attribute "away_team_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "away_team_id"
      -             loser_id = sb_matchup.home_team_id if sb_matchup.winner_id == sb_matchup.away_team_id else sb_matchup.away_team_id
      ```

- **Line**: 247
  - **Error**: Need type annotation for "position_counts" (hint: "position_counts: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         position_counts = {}
      +         position_counts: dict = {}
      ```

- **Line**: 279
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
      -             Player.is_rookie == True,
      ```

- **Line**: 279
  - **Error**: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -             Player.is_rookie == True,
      ```

- **Line**: 314
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         pick.player_id = player.id
      ```

- **Line**: 316
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.contract_years = 4
      ```

- **Line**: 317
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.is_rookie = False
      ```

- **Line**: 328
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         pick.team_id = target_team_id
      ```

- **Line**: 341
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[True]")
      -             Player.is_rookie == True,
      ```

- **Line**: 341
  - **Error**: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -             Player.is_rookie == True,
      ```

- **Line**: 350
  - **Error**: Argument 1 to "_get_team_needs" of "OffseasonService" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "_get_team_needs" of "OffseasonService" has incompatible type "Column[int]"; expected "int"
      -         team_needs = self._get_team_needs(pick.team_id)
      ```

- **Line**: 380
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         pick.player_id = player.id
      ```

- **Line**: 382
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.contract_years = 4
      ```

- **Line**: 383
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -         player.is_rookie = False
      ```

- **Line**: 388
  - **Error**: Argument "round" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "round" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
      -             round=pick.round,
      ```

- **Line**: 389
  - **Error**: Argument "pick_number" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "pick_number" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
      -             pick_number=pick.pick_number,
      ```

- **Line**: 390
  - **Error**: Argument "team_id" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "team_id" to "DraftPickSummary" has incompatible type "Column[int]"; expected "int"
      -             team_id=pick.team_id,
      ```

- **Line**: 431
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                     player.contract_years = 1
      ```

- **Line**: 443
  - **Error**: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[False]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Non-overlapping equality check (left operand type: overloaded function, right operand type: "Literal[False]")
      -             Player.is_retired == False,
      ```

- **Line**: 443
  - **Error**: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "where" of "Select" has incompatible type "bool"; expected "ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | Callable[[], ColumnElement[bool]] | LambdaElement"
      -             Player.is_retired == False,
      ```

- **Line**: 467
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 player.is_retired = True
      ```

- **Line**: 468
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -                 player.retirement_year = season.year
      ```

- **Line**: 473
  - **Error**: Argument 2 to "_check_hall_of_fame" of "OffseasonService" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_check_hall_of_fame" of "OffseasonService" has incompatible type "Column[int]"; expected "int"
      -                 self._check_hall_of_fame(player, season.year)
      ```

- **Line**: 511
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "games_played"
      -             "games_played": stats.games_played or 0,
      ```

- **Line**: 512
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_yards"
      -             "pass_yards": stats.pass_yards or 0,
      ```

- **Line**: 513
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "pass_tds"
      -             "pass_tds": stats.pass_tds or 0,
      ```

- **Line**: 514
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_yards"
      -             "rush_yards": stats.rush_yards or 0,
      ```

- **Line**: 515
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rush_tds"
      -             "rush_tds": stats.rush_tds or 0,
      ```

- **Line**: 516
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_yards"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_yards"
      -             "rec_yards": stats.rec_yards or 0,
      ```

- **Line**: 517
  - **Error**: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_tds"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "Row[tuple[int, int, int, int, int, int, int]] | None" has no attribute "rec_tds"
      -             "rec_tds": stats.rec_tds or 0
      ```


## File: app/services/playbook/clock_management.py
- **Line**: 240
  - **Error**: "GameSituation" has no attribute "yards_to_goal"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "GameSituation" has no attribute "yards_to_goal"
      -             if situation.yards_to_goal <= 35 and situation.time_remaining < 25:
      ```


## File: app/services/playbook/gameplan_service.py
- **Line**: 50
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         gameplan.prep_bonus_offense = off_bonus
      ```

- **Line**: 51
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "Column[float]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         gameplan.prep_bonus_defense = def_bonus
      ```

- **Line**: 66
  - **Error**: Incompatible types in assignment (expression has type "list[Any]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             tree.unlocked_skills = current_skills
      ```


## File: app/services/player_development_service.py
- **Line**: 19
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: AsyncSession, seed: int = None):
      ```

- **Line**: 58
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         team.medical_rating = new_rating
      ```

- **Line**: 59
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         team.training_staff_quality = new_rating
      ```

- **Line**: 78
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 xp_gain *= 1.25
      +                 xp_gain *= 1.25  # Wrap expression in int()
      ```

- **Line**: 80
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 xp_gain *= 1.5
      +                 xp_gain *= 1.5  # Wrap expression in int()
      ```

- **Line**: 82
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 xp_gain *= 2.0
      +                 xp_gain *= 2.0  # Wrap expression in int()
      ```

- **Line**: 85
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -             xp_gain *= (1.0 + coach_bonus)
      +             xp_gain *= (1.0 + coach_bonus)  # Wrap expression in int()
      ```

- **Line**: 89
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 xp_gain *= 0.8
      +                 xp_gain *= 0.8  # Wrap expression in int()
      ```

- **Line**: 91
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 xp_gain *= 1.2
      +                 xp_gain *= 1.2  # Wrap expression in int()
      ```

- **Line**: 118
  - **Error**: Cannot assign to a method
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot assign to a method
      -             player.skill_points -= 1
      ```

- **Line**: 147
  - **Error**: Argument "medical_rating" to "process_recovery_step" of "InjurySystem" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "medical_rating" to "process_recovery_step" of "InjurySystem" has incompatible type "Column[int]"; expected "int"
      -             self.injury_system.process_recovery_step(player, medical_rating=team.medical_rating)
      ```

- **Line**: 154
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[float | Decimal]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             win_pct = team.wins / (team.wins + team.losses)
      ```

- **Line**: 188
  - **Error**: Argument 1 to "calculate_injury_risk_multiplier" of "InjurySystem" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "calculate_injury_risk_multiplier" of "InjurySystem" has incompatible type "Column[int]"; expected "int"
      -         return self.injury_system.calculate_injury_risk_multiplier(team.training_staff_quality)
      ```


## File: app/services/playoff_service.py
- **Line**: 66
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season.status = SeasonStatus.POST_SEASON
      ```

- **Line**: 67
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         season.current_week = 19
      ```

- **Line**: 93
  - **Error**: Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         divisions = {}
      +         divisions: dict = {}
      ```

- **Line**: 126
  - **Error**: Incompatible return value type (got "list[Team | None]", expected "list[Team]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "list[Team | None]", expected "list[Team]")
      -         return ordered_teams
      ```

- **Line**: 282
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = 20
      ```

- **Line**: 287
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = 21
      ```

- **Line**: 291
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = 22
      ```

- **Line**: 295
  - **Error**: Incompatible types in assignment (expression has type "SeasonStatus", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.status = SeasonStatus.OFF_SEASON
      ```

- **Line**: 333
  - **Error**: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
      -         remaining_teams.sort(key=lambda x: x["seed"])
      ```

- **Line**: 333
  - **Error**: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
      -         remaining_teams.sort(key=lambda x: x["seed"])
      ```

- **Line**: 373
  - **Error**: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "key" to "sort" of "list" has incompatible type "Callable[[dict[str, Column[int] | Team | None]], Column[int] | Team | None]"; expected "Callable[[dict[str, Column[int] | Team | None]], SupportsDunderLT[Any] | SupportsDunderGT[Any]]"
      -         winners.sort(key=lambda x: x["seed"])
      ```

- **Line**: 373
  - **Error**: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Column[int] | Team | None", expected "SupportsDunderLT[Any] | SupportsDunderGT[Any]")
      -         winners.sort(key=lambda x: x["seed"])
      ```

- **Line**: 404
  - **Error**: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"
      -         afc_winner = self.db.execute(select(Team).where(Team.id == afc_conf.winner_id)).scalar_one_or_none()
      ```

- **Line**: 405
  - **Error**: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "None" of "PlayoffMatchup | None" has no attribute "winner_id"
      -         nfc_winner = self.db.execute(select(Team).where(Team.id == nfc_conf.winner_id)).scalar_one_or_none()
      ```


## File: app/services/pre_game_service.py
- **Line**: 18
  - **Error**: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "TraitService" has incompatible type "AsyncSession"; expected "Session"
      -         self.trait_service = TraitService(db)  # NEW: Trait service
      ```

- **Line**: 58
  - **Error**: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible types in "await" (actual type "list[TraitDefinition]", expected type "Awaitable[Any]")
      -             trait_defs = await self.trait_service.get_player_traits(player_id)
      ```

- **Line**: 58
  - **Error**: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Missing positional argument "player_id" in call to "get_player_traits" of "TraitService"
      -             trait_defs = await self.trait_service.get_player_traits(player_id)
      ```

- **Line**: 58
  - **Error**: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "get_player_traits" of "TraitService" has incompatible type "int"; expected "Session"
      -             trait_defs = await self.trait_service.get_player_traits(player_id)
      ```

- **Line**: 65
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -                 player.active_traits = []
      ```

- **Line**: 67
  - **Error**: "Player" has no attribute "trait_effects"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "trait_effects"
      -                 player.trait_effects = {}
      ```

- **Line**: 71
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -                 player.active_traits.append(trait_def.name)
      ```

- **Line**: 77
  - **Error**: "Player" has no attribute "trait_effects"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "trait_effects"
      -                         player.trait_effects[effect_key] = effect_value
      ```

- **Line**: 101
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                     player.active_modifiers = {}
      ```

- **Line**: 104
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                 player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
      ```

- **Line**: 113
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                     player.active_modifiers = {}
      ```

- **Line**: 116
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                 player.active_modifiers["play_recognition"] = player.active_modifiers.get("play_recognition", 0) + 5
      ```

- **Line**: 156
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Game]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stmt = select(PlayerGameStart).filter(
      ```

- **Line**: 165
  - **Error**: "Game" has no attribute "position"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Game" has no attribute "position"
      -             game_starters = {s.position: s.player_id for s in starts}
      ```

- **Line**: 165
  - **Error**: "Game" has no attribute "player_id"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Game" has no attribute "player_id"
      -             game_starters = {s.position: s.player_id for s in starts}
      ```

- **Line**: 188
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                         player.active_modifiers = {}
      ```

- **Line**: 192
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                     player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
      ```

- **Line**: 193
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                     player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
      ```

- **Line**: 194
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -                     player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
      ```

- **Line**: 230
  - **Error**: Incompatible types in assignment (expression has type "Select[tuple[PlayerGameStart]]", variable has type "Select[tuple[Player]]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 stmt = select(PlayerGameStart).filter(
      ```


## File: app/services/rating_calculator.py
- **Line**: 297
  - **Error**: Incompatible types in assignment (expression has type "Any | float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 attr_value = max(40, min(99, 100 - (threshold / 2)))
      ```


## File: app/services/ratings_generator.py
- **Line**: 42
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         return 50  # Default average
      ```

- **Line**: 54
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         return 50
      ```


## File: app/services/rookie_generator.py
- **Line**: 18
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: Session, seed: int = None):
      ```

- **Line**: 57
  - **Error**: Argument 2 to "_create_rookie" of "RookieGenerator" has incompatible type "Any | None"; expected "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 2 to "_create_rookie" of "RookieGenerator" has incompatible type "Any | None"; expected "dict[Any, Any]"
      -             player = self._create_rookie(selected_pos, league_avgs.get(selected_pos.value if hasattr(selected_pos, 'value') else selected_pos))
      ```

- **Line**: 64
  - **Error**: Incompatible default for argument "stats_context" (default has type "None", argument has type "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def _create_rookie(self, position: Position, stats_context: dict = None) -> Player:
      ```


## File: app/services/salary_cap_service.py
- **Line**: 89
  - **Error**: "Team" has no attribute "salary_cap_total"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "salary_cap_total"
      -             "total_cap": team.salary_cap_total,
      ```

- **Line**: 92
  - **Error**: "Team" has no attribute "salary_cap_total"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Team" has no attribute "salary_cap_total"
      -             "cap_percentage": round((used_cap / team.salary_cap_total) * 100, 1) if team.salary_cap_total > 0 else 0,
      ```


## File: app/services/schedule_generator.py
- **Line**: 26
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: Session, seed: int = None):
      ```

- **Line**: 34
  - **Error**: Incompatible default for argument "start_date" (default has type "None", argument has type "datetime")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -         start_date: datetime = None,
      ```

- **Line**: 50
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             start_date = self._get_next_sunday()
      ```

- **Line**: 82
  - **Error**: Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         divisions = {}
      +         divisions: dict = {}
      ```

- **Line**: 166
  - **Error**: Need type annotation for "matchups" (hint: "matchups: list[<type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         matchups = []
      +         matchups: list = []
      ```


## File: app/services/scouting/draft_board.py
- **Line**: 59
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 score *= 1.15 # 15% boost for need
      +                 score *= 1.15 # 15% boost for need  # Wrap expression in int()
      ```


## File: app/services/scouting/scout.py
- **Line**: 194
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -         return False
      ```


## File: app/services/society/social_graph.py
- **Line**: 149
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                     positive_rels += r.strength
      +                     positive_rels += r.strength  # Wrap expression in int()
      ```

- **Line**: 151
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                     negative_rels += r.strength
      +                     negative_rels += r.strength  # Wrap expression in int()
      ```


## File: app/services/standings_calculator.py
- **Line**: 67
  - **Error**: Need type annotation for "team_stats"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         team_stats = {
      +         team_stats = {
      ```

- **Line**: 99
  - **Error**: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[home_id]['opponents'].append(away_id)
      ```

- **Line**: 99
  - **Error**: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[home_id]['opponents'].append(away_id)
      ```

- **Line**: 99
  - **Error**: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[home_id]['opponents'].append(away_id)
      ```

- **Line**: 101
  - **Error**: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "dict[Any, Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[away_id]['opponents'].append(home_id)
      ```

- **Line**: 101
  - **Error**: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[away_id]['opponents'].append(home_id)
      ```

- **Line**: 101
  - **Error**: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "append"
      -                 team_stats[away_id]['opponents'].append(home_id)
      ```

- **Line**: 111
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 home_team['points_for'] += game.home_score
      ```

- **Line**: 112
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 home_team['points_against'] += game.away_score
      ```

- **Line**: 113
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 away_team['points_for'] += game.away_score
      ```

- **Line**: 114
  - **Error**: Incompatible types in assignment (expression has type "ColumnElement[int] | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                 away_team['points_against'] += game.home_score
      ```

- **Line**: 119
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     home_team['wins'] += 1
      ```

- **Line**: 119
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     home_team['wins'] += 1
      ```

- **Line**: 119
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     home_team['wins'] += 1
      ```

- **Line**: 119
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     home_team['wins'] += 1
      ```

- **Line**: 120
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     away_team['losses'] += 1
      ```

- **Line**: 120
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     away_team['losses'] += 1
      ```

- **Line**: 120
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     away_team['losses'] += 1
      ```

- **Line**: 120
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     away_team['losses'] += 1
      ```

- **Line**: 123
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     home_team['losses'] += 1
      ```

- **Line**: 123
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     home_team['losses'] += 1
      ```

- **Line**: 123
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     home_team['losses'] += 1
      ```

- **Line**: 123
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     home_team['losses'] += 1
      ```

- **Line**: 124
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     away_team['wins'] += 1
      ```

- **Line**: 124
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     away_team['wins'] += 1
      ```

- **Line**: 124
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     away_team['wins'] += 1
      ```

- **Line**: 124
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     away_team['wins'] += 1
      ```

- **Line**: 127
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     home_team['ties'] += 1
      ```

- **Line**: 127
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     home_team['ties'] += 1
      ```

- **Line**: 127
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     home_team['ties'] += 1
      ```

- **Line**: 127
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     home_team['ties'] += 1
      ```

- **Line**: 128
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                     away_team['ties'] += 1
      ```

- **Line**: 128
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                     away_team['ties'] += 1
      ```

- **Line**: 128
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     away_team['ties'] += 1
      ```

- **Line**: 128
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                     away_team['ties'] += 1
      ```

- **Line**: 132
  - **Error**: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
      -                     home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
      ```

- **Line**: 132
  - **Error**: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
      ```

- **Line**: 132
  - **Error**: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
      ```

- **Line**: 132
  - **Error**: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     home_team['head_to_head'][away_id] = home_team['head_to_head'].get(away_id, 0) + 1
      ```

- **Line**: 134
  - **Error**: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported target for indexed assignment ("dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
      -                     away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
      ```

- **Line**: 134
  - **Error**: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "list[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
      ```

- **Line**: 134
  - **Error**: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "str" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
      ```

- **Line**: 134
  - **Error**: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "get"
      -                     away_team['head_to_head'][home_id] = away_team['head_to_head'].get(home_id, 0) + 1
      ```

- **Line**: 139
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['division_wins'] += 1
      ```

- **Line**: 139
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['division_wins'] += 1
      ```

- **Line**: 139
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['division_wins'] += 1
      ```

- **Line**: 139
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['division_wins'] += 1
      ```

- **Line**: 140
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['division_losses'] += 1
      ```

- **Line**: 140
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['division_losses'] += 1
      ```

- **Line**: 140
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['division_losses'] += 1
      ```

- **Line**: 140
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['division_losses'] += 1
      ```

- **Line**: 142
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['division_losses'] += 1
      ```

- **Line**: 142
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['division_losses'] += 1
      ```

- **Line**: 142
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['division_losses'] += 1
      ```

- **Line**: 142
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['division_losses'] += 1
      ```

- **Line**: 143
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['division_wins'] += 1
      ```

- **Line**: 143
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['division_wins'] += 1
      ```

- **Line**: 143
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['division_wins'] += 1
      ```

- **Line**: 143
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['division_wins'] += 1
      ```

- **Line**: 145
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['division_ties'] += 1
      ```

- **Line**: 145
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['division_ties'] += 1
      ```

- **Line**: 145
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['division_ties'] += 1
      ```

- **Line**: 145
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['division_ties'] += 1
      ```

- **Line**: 146
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['division_ties'] += 1
      ```

- **Line**: 146
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['division_ties'] += 1
      ```

- **Line**: 146
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['division_ties'] += 1
      ```

- **Line**: 146
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['division_ties'] += 1
      ```

- **Line**: 151
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['conference_wins'] += 1
      ```

- **Line**: 151
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['conference_wins'] += 1
      ```

- **Line**: 151
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['conference_wins'] += 1
      ```

- **Line**: 151
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['conference_wins'] += 1
      ```

- **Line**: 152
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['conference_losses'] += 1
      ```

- **Line**: 152
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['conference_losses'] += 1
      ```

- **Line**: 152
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['conference_losses'] += 1
      ```

- **Line**: 152
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['conference_losses'] += 1
      ```

- **Line**: 154
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['conference_losses'] += 1
      ```

- **Line**: 154
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['conference_losses'] += 1
      ```

- **Line**: 154
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['conference_losses'] += 1
      ```

- **Line**: 154
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['conference_losses'] += 1
      ```

- **Line**: 155
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['conference_wins'] += 1
      ```

- **Line**: 155
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['conference_wins'] += 1
      ```

- **Line**: 155
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['conference_wins'] += 1
      ```

- **Line**: 155
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['conference_wins'] += 1
      ```

- **Line**: 157
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         home_team['conference_ties'] += 1
      ```

- **Line**: 157
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         home_team['conference_ties'] += 1
      ```

- **Line**: 157
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         home_team['conference_ties'] += 1
      ```

- **Line**: 157
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         home_team['conference_ties'] += 1
      ```

- **Line**: 158
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "int")
      -                         away_team['conference_ties'] += 1
      ```

- **Line**: 158
  - **Error**: No overload variant of "__add__" of "list" matches argument type "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "int"
      -                         away_team['conference_ties'] += 1
      ```

- **Line**: 158
  - **Error**: Incompatible types in assignment (expression has type "int | Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                         away_team['conference_ties'] += 1
      ```

- **Line**: 158
  - **Error**: Unsupported operand types for + ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "int")
      -                         away_team['conference_ties'] += 1
      ```

- **Line**: 162
  - **Error**: Unsupported left operand type for + ("dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for + ("dict[Any, Any]")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: No overload variant of "__add__" of "list" matches argument type "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "str"
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("str" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "dict[Any, Any]")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("str" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "list[Any]")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "dict[Any, Any]")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "list[Any]")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for + ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "str")
      -             total_games = stats['wins'] + stats['losses'] + stats['ties']
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for / ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "list[Any]")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for / ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "str")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for * ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "dict[Any, Any]")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for * ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "list[Any]")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for * ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "str")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for > ("list[Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("list[Any]" and "int")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 163
  - **Error**: Unsupported operand types for > ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("str" and "int")
      -             stats['win_percentage'] = (stats['wins'] + 0.5 * stats['ties']) / total_games if total_games > 0 else 0.0
      ```

- **Line**: 164
  - **Error**: Unsupported left operand type for - ("dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for - ("dict[Any, Any]")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("dict[Any, Any]" and "float")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported left operand type for - ("list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for - ("list[Any]")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("list[Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("list[Any]" and "float")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported left operand type for - ("str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for - ("str")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("str" and "float")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("float" and "dict[Any, Any]")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("float" and "list[Any]")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Unsupported operand types for - ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for - ("float" and "str")
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 164
  - **Error**: Incompatible types in assignment (expression has type "Any | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float] | float", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stats['point_differential'] = stats['points_for'] - stats['points_against']
      ```

- **Line**: 165
  - **Error**: Argument 1 to "round" has incompatible type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float"; expected "_SupportsRound2[Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 1 to "round" has incompatible type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float"; expected "_SupportsRound2[Any]"
      -             stats['win_percentage'] = round(stats['win_percentage'], 3)
      ```

- **Line**: 168
  - **Error**: Unsupported left operand type for + ("dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for + ("dict[Any, Any]")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: No overload variant of "__add__" of "list" matches argument type "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "str"
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("str" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "dict[Any, Any]")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("str" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "list[Any]")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "dict[Any, Any]")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "list[Any]")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 168
  - **Error**: Unsupported operand types for + ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "str")
      -             div_games = stats['division_wins'] + stats['division_losses'] + stats['division_ties']
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for / ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "list[Any]")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for / ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "str")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for * ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "dict[Any, Any]")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for * ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "list[Any]")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for * ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "str")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for > ("list[Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("list[Any]" and "int")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for > ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("str" and "int")
      -             stats['division_win_pct'] = (stats['division_wins'] + 0.5 * stats['division_ties']) / div_games if div_games > 0 else 0.0
      ```

- **Line**: 172
  - **Error**: Unsupported left operand type for + ("dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported left operand type for + ("dict[Any, Any]")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "dict[Any, Any]"
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: No overload variant of "__add__" of "list" matches argument type "str"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "str"
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("str" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "dict[Any, Any]")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("str" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "list[Any]")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "dict[Any, Any]")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "list[Any]")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 172
  - **Error**: Unsupported operand types for + ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "str")
      -             conf_games = stats['conference_wins'] + stats['conference_losses'] + stats['conference_ties']
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for / ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "list[Any]")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for / ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for / ("float" and "str")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Incompatible types in assignment (expression has type "Any | ColumnElement[float | Decimal] | float | ColumnElement[str] | ColumnElement[float]", target has type "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for + ("dict[Any, Any]" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("dict[Any, Any]" and "float")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: No overload variant of "__add__" of "list" matches argument type "float"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: No overload variant of "__add__" of "list" matches argument type "float"
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for + ("str" and "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("str" and "float")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for * ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "dict[Any, Any]")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for * ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "list[Any]")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for * ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for * ("float" and "str")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for > ("list[Any]" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("list[Any]" and "int")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 173
  - **Error**: Unsupported operand types for > ("str" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for > ("str" and "int")
      -             stats['conference_win_pct'] = (stats['conference_wins'] + 0.5 * stats['conference_ties']) / conf_games if conf_games > 0 else 0.0
      ```

- **Line**: 185
  - **Error**: Item "Column[str]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "Column[str]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
      -             for opp_id in opponents:
      ```

- **Line**: 185
  - **Error**: Item "Column[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "Column[Any]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
      -             for opp_id in opponents:
      ```

- **Line**: 185
  - **Error**: Item "Column[float]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "Column[float]" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
      -             for opp_id in opponents:
      ```

- **Line**: 185
  - **Error**: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Item "float" of "dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float" has no attribute "__iter__" (not iterable)
      -             for opp_id in opponents:
      ```

- **Line**: 187
  - **Error**: Unsupported operand types for + ("float" and "dict[Any, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "dict[Any, Any]")
      -                     opp_win_pct_sum += team_stats[opp_id]['win_percentage']
      ```

- **Line**: 187
  - **Error**: Unsupported operand types for + ("float" and "list[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "list[Any]")
      -                     opp_win_pct_sum += team_stats[opp_id]['win_percentage']
      ```

- **Line**: 187
  - **Error**: Unsupported operand types for + ("float" and "str")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("float" and "str")
      -                     opp_win_pct_sum += team_stats[opp_id]['win_percentage']
      ```

- **Line**: 187
  - **Error**: Incompatible types in assignment (expression has type "float | ColumnElement[str] | ColumnElement[Any] | ColumnElement[float]", variable has type "float")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -                     opp_win_pct_sum += team_stats[opp_id]['win_percentage']
      ```

- **Line**: 187
  - **Error**: Invalid index type "Any | str" for "dict[Column[Any], dict[str, dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float]]"; expected type "Column[Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Invalid index type "Any | str" for "dict[Column[Any], dict[str, dict[Any, Any] | list[Any] | Column[str] | str | Column[Any] | Column[float] | float]]"; expected type "Column[Any]"
      -                     opp_win_pct_sum += team_stats[opp_id]['win_percentage']
      ```

- **Line**: 226
  - **Error**: Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         divisions = {}
      +         divisions: dict = {}
      ```

- **Line**: 239
  - **Error**: Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         conferences = {}
      +         conferences: dict = {}
      ```


## File: app/services/training/coaching_tree.py
- **Line**: 126
  - **Error**: Argument "category" to "CoachSkill" has incompatible type "str"; expected "SkillCategory"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "category" to "CoachSkill" has incompatible type "str"; expected "SkillCategory"
      -                 category=data["category"],
      ```

- **Line**: 171
  - **Error**: Need type annotation for "bonuses" (hint: "bonuses: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         bonuses = {}
      +         bonuses: dict = {}
      ```


## File: app/services/training/training_programs.py
- **Line**: 169
  - **Error**: Incompatible default for argument "seed" (default has type "None", argument has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, season_phase: SeasonPhase = SeasonPhase.REGULAR, seed: int = None):
      ```


## File: app/services/trait_acquisition_service.py
- **Line**: 5
  - **Error**: Module "app.models.stats" has no attribute "PlayerSeasonStats"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Module "app.models.stats" has no attribute "PlayerSeasonStats"
      - from app.models.stats import PlayerSeasonStats
      ```

- **Line**: 8
  - **Error**: Cannot find implementation or library stub for module named "structlog"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Cannot find implementation or library stub for module named "structlog"
      - import structlog
      ```

- **Line**: 46
  - **Error**: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"
      -                         trait_name,
      ```

- **Line**: 47
  - **Error**: Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"
      -                         source="MILESTONE" # or DEVELOPMENT
      ```

- **Line**: 127
  - **Error**: Incompatible return value type (got "PlayerTrait | None", expected "bool")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "PlayerTrait | None", expected "bool")
      -         return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")
      ```

- **Line**: 127
  - **Error**: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument 3 to "assign_trait" of "TraitService" has incompatible type "str"; expected "int"
      -         return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")
      ```

- **Line**: 127
  - **Error**: Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "source" to "assign_trait" of "TraitService" has incompatible type "str"; expected "TraitSource"
      -         return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")
      ```


## File: app/services/trait_evolution_service.py
- **Line**: 114
  - **Error**: Need type annotation for "event_counts" (hint: "event_counts: dict[<type>, <type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         event_counts = {}
      +         event_counts: dict = {}
      ```

- **Line**: 135
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if sack_count >= TRAIT_TRIGGERS["sacks_in_game"]["threshold"]:
      ```

- **Line**: 142
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if td_count >= TRAIT_TRIGGERS["tds_in_game"]["threshold"]:
      ```

- **Line**: 149
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if drop_count >= TRAIT_TRIGGERS["dropped_passes_in_game"]["threshold"]:
      ```

- **Line**: 162
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if injury_count >= TRAIT_TRIGGERS["injuries_in_season"]["threshold"]:
      ```

- **Line**: 169
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if fumble_count >= TRAIT_TRIGGERS["fumbles_in_season"]["threshold"]:
      ```

- **Line**: 176
  - **Error**: Unsupported operand types for >= ("int" and "object")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for >= ("int" and "object")
      -         if catch_count >= TRAIT_TRIGGERS["spectacular_catches_in_season"]["threshold"]:
      ```

- **Line**: 226
  - **Error**: "object" has no attribute "value"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "object" has no attribute "value"
      -             "tier": trigger["tier"].value,
      ```

- **Line**: 235
  - **Error**: "object" has no attribute "value"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "object" has no attribute "value"
      -             "tier": trigger["tier"].value
      ```


## File: app/services/trait_service.py
- **Line**: 189
  - **Error**: Dict entry 1 has incompatible type "str": "float"; expected "str": "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 1 has incompatible type "str": "float"; expected "str": "int"
      -         min_stat_threshold={"receptions": 100, "drop_rate_max": 0.05},
      ```

- **Line**: 596
  - **Error**: Incompatible default for argument "db" (default has type "None", argument has type "Session")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -     def __init__(self, db: Session = None):
      ```

- **Line**: 629
  - **Error**: Incompatible return value type (got "Sequence[Trait]", expected "list[Trait]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Incompatible return value type (got "Sequence[Trait]", expected "list[Trait]")
      -         return db.scalars(select(Trait)).all()
      ```

- **Line**: 711
  - **Error**: Unsupported operand types for <= ("int" and "None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for <= ("int" and "None")
      -                 if existing_count >= cap:
      ```

- **Line**: 745
  - **Error**: Name "get_player_traits" already defined on line 631
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Name "get_player_traits" already defined on line 631
      -     async def get_player_traits(self, player_id: int) -> List[TraitDefinition]:
      ```

- **Line**: 757
  - **Error**: Subclass of "Session" and "AsyncSession" cannot exist: would have incompatible method signatures
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Subclass of "Session" and "AsyncSession" cannot exist: would have incompatible method signatures
      -         if isinstance(self.db, AsyncSession):
      ```

- **Line**: 758
  - **Error**: Statement is unreachable
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Statement is unreachable
      -             result = await self.db.execute(
      ```

- **Line**: 900
  - **Error**: Incompatible default for argument "context" (default has type "None", argument has type "dict[str, Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Change type hint to include | None or Optional
      -         context: Dict[str, Any] = None
      ```

- **Line**: 911
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -             player.active_modifiers = {}
      ```

- **Line**: 913
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -             player.active_traits = []
      ```

- **Line**: 916
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -         if trait_def.name not in player.active_traits:
      ```

- **Line**: 917
  - **Error**: "Player" has no attribute "active_traits"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_traits"
      -             player.active_traits.append(trait_def.name)
      ```

- **Line**: 922
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -             current = player.active_modifiers.get(effect_key, 0)
      ```

- **Line**: 923
  - **Error**: "Player" has no attribute "active_modifiers"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: "Player" has no attribute "active_modifiers"
      -             player.active_modifiers[effect_key] = current + effect_value
      ```


## File: app/services/use_based_progression.py
- **Line**: 165
  - **Error**: [B311] Possible hardcoded password: '3'
  - **Solve**: Use secure alternatives for cryptography, parsing, or subprocesses.
  - **Full Proposed Solve**:
      ```python
      import secrets
      # Use secrets module for cryptographically secure random generation
      -         "pass_rush": 3,
      +         "pass_rush": 3,
      ```

- **Line**: 311
  - **Error**: Need type annotation for "gains" (hint: "gains: list[<type>] = ...")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Add proper type annotation
      -         gains = []
      +         gains: list = []
      ```


## File: app/services/validation/calibrator.py
- **Line**: 94
  - **Error**: Incompatible types in assignment (expression has type "float", variable has type "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Cast float to int
      -                 total_error += target.error_pct
      +                 total_error += target.error_pct  # Wrap expression in int()
      ```


## File: app/services/week_simulator.py
- **Line**: 101
  - **Error**: Dict entry 0 has incompatible type "str": "str"; expected "int": "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 0 has incompatible type "str": "str"; expected "int": "dict[Any, Any]"
      -             return {"error": "No unplayed games found for this week"}
      ```

- **Line**: 133
  - **Error**: Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
      -                 home_team_id=game.home_team_id,
      ```

- **Line**: 134
  - **Error**: Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
      -                 away_team_id=game.away_team_id,
      ```

- **Line**: 143
  - **Error**: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             game.is_played = True
      ```

- **Line**: 144
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             game.home_score = orchestrator.home_score
      ```

- **Line**: 145
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             game.away_score = orchestrator.away_score
      ```

- **Line**: 146
  - **Error**: Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             game.game_data = {
      ```

- **Line**: 176
  - **Error**: Dict entry 0 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 0 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"
      -             "week": week,
      ```

- **Line**: 177
  - **Error**: Dict entry 1 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 1 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"
      -             "games_simulated": len(results),
      ```

- **Line**: 178
  - **Error**: Dict entry 2 has incompatible type "str": "dict[Column[Any], dict[str, object]]"; expected "int": "dict[Any, Any]"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Dict entry 2 has incompatible type "str": "dict[Column[Any], dict[str, object]]"; expected "int": "dict[Any, Any]"
      -             "results": results
      ```

- **Line**: 218
  - **Error**: Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "home_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
      -             home_team_id=game.home_team_id,
      ```

- **Line**: 219
  - **Error**: Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Argument "away_team_id" to "start_new_game_session" of "SimulationOrchestrator" has incompatible type "Column[int]"; expected "int"
      -             away_team_id=game.away_team_id,
      ```

- **Line**: 226
  - **Error**: Incompatible types in assignment (expression has type "bool", variable has type "Column[bool]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         game.is_played = True
      ```

- **Line**: 227
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         game.home_score = orchestrator.home_score
      ```

- **Line**: 228
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         game.away_score = orchestrator.away_score
      ```

- **Line**: 229
  - **Error**: Incompatible types in assignment (expression has type "dict[str, object]", variable has type "Column[Any]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -         game.game_data = {
      ```

- **Line**: 272
  - **Error**: Value of type "Coroutine[Any, Any, None]" must be used
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Value of type "Coroutine[Any, Any, None]" must be used
      -         orchestrator.save_game_result()
      ```

- **Line**: 299
  - **Error**: Incompatible types in assignment (expression has type "Column[int]", variable has type "int | None")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             end_week = season.total_weeks
      ```

- **Line**: 303
  - **Error**: Unsupported operand types for + ("None" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("None" and "int")
      -         for week_num in range(start_week, end_week + 1):
      ```

- **Line**: 309
  - **Error**: Incompatible types in assignment (expression has type "int", variable has type "Column[int]")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Ensure the assigned value matches the variable's type hint
      -             season.current_week = week_num
      ```

- **Line**: 314
  - **Error**: Unsupported operand types for + ("None" and "int")
  - **Solve**: Add correct type annotations, handle None values properly, and fix type mismatches.
  - **Full Proposed Solve**:
      ```python
      # Type Fix: Unsupported operand types for + ("None" and "int")
      -             "weeks_simulated": list(range(start_week, end_week + 1)),
      ```


## Missing Files and Documentation Issues

### Missing File/Dir: docs/architecture/README.md
- **Error**: The file or directory `docs/architecture/README.md` is missing from the repository.
- **Solve**: Create the missing file and populate it with relevant context or structure.
- **Full Proposed Solve**:
  ```bash
  mkdir -p $(dirname docs/architecture/README.md) && touch docs/architecture/README.md
  # Add appropriate documentation content.
  ```

### Missing File/Dir: docs/data/README.md
- **Error**: The file or directory `docs/data/README.md` is missing from the repository.
- **Solve**: Create the missing file and populate it with relevant context or structure.
- **Full Proposed Solve**:
  ```bash
  mkdir -p $(dirname docs/data/README.md) && touch docs/data/README.md
  # Add appropriate documentation content.
  ```

### Missing File/Dir: AGENTS.md
- **Error**: The file or directory `AGENTS.md` is missing from the repository.
- **Solve**: Create the missing file and populate it with relevant context or structure.
- **Full Proposed Solve**:
  ```bash
  mkdir -p $(dirname AGENTS.md) && touch AGENTS.md
  # Add appropriate documentation content.
  ```

### Missing File/Dir: scripts/check_docs.py
- **Error**: The file or directory `scripts/check_docs.py` is missing from the repository.
- **Solve**: Create the missing file and populate it with relevant context or structure.
- **Full Proposed Solve**:
  ```bash
  mkdir -p $(dirname scripts/check_docs.py) && touch scripts/check_docs.py
  # Add appropriate documentation content.
  ```

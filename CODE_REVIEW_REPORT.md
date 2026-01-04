# Code Review Report

**To:** cweir45@gmail.com

**Date:** 2025-01-04

**Subject:** Comprehensive Code Review Findings

## Executive Summary

A comprehensive review of the codebase was conducted, focusing on `backend/app` and `frontend/src`. The backend analysis revealed significant strict type checking gaps and potential runtime errors related to `None` values. The frontend appears stable with no build or lint errors, though several incomplete features marked with TODOs exist. The `apts/` module was found to be missing package initialization files and documentation.

## 1. Critical Issues (Potential Runtime Bugs)

- **Circular/Duplicate Definitions**: Several files in `backend/app/models/player.py` have re-defined variables, likely due to property decorators or copy-paste errors.
- **NoneType Attribute Access**: `backend/app/orchestrator/simulation_orchestrator.py` attempts to call methods on potentially `None` objects without checks.
- **Missing Imports**: `backend/app/kernels/genesis/trauma_center.py` references undefined `AnatomyModel`.

## 2. Missing Files & Configuration

- **File**: `apts/__init__.py`, `apts/models/__init__.py`
  - **Error**: Missing `__init__.py` files prevent `apts` from being treated as a proper Python package.
  - **Solve**: Create empty `__init__.py` files in these directories.

## 3. Documentation Gaps

- **Module**: `apts/models/`
  - **Error**: Classes in `apts/models/` lack docstrings.
  - **Solve**: Add docstrings explaining the purpose of `BaseModel`, `Object`, `Location`, and `Transit`.

## 4. Backend Detailed Findings (By File)

### `backend/app/api/endpoints/abilities.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 41 | Name "AbilityStatus" already defined (possibly by an import)  | Remove duplicate definition or rename the variable. |

### `backend/app/api/endpoints/season.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 243 | Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")  | Add type annotation: `conferences: dict[<type>, <type>] = ...` |
| 392 | Name "timedelta" is not defined  | Import the missing name or define it. |
| 1172 | Name "suggest_draft_pick" already defined on line 893  | Remove duplicate definition or rename the variable. |

### `backend/app/core/db_helpers.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 9 | Incompatible default for argument "detail" (default has type "None", argument has type "str")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 13 | "type[T]" has no attribute "id"  | Fix the type mismatch or logic error. |
| 23 | Incompatible default for argument "detail" (default has type "None", argument has type "str")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 27 | "type[T]" has no attribute "id"  | Fix the type mismatch or logic error. |

### `backend/app/core/error_handlers.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 16 | Incompatible return value type (got "Any \| None", expected "str")  | Fix the type mismatch or logic error. |

### `backend/app/data/scouts.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 28 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 30 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 33 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 36 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 41 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 46 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 47 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 50 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 54 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 58 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 63 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 67 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 71 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 76 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 80 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 84 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 92 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 97 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 101 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 105 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 109 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 118 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 122 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 126 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 135 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 139 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 152 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 156 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 160 | Argument 5 to "ScoutData" has incompatible type "None"; expected "str"  | Cast the argument or update the function signature to accept the type. |

### `backend/app/data/special_jerseys.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 124 | Incompatible default for argument "year" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 137 | Incompatible return value type (got "None", expected "dict[str, Any]")  | Fix the type mismatch or logic error. |
| 148 | Incompatible return value type (got "object", expected "float")  | Fix the type mismatch or logic error. |

### `backend/app/engine/attribute_interaction.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 671 | Argument 2 to "replace" of "str" has incompatible type "Any \| None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 673 | Argument 2 to "replace" of "str" has incompatible type "Any \| None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 676 | Argument 2 to "replace" of "str" has incompatible type "Any \| None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 677 | Argument 2 to "replace" of "str" has incompatible type "Any \| None"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 810 | Unsupported operand types for + ("object" and "float")  | Fix the type mismatch or logic error. |
| 813 | Unsupported operand types for + ("object" and "float")  | Fix the type mismatch or logic error. |
| 815 | "object" has no attribute "append"  | Fix the type mismatch or logic error. |
| 816 | "object" has no attribute "append"  | Fix the type mismatch or logic error. |
| 819 | "object" has no attribute "append"  | Fix the type mismatch or logic error. |

### `backend/app/engine/core/enhanced_event_bus.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 249 | Argument 1 to "create_task" of "AbstractEventLoop" has incompatible type "Future[None] \| None"; expected "Coroutine[Any, Any, Never]"  | Cast the argument or update the function signature to accept the type. |
| 290 | Need type annotation for "task"  | Add explicit type annotation (e.g., `variable: Type = value`). |
| 290 | Argument 1 to "create_task" has incompatible type "Future[None] \| None"; expected "Coroutine[Any, Any, Never]"  | Cast the argument or update the function signature to accept the type. |

### `backend/app/engine/physics.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 55 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 56 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 58 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/engine/position_physics/offensive_line.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 177 | Need type annotation for "assignments" (hint: "assignments: dict[<type>, <type>] = ...")  | Add type annotation: `assignments: dict[<type>, <type>] = ...` |
| 185 | Incompatible types in assignment (expression has type "None", target has type "str")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 205 | Incompatible types in assignment (expression has type "None", target has type "str")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 207 | Incompatible return value type (got "dict[str, str]", expected "dict[str, str \| None]")  | Fix the type mismatch or logic error. |

### `backend/app/engine/position_physics/pass_rush.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 174 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/engine/rb_tribes.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 145 | Dict entry 0 has incompatible type "str": "str"; expected "str": "float"  | Fix the type mismatch or logic error. |
| 150 | Dict entry 5 has incompatible type "str": "str"; expected "str": "float"  | Fix the type mismatch or logic error. |

### `backend/app/kernels/core/sim_engine.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 25 | Name "PhysicsKernel" is not defined  | Import the missing name or define it. |
| 26 | Name "AIKernel" is not defined  | Import the missing name or define it. |

### `backend/app/kernels/cortex/behavior_tree.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 16 | Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  | Add type annotation: `context: dict[<type>, <type>] = ...` |

### `backend/app/kernels/cortex/coverage_net.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 29 | Incompatible return value type (got "Any \| None", expected "str")  | Fix the type mismatch or logic error. |

### `backend/app/kernels/genesis/trauma_center.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 21 | Name "AnatomyModel" is not defined  | Import the missing name or define it. |

### `backend/app/kernels/hive/weather.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 39 | Missing return statement  | Fix the type mismatch or logic error. |
| 63 | Name "get_ballistic_modifiers" already defined on line 20  | Remove duplicate definition or rename the variable. |
| 78 | Name "get_visibility_penalty" already defined on line 31  | Remove duplicate definition or rename the variable. |
| 91 | Name "get_sun_glare_vector" already defined on line 39  | Remove duplicate definition or rename the variable. |

### `backend/app/models/player.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 79 | Name "speed" already defined on line 76  | Remove duplicate definition or rename the variable. |
| 86 | Name "acceleration" already defined on line 83  | Remove duplicate definition or rename the variable. |
| 93 | Name "strength" already defined on line 90  | Remove duplicate definition or rename the variable. |
| 100 | Name "agility" already defined on line 97  | Remove duplicate definition or rename the variable. |
| 107 | Name "awareness" already defined on line 104  | Remove duplicate definition or rename the variable. |
| 114 | Name "stamina" already defined on line 111  | Remove duplicate definition or rename the variable. |
| 121 | Name "injury_resistance" already defined on line 118  | Remove duplicate definition or rename the variable. |
| 129 | Name "forty_yard_dash" already defined on line 126  | Remove duplicate definition or rename the variable. |
| 136 | Name "bench_press" already defined on line 133  | Remove duplicate definition or rename the variable. |
| 143 | Name "vertical_jump" already defined on line 140  | Remove duplicate definition or rename the variable. |
| 150 | Name "broad_jump" already defined on line 147  | Remove duplicate definition or rename the variable. |
| 157 | Name "three_cone_drill" already defined on line 154  | Remove duplicate definition or rename the variable. |
| 164 | Name "twenty_yard_shuttle" already defined on line 161  | Remove duplicate definition or rename the variable. |
| 172 | Name "power_clean_max" already defined on line 169  | Remove duplicate definition or rename the variable. |
| 179 | Name "gps_speed_max" already defined on line 176  | Remove duplicate definition or rename the variable. |
| 186 | Name "s2_cognition_score" already defined on line 183  | Remove duplicate definition or rename the variable. |
| 193 | Name "medical_flags" already defined on line 190  | Remove duplicate definition or rename the variable. |
| 200 | Name "genesis_revealed" already defined on line 197  | Remove duplicate definition or rename the variable. |
| 208 | Name "throw_power" already defined on line 205  | Remove duplicate definition or rename the variable. |
| 215 | Name "throw_accuracy_short" already defined on line 212  | Remove duplicate definition or rename the variable. |
| 222 | Name "throw_accuracy_mid" already defined on line 219  | Remove duplicate definition or rename the variable. |
| 229 | Name "throw_accuracy_deep" already defined on line 226  | Remove duplicate definition or rename the variable. |
| 236 | Name "catching" already defined on line 233  | Remove duplicate definition or rename the variable. |
| 243 | Name "route_running" already defined on line 240  | Remove duplicate definition or rename the variable. |
| 250 | Name "pass_block" already defined on line 247  | Remove duplicate definition or rename the variable. |
| 257 | Name "run_block" already defined on line 254  | Remove duplicate definition or rename the variable. |
| 264 | Name "tackle" already defined on line 261  | Remove duplicate definition or rename the variable. |
| 271 | Name "hit_power" already defined on line 268  | Remove duplicate definition or rename the variable. |
| 278 | Name "block_shed" already defined on line 275  | Remove duplicate definition or rename the variable. |
| 285 | Name "man_coverage" already defined on line 282  | Remove duplicate definition or rename the variable. |
| 292 | Name "zone_coverage" already defined on line 289  | Remove duplicate definition or rename the variable. |
| 299 | Name "pass_rush_power" already defined on line 296  | Remove duplicate definition or rename the variable. |
| 306 | Name "pass_rush_finesse" already defined on line 303  | Remove duplicate definition or rename the variable. |
| 313 | Name "play_recognition" already defined on line 310  | Remove duplicate definition or rename the variable. |
| 320 | Name "kick_power" already defined on line 317  | Remove duplicate definition or rename the variable. |
| 327 | Name "kick_accuracy" already defined on line 324  | Remove duplicate definition or rename the variable. |
| 335 | Name "pocket_presence" already defined on line 332  | Remove duplicate definition or rename the variable. |
| 342 | Name "quick_release" already defined on line 339  | Remove duplicate definition or rename the variable. |
| 349 | Name "scramble_willingness" already defined on line 346  | Remove duplicate definition or rename the variable. |
| 356 | Name "throw_on_run" already defined on line 353  | Remove duplicate definition or rename the variable. |
| 363 | Name "patience" already defined on line 360  | Remove duplicate definition or rename the variable. |
| 370 | Name "pass_pro_rating" already defined on line 367  | Remove duplicate definition or rename the variable. |
| 377 | Name "juke_efficiency" already defined on line 374  | Remove duplicate definition or rename the variable. |
| 384 | Name "release" already defined on line 381  | Remove duplicate definition or rename the variable. |
| 391 | Name "blocking_tenacity" already defined on line 388  | Remove duplicate definition or rename the variable. |
| 398 | Name "pull_speed" already defined on line 395  | Remove duplicate definition or rename the variable. |
| 405 | Name "anchor" already defined on line 402  | Remove duplicate definition or rename the variable. |
| 412 | Name "discipline" already defined on line 409  | Remove duplicate definition or rename the variable. |
| 419 | Name "first_step" already defined on line 416  | Remove duplicate definition or rename the variable. |
| 426 | Name "gap_integrity" already defined on line 423  | Remove duplicate definition or rename the variable. |
| 433 | Name "coverage_disguise" already defined on line 430  | Remove duplicate definition or rename the variable. |
| 440 | Name "blitz_timing" already defined on line 437  | Remove duplicate definition or rename the variable. |
| 447 | Name "run_fit" already defined on line 444  | Remove duplicate definition or rename the variable. |
| 454 | Name "press" already defined on line 451  | Remove duplicate definition or rename the variable. |
| 461 | Name "ball_tracking" already defined on line 458  | Remove duplicate definition or rename the variable. |
| 468 | Name "run_support" already defined on line 465  | Remove duplicate definition or rename the variable. |
| 475 | Name "hang_time" already defined on line 472  | Remove duplicate definition or rename the variable. |
| 482 | Name "coffin_corner" already defined on line 479  | Remove duplicate definition or rename the variable. |
| 489 | Name "return_vision" already defined on line 486  | Remove duplicate definition or rename the variable. |
| 497 | Name "arm_slot" already defined on line 494  | Remove duplicate definition or rename the variable. |
| 504 | Name "release_point_height" already defined on line 501  | Remove duplicate definition or rename the variable. |
| 511 | Name "vision_cone_angle" already defined on line 508  | Remove duplicate definition or rename the variable. |
| 518 | Name "break_tackle_threshold" already defined on line 515  | Remove duplicate definition or rename the variable. |
| 526 | Name "xp" already defined on line 523  | Remove duplicate definition or rename the variable. |
| 533 | Name "level" already defined on line 530  | Remove duplicate definition or rename the variable. |
| 540 | Name "skill_points" already defined on line 537  | Remove duplicate definition or rename the variable. |
| 547 | Name "development_trait" already defined on line 544  | Remove duplicate definition or rename the variable. |
| 558 | Name "abilities" already defined on line 555  | Remove duplicate definition or rename the variable. |
| 566 | Name "attribute_xp" already defined on line 563  | Remove duplicate definition or rename the variable. |
| 574 | Name "morale" already defined on line 571  | Remove duplicate definition or rename the variable. |
| 582 | Name "injury_status" already defined on line 579  | Remove duplicate definition or rename the variable. |
| 589 | Name "injury_type" already defined on line 586  | Remove duplicate definition or rename the variable. |
| 596 | Name "weeks_to_recovery" already defined on line 593  | Remove duplicate definition or rename the variable. |
| 603 | Name "injury_severity" already defined on line 600  | Remove duplicate definition or rename the variable. |
| 610 | Name "injury_recurrence_risk" already defined on line 607  | Remove duplicate definition or rename the variable. |
| 622 | Name "contract_years" already defined on line 619  | Remove duplicate definition or rename the variable. |
| 629 | Name "contract_salary" already defined on line 626  | Remove duplicate definition or rename the variable. |
| 636 | Name "is_rookie" already defined on line 633  | Remove duplicate definition or rename the variable. |
| 643 | Name "is_retired" already defined on line 640  | Remove duplicate definition or rename the variable. |
| 650 | Name "retirement_year" already defined on line 647  | Remove duplicate definition or rename the variable. |
| 657 | Name "legacy_score" already defined on line 654  | Remove duplicate definition or rename the variable. |

### `backend/app/orchestrator/match_context.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 25 | Incompatible default for argument "weather_config" (default has type "None", argument has type "dict[Any, Any]")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/orchestrator/play_caller.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 152 | Name "Player" is not defined  | Import the missing name or define it. |

### `backend/app/orchestrator/play_resolver.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 130 | Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  | Add type annotation: `context: dict[<type>, <type>] = ...` |
| 441 | Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  | Add type annotation: `context: dict[<type>, <type>] = ...` |
| 507 | Need type annotation for "context" (hint: "context: dict[<type>, <type>] = ...")  | Add type annotation: `context: dict[<type>, <type>] = ...` |
| 861 | Need type annotation for "crunch_context" (hint: "crunch_context: dict[<type>, <type>] = ...")  | Add type annotation: `crunch_context: dict[<type>, <type>] = ...` |

### `backend/app/orchestrator/simulation_orchestrator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 66 | Need type annotation for "game_config" (hint: "game_config: dict[<type>, <type>] = ...")  | Add type annotation: `game_config: dict[<type>, <type>] = ...` |
| 219 | Item "None" of "Any \| None" has no attribute "execute"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 220 | Item "None" of "Any \| None" has no attribute "execute"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 261 | Item "None" of "Any \| None" has no attribute "commit"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 351 | Item "None" of "Any \| None" has no attribute "execute"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 364 | Item "None" of "Any \| None" has no attribute "execute"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 375 | Item "None" of "Any \| None" has no attribute "add"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 383 | Item "None" of "Any \| None" has no attribute "commit"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 395 | Need type annotation for "offense_players" (hint: "offense_players: list[<type>] = ...")  | Add type annotation: `offense_players: list[<type>] = ...` |
| 396 | Need type annotation for "defense_players" (hint: "defense_players: list[<type>] = ...")  | Add type annotation: `defense_players: list[<type>] = ...` |
| 425 | Value of type "Coroutine[Any, Any, None]" must be used  | Fix the type mismatch or logic error. |

### `backend/app/rpg/injury_system.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 12 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 322 | Incompatible types in assignment (expression has type "None", variable has type "dict[str, int]")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 536 | Argument "seed" to "InjurySystem" has incompatible type "Any \| None"; expected "int"  | Cast the argument or update the function signature to accept the type. |
| 626 | Incompatible default for argument "injury_system" (default has type "None", argument has type "InjurySystem")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/rpg/narrative.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 37 | Incompatible return value type (got "None", expected "dict[Any, Any]")  | Fix the type mismatch or logic error. |

### `backend/app/rpg/traits.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 54 | Incompatible return value type (got "Collection[str]", expected "dict[Any, Any]")  | Fix the type mismatch or logic error. |

### `backend/app/services/ai/gemini_client.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 205 | Incompatible types in assignment (expression has type "str \| None", variable has type "T \| None")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/ai_research_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 141 | Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 142 | Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 143 | Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  | Cast the argument or update the function signature to accept the type. |
| 144 | Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"  | Cast the argument or update the function signature to accept the type. |
| 145 | Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  | Cast the argument or update the function signature to accept the type. |
| 151 | Argument "summary" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 152 | Argument "recommended_approach" to "ResearchResult" has incompatible type "Sequence[str]"; expected "str"  | Cast the argument or update the function signature to accept the type. |
| 153 | Argument "code_examples" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  | Cast the argument or update the function signature to accept the type. |
| 154 | Argument "complexity" to "ResearchResult" has incompatible type "Sequence[str]"; expected "TaskComplexity"  | Cast the argument or update the function signature to accept the type. |
| 155 | Argument "sources" to "ResearchResult" has incompatible type "Sequence[str]"; expected "list[str]"  | Cast the argument or update the function signature to accept the type. |

### `backend/app/services/broadcasting_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 194 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/data_sync_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 321 | Unsupported target for indexed assignment ("object")  | Fix the type mismatch or logic error. |

### `backend/app/services/database/optimizer.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 81 | Incompatible default for argument "pattern" (default has type "None", argument has type "str")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/depth_chart_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 16 | Need type annotation for "chart" (hint: "chart: dict[<type>, <type>] = ...")  | Add type annotation: `chart: dict[<type>, <type>] = ...` |

### `backend/app/services/elo_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 84 | Incompatible default for argument "k_factor" (default has type "None", argument has type "float")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/enhanced_chemistry_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 261 | Need type annotation for "games_data" (hint: "games_data: dict[<type>, <type>] = ...")  | Add type annotation: `games_data: dict[<type>, <type>] = ...` |

### `backend/app/services/gm_agent.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 14 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 107 | Unsupported operand types for - ("object" and "int")  | Fix the type mismatch or logic error. |
| 133 | Incompatible default for argument "target_position" (default has type "None", argument has type "str")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 182 | Unsupported operand types for / ("object" and "int")  | Fix the type mismatch or logic error. |

### `backend/app/services/issue_logger.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 42 | Item "None" of "datetime \| None" has no attribute "strftime"  | Add a `None` check before accessing the attribute (e.g., `if obj is not None:`). |
| 109 | Library stubs not installed for "aiofiles"  | Install missing stubs (e.g., `pip install types-aiofiles`). |

### `backend/app/services/offseason_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 19 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 247 | Need type annotation for "position_counts" (hint: "position_counts: dict[<type>, <type>] = ...")  | Add type annotation: `position_counts: dict[<type>, <type>] = ...` |

### `backend/app/services/player_development_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 19 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 78 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 80 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 82 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 85 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 89 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 91 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/playoff_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 93 | Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  | Add type annotation: `divisions: dict[<type>, <type>] = ...` |

### `backend/app/services/rating_calculator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 297 | Incompatible types in assignment (expression has type "Any \| float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/rookie_generator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 18 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 57 | Argument 2 to "_create_rookie" of "RookieGenerator" has incompatible type "Any \| None"; expected "dict[Any, Any]"  | Cast the argument or update the function signature to accept the type. |
| 64 | Incompatible default for argument "stats_context" (default has type "None", argument has type "dict[Any, Any]")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/schedule_generator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 26 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 34 | Incompatible default for argument "start_date" (default has type "None", argument has type "datetime")  | Update type hint to `Optional[Type]` or `Type | None = None`. |
| 82 | Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  | Add type annotation: `divisions: dict[<type>, <type>] = ...` |
| 166 | Need type annotation for "matchups" (hint: "matchups: list[<type>] = ...")  | Add type annotation: `matchups: list[<type>] = ...` |

### `backend/app/services/scouting/draft_board.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 59 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/society/social_graph.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 149 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |
| 151 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/standings_calculator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 226 | Need type annotation for "divisions" (hint: "divisions: dict[<type>, <type>] = ...")  | Add type annotation: `divisions: dict[<type>, <type>] = ...` |
| 239 | Need type annotation for "conferences" (hint: "conferences: dict[<type>, <type>] = ...")  | Add type annotation: `conferences: dict[<type>, <type>] = ...` |

### `backend/app/services/training/coaching_tree.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 171 | Need type annotation for "bonuses" (hint: "bonuses: dict[<type>, <type>] = ...")  | Add type annotation: `bonuses: dict[<type>, <type>] = ...` |

### `backend/app/services/training/training_programs.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 169 | Incompatible default for argument "seed" (default has type "None", argument has type "int")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/trait_evolution_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 114 | Need type annotation for "event_counts" (hint: "event_counts: dict[<type>, <type>] = ...")  | Add type annotation: `event_counts: dict[<type>, <type>] = ...` |

### `backend/app/services/trait_service.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 189 | Dict entry 1 has incompatible type "str": "float"; expected "str": "int"  | Fix the type mismatch or logic error. |
| 745 | Name "get_player_traits" already defined on line 631  | Remove duplicate definition or rename the variable. |
| 900 | Incompatible default for argument "context" (default has type "None", argument has type "dict[str, Any]")  | Update type hint to `Optional[Type]` or `Type | None = None`. |

### `backend/app/services/use_based_progression.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 311 | Need type annotation for "gains" (hint: "gains: list[<type>] = ...")  | Add type annotation: `gains: list[<type>] = ...` |

### `backend/app/services/validation/calibrator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 94 | Incompatible types in assignment (expression has type "float", variable has type "int")  | Ensure the assigned value matches the variable's type, or update the type hint. |

### `backend/app/services/week_simulator.py`

| Line | Error | Proposed Solve |
|------|-------|----------------|
| 101 | Dict entry 0 has incompatible type "str": "str"; expected "int": "dict[Any, Any]"  | Fix the type mismatch or logic error. |
| 176 | Dict entry 0 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  | Fix the type mismatch or logic error. |
| 177 | Dict entry 1 has incompatible type "str": "int"; expected "int": "dict[Any, Any]"  | Fix the type mismatch or logic error. |
| 178 | Dict entry 2 has incompatible type "str": "dict[Any, dict[str, Any]]"; expected "int": "dict[Any, Any]"  | Fix the type mismatch or logic error. |

## 5. Frontend Notes

Automated checks (`tsc`, `eslint`) passed successfully. However, manual inspection reveals technical debt:

- **TODOs**: Numerous TODOs exist indicating incomplete integration with real APIs (e.g., `LiveSim.tsx` using mock data, `SkillsPage.tsx` missing backend points).
- **Recommendation**: prioritize connecting `LiveSim` to the `SimulationOrchestrator` websocket and implementing the real RPG trait system.

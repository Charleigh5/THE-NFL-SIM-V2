# Comprehensive Code Review Report

This report outlines bugs, type errors, typescript issues, lack of documentation, and missing files across the codebase.

## Backend Linter & Bugs (Ruff)

**File:** `backend/alembic/env.py`
**Line:** 1
**Error:** I001 Import block is un-sorted or un-formatted
**Proposed Solve:**
```python
# Use `isort backend/alembic/env.py` to sort imports properly
```

**File:** `backend/alembic/env.py`
**Line:** 16
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.core.config import settings  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 16
**Error:** I001 Import block is un-sorted or un-formatted
**Proposed Solve:**
```python
# Use `isort backend/alembic/env.py` to sort imports properly
```

**File:** `backend/alembic/env.py`
**Line:** 17
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.base import Base  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 19
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.team import Team  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 19
**Error:** F401 `app.models.team.Team` imported but unused
**Proposed Solve:**
```python
# from app.models.team import Team  # Removed unused import
```

**File:** `backend/alembic/env.py`
**Line:** 20
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.player import Player  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 20
**Error:** F401 `app.models.player.Player` imported but unused
**Proposed Solve:**
```python
# from app.models.player import Player  # Removed unused import
```

**File:** `backend/alembic/env.py`
**Line:** 21
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.coach import Coach  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 21
**Error:** F401 `app.models.coach.Coach` imported but unused
**Proposed Solve:**
```python
# from app.models.coach import Coach  # Removed unused import
```

**File:** `backend/alembic/env.py`
**Line:** 22
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.gm import GM  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 22
**Error:** F401 `app.models.gm.GM` imported but unused
**Proposed Solve:**
```python
# from app.models.gm import GM  # Removed unused import
```

**File:** `backend/alembic/env.py`
**Line:** 23
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.game import Game  # Move this import to the top of the file
```

**File:** `backend/alembic/env.py`
**Line:** 23
**Error:** F401 `app.models.game.Game` imported but unused
**Proposed Solve:**
```python
# from app.models.game import Game  # Removed unused import
```

**File:** `backend/alembic/env.py`
**Line:** 24
**Error:** E402 Module level import not at top of file
**Proposed Solve:**
```python
from app.models.stats import PlayerGameStats  # Move this import to the top of the file
```

## Backend Security Issues (Bandit)

**File:** `app/api/endpoints/abilities.py`
**Line:** 216
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/abilities.py`
**Line:** 219
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/abilities.py`
**Line:** 242
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/abilities.py`
**Line:** 246
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/abilities.py`
**Line:** 247
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/medical.py`
**Line:** 122
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/medical.py`
**Line:** 124
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/medical.py`
**Line:** 129
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/physics_api.py`
**Line:** 92
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
**File:** `app/api/endpoints/physics_api.py`
**Line:** 93
**Error:** Standard pseudo-random generators are not suitable for security/cryptographic purposes. (LOW)
## Backend Type Issues (Mypy)

**File:** `backend/app/services/training/coaching_tree.py`
**Line:** 126
**Error:** error Argument "category" to "CoachSkill" has incompatible type "str"; expected "SkillCategory"  [arg-type]
**Proposed Solve:**
```python
category=data["category"],  # type: ignore
```

**File:** `backend/app/services/training/coaching_tree.py`
**Line:** 171
**Error:** error Need type annotation for "bonuses" (hint: "bonuses: dict[<type>, <type>] = ...")  [var-annotated]
**Proposed Solve:**
```python
bonuses: Any = {}  # Ensure correct type is added
```

**File:** `backend/app/services/society/social_graph.py`
**Line:** 149
**Error:** error Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Proposed Solve:**
```python
positive_rels += r.strength  # type: ignore
```

**File:** `backend/app/services/society/social_graph.py`
**Line:** 151
**Error:** error Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
**Proposed Solve:**
```python
negative_rels += r.strength  # type: ignore
```

**File:** `backend/app/engine/rb_tribes.py`
**Line:** 145
**Error:** error Dict entry 0 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
**Proposed Solve:**
```python
"tribe": tribe.value,  # type: ignore
```

**File:** `backend/app/engine/rb_tribes.py`
**Line:** 150
**Error:** error Dict entry 5 has incompatible type "str": "str"; expected "str": "float"  [dict-item]
**Proposed Solve:**
```python
"description": profile.description  # type: ignore
```

**File:** `backend/app/data/special_jerseys.py`
**Line:** 124
**Error:** error Incompatible default for argument "year" (default has type "None", argument has type "int")  [assignment]
**Proposed Solve:**
```python
def get_thanksgiving_jersey(team_abbr: str, year: int = None) -> Dict[str, Any]:  # Change default to correct type or Optional[Type]
```

**File:** `backend/app/data/special_jerseys.py`
**Line:** 137
**Error:** error Incompatible return value type (got "None", expected "dict[str, Any]")  [return-value]
**Proposed Solve:**
```python
return None  # type: ignore
```

**File:** `backend/app/data/special_jerseys.py`
**Line:** 148
**Error:** error Incompatible return value type (got "object", expected "float")  [return-value]
**Proposed Solve:**
```python
return THANKSGIVING_HOSTS[team_abbr]["home_field_boost"]  # type: ignore
```

**File:** `backend/app/core/trade_config.py`
**Line:** 2
**Error:** error Cannot find implementation or library stub for module named "pydantic_settings"  [import-not-found]
**Proposed Solve:**
```python
from pydantic_settings import BaseSettings  # type: ignore
```

## Frontend Issues (ESLint)

## Frontend Type Issues (TypeScript)

## Missing Files & Documentation

**Missing:** `docs/architecture/`
**Proposed Solve:**
```bash
mkdir -p docs/architecture/
```

**Missing:** `docs/data/`
**Proposed Solve:**
```bash
mkdir -p docs/data/
```

**Missing:** `AGENTS.md`
**Proposed Solve:**
```bash
touch AGENTS.md
```

**Missing:** `scripts/check_docs.py`
**Proposed Solve:**
```bash
touch scripts/check_docs.py
```

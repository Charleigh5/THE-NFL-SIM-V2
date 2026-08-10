Code Review Report
==================

## Ruff Issues (Top 10)
File: /app/backend/alembic/env.py
Line: 1
Error: Import block is un-sorted or un-formatted
Proposed Solve:
```
# Import app config and models
import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context


```

File: /app/backend/alembic/env.py
Line: 16
Error: Module level import not at top of file
Proposed Solve:
```
No fix provided by Ruff.
```

File: /app/backend/alembic/env.py
Line: 16
Error: Import block is un-sorted or un-formatted
Proposed Solve:
```
from app.core.config import settings
from app.models.base import Base
from app.models.coach import Coach
from app.models.feedback import UserFeedback
from app.models.game import Game
from app.models.gm import GM
from app.models.player import Player

# New Player Decomposition Models
from app.models.player_attributes import PlayerAttributes
from app.models.player_contract import PlayerContract
from app.models.player_game_starts import PlayerGameStarts
from app.models.player_injury import PlayerInjury
from app.models.player_physics import PlayerPhysics
from app.models.player_progression import PlayerProgression
from app.models.stats import PlayerGameStats

# Import all models to ensure they are registered with Base.metadata
from app.models.team import Team
from app.models.trait import PlayerTrait, Trait


```

File: /app/backend/alembic/env.py
Line: 17
Error: Module level import not at top of file
Proposed Solve:
```
No fix provided by Ruff.
```

File: /app/backend/alembic/env.py
Line: 19
Error: Module level import not at top of file
Proposed Solve:
```
No fix provided by Ruff.
```

File: /app/backend/alembic/env.py
Line: 19
Error: `app.models.team.Team` imported but unused
Proposed Solve:
```

```

File: /app/backend/alembic/env.py
Line: 20
Error: Module level import not at top of file
Proposed Solve:
```
No fix provided by Ruff.
```

File: /app/backend/alembic/env.py
Line: 20
Error: `app.models.player.Player` imported but unused
Proposed Solve:
```

```

File: /app/backend/alembic/env.py
Line: 21
Error: Module level import not at top of file
Proposed Solve:
```
No fix provided by Ruff.
```

File: /app/backend/alembic/env.py
Line: 21
Error: `app.models.coach.Coach` imported but unused
Proposed Solve:
```

```

## Bandit Security Issues (Top 10)
File: ./app/api/endpoints/abilities.py
Line: 216
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/abilities.py
Line: 219
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/abilities.py
Line: 242
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/abilities.py
Line: 246
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/abilities.py
Line: 247
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/medical.py
Line: 122
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/medical.py
Line: 124
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/medical.py
Line: 129
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/physics_api.py
Line: 92
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

File: ./app/api/endpoints/physics_api.py
Line: 93
Error: Standard pseudo-random generators are not suitable for security/cryptographic purposes.
Proposed Solve:
```
# Replace or suppress bandit warning
# https://cwe.mitre.org/data/definitions/330.html
```

## ESLint Issues
## Mypy Issues (Top 10)
File: app/services/training/coaching_tree.py
Line: 126
Error: Argument "category" to "CoachSkill" has incompatible type "str"; expected "SkillCategory"  [arg-type]
Proposed Solve:
```
Fix type annotation.
```

File: app/services/training/coaching_tree.py
Line: 171
Error: Need type annotation for "bonuses" (hint
Proposed Solve:
```
Fix type annotation.
```

File: app/services/society/social_graph.py
Line: 149
Error: Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
Proposed Solve:
```
Fix type annotation.
```

File: app/services/society/social_graph.py
Line: 151
Error: Incompatible types in assignment (expression has type "float", variable has type "int")  [assignment]
Proposed Solve:
```
Fix type annotation.
```

File: app/engine/rb_tribes.py
Line: 145
Error: Dict entry 0 has incompatible type "str"
Proposed Solve:
```
Fix type annotation.
```

File: app/engine/rb_tribes.py
Line: 150
Error: Dict entry 5 has incompatible type "str"
Proposed Solve:
```
Fix type annotation.
```

File: app/data/special_jerseys.py
Line: 124
Error: Incompatible default for argument "year" (default has type "None", argument has type "int")  [assignment]
Proposed Solve:
```
Fix type annotation.
```

File: app/data/special_jerseys.py
Line: 137
Error: Incompatible return value type (got "None", expected "dict[str, Any]")  [return-value]
Proposed Solve:
```
Fix type annotation.
```

File: app/data/special_jerseys.py
Line: 148
Error: Incompatible return value type (got "object", expected "float")  [return-value]
Proposed Solve:
```
Fix type annotation.
```

File: app/core/trade_config.py
Line: 2
Error: Cannot find implementation or library stub for module named "pydantic_settings"  [import-not-found]
Proposed Solve:
```
Fix type annotation.
```

## Missing Files & Documentation
- `docs/architecture/` missing.
- `docs/data/` missing.
- `AGENTS.md` missing.
- `scripts/check_docs.py` missing.

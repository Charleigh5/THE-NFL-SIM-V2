To: cweir45@gmail.com
Subject: Comprehensive Code Review Report

# Code Review Report

## Missing Files and Directories
- **File/Directory:** `docs/architecture/`
  - **Error:** Directory is missing from the project structure.
  - **Solve:** Create the directory to store architectural diagrams and design decisions.
  ```bash
  mkdir -p docs/architecture
  ```

- **File/Directory:** `docs/data/`
  - **Error:** Directory is missing from the project structure.
  - **Solve:** Create the directory to store data schemas and sample data.
  ```bash
  mkdir -p docs/data
  ```

- **File/Directory:** `AGENTS.md`
  - **Error:** File is missing from the repository root.
  - **Solve:** Create the file to provide instructions and tips for AI agents working with the code.
  ```markdown
  # Agents Guidelines
  - Adhere to PEP 8 and use modern type hints.
  - Frontend code should use React 19 standards.
  ```

- **File/Directory:** `scripts/check_docs.py`
  - **Error:** Script is missing.
  - **Solve:** Create a Python script to validate documentation links and structure.
  ```python
  import os

  def check_docs():
      print("Checking docs...")
      if not os.path.exists("docs/"):
          print("Docs directory missing!")

  if __name__ == "__main__":
      check_docs()
  ```

## Specific Code and Security Issues
- **File:** `backend/app/core/redis_cache.py` (and others)
  - **Line:** Various
  - **Error:** [B324] Use of weak hashing algorithm `md5`.
  - **Solve:** Replace `hashlib.md5` with `hashlib.sha256`.
  ```python
  import hashlib
  hash_val = hashlib.sha256(data.encode()).hexdigest()
  ```

- **File:** `backend/tests/verify_play_calling.py`
  - **Line:** Imports
  - **Error:** `ModuleNotFoundError: No module named 'pydantic'` and `NameError` due to undefined `Player`.
  - **Solve:** Add missing imports.
  ```python
  from app.models.player import Player
  ```

- **File:** `backend/app/models/player.py`
  - **Line:** Inside TYPE_CHECKING block
  - **Error:** Missing `BodyPart` import.
  - **Solve:** Add the import.
  ```python
  from typing import TYPE_CHECKING
  if TYPE_CHECKING:
      from app.models.medical import BodyPart
  ```

- **File:** `frontend/src/services/season.ts`
  - **Line:** Various methods
  - **Error:** Functions return hardcoded mock data.
  - **Solve:** Implement actual API calls.
  ```typescript
  export const getCurrentPick = async () => {
      const response = await api.get('/draft/current-pick');
      return response.data;
  };
  ```

- **File:** `backend/app/services/standings_calculator.py`
  - **Line:** 226, 239
  - **Error:** Missing type annotations for `divisions` and `conferences`.
  - **Solve:** Add explicit dict type annotations.
  ```python
  from typing import Any
  divisions: dict[str, list[dict[str, Any]]] = {}
  conferences: dict[str, list[dict[str, Any]]] = {}
  ```

- **File:** `frontend/src/pages/DepthChart.tsx` (and others)
  - **Line:** Various
  - **Error:** Use of `alert()` and `console.log()` in production code.
  - **Solve:** Replace with proper logging and UI toast notifications.
  ```typescript
  import { logger } from '../utils/logger';
  import { toast } from 'react-toastify';
  logger.info("Message");
  toast.error("An error occurred");
  ```

## Automated Static Analysis Issues (Sampled from Artifacts)
A complete list of thousands of automated linting errors is available in `artifacts/tsc_output.txt`, `artifacts/eslint_output.txt`, `artifacts/ruff_output.txt`, `artifacts/mypy_output.txt`, and `artifacts/bandit_output.txt`. Below are representative samples indicating widespread issues.

### MyPy Type Error
- **File:** `backend/app/main.py`
- **Line:** 8
- **Error:** Skipping analyzing "app.core.app_factory": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 2
- **Error:** Cannot find implementation or library stub for module named "sqlalchemy.orm"  [import-not-found]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 3
- **Error:** Cannot find implementation or library stub for module named "sqlalchemy"  [import-not-found]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 4
- **Error:** Skipping analyzing "app.models.player": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 5
- **Error:** Skipping analyzing "app.models.stats": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 6
- **Error:** Skipping analyzing "app.services.trait_service": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 7
- **Error:** Skipping analyzing "app.services.gm_agent": module is installed, but missing library stubs or py.typed marker  [import-untyped]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/trait_acquisition_service.py`
- **Line:** 8
- **Error:** Cannot find implementation or library stub for module named "structlog"  [import-not-found]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/stats_service.py`
- **Line:** 1
- **Error:** Cannot find implementation or library stub for module named "sqlalchemy.orm"  [import-not-found]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### MyPy Type Error
- **File:** `backend/app/services/stats_service.py`
- **Line:** 2
- **Error:** Cannot find implementation or library stub for module named "sqlalchemy"  [import-not-found]
**Proposed Solve:**
```python
# Verify types and missing stubs. E.g.
from typing import Any, Dict, List
# Ensure third party modules have types installed.
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/abilities.py`
- **Line:** 216
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/abilities.py`
- **Line:** 219
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/abilities.py`
- **Line:** 242
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/abilities.py`
- **Line:** 246
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/abilities.py`
- **Line:** 247
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/medical.py`
- **Line:** 122
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/medical.py`
- **Line:** 124
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/medical.py`
- **Line:** 129
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/physics_api.py`
- **Line:** 92
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Bandit Security Issue
- **File:** `backend/app/api/endpoints/physics_api.py`
- **Line:** 93
- **Error:** [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
**Proposed Solve:**
```python
# Replace weak crypto or remove assertions from production code.
# Example: use hashlib.sha256() instead of hashlib.md5()
```

### Frontend Linting Issues
Numerous TypeScript and ESLint formatting issues exist across the `frontend/src/` directory, including missing variables and incorrectly typed React hooks. Please run `npm run lint --fix` and explicitly annotate missing TS variables.

# Build Automation Scripts

This directory contains automation scripts for building the NFL Sim Engine.

## Quick Start

```bash
# Run full automation (all 8 batches)
python scripts/run_automation.py

# Preview what will be executed (no changes)
python scripts/run_automation.py --dry-run

# Start from a specific batch
python scripts/run_automation.py --batch 3

# Skip verification tests
python scripts/run_automation.py --skip-tests
```

## Files

| File                | Description                                      |
| ------------------- | ------------------------------------------------ |
| `run_automation.py` | Simple entry point to run automation             |
| `automate_build.py` | Main orchestration script with batch definitions |
| `task_executor.py`  | Code generation for each task                    |

## Batch Overview

| Batch | Parallel Agents | Focus                      |
| ----- | --------------- | -------------------------- |
| 1     | 2               | Logging & Error Boundaries |
| 2     | 3               | Database Models            |
| 3     | 1               | Alembic Migration          |
| 4     | 4               | Backend Services           |
| 5     | 3               | API Endpoints              |
| 6     | 4               | React Components           |
| 7     | 2               | Frontend API Services      |
| 8     | 3               | Tests & Documentation      |

## Logs

Build logs are saved to: `logs/automation/`

- `build_YYYYMMDD_HHMMSS.log` - Full build log
- `report_YYYYMMDD_HHMMSS.txt` - Summary report

## Auto-Approval

The automation runs with `AUTO_APPROVE_ALL = True`, meaning:

- All review prompts are auto-approved
- All continue-on-failure prompts are auto-approved
- Verification tests still run but failures don't halt execution

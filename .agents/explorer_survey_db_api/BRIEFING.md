# BRIEFING — 2026-08-22T16:21:30Z

## Mission
Investigate Database Schema Consolidation, ORM Integrity, and Backend API Architecture, Concurrency, and Security Hardening (R1 & R4) for THE-NFL-SIM-V2.

## 🔒 My Identity
- Archetype: explorer
- Roles: Database & API Architecture Specialist
- Working directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_db_api
- Original parent: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Milestone: exploration_survey_r1_r4

## 🔒 Key Constraints
- Read-only investigation — do NOT implement or modify source files
- Exact file paths, line numbers, root causes, and recommended surgical fix strategies required
- Output comprehensive findings in handoff.md

## Current Parent
- Conversation ID: b4a0be66-d743-42bc-b0f8-c9aaf3893cdb
- Updated: 2026-08-22T16:21:30Z

## Investigation State
- **Explored paths**:
  - `backend/app/models/` (`player_game_start.py`, `player_game_starts.py`, `stats.py`, `player.py`, `trait.py`, `__init__.py`, and all 1:1 decomposition models)
  - `backend/alembic/env.py` and `backend/alembic/versions/`
  - `backend/app/core/database.py`, `app_factory.py`, `setup.py`, `auth.py`, `error_handlers.py`, `error_decorators.py`
  - `backend/app/api/endpoints/` (`coaches.py`, `news.py`, `training.py`, `season.py`, `players.py`, `websocket.py`, `live_visualization.py`, `genesis.py`, `abilities.py`, `draft.py`)
  - `backend/app/api/` (`combine.py`, `news_router.py`, `training.py`)
  - `backend/.env.example`
- **Key findings**:
  - Found triple definition of `player_game_starts` (`player_game_start.py`, `player_game_starts.py`, `stats.py`).
  - Found `alembic/env.py` misses 15+ models (`Season`, `PlayoffMatchup`, `DepthChart`, `NewsItem`, etc.).
  - Found `Player.traits` is missing on `Player` (model defines `player_traits`), breaking `GET /api/players/{player_id}/profile`.
  - Found `Player.speed` and other RPG hybrid properties lack `@expression` SQL subqueries, causing `Comparator` crashes in `DraftAssistant`.
  - Found 1:1 player decomposition relationships lack `cascade="all, delete-orphan"` and use `lazy="joined"`.
  - Found SQLite missing WAL pragmas and busy timeout.
  - Found 4 orphaned/disjoint API router files (`coaches.py`, `combine.py`, `news_router.py`, `training.py`).
  - Found blocking sync DB calls inside `async def` endpoints causing event loop starvation.
  - Found duplicate session acquisition (`db: AsyncSession` + `SessionLocal()`) in `season.py`.
  - Found competing WebSocket managers lacking game isolation, async locks, and backpressure timeouts.
  - Found hardcoded Vertex AI key in `backend/.env.example`.
  - Found unauthenticated database reset/seed endpoint at `POST /api/genesis/seed`.
  - Found raw exception string disclosures in `error_handlers.py` and file disk leaks in `error_decorators.py`.
- **Unexplored areas**: None. R1 and R4 thoroughly explored and documented.

## Key Decisions Made
- All findings documented with verbatim line numbers, evidence chains, and surgical remediation designs in `handoff.md`.

## Artifact Index
- DISPATCH.md — incoming instructions log
- BRIEFING.md — working memory and identity
- progress.md — liveness heartbeat
- handoff.md — final 5-component handoff report

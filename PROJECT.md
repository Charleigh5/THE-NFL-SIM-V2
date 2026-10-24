# Project: THE-NFL-SIM-V2 Performance Optimization (TASK-PERF-001)

## Architecture
Comprehensive full-stack performance optimization addressing database connection pool starvation, ORM N+1/selectin query amplification, unconstrained loopback HTTP timeouts on Windows, missing cache-aside layers, frontend waterfall loaders, and eager bundle bloat.

### Component Boundaries & Data Flow
1. **Broadcast & VoiceStudio Subsystem (`backend/app/services/voicestudio_tts_service.py`, `backend/app/api/endpoints/broadcast.py`)**:
   - `VoiceStudioTTSService`: Granular HTTP timeouts (`connect=0.15s`, `read=2.0s/60.0s`) and a 30s monotonic negative circuit breaker (`is_circuit_open()`, `trip_circuit()`, `reset_circuit()`).
   - `broadcast.py`: Decouples synchronous DB session from async network I/O by executing `build_fact_packet` in `run_in_threadpool` with short-lived session via `get_threadpool_db` (preserving `dependency_overrides[get_db]`). L1 thread-safe TTL response cache (`_narration_response_cache`, 60s TTL).
2. **Narrator Facts Subsystem (`backend/app/services/narrator_facts_service.py`)**:
   - `build_fact_packet`: Suppresses 5 1:1 satellite tables (`attributes`, `contract`, `physics`, `injury`, `progression`) on `Player` using `noload("*")`.
   - Consolidates `Season` queries into single `order_by(Season.is_active.desc(), desc(Season.year)).first()`.
   - Consolidates `SeasonHistory` queries into single `.filter(or_(champion_team_id == team_id, runner_up_team_id == team_id))`.
   - Eagerly loads `Team.season_history` via `joinedload` and `Game.home_team`/`away_team` via `joinedload`.
   - Eagerly loads `Player.season_stats` and `Player.player_traits`->`Trait` via `joinedload`.
   - Removes `RPGEvent` trigger checks from read-only fact gathering.
   - Total queries: 17 -> <= 6.
3. **Season Summary & Standings Cache Subsystem (`backend/app/core/season_cache.py`, `backend/app/api/endpoints/season.py`)**:
   - `SeasonCacheManager`: Thread-safe L1 memory cache (60s TTL) with `get_summary()`, `set_summary()`, `get_standings()`, `set_standings()`, and `invalidate_season_caches()`.
   - `season.py`: Consolidates two `Game` count queries into single `CASE` aggregation. Invalidation hooks in 8 simulation/advance endpoints. Also invokes `clear_narrator_response_cache()`.
4. **Frontend Architecture (`frontend/src/router.tsx`, `types/season.ts`, `RegionSelector.tsx`, `NarratorBar.tsx`)**:
   - `router.tsx`: `seasonDashboardLoader` fetches `api.getTeams()` and `seasonApi.getSeasonSummary()` concurrently, reuses `summary.standings` and `summary.league_leaders` directly, avoiding waterfalls.
   - `types/season.ts`: Strict contract parity with `ConferenceStandings`, `DivisionStandings`, and extended `SeasonSummary`.
   - `RegionSelector.tsx`: Dynamic `await import("html2canvas")` inside capture handler, eliminating eager ~201 kB bundle on initial page load.
   - `NarratorBar.tsx`: Scoped Zustand subscriptions via `useShallow` from `zustand/react/shallow`.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | VoiceStudio Granular Timeouts | Configure `httpx.Timeout(connect=0.15s, read=...)` to avoid Windows 2s TCP SYN retry | M2 | Survey 1 / Task Spec |
| 2 | VoiceStudio 30s Circuit Breaker | 30s monotonic circuit breaker in `VoiceStudioTTSService` (`_offline_until`) | M2 | Survey 1 / Task Spec |
| 3 | L1 Narrator Response Cache | Thread-safe 60s in-memory cache for `POST /api/broadcast/narrate` in `broadcast.py` | M2 | Survey 1 / Task Spec |
| 4 | Short-lived Threadpool DB Session | Run `build_fact_packet` in `run_in_threadpool`, close DB before awaiting network I/O | M2 | Survey 1 / Task Spec |
| 5 | Test Dependency Override Parity | `get_threadpool_db` respects `app.dependency_overrides[get_db]` in test fixtures | M2 | Survey 1 / Task Spec |
| 6 | Player Satellite noload("*") | Suppress 5 1:1 satellite tables (`attributes`, `contract`, `physics`, `injury`, `progression`) | M1 | Survey 2 / Task Spec |
| 7 | Season & SeasonHistory Consolidation | Deduplicate active/latest Season and champion/runner_up queries | M1 | Survey 2 / Task Spec |
| 8 | Eager Joined Loading (Facts) | Eagerly load `Team.season_history`, `Game` teams, `Player` stats and traits in <= 6 queries | M1 | Survey 2 / Task Spec |
| 9 | Storyline Read Path Purity | Remove `check_for_storyline_triggers` (RPGEvent query) from read-only fact gathering | M1 | Survey 2 / Task Spec |
| 10 | Season Cache-Aside Layer | Implement `backend/app/core/season_cache.py` L1 cache modeled after `roster_cache.py` | M3 | Survey 3 / Task Spec |
| 11 | Single-Pass Game Count Aggregation | Consolidate two `Game` count queries into single `CASE` aggregation in `season.py` | M3 | Survey 3 / Task Spec |
| 12 | Season & Narrator Invalidation Hooks | Purge season caches and narrator response cache in 8 simulation/advance endpoints | M3 | Survey 3 / Task Spec |
| 13 | Frontend Concurrent Loader | `seasonDashboardLoader` fetches concurrently and reuses `summary.standings` & `leaders` | M3 | Survey 3 / Task Spec |
| 14 | Season Type Contract Parity | Add `ConferenceStandings`, `DivisionStandings`, and full `SeasonSummary` in `types/season.ts` | M3 | Survey 3 / Task Spec |
| 15 | Dynamic html2canvas Import | Replace top-level `import html2canvas` with dynamic `await import("html2canvas")` | M4 | Survey 3 / Task Spec |
| 16 | Scoped Zustand Selector | Wrap `useNarratorStore` in `NarratorBar.tsx` with `useShallow` | M4 | Survey 3 / Task Spec |
| 17 | Performance SLA Verification | P95 < 25ms offline VoiceStudio, <= 6 SQL queries in `build_fact_packet` | M5 | Acceptance Criteria |
| 18 | Load Testing & Regression | Load test season summary & standings P95 < 300ms at concurrency 25, full pytest suite | M5 | Acceptance Criteria |
| 19 | Build, Lint & Playwright Verification | Frontend lint & build pass, Playwright `narrator.spec.ts` passes (2 passed), docs updated | M5 | Acceptance Criteria |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | NarratorFactsService ORM Query Consolidation (R2) | `backend/app/services/narrator_facts_service.py`, query budget test in `test_narrator_facts_*.py` | none | DONE |
| M2 | Fast-Fail VoiceStudio Client & Narrator Response Cache & DB Decoupling (R1 & R3) | `backend/app/services/voicestudio_tts_service.py`, `backend/app/api/endpoints/broadcast.py`, `test_voicestudio_tts.py`, `test_broadcast_narrator.py` | M1 | DONE |
| M3 | Season Cache-Aside, Single-Pass Aggregation & Router De-duplication (R4) | `backend/app/core/season_cache.py`, `backend/app/api/endpoints/season.py`, `frontend/src/router.tsx`, `frontend/src/types/season.ts` | M2 | DONE |
| M4 | Frontend Dynamic html2canvas Import & Scoped Zustand Selectors (R5) | `frontend/src/components/common/RegionSelector.tsx`, `frontend/src/components/audio/NarratorBar.tsx` | none | DONE |
| M5 | Master Verification, Load Testing & Forensic Integrity Audit | Run full test suite, mypy, load tests, frontend lint & build, Playwright E2E, auditor verification, update TASK-PERF-001.md | M1, M2, M3, M4 | DONE |

---

## Interface Contracts
### 1. `NarratorFactsService` ↔ `broadcast.py`
- Signature: `facts_service.build_fact_packet(payload: NarrationContextRequest) -> FactPacket`
- Guarantee: Output is a detached Pydantic `FactPacket` with zero attached ORM models or database dependencies.
- Query Budget: Maximum 6 SQL queries per execution under full franchise + player context.

### 2. `VoiceStudioTTSService` ↔ `broadcast.py`
- Methods:
  - `check_health(force: bool = False) -> bool`
  - `synthesize(script: str) -> bytes | None`
  - `is_circuit_open() -> bool`
  - `reset_circuit() -> None`
  - `trip_circuit() -> None`
- Guarantee: Loopback connect timeout strictly 0.15s. Negative circuit breaker trips for 30.0s on connection failure/timeout, returning in < 0.01ms on subsequent calls.

### 3. `broadcast.py` ↔ `season.py`
- Export: `clear_narrator_response_cache() -> None`
- Invalidation Trigger: Called by `season.py` when weeks are simulated or advanced.

### 4. `season_cache.py` ↔ `season.py`
- Interface:
  - `season_cache.get_summary(key: str = "active") -> str | None`
  - `season_cache.set_summary(serialized_json: str, key: str = "active", ttl: int | None = None) -> None`
  - `season_cache.get_standings(season_id: int, conference: str | None = None, division: str | None = None) -> str | None`
  - `season_cache.set_standings(...) -> None`
  - `invalidate_season_caches(season_id: int | None = None) -> None`
- Guarantee: Thread-safe in-memory L1 cache with monotonic TTL. `get_season_summary` and `get_standings` return fast `Response(content=cached_payload, media_type="application/json")`.

### 5. `backend/app/schemas/season.py` ↔ `frontend/src/types/season.ts`
- Schema parity:
  - `ConferenceStandings`: `{ conference: string; divisions: DivisionStandings[]; }`
  - `DivisionStandings`: `{ division: string; teams: TeamStanding[]; }`
  - `SeasonSummary`: includes `standings?: ConferenceStandings[] | null`, `league_leaders?: LeagueLeaders | null`, `playoff_bracket?: PlayoffMatchup[] | null`.

---

## Code Layout
### Backend Files Owned
- `backend/app/services/narrator_facts_service.py` (M1)
- `backend/tests/services/test_narrator_facts_player.py` (M1)
- `backend/app/services/voicestudio_tts_service.py` (M2)
- `backend/app/api/endpoints/broadcast.py` (M2)
- `backend/tests/services/test_voicestudio_tts.py` (M2)
- `backend/tests/api/test_broadcast_narrator.py` (M2)
- `backend/app/core/season_cache.py` (M3 - new file)
- `backend/app/api/endpoints/season.py` (M3)
- `backend/tests/test_season_summary.py` (M3)

### Frontend Files Owned
- `frontend/src/router.tsx` (M3)
- `frontend/src/types/season.ts` (M3)
- `frontend/src/components/common/RegionSelector.tsx` (M4)
- `frontend/src/components/audio/NarratorBar.tsx` (M4)

### Documentation & Verification Files Owned
- `docs/tasks/TASK-PERF-001.md` (M5)

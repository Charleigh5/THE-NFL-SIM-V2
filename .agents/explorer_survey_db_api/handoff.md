# Handoff Report: Database & API Architecture Deep Survey (R1 & R4)

**Agent:** Explorer 1 (Database & API Architecture Specialist)  
**Target:** THE-NFL-SIM-V2  
**Working Directory:** `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_db_api`  
**Date:** 2026-08-22  
**Scope:** R1 (Database Schema Consolidation & ORM Integrity) and R4 (Backend API Architecture, Concurrency & Security Hardening)

---

## 1. Observations

### 1.1 R1: Database Schema & ORM Integrity

#### Observation 1.1.1: Triple Declaration of `player_game_starts`
- **Location 1:** `backend/app/models/player_game_start.py` (lines 10–29)
  ```python
  class PlayerGameStart(Base):
      __tablename__ = 'player_game_starts'
      id = Column(Integer, primary_key=True, index=True)
      player_id = Column(Integer, ForeignKey('player.id'), nullable=False, index=True)
      game_id = Column(Integer, ForeignKey('game.id'), nullable=False, index=True)
      position = Column(Integer, nullable=False, index=True)
      started = Column(Boolean, default=True, nullable=False)
      created_at = Column(DateTime, default=datetime.utcnow)
  ```
- **Location 2:** `backend/app/models/player_game_starts.py` (lines 11–36)
  ```python
  class PlayerGameStarts(Base):
      __tablename__ = 'player_game_starts'
      id: Mapped[int] = mapped_column(primary_key=True)
      player_id: Mapped[int] = mapped_column(ForeignKey('player.id'), nullable=False)
      game_id: Mapped[int] = mapped_column(ForeignKey('game.id'), nullable=False)
      position_started: Mapped[str] = mapped_column(String(10), nullable=False)
      teammates_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
      created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
      player: Mapped["Player"] = relationship(back_populates="game_starts")
      game: Mapped["Game"] = relationship(back_populates="player_starts")
  ```
- **Location 3:** `backend/app/models/stats.py` (lines 63–71)
  ```python
  class PlayerGameStart(Base):
      __tablename__ = "player_game_starts"
      id = Column(Integer, primary_key=True, index=True)
      player_id = Column(Integer, ForeignKey("player.id"), index=True)
      game_id = Column(Integer, ForeignKey("game.id"), index=True)
      team_id = Column(Integer, ForeignKey("team.id"), index=True)
      season_id = Column(Integer, ForeignKey("season.id"), index=True)
      week = Column(Integer)
      position = Column(String)
  ```
- **Location 4:** Alembic migration `backend/alembic/versions/aa400ba86838_add_playergamestart_table.py` created the schema with columns: `id`, `player_id`, `game_id`, `team_id`, `season_id`, `week`, `position`.
- **Services Discrepancy:**
  - `backend/app/services/chemistry_service.py` (lines 10, 55, 172) imports `PlayerGameStarts` from `app.models.player_game_starts` and expects `teammates_hash` and `position_started`.
  - `backend/app/services/enhanced_chemistry_service.py` (line 15) and `backend/app/services/pre_game_service.py` (line 3) import `PlayerGameStart` from `app.models.stats` and expect `team_id`, `season_id`, `week`, `position`.
  - `backend/app/models/player.py` (line 707) binds `game_starts = relationship("PlayerGameStarts", back_populates="player")`.
  - `backend/app/models/game.py` (line 58) binds `player_starts = relationship("PlayerGameStarts", back_populates="game")`.

#### Observation 1.1.2: Missing Model Registrations in `alembic/env.py`
- **Location:** `backend/alembic/env.py` (lines 19–34)
  ```python
  from app.models.team import Team
  from app.models.player import Player
  from app.models.coach import Coach
  from app.models.gm import GM
  from app.models.game import Game
  from app.models.stats import PlayerGameStats
  from app.models.feedback import UserFeedback
  from app.models.trait import Trait, PlayerTrait
  from app.models.player_game_starts import PlayerGameStarts
  from app.models.player_attributes import PlayerAttributes
  from app.models.player_contract import PlayerContract
  from app.models.player_physics import PlayerPhysics
  from app.models.player_injury import PlayerInjury
  from app.models.player_progression import PlayerProgression
  ```
- **Omission:** 15+ models defined in `app/models/` are absent from `env.py`, including `Season`, `PlayoffMatchup`, `DepthChart`, `NewsItem`, `DraftPick`, `SeasonHistory`, `PlayerSeasonStats`, `TeamSeasonStats`, `TradeOffer`, `Scout`, `ScoutingReport`, `BodyPart`, `InjuryEvent`, `Gameplan`, `CoachingTree`, `WeeklyRecap`, `RPGEvent`, `HallOfFame`, `GMDecision`, `StadiumClimate`, and `GameWeather`. As a result, `Base.metadata` in Alembic does not contain their table definitions.
- **Model `__init__.py` Omission:** `backend/app/models/__init__.py` is missing exports for `HallOfFame`, `GMDecision`, and `Trait`.

#### Observation 1.1.3: `Player.traits` Relationship Attribute Crash
- **Location:** `backend/app/api/endpoints/players.py` (line 271)
  ```python
  stmt = select(Player).options(selectinload(Player.traits)).where(Player.id == player_id)
  ```
- **Definition in `Player`:** `backend/app/models/player.py` (line 552) defines:
  ```python
  player_traits: Mapped[List["PlayerTrait"]] = relationship("PlayerTrait", back_populates="player")
  ```
- **Error:** `Player` does not define `traits` as an attribute or relationship. Calling `Player.traits` raises:
  `AttributeError: type object 'Player' has no attribute 'traits'`.

#### Observation 1.1.4: `Player.speed` & RPG Hybrid Property Expression Missing
- **Location:** `backend/app/models/player.py` (lines 76–82, 91–96, 98–103, etc.)
  ```python
  @hybrid_property
  def speed(self) -> int:
      return self.attributes.speed if self.attributes else 50
  @speed.setter
  def speed(self, value):
      if self.attributes: self.attributes.speed = value
  ```
- **Query Context in `DraftAssistant`:** `backend/app/services/draft_assistant.py` (lines 70–79)
  ```python
  players_stmt = select(
      Player.id,
      Player.first_name,
      Player.last_name,
      Player.position,
      Player.overall_rating,
      Player.speed,
      Player.strength,
      Player.agility
  ).where(Player.id.in_(available_players))
  ```
- **Error:** When `Player.speed`, `Player.strength`, or `Player.agility` is passed to `select()` or `.where()`, SQLAlchemy evaluates the hybrid property at the class level without an `@<prop>.expression` subquery definition. Because `self.attributes` evaluates to `InstrumentedAttribute(Player.attributes)`, evaluating it in a boolean or SQL clause context raises a `TypeError` / returns an un-evaluatable `Comparator` object.

#### Observation 1.1.5: 1:1 Decomposition Relationships Missing Cascade and Using Joined Load
- **Location:** `backend/app/models/player.py` (lines 713–717)
  ```python
  attributes: Mapped["PlayerAttributes"] = relationship("PlayerAttributes", back_populates="player", uselist=False, lazy="joined")
  contract: Mapped["PlayerContract"] = relationship("PlayerContract", back_populates="player", uselist=False, lazy="joined")
  physics: Mapped["PlayerPhysics"] = relationship("PlayerPhysics", back_populates="player", uselist=False, lazy="joined")
  injury: Mapped["PlayerInjury"] = relationship("PlayerInjury", back_populates="player", uselist=False, lazy="joined")
  progression: Mapped["PlayerProgression"] = relationship("PlayerProgression", back_populates="player", uselist=False, lazy="joined")
  ```
- **Defects:**
  1. No `cascade="all, delete-orphan"`: Deleting a `Player` leaves orphaned rows or throws foreign key violations.
  2. `lazy="joined"`: Every player query performs 5 LEFT OUTER JOINs, creating Cartesian joined-load overhead on batch queries.

#### Observation 1.1.6: SQLite Engine Missing WAL Mode and Busy Timeout
- **Location:** `backend/app/core/database.py` (lines 41–53)
  ```python
  if is_sqlite:
      @event.listens_for(engine, "connect")
      def set_sqlite_pragma(dbapi_conn, connection_record):
          cursor = dbapi_conn.cursor()
          cursor.execute("PRAGMA foreign_keys=ON")
          cursor.close()

      @event.listens_for(async_engine.sync_engine, "connect")
      def set_sqlite_pragma_async(dbapi_conn, connection_record):
          cursor = dbapi_conn.cursor()
          cursor.execute("PRAGMA foreign_keys=ON")
          cursor.close()
  ```
- **Defects:**
  - `PRAGMA journal_mode=WAL;` is missing.
  - `PRAGMA busy_timeout=5000;` is missing.
  - `PRAGMA synchronous=NORMAL;` is missing.
  - Concurrent FastAPI requests produce `sqlite3.OperationalError: database is locked`.

---

### 1.2 R4: Backend API Architecture, Concurrency & Security

#### Observation 1.2.1: Orphaned & Disjoint Routers
- **`backend/app/api/endpoints/coaches.py`:** Defines `router = APIRouter(prefix="/api/coaches", tags=["coaches"])` with 8 complete endpoints (`/`, `/{coach_id}`, `/team/{team_id}`, `/hire`, `/fire`, `/carousel/available`, `/carousel/hot-seat`, `/tiers`). It is NEVER registered in `backend/app/core/setup.py`.
- **`backend/app/api/combine.py`:** Defines `router = APIRouter(prefix="/combine", tags=["Combine"])` with endpoints `/results` and `/genesis-reveal/{player_id}`. Located outside `endpoints/` and never included in `setup.py`.
- **`backend/app/api/news_router.py`:** Defines `router = APIRouter(prefix="/api/news", tags=["News & Recaps"])` with live database endpoints (`/feed`, `/items/{item_id}`, `/recap/{season_id}/{week}`, `/storylines`, `/categories`), while `backend/app/api/endpoints/news.py` is mounted in `setup.py` with mock news endpoints.
- **`backend/app/api/training.py`:** Defines `router = APIRouter(prefix="/training", tags=["Training"])` with `/drills`, `/execute`, and `/schedule` utilizing `TrainingEngine`, while `backend/app/api/endpoints/training.py` is partially mounted with conflicting stubs.

#### Observation 1.2.2: Blocking Synchronous DB Operations in `async def` Endpoints
- **Locations:**
  - `backend/app/api/endpoints/abilities.py` (lines 104, 115, 142, 163):
    `async def get_player_ability_status(player_id: int, db: Session = Depends(get_db)):`
  - `backend/app/api/endpoints/coaches.py` (lines 78, 87, 96, 117, 155, 175, 184):
    `async def get_team_coaches(team_id: int, db: Session = Depends(get_db)):`
  - `backend/app/api/endpoints/news.py` (lines 419, 457, 488, 513):
    `async def get_living_news_feed(..., db: Session = Depends(get_db)):`
  - `backend/app/api/endpoints/medical.py` (lines 26, 60, 87, 182, 219):
    `async def get_player_health(..., db: Session = Depends(get_db)):`
  - `backend/app/api/endpoints/gameplans.py` (lines 22, 40):
    `async def install_gameplan(..., db: Session = Depends(get_db)):`
- **Defect:** In FastAPI, declaring an endpoint as `async def` runs it on the main asyncio thread. Calling synchronous blocking SQLAlchemy `Session` operations (`db.query(...)`, `db.commit()`) blocks the entire asyncio event loop for all concurrent users.

#### Observation 1.2.3: Duplicate Session Acquisition in `season.py`
- **Location:** `backend/app/api/endpoints/season.py` (lines 771, 787, 801, 815, 831, 842, 853, 867, 879, 895, 927)
  ```python
  @router.post("/{season_id}/offseason/progression", response_model=List[PlayerProgressionResult])
  @handle_errors
  async def simulate_player_progression(season_id: int, db: AsyncSession = Depends(get_async_db)):
      def progression_sync():
          with SessionLocal() as sync_db:
              service = OffseasonService(sync_db)
              return service.simulate_player_progression(season_id)
      return await run_in_threadpool(progression_sync)
  ```
- **Defect:** The route injects `db: AsyncSession = Depends(get_async_db)` which opens an asynchronous connection from `async_engine`, but then never uses it, instead opening a second synchronous connection `with SessionLocal() as sync_db:`. Every single API request consumes two database connections simultaneously.

#### Observation 1.2.4: Fractured & Non-Thread-Safe WebSocket Implementations
- **Location 1:** `backend/app/api/endpoints/websocket.py` (lines 11–47)
  Uses a single un-isolated list `self.active_connections: List[WebSocket] = []` for all games. No room isolation, no locks.
- **Location 2:** `backend/app/api/endpoints/live_visualization.py` (lines 26–58)
  Uses `self.active_connections: Dict[str, List[WebSocket]] = {}`.
  Broadcasts sequentially iterate and `await connection.send_json(message)` with no `asyncio.Lock()`, no backpressure timeout, and no task fanout (`asyncio.gather`). A single slow or stalled client blocks updates to all other clients watching that game.

#### Observation 1.2.5: Plaintext Vertex API Key in `.env.example`
- **Location:** `backend/.env.example` (line 36)
  ```ini
  VERTEX_API_KEY=AQ.Ab8RN6JS3N_cUKCzzIsRDeYAXDaw0PJHf5tg9AJQXrUeIIVkZw
  ```
- **Defect:** A real plaintext API credential is committed to the version-controlled template file.

#### Observation 1.2.6: Unauthenticated Database Reset/Seed Endpoint
- **Location:** `backend/app/api/endpoints/genesis.py` (lines 88–105)
  ```python
  @router.post("/seed")
  @handle_errors
  def seed_database(db: Session = Depends(get_db)):
      from app.core.seed import seed_teams, seed_players
      from app.models.season import Season
      seed_teams(db)
      seed_players(db)
      db.query(Season).update({Season.is_active: False})
      db.commit()
      return {"message": "Database seeded successfully"}
  ```
- **Defect:** Anyone can send an unauthenticated HTTP POST request to `/api/genesis/seed` and deactivate all active seasons and mutate player/team rosters.

#### Observation 1.2.7: Raw Database Exception & Disk Debug Leaks
- **Location 1:** `backend/app/core/error_handlers.py` (lines 27, 47)
  ```python
  value=str(exc.orig) if hasattr(exc, 'orig') else str(exc)
  ```
  Returns internal database driver errors and SQL dialect strings directly to API clients.
- **Location 2:** `backend/app/core/error_decorators.py` (lines 124–129)
  ```python
  with open("debug_error.txt", "a") as f:
      f.write(f"DEBUG EXCEPTION: {type(e).__name__}: {e}\n")
      traceback.print_exc(file=f)
  ```
  Synchronous unbuffered disk I/O on every unhandled exception in request handlers.

---

## 2. Logic Chain

### 2.1 Database & ORM Integrity Logic
1. **Schema Collision (Obs 1.1.1):** Having three competing classes (`PlayerGameStart` in `player_game_start.py`, `PlayerGameStarts` in `player_game_starts.py`, and `PlayerGameStart` in `stats.py`) mapping to `__tablename__ = 'player_game_starts'` with divergent column sets (`teammates_hash` vs `team_id`/`season_id`/`week`) creates import ambiguity, relationship mapping failures in `Player` and `Game`, and query failures in chemistry services.
   $\rightarrow$ *Resolution:* Consolidate into canonical `backend/app/models/player_game_starts.py` class `PlayerGameStarts` supporting all required fields (`id`, `player_id`, `game_id`, `team_id`, `season_id`, `week`, `position`, `teammates_hash`, `created_at`), remove `PlayerGameStart` from `stats.py`, delete `player_game_start.py`, and unify service imports.
2. **Alembic Incompleteness (Obs 1.1.2):** `alembic/env.py` manually lists 14 models. The remaining 15+ models (`Season`, `PlayoffMatchup`, `DepthChart`, etc.) are never imported into Alembic's namespace. Therefore, `target_metadata = Base.metadata` does not contain them, making `alembic check` or autogenerate create duplicate or missing migration operations.
   $\rightarrow$ *Resolution:* Import `app.models` in `env.py` and register all models in `backend/app/models/__init__.py`.
3. **Player Profile Crash (Obs 1.1.3):** `GET /api/players/{player_id}/profile` executes `selectinload(Player.traits)`. Because the ORM relationship on `Player` is `player_traits`, Python raises `AttributeError` at runtime before the query executes.
   $\rightarrow$ *Resolution:* Change to `selectinload(Player.player_traits).joinedload(PlayerTrait.trait)`.
4. **DraftAssistant Crash (Obs 1.1.4):** Querying `select(Player.speed)` treats `Player.speed` as a column element. Without `@speed.expression` on `Player`, SQLAlchemy evaluates the python getter where `self.attributes` is an ORM descriptor, causing a `Comparator` failure.
   $\rightarrow$ *Resolution:* Provide `@<prop>.expression` scalar subqueries for all proxied hybrid properties.
5. **Cascades & Join Overhead (Obs 1.1.5):** 1:1 decomposition relationships default to `lazy="joined"` and lack `cascade="all, delete-orphan"`.
   $\rightarrow$ *Resolution:* Add `cascade="all, delete-orphan"` and switch to `lazy="selectin"`.
6. **SQLite Locking (Obs 1.1.6):** Without `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;`, SQLite acquires exclusive file locks during write transactions, causing immediate 500 errors on concurrent requests.
   $\rightarrow$ *Resolution:* Add connection listeners setting WAL mode and 5000ms busy timeout on both sync and async engines.

### 2.2 API Architecture & Security Logic
1. **Orphaned Routes (Obs 1.2.1):** Clients calling `/api/coaches`, `/api/combine`, `/api/news/feed`, and `/api/training` receive 404 Not Found because the router modules were never mounted in `setup.py`.
   $\rightarrow$ *Resolution:* Register `coaches.router`, `combine.router`, consolidated `news_router`, and `training_router` in `setup.py`.
2. **Event Loop Starvation (Obs 1.2.2):** `async def` endpoints executing blocking sync DB queries starve the event loop.
   $\rightarrow$ *Resolution:* Change synchronous endpoints from `async def` to `def` (allowing FastAPI's worker threadpool to handle them) or migrate them to `AsyncSession`.
3. **Double Session Waste (Obs 1.2.3):** Endpoints declaring `db: AsyncSession = Depends(get_async_db)` while using `with SessionLocal() as sync_db:` double connection allocation.
   $\rightarrow$ *Resolution:* Remove unused `db: AsyncSession` parameter on sync threadpool endpoints.
4. **WebSocket Blocking & Isolation (Obs 1.2.4):** Global un-isolated connection lists leak game events across matches, and un-gated sequential broadcast loops block all clients when one client has network lag.
   $\rightarrow$ *Resolution:* Unify into a room-isolated `ChannelConnectionManager` with per-game rooms, `asyncio.Lock()`, and `asyncio.wait_for(timeout=2.0)` / task fanout.
5. **Credential Exposure (Obs 1.2.5):** Git-tracked plaintext API keys risk unauthorized cloud billing and quota compromise.
   $\rightarrow$ *Resolution:* Scrub `.env.example` and replace with a standard placeholder.
6. **Administrative Security (Obs 1.2.6 & Obs 1.2.7):** Unauthenticated state-mutation endpoints and detailed SQL error disclosure expose administrative controls and database structure.
   $\rightarrow$ *Resolution:* Add admin guard to `/api/genesis/seed`, sanitize JSON error payloads, and remove synchronous debug file writes.

---

## 3. Caveats

1. **Active Data Migration:** If an existing SQLite database file has legacy `player_game_starts` data created by migration `aa400ba86838`, unifying the model columns (`teammates_hash`, `season_id`, `team_id`, `week`, `position`) will require either running the consolidated model or ensuring backward-compatible nullable columns.
2. **Sync vs Async Service Ecosystem:** Several services (`OffseasonService`, `FreeAgencyEngine`, `DraftAssistant`, `PlayoffService`, `GMAgent`) are written synchronously using `sqlalchemy.orm.Session`. The cleanest surgical fix is keeping them on `def` endpoints or `run_in_threadpool`, rather than attempting a high-risk full async rewrite of the entire service layer.
3. **Firebase Token Dependency:** In development mode without active Firebase service credentials, admin guards must gracefully permit local development while rejecting unauthorized remote production requests.

---

## 4. Conclusion & Recommended Surgical Fix Strategy

The database and API architecture requires surgical remediation across 8 core target areas:

| Target Component | Target File(s) | Specific Remediation |
|---|---|---|
| **1. Canonical `PlayerGameStarts`** | `backend/app/models/player_game_starts.py`, `stats.py`, `player_game_start.py` | Consolidate all fields (`id`, `player_id`, `game_id`, `team_id`, `season_id`, `week`, `position`, `teammates_hash`, `created_at`) into `player_game_starts.py`. Delete `player_game_start.py`. Remove `PlayerGameStart` from `stats.py`. Update service imports. |
| **2. Alembic Model Discovery** | `backend/alembic/env.py`, `backend/app/models/__init__.py` | In `env.py`, replace manual 14-model import with `import app.models`. Export `HallOfFame`, `GMDecision`, and `Trait` in `__init__.py`. |
| **3. Player Profile Trait Loader** | `backend/app/api/endpoints/players.py:271` | Replace `selectinload(Player.traits)` with `selectinload(Player.player_traits).joinedload(PlayerTrait.trait)`. |
| **4. Hybrid Property Expressions** | `backend/app/models/player.py` | Add `@<prop>.expression` subqueries for `speed`, `strength`, `agility`, `acceleration`, `awareness`, etc., proxying to `PlayerAttributes`. |
| **5. Player Decomposition Cascades** | `backend/app/models/player.py:713-717` | Add `cascade="all, delete-orphan"` and `lazy="selectin"` to `attributes`, `contract`, `physics`, `injury`, `progression`. |
| **6. SQLite WAL Pragmas** | `backend/app/core/database.py:41-53` | Add `PRAGMA journal_mode=WAL;` and `PRAGMA busy_timeout=5000;` on engine connect. |
| **7. API Router Mounting & Cleanup** | `backend/app/core/setup.py`, `backend/app/api/` | Mount `coaches.router`, `combine.router`, consolidated `news_router`, and `training_router`. Remove orphaned/conflicting duplicate files. |
| **8. Concurrency, Security & Error Sanitization** | `backend/app/api/endpoints/season.py`, `websocket.py`, `live_visualization.py`, `genesis.py`, `error_handlers.py`, `error_decorators.py`, `backend/.env.example` | Convert sync `async def` endpoints to `def`. Remove duplicate `db: AsyncSession` acquisition in `season.py`. Unify WebSocket managers into a room-isolated, lock-protected manager. Add admin guard to `/api/genesis/seed`. Scrub API key from `.env.example`. Sanitize error JSON responses. |

---

## 5. Verification Method

### 5.1 Static Analysis & Schema Checks
1. **Alembic Autogenerate Discovery:**
   ```bash
   cd backend
   alembic check
   ```
   *Pass Condition:* All tables (`season`, `playoff_matchups`, `depth_charts`, `news_items`, `traits`, `player_game_starts`, etc.) are recognized in `Base.metadata`.

2. **Model Import Validation:**
   ```python
   from app.models import Base, Player, Game, Season, PlayerGameStarts, DepthChart, NewsItem
   assert "player_game_starts" in Base.metadata.tables
   assert "season" in Base.metadata.tables
   ```

### 5.2 Unit & Integration Tests
1. **Player Profile Endpoint Verification:**
   ```bash
   pytest backend/tests/test_api_verification.py -k "test_player_profile"
   ```
   *Pass Condition:* `GET /api/players/{player_id}/profile` returns HTTP 200 without `AttributeError` on `Player.traits`.

2. **Draft Assistant Hybrid Expression Verification:**
   ```bash
   pytest backend/tests/ -k "test_draft_assistant or test_suggest_pick"
   ```
   *Pass Condition:* `select(Player.speed, Player.strength)` executes cleanly without `Comparator` exception.

3. **Orphaned API Route Resolution:**
   ```bash
   pytest backend/tests/ -k "test_coaches or test_combine or test_news or test_training"
   ```
   *Pass Condition:* `/api/coaches`, `/api/combine/results`, `/api/news/feed`, and `/api/training/drills` return valid HTTP 200 JSON responses.

4. **Secret Scanning Verification:**
   ```bash
   git grep "AQ.Ab8RN6JS3N"
   ```
   *Pass Condition:* Zero occurrences across all files.

5. **Concurrency & WAL Mode Verification:**
   Execute 50 concurrent requests against SQLite test database; verify zero `OperationalError: database is locked`.

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-036_REAL_TIME_ROSTER_SYNC_AND_API_INTEGRATION

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Professional sports simulation engines (such as Football Manager or OOTP) either operate in an isolated sandbox or provide live roster synchronization services to mirror real-world trades, cuts, free-agent moves, depth charts, and injury reports.
- **Related Ideas:** 
  - Provider Adapter Pattern: Abstracting heterogeneous external APIs (Tank01 via RapidAPI, SportsDataIO, Sleeper, ESPN) behind a unified domain interface.
  - Event-Driven Reconciler: Detecting delta changes between external snapshots and internal relational models, emitting events to the living league narrative (`NewsFeedService`).
  - Safe Differential Merging: Preserving in-flight game records, user-customized player attributes, and draft histories without destructive database re-seeding.
- **Future Potential:** Future capability to subscribe to real-time WebSockets or serverless push webhooks for instant in-game updates during Sunday game windows.
- **Constraints:**
  - Zero DB corruption: Foreign key integrity must be respected.
  - Non-destructive: Do not drop existing active players or wipe player stats.
  - Zero-key resilience: Must function out of the box using free community sources (`nflverse` / public ESPN) when no commercial API keys are present.
  - Security: Never expose or leak raw API keys in client responses or telemetry logs.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
A straightforward script that queries an external API (like Tank01 or SportsDataIO), truncates the `player` table, and repopulates all players from scratch with the latest data.

### Powerful Antithesis
Truncating the player table catastrophically breaks the simulation:
1. It deletes foreign-key-dependent records (`player_stats`, `player_contract`, `player_injury`, `depthchart`).
2. It wipes user career progressions, custom traits, and team cap ledgers midway through a season.
3. If the external API fails mid-fetch or encounters a rate limit (e.g., Tank01's 1,000 req/mo cap), the database is left completely empty and broken.
4. Hardcoding a specific commercial provider breaks local development for users without a paid subscription.

### The Superior Synthesis
A **Non-Destructive Differential Sync Engine** operating through a **Provider Adapter Strategy**:
1. **Configurable Provider via `.env`**: Supports `RAPIDAPI_KEY` (Tank01) and `SPORTSDATAIO_API_KEY` while gracefully defaulting to a zero-key fallback (`NflverseFreeProvider` + ESPN wire).
2. **Entity Matching & Differential Reconciler**: Matches external players by `gsis_id` (or normalized composite key) and only updates dirty fields (`team_id`, `depthchart.rank`, `injury_status`).
3. **Transaction Emission**: Real-world trades and cuts emit `EventType.TRADE_COMPLETED` through `EventBus`, automatically informing the `NewsFeedService` and updating the salary cap ledger.
4. **Dry-Run Mode**: Allows users to preview incoming trades and depth chart adjustments before applying them to the live database.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** FastAPI, Pydantic v2 Settings, SQLAlchemy 2.0, HTTPX
- **Language:** Python 3.12+ (Strict typing)
- **Design Patterns:** Provider Strategy Pattern, Factory Pattern, Unit of Work Reconciler

### 2. The Data Schema (Pre-Generation)
```python
class RosterPlayerDTO(BaseModel):
    gsis_id: Optional[str]
    first_name: str
    last_name: str
    position: str
    team_abbr: str
    jersey_number: Optional[int]
    status: str  # ACTIVE, INJURED_RESERVE, PRACTICE_SQUAD, SUSPENDED
    depth_order: Optional[int]
    injury_designation: Optional[str]

class SyncResultDTO(BaseModel):
    provider: str
    timestamp: datetime
    transfers_count: int
    depth_updates_count: int
    injuries_count: int
    unmatched_count: int
    transfers: List[Dict[str, Any]]
    depth_updates: List[Dict[str, Any]]
    injuries: List[Dict[str, Any]]
    dry_run: bool
```

### 3. Step-by-Step Execution
- [x] **Step 1: Configuration & `.env` Support.** Add `RAPIDAPI_KEY`, `RAPIDAPI_HOST`, `SPORTSDATAIO_API_KEY`, and `ROSTER_SYNC_PROVIDER` to `backend/app/core/config.py` and `backend/.env.example`.
- [x] **Step 2: Provider Abstraction Layer.** Create `BaseRosterProvider` interface and DTOs in `backend/app/services/roster_sync/base.py`.
- [x] **Step 3: Tank01 Provider.** Implement RapidAPI client in `backend/app/services/roster_sync/tank01_provider.py`.
- [x] **Step 4: SportsDataIO Provider.** Implement commercial client in `backend/app/services/roster_sync/sportsdataio_provider.py`.
- [x] **Step 5: Zero-Key Fallback Provider.** Implement free fallback in `backend/app/services/roster_sync/nflverse_provider.py`.
- [x] **Step 6: Provider Factory.** Implement dynamic factory in `backend/app/services/roster_sync/factory.py`.
- [x] **Step 7: Differential Sync Reconciler.** Implement `RosterSyncService` in `backend/app/services/roster_sync/sync_engine.py` with dry-run support and event emission.
- [x] **Step 8: REST Endpoints.** Add `/api/roster-sync/status` and `/api/roster-sync/execute` in `backend/app/api/endpoints/roster_sync.py` and register in `backend/app/core/setup.py`.
- [x] **Step 9: Frontend Sync Control.** Add TypeScript service methods in `frontend/src/services/rosterSyncApi.ts` and `LiveRosterSyncCard` component in the Front Office (`FrontOffice.tsx`).
- [x] **Step 10: Automated Tests.** Implement unit tests in `backend/tests/unit/test_roster_sync.py` and verify zero regressions (`468 passed`).

### 4. Edge Cases & Error Handling
- [Missing API Key] -> [Fallback gracefully to zero-key provider]
- [External API Timeout / 429 Rate Limit] -> [Catch `httpx.HTTPStatusError`, return clean structured error message, avoid corrupting DB state]
- [Unmatched Player in DB] -> [Log to unmatched list, do not halt sync pipeline]
- [Dry Run] -> [Calculate all diffs, generate report, rollback transaction]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** Strict Python type annotations across all new services and DTOs.
- [ ] **Security:** API keys masked in REST output (`****abcd`), zero secret leakage.
- [ ] **Performance:** Bulk query existing players in $O(1)$ memory map before diffing.
- [ ] **Self-Critique:** Does this interfere with existing franchise seasons? No, only changes dirty fields and maintains foreign key constraints.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Review and approve the implementation plan to begin Step 1 (Configuration & Provider Abstraction).
</baton_handoff>

# Phase Completion Plan: "The Wiring"

**Objective:** Transition the application from a "Simulator with a Facade UI" to a fully integrated, data-driven experience.
**Priority:** P0 (Critical Connectivity)

---

## 1. Frontend Wiring (Replacing Mocks)

### 1.1. Draft Room Integration (`frontend/src/pages/DraftRoom.tsx`)
**Current State:** `draftRoomLoader` returns hardcoded Cardinals/Falcons data.
**Action Items:**
1.  **Update API Service:** Ensure `frontend/src/services/api.ts` has endpoints for `getDraftState(seasonId)`, `getDraftPool()`, and `makePick()`.
2.  **Rewrite Loader:** Modify `draftRoomLoader` in `router.tsx` to fetch `getDraftState` from the API.
3.  **Connect UI Components:**
    - Update `DraftBoard` to map real player data from the API response.
    - Wire the "Draft Player" button to call `api.makePick`.
4.  **Handle Fallback:** If `DraftAssistant` (MCP) is offline, ensure the "Reasoning" text box falls back to "AI analysis unavailable" rather than crashing or showing Lorem Ipsum.

### 1.2. Live Simulation Connectivity (`frontend/src/pages/LiveSim.tsx`)
**Current State:** Uses `generateMockPlay()` loop.
**Action Items:**
1.  **WebSocket Hook:** Verify `useWebSocket` hook connects to `ws://localhost:8000/ws/simulation/live`.
2.  **State Consumption:**
    - Replace `mockTrajectory` with `gameState.currentPlay` from the Zustand store (`useSimulationStore`).
    - Ensure `FieldCanvas` renders the *real* `gameState` frame data.
3.  **Control Wiring:** Connect "Start/Stop" buttons to `simulationService.startLiveSimulation()` and `simulationService.stopSimulation()`.

### 1.3. Trade Center (`frontend/src/pages/TradeCenterPage.tsx`)
**Current State:** Mocks pending offers because endpoints are "undefined".
**Action Items:**
1.  **Define Endpoints:** Create `POST /api/trades/offer` and `GET /api/trades/pending` in the backend (`backend/app/api/endpoints/trade.py`).
2.  **Update Frontend Service:** Rewrite `tradeApi.ts` to call these real endpoints.
3.  **Remove Mocks:** Delete the random offer generator in `TradeCenterPage`.

---

## 2. Notification System (The Missing Layer)

**Objective:** Visualize the RPG events (Level Ups, Traits) happening in the backend.
**Action Items:**
1.  **Create Store:** Create `frontend/src/store/useNotificationStore.ts`.
    - State: `notifications: Array<{ id, type, message, icon, duration }>`
    - Actions: `addNotification`, `removeNotification`.
2.  **Create Component:** Create `frontend/src/components/overlay/GlobalNotificationLayer.tsx`.
    - Use `AnimatePresence` (framer-motion) or simple CSS transitions.
    - Overlay on top of `MainLayout`.
3.  **Connect to WebSocket:** Update `useWebSocket` to listen for specific event types (`PLAYER_LEVEL_UP`, `TRAIT_UNLOCK`, `TRADE_OFFER`) and dispatch to `useNotificationStore`.

---

## 3. Backend Logic Integration

### 3.1. Strategy Engine Hook
**Current State:** `StrategyEngine` exists but is unused in resolution.
**Action Items:**
1.  **Modify `PlayResolver`:** In `resolve_play()`:
    ```python
    # Calculate Strategy Multiplier
    strat_mult = self.strategy_engine.get_schematic_multiplier(
        command.play_type,
        match_context.defensive_scheme
    )
    # Apply to probability
    base_probability *= strat_mult
    ```

### 3.2. Injury Persistence
**Current State:** Injuries calculated post-play.
**Action Items:**
1.  **Update Match Context:** Ensure `evaluate_post_play_injuries` updates the `MatchContext.roster` status (e.g., `player.status = 'INJURED'`).
2.  **Enforce Substitutions:** In `SimulationOrchestrator.prepare_next_play()`, check if the active QB/RB is injured and auto-substitute them before the next command is generated.

---

## 4. Data Refinement & Cleanup

### 4.1. Seeding Configuration
**Action Items:**
1.  **Documentation:** Add a `docs/DATA_SEEDING_GUIDE.md` explaining how to run `SEED_MODE=REAL_2025`.
2.  **Default Config:** Set `SEED_MODE=REAL_2024` as the default in `.env.example` so new devs get real players, not random ones.

### 4.2. Code Cleanup
**Action Items:**
1.  **Remove Legacy Traits:** Delete `backend/app/rpg/traits.py` (marked deprecated) to prevent confusion.
2.  **Remove Frontend Mocks:** Delete `generateMockPlay` from `LiveSim.tsx` once wired.

---

**Next Steps:**
1.  Approve this plan.
2.  Begin execution with Section 1 (Frontend Wiring).

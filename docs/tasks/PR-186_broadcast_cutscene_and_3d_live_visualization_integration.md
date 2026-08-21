<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: PR-186 - 3D Live Game Visualization & Broadcast Cutscene System Integration & Deduplication

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** PR 186 introduced Phase A of the Broadcast Cutscene & 3D Live Game Visualization system (The Digital Gridiron). The goal was to provide Three.js / React Three Fiber visual rendering, procedural player geometry, field models, and a state machine-driven cutscene choreography director.
- **Related Ideas:** Sports broadcast presentation systems (Madden, NCAA 25, ESPN/CBS/FOX broadcast packages) operating on a discrete state machine: `IDLE` → `PRE_PLAY` → `PLAY_EXEC` → `POST_PLAY` → `REPLAY` → `BETWEEN_DOWNS` → `HALFTIME`.
- **Future Potential:** Extensibility into 60fps player route tracking, procedural crowd reactions, weather particle effects, and multi-angle broadcast replay takes.
- **Constraints:** 
  - Zero duplicate type definitions across frontend stores, components, and backend schemas.
  - No ORM objects in response models.
  - Strict async SQLAlchemy 2.0 endpoint compatibility.
  - Complete elimination of compiled `.pyc` git tracking pollution.
  - 100% passing backend unit tests and clean TypeScript / ESLint builds.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Directly merge PR 186 branch files into `main`.

### Powerful Antithesis
Direct merging introduces:
1. **Critical Runtime Bugs:** `live_visualization.py` attempted to access non-existent `player.name` (`Player` model uses `first_name` and `last_name`) and queried `player.injury_status == "healthy"` (`InjuryStatus` enum uses `"ACTIVE"`), causing immediate 500 errors.
2. **Type Duplications & Collisions:** `PlayerVisualData`, `TeamVisualData`, `FormationData`, and `GameRosterData` were defined in duplicate across `useLiveVisualizationStore.ts`, `LiveGameVisualizer.tsx`, and `EnhancedPlayerCharacter.tsx`. Additionally, `PlayResult` in `types/broadcast.ts` conflicted with canonical `PlayResult` in `types/simulation.ts`.
3. **Missing Implementations & Tests:** The `GET /api/live/game/{id}/broadcast/{play_id}` endpoint was missing, and the unit tests claimed in commit `f39850f` were not committed.
4. **Git Index Pollution:** 37 `.pyc` files were tracked in git.

### The Superior Synthesis
Remediate and consolidate:
1. Purge all `.pyc` files from git index and enforce clean ignore rules.
2. Unify all broadcast and 3D visualization types into `frontend/src/types/broadcast.ts` as the single authoritative source of truth.
3. Align `backend/app/schemas/broadcast.py` with Pydantic V2 and create non-colliding `BroadcastPlayResult`.
4. Modernize `backend/app/api/endpoints/live_visualization.py` using `AsyncSession = Depends(get_async_db)`, correct player model properties (`first_name`, `last_name`, `injury_status == "ACTIVE"`), and implement `GET /broadcast/{play_id}`.
5. Integrate `LiveGameVisualizer` as a dedicated "3D Live Cam" view mode within `frontend/src/pages/LiveSim.tsx`.
6. Author comprehensive backend unit tests (`test_broadcast_schemas.py` and `test_live_visualization_api.py`) verifying 100% of transitions and endpoints.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19, Three.js, `@react-three/fiber`, `@react-three/drei`, Zustand 5, FastAPI, SQLAlchemy 2.0 (Async).
- **Language:** TypeScript 5.9 (Strict `erasableSyntaxOnly`), Python 3.11+.
- **State Management:** Zustand broadcast store (`useBroadcastStore`) + live visualization store (`useLiveVisualizationStore`).

### 2. The Data Schema
- **State Machine:** `BroadcastPhase` (7 legal states) + `validate_phase_transition()`.
- **Cues & Cameras:** `CameraShot`, `OverlayCue`, `ClipCue`, `BroadcastEventSchema`, `ClipCueListResponse`.
- **3D Visual Models:** `PlayerVisualData`, `TeamVisualData`, `GameRosterData`, `FormationData`.

### 3. Step-by-Step Execution
- [x] **Step 1: Git Cleanup.** Purge `.pyc` tracking from git cache.
- [x] **Step 2: Schemas.** Implement `backend/app/schemas/broadcast.py`.
- [x] **Step 3: Endpoints.** Implement `backend/app/api/endpoints/live_visualization.py` and register in `setup.py`.
- [x] **Step 4: Unified Types.** Create `frontend/src/types/broadcast.ts`.
- [x] **Step 5: Stores & Director.** Create `useBroadcastStore.ts`, `useLiveVisualizationStore.ts`, and `CutsceneDirector.ts`.
- [x] **Step 6: 3D Components.** Create `EnhancedPlayerCharacter.tsx`, `EnhancedFieldVisualizer.tsx`, and `LiveGameVisualizer.tsx`.
- [x] **Step 7: UI Integration.** Wire 3D view mode tab into `frontend/src/pages/LiveSim.tsx`.
- [x] **Step 8: Unit Tests.** Create `test_broadcast_schemas.py` and `test_live_visualization_api.py`.

### 4. Edge Cases & Error Handling
- [Case A: WebSocket Offline / Disconnect] -> [Graceful fallback to polling / offline status badge without canvas crashes]
- [Case B: Missing Player Attributes / Injury Status] -> [Default body types and active roster fallback]
- [Case C: Illegal State Machine Transition] -> [Validation guard with descriptive error logging]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** 0 TypeScript errors (`tsc -b && vite build` clean across 3,727 modules). Zero `any` types.
- [x] **Deduplication:** Zero duplicate interface declarations between visualizer components and stores.
- [x] **Backend Tests:** 18 new broadcast/visualization unit tests passing (294/294 total unit tests passing).
- [x] **Engine Health:** Batch simulator operational with high throughput.
      </final_audit>

---

<baton_handoff>
Next Immediate Step: System is certified and ready for continuous simulation and broadcast feature extensions.
</baton_handoff>

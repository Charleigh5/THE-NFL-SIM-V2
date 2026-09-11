# Comprehensive Technical Survey & Systems Audit Report
**Workspace:** THE-NFL-SIM-V2 ("The Digital Gridiron")  
**Agent:** `teamwork_preview_explorer_survey_5p_3` (Track 4 Focus: QA, Harnesses, Calibration, ADRs & Living Dossiers)  
**Date:** 2026-09-06T03:35:00Z  
**Audit Scope:** Static Contract Verification, Frontend Compilation/Strict Typing, Cross-Domain Boundary Continuity, Latency Budgets/Harnesses, Monte Carlo Statistical Calibration, Architectural Records & Living Dossiers.

---

## Executive Summary

This survey report delivers an authoritative, empirical investigation into the testing, contract integrity, operational performance, statistical fidelity, and living architectural documentation across THE-NFL-SIM-V2. All findings are derived directly from code execution, compiler passes, AST inspections, and filesystem audits.

### Core Metrics & Health Matrix

| Audit Domain | Target / Requirement | Observed Status | Verdict |
| :--- | :--- | :--- | :--- |
| **Blueprint Contract Verification** | Zero schema errors in markdown design contracts | 4/4 files parsed, 39 Pydantic models validated, strict `tsc` passed | **PASS** (100%) |
| **Field & Enum Parity** | 1:1 parity between Python models and TypeScript interfaces | 21/21 master domain models match, 7/7 enums identical | **PASS** (100%) |
| **Frontend Production Build** | `npm --prefix frontend run build` (`tsc -b && vite build`) | 3,756 modules transformed, zero TS errors, built in 23.25s | **PASS** (100%) |
| **Frontend Any-Type Strictness** | Zero `any` types in `frontend/src/` | 0 occurrences in executable code (11 occurrences in comments only) | **PASS** (100%) |
| **Cross-Domain Pipeline** | Physics -> Broadcast -> Medical -> WebSocket Frame | 5 domain transitions validated with zero data loss or typing drift | **PASS** (100%) |
| **Monte Carlo Calibration** | 100 games aligned with NFL statistical distribution bounds | Sack 6.72%, YPC 3.99, Comp 66.83%, TO 0.96, PPG 24.32 | **PASS** (100%) |
| **FastR Statistical Validation** | 1,000 plays against nflfastR ground truth distributions | YPC 4.35, Comp 64.0%, Sack 7.17%, INT 2.22%, Yds/C 12.2 | **PASS** (100%) |
| **Latency Benchmark Harness** | Subsystems tested against <16ms, <40ms, <2ms budgets | MCP server tool tested (P95 <500ms); specific budget suite missing | **GAP IDENTIFIED** |
| **Architecture Records (ADRs)** | ADR coverage for major design decisions | ADR-001..004 present; ADR-005..008 missing for sprint modules | **GAP IDENTIFIED** |
| **Feature Status Matrix** | Living matrix tracks all modules and sprint tasks | 132 features tracked; TASK-010..013 entries missing | **GAP IDENTIFIED** |
| **Player System Dossier** | Living dossier tracks contract capology & injury states | 1,210 lines tracked; needs sync with advanced proration & triage | **GAP IDENTIFIED** |

---

## 1. Static Contract Verification Tools

### 1.1 `scripts/verify_blueprint_contracts.py`
- **File Location:** `scripts/verify_blueprint_contracts.py` (109 lines)
- **Target Specifications:** Markdown files in `docs/design_theory/nfl_simulation_blueprint/`:
  1. `physics_engine.md`
  2. `dynasty_empire.md`
  3. `broadcast_director.md`
  4. `ui_design_system.md`
- **Verification Logic & Mechanics:**
  - **Code Block Extraction:** Uses regular expression `r"```(\w+)?
(.*?)```"` to isolate Python and TypeScript code snippets embedded inside architecture documents.
  - **Python Model Execution:** Dynamic execution via `exec(code, ns)` within an isolated dictionary namespace. Filters instances inheriting from Pydantic `BaseModel` possessing `model_fields`. Asserts that all models execute without import failures, schema errors, or missing type references.
  - **TypeScript Compilation:** Writes extracted code to temporary `.ts` files with DOM standard library injection (`/// <reference lib="dom" />`). Executes the official TypeScript compiler:
    `node frontend/node_modules/typescript/bin/tsc --strict --noEmit --target es2022 --lib es2022,dom <tempfile>`
  - **Strict `any` Enforcement:** Scans every line of TypeScript code, stripping single-line comments (`//.*$`) and multi-line comment blocks (`/* ... */`), checking for illegal occurrences of `any` (`: any`, `as any`, `<any>`, `Array<any>`, `Promise<any>`).
- **Empirical Execution Output:**
  - `physics_engine.md`: Extracted 14 code blocks. Found 8 Pydantic models (`Vector3D`, `S2CognitiveProfile`, `BiometricCompartmentState`, `TrenchEngagement`, `PocketEnvelopeState`, `BallState`, `PhysicsTickFrameState`). TypeScript compiled strictly with 0 errors and zero `any` types.
  - `dynasty_empire.md`: Extracted 14 code blocks. Found 9 Pydantic models (`AbilityDefinitionSchema`, `PlayerDynastyProfile`, `ContractYearDetail`, `CapOptimizationProposal`, `MedicalTriageRecord`, `DAGStorylineChoice`, `DAGStorylineNode`, `TradeProposalContract`). TypeScript compiled strictly with 0 errors and zero `any` types.
  - `broadcast_director.md`: Extracted 9 code blocks. TypeScript compiled strictly with 0 errors and zero `any` types.
  - `ui_design_system.md`: Extracted 12 code blocks. Found 22 Pydantic models. TypeScript compiled strictly with 0 errors and zero `any` types.
  - **Verdict:** PASSED with 100% compliance.

### 1.2 `scripts/check_field_parity.py`
- **File Location:** `scripts/check_field_parity.py` (293 lines)
- **Target Specifications:** Deep cross-comparison between Python Pydantic V2 models and TypeScript interfaces extracted via `scripts/extract_ts_schemas.js`.
- **Parity Rules & Checks Enforced:**
  - **Casing Transformation:** Translates Python `snake_case` attributes into TypeScript `camelCase` properties via bidirectional regex transformation (`snake_to_camel`, `camel_to_snake`).
  - **Enum Member Parity:** Performs symmetric difference (`^`) sets on enum string values between Python enum members and TypeScript `const` object properties.
  - **Pillar 1 (Physics Engine):** Verifies 1:1 property matching for `Vector3D`, `S2CognitiveProfile`, `BiometricCompartmentState`, `TrenchEngagement`, `PocketEnvelopeState`, `BallState`, `PhysicsTickFrameState`.
  - **Pillar 4 (Master Domain Contracts):**
    - **Enum Parity (7/7 Perfect Match):**
      1. `DevTraitEnum` <-> `DevTrait`: 4 members (`NORMAL`, `STAR`, `SUPERSTAR`, `XFACTOR`)
      2. `OvrTierEnum` <-> `OvrTier`: 5 members (`CLUB_99`, `ELITE`, `STARTER`, `ROTATIONAL`, `BACKUP`)
      3. `InjuryStatusEnum` <-> `InjuryStatus`: 5 members (`ACTIVE`, `QUESTIONABLE`, `DOUBTFUL`, `OUT`, `IR`)
      4. `AnatomicalZoneEnum` <-> `AnatomicalZone`: 8 members (`HEAD`, `NECK`, `TORSO`, `RIGHT_ARM`, `LEFT_ARM`, `RIGHT_LEG`, `LEFT_LEG`, `ANKLE_FOOT`)
      5. `MedicalInterventionEnum` <-> `MedicalIntervention`: 4 members (`REST_AND_REHAB`, `SURGICAL_REPAIR`, `INJECTION_THERAPY`, `PHYSICAL_THERAPY`)
      6. `BroadcastPhaseEnum` <-> `BroadcastPhase`: 7 members (`PRE_GAME`, `PRE_PLAY`, `IN_PLAY`, `POST_PLAY`, `COMMERCIAL`, `HALFTIME`, `POST_GAME`)
      7. `AudioTriggerType` <-> `AudioTriggerType`: 8 members (`WHISTLE`, `CROWD_ROAR`, `CROWD_CHEER`, `CROWD_GROAN`, `TACKLE_HARD`, `TACKLE_SOFT`, `COLLISION_HIT`, `BALL_CATCH`)
    - **Master Domain Model Parity (21/21 Perfect Match):**
      - 20 Models match 1:1 on all field definitions: `Vector3D` (3 fields), `PlayerGenesisBiometrics` (7 fields), `PlayerAttributes` (17 fields), `PlayerContract` (9 fields), `PlayerFatigueState` (5 fields), `PlayerEntity` (15 fields), `CoachingPhilosophy` (6 fields), `TeamCapSheet` (7 fields), `TeamEntity` (18 fields), `TelemetryPlayerState` (8 fields), `TrenchCollisionVector` (5 fields), `TelemetryFrame` (6 fields), `PlayCallInput` (9 fields), `CameraShotSchema` / `CameraShot` (7 fields), `OverlayCueSchema` / `OverlayCue` (6 fields), `ClipCueSchema` / `ClipCue` (7 fields), `AudioTriggerPayload` (5 fields), `AnatomicalZoneInjury` (7 fields), `InjuryTriageRecord` (7 fields), `GameStateSyncPayload` (10 fields).
      - 1 Discriminated Union verified: `WebSocketBroadcastMessage` mapped to TypeScript union with discriminant literal `messageType` (`"STATE_SYNC"`, `"TELEMETRY_FRAME"`, `"AUDIO_TRIGGER"`, `"INJURY_EVENT"`).
- **Observed Structural Divergence in Pillar 2:**
  - In Pillar 2 (`dynasty_empire.md`), specialized backend financial models (`ContractYearDetail`, `CapOptimizationProposal`) and clinical models (`MedicalTriageRecord`) are projected into consolidated frontend representations (`CapologyLedgerItem`, `MedicalTriageState`). This is an intentional architectural projection rather than schema drift, supporting virtualized master-detail views.

---

## 2. Frontend Compilation & Typecheck Configuration

### 2.1 Configuration Architecture
- **Build Toolchain:** Vite 7.3.0 + TypeScript 5.9.3 + React 19.2.0.
- **`frontend/package.json`:**
  - Build script: `"build": "tsc -b && vite build"`
  - Zero tolerance for build bypasses (`tsc -b` evaluates all project references prior to Vite bundling).
- **`frontend/tsconfig.json` & `frontend/tsconfig.app.json`:**
  - Strict Mode Options Enabled:
    - `strict: true` (activates `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`)
    - `target: "ES2022"`
    - `moduleResolution: "bundler"`
    - `noUnusedLocals: true`
    - `noUnusedParameters: true`
    - `erasableSyntaxOnly: true`
    - `noFallthroughCasesInSwitch: true`
    - `noUncheckedSideEffectImports: true`

### 2.2 Compilation Verification
- Command executed: `npm --prefix frontend run build` (`tsc -b && vite build`)
- **Result:**
  - TypeScript project reference check (`tsc -b`): **0 errors**.
  - Vite compilation: **3,756 modules transformed cleanly**.
  - Generated output:
    - `dist/index.html` (0.46 kB)
    - `dist/assets/index-TwaDolIS.css` (272.03 kB)
    - `dist/assets/index-Cx62k13D.js` (2,675.61 kB)
    - Total bundle build time: **23.25s**.
  - Warnings noted: Large bundle advisory (>500 kB chunk for main index chunk) and outdated CSS gradient syntax warnings in PostCSS. No fatal errors.

### 2.3 Comprehensive `any` Type Audit
- **Methodology:** AST and lexical regex inspection across all TypeScript files (`.ts`, `.tsx`) in `frontend/src/`.
- **Target Patterns:** `:\s*any`, `as\s+any`, `<any>`, `Array<any>`, `Promise<any>`, `Record<[^,]+,\s*any>`.
- **Findings:**
  - Total type violations found: **0**.
  - Only 11 textual occurrences of the word `any` exist across `frontend/src/`, all located inside human-readable comments or UI label strings (e.g., `"* Handles all trade-related API calls with strict types (0 any)"` in `tradeApi.ts`, `"Click any of the 7 anatomical zones"` in `BodyMap.tsx`, `"Keeps the app usable without changing any server-side functionality."` in `useSettingsStore.ts`).
  - **Verdict:** 100% strict typing compliance achieved.

---

## 3. Cross-Domain Boundary Verification Pipeline

### 3.1 Script Architecture (`scripts/test_domain_boundary_pipeline.py`)
The pipeline script exercises the entire cross-domain continuum across four design domains, culminating in discriminated WebSocket broadcast frames:

1. **Dynasty Engine Domain:** Instantiates `PlayerEntity` (Patrick Mahomes, OVR 99, CLUB_99, XFACTOR) and `TeamEntity` (Kansas City Chiefs). 
   - Biometrics (Hierarchical S2 Cognition 98, Reaction Latency 155ms, Fast-Twitch Ratio 0.88).
   - Contract ($450M total, duration 6 years, $37M Year 1 cap hit, $25M proration), all validated under PSC-010 framework.
   - Fatigue Compartments (ATP-PC stamina 1.0, glycolytic burn 0.0, CNS fatigue 0.05).
2. **60Hz Physics Engine:** Simulates `TelemetryFrame` (#1420 at 842.5s).
   - BallVector: position=(0.0, 35.0, 1.8) velocity=(12.5, 28.0, 5.2).
   - `TrenchCollisionVector`: OL #74 vs DL #99 -> 3,450 N kinetic force at leverage bias 0.62.
3. **Broadcast Director Domain:** 
   - `CameraShotSchema` ("cam_deep_pocket_tracking"): Automatically targets ball 3D position (0.0, 35.0, 1.8) at FOV 42.0 deg.
   - `AudioTriggerPayload`: Synthesizes Web Audio `COLLISION_HIT` at 108.5 dB from the 3,450 N impact.
4. **Clinical Medical Triage Domain:**
   - `InjuryTriageRecord`: Player #15 evaluated for Grade II High Ankle Sprain in `ANKLE_FOOT` zone.
   - Intervention: `PAIN_MANAGEMENT_TORADOL` (1.75x reinjury hazard multiplier).
   - Cleared for limited practice while preserving medical compliance.
5. **WebSocket UI Broadcast Layer:** Packages each domain state into a discriminated `WebSocketBroadcastMessage` with sequence IDs and strict serialization:
   - Frame 10001 (`STATE_SYNC`): 278 bytes
   - Frame 10002 (`TELEMETRY_FRAME`): 823 bytes
   - Frame 10003 (`AUDIO_TRIGGER`): 228 bytes
   - Frame 10004 (`INJURY_EVENT`): 483 bytes

- **Verification Command:** `python scripts/test_domain_boundary_pipeline.py`
- **Result:** PASSED with 0 errors and zero serialization violations.

---

## 4. Latency Benchmarks & Performance Harness

### 4.1 `backend/scripts/benchmark_mcp.py`
- **Current Role:** Measures tool-call round-trip latency against `mcp_servers/nfl_stats_server/server.py` using standard IO (`stdio`) transport.
- **Workload:** Executes 50 iterations of `get_player_career_stats(player_name="Patrick Mahomes", start_year=2020, end_year=2024)`.
- **Target Budget:** Asserts P95 latency < 500ms.
- **Architecture:** Uses `MCPHostClient` with async subprocess communication.

### 4.2 `backend/scripts/load_test.py`
- **Current Role:** HTTP benchmark testing FastAPI root endpoint `/` under concurrent load.
- **Workload:** 100 concurrent workers sending 1,000 requests via `aiohttp`.
- **Metrics Collected:** Total elapsed time, requests per second (RPS), success rate, mean latency, P95 latency, max latency.

### 4.3 Identification of Latency Budget Testing Gap
The authoritative sprint mandate (in `ORIGINAL_REQUEST.md`) specifies strict operational latency thresholds across the four sprint subsystems:
1. **Live Physics & Telemetry Frame Delivery:** `<16ms` (60 FPS ceiling).
2. **Capology Multi-Year Proration & AI GM Bidding Resolution:** `<40ms`.
3. **Virtualized Free Agency & Roster Table Rendering:** `60 FPS` with 1,000+ records.
4. **Baldwin 4th-Down Decision Recommendation Lookups:** `<10ms` in-memory.
5. **Locker Room Society Chemistry Differential Equations:** `<2ms` per team.

**Gap Identified:** Neither `backend/scripts/benchmark_mcp.py` nor `backend/scripts/load_test.py` currently executes these operational budget assertions. `benchmark_mcp.py` only tests the external statistics MCP Server.

### 4.4 Proposed Latency Benchmark Harness Blueprint
A dedicated benchmark suite should be added (or integrated into `backend/scripts/benchmark_mcp.py`) that executes in-memory micro-benchmarks across:
1. **Telemetry Generation Harness:** Execute 1,000 physics frames of 22-player 3D position updates and trench collision vector resolution. Measure P95 execution time against the `<16.0ms` threshold.
2. **Capology Proration & AI GM Bidding Harness:** Run 5-year signing bonus amortization, post-June 1 cut dead cap calculations, and 32-team AI GM bidding resolution over a 500-player free agent pool. Measure P95 execution time against the `<40.0ms` threshold.
3. **Society Chemistry Differential Harness:** Solve the locker room morale/chemistry ODE system for 32 teams (53-man rosters = 1,696 players). Measure execution time against the `<2.0ms` per team threshold.

---

## 5. Statistical Calibration Engine

### 5.1 `scripts/batch_simulator.py` (Monte Carlo Calibration)
- **Engine Architecture:** Headless batch simulation running full 120-play games with complete 21-player offensive and defensive rosters. Uses `DeterministicRNG` for seeded repeatability.
- **Statistical Benchmark Bounds:**
  - **Sack Rate:** Target `6.50%` (Tolerance `±1.50%`, Valid Range: `5.00% - 8.00%`)
  - **Yards Per Carry (YPC):** Target `4.20 yds` (Tolerance `±0.50 yds`, Valid Range: `3.70 - 4.70 yds`)
  - **Completion Rate:** Target `64.50%` (Tolerance `±4.50%`, Valid Range: `60.00% - 69.00%`)
  - **Turnovers Per Game:** Target `1.30 / gm` (Tolerance `±0.50 / gm`, Valid Range: `0.80 - 1.80 / gm`)
  - **Points Per Game:** Target `21.80 pts` (Tolerance `±4.00 pts`, Valid Range: `17.80 - 25.80 pts`)
- **Empirical Execution Results (100 Games):**
  - Command: `python scripts/batch_simulator.py --games 100 --calibrate`
  - Simulation Performance: **100 games completed in 3.74s** (**26.7 games/sec**).
  - Observed Statistics:
    - **Sack Rate:** `6.72%` (Target: 6.50%, Delta: +0.22%) -> **PASS**
    - **Yards Per Carry:** `3.99 yds` (Target: 4.20, Delta: -0.21) -> **PASS**
    - **Completion Rate:** `66.83%` (Target: 64.50%, Delta: +2.33%) -> **PASS**
    - **Turnovers Per Game:** `0.96 / gm` (Target: 1.30, Delta: -0.34) -> **PASS**
    - **Points Per Game:** `24.32 pts` (Target: 21.80, Delta: +2.52) -> **PASS**
  - **Verdict:** ALL 5 GATES PASSED with 100% compliance.

### 5.2 `backend/scripts/run_statistical_validation.py` & `StatisticalValidator`
- **Data Ground Truth:** nflfastR empirical distribution parameters (2018-2023 dataset).
- **Validation Metrics & Strict Tolerances:**
  - **YPC:** Mean `4.3 ± 0.5 yds` (Valid Range: `3.8 - 4.8 yds`)
  - **Completion %:** Target `65.0% ± 2.0%` (Strict Window: `63.0% - 67.0%`)
  - **Sack Rate:** Target `7.2% ± 1.0%` (Strict Window: `6.2% - 8.2%`)
  - **Interception Rate:** Target `2.4% ± 1.0%` (Strict Window: `1.4% - 3.4%`)
  - **Yards Per Completion:** Mean `11.2 ± 2.0 yds` (Window: `9.2 - 13.2 yds`)
- **Empirical Execution Results (1,000 Plays):**
  - Command: `python backend/scripts/run_statistical_validation.py --plays 1000`
  - Observed Statistics:
    - **YPC:** `4.35 yds` (Expected: 4.30) -> **PASS**
    - **Completion %:** `64.0%` (Expected: 65.0%) -> **PASS**
    - **Sack Rate:** `7.17%` (Expected: 7.20%) -> **PASS**
    - **INT Rate:** `2.22%` (Expected: 2.40%) -> **PASS**
    - **Yards/Completion:** `12.2 yds` (Expected: 11.20) -> **PASS**
  - **Verdict:** OVERALL PASSED in <0.1s.

---

## 6. Architectural Records & Living Dossiers

### 6.1 Architecture Decision Records (`docs/decisions/`)
- **Current Inventory:**
  1. `ADR-001-database-orm-choice.md`: Selection of SQLAlchemy 2.0 with async engine and Alembic migrations.
  2. `ADR-002-mcp-integration-architecture.md`: Adoption of Model Context Protocol over stdio transport.
  3. `ADR-003-trait-system.md`: Database trait persistence and delegated adapter pattern.
  4. `ADR-004-attribute-interaction-model.md`: 13-system inter-positional attribute equation engine.
- **Identified Gaps (Missing ADRs for Sprint Subsystems):**
  - **ADR-005 (CBA-Compliant Capology & Multi-Year Proration):** Must document the 5-year maximum signing bonus proration, the post-June 1st two-season dead money acceleration split, the top-51 offseason rule, and multi-team AI GM auction mechanics.
  - **ADR-006 (Locker Room Dynamic Differential Equations & Council Narrative Synthesis):** Must document deterministic Tier 1 differential equations for team chemistry/morale and Tier 2/3 LLM narrative council events with prompt injection defense.
  - **ADR-007 (Clinical Orthopedic Trauma Triage & Dynamic RTP Roster Synchronization):** Must document 5 clinical pathways (Rest, PRP, Arthroscopic, Reconstructive, Cortisone), anatomical zone health tracking, and bidirectional roster status synchronization.
  - **ADR-008 (60Hz Live Play-Calling HUD & Real-Time Baldwin 4th-Down Analytics):** Must document HUD event dispatching during 60Hz physics ticks and Ben Baldwin expected points lookup models.

### 6.2 Living Feature Status Matrix (`docs/FEATURE_STATUS_MATRIX.md`)
- **Current State:** 132 features tracked across 10 categories (GAME, AI, ATTR, RPG, FRAN, MCP, UI, DEP, SUBSYS, AUDIT). All 42 P0 features marked PRODUCTION_READY. Last certified on 2026-08-31.
- **Identified Gaps:** Zero entries exist for:
  - `TASK-010`: Interactive Free Agency Market & Contract Bidding Hub
  - `TASK-011`: Locker Room & Closed-Door Council UI
  - `TASK-012`: Medical Center Live Roster & Surgical Triage Integration
  - `TASK-013`: In-Game Play-Calling HUD During Live Sim
- **Action Required:** Author and insert feature entries into `docs/FEATURE_STATUS_MATRIX.md` under dedicated sections, linking task specifications, test paths, and production readiness certifications.

### 6.3 Player System Living Dossier (`docs/player-system/PLAYER_SYSTEM_DOSSIER.md`)
- **Current State:** 1,210-line comprehensive reference mapping models, attributes, positions, progression, traits, and injuries. Last certified on 2026-08-22.
- **Identified Gaps:**
  - **Section 10 (Contracts & Salary Cap):** Currently documents only baseline `PlayerContract` fields and 3-wave free agency interest formulas. Must be updated to include:
    - 5-year maximum signing bonus proration formula: `prorated = bonus / min(years, 5)`
    - Post-June 1 cut dead cap acceleration split over two league years
    - Top-51 offseason salary cap rule enforcement
    - AI GM bidding auction algorithm and tax-adjusted market valuations
  - **Section 11 (Injury System & GENESIS Biometrics):** Documents 7 body parts and recovery formulas, but needs synchronization with:
    - 5-pathway clinical triage decision matrix
    - Real-time hazard multiplication curves during live game simulation
    - Automatic bidirectional roster state synchronization (`ACTIVE`, `QUESTIONABLE`, `DOUBTFUL`, `OUT`, `IR`) based on clinical protocol selection.

---

## 7. Recommended Action Plan for Implementation Tracks

1. **Track 1 (Contract & Capology):**
   - Formalize ADR-005 for CBA capology mechanics.
   - Update Section 10 of `docs/player-system/PLAYER_SYSTEM_DOSSIER.md`.
   - Update `docs/FEATURE_STATUS_MATRIX.md` with TASK-010 entry.
2. **Track 2 (Frontend UI Virtualization):**
   - Ensure virtualized scrolling harnesses are verified for >1,000 free agent records.
   - Maintain strict typing (0 `any` types) and strict TS mode across new UI components.
3. **Track 3 (Physics, Telemetry & HUD):**
   - Formalize ADR-006 (Locker Room) and ADR-008 (Play-Calling HUD).
   - Ensure 60Hz WebSocket frame delivery stays within <16ms latency ceiling.
4. **Track 4 (QA, Harnesses, Validation & Dossier Sync):**
   - Author missing ADRs (ADR-005, ADR-006, ADR-007, ADR-008) in `docs/decisions/`.
   - Extend `backend/scripts/benchmark_mcp.py` to benchmark operational latency budgets (<16ms, <40ms, <2ms).
   - Synchronize `docs/FEATURE_STATUS_MATRIX.md` with TASK-010..013 entries.
   - Update `docs/player-system/PLAYER_SYSTEM_DOSSIER.md` Sections 10, 11, and 16 (Changelog).

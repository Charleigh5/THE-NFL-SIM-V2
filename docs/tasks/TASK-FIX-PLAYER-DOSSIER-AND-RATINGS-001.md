<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-FIX-PLAYER-DOSSIER-AND-RATINGS-001: Resolve Player Dossier 500 Error, Reseed Authentic Positional Ratings & Dynamic Roster Badges

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:**
  - In `THE-NFL-SIM-V2`, player profiles display biometric telemetry, personality traits, and career statistics via the `EnhancedPlayerProfile` modal triggered by "OPEN IN-DEPTH BIOMETRICS & TRAITS DOSSIER".
  - During season 2026 seeding from `nflverse`, player ratings were generated using `generate_player_ratings()` in `ratings_generator.py`.
- **Related Ideas:**
  - Modern sports management simulators (e.g., Football Manager, Out of the Park Baseball) avoid flat baseline ratings (50/50/50) and provide position-contextual scouting metrics on roster overview cards rather than generic athletic speed for 330lb offensive linemen.
  - SQLAlchemy 2.0 type-safe row queries with aggregate functions require exact label aliasing (`func.sum(...).label("rushing_tds")` matching `stats.rushing_tds`).
- **Future Potential:**
  - Enables full fidelity scouting, player development progression, and game-planning AI where OL pass/run blocking and DL pass rushing accurately influence pocket breakdown and blitz success.
- **Constraints:**
  - Zero regression in existing test suites (`pytest`, Playwright E2E).
  - Clean TypeScript build (`tsc --noEmit` and Vite build).
  - Reseed must accurately populate all 3,219 NFL players across all 32 franchises.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Patch the single typo in `backend/app/api/endpoints/players.py` (`rush_tds` -> `rushing_tds`) and run an ad-hoc SQL update on the database to bump speed, strength, and agility for linemen.

### Powerful Antithesis
Merely fixing the typo leaves the underlying simulation engine compromised:
1. 951 NFL players (423 DL, 517 OL, 36 LS, 39 P) were incorrectly categorized because `nflverse_service.py` read the generic `position` ("DL", "OL") rather than the granular `depth_chart_position` ("DE", "DT", "NT", "T", "G", "C").
2. `ratings_generator.py` fell into an unhandled `else:` branch that assigned kicker ratings (`kick_power`, `kick_accuracy`) to interior offensive and defensive linemen, calculating overall ratings while leaving all athletic skills at 50.
3. Roster cards in `FrontOffice.tsx` hardcoded `SPD`, `STR`, `AGI` across all positions, forcing users to view irrelevant metrics for linemen and kickers.

### The Superior Synthesis
Execute a complete 3-tier remediation:
1. **API & Profiler Integrity**: Fix `rushing_tds` in `backend/app/api/endpoints/players.py` and extend `_get_position_attributes` to support `DL`, `OL`, `EDGE`, `NT`, `T`, `G`, `FB`, `LS`.
2. **Positional Matrix & Reseed Pipeline**:
   - Update `POSITION_MAP` and `nflverse_service.py` to read `depth_chart_position`.
   - Update `ratings_generator.py` to calculate authentic physical ratings (speed, acceleration, agility, strength, pass/run block, pass rush power/finesse) using weight-calibrated physics baselines when combine data is missing.
   - Reseed the 2026 league database cleanly (`seed_players_from_nflverse(season=2026, force=True)`).
3. **Dynamic Frontend Telemetry Badges**:
   - Extend `PlayerSchema` in `backend/app/api/endpoints/teams.py` to expose core position attributes (`pass_block`, `run_block`, `tackle`, `pass_rush_power`, `throw_power`, `man_coverage`, etc.).
   - In `frontend/src/pages/FrontOffice.tsx`, replace the static `SPD | STR | AGI` triplet with dynamic, position-relevant metric badges (e.g., `PBK | RBK | STR` for OL, `TAK | BKS | STR` for DL, `THP | THA | SPD` for QB, `MCV | ZCV | SPD` for DB).
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** FastAPI, SQLAlchemy 2.0 (AsyncSession), React 18, Vite, TailwindCSS
- **Language:** Python 3.13, TypeScript 5.5
- **Data Source:** nflreadpy / nflverse 2026 roster and contract data

### 2. The Data Schema (Pre-Generation)
- `PlayerSchema`: Expose `pass_block`, `run_block`, `tackle`, `block_shed`, `pass_rush_power`, `throw_power`, `throw_accuracy_short`, `catching`, `route_running`, `man_coverage`, `zone_coverage`, `kick_power`, `kick_accuracy`.

### 3. Step-by-Step Execution
- [ ] **Step 1: Backend Endpoint Fix.** Fix `stats.rushing_tds` in `backend/app/api/endpoints/players.py` and extend position attribute mappings.
- [ ] **Step 2: Positional Mapping & Rating Generator Overhaul.** Update `nflverse_service.py` and `ratings_generator.py` with physical estimations and specific positions.
- [ ] **Step 3: Database Reseed.** Run clean 2026 roster reseed using updated generator.
- [ ] **Step 4: Roster Endpoint Schema & Cache Invalidation.** Extend `PlayerSchema` in `teams.py` and invalidate roster cache.
- [ ] **Step 5: Frontend Dynamic Positional Badges.** Update `FrontOffice.tsx` to render contextual stat triplets based on position.
- [ ] **Step 6: End-to-End Verification.** Test player dossier profile endpoint, verify non-50 ratings in database, verify UI with Playwright.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** No `any` types in frontend; strict Pydantic models.
- [ ] **API Verification:** `GET /api/players/909/profile` returns HTTP 200 with populated traits, position attributes, and stats.
- [ ] **Database Integrity:** Zero OL/DL players with 50/50/50 SPD/STR/AGI.
- [ ] **Frontend Verification:** Build and lint pass without warnings or errors.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Execute Step 1 to Step 6 and verify in the terminal.
</baton_handoff>

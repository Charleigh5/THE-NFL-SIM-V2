<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-035_CURRENT_2026_2027_NFL_SCHEDULE_AND_ROSTERS

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>
- **Historical Origins:** NFL simulation engines often rely on synthetic schedules and randomized players or outdated static rosters. Authentic gameplay requires exact parity with real NFL operations, using authoritative league schedules (18 weeks, 272 games, bye weeks, primetime and Thanksgiving slots) and authentic 90/53-man rosters.
- **Related Ideas:** `nflverse` / `nflreadpy` open-source data pipelines, sports simulation database architectures, Madden franchise mode initialization patterns.
- **Future Potential:** Multi-year franchise dynasty transitions where 2026 is grounded in verified real-world schedule and contracts, while 2027+ dynamically leverages procedural scheduling, rookie drafts, and free agent markets.
- **Constraints:**
  - Strict preservation of SQLite/SQLAlchemy schema and models (`Game`, `Player`, `Season`, `Team`).
  - Zero corruption of existing 32 team IDs or foreign keys.
  - Contract APY must be accurately parsed into dollar units (avoiding 55.0 being truncated to $55 instead of $55,000,000).
  - All 455 unit tests must pass without regressions.
  - Frontend must compile with zero errors (`tsc -b && vite build`).
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>
### Primary Thesis
Hardcode or import a static CSV of 2026 games and players into the database once via a one-off script.

### Powerful Antithesis
A static dump creates orphaned state, fails if new databases are initialized or tests reset tables, breaks contract financial systems due to OTC unit mismatches, and prevents dynamic season initialization when users click "Kickoff" or reset seasons through `/api/season/init`.

### The Superior Synthesis
Integrate `nflreadpy` natively into the `ScheduleGenerator` and `NflverseService`.
1. `ScheduleGenerator.load_real_schedule` dynamically parses official 2026 NFL schedule data (272 games), mapping team abbreviations (`LA` -> `LAR`, `WSH` -> `WAS`) and injecting gameday timestamps, venue weather conditions, and game types.
2. In `NflverseService`, normalize contract APY and map rosters across all 32 teams.
3. In `seed.py`, provide `seed_2026_season` and `SEED_MODE=REAL_2026` to guarantee reproducible bootstrap in development, staging, or production.
4. Align frontend controls in `Dashboard.tsx` to initiate the 2026-2027 campaign.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>
### 1. Technology & Architecture Context
- **Frameworks:** FastAPI, SQLAlchemy 2.0, Polars, nflreadpy, React 19, Vite, Tailwind CSS
- **Language:** Python 3.13+, TypeScript 5.7+
- **State Management:** TanStack Query, Zustand, React Router v7

### 2. The Data Schema (Pre-Generation)
- `Season`: `year=2026`, `status=REGULAR_SEASON`, `current_week=1`, `total_weeks=18`, `is_active=True`
- `Game`: 272 games, `season=2026`, `week` 1-18, `away_team_id`, `home_team_id`, `date`, `weather_temperature`, `wind_speed`, `weather_condition`, `is_played=False`
- `Player`: 2,963 active players across 32 teams, with scaled `contract_salary` and `depth_chart_rank`.

### 3. Step-by-Step Execution
- [ ] **Step 1: Scaffolding.** Update `nflverse_service.py` with corrected team abbreviation mappings and contract scaling.
- [ ] **Step 2: Core Logic.** Add `load_real_schedule` in `schedule_generator.py` and connect `initialize_season` in `season.py`.
- [ ] **Step 3: Database Bootstrap.** Implement `seed_2026_season` and update `seed.py` for 2026 rosters and schedule.
- [ ] **Step 4: Interface.** Update `Dashboard.tsx`, `SeasonDashboard.tsx`, and `router.tsx` to launch the 2026-2027 season.
- [ ] **Step 5: Verification.** Execute unit tests, test 2026 real schedule loading, and verify frontend production build.

### 4. Edge Cases & Error Handling
- [Case A: nflreadpy network offline during dynasty sim] -> [Gracefully falls back to procedural schedule generation]
- [Case B: Player contract APY in millions vs raw dollars] -> [Threshold check `< 1000` scales millions to full dollar integer; raw dollars preserved]
</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** No `any` types introduced in TypeScript; strict typing maintained in Python models.
- [ ] **Security:** No secrets or dynamic loader vulnerabilities injected.
- [ ] **Performance:** Schedule loading and roster mapping executes in <4 seconds.
- [ ] **Self-Critique:** Starters must have `depth_chart_rank=1` so users aren't met with unassigned depth charts.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Execute the code updates across `nflverse_service.py`, `schedule_generator.py`, `seed.py`, `season.py`, and frontend dashboard components.
</baton_handoff>

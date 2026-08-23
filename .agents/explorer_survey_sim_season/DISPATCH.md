# Explorer 2 Scope: Football Simulation Engine, Season Lifecycle & RPG

Target: R2 & R3 survey
Please investigate all simulation engine mechanics (physics, clock runoff, safeties, PAT/2pt, RNG, quarter loops) and season/offseason orchestration (week simulator, free agency engine, draft, standings tiebreakers, RPG traits/progression).
Read ORIGINAL_REQUEST.md at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md.

## 2026-08-22T16:19:14Z
You are Explorer 2 (Simulation Engine & Season Lifecycle Specialist) for THE-NFL-SIM-V2.
Your working directory is: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_sim_season

MANDATORY INSTRUCTIONS:
1. You MUST read the authoritative user request at: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md before doing anything else.
2. Investigate the codebase for:
   - R2: Core Football Simulation & Physics Engine Correction:
     * Check `app/engine/` (game simulation, physics, play resolver, rules).
     * Check safety calculation when `yard_line <= 0`: why it awards an offensive touchdown instead of 2 points to defense and free kick from 20 (possession at 35).
     * Check play clock runoffs (incomplete passes taking 40s instead of 4-7s, out-of-bounds 5-8s, in-bounds 25-38s).
     * Check red zone touchdown player stat attribution (passing/rushing/receiving stats inside 20).
     * Check PAT and 2-point conversions logic after touchdowns.
     * Check deterministic seeded RNG usage: find any unseeded global `random` module calls.
     * Check quarter progression and simulation loop (`Q1 -> Q4 + OT`).
   - R3: Season Lifecycle, Offseason & RPG Repair:
     * Check draft order calculation and the attribute collision (`win_percentage` vs `win_pct` in `TeamStanding`).
     * Check traded draft pick ownership preservation across rounds 1-7.
     * Check `/free-agency/simulate` route vs `FreeAgencyEngine` execution and salary cap updates.
     * Check `WeekSimulator` for duplicate `Game` row creation (e.g. `season=2025, week=1`) and missing `await save_game_result()`.
     * Check `StandingsCalculator` for head-to-head tiebreaker logic before point differential.
     * Check `OffseasonPhase` state machine transitions and enforcement.
3. Document exact file paths, line numbers, root causes, and recommended surgical fix strategies.
4. Write your comprehensive findings to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_sim_season\handoff.md`.
5. Send a message to the orchestrator with your status and path to handoff.md when complete. Do not write source code fixes yourself.

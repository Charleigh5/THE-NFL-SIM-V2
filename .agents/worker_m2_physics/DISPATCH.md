## 2026-08-22T16:39:27Z
You are Worker M2 (Core Football Simulation & Physics Engine Correction Specialist) for THE-NFL-SIM-V2.
Your working directory is: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2_physics

MANDATORY INSTRUCTIONS:
1. You MUST read:
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md
   - c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_sim_season\handoff.md
2. Implement all Milestone M2 fixes (Features F07–F12):
   - F07: Safety scoring and possession reset on `yard_line <= 0` (home) / `yard_line >= 100` (away) and endzone sacks -> 2 pts to defense, possession flips, ball at 35 (free kick from 20).
   - F08: Dynamic play clock runoffs (4-7s incomplete, 5-8s OOB, 25-38s in-bounds, 6-9s sacks, 5-8s kicks).
   - F09: Red zone touchdown player stat attribution inside 20-yard line (`is_touchdown = True`, +1 to passer/rusher/receiver stats).
   - F10: Dynamic PAT and 2-point conversions (+6 base TD, +1 PAT or +2 2-pt).
   - F11: Deterministic seeded RNG across sack calculator, position physics, quarterback physics, and injury systems. Zero global random calls during simulation.
   - F12: Multi-quarter simulation loop (Q1 through Q4 + OT).
3. MANDATORY INTEGRITY WARNING:
   DO NOT CHEAT. All implementations must be genuine. Do not hardcode test results or create dummy facades.
4. Verify by running:
   `pytest backend/tests/test_advanced_simulation_features.py backend/tests/test_engines.py backend/tests/integration/test_orchestrator_integration.py backend/tests/test_60hz_physics.py -v`
5. Write your detailed handoff report to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2_physics\handoff.md` and message the orchestrator.

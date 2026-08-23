## 2026-08-21T21:17:35Z
You are Worker M3: Broadcast Director & Camera State Machine Architect.
Working Directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m3
Project Root: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2
Original Request: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\ORIGINAL_REQUEST.md
Survey Reference: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_survey_3\survey_broadcast_ui.md
Project Blueprint: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Mission:
Write the complete, comprehensive architectural specification file:
c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\docs\design_theory\nfl_simulation_blueprint\broadcast_director.md

You MUST structure the document strictly following the 4-phase template in .agent/rules/task-list-template.md:
- <system_context> header (Persona, 2025/2026 Standards)
- # TASK: Broadcast Camera State Machine & Cutscene Choreography Specification (R3)
- ## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout) - Historical Origins, Related Ideas, Future Potential, Constraints
- ## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect) - Primary Thesis, Powerful Antithesis, Superior Synthesis
- ## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer):
  1. 7-State Discrete Broadcast Engine: Complete 7x7 state transition matrix for [IDLE_STADIUM, PRE_PLAY, PRE_SNAP, IN_PLAY, POST_PLAY_REACTION, HUD_UPDATE, HIGHLIGHT_REPLAY], transition conditions, and watchdog timeout cascade (4.0s - 25.0s) for zero deadlock.
  2. Procedural 3D Camera Orbit Trajectories: NFL Cartesian coordinate grid (X [-26.65, 26.65], Y [0, inf], Z [-60, 60]), Catmull-Rom splines, quaternion slerp, 4 tracking focal point algorithms (ball carrier, pocket cylinder, deep ball apex, sideline celebration), screen shake / trauma models.
  3. Procedural Web Audio API DSP Synthesis: Zero-dependency audio synthesis graphs for pink-noise crowd dynamics (50dB-120dB), stadium PA formant acoustics, dual-sine referee whistles, kinetic collision impacts, 4-operator FM broadcast stingers.
  4. Broadcast Overlay Cues & Synchronization: Lower thirds, scorebugs, next-gen stat callouts, replay wipe transition timings.
  5. Error Recovery & Fallback Matrices: Network jitter, render stall, missing asset fallbacks.
- ## 🛡️ PHASE 4: THE AUDITOR (Verification) - Frame budget (<1.5ms), Audio buffer underrun prevention, State determinism, Type Check, Security, Performance, Self-Critique
- <baton_handoff>

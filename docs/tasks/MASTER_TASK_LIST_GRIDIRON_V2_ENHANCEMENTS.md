# MASTER TASK LIST: GRIDIRON V2 SUBSYSTEM ENHANCEMENTS
**DOCUMENT ID:** MASTER-TASK-ENHANCE-001  
**SYSTEM:** THE-NFL-SIM-V2 ("The Digital Gridiron")  
**STANDARDS:** Production-Grade Architecture, Deterministic Simulation, Zero Type Drift, Hard Latency Budgets

---

## 🗺️ EXECUTIVE ROADMAP OVERVIEW

This enhancement roadmap elevates the four core subsystems deployed in the previous sprint (**TASK-010** through **TASK-013**) by incorporating cutting-edge NFL Collective Bargaining Agreement (CBA) mathematical rules, 2D interactive social graph visualization, orthopedic return-to-play clinical trajectories, and sub-millisecond keyboard-driven live play-calling.

```text
+---------------------------------------------------------------------------------------------------------+
|                               GRIDIRON V2 ENHANCEMENT SUITE (TASKS 014 - 017)                           |
+---------------------------------------------------------------------------------------------------------+
       |                                      |                                  |
       V                                      V                                  V
+-------------------------------+ +-------------------------------+ +-------------------------------+
|           TASK-014            | |           TASK-015            | |           TASK-016            |
| Multi-Year Capology Heatmap   | | Locker Room Social Graph &    | | Orthopedic RTP Trajectory &   |
|  & Void Years Proration Engine| |  Media Leaks Beat Writer Feed | |  Re-Injury In-Game Hazards    |
+-------------------------------+ +-------------------------------+ +-------------------------------+
       |                                      |                                  |
       - 5-Year Dynamic Heatmap               - D3/Canvas Social Clique Map      - 3-Curve RTP Comparison Graph
       - Void Years (2-3 Yr Accel)            - Post-Council Beat Writer Ticker  - 2nd Opinion Referral Clinic
       - CFA Comp Pick Offset Warning         - Contract Holdout Gating (>=90)   - Cortisone Live Sim 2.5x Hazard
       |                                      |                                  |
       +--------------------------------------+----------------------------------+
                                              |
                                              V
                               +-------------------------------+
                               |           TASK-017            |
                               | Floating Baldwin Pill &       |
                               |  Keyboard Audibles HUD        |
                               +-------------------------------+
                                              |
                               - Non-modal Floating 4th-Down Pill
                               - Space/1-4/T Hotkey Engine
                               - Live EPA & Win Probability Flow
```

---

## 📋 THE FOUR ENHANCEMENT BLUEPRINTS

### 1. [`TASK-014: MULTI_YEAR_CAPOLOGY_HEATMAP_AND_VOID_YEARS_CALCULATOR.md`](./TASK-014_MULTI_YEAR_CAPOLOGY_HEATMAP_AND_VOID_YEARS_CALCULATOR.md)
- **Subsystem:** Free Agency Market & Contract Bidding Hub (TASK-010 Enhancement)
- **Key Deliverables:**
  - Interactive 5-year cap liability bar chart with live slider reactivity.
  - NFL CBA Void Years proration spreading signing bonuses over up to 5 accounting years with post-void dead money acceleration.
  - Appendix V Compensatory Free Agent (CFA) cancellation warning preventing loss of round 3-5 compensatory draft picks.
- **Latency Ceiling:** $<40$ms full multi-year schedule calculation.

### 2. [`TASK-015: LOCKER_ROOM_SOCIAL_GRAPH_AND_MEDIA_LEAKS_ENGINE.md`](./TASK-015_LOCKER_ROOM_SOCIAL_GRAPH_AND_MEDIA_LEAKS_ENGINE.md)
- **Subsystem:** Locker Room & Closed-Door Council (TASK-011 Enhancement)
- **Key Deliverables:**
  - 2D Canvas/SVG force-directed locker room social graph mapping clique formations, veteran mentors, and toxic friction nodes.
  - Media leak generation dispatching real-time local beat writer and national insider tweets into the League Wire feed.
  - Contract holdout mechanics triggering training camp holdouts and trade demands for athletes with Tension $\ge 90.0$.
- **Latency Ceiling:** $<2$ms Tier 1 differential kernel; 60 FPS graph rendering.

### 3. [`TASK-016: ORTHOPEDIC_RTP_PROJECTION_TRAJECTORY_AND_RE_INJURY_HAZARDS.md`](./TASK-016_ORTHOPEDIC_RTP_PROJECTION_TRAJECTORY_AND_RE_INJURY_HAZARDS.md)
- **Subsystem:** Medical Center & Surgical Triage (TASK-012 Enhancement)
- **Key Deliverables:**
  - Return-To-Play (RTP) clinical comparison curves projecting weekly recovery percentages across all 5 protocols.
  - Outside Specialist referral clinic (Mayo Clinic / Kerlan-Jobe) revealing occult structural pathology and halving surgical risks.
  - In-game Cortisone re-injury degradation engine applying a $2.5\times$ hazard multiplier to field cut movements in 60Hz physics.
- **Latency Ceiling:** $<5$ms curve generation; 0ms live physics tick overhead.

### 4. [`TASK-017: IN_GAME_FLOATING_BALDWIN_HUD_AND_KEYBOARD_AUDIBLES_ENGINE.md`](./TASK-017_IN_GAME_FLOATING_BALDWIN_HUD_AND_KEYBOARD_AUDIBLES_ENGINE.md)
- **Subsystem:** Live Sim & Play-Calling HUD (TASK-013 Enhancement)
- **Key Deliverables:**
  - Floating non-intrusive Baldwin 4th-down decision pill embedded directly into the field viewport with $<10$ms recommendation speed.
  - Full keyboard hotkey controller (`Spacebar` to snap, `1`-`4` for tactical concepts, `T` for timeout, `A` for audible).
  - Real-time Win Probability & EPA flow graph plotting momentum swings beneath the live scoreboard.
- **Latency Ceiling:** $<16$ms 60Hz frame delivery; $<0.01$ms decision pill calculations.

---

## 🛡️ CROSS-SUBSYSTEM GOVERNANCE GATE

Every task must satisfy:
1. **Contract Parity**: 1:1 schema parity verified via `python scripts/verify_blueprint_contracts.py`.
2. **Strict Types**: 0 `any` types in TypeScript (`tsc --strict`).
3. **Operational Benchmarks**: Subsystems benchmarked via `python backend/scripts/benchmark_operational_latencies.py`.
4. **Statistical Realism**: 100-game Monte Carlo simulation verification against NFL reference distribution bounds.

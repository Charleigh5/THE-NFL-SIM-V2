# Project: THE-NFL-SIM-V2 ("The Digital Gridiron") - 5-Pillar Architectural Review & Optimization

## Architecture
THE-NFL-SIM-V2 is a full-stack professional football simulation platform uniting:
- **Dynasty & Empire**: Relational persistence (SQLAlchemy 2.0/PostgreSQL/SQLite), salary cap management, multi-year contracts, and free agency bidding auctions.
- **Physics Engine**: Deterministic 60Hz frame physics (`FramePhysicsEngine`) simulating player collisions, trajectories, and on-field mechanics at sub-millisecond rates (<0.05ms/frame).
- **Society Engine**: Tier 1 deterministic differential equations (`tension_engine.py`) modeling locker-room chemistry and morale (<2.0ms per 53-man roster), Tier 2 event activation gating (threshold >= 75.0), and Tier 3 agentic dialogue synthesis (`locker_room_agent.py`).
- **Medical Trauma & Triage**: 5-pathway anatomical orthopedic triage (`REST`, `PRP_THERAPY`, `ARTHROSCOPIC_SURGERY`, `RECONSTRUCTIVE_SURGERY`, `CORTISONE_STABILIZATION`) with dynamic body health state transitions and roster status synchronization.
- **In-Game Play-Calling HUD**: Interactive play-calling interface with Ben Baldwin 4th-down decision modeling (Go/Punt/FG) operational during live 60Hz physics telemetry.
- **Frontend Presentation**: React/Vite/TypeScript interface featuring @tanstack/react-virtual windowing for 1,500+ free agents and 53-man rosters maintaining 60 FPS.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Post-June 1st Cap Splits | Two-year dead money allocation upon contract termination | M1 | ORIGINAL_REQUEST R2.1 |
| 2 | Top-51 Offseason Rule | Only top 51 cap hits count toward team cap during offseason | M1 | ORIGINAL_REQUEST R2.1 |
| 3 | Market Overview & Bidding API | Fix parameter mapping in FreeAgencyEngine and expose endpoints | M1 | ORIGINAL_REQUEST R2.1 |
| 4 | Free Agency Contract Types | Ensure FreeAgentSigning and FreeAgentMarketPlayer in TS types | M1 | ORIGINAL_REQUEST R1 |
| 5 | UI Virtualization Framework | Install @tanstack/react-virtual and create VirtualizedTable | M2 | ORIGINAL_REQUEST R3 |
| 6 | Interactive Free Agency Hub UI | Full interactive free agency market & contract bidding screen | M2 | ORIGINAL_REQUEST R2.1 |
| 7 | FrontOffice Roster Virtualization | Virtualized scrolling list for 53-man roster at 60 FPS | M2 | ORIGINAL_REQUEST R3 |
| 8 | Locker Room & Council UI | Closed-Door Council modal and locker room tension telemetry | M2 | ORIGINAL_REQUEST R2.2 |
| 9 | Society API Client Service | Frontend service integration for /api/society/teams/{id}/locker-room | M2 | ORIGINAL_REQUEST R2.2 |
| 10 | Medical Active Status Fix | Correct is_injured enum check to InjuryStatus.ACTIVE | M3 | ORIGINAL_REQUEST R2.3 |
| 11 | Medical Scalar Subscript Fix | Fix player.body_health[0] to player.body_health | M3 | ORIGINAL_REQUEST R2.3 |
| 12 | Medical Triage Persistence | Persist zone integrity forecast and insert InjuryEvent | M3 | ORIGINAL_REQUEST R2.3 |
| 13 | Medical Center Live Roster UI | Remove mock roster, wire to getTeamInjuries & triage endpoints | M3 | ORIGINAL_REQUEST R2.3 |
| 14 | Ben Baldwin 4th-Down Model | Expected Points / Win Probability model for Go/Punt/FG (<10ms) | M3 | ORIGINAL_REQUEST R2.4 |
| 15 | Play-Calling HUD & Telemetry UI | Interactive play-calling interface during 60Hz physics stream | M3 | ORIGINAL_REQUEST R2.4 |
| 16 | Operational Latency Harness | Benchmark script for <16ms telemetry, <40ms cap, <2ms society | M4 | ORIGINAL_REQUEST R3 |
| 17 | Architecture Decision Records | Author ADR-005 through ADR-008 in docs/decisions/ | M4 | ORIGINAL_REQUEST R5 |
| 18 | Status Matrix & Dossier Sync | Sync docs/FEATURE_STATUS_MATRIX.md & PLAYER_SYSTEM_DOSSIER.md | M4 | ORIGINAL_REQUEST R5 |
| 19 | Verification & Parity Certification | Run verify_blueprint_contracts, check_field_parity, npm build | M4 | ORIGINAL_REQUEST R1, R4 |
| 20 | Multi-Agent Review & Challenge | Full reviewer, challenger, and forensic auditor validation gates | M5 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Track 1: Contract/Capology Specialist | Features 1, 2, 3, 4: Post-June 1st, Top-51, FreeAgencyEngine fix, Offseason TS types | None | DONE |
| M2 | Track 2: Frontend UI Virtualization Specialist | Features 5, 6, 7, 8, 9: @tanstack/react-virtual, Free Agency UI, Roster virtualization, Locker Room UI | M1 contracts | DONE |
| M3 | Track 3: Physics/HUD & Medical Specialist | Features 10, 11, 12, 13, 14, 15: Medical fixes & live UI, Baldwin 4th-down, PlayCallingHUD | None | DONE |
| M4 | Track 4: QA, Latency, ADRs & Dossier | Features 16, 17, 18, 19: Latency benchmark, ADR-005..008, matrix & dossier sync, calibration | M1, M2, M3 | DONE |
| M5 | Final Verification & Forensic Audit | Feature 20: 2 Reviewers, 2 Challengers, 1 Forensic Auditor | M4 | DONE |

## Gate Summary
- **Reviewer 1**: APPROVE
- **Reviewer 2**: APPROVE
- **Challenger 1**: APPROVE
- **Challenger 2**: APPROVE
- **Forensic Auditor**: CLEAN
- **Gate Result**: **PASS**

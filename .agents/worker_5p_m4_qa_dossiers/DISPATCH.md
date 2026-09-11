# Dispatch: Worker M4 (Track 4: QA, Latency Benchmarks, ADRs & Living Dossiers)

## Mandatory Context
Read the authoritative user request at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`

Read the survey findings at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_5p_3\handoff.md`

Read the project scope and interface contracts at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_5pillar\PROJECT.md`

Read the worker handoffs at:
- `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m1_capology\handoff.md`
- `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m2_frontend_virtualization\handoff.md`
- `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m3_medical_hud\handoff.md`

## Working Directory
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m4_qa_dossiers`
Maintain your `BRIEFING.md` and `progress.md` in this directory.

## Exclusive File Ownership
You exclusively own and modify:
- `backend/scripts/benchmark_operational_latencies.py`
- `docs/decisions/ADR-005_FREE_AGENCY_CAPOLOGY_AND_TOP_51_RULE.md`
- `docs/decisions/ADR-006_LOCKER_ROOM_SOCIETY_AND_COUNCIL_SYNTHESIS.md`
- `docs/decisions/ADR-007_ORTHOPEDIC_TRIAGE_AND_RTP_SYNCHRONIZATION.md`
- `docs/decisions/ADR-008_IN_GAME_PLAY_CALLING_HUD_AND_BALDWIN_MODEL.md`
- `docs/FEATURE_STATUS_MATRIX.md`
- `docs/player-system/PLAYER_SYSTEM_DOSSIER.md`

DO NOT modify source code in frontend or backend engines.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Requirements
1. **Operational Latency Benchmark Script**:
   - Create `backend/scripts/benchmark_operational_latencies.py` testing live latency against strict operational budgets:
     - Live 60Hz physics & telemetry frame delivery: <16ms (runs FramePhysicsEngine)
     - Capology multi-year proration and AI GM bidding resolution: <40ms (runs CapologistPhysics and FreeAgencyEngine.process_user_bid)
     - 4th-down decision recommendation lookups: <10ms (runs FourthDownCalculator)
     - Locker room society chemistry evaluation: <2ms per team (runs TensionEngine on 53-man roster)
   - Must fail with non-zero exit code if any subsystem exceeds its latency budget.
2. **Formal Architecture Decision Records**:
   - Author 4 formal ADRs in `docs/decisions/` following the existing ADR-001..004 format:
     - `ADR-005_FREE_AGENCY_CAPOLOGY_AND_TOP_51_RULE.md`: Context, Decision, Consequences of 5-year proration ceiling, post-June 1st two-year split, Top-51 offseason calculation.
     - `ADR-006_LOCKER_ROOM_SOCIETY_AND_COUNCIL_SYNTHESIS.md`: Context, Decision, Consequences of 3-tier society engine (Tier 1 deterministic ODEs, Tier 2 threshold gating >=75, Tier 3 agentic closed-door council with offline fallback).
     - `ADR-007_ORTHOPEDIC_TRIAGE_AND_RTP_SYNCHRONIZATION.md`: Context, Decision, Consequences of 5-pathway anatomical triage, body health integrity forecast persistence, and RTP roster synchronization.
     - `ADR-008_IN_GAME_PLAY_CALLING_HUD_AND_BALDWIN_MODEL.md`: Context, Decision, Consequences of in-game play calling HUD with Ben Baldwin 4th-down model during 60Hz physics.
3. **FEATURE_STATUS_MATRIX Synchronization**:
   - Update `docs/FEATURE_STATUS_MATRIX.md` to add and update TASK-010, TASK-011, TASK-012, and TASK-013 to `PRODUCTION_READY` with test coverage and latency details.
4. **PLAYER_SYSTEM_DOSSIER Synchronization**:
   - Update `docs/player-system/PLAYER_SYSTEM_DOSSIER.md`:
     - Section 10: Document 5-year signing bonus proration, post-June 1st cap splits, and Top-51 offseason rule.
     - Section 11: Document the 5 clinical orthopedic triage pathways, body health integrity forecast updates, and RTP roster status synchronization.
5. **Run & Document All Full Verification Commands**:
   - `python scripts/verify_blueprint_contracts.py`
   - `python scripts/check_field_parity.py`
   - `npm --prefix frontend run build`
   - `python scripts/test_domain_boundary_pipeline.py`
   - `python backend/scripts/benchmark_operational_latencies.py`
   - `python scripts/batch_simulator.py --games 100 --calibrate`
   - `python backend/scripts/run_statistical_validation.py`

Deliver your report in `handoff.md` in your working directory and notify parent.

## 2026-09-06T03:52:00Z
User Request received:
Read your dispatch file at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m4_qa_dossiers\DISPATCH.md and the authoritative request at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md.

Implement:
1. Build backend/scripts/benchmark_operational_latencies.py verifying all operational thresholds (<16ms telemetry, <40ms capology, <10ms Baldwin 4th down, <2ms society chemistry).
2. Author ADR-005, ADR-006, ADR-007, and ADR-008 in docs/decisions/.
3. Update docs/FEATURE_STATUS_MATRIX.md with TASK-010..013 marked PRODUCTION_READY.
4. Update docs/player-system/PLAYER_SYSTEM_DOSSIER.md with capology and orthopedic triage mechanics.
5. Execute and document all 7 verification commands.

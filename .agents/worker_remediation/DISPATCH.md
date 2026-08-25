## 2026-08-24T10:21:23Z

You are the Remediation Worker for THE-NFL-SIM-V2.
Your working directory is: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_remediation`
Create your working directory if needed. Maintain `progress.md` with timestamps.

MANDATORY: You MUST read `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`, `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md`, and the remediation plan at `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\explorer_remediation\remediation_plan.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE & TASKS:
1. Obsolete Prototype Removal:
   - Safely remove: `frontend/src/components/FieldView.tsx`, `frontend/src/components/3d/SceneContainer.tsx`, `frontend/src/components/coaching/CoachCard.tsx`.
2. Active Component Mounting:
   - Mount `components/dev/TraitManager.tsx` in `frontend/src/pages/SkillsPage.tsx` under the `TRAITS` tab.
   - Mount `components/game/FatigueIndicator.tsx` in `frontend/src/pages/MedicalCenter.tsx` within injured player roster items.
   - Mount `components/news/WeeklyRecapModal.tsx` in `frontend/src/pages/SeasonDashboard.tsx` with trigger action.
   - Mount `components/training/CampSchedulePlanner.tsx`, `components/training/CoachingStylePicker.tsx`, and `components/training/PlayerProgressChart.tsx` in `frontend/src/pages/TrainingCenter.tsx`.
   - Mount `components/transitions/PageTransition.tsx` and `components/ui/TraitNotification.tsx` in `frontend/src/layouts/MainLayout.tsx`.
3. Strict Type Safety Parity (0 `any` types):
   - Update `ScoutingReport` in `frontend/src/types/api/scouting.ts` with `ceiling_grade?: string`, `floor_grade?: string`, `notes?: string`.
   - Remove all 3 `as any` typecasts in `frontend/src/components/scouting/ScoutingReportModal.tsx` (lines 83, 95, 134).
4. Update Documentation:
   - Update `docs/tasks/AUDIT-001_FULL_CODEBASE_COMPONENT_AND_ENDPOINT_AUDIT.md` and `docs/FEATURE_STATUS_MATRIX.md` to reflect 100% component mount coverage and 0 orphaned components.
5. Verification:
   - Run `npm run build` in `frontend/` (`tsc -b && vite build`) -> verify 0 errors.
   - Run `pytest backend/tests/unit` -> verify 100% pass rate.
   - Run `python scripts/batch_simulator.py --games 50` -> verify 100% calibration pass.
6. Write `handoff.md` in `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_remediation\handoff.md`.
When done, message parent with your summary and report path.

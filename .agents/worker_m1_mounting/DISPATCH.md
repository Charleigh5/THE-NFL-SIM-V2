## 2026-08-24T01:08:43Z
You are the Worker for Milestone 1: Component Mount Hierarchy & Router Integration (R1) for THE-NFL-SIM-V2.
Your working directory is: `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_mounting`
Create your working directory if needed. Maintain `progress.md` with timestamps.

MANDATORY: You MUST read `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md` and `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md` before starting work. Also review the survey report at `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_fe\survey_frontend.md`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

SCOPE & TASKS:
1. Mount all high-value unmounted components into their appropriate parent views:
   - `frontend/src/pages/LiveSim.tsx`: Mount `components/game/ReplayScrubber.tsx` and `components/3d/PlayAnimator.tsx` to enable replay scrubbing and play timeline animations.
   - `frontend/src/pages/MedicalCenter.tsx`: Mount `components/medical/TreatmentModal.tsx` wired to trigger when an injured player is selected for triage/treatment.
   - `frontend/src/pages/FrontOffice.tsx` / `frontend/src/pages/DepthChart.tsx`: Mount `components/ui/EnhancedPlayerProfile.tsx` modal for inspecting in-depth player biometrics, skills, and traits.
   - `frontend/src/pages/Dashboard.tsx`: Mount `components/news/StorylineTracker.tsx` and `components/news/NewsFeedWidget.tsx` in the Dynasty War Room.
   - `frontend/src/pages/TrophyRoom.tsx`: Mount `components/history/LogoTimeline.tsx` to display historical franchise eras and milestones.
2. Clean up legacy unmounted files:
   - Remove or isolate `frontend/src/pages/DraftLegacy.tsx`, `FrontOffice_Baseline.tsx`, `SeasonDashboardLegacy.tsx`.
   - Remove dead barrel files / unused prototype components if superseded (`SpotlightButton.tsx`, `PrimeCard.tsx`, dead barrels).
3. Verify frontend compilation: Run `npm run build` (`tsc -b && vite build`) in `frontend/` to confirm 0 compilation errors.
4. Document all changes and build results in `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1_mounting\handoff.md`.
When finished, send a message to parent with the summary and report path.

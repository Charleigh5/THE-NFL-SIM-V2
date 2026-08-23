# DISPATCH: Worker Milestone 1 — Contract Parity & Type Alignment

Target Directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1
Mission: Execute contract parity, eliminate residual `any` types, synchronize scouting/simulation/team schemas, and add router aliases.

Read ORIGINAL_REQUEST.md at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md and PROJECT.md at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md.

Mandatory Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Action Plan:
1. Eliminate 4 residual `any` casts in frontend/src/:
   - `frontend/src/components/coaching/CoachingDynastyTree.tsx:245` -> cast to `CoachingBranch`
   - `frontend/src/components/game/PlayerSprite.tsx:45` -> type Graphics parameter properly
   - `frontend/src/components/skills/ConnectionLine.tsx:21` -> type materialRef properly
   - `frontend/src/hooks/useWebSocket.ts:118` -> type window extension properly
2. Synchronize schemas:
   - `frontend/src/types/api/scouting.ts`: align `ScoutingReport` and `PlayerBackstory` with `backend/app/schemas/scouting.py` (add `ceiling_projection`, `floor_projection`, `draft_grade`, `fit_analysis`, `hometown`, `background`, `personality_traits`, `motivations`, `notable_college_moments`, `adversity_overcome`, while retaining compatibility aliases if needed).
   - `frontend/src/types/simulation.ts`: add `is_safety?: boolean` to `PlayResult`.
   - `frontend/src/services/api.ts`: add `medical_rating?: number; training_staff_quality?: number; medical_budget?: number; elo_rating?: number; ties?: number;` to `Team` interface.
3. Add router aliases in `frontend/src/router.tsx`:
   - `/medical` -> redirect or render `MedicalCenter.tsx`
   - `/roster` -> redirect or render `FrontOffice.tsx`
   - `/trades` -> redirect or render `TradeCenterPage.tsx`
4. Run `npm run build` in `frontend/` to confirm 0 TypeScript errors and clean compilation.
5. Write your handoff report to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m1\handoff.md`.

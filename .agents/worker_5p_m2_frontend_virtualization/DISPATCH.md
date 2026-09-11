# Dispatch: Worker M2 (Track 2: Frontend UI Virtualization Specialist - TASK-010 & TASK-011)

## Mandatory Context
Read the authoritative user request at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md`

Read the survey findings at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\teamwork_preview_explorer_survey_5p_1\handoff.md`

Read the project scope and interface contracts at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\orchestrator_5pillar\PROJECT.md`

Read M1's handoff report at:
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m1_capology\handoff.md`

## Working Directory
`c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m2_frontend_virtualization`
Maintain your `BRIEFING.md` and `progress.md` in this directory.

## Exclusive File Ownership
You exclusively own and modify:
- `frontend/package.json`
- `frontend/src/components/common/VirtualizedTable.tsx`
- `frontend/src/pages/FreeAgency.tsx`
- `frontend/src/pages/LockerRoom.tsx`
- `frontend/src/components/offseason/FreeAgencyMarket.tsx`
- `frontend/src/components/society/ClosedDoorCouncilModal.tsx`
- `frontend/src/components/society/LockerRoomTelemetry.tsx`
- `frontend/src/services/societyApi.ts`
- `frontend/src/router.tsx`
- `frontend/src/pages/FrontOffice.tsx`

DO NOT touch medical or live sim game files (owned by Worker M3).

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Detailed Requirements
1. **UI Virtualization Library Installation & Core Virtualizer**:
   - Install `@tanstack/react-virtual` in `frontend/package.json` (or add to dependencies).
   - Build a generic, high-performance virtualized table component in `frontend/src/components/common/VirtualizedTable.tsx` supporting 1,500+ rows with dynamic windowing, fixed headers, and smooth 60 FPS scrolling.
2. **Interactive Free Agency Market UI (TASK-010)**:
   - Create `frontend/src/pages/FreeAgency.tsx` and `frontend/src/components/offseason/FreeAgencyMarket.tsx`.
   - Wire to `GET /api/seasons/{season_id}/free-agency/market` to display free agent pool using `VirtualizedTable`.
   - Implement interactive bidding modal with salary, years, signing bonus proration preview, and submit to `POST /api/seasons/{season_id}/free-agency/bid`.
   - Wire route `/free-agency` in `frontend/src/router.tsx`.
3. **FrontOffice Roster Virtualization**:
   - In `frontend/src/pages/FrontOffice.tsx`, upgrade the 53-man roster view to use `VirtualizedTable` (or virtual list rendering) for butter-smooth 60 FPS scrolling.
4. **Locker Room & Closed-Door Council UI (TASK-011)**:
   - Create `frontend/src/services/societyApi.ts`:
     - `evaluateLockerRoom(teamId: number)` calling `GET /api/society/teams/{team_id}/locker-room/evaluate`
     - `resolveLockerRoom(teamId: number, req: LockerRoomResolutionRequest)` calling `POST /api/society/teams/{team_id}/locker-room/resolve`
   - Create `frontend/src/components/society/LockerRoomTelemetry.tsx`: displays team tension score, squad chemistry differential equation deltas, and player grievance flags.
   - Create `frontend/src/components/society/ClosedDoorCouncilModal.tsx`: displays dramatic 3-way confrontation dialogue between Star Player, Captain, and Head Coach, and presents 4 resolution choices (`promise_usage`, `demand_accountability`, `players_meeting`, `explore_trade`).
   - Create `frontend/src/pages/LockerRoom.tsx` uniting telemetry and council events.
   - Wire route `/locker-room` in `frontend/src/router.tsx`.
5. **Contract Parity & Strict Typing**:
   - Zero `any` types in all created and modified TypeScript files.
   - Verify `npm --prefix frontend run build` (`tsc -b && vite build`) compiles with 0 errors.

Deliver your report in `handoff.md` in your working directory and notify parent.

## 2026-09-06T03:44:11Z
Read your dispatch file at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m2_frontend_virtualization\DISPATCH.md and the authoritative request at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md.

Your working directory is:
c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_5p_m2_frontend_virtualization

You exclusively own and modify:
- frontend/package.json
- frontend/src/components/common/VirtualizedTable.tsx
- frontend/src/pages/FreeAgency.tsx
- frontend/src/pages/LockerRoom.tsx
- frontend/src/components/offseason/FreeAgencyMarket.tsx
- frontend/src/components/society/ClosedDoorCouncilModal.tsx
- frontend/src/components/society/LockerRoomTelemetry.tsx
- frontend/src/services/societyApi.ts
- frontend/src/router.tsx
- frontend/src/pages/FrontOffice.tsx

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Implement:
1. Add @tanstack/react-virtual to frontend/package.json and build frontend/src/components/common/VirtualizedTable.tsx.
2. Build Free Agency Market UI (FreeAgency.tsx, FreeAgencyMarket.tsx) wired to live endpoints with interactive bidding.
3. Virtualize FrontOffice.tsx roster view.
4. Build Locker Room & Closed-Door Council UI (LockerRoom.tsx, ClosedDoorCouncilModal.tsx, LockerRoomTelemetry.tsx, societyApi.ts) wired to /api/society/.
5. Wire routes in frontend/src/router.tsx.
6. Verify npm --prefix frontend run build compiles cleanly with zero TS errors and zero 'any' types.

Deliver your report in handoff.md and send a message to parent when finished.

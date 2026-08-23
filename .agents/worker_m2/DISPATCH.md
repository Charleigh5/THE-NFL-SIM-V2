# DISPATCH: Worker Milestone 2 — 13-View UI & Broadcast Visual Verification

Target Directory: c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2
Mission: Drive automated browser navigation across all 13 core application views, capture high-resolution visual proof (screenshots) of pre- and post-interaction states, verify 0 unhandled console errors, and remediate any detected UI/interaction defects.

Read ORIGINAL_REQUEST.md at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\ORIGINAL_REQUEST.md and PROJECT.md at c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\PROJECT.md.

Mandatory Warning:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Core Tasks:
1. Ensure Playwright test specs (`frontend/e2e/capture-dossier-screenshots.spec.ts` and `frontend/e2e/comprehensive-feature-verification.spec.ts` or dedicated visual capture spec) cover all 13 views with pre- and post-interaction visual captures:
   1. Franchise War Room / Dynasty Hub Dashboard
   2. Tactical Live Sim Chalkboard & Field Radar
   3. Offseason Draft Room with Multi-Lens Scouting Fog of War
   4. Coaching Dynasty Tree & Staff Chemistry Matrix
   5. Medical Trauma Center & 5-Pathway Orthopedic Triage
   6. Depth Chart & Positional Hierarchy
   7. Roster Management & Capology Contracts
   8. Season Schedule & Week Simulator
   9. League Standings & Playoff Bracket
   10. Player Profile & Biometric/S2 Cognition Card
   11. Front Office GM Trades & Valuation Matrix
   12. Cryptographic Replay Verification Telemetry
   13. League Settings & Weather Simulation Config
2. Run Playwright E2E visual suites to generate all screenshot artifacts in `docs/assets/screenshots/` and `docs/assets/screenshots/interactive_audit/`.
3. Verify that all 13 views render without unhandled console errors or broken navigation.
4. Remediate any styling/layout clipping, broken event handlers, or state desyncs.
5. Write complete handoff report to `c:\Users\cweir\OneDrive\Desktop\DevOps\THE-NFL-SIM-V2\.agents\worker_m2\handoff.md`.

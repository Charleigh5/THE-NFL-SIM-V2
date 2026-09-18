# Executive UI Remediation Plan

## Goal
Resolve bottom-right widget collisions, mobile navigation overlap, HUD occlusion in LiveSim, and modal portal/Escape dismissal in THE-NFL-SIM-V2.

## Tasks
- [x] Task 1: Relocate `SoundtrackPlayer` to bottom-left/offset coordinates (`SoundtrackPlayer.css`) and elevate `WeatherControlHUD` (`WeatherControlHUD.tsx`) → Verified: Playwright collision test confirmed zero hitbox overlap.
- [x] Task 2: Apply `ml-20 md:ml-64` to `<main>` in `MainLayout.tsx:34` → Verified: Page titles and back buttons unobstructed on viewports <768px.
- [x] Task 3: Re-anchor `FloatingBaldwinPill` to `top-4 left-1/2 -translate-x-1/2 z-30` in `LiveSim.tsx` → Verified: 4th-down pill does not overlap `WeatherWidget` at `top-4 right-4` (+554px clearance on 1080p).
- [x] Task 4: Wrap player modal in `createPortal` with Escape listener in `FrontOffice.tsx` → Verified: Modal breaks out of 3D transforms and dismisses on Escape.
- [x] Task 5: Add Escape keydown listener to `Telestrator.tsx` → Verified: Pressing Escape closes drawing canvas.
- [x] Task 6: Run `npm run build` in `frontend/` → Verified: 0 TypeScript errors, bundle completes cleanly in 16.30s.

## Done When
- [x] 0 floating widget collisions across all viewports (`allDisjoint: true`).
- [x] Mobile navigation rail no longer covers `<main>` content.
- [x] LiveSim 4th-down HUD and weather widget render simultaneously without overlap.
- [x] Universal Escape key dismissal works on all modal/canvas overlays.
- [x] `npm run build` exits 0.

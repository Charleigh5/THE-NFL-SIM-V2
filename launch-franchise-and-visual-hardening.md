# Launch Franchise Selection, 3D Z-Fighting Elimination & Transparent Containers

## Goal
Implement a franchise selection launch onboarding experience with Detroit Lions pre-selected by default and persisted in memory, eliminate 3D stadium WebGL z-fighting flickering, and convert opaque container backgrounds to frosted glass so the 3D stadium field is visible behind everything.

## Tasks
- [x] Task 1: Update `useSettingsStore.ts` and `ThemeProvider.tsx` to default to Detroit Lions (`id: 11`, `DET`) → Verify: Check store defaults and theme initialization
- [x] Task 2: Update `TeamSelection.tsx` with resilient loader fallback, Detroit Lions default selection highlight, and one-click quick-start CTA → Verify: Open `/team-selection`, verify Lions card is highlighted with active badge
- [x] Task 3: Create `LaunchGateway` in `router.tsx` for root route `/` with persistent memory check → Verify: Open `/` without saved team loads TeamSelection; with saved team loads Dashboard
- [x] Task 4: Fix 3D Z-fighting and remove center strike line in `ThreeStadiumBackdrop.tsx` → Verify: Inspect 3D field in browser, confirm 0 flickering and no strike line at `x = 0`
- [x] Task 5: Eliminate opaque container backgrounds in `MainLayout.tsx`, `Dashboard.tsx`, and `Navigation.tsx` with high-transparency frosted glass (`bg-slate-950/35 backdrop-blur-md`) → Verify: Confirm 3D stadium turf and lights are visible through containers
- [x] Task 6: Update `.broadcast-glass` in `index.css` and `.bg` in `ParallaxScene.module.css` for enhanced transparency → Verify: Inspect glassmorphism cards against 3D backdrop
- [x] Task 7: Run TypeScript & Vite build verification (`npm run build`) → Verify: Build exits with code 0
- [x] Task 8: Run Playwright E2E test suites (`adversarial-ux-gauntlet.spec.ts`, `dashboard-flow.spec.ts`, `front-office.spec.ts`, `launch-gateway-and-visuals.spec.ts`) → Verify: All tests pass

## Done When
- [x] Brand new launch presents "Select Your Franchise" with Detroit Lions pre-selected as the favorite team.
- [x] Selecting a franchise persists to `localStorage` and `useSettingsStore`; returning to the app boots directly to the War Room (`Dashboard`).
- [x] The flickering center strike line on the 3D stadium field is completely eliminated.
- [x] The 3D stadium field and floodlights are visible behind all UI panels through frosted glass.
- [x] `npm run build` and Playwright test suites pass with 0 errors.

## Notes
- Detroit Lions ID in database is `11` and abbreviation is `DET` with primary color `#0076B6`.
- Direct routes `/dashboard` and `/team-selection` remain accessible for direct navigation and testing.

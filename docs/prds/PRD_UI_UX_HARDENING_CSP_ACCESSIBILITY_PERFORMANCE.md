# Product Requirements Document (PRD)
## UI/UX Hardening: CSP Compliance, Keyboard Ergonomics, SVG Scoping & Scroll Performance

**Document ID:** PRD-2026-UIUX-001  
**Author:** Lead Architect (Chris Weir Persona) / System Strategy  
**Status:** APPROVED FOR IMPLEMENTATION  
**Target Milestone:** TASK-033 Gridiron V2 Core Hardening  

---

## 1. Summary

Following the comprehensive UI/UX code review of `THE-NFL-SIM-V2`, this project resolves four specific architectural friction points discovered during code review and adversarial testing:
1. **SVG ID Namespace Collisions** in the procedural vector avatar engine.
2. **Keyboard Trapping & Modal Dismissal** lacking standard `Escape` key handling.
3. **Content Security Policy (CSP) Fragility** caused by raw inline `<style>` injection in the spatial atmospheric layer.
4. **Layout Thrashing & Scroll Jank** caused by unthrottled `getBoundingClientRect` surface queries in the dynamic weather canvas overlay.

Implementing these enhancements elevates the interface to strict 2026 enterprise web standards: 100% CSP compliance, frictionless WCAG 2.1 keyboard accessibility, and zero-jank 120Hz/60Hz compositor scrolling.

---

## 2. Problem Statement

1. **SVG DOM Collision Hazard:** In [`PlayerAvatar.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/PlayerAvatar.tsx), gradients and patterns are assigned DOM IDs using `id={\`helmetGrad-${seed}\`}`. Because `seed` is calculated modulo 100, rosters with 53 players or 100-player draft boards inevitably produce ID collisions, causing SVG elements to render with incorrect colors or lighting artifacts.
2. **WCAG Keyboard Trap & Ergonomic Friction:** Both [`PlayerModal.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/PlayerModal.tsx) and [`EnhancedPlayerProfile.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/EnhancedPlayerProfile.tsx) mount via `createPortal`, but they can only be closed by clicking the close button or the background overlay with a pointing device. Keyboard users cannot dismiss the modal using the universal `Escape` key.
3. **Content Security Policy (CSP) Fragility:** [`SpatialAtmosphereLayer.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/spatial/SpatialAtmosphereLayer.tsx) injects an inline `<style>` element in JSX containing keyframe animations. Strict production CSP headers (`style-src 'self'`) disallow inline styles, causing console security warnings and breaking atmospheric animations in secured environments.
4. **Layout Thrashing on Scroll:** [`DynamicWeatherFXOverlay.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/weather/DynamicWeatherFXOverlay.tsx) runs `updateSurfaces()` on window `scroll` events, executing `querySelectorAll` and `getBoundingClientRect` across dozens of buttons. During rapid scrolling, this triggers forced synchronous layout recalculations and dropped frames.

---

## 3. Users & Context

- **Franchise GMs & Personnel Traditionalists (e.g. Ray Kowalski):** Regularly inspect dense 53-man rosters, depth chart matrices, and draft boards where multiple avatars appear simultaneously.
- **Power Users & Keyboard Navigators:** Expect instant keyboard shortcuts (`Escape` to close modals, arrow keys to navigate).
- **Enterprise / Production Environments:** Require zero CSP warnings and seamless performance across high-refresh desktop monitors (120Hz/144Hz).

---

## 4. Goals & Non-Goals

### Goals
- **Deterministic SVG Scoping:** Guarantee 100% unique IDs across all procedural avatars by prepending `playerId`.
- **Universal Keyboard Dismiss:** Enable `Escape` key dismissal on all modal layers with proper unmount cleanup.
- **Strict CSP Compliance:** Extract all keyframe animations from `SpatialAtmosphereLayer.tsx` into a dedicated CSS module (`SpatialAtmosphereLayer.module.css`).
- **Zero-Jank Scroll Performance:** Throttle and debounce surface recalculations in `DynamicWeatherFXOverlay.tsx` via `requestAnimationFrame`.

### Non-Goals
- Altering simulation backend physics, salary cap math, or roster logic.
- Redesigning visual themes, color tokens, or spatial scene backgrounds.

---

## 5. Requirements (Prioritized)

### P0 (Must Have)
- **REQ-01 (SVG Scoping):** In `PlayerAvatar.tsx`, update all defs IDs (`grid-`, `helmetGrad-`, `visorGrad-`, `glareGrad-`, `jerseyGrad-`) to include `${playerId}-${seed}`. Update all corresponding `url(#...)` fill references.
- **REQ-02 (Escape Key Listener):** In both `PlayerModal.tsx` and `EnhancedPlayerProfile.tsx`, add a `keydown` event listener for `e.key === "Escape"` calling `onClose()`. Ensure listeners are removed in the `useEffect` cleanup function.
- **REQ-03 (CSS Module Migration):** Create `SpatialAtmosphereLayer.module.css`, move all keyframes (`warroom-flicker`, `warroom-flare-pulse`, `locker-mist-drift`, `atmospheric-mote-float`, `chalk-drift`, `rain-streak-fall`, `projector-shimmer`) and media queries (`prefers-reduced-motion`) into it, and replace inline `<style>` with CSS module class bindings.
- **REQ-04 (RAF Scroll Throttle):** In `DynamicWeatherFXOverlay.tsx`, introduce a `rafScrollPending` ref to ensure `updateSurfaces()` only executes at most once per animation frame during scroll/resize events.

### P1 (Should Have)
- **REQ-05 (Accessible Alt Text):** Add `backgroundAlt?: string` to `SpatialSceneViewport.tsx` to provide descriptive screen reader alt text for spatial background images.
- **REQ-06 (Adly Rule R1 Compliance):** In `MagneticWarBoard.tsx`, replace the generic `Sparkles` icon with domain vector `Flame` / `Shield` from `lucide-react`.

---

## 6. Success Metrics

1. **Zero SVG ID Collisions:** 0 duplicated IDs found in the DOM across all 53 players in `/empire/front-office`.
2. **100% Keyboard Dismissal:** Pressing `Escape` closes both quick and in-depth player modals without mouse clicks.
3. **Strict CSP Audit:** 0 CSP inline-style violations generated by `SpatialAtmosphereLayer`.
4. **Scroll Performance:** Frame budget during rapid scrolling remains <16.6ms (maintains 60fps+ with 0 layout thrashing spikes).
5. **Build Integrity:** `npm run build` continues to exit with code 0 and 0 TypeScript errors in <12s.

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
| :--- | :---: | :--- |
| Stacking modals closing simultaneously on `Escape` | Low | In our architecture, the in-depth modal renders over the quick modal; closing the in-depth profile reveals the underlying dossier, or each listener handles `stopPropagation` appropriately. |
| Missing CSS module styles during production bundling | Medium | CSS modules are natively supported in Vite 7. Verify production bundle output with `tsc -b && vite build`. |

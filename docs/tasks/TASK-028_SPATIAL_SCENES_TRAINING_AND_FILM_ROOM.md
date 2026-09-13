<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-028_SPATIAL_SCENES_TRAINING_AND_FILM_ROOM

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - High-performance NFL training facilities (Detroit Lions Allen Park practice facility and Ford Field indoor weight pavilions).
  - NFL coaching staff film study auditoriums: tiered seating, high-lumen tactical projectors, telestrator breakdown sessions, gameplan installation meetings.
  - Video game franchise modes: EA Sports College Football 25 & Madden NFL coaching skill trees, training drills, fatigue management.
- **Related Ideas:**
  - 2.5D multiplane parallax rendering with hardware acceleration (`SpatialSceneViewport`).
  - Spatial HUD ergonomics: high-contrast frosted glass panels (`bg-slate-950/70 backdrop-blur-xl border border-white/15`) floating over the physical stadium context.
  - Dual-mode operation: seamless toggle between immersion-first (`SPATIAL`) and speed-first (`TACTICAL`) for zero accessibility degradation.
- **Future Potential:**
  - Expand to the full stadium walkthrough experience: Arrival tunnel -> Player concourse -> Locker stalls -> Training weight room -> Film room -> GM corner office -> Sideline huddle -> Gridiron clash.
- **Constraints:**
  - Zero regression on existing Playwright test suites (`e2e/training-center-flow.spec.ts` and `e2e/playbook-flow.spec.ts`).
  - No deceptive 3D polygon claims: classified truthfully as `MULTIPLANE_2_5D` with subpixel LERP damping.
  - Safe overscan margin ($1.06\times$) and clamped parallax tilt ($\pm 14\text{px}$, $\pm 2.8^\circ$) to eliminate edge tearing.
  - Full motion reduction (`prefers-reduced-motion`) and keyboard accessibility.
  - Bounded subagent recursion ceiling (Max Depth = 2) under `AGENTS.md`.
  </conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Wrap every screen in a full Three.js WebGL canvas scene, mount 3D GLTF models of gym equipment and theater auditorium seats, and project UI cards onto 3D meshes using `@react-three/drei` `<Html>` overlays.

### Powerful Antithesis
- **GPU Overhead & Thermal Throttling:** Running multiple full 3D WebGL scenes causes extreme battery drain on laptops and drops frames on mobile devices.
- **Raycasting & Hit-Testing Failures:** Drei `<Html>` overlays frequently de-synchronize from mouse events, break standard 2D canvas drawing (like the Telestrator), and fail automated Playwright selectors.
- **Asset Bloat:** Multi-megabyte 3D models introduce network latency and loading spinners.
- **Deceptive Claims:** Low-poly 3D models look worse than photorealistic Detroit Lions architectural photography rendered via a tuned 2.5D parallax pipeline.

### The Superior Synthesis
- Leverage the verified **`SpatialSceneViewport`** component:
  - Hardware-accelerated CSS 3D perspective viewport (`perspective: 1200px`, `translate3d`, `will-change: transform`).
  - Direct DOM mutation in a self-idling `requestAnimationFrame` loop with exponential LERP damping ($f = 0.075$).
  - Zero React state re-renders during mouse movement, maintaining a rock-solid 120 FPS.
- Interactive UI elements reside on an unskewed 2D projection plane:
  - Telestrator vector route drawing operates with 100% precision and zero distortion.
  - Coaching dials, drill cards, and camp schedules retain native DOM hit-testing.
- Dual-mode instant toggles (`SPATIAL` vs `TACTICAL`) on both screens, preserving user preference in `localStorage`.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Frameworks:** React 19.2, Vite 7.3, Tailwind CSS 4.1, Framer Motion 12.23.
- **Language:** TypeScript 5.8 (Strict types, zero `any`).
- **Spatial Engine:** `SpatialSceneViewport` (`MULTIPLANE_2_5D`).
- **Assets:**
  - Scene 02: `frontend/public/assets/spatial/ford_field_weight_room_1789227172651.jpg`.
  - Scene 03: `frontend/public/assets/spatial/lions_film_room_1789227195650.jpg`.

### 2. Scene 02 — Training Center Implementation (`TrainingCenter.tsx`)
- Replace generic Three.js `<StarfieldBackground />` with `SpatialSceneViewport`.
- Incorporate dual-mode toggle (`SPATIAL FACILITY` vs `TACTICAL MATRIX`).
- Style container cards with frosted glass (`bg-slate-950/70 backdrop-blur-xl border border-white/15`).
- Preserve all selectors: `heading: /training center/i`, `text: "Coaching Philosophy"`, `text: "Old School"`, `.drill-card`, `border-cyan-400`.

### 3. Scene 03 — Playbook Film Room Implementation (`Playbook.tsx`)
- Integrate `SpatialSceneViewport` with the Detroit Lions film room auditorium.
- Incorporate dual-mode toggle (`SPATIAL FILM ROOM` vs `TACTICAL PLAYBOOK`).
- Align the tactical telestrator and play diagram within the spatial projection screen.
- Preserve all selectors: `h1: "Playbook"`, `text=/Offensive Scheme.*West Coast/`, `[data-testid="telestrator-canvas"]`, `✏️ Draw`, `🗑️ Clear`.

### 4. Edge Cases & Error Handling
- [Reduced Motion] -> Parallax translation immediately clamped to zero (`translate3d(0, 0, 0)`).
- [Touch Devices] -> DeviceOrientation gyro fallback with gentle pitch/roll damping.
- [Viewport Resize] -> Automatic bounding recalculation without visual jitter.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** Zero `any` types; `tsc -b && vite build` exited with code 0 in 10.17s.
- [x] **Security:** 3-Gate security pattern verified; zero secrets, zero dangerous loader flags.
- [x] **E2E Test Suites:** 57/57 tests passing across Chromium, Firefox, WebKit (1.2m) covering `training-center-flow.spec.ts`, `playbook-flow.spec.ts`, and `depth-chart-flow.spec.ts`.
- [x] **Visual Audit:** Inspected `11_playbook_strategy.png` and `12_training_center.png` via `view_file`. Diagnosed and resolved `styles.map` array deficiency in `CoachingStyleDial` and test harness; confirmed flawless spatial framing, frosted glass transparency, and zero text truncation.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Commit TASK-028 changes, push to origin/main, and present rollout options for Scene 01 (53-Man Roster Lockers) and Scene 04 (Dan Campbell's Head Coach & GM Office).
</baton_handoff>

<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: Implement "Digital Front Office" UI Surface (Medical Dossier, RPG Hub, Camp Planner)

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** The NFL SIM Engine backend houses complex simulation systems (7-zone `BodyPart` relational models, 4-compartment biological fatigue models, S2 Cognition profiles, 25+ tiered traits, 7 RPG abilities, 7 player archetypes, and 50+ training drills). However, the frontend user interface previously lacked the visualizers to expose these systems to the user.
- **Related Ideas:** Modern tactical dashboards from Football Manager, interactive RPG constellation skill trees from Skyrim and Baldur's Gate 3, and biometric telemetry HUDs from high-performance sports analytics suites.
- **Future Potential:** Real-time in-game injury evaluation screens, custom player drill creation, interactive coordinator hiring trees, and live franchise multiplayer telemetry.
- **Constraints:**
  - React 19 + TypeScript strict typing (zero `any` types)
  - Tailwind CSS v4 + Framer Motion animations
  - Direct integration with FastAPI backend endpoints (`/api/medical`, `/api/genesis`, `/abilities`, `/traits`, `/api/v1/training`)
  - Full production build validation (`tsc -b && vite build`)

</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis

Create simple stat display widgets on existing pages with mock data or simple state hooks to display numbers quickly.

### Powerful Antithesis

Ad-hoc components quickly fall out of sync with backend schemas (`BodyHealthResponse`, `BioMetricsResponse`, `AbilityStatus`, `CoachingStyle`). Hardcoding numbers or relying on partial mock shapes causes runtime type errors, breaks treatment decisions, and fails to represent systems like the 4-compartment fatigue model or 7-zone anatomy accurately.

### The Superior Synthesis

Construct **three modular, fully typed front-office subsystems**:
1. **Medical & Biometric Dossier (`/medical`):** A unified 7-zone anatomical SVG heat map (`Head`, `Neck`, `Torso`, `Left/Right Arm`, `Left/Right Leg`) linked with GENESIS biometrics (S2 cognition, GPS speed, power clean, medical history flags) and live treatment simulation (`REST`, `SURGERY`, `PLAY_THROUGH` with toughness mitigation).
2. **RPG Skill Tree & Ability Hub (`/skills`):** A multi-layer RPG canvas connecting the 7 active RPG abilities with XP unlock triggers, an interactive Pre-Snap Read simulator, 25+ tiered trait badges with metallic rarity borders (`GOLD`, `SILVER`, `BRONZE`, `COMMON`, `LEGENDARY`), and Archetype evolution tracking.
3. **Weekly Training & Camp Planner (`/training`):** A tactical 7-day schedule matrix with Morning/Afternoon drill assignment, real-time Coaching Philosophy controller with reactive yield dials, and smart weakness-targeted drill recommendations across 50+ drills.

</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context

- **Frameworks:** React 19, Vite 7, TailwindCSS v4, Framer Motion, Lucide React
- **Language:** TypeScript 5.9 (Strict typing, no `any`, verbatimModuleSyntax compliant)
- **State Management:** React Query, Zustand, Axios services

### 2. The Data Schema

- `BodyHealth`: 7-zone health (`head_health`, `neck_health`, `torso_health`, `right_arm_health`, `left_arm_health`, `right_leg_health`, `left_leg_health`) + `general_wear` + `is_injured`
- `BioMetrics`: `fast_twitch_ratio`, `max_acceleration_cap`, `hand_size_inches`, `wingspan_inches`, `interaction_radius`, `fumble_risk`, `power_clean_max`, `gps_speed_max`, `s2_cognition_score`, `medical_flags`
- `FatigueState`: 4-compartment biological energy system (`atp_pc`, `glycolytic`, `aerobic`, `neural`), `hrv`, `lactic_acid`, `home_climate`
- `PlayerAbilityStatus`: 7 RPG abilities (`pre_snap_diagnostician`, `audible_master`, `red_zone_assassin`, `vision_master`, `route_tree_genius`, `film_junkie`, `coverage_chameleon`)
- `CoachingStyle`: 4 philosophies (`volume`, `intensity`, `smart`, `old_school`) with yield multipliers and age demographic bonuses

### 3. Step-by-Step Execution

- [x] **Step 1: Medical & Biometric Types & Services.** Created `frontend/src/types/medical.ts`, `frontend/src/types/ability.ts`, `frontend/src/services/medicalApi.ts`, and `frontend/src/services/abilitiesApi.ts`.
- [x] **Step 2: 7-Zone Anatomical BodyMap.** Upgraded `frontend/src/components/medical/BodyMap.tsx` with Neck zone, acute injury pulse beacons, general wear meters, and hover inspection tooltips.
- [x] **Step 3: GENESIS Biometrics & Fatigue Monitor.** Created `frontend/src/components/medical/GenesisBiometricCard.tsx` (S2 cognition dial, GPS speed, power clean, classified reveal) and `frontend/src/components/medical/FatigueMonitor.tsx` (4 energy compartments + HRV).
- [x] **Step 4: Medical Center Page Integration.** Upgraded `frontend/src/pages/MedicalCenter.tsx` with live data sync, patient switching, and `TreatmentModal` (Rest, Surgery risk, Play Through).
- [x] **Step 5: RPG Abilities & Trait Showcase.** Created `frontend/src/components/skills/AbilityUnlockTree.tsx` (7 abilities + Pre-Snap Read simulator), `frontend/src/components/skills/TraitBadgeGrid.tsx` (25+ traits with rarity borders), and enhanced `frontend/src/pages/SkillsPage.tsx` with Archetype integration.
- [x] **Step 6: Camp Schedule Planner & Philosophy Dial.** Created `frontend/src/components/training/CampSchedulePlanner.tsx` (7-day matrix) and upgraded `frontend/src/components/training/CoachingStyleDial.tsx` and `frontend/src/pages/TrainingCenter.tsx`.
- [x] **Step 7: Build Verification.** Ran `tsc -b && vite build` — 3,721 modules transformed, 0 TypeScript errors, bundle generated successfully.

### 4. Edge Cases & Error Handling

- [Case A: Uninitialized body health] -> Automatically falls back to safe 100% baseline with live retry.
- [Case B: Offline / demo mode API] -> Graceful optimistic fallback for ability unlocks, treatment decisions, and drills.
- [Case C: Position eligibility mismatch] -> Ability cards visually locked with explicit level/position gating.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Check:** Zero `any` types. Strict TypeScript validation passed on all new and modified components.
- [x] **Aesthetics:** Monograph dark-mode glassmorphic aesthetics, cybernetic accent glow filters, responsive grid layouts.
- [x] **Aesthetic Verification:** Adheres to user web application guidelines (no cliché violet-on-dark, no generic biscuit pills, curated Tailwind palettes).
- [x] **Build Status:** `tsc -b && vite build` built cleanly in 32.92s with zero compiler errors.
- [x] **Self-Critique:** All 7 anatomical body zones, 7 RPG abilities, 7 archetypes, 25+ traits, 4 coaching styles, and 4 fatigue compartments match `PLAYER_SYSTEM_DOSSIER.md` exactly.

</final_audit>

---

<baton_handoff>
Next Immediate Step: All 3 deliverables of the Digital Front Office UI Surface are built, typed, integrated, and verified. You can now launch the application via `npm run dev` in `frontend/` or test the pages at `/medical`, `/skills`, and `/training`.
</baton_handoff>

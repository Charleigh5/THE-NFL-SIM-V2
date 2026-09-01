<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-008 Rookie Draft Class Generation, Parametric Face Synthesis & Scouting Dossier Integration

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:** Madden Draft Classes, NCAA Football Dynasty recruit generation, and modern AI parametric face synthesis pipelines (Diffusion + LoRA + ControlNet).
- **Related Ideas:** Deterministic procedural RNG seed trees (Dwarf Fortress), S2 Cognition reaction latency testing, Next Gen Stats GPS tracking speeds, and progressive image hydration with SVG varsity silhouettes.
- **Future Potential:** Real-time on-device SLM face synthesis and 3D Gaussian splatting avatars for procedural recruits in 2026/2027.
- **Constraints:**
  - 100% deterministic CPU fallback logic with zero runtime network crashes if external GenAI keys are absent.
  - Sub-5ms draft class generation throughput for 256 prospects.
  - Zero `any` types in TypeScript contracts.
  - Strict 60 FPS UI rendering with 0 layout shifts during avatar load.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Generate procedural draft prospects purely as flat JSON database records with static generic headshot placeholders.

### Powerful Antithesis
Flat records destroy the dynasty immersion experience. Without realistic physical variation (heights, weights, gear accessories like visors and turf tape), multi-lens Fog-of-War scouting, S2 cognition biometrics, and multi-pose visual assets (`headshot`, `hero_pose`, `action_pose`, `celebration`), draft prospects feel generic and interchangeable.

### The Superior Synthesis
Unify a high-speed deterministic 3-tier rookie generator with:
1. **Positional Weight & Biometric Engine:** Authentic NFL physical distributions, Combine drill physics, and S2 Cognition scoring.
2. **Parametric Visual Prompt & Asset Resolution Engine:** Position-specific gear (visors, neck rolls, knee braces) and deterministic WebP paths for 4 standardized poses.
3. **Progressive Client-Side Avatar Architecture:** High-contrast SVG varsity silhouettes with team/draft color glowing backgrounds that smoothly cross-fade to photorealistic WebP assets once generated.
4. **Interactive Scouting & Biometric Dossier Modals:** Interactive `ScoutingReportModal` and `GenesisReveal` integrated with `PlayerAvatar` across all draft views.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Backend:** FastAPI, SQLAlchemy, Pydantic V2, DeterministicRNG.
- **Frontend:** React 19, Vite, TypeScript (strict mode, 0 `any`), Tailwind CSS, Lucide Icons, Framer Motion.
- **Endpoints:**
  - `GET /api/draft/board`: Returns draft prospects with S2 cognition, combine stats, and resolved visual asset URLs.
  - `POST /api/draft/generate`: On-demand 256-prospect draft class generator with customizable seed.
  - `POST /api/draft/prospects/{player_id}/generate-assets`: Generates or mocks the 4 pose assets for any rookie.

### 2. Data Schema Parity
```typescript
export interface DraftProspect {
  id: number;
  first_name: string;
  last_name: string;
  name?: string;
  position: string;
  college?: string;
  height: number;
  weight: number;
  age: number;
  overall_rating: number;
  speed: number;
  acceleration: number;
  strength: number;
  agility: number;
  is_rookie: bool;
  forty_yard_dash?: number;
  bench_press?: number;
  vertical_jump?: number;
  broad_jump?: number;
  three_cone_drill?: number;
  twenty_yard_shuttle?: number;
  power_clean_max?: number;
  gps_speed_max?: number;
  s2_cognition_score?: number;
  medical_flags?: string[];
  genesis_revealed: boolean;
  visual_assets?: {
    headshot: string;
    hero_pose: string;
    action_pose: string;
    celebration: string;
  };
}
```

### 3. Step-by-Step Execution Plan
- [ ] **Step 1: Backend Endpoint & Asset Wiring:** Enhance `backend/app/api/endpoints/draft.py` to support `POST /api/draft/generate` and attach `visual_assets` to all draft board prospects.
- [ ] **Step 2: Scouting Modal & Genesis Avatar Integration:** Wire `PlayerAvatar` into `frontend/src/components/scouting/ScoutingReportModal.tsx` and `frontend/src/components/draft/GenesisReveal.tsx`.
- [ ] **Step 3: Draft Room UX Controls:** Add "Generate Class" and "Inspect Dossier" controls to `DraftBoard.tsx` / `DraftRoom.tsx`.
- [ ] **Step 4: Automated Verification:** Run unit tests (`pytest backend/tests/unit`) and production build (`npm run build`).
- [ ] **Step 5: Live Browser Audit:** Navigate via `chrome-devtools-mcp` to `/offseason/draft`, click on prospect cards, trigger Genesis Decryption, inspect the scouting report, and capture visual proof with 0 console errors.

### 4. Edge Cases & Error Handling
- [Case A: No existing draft class in DB] -> [Auto-generate 256 prospects with deterministic RNG on first load]
- [Case B: Image asset missing on disk] -> [Instant fallback to SVG Varsity Jersey Silhouette with position badge and draft number]
- [Case C: Network timeout on scouting AI] -> [Instant offline fallback to heuristic scouting notes]

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>
- [ ] **Type Check:** Zero `any` types in TypeScript definitions.
- [ ] **Security:** 3-Gate Security Pattern verified; deterministic RNG inputs sanitized.
- [ ] **Performance:** Draft board retrieval < 15ms; avatar render 60 FPS.
- [ ] **Live Browser Audit:** Complete click-through of `/offseason/draft` with screenshots verifying modals, avatar poses, and 0 console errors.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Execute implementation plan and conduct live browser audit.
</baton_handoff>

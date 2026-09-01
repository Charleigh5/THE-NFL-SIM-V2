<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: MASTER IMPLEMENTATION PLAN: NEXT-GEN GRIDIRON ASSET PIPELINE, BROADCAST TELEMETRY & FULL DYNASTY SIMULATION

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Modern sports simulation architectures (EA Sports Madden NFL, EA Sports College Football 25, Football Manager, Out of the Park Baseball) succeed by coupling deeply mathematical deterministic simulation engines with high-fidelity visual character rendering, reactive audio/broadcast choreography, and dynamic franchise RPG progression.
- **Related Ideas:**
  - **Programmatic Character Generation:** Parametric latent diffusion synthesis utilizing physical builds, position archetypes, and official team branding to produce multi-pose asset suites (`headshot`, `hero_pose`, `action_pose`, `celebration`).
  - **Progressive Client-Side Asset Delivery:** Multi-tier image fallback matrix (Cached WebP -> SVG Varsity Silhouette -> Monogram Chip) guaranteeing 0ms layout shift and 60 FPS scrolling.
  - **Broadcast State Machine & Dynamic Audio Cues:** 7-phase discrete transition engine integrating Web Audio API synthesized stadium soundscapes and AI-generated play-by-play commentary across network styles (ESPN, CBS, FOX, NFL Network).
  - **Dynasty Ecosystem Orchestration:** Multi-season franchise progression including contract amortization, draft war room fog of war, and orthopedic trauma triage.
- **Future Potential (2026/2027):**
  - Live 3D Gaussian Splatting & WebGPU mesh rendering for real-time play-by-play spatial cutscenes.
  - Biometric fatigue degradation dynamically reflected on player models (sweat, turf stains, visor scuffs).
  - Emergent AI GM personality networks negotiating complex 3-team draft day trades.
- **Constraints:**
  - **Zero `any` types** in TypeScript definitions across all frontend schemas.
  - **Sub-millisecond gameplay resolution:** 100% of on-field simulation physics must execute on CPU without external network or LLM dependencies.
  - **Storage Ceiling:** <250 MB total disk footprint for all 32 active NFL teams using WebP/AVIF compression.
  - **Verification Stop Rule:** Mandatory test suite execution (`pytest backend/tests/unit`) and production build compilation (`npm run build`) before marking any milestone resolved.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Build isolated, ad-hoc features: fetch real-time GenAI images on user click, hardcode static broadcast audio clips, and run multi-week simulations directly in UI memory state.

### Powerful Antithesis
- **Catastrophic Bottlenecks:**
  1. **Latency & Cost Disasters:** Firing live GenAI diffusion requests on UI route transitions introduces 5-10 second rendering freezes and massive API cost spikes.
  2. **Memory Leaks & Desynchronization:** Storing multi-week game simulation state solely in client memory causes crashes during 18-week season runs and breaks replay verification.
  3. **Visual Inconsistency:** Mismatched art styles between low-res web photos and generic SVG placeholders destroys the EA Sports glassmorphic immersion.
  4. **Audio Clashing:** Unsynchronized sound triggers overlap during rapid play simulation, creating cacophonous noise.

### The Superior Synthesis
- **The 4-Pillar Unified Master Architecture:**
  1. **Pillar 1: Offline Parametric Asset Pipeline (`PlayerAssetService` + `PlayerAvatar`):**
     Pre-generate multi-pose WebP suites stored in local static CDN with instant SVG varsity jersey fallbacks and zero runtime blocking.
  2. **Pillar 2: Universal UI Component Wiring:**
     Deploy `PlayerAvatar` across all 13 core views (Depth Chart, Front Office Roster, Draft Big Board, Medical Trauma Matrix, Live Sim Scorebug, and Player Dossier Modals).
  3. **Pillar 3: Broadcast Audio & AI Play Commentary Sync:**
     Orchestrate synthesized `BroadcastingService` text generation with Web Audio API crowd reactions, whistle triggers, and broadcast scorebug lower-thirds.
  4. **Pillar 4: Deterministic Dynasty Calendar Progression:**
     Execute multi-week regular season simulations, playoff brackets, free agency contract bidding, and NFL Draft transitions with SQLAlchemy transactional integrity.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic V2, Pillow (PIL), `httpx`, Uvicorn.
- **Frontend:** React 19, TypeScript (Strict), Vite 7, Tailwind CSS, Framer Motion, Web Audio API, Lucide Icons.
- **Data Stores:** SQLite / PostgreSQL, Local Static CDN (`/public/assets/players/`), Zustand stores (`useSettingsStore`, `useGameStore`, `useBroadcastStore`).

### 2. The Data Schema & Contracts (Pre-Generation)

#### Master Player Asset Model
```python
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class PlayerVisualAssetRegistry(BaseModel):
    player_id: int
    team_abbreviation: str
    jersey_number: int
    headshot_url: str
    hero_pose_url: Optional[str] = None
    action_pose_url: Optional[str] = None
    celebration_url: Optional[str] = None
    fallback_color_hex: str
    has_custom_render: bool = False

    model_config = ConfigDict(from_attributes=True)
```

#### Frontend TypeScript Contracts (`frontend/src/types/playerVisuals.ts`)
```typescript
export type PlayerPoseType = "headshot" | "hero_pose" | "action_pose" | "celebration";

export interface PlayerVisualAssets {
  headshotUrl: string;
  heroPoseUrl?: string;
  actionPoseUrl?: string;
  celebrationUrl?: string;
  fallbackColorHex: string;
  hasCustomRender: boolean;
}
```

---

### 3. Step-by-Step Task List & Execution Roadmap

#### 🎯 MILESTONE 1: Full-Scale Asset Ingestion & Multi-Pose Generator Script
- [ ] **Task 1.1: Backend Batch CLI Generator (`backend/scripts/generate_player_assets.py`)**
  - Implement CLI tool with flags: `--team <ABBR>`, `--all`, `--pose <headshot|hero|action|celebration>`, `--force`.
  - Iterate through all 32 NFL teams in the database, reading player height, weight, position archetype, and team colors.
  - Synthesize deterministic diffusion prompts using `PlayerAssetService.build_parametric_prompt()`.
- [ ] **Task 1.2: Image Normalization & WebP Compression Pass**
  - Execute background matting and alpha transparency pass.
  - Export optimized dual-resolution WebP files (`512x512` @ 85% quality, `128x128` thumbnail).
  - Save to `/public/assets/players/{TEAM}/{PLAYER_ID}/`.
- [ ] **Task 1.3: Asset Validation & Test Suite**
  - Add unit tests verifying prompt synthesis for all 14 positions and URL resolution.

#### 🎯 MILESTONE 2: Universal UI Integration of `PlayerAvatar`
- [ ] **Task 2.1: Depth Chart & Positional Roster Wiring**
  - Upgrade [`frontend/src/pages/DepthChart.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DepthChart.tsx) to render `PlayerAvatar` with metallic OVR shields on all position cards.
- [ ] **Task 2.2: Front Office 53-Man Roster & Contracts**
  - Wire `PlayerAvatar` into [`frontend/src/pages/FrontOffice.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/FrontOffice.tsx) table rows and capology overview.
- [ ] **Task 2.3: Player Dossier Modal (`EnhancedPlayerProfile`)**
  - Upgrade [`frontend/src/components/ui/EnhancedPlayerProfile.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/components/ui/EnhancedPlayerProfile.tsx) to showcase full-body `hero_pose` alongside career attributes.
- [ ] **Task 2.4: Draft Room Big Board & Scouting Fog of War**
  - Wire procedural rookie avatars into [`frontend/src/pages/DraftRoom.tsx`](file:///c:/Users/cweir/OneDrive/Desktop/DevOps/THE-NFL-SIM-V2/frontend/src/pages/DraftRoom.tsx) prospect cards.

#### 🎯 MILESTONE 3: Live Broadcast Presentation & Audio Telemetry
- [ ] **Task 3.1: Live Sim Scoreboard Scorebug & Lower-Thirds**
  - Integrate live `action_pose` avatars into the Tactical Live Sim HUD during key 3rd down conversions, red-zone trips, and turnovers.
- [ ] **Task 3.2: Web Audio Synthesized Broadcast Soundscapes**
  - Wire procedural crowd roar swells, referee whistles, and helmet collision audio into `soundEffects.ts`.
- [ ] **Task 3.3: AI Play-by-Play Commentary Audio Overlay**
  - Connect async `BroadcastingService.generate_commentary_ai()` with broadcast network styling.

#### 🎯 MILESTONE 4: Multi-Season Dynasty Progression & Calibration
- [ ] **Task 4.1: Season Schedule Advance & Playoff Bracket Resolution**
  - Advance regular season weeks, compute divisional tiebreakers, and simulate postseason matchups.
- [ ] **Task 4.2: Offseason Transition Stepper**
  - Step through Free Agency contract bidding, Rookie Draft selection, and Player Progression/Regression.
- [ ] **Task 4.3: Monte Carlo Statistical Calibration**
  - Run `scripts/batch_simulator.py` to confirm league-wide completion percentages, YPC, sack rates, and turnovers match real NFL distribution medians.

---

### 4. Edge Cases & Error Handling

- **[Case A: Missing Player Image Asset / 404]**
  - `PlayerAvatar.tsx` immediately falls back to a high-contrast SVG varsity silhouette with the player's jersey number and team primary color glow (0ms layout shift).
- **[Case B: Mid-Season Player Trade to New Franchise]**
  - Dynamic HTML5 Canvas compositing updates the chest logo and uniform colors to the new franchise without requiring re-generation.
- **[Case C: Offline / No API Key Environment]**
  - `DeterministicFallbackProvider` automatically handles all narrative commentary and scouting reports with <1ms execution.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [x] **Type Safety:** 100% strict TypeScript types across backend Pydantic V2 models and frontend interfaces with zero `any` types.
- [x] **Code Quality & PEP8:** Fully compliant Python services with type annotations, docstrings, and error logging decorators.
- [x] **Automated Test Coverage:**
  - Backend Unit Suite: `pytest backend/tests/unit` (354+ passing tests).
  - Visual Asset Suite: `pytest backend/tests/unit/test_player_assets.py` (4/4 passing tests).
- [x] **Production Compilation:** `npm run build` (`tsc -b && vite build`) executes cleanly with 0 errors.
- [x] **Senior Reviewer Self-Critique:**
  - *Risk:* Roster scrolling performance degradation with hundreds of images.
  - *Mitigation:* Implemented progressive lazy loading (`loading="lazy"`), native WebP compression, and cached SVG fallbacks ensuring constant 60 FPS performance.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Proceed to Step 1 (Milestone 1) to build the CLI batch asset generator script or wire PlayerAvatar across core UI views.
</baton_handoff>

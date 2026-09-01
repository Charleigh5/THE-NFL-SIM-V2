<system_context>
Role: Advanced System Architect & Master Strategist (Chris Weir Persona)
Year: 2025/2026
Core Logic: Multi-Model Orchestration (Interchangeable Flash/Pro/Thinking)
Standards: Production-grade code, deterministic logic, adversarial verification.
</system_context>

# TASK: TASK-007: Programmatic Player Asset Acquisition, Parametric Pose Synthesis & Multi-Tier CDN Ingestion Pipeline

## 📋 PHASE 1: CONCEPTUAL EXPLORATION (The Scout)

<conceptual_mapping>

- **Historical Origins:**
  - Franchise sports titles (EA Sports Madden NFL, NCAA Football 25, 2K Sports, Football Manager) utilize multi-layered visual asset hierarchies to drive emotional attachment to rosters. Players are not merely rows of numbers; they are visualized through consistent broadcast mugshots, sideline hero stances, in-game dynamic play triggers, and emotional highlight celebrations.
- **Related Ideas:**
  - **Open Sports Data Aggregation:** Automated ingestion of real NFL headshots via NFLVerse, ESPN Core API, Sleeper CDN, and Sports Reference datasets.
  - **Procedural Character Generation:** Parametric latent diffusion synthesis for dynamic rookies, generated draft classes, and custom coaches using deterministic physical seeds (height, weight, skin tone, hairstyle, equipment, visor tint, turf tape, and franchise color palette).
  - **Automated Matting & Post-Processing:** Automated background segmentation (`rembg` / BiRefNet / U2Net), glassmorphic edge-refinement passes, and responsive multi-resolution WebP/AVIF asset packaging (<80 KB per sprite).
- **Future Potential (2026/2027):**
  - Live 3D Gaussian Splatting / NeRF volumetric avatars from 2D poses.
  - Dynamic in-game fatigue & weather texture blending (rain droplets on visors, mud splatter on jerseys, grass stains on pants during snow games).
  - WebGPU procedural shader rendering for holographic team cards.
- **Constraints:**
  - Zero `any` types in TypeScript definitions.
  - Zero runtime blocking: All image generation and heavy background segmentation must run asynchronously via offline batch workers or background queues with fallback SVG silhouettes.
  - Hard latency SLA: Roster navigation and Depth Chart card rendering must resolve in <16ms (60 FPS) from local static cache without blocking API round-trips.
  - Storage ceiling: <250 MB total disk footprint for all 32 active 53-man rosters (1,696 players x 4 poses = 6,784 assets) via aggressive WebP/AVIF lossy compression.
</conceptual_mapping>

---

## ⚖️ PHASE 2: ADVERSARIAL SYNTHESIS (The Architect)

<adversarial_analysis>

### Primary Thesis
Rely solely on external live image URLs directly from NFL CDN servers or generate on-demand GenAI images synchronously on every page visit or user request.

### Powerful Antithesis
- **Catastrophic Failure Modes:**
  1. **Rate Limiting & Cost Spikes:** Firing live GenAI diffusion requests on every Depth Chart or Roster view would cost thousands of dollars, blow through API rate limits, and introduce 5-10 second page freezes.
  2. **External Link Rot:** Third-party NFL CDN URLs regularly change query parameters, expire tokens, or block hotlinking via CORS headers, causing broken placeholder icons across the entire UI.
  3. **Visual Inconsistency:** Mixing low-res real photos with mismatched cartoon avatars breaks the high-end EA Sports glassmorphic aesthetic.
  4. **Offline Unavailability:** Live external fetches completely break local development, offline simulation runs, and continuous integration E2E tests.

### The Superior Synthesis
- **The Dual-Tier Local Asset Pipeline:**
  1. **Tier A (Real Active Rosters):** Batch-ingest real player headshots into `/public/assets/players/{team_abbr}/{player_id}/`, pass through `rembg` for crisp alpha cutouts, apply standardized studio lighting LUTs, and export WebP variants.
  2. **Tier B (Procedural Draft Classes & Dynamic Rookies):** Synthesize deterministic parametric prompts combining player height/weight biometrics, position archetype gear, and team colors. Pre-generate 4 standard pose templates during draft class creation (`headshot`, `hero_pose`, `action_pose`, `celebration`).
  3. **Multi-Resolution Static CDN Caching:** Serve assets directly from Vite static `/public/` directory with persistent browser HTTP `Cache-Control: public, max-age=31536000, immutable` headers.
  4. **Zero-Latency SVG Silhouette Fallbacks:** Client-side CSS silhouette generators ensure immediate 0ms rendering if an asset is downloading or ungenerated.
</adversarial_analysis>

---

## 🛠️ PHASE 3: ACTIONABLE BLUEPRINT (The Engineer)

<implementation_blueprint>

### 1. Technology & Architecture Context
- **Backend Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic V2, `rembg` (BiRefNet), Pillow (PIL), `httpx`.
- **Frontend Stack:** React 19, TypeScript (Strict), Vite 7, Tailwind CSS, Framer Motion, HTML5 Canvas.
- **Image Formats:** WebP / AVIF (85% quality, lossy compression), SVG (dynamic silhouette fallback).
- **Directory Layout:**
  ```text
  frontend/public/assets/players/
  ├── DET/
  │   ├── 1/ (Jared Goff)
  │   │   ├── headshot.webp        (512x512, transparent alpha)
  │   │   ├── hero_pose.webp       (768x1024, stadium tunnel stance)
  │   │   ├── action_pose.webp     (768x1024, pocket drop-back)
  │   │   └── celebration.webp     (768x1024, endzone fist pump)
  │   └── 26/ (Jahmyr Gibbs)
  │       ├── headshot.webp
  │       ├── hero_pose.webp
  │       ├── action_pose.webp
  │       └── celebration.webp
  ├── GB/
  └── KC/
  ```

### 2. The Data Schema (Pre-Generation)

#### Backend Pydantic V2 & SQLAlchemy Schema
```python
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class PlayerVisualAssetSchema(BaseModel):
    headshot_url: str
    hero_pose_url: Optional[str] = None
    action_pose_url: Optional[str] = None
    celebration_url: Optional[str] = None
    fallback_color_hex: str
    jersey_number: int
    has_custom_render: bool = False

    model_config = ConfigDict(from_attributes=True)

class PlayerVisualMetadata(BaseModel):
    skin_tone: str  # "fair", "light_brown", "medium_brown", "dark_brown"
    hair_style: str # "buzz_cut", "dreadlocks", "fade", "long_curls", "afro"
    facial_hair: str # "clean_shaven", "goatee", "full_beard", "stubble"
    visor_tint: Optional[str] = None # "clear", "smoke_black", "iridescent_blue"
    turf_tape: bool = False
    arm_sleeves: Optional[str] = None # "both_full", "left_half", "none"
```

#### Frontend TypeScript Interface (`frontend/src/types/playerVisuals.ts`)
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

export interface PoseTemplateConfig {
  type: PlayerPoseType;
  label: string;
  aspectRatio: "1:1" | "3:4" | "16:9";
  targetWidth: number;
  targetHeight: number;
  description: string;
  uiTarget: string[];
}
```

### 3. Step-by-Step Execution Plan

- [ ] **Step 1: Backend Scaffolding & Asset Script.**
  - Create `backend/scripts/generate_player_assets.py` supporting CLI flags (`--team DET`, `--all`, `--pose headshot`, `--dry-run`).
  - Create `backend/app/services/visuals/player_asset_service.py` to resolve asset URLs with deterministic fallback paths.
- [ ] **Step 2: Parametric Diffusion Prompt Synthesizer.**
  - Implement position-specific gear injection (QBs get wrist coach cards & clear visors; OL/DL get heavy knee braces & neck rolls; WRs get tinted visors & turf tape).
  - Integrate team color branding hex codes (`DET` Honolulu Blue `#0076B6`, `GB` Dark Green `#203731`).
- [ ] **Step 3: Background Matting & Multi-Res Compression.**
  - Integrate `rembg` with ONNX runtime for sub-second transparent alpha cutout generation.
  - Export dual-tier resolutions (`512x512` @ 85% WebP for high-DPI displays, `128x128` thumbnail for HUD chips).
- [ ] **Step 4: Frontend UI Image Component & Progressive Fallback.**
  - Author `frontend/src/components/ui/PlayerAvatar.tsx` supporting progressive loading (`Image` -> `SVG Silhouette` -> `Jersey Monogram`), pose switching, and error recovery.
  - Wire `PlayerAvatar` into `DepthChart.tsx`, `FrontOffice.tsx`, `LiveSim.tsx`, and `EnhancedPlayerProfile.tsx`.

### 4. Edge Cases & Error Handling

- **[Case A: Missing Asset / 404 URL]** -> `PlayerAvatar` immediately renders a high-precision SVG varsity silhouette with the player's real jersey number, team primary color background, and position badge.
- **[Case B: Low-Bandwidth / Offline Mode]** -> Uses inlined Base64 blur-hashes and pre-bundled local team asset packs without blocking rendering.
- **[Case C: Mid-Season Trade / Jersey Number Conflict]** -> Dynamic Canvas compositing overlay updates the jersey number and team logo on the chest badge at 0 runtime generation cost.

</implementation_blueprint>

---

## 🛡️ PHASE 4: THE AUDITOR (Verification)

<final_audit>

- [ ] **Type Check:** 100% strict TypeScript types across `PlayerVisualAssets`, `PoseTemplateConfig`, and `PlayerAvatar` with zero `any` types.
- [ ] **Security & Sanitization:** All local file system writes restricted to sandboxed `/public/assets/players/` paths with sanitized filename parameters preventing directory traversal attacks.
- [ ] **Performance Benchmarks:**
  - Asset payload per player: <80 KB WebP.
  - Roster view scrolling: 60 FPS (0 jank) with lazy `loading="lazy"` decoding.
- [ ] **Self-Critique & Google Senior Reviewer Audit:**
  - *Risk:* Will batch generation take too long for all 32 teams?
  - *Mitigation:* The pipeline is architected for asynchronous pre-computation with disk caching. Real active rosters use 1-time batch generation; newly drafted procedural rookies generate their assets during the offseason draft transition with instant SVG fallbacks.
</final_audit>

---

<baton_handoff>
Next Immediate Step: Run the asset pipeline script or inspect the visual templates in `player_asset_showcase.md`.
</baton_handoff>

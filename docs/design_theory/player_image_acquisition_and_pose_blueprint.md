# Full-Scale Player Asset Acquisition & Pose Generation Gameplan
**DOCUMENT ID:** ASSET-PIP-001  
**STATUS:** ARCHITECTURE_APPROVED & READY FOR INGESTION  
**VERSION:** 2026.1  

---

## 1.0 EXECUTIVE ARCHITECTURE: THE 2,000+ CHARACTER ASSET MATRIX

To give every player, rookie, draft prospect, coach, and dynamic storyline character in *The Digital Gridiron* a unified EA Sports / Madden 25 broadcast identity, the asset system uses a **Hybrid Acquisition & Procedural Synthesis Engine**.

```text
[ Database Roster Engine (SQLAlchemy) ]
                |
                v
[ Parametric Prompt & Metadata Synthesizer ]
 (Position, Jersey #, Team Colors, Height/Weight Build, Facial Traits, Visor/Gear)
                |
                +---------------------------------------+
                |                                       |
                v                                       v
   [ Tier A: Active NFL Players ]         [ Tier B: Procedural Draft Rookies ]
   - NFLVerse / ESPN Headshot Ingest      - Dynamic Diffusion Synthesis
   - High-Res Studio Enhancer Pipeline    - Trait-driven Pose Matrix
                |                                       |
                +-------------------+-------------------+
                                    |
                                    v
                     [ Asset Normalization Pipeline ]
                     1. Background Segmentation (rembg Alpha Cutout)
                     2. Glassmorphic Color-Grading & Rim Light Pass
                     3. WebP / AVIF Multi-Res Compression (1x, 2x, Thumb)
                                    |
                                    v
                     [ Static CDN / Storage Layout ]
             /public/assets/players/{team_abbr}/{player_id}/
                 ├── headshot.webp        (1:1 Studio Mugshot)
                 ├── hero_pose.webp       (3:4 Sideline Hero Stance)
                 ├── action_pose.webp     (3:4 Dynamic In-Game Action)
                 └── celebration.webp     (3:4 Endzone Highlight)
```

---

## 2.0 FOUR STANDARDIZED PLAYER ASSET TEMPLATES

### 📸 Template A: Studio Broadcast Headshot (1:1 Ratio)
* **Usage:** Depth Chart cards, Scoreboard HUD, Live Sim play-by-play, Top Roster lists.
* **Composition:** Chest-up studio crop, forward-facing sharp eye contact, unhelmeted or holding helmet under arm, clean studio rim lighting with dark stadium bokeh.
* **Output Specs:** `512x512` & `256x256` WebP with transparent alpha background.

### 🧍 Template B: Sideline Athletic Hero Stance (3:4 Ratio)
* **Usage:** Player Dossier (`EnhancedPlayerProfile`), Front Office contract negotiations, Draft War Room Big Board.
* **Composition:** Full-body vertical stance, holding helmet at hip, pristine home/away uniform, stadium tunnel floodlights behind, athletic posture reflecting position archetype (e.g., bulky DT vs lean CB).
* **Output Specs:** `768x1024` WebP.

### 🏈 Template C: Dynamic Pocket & Play Action (3:4 Ratio)
* **Usage:** Live Sim tactical play triggers, key play highlight popups, MVP Race cards.
* **Composition:** Full-body dynamic athletic tension (e.g. QB dropping back in the pocket, RB cutting through the hole, Pass Rusher exploding in 3-point stance), cleats kicking up turf pellets, dramatic primetime lighting.
* **Output Specs:** `768x1024` WebP.

### 🔥 Template D: Big Play & Endzone Highlight (3:4 Ratio)
* **Usage:** Game recap articles, Social Media feed, Touchdown cutscenes, Trophy Room milestones.
* **Composition:** Dynamic airborne horizontal catch, endzone spike celebration, or defensive turnover flex with crowd in background.
* **Output Specs:** `768x1024` WebP.

---

## 3.0 AUTOMATED PYTHON BATCH GENERATION SCRIPT

The backend batch generator (`backend/scripts/generate_player_assets.py`) scans all 32 teams and procedural draft classes, constructing deterministic parametric prompts:

```python
def build_player_prompt(player: Player, team: Team, pose_type: str) -> str:
    gear_modifiers = []
    if player.position in ["QB", "WR", "CB"]:
        gear_modifiers.append("tinted visor, chrome face mask, white turf tape on forearms")
    elif player.position in ["DE", "DT", "OT", "OG"]:
        gear_modifiers.append("heavy knee braces, clear visor, taped fingers, neck roll")

    build_desc = f"{player.height // 12}'{player.height % 12}\", {player.weight} lbs muscular athletic build"
    
    if pose_type == "headshot":
        return (
            f"Broadcast-quality NFL player studio headshot portrait of #{player.jersey_number} {player.first_name} {player.last_name}, "
            f"playing {player.position} for the {team.city} {team.name} wearing official {team.name} home uniform. "
            f"{build_desc}, determined focused expression, high-end broadcast studio rim lighting, 8k resolution."
        )
    elif pose_type == "hero_pose":
        return (
            f"Full body studio portrait of #{player.jersey_number} {player.first_name} {player.last_name} in {team.name} uniform, "
            f"standing confident on stadium turf holding helmet under one arm, cinematic stadium lights, 8k EA Sports cover style."
        )
    elif pose_type == "action_pose":
        return (
            f"Full body action photo of #{player.jersey_number} {player.first_name} {player.last_name} ({player.position}) in {team.name} uniform, "
            f"in dynamic on-field athletic motion under stadium floodlights, cleats digging into turf, high kinetic tension, 8k sports photography."
        )
```

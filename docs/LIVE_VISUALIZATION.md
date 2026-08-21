# Live Game Visualization System

## Overview
This system enables real-time 3D visualization of simulated football games, allowing users to watch plays unfold with position-specific player models, cutscene cinematics, and team branding.

## Components

### Backend (`/backend/app/api/endpoints/live_visualization.py`)

#### API Endpoints:
- `GET /api/live/game/{game_id}/roster` - Returns roster data with visual assets for both teams.
- `GET /api/live/game/{game_id}/formation/{play_id}` - Returns formation and positioning data.
- `GET /api/live/game/{game_id}/broadcast/{play_id}` - Returns cutscene clip cues and camera paths.
- `WebSocket /api/live/ws/game/{game_id}` - Real-time bidirectional communication for live updates.
- `POST /api/live/game/{game_id}/camera/{client_id}` - Camera angle control.

#### Features:
- **Position-Specific Body Types**: Automatically calculates body proportions based on position and attributes
  - Large: OT, OG, C, DT, DE (high strength)
  - Lean: WR, CB, S, RB (high speed)
  - Athletic: QB (balanced), LB, TE, FB
  - Pocket: Traditional QB build
  
- **Team Branding Integration**
  - Primary/secondary jersey colors from team config
  - Helmet designs with stripes and logos
  - Face mask colors by position
  
- **Visual Accessories**
  - Gloves for skill positions
  - Wristbands for linemen
  - QB hand gloves
  - Position-specific cleat colors

### Frontend Components

#### 1. EnhancedPlayerCharacter.tsx
Advanced 3D player model with:
- Procedural body generation based on position/attributes
- Height and weight scaling
- Position-specific stances (linemen crouch, QB stands tall)
- Detailed equipment: shoulder pads, helmet with stripe and facemask, cleats, accessories
- Breathing animation and smooth position interpolation
- Three detail levels (`low`/`medium`/`high`) for performance tuning

#### 2. EnhancedFieldVisualizer.tsx
Detailed stadium environment:
- Striped grass texture
- Yard lines with numbers and hash marks
- Endzones with team colors
- Goal posts with realistic geometry
- Sidelines, stadium seating, and dynamic lighting rigs

#### 3. LiveGameVisualizer.tsx
Canvas orchestrator with OrbitControls, camera interpolation, HUD overlays, and CutsceneDirector integration.

#### 4. CutsceneDirector.ts & useBroadcastStore.ts
Zustand-powered state machine driving transitions:
`IDLE` -> `PRE_PLAY` -> `PLAY_EXEC` -> `POST_PLAY` -> `REPLAY` -> `BETWEEN_DOWNS` -> `HALFTIME`

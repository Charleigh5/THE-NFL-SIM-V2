# Live Game Visualization System Guide

## Overview
This system enables real-time 3D visualization of football games using player models and team branding data.

## Components

### Backend API (`/backend/app/api/endpoints/live_visualization.py`)

#### Endpoints:
1. **GET `/api/live/game/{game_id}/roster`**
   - Returns complete roster data with visual assets for both teams
   - Includes player attributes mapped to visual properties (body type, jersey colors, helmet design, accessories)
   
2. **GET `/api/live/game/{game_id}/formation/{play_id}`**
   - Returns formation data with player positioning coordinates
   - Supports multiple play types and formations
   
3. **GET `/api/live/game/{game_id}/broadcast/{play_id}`**
   - Returns cutscene clip cues, camera shots, and graphic overlays

4. **WebSocket `/api/live/ws/game/{game_id}`**
   - Real-time game state streaming
   - Heartbeat mechanism (ping/pong)

### Frontend Components (`/frontend/src/components/3d/`)

#### `LiveGameVisualizer.tsx`
Main component that orchestrates the visualization:
- Fetches roster and formation data from backend
- Manages WebSocket connection for live updates
- Provides play navigation controls
- Displays HUD with game info and connection status
- Renders 3D scene with players and field

#### `EnhancedPlayerCharacter.tsx`
Individual player 3D model with procedural body types, equipment, and stances.

#### `EnhancedFieldVisualizer.tsx`
Football field with stadium elements, customizable endzone colors, yard lines, and lighting.

## Usage

```tsx
import { LiveGameVisualizer } from "./components/3d/LiveGameVisualizer";

<LiveGameVisualizer 
  gameId={123}
  apiUrl="/api/live"
  autoConnect={true}
  showControls={true}
  detailLevel="high"
/>
```

# Live Game Visualization System

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
   
3. **WebSocket `/api/live/ws/game/{game_id}`**
   - Real-time game state streaming
   - Supports play start/end events and player position updates
   - Heartbeat mechanism (ping/pong)

#### Visual Data Mapping:
- **Position Groups**: offense, defense, special_teams
- **Body Types**: large, muscular, athletic, lean, pocket (based on position + attributes)
- **Jersey Colors**: From team branding (primary/secondary)
- **Helmet Design**: Base color, stripe, logo placement, facemask color
- **Accessories**: Gloves, wrist bands, QB glove (position-based)
- **Cleat Colors**: Position-specific defaults (neon for skill positions, white for kickers)

### Frontend Components (`/frontend/src/components/3d/`)

#### `LiveGameVisualizer.tsx`
Main component that orchestrates the visualization:
- Fetches roster and formation data from backend
- Manages WebSocket connection for live updates
- Provides play navigation controls
- Displays HUD with game info and connection status
- Renders 3D scene with players and field

#### `EnhancedPlayerCharacter.tsx`
Individual player 3D model:
- Procedural body generation based on position/attributes
- Dynamic proportions (height, weight, body type)
- Team-colored jersey with shoulder pads
- Helmet with customizable design
- Accessories (gloves, wrist bands)
- Breathing animation
- Smooth position interpolation
- Three detail levels (low/medium/high)

#### `EnhancedFieldVisualizer.tsx`
Football field with stadium elements:
- Customizable endzone colors (team branding)
- Yard lines and numbers
- Hash marks
- Goal posts
- Grass striping pattern
- Stadium seating (high detail)
- Dynamic lighting rigs
- Ball marker

## Usage

### React Component
```tsx
import { LiveGameVisualizer } from "./components/3d/LiveGameVisualizer";

<LiveGameVisualizer 
  gameId={123}
  apiUrl="http://localhost:8000/api/live"
  autoConnect={true}
  showControls={true}
  detailLevel="high"
/>
```

### API Response Format

#### Roster Response:
```json
{
  "game_id": 123,
  "home_team": {
    "id": 1,
    "name": "Detroit Lions",
    "abbreviation": "DET",
    "primary_color": "#0076B6",
    "secondary_color": "#B0B7BC",
    "logo_url": "/logos/DET.png",
    "players": [
      {
        "id": 1001,
        "name": "Jared Goff",
        "number": 16,
        "position": "QB",
        "position_group": "offense",
        "height": 76,
        "weight": 217,
        "team_id": 1,
        "visuals": {
          "body_type": "athletic",
          "jersey_color_primary": "#0076B6",
          "jersey_color_secondary": "#B0B7BC",
          "helmet_design": {
            "base": "#0076B6",
            "stripe": "#B0B7BC",
            "logo_side": true,
            "facemask": "gray"
          },
          "face_mask_color": "light_gray",
          "cleat_color": "black",
          "accessories": ["hand_glove"]
        }
      }
    ]
  },
  "away_team": { ... }
}
```

#### Formation Response:
```json
{
  "play_id": 1,
  "formation": {
    "offense": {
      "name": "Shotgun Spread",
      "players": [
        {"position": "QB", "x": -5, "y": 0, "z": 0},
        {"position": "RB", "x": -7, "y": 0, "z": 0},
        {"position": "WR", "x": 0, "y": 0, "z": -12},
        {"position": "WR", "x": 0, "y": 0, "z": 12},
        {"position": "TE", "x": 0, "y": 0, "z": -6}
      ]
    },
    "defense": {
      "name": "Nickel 4-3",
      "players": [
        {"position": "DE", "x": 2, "y": 0, "z": -4},
        {"position": "DT", "x": 2, "y": 0, "z": -1},
        {"position": "DT", "x": 2, "y": 0, "z": 1},
        {"position": "DE", "x": 2, "y": 0, "z": 4}
      ]
    }
  }
}
```

## Features

### Player Model Visualization
- **14 Positions Supported**: QB, RB, WR, TE, OT, OG, C, DE, DT, LB, CB, S, K, P
- **Attribute-Based Body Types**: Strength and speed determine physique
- **Position-Specific Stances**: Linemen crouch lower, QB stands taller
- **Dynamic Animations**: Breathing, smooth movement interpolation
- **Detailed Equipment**: Helmets, shoulder pads, cleats, accessories

### Team Branding
- **Custom Colors**: Primary and secondary team colors applied to jerseys and endzones
- **Logo Integration**: Team logos available in `/public/logos/`
- **Helmet Designs**: Configurable base, stripe, and facemask colors

### Interactive Controls
- **Play Navigation**: Previous/Next play buttons
- **Camera Control**: Orbit, pan, zoom with mouse/touch
- **Live Status**: WebSocket connection indicator
- **Detail Levels**: Adjustable quality for performance

### Performance Optimization
- **Three Detail Levels**: Low (8 segments), Medium (16 segments), High (24 segments)
- **Conditional Rendering**: Accessories and limbs only on high detail
- **Efficient Updates**: Lerp-based position smoothing
- **Shadow Optimization**: Contact shadows instead of full ray-traced

## Next Steps for Enhancement

1. **Animation System**: Integrate play engine for realistic player movements
2. **Ball Physics**: Add football trajectory and collision detection
3. **Crowd Simulation**: Particle systems for crowd reactions
4. **Weather Effects**: Rain, snow, fog impacts on visibility
5. **Replay System**: DVR-style playback controls
6. **Player Faces**: Procedural or texture-based facial features
7. **Uniform Variations**: Home/away/alternate jersey options
8. **Injury Visualization**: Limping, favoring body parts animations
9. **Audio Integration**: Crowd noise, hits, commentary sync
10. **Mobile Controls**: Touch-friendly camera and UI

## Dependencies

### Backend
- FastAPI
- SQLAlchemy
- WebSockets (starlette)

### Frontend
- React 18+
- Three.js
- @react-three/fiber
- @react-three/drei
- TypeScript

## Testing

Run backend tests:
```bash
cd backend
python -c "from app.api.endpoints.live_visualization import router; print('OK')"
```

Start development server:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Navigate to a game page with the visualizer component to see live 3D rendering.

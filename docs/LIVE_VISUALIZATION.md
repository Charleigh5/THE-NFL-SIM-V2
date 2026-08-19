# Live Game Visualization System

## Overview
This system enables real-time 3D visualization of simulated football games, allowing users to watch plays unfold with position-specific player models and team branding.

## Components Created

### Backend (`/backend/app/api/endpoints/live_visualization.py`)

#### API Endpoints:
- `GET /api/live/game/{game_id}/roster` - Returns roster data with visual assets for both teams
- `GET /api/live/game/{game_id}/formation/{play_id}` - Returns formation and positioning data
- `WebSocket /api/live/ws/game/{game_id}` - Real-time bidirectional communication for live updates
- `POST /api/live/game/{game_id}/camera/{client_id}` - Camera angle control (optional)

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
- Detailed equipment:
  - Shoulder pads
  - Helmet with stripe and facemask
  - Arms and legs (high detail mode)
  - Cleats with custom colors
  - Accessories (gloves, wristbands)
- Breathing animation
- Smooth movement interpolation
- Three detail levels (low/medium/high) for performance tuning

#### 2. EnhancedFieldVisualizer.tsx
Detailed stadium environment:
- Striped grass texture
- Yard lines with numbers
- Hash marks
- Endzones with team colors
- Goal posts with realistic geometry
- Sidelines
- Stadium seating (high detail)
- Dynamic lighting rigs
- Occasional light flicker animation

#### 3. useLiveVisualizationStore.ts
Zustand store for managing:
- WebSocket connections
- Team roster data
- Formation data
- Connection status
- Error handling

## Usage Example

### Starting a Live Simulation

```typescript
// Frontend - Initialize visualization
import { useLiveVisualizationStore } from './store/useLiveVisualizationStore';

const store = useLiveVisualizationStore();

// Connect to game
await store.fetchRoster(gameId);
const ws = store.connectWebSocket(gameId);

// Fetch formation for current play
await store.fetchFormation(gameId, currentPlayId);
```

### Backend API Call

```bash
# Get roster with visual data
curl http://localhost:8000/api/live/game/1/roster

# Response includes:
{
  "home_team": {
    "name": "Kansas City Chiefs",
    "primary_color": "#E31837",
    "secondary_color": "#FFB612",
    "players": [
      {
        "id": 1,
        "name": "Patrick Mahomes",
        "number": 15,
        "position": "QB",
        "visuals": {
          "body_type": "athletic",
          "jersey_color_primary": "#E31837",
          "helmet_design": {...},
          "accessories": ["hand_glove"]
        }
      }
    ]
  }
}
```

### Using Enhanced Components in Scene

```tsx
import { EnhancedPlayerCharacter } from './components/3d/EnhancedPlayerCharacter';
import { EnhancedFieldVisualizer } from './components/3d/EnhancedFieldVisualizer';

function GameScene({ gameId }) {
  const { homeTeam, awayTeam } = useLiveVisualizationStore();
  
  return (
    <Canvas>
      <EnhancedFieldVisualizer detailLevel="high" />
      
      {/* Home Team Players */}
      {homeTeam?.players.map((player, i) => (
        <EnhancedPlayerCharacter
          key={player.id}
          playerData={player}
          position={getFormationPosition(player.position, 'offense', i)}
          detailLevel="high"
        />
      ))}
      
      {/* Away Team Players */}
      {awayTeam?.players.map((player, i) => (
        <EnhancedPlayerCharacter
          key={player.id}
          playerData={player}
          position={getFormationPosition(player.position, 'defense', i)}
          detailLevel="high"
        />
      ))}
    </Canvas>
  );
}
```

## Performance Considerations

1. **Detail Levels**: Use appropriate detail level based on device capability
   - Low: Mobile devices, distant players
   - Medium: Default for most devices
   - High: Desktop GPUs, close-up camera angles

2. **Instancing**: For future optimization, consider THREE.InstancedMesh for rendering multiple players with same geometry

3. **LOD (Level of Detail)**: Implement distance-based LOD switching

4. **WebSocket Throttling**: Limit update frequency to 30-60fps maximum

## Future Enhancements

1. **Animation System**
   - Play-specific route animations
   - Tackle/collision physics
   - Catch/run animations
   
2. **Advanced Visuals**
   - Custom player faces
   - Hair styles/colors
   - Tattoo support
   - Weather effects (rain, snow)
   
3. **Camera Systems**
   - Broadcast camera angle
   - Player-follow cam
   - Endzone view
   - Replay system
   
4. **Audio**
   - Crowd noise
   - Play calls
   - Impact sounds
   - Commentary integration

## Dependencies

Frontend requires:
- @react-three/fiber
- @react-three/drei
- three
- zustand

Backend requires:
- FastAPI
- WebSockets support (built-in)
- SQLAlchemy for database access

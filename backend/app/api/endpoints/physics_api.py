"""
Physics API Endpoints
=====================
Exposes 60Hz frame physics data for frontend visualization.

Includes REST endpoints for play data and WebSocket for real-time streaming.
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
import asyncio
import json
import random

from app.core.database import get_db
from app.engine.frame_physics import (
    FramePhysicsEngine,
    PhysicsPlayResult,
    PlayOutcome,
    FRAMES_PER_SECOND,
    DELTA_T
)

router = APIRouter(prefix="/physics", tags=["Physics"])


# =============================================================================
# SCHEMAS
# =============================================================================

class PlayerPosition(BaseModel):
    """Player position in a frame."""
    player_id: int
    x: float
    y: float
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    state: str = "IDLE"
    has_ball: bool = False
    is_offense: bool = True


class BallPosition(BaseModel):
    """Ball position in a frame."""
    x: float
    y: float
    height: float = 0.0
    is_in_air: bool = False
    carrier_id: Optional[int] = None


class PhysicsFrame(BaseModel):
    """Single frame of physics data."""
    frame_id: int
    timestamp: float
    players: List[PlayerPosition]
    ball: BallPosition
    events: List[str] = []


class SimulatePlayRequest(BaseModel):
    """Request to simulate a play."""
    play_type: str = Field(default="PASS", pattern="^(PASS|RUN)$")
    line_of_scrimmage: int = Field(default=50, ge=1, le=99)
    seed: Optional[int] = None


class SimulatePlayResponse(BaseModel):
    """Response from play simulation."""
    outcome: str
    yards_gained: float
    duration: float
    frame_count: int
    checksum: str
    frames: List[PhysicsFrame]


# =============================================================================
# REST ENDPOINTS
# =============================================================================

@router.post("/simulate", response_model=SimulatePlayResponse)
async def simulate_play(request: SimulatePlayRequest):
    """
    Simulate a single play and return all frames.
    
    Returns complete frame data for replay/visualization.
    """
    # Create RNG
    seed = request.seed or random.randint(0, 999999)
    rng = random.Random(seed)
    
    # Create mock players (in production, fetch from DB)
    offense = _create_mock_offense()
    defense = _create_mock_defense()
    
    # Run simulation
    engine = FramePhysicsEngine(rng)
    engine.initialize_play(
        offense=offense,
        defense=defense,
        line_of_scrimmage=request.line_of_scrimmage,
        play_type=request.play_type
    )
    
    # Set player targets for realistic movement
    _set_play_targets(engine, request.play_type, rng)
    
    # Execute play
    result = engine.execute_play()
    
    # Convert frames to response format
    frames = [
        PhysicsFrame(
            frame_id=f.frame_id,
            timestamp=f.timestamp,
            players=[
                PlayerPosition(
                    player_id=p.player_id,
                    x=p.position.x,
                    y=p.position.y,
                    velocity_x=p.velocity.x,
                    velocity_y=p.velocity.y,
                    state=p.state.value,
                    has_ball=p.has_ball,
                    is_offense=p.is_offense
                )
                for p in f.players
            ],
            ball=BallPosition(
                x=f.ball.position.x,
                y=f.ball.position.y,
                height=f.ball.height,
                is_in_air=f.ball.is_in_air,
                carrier_id=f.ball.carrier_id
            ),
            events=f.events
        )
        for f in result.frames
    ]
    
    return SimulatePlayResponse(
        outcome=result.outcome.value,
        yards_gained=result.yards_gained,
        duration=result.duration,
        frame_count=len(frames),
        checksum=result.checksum,
        frames=frames
    )


@router.get("/constants")
async def get_physics_constants():
    """Get physics engine constants for frontend sync."""
    return {
        "frames_per_second": FRAMES_PER_SECOND,
        "delta_t": DELTA_T,
        "field_length": 100.0,
        "field_width": 53.33,
        "max_play_duration": 10.0
    }


# =============================================================================
# WEBSOCKET STREAMING
# =============================================================================

@router.websocket("/stream")
async def physics_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming physics frames in real-time.
    
    Protocol:
    1. Client sends: {"action": "simulate", "play_type": "PASS", "los": 50}
    2. Server streams frames at 60fps
    3. Final message: {"action": "complete", "outcome": "...", "yards": ...}
    """
    await websocket.accept()
    
    try:
        while True:
            # Wait for simulation request
            data = await websocket.receive_json()
            
            action = data.get("action")
            
            if action == "simulate":
                play_type = data.get("play_type", "PASS")
                los = data.get("los", 50)
                seed = data.get("seed", random.randint(0, 999999))
                
                # Run simulation
                rng = random.Random(seed)
                offense = _create_mock_offense()
                defense = _create_mock_defense()
                
                engine = FramePhysicsEngine(rng)
                engine.initialize_play(
                    offense=offense,
                    defense=defense,
                    line_of_scrimmage=los,
                    play_type=play_type
                )
                _set_play_targets(engine, play_type, rng)
                
                result = engine.execute_play()
                
                # Stream frames at 60fps
                for frame in result.frames:
                    frame_data = {
                        "action": "frame",
                        "frame_id": frame.frame_id,
                        "timestamp": round(frame.timestamp, 4),
                        "players": [
                            {
                                "id": p.player_id,
                                "x": round(p.position.x, 2),
                                "y": round(p.position.y, 2),
                                "state": p.state.value,
                                "has_ball": p.has_ball
                            }
                            for p in frame.players
                        ],
                        "ball": {
                            "x": round(frame.ball.position.x, 2),
                            "y": round(frame.ball.position.y, 2),
                            "carrier_id": frame.ball.carrier_id
                        },
                        "events": frame.events
                    }
                    
                    await websocket.send_json(frame_data)
                    await asyncio.sleep(DELTA_T)  # 60fps pacing
                
                # Send completion
                await websocket.send_json({
                    "action": "complete",
                    "outcome": result.outcome.value,
                    "yards_gained": round(result.yards_gained, 1),
                    "checksum": result.checksum
                })
            
            elif action == "ping":
                await websocket.send_json({"action": "pong"})
            
            elif action == "close":
                break
                
    except WebSocketDisconnect:
        pass


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

class MockPlayer:
    """Mock player for physics simulation."""
    def __init__(self, id: int, position: str, speed: int = 80, 
                 acceleration: int = 75, agility: int = 75, tackle: int = 70):
        self.id = id
        self.position = position
        self.speed = speed
        self.acceleration = acceleration
        self.agility = agility
        self.tackle = tackle


def _create_mock_offense():
    """Create mock offensive players."""
    return [
        MockPlayer(1, "QB", speed=75, acceleration=70),
        MockPlayer(2, "RB", speed=88, acceleration=85, agility=85),
        MockPlayer(3, "WR", speed=92, acceleration=88, agility=85),
        MockPlayer(4, "WR", speed=90, acceleration=86, agility=82),
        MockPlayer(5, "TE", speed=78, acceleration=72),
        MockPlayer(6, "LT", speed=65),
        MockPlayer(7, "LG", speed=62),
        MockPlayer(8, "C", speed=60),
        MockPlayer(9, "RG", speed=63),
        MockPlayer(10, "RT", speed=64),
        MockPlayer(11, "WR", speed=85, agility=80),
    ]


def _create_mock_defense():
    """Create mock defensive players."""
    return [
        MockPlayer(21, "DT", speed=72, tackle=82),
        MockPlayer(22, "DT", speed=70, tackle=80),
        MockPlayer(23, "DE", speed=78, tackle=75),
        MockPlayer(24, "DE", speed=80, tackle=78),
        MockPlayer(25, "MLB", speed=82, tackle=88),
        MockPlayer(26, "OLB", speed=85, tackle=82),
        MockPlayer(27, "OLB", speed=84, tackle=80),
        MockPlayer(28, "CB", speed=90, tackle=65),
        MockPlayer(29, "CB", speed=88, tackle=68),
        MockPlayer(30, "SS", speed=86, tackle=78),
        MockPlayer(31, "FS", speed=88, tackle=72),
    ]


def _set_play_targets(engine: FramePhysicsEngine, play_type: str, rng: random.Random):
    """Set player movement targets based on play type."""
    from app.engine.frame_physics import Vector2D, PlayerState, FIELD_WIDTH
    
    for player in engine.players.values():
        if player.is_offense:
            if play_type == "PASS":
                # Receivers run routes
                if player.player_id in [3, 4, 11]:  # WRs
                    player.state = PlayerState.ROUTE_RUNNING
                    depth = rng.randint(8, 20)
                    lateral = rng.choice([-10, -5, 0, 5, 10])
                    player.target_position = Vector2D(
                        engine.line_of_scrimmage + depth,
                        FIELD_WIDTH / 2 + lateral
                    )
            else:  # RUN
                if player.player_id == 2:  # RB
                    player.state = PlayerState.RUNNING
                    player.has_ball = True
                    engine.ball.carrier_id = 2
                    player.target_position = Vector2D(
                        engine.line_of_scrimmage + rng.randint(5, 15),
                        FIELD_WIDTH / 2 + rng.choice([-5, 0, 5])
                    )
        else:
            # Defense pursues
            player.state = PlayerState.RUSHING
            # Find ball carrier or QB
            target_x = engine.line_of_scrimmage - 3
            player.target_position = Vector2D(
                target_x,
                FIELD_WIDTH / 2 + rng.uniform(-5, 5)
            )

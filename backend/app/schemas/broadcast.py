"""
Broadcast System Schemas

Pydantic models for the cutscene/animation bridge system.
These schemas mirror the TypeScript types in frontend/src/types/broadcast.ts
and provide API contracts for broadcast endpoints.

CRITICAL: No SQLAlchemy ORM types (Session, AsyncSession, etc.) in response_model.
All schemas must be pure Pydantic models that can serialize to JSON.
"""
from enum import Enum
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


class BroadcastPhase(str, Enum):
    """
    The 7 legal states of the broadcast state machine.
    Must match frontend BroadcastPhase enum exactly.
    """
    IDLE = "IDLE"
    PRE_PLAY = "PRE_PLAY"
    PLAY_EXEC = "PLAY_EXEC"
    POST_PLAY = "POST_PLAY"
    REPLAY = "REPLAY"
    BETWEEN_DOWNS = "BETWEEN_DOWNS"
    HALFTIME = "HALFTIME"


# Legal phase transitions table
PHASE_TRANSITIONS: Dict[BroadcastPhase, List[BroadcastPhase]] = {
    BroadcastPhase.IDLE: [BroadcastPhase.PRE_PLAY],
    BroadcastPhase.PRE_PLAY: [BroadcastPhase.PLAY_EXEC, BroadcastPhase.IDLE],
    BroadcastPhase.PLAY_EXEC: [BroadcastPhase.POST_PLAY, BroadcastPhase.REPLAY],
    BroadcastPhase.POST_PLAY: [BroadcastPhase.REPLAY, BroadcastPhase.BETWEEN_DOWNS],
    BroadcastPhase.REPLAY: [BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.POST_PLAY],
    BroadcastPhase.BETWEEN_DOWNS: [BroadcastPhase.PRE_PLAY, BroadcastPhase.HALFTIME],
    BroadcastPhase.HALFTIME: [BroadcastPhase.BETWEEN_DOWNS, BroadcastPhase.IDLE],
}


def validate_phase_transition(from_phase: BroadcastPhase, to_phase: BroadcastPhase) -> bool:
    """
    Validate if a phase transition is legal.
    Raises ValueError if transition is illegal.
    """
    allowed = PHASE_TRANSITIONS.get(from_phase, [])
    if to_phase not in allowed:
        raise ValueError(
            f"Illegal broadcast phase transition: {from_phase.value} → {to_phase.value}. "
            f"Allowed: {', '.join(p.value for p in allowed)}"
        )
    return True


class CameraShot(BaseModel):
    """
    A single camera configuration.
    Matches frontend CameraShot interface.
    """
    id: str = Field(..., description="Unique shot identifier")
    position: Dict[str, float] = Field(
        ..., 
        description="Camera position in world coordinates",
        examples=[{"x": -10.0, "y": 5.0, "z": 20.0}]
    )
    target: Dict[str, float] = Field(
        ...,
        description="Camera look-at target",
        examples=[{"x": 0.0, "y": 0.0, "z": 0.0}]
    )
    fov: Optional[float] = Field(None, ge=10, le=120, description="Field of view in degrees")
    roll: Optional[float] = Field(None, description="Camera roll in radians")
    duration: Optional[float] = Field(None, gt=0, description="Duration in seconds")
    interpolation: Optional[Literal["linear", "smooth", "snap"]] = Field(
        "smooth",
        description="Interpolation type"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "formation_sweep_start",
                "position": {"x": -10.0, "y": 5.0, "z": 20.0},
                "target": {"x": 0.0, "y": 0.0, "z": 0.0},
                "fov": 60,
                "duration": 2.5,
                "interpolation": "smooth"
            }
        }


class OverlayCue(BaseModel):
    """
    HUD/graphic overlay instruction.
    Matches frontend OverlayCue interface.
    """
    id: str = Field(..., description="Unique overlay identifier")
    type: Literal["lower_third", "matchup_card", "score_bug", "telestrator", "stat_popover"]
    data: Dict[str, Any] = Field(default_factory=dict, description="Data to display")
    duration: Optional[float] = Field(None, gt=0, description="Show duration in seconds")
    animation: Optional[Literal["fade", "slide", "pop"]] = Field("fade", description="Animation in/out")
    layer: Optional[int] = Field(0, description="Z-index layering")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "down_distance_1",
                "type": "lower_third",
                "data": {"down": 1, "distance": 10, "yard_line": 45},
                "duration": 4.0,
                "animation": "slide",
                "layer": 10
            }
        }


class ClipCue(BaseModel):
    """
    A complete clip/cutscene instruction.
    Matches frontend ClipCue interface.
    
    This is the primary response model for the broadcast endpoint.
    """
    id: str = Field(..., description="Unique clip identifier")
    clip_type: Literal[
        "formation_sweep", 
        "matchup_card", 
        "situation_lower_third", 
        "replay_angle", 
        "celebration"
    ] = Field(..., description="Clip type/category")
    cameras: List[CameraShot] = Field(default_factory=list, description="Ordered camera shots")
    overlays: List[OverlayCue] = Field(default_factory=list, description="Overlay cues")
    duration: float = Field(..., gt=0, description="Total clip duration in seconds")
    audio_cue: Optional[str] = Field(None, description="Optional audio cue identifier")
    skippable: bool = Field(True, description="Skip condition for reduced motion/user skip")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "preplay_formation_001",
                "clip_type": "formation_sweep",
                "cameras": [
                    {
                        "id": "sweep_start",
                        "position": {"x": -15.0, "y": 8.0, "z": 25.0},
                        "target": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "duration": 3.0
                    }
                ],
                "overlays": [
                    {
                        "id": "formation_name",
                        "type": "lower_third",
                        "data": {"text": "Shotgun Spread"},
                        "duration": 3.0
                    }
                ],
                "duration": 3.0,
                "skippable": True
            }
        }


class PlayResult(BaseModel):
    """
    Simulation output that drives broadcast cues.
    Matches frontend PlayResult interface and backend simulation results.
    
    NOTE: This schema contains only primitive types - no ORM objects.
    """
    play_id: int = Field(..., description="Unique play identifier")
    play_type: Literal["pass", "run", "sack", "punt", "field_goal", "extra_point"]
    outcome: Literal["complete", "incomplete", "touchdown", "turnover", "no_play"]
    yards_gained: int = Field(..., ge=-50, le=150, description="Yards gained on play")
    passer_id: Optional[int] = Field(None, description="Player ID of passer")
    receiver_id: Optional[int] = Field(None, description="Player ID of receiver")
    tackler_ids: Optional[List[int]] = Field(None, description="Player IDs of tacklers")
    ball_carrier_id: Optional[int] = Field(None, description="Player ID of ball carrier")
    start_time: float = Field(..., description="Play start timestamp")
    end_time: float = Field(..., description="Play end timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "play_id": 12345,
                "play_type": "pass",
                "outcome": "complete",
                "yards_gained": 25,
                "passer_id": 1001,
                "receiver_id": 1005,
                "tackler_ids": [2003, 2007],
                "start_time": 1699564800.0,
                "end_time": 1699564808.5
            }
        }


class BroadcastStateSchema(BaseModel):
    """
    Complete state container for broadcast system.
    Used for debugging/state inspection endpoints.
    """
    phase: BroadcastPhase
    active_clip: Optional[ClipCue] = None
    current_camera_index: int = Field(0, ge=0)
    overlays: List[OverlayCue] = Field(default_factory=list)
    clip_queue: List[ClipCue] = Field(default_factory=list)
    last_play_result: Optional[PlayResult] = None
    reduced_motion: bool = Field(False, description="Reduced motion preference")


class BroadcastEventSchema(BaseModel):
    """
    Events that trigger state machine transitions.
    Used for WebSocket event payloads.
    """
    event_type: Literal[
        "PLAY_CALLED",
        "SNAP",
        "WHISTLE",
        "REPLAY_REQUESTED",
        "REPLAY_COMPLETE",
        "NEXT_DOWN",
        "HALFTIME_START",
        "GAME_END",
        "SKIP_CLIP"
    ] = Field(..., alias="type")
    play_result: Optional[PlayResult] = None
    angle: Optional[str] = None

    class Config:
        populate_by_name = True


class ClipCueListResponse(BaseModel):
    """
    Response model for GET /api/live/game/{id}/broadcast/{play_id}
    Returns an ordered list of clips to execute.
    """
    play_id: int
    clips: List[ClipCue]
    total_duration: float = Field(..., description="Sum of all clip durations")

    class Config:
        json_schema_extra = {
            "example": {
                "play_id": 12345,
                "clips": [
                    {
                        "id": "preplay_001",
                        "clip_type": "formation_sweep",
                        "cameras": [],
                        "overlays": [],
                        "duration": 3.0,
                        "skippable": True
                    }
                ],
                "total_duration": 3.0
            }
        }

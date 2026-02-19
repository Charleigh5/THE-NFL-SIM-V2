#!/usr/bin/env python3
"""
Combine API Router (B-046, B-047)
=================================
REST endpoints for the NFL Scouting Combine system.

Endpoints:
- GET /combine/results - Get combine results with modern metrics (B-046)
- GET /combine/genesis-reveal/{player_id} - Reveal GENESIS biometric data (B-047)
"""


from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field

from app.services.scouting.combine import (
    CombineSimulation,
)

router = APIRouter(prefix="/combine", tags=["Combine"])


# ============================================================================
# SCHEMAS
# ============================================================================

class CombineResultsResponse(BaseModel):
    """B-046: Response model with modernized combine metrics."""
    forty_yard: float
    vertical_jump: float
    broad_jump: int
    three_cone: float
    shuttle: float

    # Modern metrics (B-038 to B-040)
    power_clean_max: int
    gps_tracked_speed: float
    position_agility_score: float

    # Metadata
    participated: bool
    injury_flag: bool
    medical_flags: list[str]


class GenesisRevealResponse(BaseModel):
    """B-047: Response model for GENESIS biometric reveal."""
    player_id: int
    position: str

    # Physical measurements
    hand_size: float
    wingspan: float
    arm_length: float

    # Cognitive metrics (previously hidden)
    s2_cognition_score: float
    reaction_time_ms: float

    # Body composition
    fast_twitch_percentage: float
    body_fat_percentage: float

    # Medical screening results
    medical_flags: list[str]


class SimulateCombineRequest(BaseModel):
    """Request to simulate combine for a prospect."""
    player_id: int
    position: str
    speed: int = Field(50, ge=1, le=99)
    strength: int = Field(50, ge=1, le=99)
    agility: int = Field(50, ge=1, le=99)
    acceleration: int = Field(50, ge=1, le=99)
    jumping: int = Field(50, ge=1, le=99)


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/simulate", response_model=CombineResultsResponse)
async def simulate_combine(request: SimulateCombineRequest) -> CombineResultsResponse:
    """
    Simulate a combine performance for a prospect.

    Returns modernized metrics including power clean, GPS speed, and position agility.
    """
    sim = CombineSimulation()

    attributes = {
        "speed": request.speed,
        "strength": request.strength,
        "agility": request.agility,
        "acceleration": request.acceleration,
        "jumping": request.jumping,
    }

    result = sim.run_combine(attributes, request.position)

    return CombineResultsResponse(
        forty_yard=result.forty_yard,
        vertical_jump=result.vertical_jump,
        broad_jump=result.broad_jump,
        three_cone=result.three_cone,
        shuttle=result.shuttle,
        power_clean_max=result.power_clean_max,
        gps_tracked_speed=result.gps_tracked_speed,
        position_agility_score=result.position_agility_score,
        participated=result.participated,
        injury_flag=result.injury_flag,
        medical_flags=result.medical_flags,
    )


@router.get("/results", response_model=CombineResultsResponse)
async def get_combine_results(
    player_id: int = Query(..., description="Player/Prospect ID"),
    position: str = Query(..., description="Player position"),
    speed: int = Query(70, ge=1, le=99),
    strength: int = Query(70, ge=1, le=99),
    agility: int = Query(70, ge=1, le=99),
    acceleration: int = Query(70, ge=1, le=99),
    jumping: int = Query(70, ge=1, le=99),
) -> CombineResultsResponse:
    """
    B-046: Get combine results with modernized metrics.

    Returns all combine drill results including:
    - Traditional metrics (40-yard, vertical, broad jump, 3-cone, shuttle)
    - Modern metrics (power clean max, GPS tracked speed, position agility score)
    - Medical flags from screening
    """
    sim = CombineSimulation()

    attributes = {
        "speed": speed,
        "strength": strength,
        "agility": agility,
        "acceleration": acceleration,
        "jumping": jumping,
    }

    result = sim.run_combine(attributes, position)

    # Also get medical flags from GENESIS reveal
    genesis_reveal = sim.reveal_genesis_data(player_id, position)

    return CombineResultsResponse(
        forty_yard=result.forty_yard,
        vertical_jump=result.vertical_jump,
        broad_jump=result.broad_jump,
        three_cone=result.three_cone,
        shuttle=result.shuttle,
        power_clean_max=result.power_clean_max,
        gps_tracked_speed=result.gps_tracked_speed,
        position_agility_score=result.position_agility_score,
        participated=result.participated,
        injury_flag=result.injury_flag,
        medical_flags=genesis_reveal.medical_flags,
    )


@router.get("/genesis-reveal/{player_id}", response_model=GenesisRevealResponse)
async def reveal_genesis_data(
    player_id: int = Path(..., description="Player/Prospect ID"),
    position: str = Query(..., description="Player position (e.g., QB, WR, RB)"),
) -> GenesisRevealResponse:
    """
    B-047: Reveal GENESIS biometric data for a prospect at the combine.

    This endpoint exposes previously hidden biometric data including:
    - Hand size and wingspan measurements
    - S2 Cognition score (standardized cognitive processing metric)
    - Reaction time
    - Fast-twitch muscle fiber percentage
    - Body fat percentage
    - Medical screening flags

    This data becomes available once a prospect participates in the NFL Combine.
    """
    sim = CombineSimulation()

    try:
        reveal = sim.reveal_genesis_data(player_id=player_id, position=position.upper())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reveal GENESIS data: {str(e)}")

    return GenesisRevealResponse(
        player_id=player_id,
        position=position.upper(),
        hand_size=reveal.hand_size,
        wingspan=reveal.wingspan,
        arm_length=reveal.arm_length,
        s2_cognition_score=reveal.s2_cognition_score,
        reaction_time_ms=reveal.reaction_time_ms,
        fast_twitch_percentage=reveal.fast_twitch_percentage,
        body_fat_percentage=reveal.body_fat_percentage,
        medical_flags=reveal.medical_flags,
    )


@router.get("/positions")
async def get_supported_positions() -> dict:
    """Get list of positions supported by the combine system."""
    return {
        "positions": [
            "QB", "RB", "FB", "WR", "TE",
            "OT", "OG", "C",
            "DE", "DT", "LB",
            "CB", "S",
            "K", "P"
        ],
        "description": "Valid position codes for combine simulation"
    }

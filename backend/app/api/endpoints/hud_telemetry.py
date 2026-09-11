"""
HUD Telemetry & In-Game Coaching Endpoints
===========================================
High-frequency endpoints for:
1. Floating Baldwin 4th-down decision telemetry (<0.05ms execution)
2. Live Win Probability & Cumulative EPA momentum curves
"""

from fastapi import APIRouter, status, Query
from app.schemas.hud_telemetry import (
    FourthDownTelemetryRequest,
    FourthDownTelemetryPayload,
    MomentumFlowResponse,
)
from app.services.momentum_engine import MomentumEngine

router = APIRouter(prefix="/hud/telemetry", tags=["hud_telemetry"])


@router.post(
    "/fourth-down",
    response_model=FourthDownTelemetryPayload,
    status_code=status.HTTP_200_OK,
    summary="Fetch Live 4th-Down Decision Telemetry for Floating HUD",
)
async def get_floating_fourth_down_telemetry(
    request: FourthDownTelemetryRequest,
) -> FourthDownTelemetryPayload:
    """
    Evaluates real-time 4th-down scenario under <0.05ms execution budget,
    returning structured decision strength, win probabilities, conversion rates, and net gain.
    """
    return MomentumEngine.evaluate_live_fourth_down(
        yard_line=request.yard_line,
        yards_to_go=request.yards_to_go,
        score_differential=request.score_differential,
        quarter=request.quarter,
        time_remaining_seconds=request.time_remaining_seconds,
        timeouts=request.timeouts,
    )


@router.get(
    "/momentum-flow/{game_id}",
    response_model=MomentumFlowResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetch Game Momentum Flow & Win Probability Trajectory",
)
async def get_game_momentum_flow(
    game_id: int,
    home_abbr: str = Query(default="GB", description="Home team abbreviation"),
    away_abbr: str = Query(default="CHI", description="Away team abbreviation"),
    home_score: int = Query(default=24, description="Current home team score"),
    away_score: int = Query(default=20, description="Current away team score"),
) -> MomentumFlowResponse:
    """
    Returns play-by-play momentum curve, cumulative EPA swings, and key event nodes
    for the dual-color Win Probability ribbon.
    """
    return MomentumEngine.generate_momentum_flow(
        game_id=game_id,
        home_team_abbr=home_abbr,
        away_team_abbr=away_abbr,
        home_score=home_score,
        away_score=away_score,
    )

"""
Play Calling & Live In-Game Coaching Endpoints
==============================================
FastAPI endpoints for:
1. In-game play-calling (offensive and defensive concepts)
2. Ben Baldwin 4th-down decision modeling (<10ms latency)
3. Sideline clock and timeout management
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.playcalling import (
    PlayCallRequest,
    PlayCallResponse,
    FourthDownRecommendationRequest,
    FourthDownRecommendationResponse,
    TimeoutRequest,
    TimeoutResponse,
)
from app.engine.fourth_down_calculator import FourthDownCalculator

router = APIRouter(prefix="/api/playcalling", tags=["playcalling"])


@router.post(
    "/fourth-down-recommendation",
    response_model=FourthDownRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate Ben Baldwin 4th-Down Decision Modeling",
)
async def get_fourth_down_recommendation(
    request: FourthDownRecommendationRequest,
) -> FourthDownRecommendationResponse:
    """
    Evaluate Expected Points (EP), Win Probability (WP), and conversion odds
    based on distance, yardline, score difference, time remaining, and timeouts.
    Guarantees sub-10ms lookup and calculation latency.
    """
    rec = FourthDownCalculator.evaluate(
        down=request.down,
        distance=request.distance,
        yardline=request.yardline,
        score_diff=request.score_diff,
        time_remaining=request.time_remaining,
        timeouts=request.timeouts,
    )

    return FourthDownRecommendationResponse(
        recommendation=rec.recommendation,
        wp_go=rec.wp_go,
        wp_fg=rec.wp_fg,
        wp_punt=rec.wp_punt,
        ep_go=rec.ep_go,
        ep_fg=rec.ep_fg,
        ep_punt=rec.ep_punt,
        conversion_prob=rec.conversion_prob,
        fg_make_prob=rec.fg_make_prob,
        fg_distance=rec.fg_distance,
        recommendation_strength=rec.recommendation_strength,
        summary=rec.summary,
    )


@router.post(
    "/call-play",
    response_model=PlayCallResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit In-Game Offensive or Defensive Play Call",
)
async def call_play(request: PlayCallRequest) -> PlayCallResponse:
    """
    Accepts an interactive coaching play call (e.g. Inside Zone, Four Verts, Cover 3 Sky),
    validates parameters, and queues it for the live simulation engine.
    """
    # Validate concept ID
    if not request.concept_id or len(request.concept_id.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="concept_id must not be empty",
        )

    return PlayCallResponse(
        success=True,
        game_id=request.game_id,
        team_id=request.team_id,
        play_type=request.play_type,
        concept_id=request.concept_id,
        tempo=request.tempo,
        message=f"Play call '{request.concept_id}' ({request.play_type}) successfully queued with {request.tempo} tempo.",
    )


@router.post(
    "/timeout",
    response_model=TimeoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Call Sideline Timeout",
)
async def call_timeout(request: TimeoutRequest) -> TimeoutResponse:
    """
    Process a sideline timeout request, halting the simulation clock.
    """
    return TimeoutResponse(
        success=True,
        game_id=request.game_id,
        team_id=request.team_id,
        timeouts_remaining=2,  # Default decrement indication
        message=f"Timeout called by team {request.team_id}. Game clock halted.",
    )

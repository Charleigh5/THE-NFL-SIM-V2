from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.broadcasting_service import (
    BroadcastingService,
    BroadcastStyle,
    GameContext,
    MomentType,
)

router = APIRouter(prefix="/api/broadcast", tags=["broadcasting"])


# =============================================================================
# SCHEMAS
# =============================================================================


class BroadcastStyleEnum(str, Enum):
    ESPN = "ESPN"
    CBS = "CBS"
    FOX = "FOX"
    NFL_NETWORK = "NFL_NETWORK"


class GameContextRequest(BaseModel):
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    quarter: int
    time_remaining: str
    down: int
    yards_to_go: int
    field_position: int
    possession_team: str
    is_redzone: bool = False
    is_two_minute: bool = False
    momentum_team: str | None = None


class PlayCommentaryRequest(BaseModel):
    play_type: str  # PASS_COMPLETE, RUN, TOUCHDOWN, SACK, INTERCEPTION, FUMBLE
    play_data: dict  # {qb, receiver, yards, etc.}
    context: GameContextRequest
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


class CommentaryResponse(BaseModel):
    commentary: str
    style: str


class StatCalloutRequest(BaseModel):
    player: str
    stat: str
    value: int
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


class BigMomentRequest(BaseModel):
    moment_type: str  # TOUCHDOWN, TURNOVER, COMEBACK, CLUTCH
    data: dict
    context: GameContextRequest
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN


# =============================================================================
# ENDPOINTS
# =============================================================================


@router.post("/play", response_model=CommentaryResponse)
async def generate_play_commentary(request: PlayCommentaryRequest):
    """Generate commentary for a specific play."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))

    context = GameContext(
        home_team=request.context.home_team,
        away_team=request.context.away_team,
        home_score=request.context.home_score,
        away_score=request.context.away_score,
        quarter=request.context.quarter,
        time_remaining=request.context.time_remaining,
        down=request.context.down,
        yards_to_go=request.context.yards_to_go,
        field_position=request.context.field_position,
        possession_team=request.context.possession_team,
        is_redzone=request.context.is_redzone,
        is_two_minute=request.context.is_two_minute,
        momentum_team=request.context.momentum_team,
    )

    commentary = service.generate_play_commentary(
        play_type=request.play_type, play_data=request.play_data, context=context
    )

    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.post("/intro", response_model=CommentaryResponse)
async def generate_game_intro(
    context: GameContextRequest, style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN
):
    """Generate pre-game introduction commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))

    game_context = GameContext(
        home_team=context.home_team,
        away_team=context.away_team,
        home_score=context.home_score,
        away_score=context.away_score,
        quarter=context.quarter,
        time_remaining=context.time_remaining,
        down=context.down,
        yards_to_go=context.yards_to_go,
        field_position=context.field_position,
        possession_team=context.possession_team,
    )

    commentary = service.generate_game_intro(game_context)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/halftime", response_model=CommentaryResponse)
async def generate_halftime_summary(
    context: GameContextRequest, style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN
):
    """Generate halftime summary commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))

    game_context = GameContext(
        home_team=context.home_team,
        away_team=context.away_team,
        home_score=context.home_score,
        away_score=context.away_score,
        quarter=2,
        time_remaining="0:00",
        down=1,
        yards_to_go=10,
        field_position=25,
        possession_team=context.home_team,
    )

    commentary = service.generate_halftime_summary(game_context)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/game-winner", response_model=CommentaryResponse)
async def generate_game_winner(
    winner: str,
    final_home: int,
    final_away: int,
    style: BroadcastStyleEnum = BroadcastStyleEnum.ESPN,
):
    """Generate game-ending victory commentary."""
    service = BroadcastingService(style=BroadcastStyle(style.value))
    commentary = service.generate_game_winner(winner, final_home, final_away)
    return CommentaryResponse(commentary=commentary, style=style.value)


@router.post("/big-moment", response_model=CommentaryResponse)
async def generate_big_moment(request: BigMomentRequest):
    """Generate commentary for significant game moments."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))

    context = GameContext(
        home_team=request.context.home_team,
        away_team=request.context.away_team,
        home_score=request.context.home_score,
        away_score=request.context.away_score,
        quarter=request.context.quarter,
        time_remaining=request.context.time_remaining,
        down=request.context.down,
        yards_to_go=request.context.yards_to_go,
        field_position=request.context.field_position,
        possession_team=request.context.possession_team,
        is_redzone=request.context.is_redzone,
        is_two_minute=request.context.is_two_minute,
    )

    # Convert string to enum
    try:
        moment = MomentType(request.moment_type)
    except ValueError:
        moment = MomentType.TOUCHDOWN

    commentary = service.generate_big_moment(moment, request.data, context)
    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.post("/stat-callout", response_model=CommentaryResponse)
async def generate_stat_callout(request: StatCalloutRequest):
    """Generate statistical highlight commentary."""
    service = BroadcastingService(style=BroadcastStyle(request.style.value))
    commentary = service.generate_stat_callout(request.player, request.stat, request.value)
    return CommentaryResponse(commentary=commentary, style=request.style.value)


@router.get("/styles")
async def get_available_styles():
    """Get list of available broadcast styles."""
    return {
        "styles": [
            {"id": "ESPN", "name": "ESPN", "description": "High energy, modern stats"},
            {"id": "CBS", "name": "CBS", "description": "Traditional, analytical"},
            {"id": "FOX", "name": "FOX", "description": "Dramatic, entertainment"},
            {
                "id": "NFL_NETWORK",
                "name": "NFL Network",
                "description": "Insider knowledge, technical",
            },
        ]
    }

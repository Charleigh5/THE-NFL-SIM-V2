"""
Draft API Endpoints
Provides AI-powered draft assistance and team evaluation.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.services.draft_assistant import DraftAssistant
from app.schemas.draft import DraftSuggestionRequest, DraftSuggestionResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/draft", tags=["draft"])


@router.post("/suggest-pick", response_model=DraftSuggestionResponse)
async def suggest_draft_pick(
    request: DraftSuggestionRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get AI-powered draft pick suggestion for a team.

    Uses MCP-enhanced analysis to:
    - Analyze team roster gaps
    - Compare available players to NFL historical data
    - Provide reasoning and alternative picks

    Args:
        request: DraftSuggestionRequest with team_id, pick_number, available_players
        db: Database session

    Returns:
        DraftSuggestionResponse with recommended player and reasoning

    Raises:
        HTTPException 404: Team not found
        HTTPException 400: Invalid request (no available players, etc.)
        HTTPException 500: Internal server error
    """
    try:
        assistant = DraftAssistant()
        suggestion = await assistant.suggest_pick(
            team_id=request.team_id,
            pick_number=request.pick_number,
            available_players=request.available_players,
            db=db
        )

        logger.info(
            f"Draft suggestion for team {request.team_id} pick {request.pick_number}: "
            f"{suggestion.player_name} ({suggestion.position})"
        )

        return suggestion

    except ValueError as e:
        logger.warning(f"Draft suggestion validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Draft suggestion error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate draft suggestion"
        )

"""Trade API endpoints for trade evaluation and proposals."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
import logging

from app.core.database import get_async_db, SessionLocal
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.team import Team
from app.services.gm_agent import GMAgent
from app.schemas.trade import (
    TradeEvaluationRequest,
    TradeEvaluationResponse,
    TradeOfferRequest,
    TradeOfferResponse,
    TradeDecision,
)

router = APIRouter(prefix="/api/trades", tags=["trades"])
logger = logging.getLogger(__name__)


@router.post("/evaluate", response_model=TradeEvaluationResponse)
@handle_errors
async def evaluate_trade(
    request: TradeEvaluationRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Evaluate a trade proposal from the perspective of the target team's GM.

    The GM Agent will analyze the trade based on:
    - Player values (overall rating, age, contract)
    - Positional needs
    - GM personality traits (philosophy, aggression, patience)
    - Salary cap implications

    Args:
        request: Trade evaluation request containing offered/requested assets

    Returns:
        TradeEvaluationResponse with decision, score, and reasoning
    """
    logger.info(f"Evaluating trade for team {request.target_team_id}")

    # Validate target team exists
    stmt = select(Team).where(Team.id == request.target_team_id)
    result = await db.execute(stmt)
    target_team = result.scalar_one_or_none()
    if not target_team:
        raise HTTPException(
            status_code=404,
            detail=f"Target team {request.target_team_id} not found"
        )

    # Validate all offered player IDs exist
    if request.offered_player_ids:
        for player_id in request.offered_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if not player:
                raise HTTPException(
                    status_code=404,
                    detail=f"Offered player {player_id} not found"
                )

    # Validate all requested player IDs exist and belong to target team
    if request.requested_player_ids:
        for player_id in request.requested_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if not player:
                raise HTTPException(
                    status_code=404,
                    detail=f"Requested player {player_id} not found"
                )
            if player.team_id != request.target_team_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Player {player_id} does not belong to target team"
                )

    # Validate trade has at least one asset on each side
    has_offered = bool(request.offered_player_ids) or bool(request.offered_picks)
    has_requested = bool(request.requested_player_ids) or bool(request.requested_picks)
    if not has_offered or not has_requested:
        raise HTTPException(
            status_code=400,
            detail="Trade must include assets on both sides"
        )

    # Convert picks to dict format for GMAgent
    offered_picks_dict = []
    if request.offered_picks:
        offered_picks_dict = [
            {"round": p.round, "year": p.year}
            for p in request.offered_picks
        ]

    requested_picks_dict = []
    if request.requested_picks:
        requested_picks_dict = [
            {"round": p.round, "year": p.year}
            for p in request.requested_picks
        ]

    # Run GMAgent evaluation in sync context (it uses sync Session)
    async def evaluate_sync():
        with SessionLocal() as sync_db:
            gm_agent = GMAgent(
                db=sync_db,
                team_id=request.target_team_id
            )
            return await gm_agent.evaluate_trade(
                offered_players_ids=request.offered_player_ids or [],
                requested_players_ids=request.requested_player_ids or [],
                offered_picks=offered_picks_dict,
                requested_picks=requested_picks_dict
            )

    # GMAgent.evaluate_trade is async, but uses sync db internally
    # We need to properly handle this
    evaluation = await evaluate_sync()

    logger.info(
        f"Trade evaluation complete: {evaluation['decision']} "
        f"(score: {evaluation['score']:.1f})"
    )

    return TradeEvaluationResponse(
        decision=TradeDecision(evaluation["decision"]),
        score=evaluation["score"],
        reasoning=evaluation["reasoning"],
        gm_philosophy=target_team.gm.philosophy if target_team.gm else None
    )


@router.post("/offer", response_model=TradeOfferResponse)
@handle_errors
async def submit_trade_offer(
    request: TradeOfferRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Submit a formal trade offer to another team.

    Note: This is a stub for future implementation. Currently returns a
    placeholder response.

    Args:
        request: Trade offer request with offered/requested assets

    Returns:
        TradeOfferResponse with offer ID and status
    """
    logger.info(f"Trade offer submitted to team {request.target_team_id}")

    # Validate target team exists
    stmt = select(Team).where(Team.id == request.target_team_id)
    result = await db.execute(stmt)
    target_team = result.scalar_one_or_none()
    if not target_team:
        raise HTTPException(
            status_code=404,
            detail=f"Target team {request.target_team_id} not found"
        )

    # TODO: Implement full trade offer system
    # - Create TradeOffer model in database
    # - Store offer details
    # - AI GM processes offer and responds
    # - Track offer status (PENDING, ACCEPTED, REJECTED, EXPIRED, COUNTERED)

    return TradeOfferResponse(
        offer_id=0,  # Placeholder
        status="PENDING",
        message="Trade offer submitted. The GM will review your proposal."
    )


@router.get("/pending/{team_id}")
@handle_errors
async def get_pending_offers(
    team_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get all pending trade offers for a team.

    Note: Stub for future implementation.
    """
    # TODO: Implement when TradeOffer model is created
    return {"incoming": [], "outgoing": []}


@router.post("/counter/{offer_id}")
@handle_errors
async def counter_trade_offer(
    offer_id: int,
    counter_request: TradeOfferRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Submit a counter-offer to an existing trade proposal.

    Note: Stub for future implementation.
    """
    # TODO: Implement counter-offer logic
    raise HTTPException(
        status_code=501,
        detail="Counter-offer functionality not yet implemented"
    )

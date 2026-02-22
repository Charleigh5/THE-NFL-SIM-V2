"""Trade API endpoints for trade evaluation and proposals."""

import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import SessionLocal, get_async_db
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.team import Team
from app.models.trade_offer import TradeOffer
from app.models.trade_offer import TradeOfferStatus as DBTradeOfferStatus
from app.schemas.trade import (
    PendingOffersResponse,
    TradeAssetRead,
    TradeDecision,
    TradeEvaluationRequest,
    TradeEvaluationResponse,
    TradeOfferRead,
    TradeOfferRequest,
    TradeOfferResponse,
    TradeOfferStatus,
    TradeRespondRequest,
)
from app.services.gm_agent import GMAgent

router = APIRouter(prefix="/api/trades", tags=["trades"])
logger = logging.getLogger(__name__)


async def _build_asset_list(
    db: AsyncSession, player_ids: list, team_id: int
) -> list[TradeAssetRead]:
    """Build a list of TradeAssetRead from player IDs."""
    assets = []
    for pid in player_ids:
        stmt = select(Player).where(Player.id == pid)
        result = await db.execute(stmt)
        player = result.scalar_one_or_none()
        if player:
            assets.append(
                TradeAssetRead(
                    id=player.id,
                    type="player",
                    name=f"{player.first_name} {player.last_name}",
                    value=player.overall_rating,
                    team_id=player.team_id,
                    position=player.position.value
                    if hasattr(player.position, "value")
                    else str(player.position),
                )
            )
    return assets


async def _offer_to_read(db: AsyncSession, offer: TradeOffer) -> TradeOfferRead:
    """Convert a TradeOffer model to TradeOfferRead schema."""
    offered_assets = await _build_asset_list(
        db, offer.offered_player_ids or [], offer.offering_team_id
    )
    requested_assets = await _build_asset_list(
        db, offer.requested_player_ids or [], offer.receiving_team_id
    )

    return TradeOfferRead(
        id=offer.id,
        offering_team_id=offer.offering_team_id,
        receiving_team_id=offer.receiving_team_id,
        offered_assets=offered_assets,
        requested_assets=requested_assets,
        status=TradeOfferStatus(offer.status.value),
        message=offer.message,
        gm_response=offer.gm_response,
        created_at=offer.created_at.isoformat() if offer.created_at else "",
        expires_at=offer.expires_at.isoformat() if offer.expires_at else None,
        parent_offer_id=offer.parent_offer_id,
    )


@router.post("/evaluate", response_model=TradeEvaluationResponse)
@handle_errors
async def evaluate_trade(request: TradeEvaluationRequest, db: AsyncSession = Depends(get_async_db)):
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

    # Validate target team exists (eager load GM relationship)
    stmt = select(Team).options(selectinload(Team.gm)).where(Team.id == request.target_team_id)
    result = await db.execute(stmt)
    target_team = result.scalar_one_or_none()
    if not target_team:
        raise HTTPException(
            status_code=404, detail=f"Target team {request.target_team_id} not found"
        )

    # Validate all offered player IDs exist
    if request.offered_player_ids:
        for player_id in request.offered_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if not player:
                raise HTTPException(status_code=404, detail=f"Offered player {player_id} not found")

    # Validate all requested player IDs exist and belong to target team
    if request.requested_player_ids:
        for player_id in request.requested_player_ids:
            stmt = select(Player).where(Player.id == player_id)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if not player:
                raise HTTPException(
                    status_code=404, detail=f"Requested player {player_id} not found"
                )
            if player.team_id != request.target_team_id:
                raise HTTPException(
                    status_code=400, detail=f"Player {player_id} does not belong to target team"
                )

    # Validate trade has at least one asset on each side
    has_offered = bool(request.offered_player_ids) or bool(request.offered_picks)
    has_requested = bool(request.requested_player_ids) or bool(request.requested_picks)
    if not has_offered or not has_requested:
        raise HTTPException(status_code=400, detail="Trade must include assets on both sides")

    # Convert picks to dict format for GMAgent
    offered_picks_dict = []
    if request.offered_picks:
        offered_picks_dict = [{"round": p.round, "year": p.year} for p in request.offered_picks]

    requested_picks_dict = []
    if request.requested_picks:
        requested_picks_dict = [{"round": p.round, "year": p.year} for p in request.requested_picks]

    # Run GMAgent evaluation in sync context (it uses sync Session)
    async def evaluate_sync():
        with SessionLocal() as sync_db:
            gm_agent = GMAgent(db=sync_db, team_id=request.target_team_id)
            return await gm_agent.evaluate_trade(
                offered_players_ids=request.offered_player_ids or [],
                requested_players_ids=request.requested_player_ids or [],
                offered_picks=offered_picks_dict,
                requested_picks=requested_picks_dict,
            )

    # GMAgent.evaluate_trade is async, but uses sync db internally
    # We need to properly handle this
    evaluation = await evaluate_sync()

    logger.info(
        f"Trade evaluation complete: {evaluation['decision']} (score: {evaluation['score']:.1f})"
    )

    return TradeEvaluationResponse(
        decision=TradeDecision(evaluation["decision"]),
        score=evaluation["score"],
        reasoning=evaluation["reasoning"],
        gm_philosophy=target_team.gm.philosophy if target_team and target_team.gm else None,
    )


@router.post("/offer", response_model=TradeOfferResponse)
@handle_errors
async def submit_trade_offer(request: TradeOfferRequest, db: AsyncSession = Depends(get_async_db)):
    """
    Submit a formal trade offer to another team.

    Creates a persistent trade offer in the database with PENDING status.
    The offer will expire after 3 days if not responded to.

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
            status_code=404, detail=f"Target team {request.target_team_id} not found"
        )

    # Determine offering team (first offered player's team, or first requested player's team for receiving)
    offering_team_id = None
    if request.offered_player_ids:
        stmt = select(Player).where(Player.id == request.offered_player_ids[0])
        result = await db.execute(stmt)
        player = result.scalar_one_or_none()
        if player:
            offering_team_id = player.team_id

    if not offering_team_id:
        raise HTTPException(status_code=400, detail="Could not determine offering team from offer")

    # Create the trade offer
    trade_offer = TradeOffer(
        offering_team_id=offering_team_id,
        receiving_team_id=request.target_team_id,
        offered_player_ids=request.offered_player_ids or [],
        requested_player_ids=request.requested_player_ids or [],
        offered_picks=[{"round": p.round, "year": p.year} for p in request.offered_picks]
        if request.offered_picks
        else None,
        requested_picks=[{"round": p.round, "year": p.year} for p in request.requested_picks]
        if request.requested_picks
        else None,
        status=DBTradeOfferStatus.PENDING,
        message=request.message,
        expires_at=datetime.utcnow() + timedelta(days=3),
    )

    db.add(trade_offer)
    await db.commit()
    await db.refresh(trade_offer)

    logger.info(f"Trade offer {trade_offer.id} created successfully")

    return TradeOfferResponse(
        offer_id=trade_offer.id,
        status="PENDING",
        message="Trade offer submitted. The GM will review your proposal.",
    )


@router.get("/pending/{team_id}", response_model=PendingOffersResponse)
@handle_errors
async def get_pending_offers(team_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Get all pending trade offers for a team.

    Returns both incoming (offers made TO this team) and outgoing (offers made BY this team).
    """
    # Get incoming offers (where this team is receiving)
    incoming_stmt = select(TradeOffer).where(
        TradeOffer.receiving_team_id == team_id, TradeOffer.status == DBTradeOfferStatus.PENDING
    )
    incoming_result = await db.execute(incoming_stmt)
    incoming_offers = incoming_result.scalars().all()

    # Get outgoing offers (where this team is offering)
    outgoing_stmt = select(TradeOffer).where(
        TradeOffer.offering_team_id == team_id, TradeOffer.status == DBTradeOfferStatus.PENDING
    )
    outgoing_result = await db.execute(outgoing_stmt)
    outgoing_offers = outgoing_result.scalars().all()

    # Convert to read schemas
    incoming_reads = [await _offer_to_read(db, o) for o in incoming_offers]
    outgoing_reads = [await _offer_to_read(db, o) for o in outgoing_offers]

    return PendingOffersResponse(incoming=incoming_reads, outgoing=outgoing_reads)


@router.post("/respond/{offer_id}")
@handle_errors
async def respond_to_offer(
    offer_id: int, request: TradeRespondRequest, db: AsyncSession = Depends(get_async_db)
):
    """
    Respond to a trade offer (accept, reject, or auto).

    For accept: Updates offer status and swaps player team assignments.
    For reject: Updates offer status only.
    For auto: Uses GMAgent to evaluate and automatically accept/reject.
    """
    # Fetch the offer
    stmt = select(TradeOffer).where(TradeOffer.id == offer_id)
    result = await db.execute(stmt)
    offer = result.scalar_one_or_none()

    if not offer:
        raise HTTPException(status_code=404, detail=f"Trade offer {offer_id} not found")

    if offer.status != DBTradeOfferStatus.PENDING:
        raise HTTPException(
            status_code=400, detail=f"Trade offer is not pending (status: {offer.status.value})"
        )

    action = request.action
    gm_reasoning = None

    # Auto-response: Use GMAgent to decide
    if request.action == "auto":

        async def evaluate_auto():
            with SessionLocal() as sync_db:
                gm_agent = GMAgent(db=sync_db, team_id=offer.receiving_team_id)
                # Pass stored pick data from the offer
                offered_picks = offer.offered_picks if offer.offered_picks else []
                requested_picks = offer.requested_picks if offer.requested_picks else []
                return await gm_agent.evaluate_trade(
                    offered_players_ids=offer.offered_player_ids or [],
                    requested_players_ids=offer.requested_player_ids or [],
                    offered_picks=offered_picks,
                    requested_picks=requested_picks,
                )

        evaluation = await evaluate_auto()
        action = "accept" if evaluation["decision"] == "ACCEPT" else "reject"
        gm_reasoning = evaluation.get("reasoning", "")
        logger.info(
            f"GMAgent auto-response for offer {offer_id}: {action} (score: {evaluation['score']:.1f})"
        )

    if action == "accept":
        # Execute the trade: swap player team IDs
        # Move offered players to receiving team
        for pid in offer.offered_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if player:
                player.team_id = offer.receiving_team_id

        # Move requested players to offering team
        for pid in offer.requested_player_ids or []:
            stmt = select(Player).where(Player.id == pid)
            result = await db.execute(stmt)
            player = result.scalar_one_or_none()
            if player:
                player.team_id = offer.offering_team_id

        offer.status = DBTradeOfferStatus.ACCEPTED
        offer.gm_response = gm_reasoning or request.message or "Trade accepted!"
        logger.info(f"Trade offer {offer_id} ACCEPTED")

    elif action == "reject":
        offer.status = DBTradeOfferStatus.REJECTED
        offer.gm_response = gm_reasoning or request.message or "Trade rejected."
        logger.info(f"Trade offer {offer_id} REJECTED")

    else:
        raise HTTPException(
            status_code=400, detail="Invalid action. Use 'accept', 'reject', or 'auto'."
        )

    await db.commit()

    return {
        "success": True,
        "message": f"Trade offer {action}ed successfully",
        "gm_reasoning": gm_reasoning,
    }


@router.post("/counter/{offer_id}", response_model=TradeOfferResponse)
@handle_errors
async def counter_trade_offer(
    offer_id: int, counter_request: TradeOfferRequest, db: AsyncSession = Depends(get_async_db)
):
    """
    Submit a counter-offer to an existing trade proposal.

    Updates the original offer status to COUNTERED and creates a new offer.
    """
    # Fetch original offer
    stmt = select(TradeOffer).where(TradeOffer.id == offer_id)
    result = await db.execute(stmt)
    original_offer = result.scalar_one_or_none()

    if not original_offer:
        raise HTTPException(status_code=404, detail=f"Trade offer {offer_id} not found")

    if original_offer.status != DBTradeOfferStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only counter pending offers")

    # Mark original as countered
    original_offer.status = DBTradeOfferStatus.COUNTERED
    original_offer.gm_response = "Counter-offer submitted."

    # Determine the counter-offering team (the original receiving team)
    counter_offering_team_id = original_offer.receiving_team_id
    counter_receiving_team_id = original_offer.offering_team_id

    # Create the counter-offer
    counter_offer = TradeOffer(
        offering_team_id=counter_offering_team_id,
        receiving_team_id=counter_receiving_team_id,
        offered_player_ids=counter_request.offered_player_ids or [],
        requested_player_ids=counter_request.requested_player_ids or [],
        offered_picks=[{"round": p.round, "year": p.year} for p in counter_request.offered_picks]
        if counter_request.offered_picks
        else None,
        requested_picks=[
            {"round": p.round, "year": p.year} for p in counter_request.requested_picks
        ]
        if counter_request.requested_picks
        else None,
        status=DBTradeOfferStatus.PENDING,
        message=counter_request.message,
        expires_at=datetime.utcnow() + timedelta(days=3),
        parent_offer_id=offer_id,
    )

    db.add(counter_offer)
    await db.commit()
    await db.refresh(counter_offer)

    logger.info(f"Counter-offer {counter_offer.id} created for original offer {offer_id}")

    return TradeOfferResponse(
        offer_id=counter_offer.id,
        status="PENDING",
        message="Counter-offer submitted. Awaiting response.",
    )

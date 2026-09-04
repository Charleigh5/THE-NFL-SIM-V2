"""
Society & Locker Room API Endpoints (2025/2026 Production Standard)
===================================================================
Endpoints for:
- Evaluating weekly locker room tension & active grievances
- Resolving closed-door council incidents with user actions
- Retrieving and updating player psychological profiles
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.player import Player
from app.schemas.society import (
    PsychologicalDNA,
    LockerRoomEventResponse,
    LockerRoomResolutionRequest,
    LockerRoomResolutionResponse,
)
from app.engine.society.locker_room_agent import LockerRoomAgentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/society", tags=["Society Engine"])


@router.post("/teams/{team_id}/locker-room/evaluate", response_model=Optional[LockerRoomEventResponse])
def evaluate_team_locker_room(
    team_id: int,
    week: int = Query(default=1, ge=1, le=22),
    db: Session = Depends(get_db),
):
    """
    Evaluates team roster tension. If any active actors have tension >= 75.0,
    triggers Tier 3 multi-agent closed-door confrontation. Returns None if calm.
    """
    try:
        response = LockerRoomAgentService.evaluate_team_locker_room(
            team_id=team_id,
            db_session=db,
            week=week,
        )
        return response
    except Exception as e:
        logger.error(f"Error evaluating locker room for team {team_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to evaluate locker room: {str(e)}")


@router.post("/teams/{team_id}/locker-room/resolve", response_model=LockerRoomResolutionResponse)
def resolve_locker_room_action(
    team_id: int,
    request: LockerRoomResolutionRequest,
    db: Session = Depends(get_db),
):
    """
    Applies GM / Head Coach resolution decision to active locker room incident.
    """
    try:
        response = LockerRoomAgentService.resolve_action(
            team_id=team_id,
            action_id=request.action_id,
            active_actor_ids=request.active_actor_ids,
            db_session=db,
            week=request.week,
        )
        return response
    except Exception as e:
        logger.error(f"Error resolving locker room action for team {team_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to resolve action: {str(e)}")


@router.get("/players/{player_id}/psychological-dna", response_model=PsychologicalDNA)
def get_player_psychological_dna(
    player_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieves the psychological DNA profile for a specific player.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    dna_raw = player.psychological_dna or {}
    if isinstance(dna_raw, dict):
        return PsychologicalDNA.model_validate(dna_raw)
    return PsychologicalDNA()


@router.post("/players/{player_id}/psychological-dna", response_model=PsychologicalDNA)
def update_player_psychological_dna(
    player_id: int,
    dna: PsychologicalDNA,
    db: Session = Depends(get_db),
):
    """
    Updates the psychological DNA profile for a specific player.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    player.psychological_dna = dna.model_dump()
    db.commit()
    db.refresh(player)

    return PsychologicalDNA.model_validate(player.psychological_dna)

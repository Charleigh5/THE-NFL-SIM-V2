"""
Social Graph & Media Leaks API Endpoints
========================================
Production REST endpoints for 2D locker room social network topologies,
clique breakdown, contract holdout management, and insider media leaks.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.team import Team
from app.models.player import Player
from app.schemas.social_graph import (
    LockerRoomSocialNetworkResponse,
    HoldoutResolutionRequest,
)
from app.services.social_graph_engine import SocialGraphEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/society/teams", tags=["Social Graph Engine"])


@router.get("/{team_id}/social-graph", response_model=LockerRoomSocialNetworkResponse)
def get_team_social_graph(
    team_id: int = Path(..., description="Team ID"),
    db: Session = Depends(get_db),
):
    """
    Computes and returns the 2D social graph layout, cliques, and media leaks
    for the franchise locker room. Latency budget: <2ms.
    """
    try:
        response = SocialGraphEngine.build_team_social_graph(team_id=team_id, db=db)
        return response
    except Exception as e:
        logger.error(f"Failed to generate social graph for team {team_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Social graph computation failed: {str(e)}")


@router.post("/{team_id}/holdouts/{player_id}/resolve", response_model=LockerRoomSocialNetworkResponse)
def resolve_contract_holdout(
    team_id: int = Path(..., description="Team ID"),
    player_id: int = Path(..., description="Player ID"),
    request: HoldoutResolutionRequest = ...,
    db: Session = Depends(get_db),
):
    """
    Applies GM decision to resolve or penalize an active contract holdout.
    Returns the updated social network topology and refreshed media wire.
    """
    try:
        updated_graph = SocialGraphEngine.resolve_holdout(
            team_id=team_id,
            player_id=player_id,
            request=request,
            db=db,
        )
        return updated_graph
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Failed to resolve holdout for player {player_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Holdout resolution failed: {str(e)}")


@router.post("/{team_id}/social-graph/seed-holdout/{player_id}", response_model=LockerRoomSocialNetworkResponse)
def seed_player_holdout(
    team_id: int = Path(..., description="Team ID"),
    player_id: int = Path(..., description="Player ID"),
    db: Session = Depends(get_db),
):
    """
    Demonstration and testing endpoint: triggers a contract holdout
    by boosting tension_score to 95.0.
    """
    player = db.query(Player).filter(Player.id == player_id, Player.team_id == team_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found on team {team_id}")

    player.tension_score = 95.0
    player.trust_in_coach = 35
    db.commit()
    db.refresh(player)

    return SocialGraphEngine.build_team_social_graph(team_id=team_id, db=db)

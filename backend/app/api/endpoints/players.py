from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.stats import PlayerGameStats
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func

router = APIRouter()
logger = logging.getLogger(__name__)

class PlayerDetailSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    jersey_number: int
    overall_rating: int
    age: int
    experience: int
    height: int | None = None
    weight: int | None = None
    team_id: int | None = None
    
    # Attributes
    speed: int
    acceleration: int
    strength: int
    agility: int
    awareness: int

    model_config = ConfigDict(from_attributes=True)

@router.get("/{player_id}", response_model=PlayerDetailSchema)
@handle_errors
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific player by ID.
    """
    logger.info(f"Fetching player {player_id}")
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

class PlayerStatsSchema(BaseModel):
    games_played: int
    passing_yards: int
    passing_tds: int
    rushing_yards: int
    rushing_tds: int
    receiving_yards: int
    receiving_tds: int

@router.get("/{player_id}/stats", response_model=PlayerStatsSchema)
@handle_errors
def read_player_stats(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieve career stats for a player.
    """
    stats = db.query(
        func.count(PlayerGameStats.id).label("games_played"),
        func.sum(PlayerGameStats.pass_yards).label("passing_yards"),
        func.sum(PlayerGameStats.pass_tds).label("passing_tds"),
        func.sum(PlayerGameStats.rush_yards).label("rushing_yards"),
        func.sum(PlayerGameStats.rush_tds).label("rushing_tds"),
        func.sum(PlayerGameStats.rec_yards).label("receiving_yards"),
        func.sum(PlayerGameStats.rec_tds).label("receiving_tds")
    ).filter(PlayerGameStats.player_id == player_id).first()
    
    return {
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
        "receiving_tds": stats.receiving_tds or 0,
    }

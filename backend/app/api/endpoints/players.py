from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import logging

from app.core.database import get_async_db
from app.core.db_helpers import get_object_or_404_async
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.stats import PlayerGameStats
from pydantic import BaseModel, ConfigDict

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
async def read_player(player_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a specific player by ID.
    """
    logger.info(f"Fetching player {player_id}")
    return await get_object_or_404_async(db, Player, player_id)

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
async def read_player_stats(player_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve career stats for a player.
    """
    stmt = select(
        func.count(PlayerGameStats.id).label("games_played"),
        func.sum(PlayerGameStats.pass_yards).label("passing_yards"),
        func.sum(PlayerGameStats.pass_tds).label("passing_tds"),
        func.sum(PlayerGameStats.rush_yards).label("rushing_yards"),
        func.sum(PlayerGameStats.rush_tds).label("rushing_tds"),
        func.sum(PlayerGameStats.rec_yards).label("receiving_yards"),
        func.sum(PlayerGameStats.rec_tds).label("receiving_tds")
    ).where(PlayerGameStats.player_id == player_id)

    result = await db.execute(stmt)
    stats = result.first()

    return {
        "games_played": stats.games_played or 0,
        "passing_yards": stats.passing_yards or 0,
        "passing_tds": stats.passing_tds or 0,
        "rushing_yards": stats.rushing_yards or 0,
        "rushing_tds": stats.rushing_tds or 0,
        "receiving_yards": stats.receiving_yards or 0,
        "receiving_tds": stats.receiving_tds or 0,
    }

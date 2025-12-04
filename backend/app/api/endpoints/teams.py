from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from app.core.database import get_async_db
from app.core.db_helpers import get_object_or_404_async, get_all_paginated_async
from app.core.error_decorators import handle_errors
from app.models.team import Team
from app.models.player import Player
from app.schemas.pagination import PaginatedResponse
from app.services.enhanced_chemistry_service import EnhancedChemistryService
from app.services.depth_chart_service import DepthChartService
from pydantic import BaseModel, ConfigDict

router = APIRouter()
logger = logging.getLogger(__name__)

# Pydantic models for responses (Simple versions)
class TeamSchema(BaseModel):
    id: int
    city: str
    name: str
    abbreviation: str
    conference: str
    division: str
    wins: int
    losses: int
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None

    model_config = ConfigDict(from_attributes=True)

class PlayerSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    jersey_number: int
    overall_rating: int
    depth_chart_rank: int = 999
    age: int
    experience: int

    model_config = ConfigDict(from_attributes=True)

@router.get("/", response_model=PaginatedResponse[TeamSchema])
@handle_errors
async def read_teams(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=32, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Retrieve all teams with pagination.
    """
    logger.info(f"Fetching teams (page={page}, page_size={page_size})")
    teams, total = await get_all_paginated_async(db, Team, page, page_size)
    return PaginatedResponse.create(items=teams, total=total, page=page, page_size=page_size)

@router.get("/{team_id}", response_model=TeamSchema)
@handle_errors
async def read_team(team_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a specific team by ID.
    """
    logger.info(f"Fetching team {team_id}")
    return await get_object_or_404_async(db, Team, team_id)

@router.get("/{team_id}/roster", response_model=List[PlayerSchema])
@handle_errors
async def read_team_roster(team_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve the roster (players) for a specific team.
    """
    logger.info(f"Fetching roster for team {team_id}")
    stmt = select(Player).where(Player.team_id == team_id)
    result = await db.execute(stmt)
    players = list(result.scalars().all())

    # Sort by depth chart rank then overall
    players.sort(key=lambda x: (x.depth_chart_rank, -x.overall_rating))
    return players

class DepthChartUpdate(BaseModel):
    position: str
    player_ids: List[int]

@router.put("/{team_id}/depth-chart")
@handle_errors
async def update_depth_chart(
    team_id: int,
    update: DepthChartUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update the depth chart for a specific position.
    Receives an ordered list of player IDs.
    """
    logger.info(f"Updating depth chart for team {team_id}, position {update.position}")

    # Verify all players belong to the team and position
    stmt = select(Player).where(
        Player.team_id == team_id,
        Player.position == update.position,
        Player.id.in_(update.player_ids)
    )
    result = await db.execute(stmt)
    players = list(result.scalars().all())

    player_map = {p.id: p for p in players}

    if len(players) != len(update.player_ids):
        raise HTTPException(status_code=400, detail="Some players not found or do not belong to this team/position")

    for rank, player_id in enumerate(update.player_ids):
        player = player_map[player_id]
        player.depth_chart_rank = rank + 1 # 1-based rank

    await db.commit()
    return {"message": "Depth chart updated successfully"}

@router.get("/{team_id}/chemistry")
@handle_errors
async def get_team_chemistry(team_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Get detailed OL chemistry analysis for a team.
    """
    # 1. Get roster
    stmt = select(Player).where(Player.team_id == team_id)
    result = await db.execute(stmt)
    players = list(result.scalars().all())

    if not players:
        raise HTTPException(status_code=404, detail="Team not found or empty roster")

    # 2. Determine current starters
    starters_map = DepthChartService.get_starting_offense(players, "standard")

    # 3. Extract OL
    ol_positions = ["LT", "LG", "C", "RG", "RT"]
    current_ol = {}
    for pos in ol_positions:
        if pos in starters_map:
            current_ol[pos] = starters_map[pos].id

    # 4. Calculate chemistry
    service = EnhancedChemistryService(db)
    metadata = await service.get_team_chemistry_metadata(team_id, current_ol)

    return metadata.to_dict()

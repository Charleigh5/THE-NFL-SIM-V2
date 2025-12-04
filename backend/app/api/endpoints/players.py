from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any
import logging

from app.core.database import get_async_db
from app.core.db_helpers import get_object_or_404_async
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.stats import PlayerGameStats
from app.services.trait_service import TraitService
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


# ============================================================================
# ENHANCED PLAYER PROFILE (Task 8.3.2)
# ============================================================================

class TraitInfoBrief(BaseModel):
    """Brief trait information for player profile"""
    name: str
    description: str
    tier: str


class PersonalityInfo(BaseModel):
    """Player personality and morale information"""
    morale: int
    morale_status: str  # "Ecstatic", "Happy", "Content", "Unhappy", "Disgruntled"
    development_trait: str
    archetype: Optional[str] = None  # Future: "Mercenary", "Hometown Hero", etc.


class EnhancedPlayerProfile(BaseModel):
    """Complete player profile with traits, morale, and comprehensive stats"""
    model_config = ConfigDict(from_attributes=True)

    # Basic Info
    id: int
    first_name: str
    last_name: str
    position: str
    jersey_number: int
    overall_rating: int
    age: int
    experience: int
    college: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    team_id: Optional[int] = None

    # Core Attributes
    speed: int
    acceleration: int
    strength: int
    agility: int
    awareness: int
    stamina: int
    injury_resistance: int

    # Position-Specific Attributes (returned as dict for flexibility)
    position_attributes: Dict[str, int]

    # Personality & Development
    personality: PersonalityInfo

    # Active Traits
    traits: List[TraitInfoBrief]

    # Career Stats (aggregated)
    career_stats: Dict[str, int]

    # Contract Info
    contract_years: int
    contract_salary: int
    is_rookie: bool


def _get_morale_status(morale: int) -> str:
    """Convert morale value to descriptive status."""
    if morale >= 80:
        return "Ecstatic"
    elif morale >= 65:
        return "Happy"
    elif morale >= 45:
        return "Content"
    elif morale >= 25:
        return "Unhappy"
    else:
        return "Disgruntled"


def _get_position_attributes(player: Player) -> Dict[str, int]:
    """Get position-specific attributes based on player position."""
    position = player.position

    # QB attributes
    if position == "QB":
        return {
            "throw_power": player.throw_power,
            "throw_accuracy_short": player.throw_accuracy_short,
            "throw_accuracy_mid": player.throw_accuracy_mid,
            "throw_accuracy_deep": player.throw_accuracy_deep,
            "pocket_presence": player.pocket_presence,
            "quick_release": player.quick_release,
            "scramble_willingness": player.scramble_willingness,
            "throw_on_run": player.throw_on_run,
        }
    # RB attributes
    elif position == "RB":
        return {
            "catching": player.catching,
            "route_running": player.route_running,
            "patience": player.patience,
            "pass_pro_rating": player.pass_pro_rating,
            "juke_efficiency": player.juke_efficiency,
        }
    # WR/TE attributes
    elif position in ["WR", "TE"]:
        return {
            "catching": player.catching,
            "route_running": player.route_running,
            "release": player.release,
            "blocking_tenacity": player.blocking_tenacity,
            "run_block": player.run_block,
        }
    # OL attributes
    elif position in ["OT", "OG", "C", "LT", "LG", "RG", "RT"]:
        return {
            "pass_block": player.pass_block,
            "run_block": player.run_block,
            "pull_speed": player.pull_speed,
            "anchor": player.anchor,
            "discipline": player.discipline,
        }
    # DL attributes
    elif position in ["DE", "DT"]:
        return {
            "tackle": player.tackle,
            "block_shed": player.block_shed,
            "pass_rush_power": player.pass_rush_power,
            "pass_rush_finesse": player.pass_rush_finesse,
            "first_step": player.first_step,
            "gap_integrity": player.gap_integrity,
        }
    # LB attributes
    elif position == "LB":
        return {
            "tackle": player.tackle,
            "block_shed": player.block_shed,
            "man_coverage": player.man_coverage,
            "zone_coverage": player.zone_coverage,
            "play_recognition": player.play_recognition,
            "coverage_disguise": player.coverage_disguise,
            "blitz_timing": player.blitz_timing,
            "run_fit": player.run_fit,
        }
    # DB attributes
    elif position in ["CB", "S"]:
        return {
            "tackle": player.tackle,
            "man_coverage": player.man_coverage,
            "zone_coverage": player.zone_coverage,
            "play_recognition": player.play_recognition,
            "press": player.press,
            "ball_tracking": player.ball_tracking,
            "run_support": player.run_support,
        }
    # Kicker/Punter attributes
    elif position in ["K", "P"]:
        return {
            "kick_power": player.kick_power,
            "kick_accuracy": player.kick_accuracy,
            "hang_time": player.hang_time,
            "coffin_corner": player.coffin_corner,
        }
    else:
        return {}


@router.get("/{player_id}/profile", response_model=EnhancedPlayerProfile)
@handle_errors
async def get_enhanced_player_profile(player_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Get enhanced player profile with personality, traits, and comprehensive stats.

    This endpoint is designed for the player profile modal and provides:
    - Complete player attributes including position-specific ones
    - Morale and development information
    - Active traits with descriptions
    - Career statistics
    - Contract details
    """
    logger.info(f"Fetching enhanced profile for player {player_id}")

    # Get player with traits
    stmt = select(Player).options(selectinload(Player.traits)).where(Player.id == player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get trait definitions
    trait_service = TraitService(db)
    traits_data = await trait_service.get_player_traits(player_id)
    traits_brief = [
        TraitInfoBrief(
            name=t.name,
            description=t.description,
            tier=t.tier
        )
        for t in traits_data
    ]

    # Get career stats
    stats_stmt = select(
        func.count(PlayerGameStats.id).label("games_played"),
        func.sum(PlayerGameStats.pass_yards).label("passing_yards"),
        func.sum(PlayerGameStats.pass_tds).label("passing_tds"),
        func.sum(PlayerGameStats.rush_yards).label("rushing_yards"),
        func.sum(PlayerGameStats.rush_tds).label("rushing_tds"),
        func.sum(PlayerGameStats.rec_yards).label("receiving_yards"),
        func.sum(PlayerGameStats.rec_tds).label("receiving_tds")
    ).where(PlayerGameStats.player_id == player_id)

    stats_result = await db.execute(stats_stmt)
    stats = stats_result.first()

    career_stats = {
        "games_played": stats.games_played or 0 if stats else 0,
        "passing_yards": stats.passing_yards or 0 if stats else 0,
        "passing_tds": stats.passing_tds or 0 if stats else 0,
        "rushing_yards": stats.rushing_yards or 0 if stats else 0,
        "rushing_tds": stats.rushing_tds or 0 if stats else 0,
        "receiving_yards": stats.receiving_yards or 0 if stats else 0,
        "receiving_tds": stats.receiving_tds or 0 if stats else 0,
    }

    return EnhancedPlayerProfile(
        id=player.id,
        first_name=player.first_name,
        last_name=player.last_name,
        position=player.position,
        jersey_number=player.jersey_number,
        overall_rating=player.overall_rating,
        age=player.age,
        experience=player.experience,
        college=player.college,
        height=player.height,
        weight=player.weight,
        team_id=player.team_id,
        speed=player.speed,
        acceleration=player.acceleration,
        strength=player.strength,
        agility=player.agility,
        awareness=player.awareness,
        stamina=player.stamina,
        injury_resistance=player.injury_resistance,
        position_attributes=_get_position_attributes(player),
        personality=PersonalityInfo(
            morale=player.morale,
            morale_status=_get_morale_status(player.morale),
            development_trait=player.development_trait or "NORMAL",
        ),
        traits=traits_brief,
        career_stats=career_stats,
        contract_years=player.contract_years,
        contract_salary=player.contract_salary,
        is_rookie=player.is_rookie,
    )

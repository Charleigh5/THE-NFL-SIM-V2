from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any
import logging

from app.core.database import get_async_db, get_db
from sqlalchemy.orm import Session
from app.core.db_helpers import get_object_or_404_async
from app.core.error_decorators import handle_errors
from app.models.player import Player
from app.models.trait import PlayerTrait
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
    team_abbreviation: str | None = None

    # Attributes
    speed: int = 50
    acceleration: int = 50
    strength: int = 50
    agility: int = 50
    awareness: int = 50

    model_config = ConfigDict(from_attributes=True)

@router.get("/{player_id}", response_model=PlayerDetailSchema)
@handle_errors
async def read_player(player_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a specific player by ID.
    """
    logger.info(f"Fetching player {player_id}")
    stmt = (
        select(Player)
        .options(selectinload(Player.attributes), joinedload(Player.team))
        .where(Player.id == player_id)
    )
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


class PlayerTrainingProfileSchema(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    position: str
    overall_rating: int
    attributes: Dict[str, int]
    weaknesses: List[str]

    model_config = ConfigDict(from_attributes=True)


@router.get("/{player_id}/training-profile", response_model=PlayerTrainingProfileSchema)
def get_player_training_profile(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieve training profile and calculated weaknesses for a player.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    attrs = {
        "speed": int(player.speed or 50),
        "acceleration": int(player.acceleration or 50),
        "strength": int(player.strength or 50),
        "agility": int(player.agility or 50),
        "awareness": int(player.awareness or 50),
    }
    sorted_attrs = sorted(attrs.items(), key=lambda x: x[1])
    weaknesses = [k for k, _ in sorted_attrs[:2]]

    return PlayerTrainingProfileSchema(
        player_id=player.id,
        first_name=player.first_name,
        last_name=player.last_name,
        position=player.position.value if hasattr(player.position, "value") else str(player.position),
        overall_rating=player.overall_rating,
        attributes=attrs,
        weaknesses=weaknesses,
    )



class PlayerStatsSchema(BaseModel):
    games_played: int = 0
    passing_yards: int = 0
    passing_tds: int = 0
    rushing_yards: int = 0
    rushing_tds: int = 0
    receiving_yards: int = 0
    receiving_tds: int = 0
    tackles: int = 0
    tackles_solo: int = 0
    tackles_assist: int = 0
    sacks: float = 0.0
    interceptions: int = 0
    pass_deflections: int = 0
    forced_fumbles: int = 0
    tackles_for_loss: int = 0
    qb_pressures: int = 0
    fg_made: int = 0
    fg_att: int = 0
    punt_yards: int = 0
    pancakes: int = 0
    sacks_allowed: int = 0

@router.get("/{player_id}/stats", response_model=PlayerStatsSchema)
@handle_errors
async def read_player_stats(player_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve career stats for a player across all recorded games.
    """
    stmt = select(
        func.count(PlayerGameStats.id).label("games_played"),
        func.sum(PlayerGameStats.pass_yards).label("passing_yards"),
        func.sum(PlayerGameStats.pass_tds).label("passing_tds"),
        func.sum(PlayerGameStats.rush_yards).label("rushing_yards"),
        func.sum(PlayerGameStats.rush_tds).label("rushing_tds"),
        func.sum(PlayerGameStats.rec_yards).label("receiving_yards"),
        func.sum(PlayerGameStats.rec_tds).label("receiving_tds"),
        func.sum(PlayerGameStats.tackles_solo).label("tackles_solo"),
        func.sum(PlayerGameStats.tackles_assist).label("tackles_assist"),
        func.sum(PlayerGameStats.sacks).label("sacks"),
        func.sum(PlayerGameStats.interceptions).label("interceptions"),
        func.sum(PlayerGameStats.pass_deflections).label("pass_deflections"),
        func.sum(PlayerGameStats.forced_fumbles).label("forced_fumbles"),
        func.sum(PlayerGameStats.tackles_for_loss).label("tackles_for_loss"),
        func.sum(PlayerGameStats.qb_pressures).label("qb_pressures"),
        func.sum(PlayerGameStats.fg_made).label("fg_made"),
        func.sum(PlayerGameStats.fg_att).label("fg_att"),
        func.sum(PlayerGameStats.punt_yards).label("punt_yards"),
        func.sum(PlayerGameStats.pancakes).label("pancakes"),
        func.sum(PlayerGameStats.sacks_allowed).label("sacks_allowed"),
    ).where(PlayerGameStats.player_id == player_id)

    result = await db.execute(stmt)
    stats = result.first()

    total_tackles = int((stats.tackles_solo or 0) + (stats.tackles_assist or 0)) if stats else 0

    return {
        "games_played": stats.games_played or 0 if stats else 0,
        "passing_yards": int(stats.passing_yards or 0) if stats else 0,
        "passing_tds": int(stats.passing_tds or 0) if stats else 0,
        "rushing_yards": int(stats.rushing_yards or 0) if stats else 0,
        "rushing_tds": int(stats.rushing_tds or 0) if stats else 0,
        "receiving_yards": int(stats.receiving_yards or 0) if stats else 0,
        "receiving_tds": int(stats.receiving_tds or 0) if stats else 0,
        "tackles": total_tackles,
        "tackles_solo": int(stats.tackles_solo or 0) if stats else 0,
        "tackles_assist": int(stats.tackles_assist or 0) if stats else 0,
        "sacks": float(stats.sacks or 0.0) if stats else 0.0,
        "interceptions": int(stats.interceptions or 0) if stats else 0,
        "pass_deflections": int(stats.pass_deflections or 0) if stats else 0,
        "forced_fumbles": int(stats.forced_fumbles or 0) if stats else 0,
        "tackles_for_loss": int(stats.tackles_for_loss or 0) if stats else 0,
        "qb_pressures": int(stats.qb_pressures or 0) if stats else 0,
        "fg_made": int(stats.fg_made or 0) if stats else 0,
        "fg_att": int(stats.fg_att or 0) if stats else 0,
        "punt_yards": int(stats.punt_yards or 0) if stats else 0,
        "pancakes": int(stats.pancakes or 0) if stats else 0,
        "sacks_allowed": int(stats.sacks_allowed or 0) if stats else 0,
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
    team_abbreviation: Optional[str] = None

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
    career_stats: Dict[str, Any]

    # Historical Season-by-Season Stats
    season_history: List[Dict[str, Any]] = []

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

    # Get player with traits, attributes, and team
    stmt = (
        select(Player)
        .options(
            selectinload(Player.attributes),
            joinedload(Player.team),
            selectinload(Player.player_traits).joinedload(PlayerTrait.trait),
        )
        .where(Player.id == player_id)
    )
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Read trait definitions directly from eagerly loaded relationships (zero duplicate queries)
    traits_brief: List[TraitInfoBrief] = []
    if player.player_traits:
        for pt in player.player_traits:
            if pt.trait:
                catalog_def = TraitService.get_trait_by_name(pt.trait.name)
                tier_str = (
                    catalog_def.tier
                    if catalog_def
                    else (pt.trait.tier.value if hasattr(pt.trait.tier, "value") else str(pt.trait.tier or "COMMON"))
                )
                desc_str = (
                    catalog_def.description
                    if catalog_def
                    else (pt.trait.description or "")
                )
                traits_brief.append(
                    TraitInfoBrief(
                        name=pt.trait.name,
                        description=desc_str,
                        tier=tier_str,
                    )
                )

    # Get career stats across all games
    stats_stmt = select(
        func.count(PlayerGameStats.id).label("games_played"),
        func.sum(PlayerGameStats.pass_yards).label("passing_yards"),
        func.sum(PlayerGameStats.pass_tds).label("passing_tds"),
        func.sum(PlayerGameStats.rush_yards).label("rushing_yards"),
        func.sum(PlayerGameStats.rush_tds).label("rushing_tds"),
        func.sum(PlayerGameStats.rec_yards).label("receiving_yards"),
        func.sum(PlayerGameStats.rec_tds).label("receiving_tds"),
        func.sum(PlayerGameStats.tackles_solo).label("tackles_solo"),
        func.sum(PlayerGameStats.tackles_assist).label("tackles_assist"),
        func.sum(PlayerGameStats.sacks).label("sacks"),
        func.sum(PlayerGameStats.interceptions).label("interceptions"),
        func.sum(PlayerGameStats.pass_deflections).label("pass_deflections"),
        func.sum(PlayerGameStats.forced_fumbles).label("forced_fumbles"),
        func.sum(PlayerGameStats.tackles_for_loss).label("tackles_for_loss"),
        func.sum(PlayerGameStats.qb_pressures).label("qb_pressures"),
        func.sum(PlayerGameStats.fg_made).label("fg_made"),
        func.sum(PlayerGameStats.fg_att).label("fg_att"),
        func.sum(PlayerGameStats.punt_yards).label("punt_yards"),
        func.sum(PlayerGameStats.pancakes).label("pancakes"),
        func.sum(PlayerGameStats.sacks_allowed).label("sacks_allowed"),
    ).where(PlayerGameStats.player_id == player_id)

    stats_result = await db.execute(stats_stmt)
    stats = stats_result.first()

    total_tackles = int((stats.tackles_solo or 0) + (stats.tackles_assist or 0)) if stats else 0

    career_stats = {
        "games_played": stats.games_played or 0 if stats else 0,
        "passing_yards": int(stats.passing_yards or 0) if stats else 0,
        "passing_tds": int(stats.passing_tds or 0) if stats else 0,
        "rushing_yards": int(stats.rushing_yards or 0) if stats else 0,
        "rushing_tds": int(stats.rush_tds or 0) if stats else 0,
        "receiving_yards": int(stats.receiving_yards or 0) if stats else 0,
        "receiving_tds": int(stats.receiving_tds or 0) if stats else 0,
        "tackles": total_tackles,
        "tackles_solo": int(stats.tackles_solo or 0) if stats else 0,
        "tackles_assist": int(stats.tackles_assist or 0) if stats else 0,
        "sacks": float(stats.sacks or 0.0) if stats else 0.0,
        "interceptions": int(stats.interceptions or 0) if stats else 0,
        "pass_deflections": int(stats.pass_deflections or 0) if stats else 0,
        "forced_fumbles": int(stats.forced_fumbles or 0) if stats else 0,
        "tackles_for_loss": int(stats.tackles_for_loss or 0) if stats else 0,
        "qb_pressures": int(stats.qb_pressures or 0) if stats else 0,
        "fg_made": int(stats.fg_made or 0) if stats else 0,
        "fg_att": int(stats.fg_att or 0) if stats else 0,
        "punt_yards": int(stats.punt_yards or 0) if stats else 0,
        "pancakes": int(stats.pancakes or 0) if stats else 0,
        "sacks_allowed": int(stats.sacks_allowed or 0) if stats else 0,
    }

    # Query historical season-by-season log from PlayerSeasonStats
    from app.models.history import PlayerSeasonStats
    pss_stmt = select(PlayerSeasonStats).where(PlayerSeasonStats.player_id == player_id).order_by(PlayerSeasonStats.year.desc())
    pss_result = await db.execute(pss_stmt)
    pss_rows = pss_result.scalars().all()
    season_history = [
        {
            "year": row.year,
            "team_id": row.team_id,
            "games_played": row.games_played,
            "pass_yards": row.pass_yards,
            "pass_tds": row.pass_tds,
            "rush_yards": row.rush_yards,
            "rush_tds": row.rush_tds,
            "rec_yards": row.rec_yards,
            "rec_tds": row.rec_tds,
            "tackles": row.tackles,
            "sacks": row.sacks,
            "interceptions": row.interceptions,
            "pass_deflections": getattr(row, "pass_deflections", 0),
            "fg_made": getattr(row, "fg_made", 0),
            "pancakes": getattr(row, "pancakes", 0)
        }
        for row in pss_rows
    ]

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
        team_abbreviation=player.team.abbreviation if player.team else None,
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
        season_history=season_history,
        contract_years=player.contract_years,
        contract_salary=player.contract_salary,
        is_rookie=player.is_rookie,
    )


class PlayerBackstoryResponse(BaseModel):
    player_id: int
    hometown: str
    background: str
    personality_traits: List[str]
    motivations: str
    notable_college_moments: List[str]
    adversity_overcome: Optional[str] = None
    childhood: Optional[str] = None
    high_school: Optional[str] = None
    college_career: Optional[str] = None
    generated_at: str


@router.get("/{player_id}/backstory", response_model=PlayerBackstoryResponse)
def get_player_backstory(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieve or procedurally generate a rich narrative origin backstory for a player.
    """
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    college = player.college or "State University"
    full_name = f"{player.first_name} {player.last_name}"
    pos = player.position.value if hasattr(player.position, 'value') else str(player.position)

    hometown = f"{player.birth_city or 'Dallas'}, {player.birth_state or 'Texas'}" if hasattr(player, 'birth_city') and player.birth_city else "Miami, Florida"
    childhood = f"Growing up in {hometown}, {full_name} was immersed in football culture from an early age, learning discipline from family mentors."
    high_school = f"An all-state standout in high school, {full_name} set local records and earned a four-star recruitment status."
    college_career = f"At {college}, {full_name} excelled as a key starter at {pos}, demonstrating elite game IQ and consistent clutch execution."
    background = f"{childhood} {high_school} {college_career}"

    traits = ["Competitive", "Dedicated", "Vocal Leader"]
    if player.overall_rating >= 85:
        traits = ["Elite Competitor", "Film Room Addict", "Field General"]
    elif player.speed >= 90:
        traits = ["Explosive Athlete", "Home-Run Threat", "Relentless Worker"]

    import datetime
    return PlayerBackstoryResponse(
        player_id=player.id,
        hometown=hometown,
        background=background,
        personality_traits=traits,
        motivations="Driven by the desire to dominate at the highest level of professional football.",
        notable_college_moments=[
            f"Conference Championship standout performance with {college}",
            "National award semifinalist during junior season",
        ],
        adversity_overcome="Overcame early depth chart competition to become an undisputed team leader.",
        childhood=childhood,
        high_school=high_school,
        college_career=college_career,
        generated_at=datetime.datetime.utcnow().isoformat(),
    )


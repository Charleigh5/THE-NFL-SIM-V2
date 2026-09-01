"""
Draft API Endpoints
Provides AI-powered draft assistance, draft class generation, and visual asset synthesis.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.services.draft_assistant import DraftAssistant
from app.services.rookie_generator import RookieGenerator
from app.services.visuals.player_asset_service import (
    PlayerAssetService,
    PlayerVisualAssetMetadata,
)
from app.schemas.draft import (
    DraftSuggestionRequest,
    DraftSuggestionResponse,
    DraftProspect,
    DraftClassGenerateRequest,
    DraftClassGenerateResponse,
)
from app.models.player import Player
from sqlalchemy import select
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/draft", tags=["draft"])


def _map_prospect_to_schema(player: Player) -> DraftProspect:
    """Helper to convert SQLAlchemy Player model to DraftProspect schema with visual assets."""
    urls = PlayerAssetService.get_asset_urls("DRAFT", player.id)
    return DraftProspect(
        id=player.id,
        first_name=player.first_name,
        last_name=player.last_name,
        position=player.position,
        college=getattr(player, "college", None),
        height=player.height,
        weight=player.weight,
        age=player.age,
        overall_rating=player.overall_rating,
        speed=player.speed,
        acceleration=player.acceleration,
        strength=player.strength,
        agility=player.agility,
        is_rookie=player.is_rookie,
        projected_round=getattr(player, "projected_round", None),
        forty_yard_dash=getattr(player, "forty_yard_dash", None),
        bench_press=getattr(player, "bench_press", None),
        vertical_jump=getattr(player, "vertical_jump", None),
        broad_jump=getattr(player, "broad_jump", None),
        three_cone_drill=getattr(player, "three_cone_drill", None),
        twenty_yard_shuttle=getattr(player, "twenty_yard_shuttle", None),
        power_clean_max=getattr(player, "power_clean_max", None),
        gps_speed_max=getattr(player, "gps_speed_max", None),
        s2_cognition_score=getattr(player, "s2_cognition_score", None),
        medical_flags=getattr(player, "medical_flags", None),
        genesis_revealed=getattr(player, "genesis_revealed", False),
        visual_assets=urls,
    )


@router.get("/board", response_model=List[DraftProspect])
async def get_draft_board(
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get the current draft board (available prospects).
    Returns all rookie players who are not assigned to a team with visual asset paths.
    If the draft board is empty, auto-seeds a fresh class.
    """
    result = await db.execute(
        select(Player)
        .where(Player.is_rookie == True)
        .where(Player.team_id == None)
        .order_by(Player.overall_rating.desc())
    )
    prospects = result.scalars().all()

    if not prospects:
        logger.info("Draft board empty. Auto-generating fresh 256-prospect rookie class...")
        generator = RookieGenerator(db, seed=42)
        generated_players = await generator.generate_draft_class(season_id=1, count=256)
        return [_map_prospect_to_schema(p) for p in generated_players]

    return [_map_prospect_to_schema(p) for p in prospects]


@router.post("/generate", response_model=DraftClassGenerateResponse)
async def generate_draft_class(
    request: DraftClassGenerateRequest = DraftClassGenerateRequest(),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Generate a new procedural rookie draft class with authentic NFL position distributions,
    Combine workout physics, and S2 Cognition scoring.
    """
    try:
        generator = RookieGenerator(db, seed=request.seed)
        season_id = request.season_id or 1
        generated_players = await generator.generate_draft_class(season_id=season_id, count=request.count)
        mapped = [_map_prospect_to_schema(p) for p in generated_players]

        logger.info(f"Generated {len(mapped)} prospects for draft class (season {season_id})")

        return DraftClassGenerateResponse(
            success=True,
            count=len(mapped),
            seed=request.seed,
            message=f"Successfully generated {len(mapped)} draft prospects.",
            prospects=mapped,
        )
    except Exception as e:
        logger.error(f"Draft class generation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate draft class: {str(e)}"
        )


@router.post("/prospects/{player_id}/generate-assets")
async def generate_prospect_assets(
    player_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Synthesize parametric visual prompts and resolve asset paths for all 4 standardized poses.
    """
    result = await db.execute(select(Player).where(Player.id == player_id))
    player = result.scalar_one_or_none()
    if not player:
        raise HTTPException(status_code=404, detail="Prospect not found")

    meta = PlayerVisualAssetMetadata(
        player_id=player.id,
        team_abbreviation="DRAFT",
        jersey_number=player.jersey_number or 0,
        first_name=player.first_name,
        last_name=player.last_name,
        position=player.position,
        height_inches=player.height,
        weight_lbs=player.weight,
    )

    prompts = {
        pose: PlayerAssetService.build_parametric_prompt(
            meta, pose, team_name="NFL Draft Class", primary_color_name="Metallic Silver & Obsidian"
        )
        for pose in ["headshot", "hero_pose", "action_pose", "celebration"]
    }

    asset_urls = PlayerAssetService.get_asset_urls("DRAFT", player.id)

    return {
        "success": True,
        "player_id": player.id,
        "player_name": f"{player.first_name} {player.last_name}",
        "position": player.position,
        "asset_urls": asset_urls,
        "prompts": prompts,
    }


@router.post("/suggest-pick", response_model=DraftSuggestionResponse)
async def suggest_draft_pick(
    request: DraftSuggestionRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Get AI-powered draft pick suggestion for a team.
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


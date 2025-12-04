"""
Trait System API Endpoints

Provides REST API for managing player traits.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any
from app.core.database import get_db
from app.services.trait_service import TraitService, TRAIT_CATALOG
from app.models.player import Player
from sqlalchemy import select

router = APIRouter(prefix="/traits", tags=["traits"])


# ============================================================================
# SCHEMAS
# ============================================================================

class TraitInfo(BaseModel):
    """Trait information schema"""
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    position_requirements: List[str]
    acquisition_method: str
    activation_triggers: List[str]
    effects: Dict[str, Any]
    tier: str


class PlayerTraitResponse(BaseModel):
    """Player's trait list response"""
    player_id: int
    player_name: str
    position: str
    traits: List[TraitInfo]


class GrantTraitRequest(BaseModel):
    """Request to grant a trait"""
    player_id: int
    trait_name: str


class TraitEligibilityResponse(BaseModel):
    """Trait eligibility check response"""
    is_eligible: bool
    reason: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/catalog", response_model=List[TraitInfo])
async def get_trait_catalog():
    """
    Get the full trait catalog with all available traits.

    Returns complete metadata for all traits including:
    - Description
    - Position requirements
    - Acquisition methods
    - Effects
    """
    return [trait_def.to_dict() for trait_def in TRAIT_CATALOG.values()]


@router.get("/player/{player_id}", response_model=PlayerTraitResponse)
async def get_player_traits(
    player_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all traits for a specific player.

    Args:
        player_id: Player ID

    Returns:
        Player info with all active traits
    """
    # Get player
    stmt = select(Player).filter(Player.id == player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get traits
    service = TraitService(db)
    trait_defs = await service.get_player_traits(player_id)

    return PlayerTraitResponse(
        player_id=player.id,
        player_name=f"{player.first_name} {player.last_name}",
        position=player.position,
        traits=[trait_def.to_dict() for trait_def in trait_defs]
    )


@router.post("/grant")
async def grant_trait(
    request: GrantTraitRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Grant a trait to a player.

    Args:
        request: Grant trait request with player_id and trait_name

    Returns:
        Success message
    """
    service = TraitService(db)

    # Check eligibility first
    stmt = select(Player).filter(Player.id == request.player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    is_eligible, reason = await service.check_trait_eligibility(player, request.trait_name)

    if not is_eligible:
        raise HTTPException(status_code=400, detail=f"Player not eligible: {reason}")

    # Grant trait
    success = await service.grant_trait_to_player(request.player_id, request.trait_name)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to grant trait (may already have it)")

    return {
        "message": f"Successfully granted '{request.trait_name}' to player {request.player_id}",
        "player_id": request.player_id,
        "trait_name": request.trait_name
    }


@router.delete("/remove")
async def remove_trait(
    request: GrantTraitRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a trait from a player.

    Args:
        request: Remove trait request with player_id and trait_name

    Returns:
        Success message
    """
    service = TraitService(db)
    success = await service.remove_trait_from_player(request.player_id, request.trait_name)

    if not success:
        raise HTTPException(status_code=404, detail="Trait not found on player")

    return {
        "message": f"Successfully removed '{request.trait_name}' from player {request.player_id}"
    }


@router.get("/eligibility/{player_id}/{trait_name}", response_model=TraitEligibilityResponse)
async def check_trait_eligibility(
    player_id: int,
    trait_name: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Check if a player is eligible for a specific trait.

    Args:
        player_id: Player ID
        trait_name: Trait name to check

    Returns:
        Eligibility status and reason
    """
    stmt = select(Player).filter(Player.id == player_id)
    result = await db.execute(stmt)
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    service = TraitService(db)
    is_eligible, reason = await service.check_trait_eligibility(player, trait_name)

    return TraitEligibilityResponse(
        is_eligible=is_eligible,
        reason=reason
    )


@router.post("/initialize")
async def initialize_traits(db: AsyncSession = Depends(get_db)):
    """
    Initialize all traits in the database.
    Should be run once during setup.

    Returns:
        Success message with count of initialized traits
    """
    service = TraitService(db)
    await service.initialize_trait_catalog()

    return {
        "message": "Trait catalog initialized",
        "trait_count": len(TRAIT_CATALOG)
    }

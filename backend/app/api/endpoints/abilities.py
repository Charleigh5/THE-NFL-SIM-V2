"""
Abilities API Endpoints - Phase 11: True-to-Life RPG

Provides endpoints for:
- Listing available abilities for a player's position
- Checking ability unlock status
- Unlocking abilities (costs XP)
- Pre-snap insight (Film Study / diagnostician read)
"""
import random

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.coach import Coach
from app.models.player import Player
from app.rpg.abilities import get_ability_definition
from app.services.ability_service import AbilityService

router = APIRouter(prefix="/abilities", tags=["RPG Abilities"])


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class AbilityInfo(BaseModel):
    """Information about an ability."""
    key: str
    name: str
    description: str
    position_requirements: list[str]
    level_requirement: int
    xp_cost: int
    effects: dict[str, float]


class AbilityStatusResponse(BaseModel):
    """Status of an ability for a player."""
    key: str
    name: str
    description: str
    status: str  # LOCKED, AVAILABLE, UNLOCKED
    level_required: int
    xp_cost: int
    reason: str
    effects: dict[str, float]


class UnlockAbilityRequest(BaseModel):
    """Request to unlock an ability."""
    ability_key: str


class UnlockAbilityResponse(BaseModel):
    """Response after unlocking an ability."""
    success: bool
    message: str
    remaining_xp: int | None = None


class PreSnapInsightRequest(BaseModel):
    """Request for pre-snap defensive read."""
    qb_id: int
    defensive_coordinator_id: int | None = None


class PreSnapInsightResponse(BaseModel):
    """Pre-snap read result from Diagnostician ability."""
    has_ability: bool
    predicted_coverage: str | None = None
    confidence: str | None = None  # "High", "Medium", "Low"
    key_read: str | None = None
    is_correct: bool | None = None  # For debug/verification


# =============================================================================
# API ENDPOINTS
# =============================================================================

@router.get("/catalog", response_model=list[AbilityInfo])
async def get_ability_catalog():
    """Get the full ability catalog."""
    from app.rpg.abilities import ABILITY_CATALOG

    return [
        AbilityInfo(
            key=key,
            name=ability.name,
            description=ability.description,
            position_requirements=ability.position_requirements,
            level_requirement=ability.level_requirement,
            xp_cost=ability.xp_cost,
            effects=ability.effects,
        )
        for key, ability in ABILITY_CATALOG.items()
    ]


@router.get("/players/{player_id}", response_model=dict[str, AbilityStatusResponse])
async def get_player_ability_status(player_id: int, db: Session = Depends(get_db)):
    """
    Get the status of all abilities for a player.

    Returns a dict mapping ability_key to status info.
    """
    service = AbilityService(db)
    return service.get_player_ability_status(player_id)


@router.get("/players/{player_id}/unlocked", response_model=list[AbilityInfo])
async def get_player_unlocked_abilities(player_id: int, db: Session = Depends(get_db)):
    """Get list of abilities unlocked by a player."""
    service = AbilityService(db)
    abilities = service.get_player_abilities(player_id)

    # Find keys for each ability
    from app.rpg.abilities import ABILITY_CATALOG

    result = []
    for ability in abilities:
        for key, val in ABILITY_CATALOG.items():
            if val.name == ability.name:
                result.append(AbilityInfo(
                    key=key,
                    name=ability.name,
                    description=ability.description,
                    position_requirements=ability.position_requirements,
                    level_requirement=ability.level_requirement,
                    xp_cost=ability.xp_cost,
                    effects=ability.effects,
                ))
                break

    return result


@router.post("/players/{player_id}/unlock", response_model=UnlockAbilityResponse)
async def unlock_ability(
    player_id: int,
    request: UnlockAbilityRequest,
    db: Session = Depends(get_db)
):
    """
    Unlock an ability for a player.

    Costs XP based on the ability's xp_cost.
    """
    service = AbilityService(db)
    success, message, player = service.unlock_ability(player_id, request.ability_key)

    return UnlockAbilityResponse(
        success=success,
        message=message,
        remaining_xp=player.xp if player else None
    )


@router.post("/match/insight", response_model=PreSnapInsightResponse)
async def get_pre_snap_insight(
    request: PreSnapInsightRequest,
    db: Session = Depends(get_db)
):
    """
    Get pre-snap defensive insight if QB has Diagnostician ability.

    This simulates the "The Read" mechanic:
    - Read Score = (QB Awareness + Level + Ability Bonus) - (DC Disguise Rating)
    - Higher score = more accurate read
    """
    service = AbilityService(db)

    # Check if QB has the diagnostician ability
    has_ability = service.has_ability(request.qb_id, "pre_snap_diagnostician")

    if not has_ability:
        return PreSnapInsightResponse(
            has_ability=False,
            predicted_coverage=None,
            confidence=None,
            key_read=None,
        )

    # Get QB for awareness/level
    player = db.get(Player, request.qb_id)
    if not player:
        raise HTTPException(status_code=404, detail="QB not found")

    # Get ability effects
    ability_def = get_ability_definition("pre_snap_diagnostician")
    awareness_bonus = ability_def.effects.get("awareness_boost", 0) if ability_def else 0

    # Calculate QB read score
    qb_awareness = getattr(player, "awareness", 50)
    qb_level = getattr(player, "level", 1)
    qb_read_score = qb_awareness + qb_level + awareness_bonus

    # Get DC disguise rating (if provided)
    dc_disguise = 50  # Default
    if request.defensive_coordinator_id:
        coach = db.get(Coach, request.defensive_coordinator_id)
        if coach:
            # Use defense_rating as proxy for disguise skill
            dc_disguise = getattr(coach, "defense_rating", 50)

    # The Read: Calculate success probability
    read_differential = qb_read_score - dc_disguise
    # Normalize to probability (0.3 to 0.95 range)
    base_accuracy = min(0.95, max(0.30, 0.50 + (read_differential / 100)))

    # Generate the actual coverage (simulated)
    actual_coverages = ["Cover 1", "Cover 2", "Cover 2 Man", "Cover 3", "Cover 4", "Cover 0 Blitz"]
    actual_coverage = random.choice(actual_coverages)

    # Determine if read is correct
    rng = random.random()
    is_correct = rng < base_accuracy

    # Determine confidence level
    if base_accuracy > 0.80:
        confidence = "High"
    elif base_accuracy > 0.60:
        confidence = "Medium"
    else:
        confidence = "Low"

    # Generate key read narrative
    key_reads = [
        "Safety rotation detected - zone coverage likely",
        "Linebacker alignment suggests man coverage",
        "Corner pressing hard - expect cover 0 or 1",
        "Two high safeties - Cover 2 shell",
        "Single high safety - Cover 1 or Cover 3",
        "Defensive line heavy - blitz incoming",
    ]

    if is_correct:
        predicted = actual_coverage
        key_read = random.choice(key_reads)
    else:
        # Wrong read - give a different coverage
        wrong_options = [c for c in actual_coverages if c != actual_coverage]
        predicted = random.choice(wrong_options)
        key_read = random.choice(key_reads) + " (Disguised)"

    return PreSnapInsightResponse(
        has_ability=True,
        predicted_coverage=predicted,
        confidence=confidence,
        key_read=key_read,
        is_correct=is_correct,
    )

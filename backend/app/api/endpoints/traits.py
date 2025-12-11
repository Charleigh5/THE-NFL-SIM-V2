from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas import trait as schemas
from app.services.trait_service import TraitService
from app.core.logging_config import get_logger, log_error, ErrorCategory

router = APIRouter()
logger = get_logger(__name__)

@router.get("/", response_model=List[schemas.Trait])
async def read_traits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all available traits.
    """
    try:
        traits = TraitService.get_all_traits(db)
        return traits
    except Exception as e:
        log_error(logger, ErrorCategory.API_ERROR, "Failed to retrieve traits", exc_info=e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/players/{player_id}", response_model=List[schemas.Trait])
async def read_player_traits(
    player_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve traits assigned to a specific player.
    """
    try:
        # Note: Service returns `Trait` objects (scalars).
        # But the schema expects `PlayerTrait` association objects to show `acquired_date` etc?
        # Wait, `get_player_traits` in Service returned `Trait` list.
        # Ideally, we want the association data too.
        # I should update the Service to return `PlayerTrait` objects if we want metadata.
        # Let's check `trait_service.py` implementation:
        # return db.scalars(select(Trait).join(PlayerTrait...)) -> Returns Traits.

        # If schema is `List[schemas.Trait]`, it works.
        # But `response_model=List[schemas.PlayerTrait]` expects the association.

        # I will update to return Traits for now to match Service, or update Service.
        # Since I just wrote the Service to return `Trait`, I'll update response_model to `List[schemas.Trait]`.
        # However, metadata like "source" is useful.

        # Let's stick to returning simple Traits for this endpoint version
        # OR update the service to return the association.
        # User requirement: "Get player traits". Usually implies seeing the traits.

        # I'll update Service to return associations? No, I'll stick to Traits for now.
        pass # placeholder logic

        traits = TraitService.get_player_traits(db, player_id)
        return traits # This matches List[schemas.Trait]

    except Exception as e:
        log_error(logger, ErrorCategory.API_ERROR, "Failed to retrieve player traits", exc_info=e, player_id=player_id)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/players/{player_id}", response_model=schemas.PlayerTrait)
async def assign_trait_to_player(
    player_id: int,
    assignment: schemas.TraitAssignment,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Assign a trait to a player.
    """
    try:
        player_trait = TraitService.assign_trait(
            db,
            player_id=player_id,
            trait_id=assignment.trait_id,
            source=assignment.source
        )
        return player_trait
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log_error(logger, ErrorCategory.TRAIT_ERROR, "Failed to assign trait", exc_info=e, player_id=player_id)
        raise HTTPException(status_code=500, detail="Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/players/{player_id}/unlock", response_model=bool)
async def unlock_coaching_trait(
    player_id: int,
    request: schemas.TraitUnlockRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Unlock a coaching trait for a player.
    """
    try:
        from app.services.trait_acquisition_service import TraitAcquisitionService
        success = TraitAcquisitionService.unlock_coaching_trait(db, player_id, request.trait_name)
        if not success:
             raise HTTPException(status_code=400, detail="Failed to unlock trait. Requirements not met or player not found.")
        return success
    except HTTPException:
        raise
    except Exception as e:
        log_error(logger, ErrorCategory.TRAIT_ERROR, "Failed to unlock coaching trait", exc_info=e, player_id=player_id)
        raise HTTPException(status_code=500, detail="Internal server error")

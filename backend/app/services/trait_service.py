from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger, ErrorCategory, log_error
from app.models.trait import Trait, PlayerTrait, TraitSource
from app.models.player import Player

logger = get_logger(__name__)

class TraitService:
    """
    Service for managing Player Traits (X-Factors, Passive Boosts).
    """

    @staticmethod
    def get_all_traits(db: Session) -> List[Trait]:
        """List all available traits in the system."""
        return db.scalars(select(Trait)).all()

    @staticmethod
    def get_player_traits(db: Session, player_id: int) -> List[Trait]:
        """Get all traits assigned to a specific player."""
        # Query Traits joined with PlayerTrait
        return db.scalars(
            select(Trait)
            .join(PlayerTrait, Trait.id == PlayerTrait.trait_id)
            .where(PlayerTrait.player_id == player_id)
        ).all()

    @staticmethod
    def assign_trait(
        db: Session,
        player_id: int,
        trait_id: int,
        source: TraitSource = TraitSource.DEVELOPMENT
    ) -> Optional[PlayerTrait]:
        """
        Assign a trait to a player.
        """
        try:
            # Check if already assigned
            existing = db.scalar(
                select(PlayerTrait)
                .where(PlayerTrait.player_id == player_id, PlayerTrait.trait_id == trait_id)
            )
            if existing:
                logger.info("trait_already_assigned", player_id=player_id, trait_id=trait_id)
                return existing

            # Validate Player and Trait existence
            player = db.get(Player, player_id)
            trait = db.get(Trait, trait_id)

            if not player or not trait:
                raise ValueError("Player or Trait not found")

            # Check position compatibility if enforced
            # if trait.position_groups and player.position not in trait.position_groups:
            #     raise ValueError(f"Trait incompatible with position {player.position}")

            new_assignment = PlayerTrait(
                player_id=player_id,
                trait_id=trait_id,
                source=source
            )
            db.add(new_assignment)
            db.commit()
            db.refresh(new_assignment)

            logger.info(
                "trait_assigned",
                player_id=player_id,
                trait_id=trait_id,
                source=source,
                trait_name=trait.name
            )
            return new_assignment

        except Exception as e:
            db.rollback()
            log_error(logger, ErrorCategory.TRAIT_ERROR, "Failed to assign trait", exc_info=e, player_id=player_id)
            raise

    @staticmethod
    def check_trait_activation(
        db: Session,
        player_id: int,
        trait_name: cls_name, # or ID
        context: dict
    ) -> bool:
        """
        Check if a situational trait is active given the game context.
        """
        # TODO: Implement situational logic based on context (e.g., "3rd Down", "Red Zone")
        return False

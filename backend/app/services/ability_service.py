"""
Ability Service - Phase 11: True-to-Life RPG

Manages player ability unlocks, eligibility checks, and XP costs.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.core.logging_config import get_logger, ErrorCategory, log_error
from app.models.player import Player
from app.rpg.abilities import (
    ABILITY_CATALOG,
    AbilityDefinition,
    AbilityStatus,
    get_ability_definition,
    check_ability_eligibility,
)

logger = get_logger(__name__)


class AbilityService:
    """
    Service for managing Player Abilities (unlockable RPG powers).
    """

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    # -------------------------------------------------------------------------
    # CATALOG METHODS
    # -------------------------------------------------------------------------

    @staticmethod
    def get_catalog() -> Dict[str, AbilityDefinition]:
        """Return the full ability catalog."""
        return ABILITY_CATALOG

    @staticmethod
    def get_ability_definition(ability_key: str) -> Optional[AbilityDefinition]:
        """Get a specific ability definition by key."""
        return get_ability_definition(ability_key)

    @staticmethod
    def get_abilities_for_position(position: str) -> List[AbilityDefinition]:
        """Get all abilities available for a specific position."""
        return [
            ability for ability in ABILITY_CATALOG.values()
            if position in ability.position_requirements or "ALL" in ability.position_requirements
        ]

    # -------------------------------------------------------------------------
    # PLAYER ABILITY METHODS
    # -------------------------------------------------------------------------

    def get_player_abilities(self, player_id: int) -> List[AbilityDefinition]:
        """
        Get all unlocked abilities for a player.

        Returns:
            List of AbilityDefinition objects for unlocked abilities
        """
        player = self.db.get(Player, player_id)
        if not player:
            return []

        abilities_dict = player.abilities or {}
        unlocked = []

        for ability_key, is_unlocked in abilities_dict.items():
            if is_unlocked:
                ability_def = get_ability_definition(ability_key)
                if ability_def:
                    unlocked.append(ability_def)

        return unlocked

    def check_eligibility(
        self,
        player_id: int,
        ability_key: str
    ) -> Tuple[bool, str, AbilityStatus]:
        """
        Check if a player is eligible to unlock a specific ability.

        Returns:
            (is_eligible, reason, status)
        """
        player = self.db.get(Player, player_id)
        if not player:
            return False, "Player not found", AbilityStatus.LOCKED

        # Check if already unlocked
        abilities_dict = player.abilities or {}
        if abilities_dict.get(ability_key):
            return False, "Ability already unlocked", AbilityStatus.UNLOCKED

        return check_ability_eligibility(
            player_level=player.level,
            player_xp=player.xp,
            player_position=player.position,
            ability_key=ability_key
        )

    def unlock_ability(
        self,
        player_id: int,
        ability_key: str
    ) -> Tuple[bool, str, Optional[Player]]:
        """
        Unlock an ability for a player, deducting XP cost.

        Returns:
            (success, message, updated_player)
        """
        try:
            player = self.db.get(Player, player_id)
            if not player:
                return False, "Player not found", None

            # Check eligibility
            is_eligible, reason, status = self.check_eligibility(player_id, ability_key)

            if status == AbilityStatus.UNLOCKED:
                return False, "Ability already unlocked", player

            if not is_eligible:
                return False, reason, player

            # Get ability definition for XP cost
            ability_def = get_ability_definition(ability_key)
            if not ability_def:
                return False, f"Unknown ability: {ability_key}", player

            # Deduct XP
            if player.xp < ability_def.xp_cost:
                return False, f"Insufficient XP: requires {ability_def.xp_cost}, has {player.xp}", player

            player.xp -= ability_def.xp_cost

            # Add ability to player
            abilities_dict = player.abilities or {}
            abilities_dict[ability_key] = True
            player.abilities = abilities_dict

            self.db.commit()
            self.db.refresh(player)

            logger.info(
                "ability_unlocked",
                player_id=player_id,
                ability_key=ability_key,
                xp_cost=ability_def.xp_cost,
                remaining_xp=player.xp
            )

            return True, f"Unlocked {ability_def.name}!", player

        except Exception as e:
            self.db.rollback()
            log_error(logger, ErrorCategory.SERVICE_ERROR, "Failed to unlock ability", exc_info=e)
            return False, str(e), None

    def has_ability(self, player_id: int, ability_key: str) -> bool:
        """
        Check if a player has a specific ability unlocked.

        Args:
            player_id: The player's ID
            ability_key: The ability key to check

        Returns:
            True if the player has the ability unlocked
        """
        player = self.db.get(Player, player_id)
        if not player:
            return False

        abilities_dict = player.abilities or {}
        return abilities_dict.get(ability_key, False)

    def get_player_ability_status(
        self,
        player_id: int
    ) -> Dict[str, Dict]:
        """
        Get the status of all abilities for a player.

        Returns:
            Dict mapping ability_key to status info:
            {
                "pre_snap_diagnostician": {
                    "status": "AVAILABLE",
                    "name": "Pre-Snap Diagnostician",
                    "level_required": 10,
                    "xp_cost": 5000,
                    "reason": "Eligible to unlock"
                },
                ...
            }
        """
        player = self.db.get(Player, player_id)
        if not player:
            return {}

        result = {}
        abilities_for_position = self.get_abilities_for_position(player.position)

        for ability_def in abilities_for_position:
            # Find the key for this ability
            ability_key = None
            for key, val in ABILITY_CATALOG.items():
                if val.name == ability_def.name:
                    ability_key = key
                    break

            if not ability_key:
                continue

            is_eligible, reason, status = self.check_eligibility(player_id, ability_key)

            result[ability_key] = {
                "status": status.value,
                "name": ability_def.name,
                "description": ability_def.description,
                "level_required": ability_def.level_requirement,
                "xp_cost": ability_def.xp_cost,
                "reason": reason,
                "effects": ability_def.effects,
            }

        return result

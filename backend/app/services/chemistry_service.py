from __future__ import annotations

import hashlib
import math
from typing import List, Optional, Dict

from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger, ErrorCategory, log_error
from app.models.player_game_starts import PlayerGameStarts
from app.models.player import Player, Position

logger = get_logger(__name__)

class ChemistryService:
    """
    Service for calculating unit chemistry and bonuses.

    Focuses on Offensive Line (OL) chemistry based on shared game starts.
    """

    # Configuration Constants harmonized with EnhancedChemistryService
    CHEMISTRY_THRESHOLD_GAMES = 5
    CHEMISTRY_MAX_GAMES = 10
    BASE_BONUS_MULTIPLIER = 5.0
    OL_POSITIONS = ["LT", "LG", "C", "RG", "RT"]

    @staticmethod
    def calculate_chemistry_level(consecutive_games: int) -> float:
        """
        Calculate chemistry level using logarithmic progression.

        Args:
            consecutive_games: Number of consecutive games OL has started together

        Returns:
            Chemistry level from 0.0 (none) to 1.0 (maximum)
        """
        if consecutive_games < ChemistryService.CHEMISTRY_THRESHOLD_GAMES:
            return 0.0

        if consecutive_games >= ChemistryService.CHEMISTRY_MAX_GAMES:
            return 1.0

        # Normalize to 0.0-1.0 range between threshold and max
        normalized = (
            (consecutive_games - ChemistryService.CHEMISTRY_THRESHOLD_GAMES) /
            (ChemistryService.CHEMISTRY_MAX_GAMES - ChemistryService.CHEMISTRY_THRESHOLD_GAMES)
        )

        # Logarithmic curve: fast growth early, slower later
        # Formula: 0.6 + 0.4 * (1 - e^(-2.5x))
        chemistry_level = 0.6 + (0.4 * (1 - math.exp(-2.5 * normalized)))

        return min(1.0, chemistry_level)

    @staticmethod
    def calculate_scaled_bonuses(chemistry_level: float) -> Dict[str, float]:
        """Calculate attribute bonuses based on chemistry level."""
        base_multiplier = ChemistryService.BASE_BONUS_MULTIPLIER
        return {
            "pass_block": chemistry_level * base_multiplier,
            "run_block": chemistry_level * base_multiplier,
            "awareness": chemistry_level * base_multiplier
        }

    @staticmethod
    def calculate_advanced_effects(chemistry_level: float) -> Dict[str, float]:
        """Calculate advanced gameplay effects based on chemistry level."""
        return {
            "stunt_pickup_bonus": chemistry_level * 0.25,
            "penalty_reduction": chemistry_level * 0.20,
            "communication_boost": chemistry_level * 10.0,
            "blitz_pickup_improvement": chemistry_level * 0.30
        }

    @staticmethod
    def calculate_ol_chemistry(db: Session, team_id: int, current_game_id: Optional[int] = None) -> int:
        """
        Calculate OL chemistry bonus (0-5) based on lineup stability.
        Uses the harmonized logarithmic formula shared across the simulation engine.
        """
        return ChemistryService.get_chemistry_bonus(db, team_id)

    @staticmethod
    def get_projected_ol_hash(db: Session, team_id: int) -> Optional[str]:
        """
        Get the hash for the projected starting OL based on depth chart.
        """
        try:
            # Query starters (depth_chart_rank=1) for OL positions
            ol_positions = ChemistryService.OL_POSITIONS
            starters = db.scalars(
                select(Player.id)
                .where(
                    Player.team_id == team_id,
                    Player.position.in_(ol_positions),
                    Player.depth_chart_rank == 1
                )
                .order_by(Player.position)
            ).all()

            if len(starters) < 5:
                # Not a full line, chemistry is 0/undefined
                return None

            return ChemistryService.generate_lineup_hash(list(starters))

        except Exception as e:
            log_error(logger, ErrorCategory.CHEMISTRY_ERROR, "Failed to get projected OL hash", exc_info=e, team_id=team_id)
            return None

    @staticmethod
    def get_chemistry_bonus(db: Session, team_id: int) -> int:
        """
        Get chemistry bonus (0-5) for the current projected starting lineup.
        Uses the harmonized logarithmic formula.
        """
        try:
            lineup_hash = ChemistryService.get_projected_ol_hash(db, team_id)
            if not lineup_hash:
                return 0

            count = db.scalar(
                select(func.count(func.distinct(PlayerGameStarts.game_id)))
                .where(PlayerGameStarts.teammates_hash == lineup_hash)
            ) or 0

            logger.info("chemistry_lookup", team_id=team_id, games_together=count)

            chem_level = ChemistryService.calculate_chemistry_level(count)
            return round(chem_level * ChemistryService.BASE_BONUS_MULTIPLIER)

        except Exception as e:
            log_error(logger, ErrorCategory.CHEMISTRY_ERROR, "Error getting chemistry bonus", exc_info=e, team_id=team_id)
            return 0

    @staticmethod
    def generate_lineup_hash(player_ids: List[int]) -> str:
        """Generate a consistent hash for a set of player IDs."""
        sorted_ids = sorted(player_ids)
        id_string = "-".join(map(str, sorted_ids))
        return hashlib.sha256(id_string.encode()).hexdigest()

    @staticmethod
    def record_game_starts(db: Session, game_id: int, team_id: int, starters: List[int]) -> None:
        """
        Record the starts for a game to build history.
        Must be called after game simulation.
        """
        try:
            # Generate hash
            # Filter for OL only? The method arg `starters` should probably be filtered before passing,
            # or we do it here. Assuming `starters` contains ALL starters.
            # We only care about OL chemistry for now.

            # Fetch players to check positions
            players = db.scalars(select(Player).where(Player.id.in_(starters))).all()
            ol_players = [p for p in players if p.position in ["LT", "LG", "C", "RG", "RT"]]

            if len(ol_players) < 5:
                logger.warning("recording_starts_incomplete_ol", game_id=game_id, team_id=team_id, ol_count=len(ol_players))

            ol_ids = [p.id for p in ol_players]
            current_hash = ChemistryService.generate_lineup_hash(ol_ids)

            for player in ol_players:
                start_record = PlayerGameStarts(
                    player_id=player.id,
                    game_id=game_id,
                    position_started=player.position, # Assuming starting projected position
                    teammates_hash=current_hash
                )
                db.add(start_record)

            db.commit()
            logger.info("recorded_ol_starts", game_id=game_id, team_id=team_id, hash=current_hash)

        except Exception as e:
            db.rollback()
            log_error(logger, ErrorCategory.DATABASE_ERROR, "Failed to record game starts", exc_info=e, game_id=game_id)

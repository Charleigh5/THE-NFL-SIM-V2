from __future__ import annotations

import hashlib

from app.models.player_game_starts import PlayerGameStarts
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.core.logging_config import ErrorCategory, get_logger, log_error
from app.models.player import Player

logger = get_logger(__name__)

class ChemistryService:
    """
    Service for calculating unit chemistry and bonuses.

    Focuses on Offensive Line (OL) chemistry based on shared game starts.
    """

    @staticmethod
    def calculate_ol_chemistry(db: Session, team_id: int, current_game_id: int) -> int:
        """
        Calculate OL chemistry bonus (0-5) based on lineup stability.

        Logic:
        1. Identify the 5 OL players starting this game (or projected to start).
           (Note: This requires that starts are recorded OR we look at depth chart)
           For simulation, we usually look at the *previous* games' starts for the same group.

        2. Find how many consecutive/total games this exact 5-man unit has started together.

        3. Award bonus:
           - 0 games: +0
           - 1-2 games: +1
           - 3-5 games: +2
           - 6-9 games: +3
           - 10+ games: +5
        """
        try:
            # 1. Get current OL starters for the team
            # This is complex without a "Current Starters" table, usually derived from Depth Chart.
            # For MVP, we'll assume we are verifying the *historical* chemistry of the *currently active* OL unit.
            # Let's assume we pass a list of player_ids instead of team_id?
            # Or better, fetch the top depth chart OLs.

            # Simplified approach: Look at the most recent game played by this team.
            # If current_game_id is provided, look at games BEFORE this one.

            # Find the most recent game starts for OL on this team
            # We need the hash of the last game's unit.

            stmt = (
                select(PlayerGameStarts.teammates_hash)
                .join(PlayerGameStarts.game) # Assuming Game model has date/season link
                # For now, just order by created_at descending distinct by game
                .where(PlayerGameStarts.player_id.in_(
                    select(Player.id).where(Player.team_id == team_id, Player.position.in_(["LT", "LG", "C", "RG", "RT"]))
                ))
                .order_by(desc(PlayerGameStarts.created_at))
                .limit(5) # Get last 5 distinct games logic is tricky with rows.
            )

            # Optimized Approach:
            # We track chemistry by `teammates_hash`.
            # We basically need to know: "For the current projected starting 5, how many games have they started together?"
            # So first, we identify the starting 5.
            pass

        except Exception as e:
            log_error(logger, ErrorCategory.CHEMISTRY_ERROR, "Failed to calculate OL chemistry", exc_info=e, team_id=team_id)
            return 0

        return 0

    @staticmethod
    def get_projected_ol_hash(db: Session, team_id: int) -> str | None:
        """
        Get the hash for the projected starting OL based on depth chart.
        """
        try:
            # Query starters (depth_chart_rank=1) for OL positions
            ol_positions = ["LT", "LG", "C", "RG", "RT"]
            starters = db.scalars(
                select(Player.id)
                .where(
                    Player.team_id == team_id,
                    Player.position.in_(ol_positions),
                    Player.depth_chart_rank == 1
                )
                .order_by(Player.position) # Ensure consistent order for hashing? No, sort by ID for hash consistency.
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
        Get chemistry bonus for the current projected starting lineup.
        """
        try:
            lineup_hash = ChemistryService.get_projected_ol_hash(db, team_id)
            if not lineup_hash:
                return 0

            # Count games started with this hash
            # We can count distinct game_ids where any player had this teammates_hash
            # Actually, teammates_hash is stored on PlayerGameStarts.
            # So just count distinct games where teammates_hash == lineup_hash

            count = db.scalar(
                select(func.count(func.distinct(PlayerGameStarts.game_id)))
                .where(PlayerGameStarts.teammates_hash == lineup_hash)
            ) or 0

            logger.info("chemistry_lookup", team_id=team_id, games_together=count)

            if count >= 10:
                return 5
            elif count >= 6:
                return 3
            elif count >= 3:
                return 2
            elif count >= 1:
                return 1
            else:
                return 0

        except Exception as e:
            log_error(logger, ErrorCategory.CHEMISTRY_ERROR, "Error getting chemistry bonus", exc_info=e, team_id=team_id)
            return 0

    @staticmethod
    def generate_lineup_hash(player_ids: list[int]) -> str:
        """Generate a consistent hash for a set of player IDs."""
        sorted_ids = sorted(player_ids)
        id_string = "-".join(map(str, sorted_ids))
        return hashlib.sha256(id_string.encode()).hexdigest()

    @staticmethod
    def record_game_starts(db: Session, game_id: int, team_id: int, starters: list[int]) -> None:
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

import structlog
from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.stats import PlayerSeasonStats
from app.services.trait_service import TraitService

logger = structlog.get_logger()


class TraitAcquisitionService:
    """
    Handles logic for acquiring traits via progression, stat thresholds, and coaching unlocks.
    """

    @staticmethod
    def process_season_end_progression(db: Session, season_id: int):
        """
        Evaluates all players for potential trait acquisition at the end of the season.
        """
        logger.info("processing_season_end_traits", season_id=season_id)

        # Get all players active in the season
        # simplified: get all players on a team
        players = db.query(Player).filter(Player.team_id.isnot(None)).all()

        granted_count = 0

        for player in players:
            # 1. Check Stat Thresholds
            # We need stats for the season.
            # Assuming PlayerSeasonStats exists and is keyed by player_id, season_id
            stats = (
                db.query(PlayerSeasonStats)
                .filter(
                    PlayerSeasonStats.player_id == player.id,
                    PlayerSeasonStats.season_id == season_id,
                )
                .first()
            )

            if stats:
                new_traits = TraitAcquisitionService.check_stat_thresholds(player, stats)
                for trait_name in new_traits:
                    # Grant trait
                    result = TraitService.assign_trait(
                        db,
                        player.id,
                        trait_name,
                        source="MILESTONE",  # or DEVELOPMENT
                    )
                    if result:
                        granted_count += 1
                        logger.info("trait_granted_stat", player_id=player.id, trait=trait_name)

            # 2. Check Auto Unlocks (like Field General based on Awareness)
            # This is covered by check_trait_eligibility but we need to trigger it.
            # We can iterate through "AUTO_UNLOCK" traits in catalog relevant to player position.
            # For efficiency, we might just check specific high-value ones.
            # But let's check all relevant ones.
            # (Simplification: relying on TraitService.TRAIT_CATALOG exposure or helper)

            # 3. Progression (Development) - Random chance based on dev trait/potential?
            # Implemented as a separate pass or part of Offseason Orchestrator

        logger.info("season_end_traits_complete", granted=granted_count)
        return granted_count

    @staticmethod
    def check_stat_thresholds(player: Player, stats: PlayerSeasonStats) -> list[str]:
        """
        Checks if player stats meet thresholds for specific traits.
        Returns list of trait names to grant.
        """
        grant_list = []

        # QB Traits
        if player.position == "QB":
            # Gunslinger: > 4000 yards, > 30 TDs (Example)
            if (stats.passing_yards or 0) > 4000 and (stats.passing_tds or 0) > 30:
                grant_list.append("gunslinger")

            # Escape Artist: > 500 rushing yards for QB
            if (stats.rushing_yards or 0) > 500:
                grant_list.append("escape_artist")

        # RB Traits
        elif player.position == "RB":
            # Bruiser: > 1000 yards, > 10 TDs
            if (stats.rushing_yards or 0) > 1000 and (stats.rushing_tds or 0) > 10:
                grant_list.append("bruiser")

            # Satellite: > 50 catches
            if (stats.receptions or 0) > 50:
                grant_list.append("satellite")

        # WR Traits
        elif player.position in ["WR", "TE"]:
            # Deep Threat: > 1200 yards, > 15 YPC
            ypc = (
                (stats.receiving_yards or 0) / (stats.receptions or 1)
                if (stats.receptions or 0) > 0
                else 0
            )
            if (stats.receiving_yards or 0) > 1200 and ypc > 15.0:
                grant_list.append("deep_threat")

            # Possession Receiver: > 80 catches
            if (stats.receptions or 0) > 80:
                grant_list.append("possession_receiver")

        # DEFENSE (Simplification - needs defensive stats)
        # Assuming we have defensive stats fields on PlayerSeasonStats

        return grant_list

    @staticmethod
    def unlock_coaching_trait(db: Session, player_id: int, trait_name: str) -> bool:
        """
        Manually unlocks a coaching trait if requirements are met (e.g. coaching points).
        """
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            return False

        # Verify it's a COACHING_UNLOCK trait
        # We need to access catalog.
        # Assuming we can import TRAIT_CATALOG or check via service helper
        # For now, relying on TraitService.check_trait_eligibility which should check requirements

        # In a real implementation we would deduct "Coaching Points" here.
        # For MVP, we'll just assign it if eligible.

        return TraitService.assign_trait(db, player_id, trait_name, source="DEVELOPMENT")

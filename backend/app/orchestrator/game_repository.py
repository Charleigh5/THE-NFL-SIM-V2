"""
Game Repository.

Handles persistence of game state and player statistics.
Extracted from SimulationOrchestrator for single responsibility.
"""

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import Game
from app.models.player import Player
from app.models.stats import PlayerGameStats
from app.schemas.play import PlayResult

logger = logging.getLogger(__name__)


class GameRepository:
    """
    Handles game persistence and player stat aggregation.

    Extracted from SimulationOrchestrator to:
    - Isolate database operations from game logic
    - Enable easier mocking in unit tests
    - Improve debugging by centralizing persistence
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def save_game_progress(
        self, game_id: int, state: dict[str, Any], history: list[PlayResult]
    ) -> None:
        """
        Save current game state and play history to database.

        Args:
            game_id: The game's database ID
            state: Current game state dictionary
            history: List of PlayResult objects from the game
        """
        if not game_id:
            return

        try:
            stmt = select(Game).where(Game.id == game_id)
            result = await self.db.execute(stmt)
            game = result.scalar_one_or_none()

            if game:
                game.home_score = state.get("home_score", 0)
                game.away_score = state.get("away_score", 0)
                game.current_quarter = state.get("quarter", 1)
                game.time_left = state.get("time_left", "15:00")

                # Update game data with plays and config
                current_data = dict(game.game_data) if game.game_data else {}
                current_data["plays"] = [p.model_dump() for p in history]
                current_data["state"] = state
                game.game_data = current_data

                await self.db.commit()
                logger.debug("Game progress saved", extra={"game_id": game_id})
        except Exception:
            logger.exception("Error saving game progress", extra={"game_id": game_id})
            await self.db.rollback()

    async def finalize_game(self, game_id: int) -> Game | None:
        """
        Mark game as complete in database.

        Args:
            game_id: The game's database ID

        Returns:
            The updated Game object, or None if not found
        """
        try:
            stmt = select(Game).where(Game.id == game_id)
            result = await self.db.execute(stmt)
            game = result.scalar_one_or_none()

            if game:
                game.is_played = True
                await self.db.commit()
                logger.info("Game finalized", extra={"game_id": game_id})
                return game
        except Exception:
            logger.exception("Error finalizing game", extra={"game_id": game_id})

        return None

    async def save_player_stats(
        self, game: Game, history: list[PlayResult], player_team_map: dict[int, int]
    ) -> int:
        """
        Aggregate and save player stats from game history.

        Args:
            game: The Game object
            history: List of PlayResult objects
            player_team_map: Mapping of player_id -> team_id

        Returns:
            Number of player stat records saved
        """
        if not history:
            return 0

        logger.info("Saving player stats", extra={"game_id": game.id})

        # Aggregate stats from play history
        stats_agg = self._aggregate_stats(history)

        # Save to database
        count = 0
        for pid, stats in stats_agg.items():
            team_id = player_team_map.get(pid)
            if not team_id:
                # Fallback: query player if not in match context
                team_id = await self._get_player_team_id(pid)

            if not team_id:
                continue

            # Check if stats record exists
            stmt = select(PlayerGameStats).where(
                PlayerGameStats.player_id == pid, PlayerGameStats.game_id == game.id
            )
            result = await self.db.execute(stmt)
            pgs = result.scalar_one_or_none()

            if not pgs:
                pgs = PlayerGameStats(
                    player_id=pid,
                    game_id=game.id,
                    team_id=team_id,
                    season_id=game.season_id,
                    **stats,
                )
                self.db.add(pgs)
            else:
                # Update existing
                for k, v in stats.items():
                    setattr(pgs, k, getattr(pgs, k, 0) + v)

            count += 1

        await self.db.commit()
        logger.info("Player stats saved", extra={"game_id": game.id, "player_count": count})
        return count

    def _aggregate_stats(self, history: list[PlayResult]) -> dict[int, dict[str, int]]:
        """
        Aggregate player statistics from play history.

        Args:
            history: List of PlayResult objects

        Returns:
            Dictionary mapping player_id to stat dictionary
        """
        stats_agg: dict[int, dict[str, int]] = {}

        def get_stats(pid: int) -> dict[str, int]:
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0,
                    "pass_completions": 0,
                    "pass_yards": 0,
                    "pass_tds": 0,
                    "pass_ints": 0,
                    "rush_attempts": 0,
                    "rush_yards": 0,
                    "rush_tds": 0,
                    "targets": 0,
                    "receptions": 0,
                    "rec_yards": 0,
                    "rec_tds": 0,
                }
            return stats_agg[pid]

        for play in history:
            # Passing stats
            if play.passer_id:
                s = get_stats(play.passer_id)
                s["pass_attempts"] += 1
                if play.yards_gained > 0 or "complete" in play.description.lower():
                    s["pass_completions"] += 1
                    s["pass_yards"] += play.yards_gained

                if play.is_touchdown:
                    s["pass_tds"] += 1
                if play.is_turnover:
                    s["pass_ints"] += 1

            # Rushing stats
            if play.rusher_id:
                s = get_stats(play.rusher_id)
                s["rush_attempts"] += 1
                s["rush_yards"] += play.yards_gained
                if play.is_touchdown:
                    s["rush_tds"] += 1

            # Receiving stats
            if play.receiver_id:
                s = get_stats(play.receiver_id)
                s["targets"] += 1
                if play.yards_gained > 0 or "complete" in play.description.lower():
                    s["receptions"] += 1
                    s["rec_yards"] += play.yards_gained
                    if play.is_touchdown:
                        s["rec_tds"] += 1

        return stats_agg

    async def _get_player_team_id(self, player_id: int) -> int | None:
        """Fetch player's team ID from database."""
        stmt = select(Player).where(Player.id == player_id)
        result = await self.db.execute(stmt)
        player = result.scalar_one_or_none()
        return player.team_id if player else None

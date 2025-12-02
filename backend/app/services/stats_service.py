from sqlalchemy.orm import Session
from sqlalchemy import func, desc, select
from typing import List, Optional
from app.models.stats import PlayerGameStats
from app.models.player import Player
from app.models.team import Team
from app.models.game import Game
from app.schemas.stats import PlayerLeader

class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_league_leaders(self, season_id: int, stat_type: str, limit: int = 5) -> List[PlayerLeader]:
        """
        Get top players for a specific statistic in a season.

        Args:
            season_id: The season to query
            stat_type: One of 'passing_yards', 'passing_tds', 'rushing_yards',
                      'rushing_tds', 'receiving_yards', 'receiving_tds'
            limit: Number of results to return

        Returns:
            List of PlayerLeader objects
        """
        # Map stat_type to model column
        stat_map = {
            'passing_yards': PlayerGameStats.pass_yards,
            'passing_tds': PlayerGameStats.pass_tds,
            'rushing_yards': PlayerGameStats.rush_yards,
            'rushing_tds': PlayerGameStats.rush_tds,
            'receiving_yards': PlayerGameStats.rec_yards,
            'receiving_tds': PlayerGameStats.rec_tds
        }

        if stat_type not in stat_map:
            raise ValueError(f"Invalid stat_type: {stat_type}")

        stat_col = stat_map[stat_type]

        # Query: Join PlayerGameStats -> Game (filter season) -> Player -> Team
        # Group by Player, Sum stat
        stmt = (
            select(
                Player.id,
                Player.first_name,
                Player.last_name,
                Player.position,
                Team.name.label("team_name"),
                Team.city.label("team_city"),
                func.sum(stat_col).label("total_value")
            )
            .join(Game, PlayerGameStats.game_id == Game.id)
            .join(Player, PlayerGameStats.player_id == Player.id)
            .join(Team, PlayerGameStats.team_id == Team.id)
            .where(Game.season_id == season_id)
            .group_by(Player.id, Player.first_name, Player.last_name, Player.position, Team.name, Team.city)
            .order_by(desc("total_value"))
            .limit(limit)
        )

        results = self.db.execute(stmt).all()

        leaders = []
        for r in results:
            leaders.append(PlayerLeader(
                player_id=r.id,
                name=f"{r.first_name} {r.last_name}",
                team=f"{r.team_city} {r.team_name}",
                position=r.position,
                value=r.total_value or 0,
                stat_type=stat_type
            ))

        return leaders

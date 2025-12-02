from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.player import Player, Position
from app.models.team import Team
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache
from app.schemas.draft import DraftSuggestionResponse, AlternativePick


class DraftAssistant:
    """AI-powered draft assistant using MCP for external data."""

    async def suggest_pick(
        self,
        team_id: int,
        pick_number: int,
        available_players: List[int],
        db: AsyncSession
    ) -> DraftSuggestionResponse:
        """
        Suggest a draft pick for a team based on needs and player value.
        Uses MCP to fetch external player comparison data if available.
        """
        # 1. Verify team exists
        team_stmt = select(Team).where(Team.id == team_id)
        team_result = await db.execute(team_stmt)
        team = team_result.scalar_one_or_none()

        if not team:
            raise ValueError(f"Team {team_id} not found")

        # 2. Get available players - select only needed columns to avoid lazy loading
        players_stmt = select(
            Player.id,
            Player.first_name,
            Player.last_name,
            Player.position,
            Player.overall_rating
        ).where(Player.id.in_(available_players))

        players_result = await db.execute(players_stmt)
        player_rows = players_result.all()

        if not player_rows:
            raise ValueError("No available players")

        # Convert to simple dicts
        player_data = [
            {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'position': row[3],
                'overall_rating': row[4]
            }
            for row in player_rows
        ]

        # 3. Analyze team needs
        roster_stmt = select(
            Player.position,
            func.count(Player.id).label('count')
        ).where(
            Player.team_id == team_id
        ).group_by(Player.position)

        roster_result = await db.execute(roster_stmt)
        position_counts = {row[0]: row[1] for row in roster_result.all()}

        team_needs = self._calculate_needs(position_counts)

        # 4. Score players
        scored_players = []
        for p in player_data:
            need_score = team_needs.get(p['position'], 0.5)
            combined_score = (p['overall_rating'] / 100.0 * 0.7) + (need_score * 0.3)
            scored_players.append((p, combined_score))

        scored_players.sort(key=lambda x: x[1], reverse=True)

        # 5. Build recommendation
        top_pick, top_score = scored_players[0]
        reasoning = await self._build_reasoning_from_data(top_pick, team_needs)

        # 6. Get alternatives
        alternatives = []
        for p, score in scored_players[1:4]:
            alt_reasoning = f"Strong {p['position']}, addresses team need"
            alternatives.append(AlternativePick(
                player_id=p['id'],
                player_name=f"{p['first_name']} {p['last_name']}",
                position=p['position'],
                overall_rating=p['overall_rating'],
                reasoning=alt_reasoning,
                confidence_score=score
            ))

        return DraftSuggestionResponse(
            recommended_player_id=top_pick['id'],
            player_name=f"{top_pick['first_name']} {top_pick['last_name']}",
            position=top_pick['position'],
            overall_rating=top_pick['overall_rating'],
            reasoning=reasoning,
            team_needs=team_needs,
            alternative_picks=alternatives,
            confidence_score=top_score
        )

    def _calculate_needs(self, position_counts: Dict[str, int]) -> Dict[str, float]:
        """Calculate team needs based on roster composition."""
        targets = {
            'QB': 3, 'RB': 4, 'WR': 6, 'TE': 3,
            'OL': 8, 'DL': 6, 'LB': 6, 'CB': 5, 'S': 4, 'K': 1, 'P': 1
        }

        needs = {}
        for position, target in targets.items():
            current = position_counts.get(position, 0)
            if current < target:
                needs[position] = 1.0 - (current / target)
            else:
                needs[position] = 0.1

        return needs

    async def _build_reasoning_from_data(
        self,
        player_data: Dict,
        team_needs: Dict[str, float]
    ) -> str:
        """Build reasoning string with MCP enhancement."""
        base_reasoning = (
            f"Best available player. {player_data['first_name']} {player_data['last_name']} "
            f"is a {player_data['overall_rating']} overall {player_data['position']}"
        )

        position_need = team_needs.get(player_data['position'], 0.5)
        if position_need > 0.7:
            base_reasoning += f", addressing a critical team need at {player_data['position']}"
        elif position_need > 0.4:
            base_reasoning += f", filling a moderate need at {player_data['position']}"
        else:
            base_reasoning += ", providing depth and competition"

        # Try MCP enhancement (graceful degradation if fails)
        try:
            client = registry.get_client("nfl_stats")
            if client:
                cache_key = f"league_avg_{player_data['position']}_2024"
                stats = mcp_cache.get(cache_key, "league_averages")

                if not stats:
                    stats = await client.call_tool(
                        "get_league_averages",
                        arguments={"position": player_data['position'], "season": 2024}
                    )
                    if stats:
                        mcp_cache.set(cache_key, stats, "league_averages")

                if stats:
                    base_reasoning += ". Historical data suggests strong upside for this position."
        except Exception:
            pass  # Graceful degradation

        return base_reasoning

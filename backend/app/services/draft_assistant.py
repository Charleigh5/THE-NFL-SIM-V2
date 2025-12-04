from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.player import Player, Position
from app.models.team import Team
from app.core.mcp_registry import registry
from app.core.mcp_cache import mcp_cache
from app.schemas.draft import (
    DraftSuggestionResponse,
    AlternativePick,
    HistoricalComparison,
    RosterGapAnalysis
)
import logging

logger = logging.getLogger(__name__)

DRAFT_ANALYSIS_TEMPLATE = """
**Draft Analysis: {player_name}**
*Position: {position} | Overall: {overall_rating}*

**Team Fit:**
{team_fit_analysis}

**Market Value:**
{market_value_analysis}

**Historical Context:**
{historical_context}

**Recommendation:**
{recommendation}
"""


class DraftAssistant:
    """AI-powered draft assistant using MCP for external data."""

    async def suggest_pick(
        self,
        team_id: int,
        pick_number: int,
        available_players: List[int],
        db: AsyncSession,
        include_historical_data: bool = True
    ) -> DraftSuggestionResponse:
        """
        Suggest a draft pick for a team based on needs and player value.
        Uses MCP to fetch external player comparison data if available.

        Args:
            team_id: Team making the pick
            pick_number: Overall pick number in draft
            available_players: List of player IDs still available
            db: Database session
            include_historical_data: Whether to use MCP for historical comparisons

        Returns:
            Enhanced draft suggestion with historical comparisons and analytics
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
            Player.overall_rating,
            Player.speed,
            Player.strength,
            Player.agility
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
                'overall_rating': row[4],
                'speed': row[5],
                'strength': row[6],
                'agility': row[7]
            }
            for row in player_rows
        ]

        # 3. Analyze team needs with detailed gap analysis
        roster_stmt = select(
            Player.position,
            func.count(Player.id).label('count'),
            func.avg(Player.overall_rating).label('avg_rating')
        ).where(
            Player.team_id == team_id
        ).group_by(Player.position)

        roster_result = await db.execute(roster_stmt)
        position_stats = {
            row[0]: {'count': row[1], 'avg_rating': row[2] or 0}
            for row in roster_result.all()
        }

        team_needs, roster_gaps = self._calculate_needs_and_gaps(position_stats)

        # 4. Calculate draft value for pick position
        draft_value_multiplier = self._calculate_draft_value_multiplier(pick_number)

        # 5. Score players with enhanced metrics
        scored_players = []
        for p in player_data:
            need_score = team_needs.get(p['position'], 0.5)

            # Enhanced scoring considering pick value
            talent_score = p['overall_rating'] / 100.0
            value_score = talent_score * draft_value_multiplier
            combined_score = min(1.0, (talent_score * 0.5) + (need_score * 0.3) + (value_score * 0.2))

            scored_players.append((p, combined_score))

        scored_players.sort(key=lambda x: x[1], reverse=True)

        # 6. Build recommendation with MCP enhancement
        top_pick, top_score = scored_players[0]

        historical_comparison = None
        mcp_data_used = False

        if include_historical_data:
            historical_comparison, mcp_data_used = await self._get_historical_comparison(
                top_pick
            )

        reasoning = await self._build_reasoning_from_data(
            top_pick,
            team_needs,
            historical_comparison,
            pick_number
        )

        # 7. Calculate overall draft value score
        draft_value_score = self._calculate_draft_value_score(
            top_pick['overall_rating'],
            pick_number,
            team_needs.get(top_pick['position'], 0.5)
        )

        # 8. Get alternatives with historical data
        alternatives = []
        for p, score in scored_players[1:4]:
            alt_historical = None
            if include_historical_data:
                alt_historical, _ = await self._get_historical_comparison(p)

            alt_reasoning = self._build_alternative_reasoning(
                p,
                team_needs,
                alt_historical
            )

            alternatives.append(AlternativePick(
                player_id=p['id'],
                player_name=f"{p['first_name']} {p['last_name']}",
                position=p['position'],
                overall_rating=p['overall_rating'],
                reasoning=alt_reasoning,
                confidence_score=score,
                historical_comparison=alt_historical
            ))

        return DraftSuggestionResponse(
            recommended_player_id=top_pick['id'],
            player_name=f"{top_pick['first_name']} {top_pick['last_name']}",
            position=top_pick['position'],
            overall_rating=top_pick['overall_rating'],
            reasoning=reasoning,
            team_needs=team_needs,
            alternative_picks=alternatives,
            confidence_score=top_score,
            historical_comparison=historical_comparison,
            roster_gap_analysis=roster_gaps,
            draft_value_score=draft_value_score,
            mcp_data_used=mcp_data_used
        )

    def _calculate_needs_and_gaps(
        self,
        position_stats: Dict[str, Dict]
    ) -> tuple[Dict[str, float], List[RosterGapAnalysis]]:
        """Calculate team needs and detailed roster gap analysis."""
        targets = {
            'QB': 3, 'RB': 4, 'WR': 6, 'TE': 3,
            'OL': 8, 'DL': 6, 'LB': 6, 'CB': 5, 'S': 4, 'K': 1, 'P': 1
        }

        needs = {}
        gaps = []

        for position, target in targets.items():
            stats = position_stats.get(position, {'count': 0, 'avg_rating': 0})
            current = stats['count']
            avg_rating = stats['avg_rating']

            # Calculate need score
            if current < target:
                need_score = 1.0 - (current / target)
            else:
                need_score = 0.1

            # Adjust for quality
            if avg_rating < 70:
                need_score = min(1.0, need_score + 0.2)

            needs[position] = need_score

            # Determine priority level
            if need_score > 0.7:
                priority = "CRITICAL"
            elif need_score > 0.5:
                priority = "HIGH"
            elif need_score > 0.3:
                priority = "MODERATE"
            else:
                priority = "LOW"

            gaps.append(RosterGapAnalysis(
                position=position,
                current_count=current,
                target_count=target,
                starter_quality=avg_rating / 100.0,
                priority_level=priority
            ))

        return needs, gaps

    def _calculate_draft_value_multiplier(self, pick_number: int) -> float:
        """
        Calculate value multiplier based on pick position.
        Early picks should yield more value.
        """
        if pick_number <= 10:
            return 1.3  # Top 10 picks
        elif pick_number <= 32:
            return 1.2  # First round
        elif pick_number <= 64:
            return 1.1  # Second round
        elif pick_number <= 100:
            return 1.0  # Third round
        else:
            return 0.9  # Later rounds

    def _calculate_draft_value_score(
        self,
        overall_rating: int,
        pick_number: int,
        need_score: float
    ) -> float:
        """
        Calculate draft value score (1-10) based on:
        - Player talent vs pick position
        - Team need satisfaction
        """
        # Expected rating by pick
        if pick_number <= 10:
            expected_rating = 85
        elif pick_number <= 32:
            expected_rating = 80
        elif pick_number <= 64:
            expected_rating = 75
        elif pick_number <= 100:
            expected_rating = 70
        else:
            expected_rating = 65

        talent_value = (overall_rating / expected_rating) * 5  # 0-10 scale
        need_value = need_score * 5  # 0-5 scale

        total_score = min(10.0, talent_value + need_value)
        return round(total_score, 1)

    async def _get_historical_comparison(
        self,
        player_data: Dict
    ) -> tuple[Optional[HistoricalComparison], bool]:
        """
        Fetch historical player comparison using NFL Stats MCP.
        Returns (comparison, mcp_data_used)
        """
        try:
            client = registry.get_client("nfl_stats")
            if not client:
                logger.debug("NFL Stats MCP client not available")
                return None, False

            cache_key = f"historical_comp_{player_data['position']}_{player_data['overall_rating']}"
            cached_data = mcp_cache.get(cache_key, "historical_comparisons")

            if cached_data:
                logger.debug(f"Cache hit for historical comparison: {cache_key}")
                return HistoricalComparison(**cached_data), True

            # Call MCP tool for historical data
            result = await client.call_tool(
                "get_player_career_stats",
                arguments={
                    "player_name": f"{player_data['first_name']} {player_data['last_name']}",
                    "position": player_data['position']
                }
            )

            if result and isinstance(result, dict):
                comparison = HistoricalComparison(
                    comparable_player_name=result.get('name', 'Similar Player'),
                    seasons_active=result.get('years_active', 'N/A'),
                    career_highlights=result.get('highlights', 'Solid career stats'),
                    similarity_score=0.85  # Placeholder - would be calculated by MCP
                )

                # Cache the result
                mcp_cache.set(cache_key, comparison.model_dump(), "historical_comparisons")
                logger.info(f"Retrieved historical comparison via MCP for {player_data['position']}")
                return comparison, True

        except Exception as e:
            logger.warning(f"MCP historical comparison failed: {str(e)}")

        return None, False

    async def _build_reasoning_from_data(
        self,
        player_data: Dict,
        team_needs: Dict[str, float],
        historical_comparison: Optional[HistoricalComparison],
        pick_number: int
    ) -> str:
        """Build comprehensive reasoning with MCP enhancement."""
        position = player_data['position']
        overall = player_data['overall_rating']
        need_score = team_needs.get(position, 0.5)

        # 1. Team Fit Analysis
        if need_score > 0.7:
            team_fit = f"Critical need. The team is significantly understaffed at {position}."
        elif need_score > 0.4:
            team_fit = f"Moderate need. Adding depth at {position} would be beneficial."
        else:
            team_fit = f"Luxury pick. The team is well-stocked at {position}, but talent is hard to pass up."

        # 2. Market Value Analysis
        if overall > 80:
            market_value = f"Elite prospect. Excellent value for pick #{pick_number}."
        elif overall > 70:
            market_value = f"Strong prospect. Good value for pick #{pick_number}."
        else:
            market_value = f"Developmental prospect. Reasonable for pick #{pick_number}."

        # 3. Historical Context
        if historical_comparison:
            historical_context = (
                f"Projects similar to {historical_comparison.comparable_player_name} "
                f"({historical_comparison.seasons_active}). "
                f"{historical_comparison.career_highlights}"
            )
        else:
            historical_context = "No direct historical comparison available."
            # Try to get league averages if not already handled
            try:
                client = registry.get_client("nfl_stats")
                if client:
                    cache_key = f"league_avg_{position}_2024"
                    stats = mcp_cache.get(cache_key, "league_averages")
                    if not stats:
                        stats = await client.call_tool(
                            "get_league_averages",
                            arguments={"position": position, "season": 2024}
                        )
                        if stats:
                            mcp_cache.set(cache_key, stats, "league_averages")

                    if stats:
                        historical_context = f"League average for {position} in 2024 suggests high value for this archetype."
            except Exception:
                pass

        # 4. Recommendation
        recommendation = f"Draft {player_data['first_name']} {player_data['last_name']}."
        if need_score > 0.6 and overall > 75:
            recommendation += " This is a can't-miss pick for your team."

        return DRAFT_ANALYSIS_TEMPLATE.format(
            player_name=f"{player_data['first_name']} {player_data['last_name']}",
            position=position,
            overall_rating=overall,
            team_fit_analysis=team_fit,
            market_value_analysis=market_value,
            historical_context=historical_context,
            recommendation=recommendation
        )

    def _build_alternative_reasoning(
        self,
        player_data: Dict,
        team_needs: Dict[str, float],
        historical_comparison: Optional[HistoricalComparison]
    ) -> str:
        """Build concise reasoning for alternative picks."""
        position_need = team_needs.get(player_data['position'], 0.5)

        if historical_comparison:
            return (
                f"Strong {player_data['position']} prospect "
                f"(similar to {historical_comparison.comparable_player_name}). "
                f"{'Addresses team need' if position_need > 0.5 else 'Adds depth'}"
            )
        else:
            return (
                f"{player_data['overall_rating']} overall {player_data['position']}. "
                f"{'High priority position' if position_need > 0.5 else 'Quality depth option'}"
            )

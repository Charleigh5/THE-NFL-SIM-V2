"""
Enhanced OL Chemistry Service with progressive scaling and advanced effects.

This service extends the existing PreGameService with sophisticated chemistry
calculations, progressive bonuses, and advanced gameplay modifiers.
"""

import math
import hashlib
from typing import Dict, List, Tuple, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.player import Player
from app.models.game import Game
from app.models.stats import PlayerGameStart
from app.services.depth_chart_service import DepthChartService
from app.orchestrator.match_context import MatchContext
import logging

logger = logging.getLogger(__name__)


class ChemistryMetadata:
    """
    Data class representing chemistry state for an OL unit.
    """
    def __init__(
        self,
        chemistry_level: float,
        consecutive_games: int,
        player_ids: List[int],
        position_map: Dict[str, int],
        bonuses: Dict[str, float],
        advanced_effects: Dict[str, float]
    ):
        self.chemistry_level = chemistry_level
        self.consecutive_games = consecutive_games
        self.player_ids = player_ids
        self.position_map = position_map
        self.bonuses = bonuses
        self.advanced_effects = advanced_effects
        self.lineup_hash = self._calculate_lineup_hash()

    def _calculate_lineup_hash(self) -> str:
        """Generate deterministic hash for current OL lineup"""
        lineup_string = ",".join(
            f"{pos}:{pid}" for pos, pid in sorted(self.position_map.items())
        )
        return hashlib.md5(lineup_string.encode()).hexdigest()[:12]

    def to_dict(self) -> Dict:
        """Serialize for API response"""
        return {
            "chemistry_level": round(self.chemistry_level, 2),
            "consecutive_games": self.consecutive_games,
            "lineup_hash": self.lineup_hash,
            "player_ids": self.player_ids,
            "position_map": self.position_map,
            "bonuses": self.bonuses,
            "advanced_effects": self.advanced_effects,
            "status": self._get_status_label()
        }

    def _get_status_label(self) -> str:
        """Get human-readable chemistry status"""
        if self.chemistry_level == 0:
            return "NONE"
        elif self.chemistry_level < 0.7:
            return "DEVELOPING"
        elif self.chemistry_level < 0.9:
            return "STRONG"
        elif self.chemistry_level < 1.0:
            return "ELITE"
        else:
            return "MAXIMUM"


from app.core.redis_cache import chemistry_cache

class EnhancedChemistryService:
    """
    Enhanced chemistry service with progressive scaling, advanced effects,
    and full metadata tracking.
    """

    # Configuration Constants
    CHEMISTRY_THRESHOLD_GAMES = 5
    CHEMISTRY_MAX_GAMES = 10
    BASE_BONUS_MULTIPLIER = 5.0  # Max blocking bonus at 100% chemistry

    OL_POSITIONS = ["LT", "LG", "C", "RG", "RT"]

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # CORE CHEMISTRY CALCULATION
    # ========================================================================

    @staticmethod
    def calculate_chemistry_level(consecutive_games: int) -> float:
        """
        Calculate chemistry level using logarithmic progression.

        Args:
            consecutive_games: Number of consecutive games OL has started together

        Returns:
            Chemistry level from 0.0 (none) to 1.0 (maximum)
        """
        if consecutive_games < EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES:
            return 0.0

        if consecutive_games >= EnhancedChemistryService.CHEMISTRY_MAX_GAMES:
            return 1.0

        # Normalize to 0.0-1.0 range between threshold and max
        normalized = (
            (consecutive_games - EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES) /
            (EnhancedChemistryService.CHEMISTRY_MAX_GAMES - EnhancedChemistryService.CHEMISTRY_THRESHOLD_GAMES)
        )

        # Logarithmic curve: fast growth early, slower later
        # Formula: 0.6 + 0.4 * (1 - e^(-2.5x))
        chemistry_level = 0.6 + (0.4 * (1 - math.exp(-2.5 * normalized)))

        return min(1.0, chemistry_level)

    def calculate_scaled_bonuses(self, chemistry_level: float) -> Dict[str, float]:
        """
        Calculate attribute bonuses based on chemistry level.

        Args:
            chemistry_level: 0.0 to 1.0

        Returns:
            Dictionary of attribute bonuses
        """
        base_multiplier = self.BASE_BONUS_MULTIPLIER

        return {
            "pass_block": chemistry_level * base_multiplier,
            "run_block": chemistry_level * base_multiplier,
            "awareness": chemistry_level * base_multiplier
        }

    def calculate_advanced_effects(self, chemistry_level: float) -> Dict[str, float]:
        """
        Calculate advanced gameplay effects based on chemistry level.

        Args:
            chemistry_level: 0.0 to 1.0

        Returns:
            Dictionary of advanced effect modifiers
        """
        return {
            "stunt_pickup_bonus": chemistry_level * 0.25,  # Up to +25% stunt recognition
            "penalty_reduction": chemistry_level * 0.20,   # Up to -20% penalties
            "communication_boost": chemistry_level * 10.0,  # Up to +10 communication
            "blitz_pickup_improvement": chemistry_level * 0.30  # Up to +30% blitz pickup
        }

    # ========================================================================
    # CHEMISTRY DETECTION & TRACKING
    # ========================================================================

    async def get_team_chemistry_metadata(
        self,
        team_id: int,
        current_starters: Dict[str, int],
        season_id: int = 2025, # Default for now
        week: int = 1 # Default for now
    ) -> ChemistryMetadata:
        """
        Analyze team's OL chemistry based on historical starts.
        Checks cache first, then falls back to optimized DB query.

        Args:
            team_id: Team ID to analyze
            current_starters: Dict[position, player_id] for current OL
            season_id: Current season ID
            week: Current week

        Returns:
            ChemistryMetadata object with full chemistry state
        """
        # TRY CACHE FIRST
        cached = await chemistry_cache.get(
            team_id=team_id,
            season_id=season_id,
            week=week,
            lineup=current_starters
        )

        if cached:
            # Cache hit! Reconstruct metadata from cached data
            return ChemistryMetadata(
                chemistry_level=cached['chemistry_level'],
                consecutive_games=cached['consecutive_games'],
                player_ids=cached['player_ids'],
                position_map=cached['position_map'],
                bonuses=cached['bonuses'],
                advanced_effects=cached['advanced_effects']
            )

        # Cache miss - calculate using optimized query
        metadata = await self.get_team_chemistry_metadata_optimized(
            team_id, current_starters
        )

        # Store in cache for next time
        await chemistry_cache.set(
            team_id=team_id,
            season_id=season_id,
            week=week,
            lineup=current_starters,
            metadata=metadata.to_dict()
        )

        return metadata

    async def get_team_chemistry_metadata_optimized(
        self,
        team_id: int,
        current_starters: Dict[str, int]
    ) -> ChemistryMetadata:
        """
        OPTIMIZED: Single-query chemistry calculation.

        Performance optimizations:
        1. Single JOIN query instead of N+1
        2. In-memory processing
        3. Early termination on lineup mismatch
        """
        # Validate input
        if len(current_starters) < 5:
            return self._empty_chemistry_metadata()

        # OPTIMIZATION 1: Batch load with single query
        stmt = (
            select(Game.id, Game.week, PlayerGameStart.position, PlayerGameStart.player_id)
            .join(PlayerGameStart, Game.id == PlayerGameStart.game_id)
            .filter(
                (Game.home_team_id == team_id) | (Game.away_team_id == team_id),
                Game.is_played == True,
                PlayerGameStart.team_id == team_id,
                PlayerGameStart.position.in_(self.OL_POSITIONS)
            )
            .order_by(desc(Game.season), desc(Game.week))
            .limit(self.CHEMISTRY_MAX_GAMES * 5)  # 10 games × 5 positions
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        if not rows:
            return self._empty_chemistry_metadata()

        # OPTIMIZATION 2: Group by game_id in memory (no additional queries)
        games_data = {}
        for game_id, week, position, player_id in rows:
            if game_id not in games_data:
                games_data[game_id] = {}
            games_data[game_id][position] = player_id

        # OPTIMIZATION 3: Count consecutive games with early termination
        consecutive_games = 0

        for game_id in sorted(games_data.keys(), reverse=True):
            game_lineup = games_data[game_id]

            # Check match
            if self._lineups_match(current_starters, game_lineup):
                consecutive_games += 1
            else:
                # EARLY TERMINATION: Stop at first mismatch
                break

            # EARLY TERMINATION: Stop at max
            if consecutive_games >= self.CHEMISTRY_MAX_GAMES:
                break

        # Calculate chemistry
        chemistry_level = self.calculate_chemistry_level(consecutive_games)
        bonuses = self.calculate_scaled_bonuses(chemistry_level)
        advanced_effects = self.calculate_advanced_effects(chemistry_level)

        return ChemistryMetadata(
            chemistry_level=chemistry_level,
            consecutive_games=consecutive_games,
            player_ids=list(current_starters.values()),
            position_map=current_starters,
            bonuses=bonuses,
            advanced_effects=advanced_effects
        )

    def _lineups_match(
        self,
        lineup_a: Dict[str, int],
        lineup_b: Dict[str, int]
    ) -> bool:
        """Check if two OL lineups are identical"""
        if len(lineup_a) != len(lineup_b):
            return False

        for pos in self.OL_POSITIONS:
            if lineup_a.get(pos) != lineup_b.get(pos):
                return False

        return True

    def _empty_chemistry_metadata(self) -> ChemistryMetadata:
        """Return metadata for no chemistry"""
        return ChemistryMetadata(
            chemistry_level=0.0,
            consecutive_games=0,
            player_ids=[],
            position_map={},
            bonuses={"pass_block": 0.0, "run_block": 0.0, "awareness": 0.0},
            advanced_effects={
                "stunt_pickup_bonus": 0.0,
                "penalty_reduction": 0.0,
                "communication_boost": 0.0,
                "blitz_pickup_improvement": 0.0
            }
        )

    # ========================================================================
    # APPLICATION TO MATCH CONTEXT
    # ========================================================================

    async def apply_chemistry_to_match_context(
        self,
        match_context: MatchContext
    ) -> Tuple[Optional[ChemistryMetadata], Optional[ChemistryMetadata]]:
        """
        Apply chemistry bonuses to both teams in match context.

        Args:
            match_context: MatchContext with loaded rosters

        Returns:
            Tuple of (home_chemistry, away_chemistry) metadata
        """
        home_chemistry = await self._apply_team_chemistry(
            match_context.home_team_id,
            match_context.home_roster
        )

        away_chemistry = await self._apply_team_chemistry(
            match_context.away_team_id,
            match_context.away_roster
        )

        # Store metadata in match context for PlayResolver access
        match_context.home_ol_chemistry = home_chemistry
        match_context.away_ol_chemistry = away_chemistry

        return home_chemistry, away_chemistry

    async def _apply_team_chemistry(
        self,
        team_id: int,
        roster: Dict[int, Player]
    ) -> Optional[ChemistryMetadata]:
        """Apply chemistry bonuses to one team"""
        roster_list = list(roster.values())

        # Get current starters
        starters_map = DepthChartService.get_starting_offense(roster_list, "standard")

        # Extract OL starters
        current_ol = {}
        for pos in self.OL_POSITIONS:
            if pos in starters_map:
                current_ol[pos] = starters_map[pos].id

        if len(current_ol) < 5:
            return None

        # Get chemistry metadata
        chemistry = await self.get_team_chemistry_metadata(team_id, current_ol)

        if chemistry.chemistry_level > 0:
            logger.info(
                f"Applying OL Chemistry to Team {team_id}",
                extra={
                    "chemistry_level": chemistry.chemistry_level,
                    "consecutive_games": chemistry.consecutive_games,
                    "bonuses": chemistry.bonuses
                }
            )

            # Apply bonuses to players
            for player_id in chemistry.player_ids:
                player = roster.get(player_id)
                if player:
                    if not hasattr(player, "active_modifiers"):
                        player.active_modifiers = {}

                    # Apply scaled bonuses
                    for attr, bonus in chemistry.bonuses.items():
                        player.active_modifiers[attr] = (
                            player.active_modifiers.get(attr, 0) + bonus
                        )

                    # Store advanced effects metadata
                    if not hasattr(player, "chemistry_effects"):
                        player.chemistry_effects = {}

                    player.chemistry_effects = chemistry.advanced_effects

        return chemistry

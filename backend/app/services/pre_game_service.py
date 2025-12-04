from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.stats import PlayerGameStart
from app.models.player import Player
from app.models.game import Game
from app.services.depth_chart_service import DepthChartService
from app.orchestrator.match_context import MatchContext
from app.services.enhanced_chemistry_service import EnhancedChemistryService
from app.services.trait_service import TraitService, TRAIT_CATALOG
import logging

logger = logging.getLogger(__name__)

class PreGameService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.enhanced_chemistry = EnhancedChemistryService(db)
        self.trait_service = TraitService(db)  # NEW: Trait service

    async def apply_chemistry_boosts(self, match_context: MatchContext):
        """
        ENHANCED: Use new scaling chemistry service
        """
        # Use enhanced service instead of old logic
        home_chem, away_chem = await self.enhanced_chemistry.apply_chemistry_to_match_context(
            match_context
        )

        # Log results
        if home_chem and home_chem.chemistry_level > 0:
            logger.info(
                f"Home OL Chemistry Active: {home_chem.chemistry_level:.2f} "
                f"({home_chem.consecutive_games} games)"
            )

        if away_chem and away_chem.chemistry_level > 0:
            logger.info(
                f"Away OL Chemistry Active: {away_chem.chemistry_level:.2f} "
                f"({away_chem.consecutive_games} games)"
            )

    async def apply_trait_effects(self, match_context: MatchContext):
        """
        Load and apply all player traits before game starts.
        Handles both individual and team-wide trait effects.
        """
        await self._apply_team_traits(match_context.home_team_id, match_context.home_roster)
        await self._apply_team_traits(match_context.away_team_id, match_context.away_roster)

    async def _apply_team_traits(self, team_id: int, roster: dict[int, Player]):
        """Apply traits for a single team"""
        field_general_active = False
        green_dot_active = False

        # Load traits for all players
        for player_id, player in roster.items():
            # Get player's traits
            trait_defs = await self.trait_service.get_player_traits(player_id)

            if not trait_defs:
                continue

            # Initialize trait storage on player
            if not hasattr(player, "active_traits"):
                player.active_traits = []
            if not hasattr(player, "trait_effects"):
                player.trait_effects = {}

            # Apply each trait
            for trait_def in trait_defs:
                player.active_traits.append(trait_def.name)

                # Check if trait is active (simplified - assume ON_FIELD traits are active)
                if "ON_FIELD" in trait_def.activation_triggers:
                    # Apply individual effects
                    for effect_key, effect_value in trait_def.effects.items():
                        player.trait_effects[effect_key] = effect_value

                    # Track team-wide traits
                    if trait_def.name == "Field General" and player.position == "QB":
                        field_general_active = True
                        logger.info(f"Field General active for Team {team_id}: {player.first_name} {player.last_name}")

                    if trait_def.name == "Green Dot (Defensive Captain)" and player.position == "LB":
                        green_dot_active = True
                        logger.info(f"Green Dot active for Team {team_id}: {player.first_name} {player.last_name}")

        # Apply team-wide boosts
        if field_general_active:
            self._apply_field_general_boost(roster, offense=True)

        if green_dot_active:
            self._apply_green_dot_boost(roster)

    def _apply_field_general_boost(self, roster: dict[int, Player], offense: bool = True):
        """Apply Field General team-wide awareness boost to offensive players"""
        for player in roster.values():
            # Apply to offensive positions
            if player.position in ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT"]:
                if not hasattr(player, "active_modifiers"):
                    player.active_modifiers = {}

                # +5 awareness to all offensive players
                player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5
                logger.debug(f"Field General boost applied to {player.last_name} ({player.position})")

    def _apply_green_dot_boost(self, roster: dict[int, Player]):
        """Apply Green Dot team-wide boost to defensive players"""
        for player in roster.values():
            # Apply to defensive positions
            if player.position in ["DE", "DT", "LB", "CB", "S"]:
                if not hasattr(player, "active_modifiers"):
                    player.active_modifiers = {}

                # +5 play recognition to all defenders
                player.active_modifiers["play_recognition"] = player.active_modifiers.get("play_recognition", 0) + 5
                logger.debug(f"Green Dot boost applied to {player.last_name} ({player.position})")

    async def _check_and_apply_team_chemistry(self, team_id: int, roster: dict[int, Player]):
        # 1. Identify current starters
        roster_list = list(roster.values())

        # Get OL starters (Standard formation usually includes all 5 OL)
        starters_map = DepthChartService.get_starting_offense(roster_list, "standard")

        ol_positions = ["LT", "LG", "C", "RG", "RT"]
        current_ol_ids = {}
        for pos in ol_positions:
            if pos in starters_map:
                current_ol_ids[pos] = starters_map[pos].id

        if len(current_ol_ids) < 5:
            # Not a full line, skip
            return

        # 2. Check history
        # Find last 5 played games for this team
        stmt = select(Game).filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id),
            Game.is_played == True
        ).order_by(desc(Game.season), desc(Game.week)).limit(5)

        result = await self.db.execute(stmt)
        last_games = result.scalars().all()

        # If fewer than 5 games played, we can't have a streak of 5
        # But maybe the threshold is lower? User said "e.g., 5 games".
        # If they have 3 games, streak is 3. If threshold is 5, we need 5.
        if len(last_games) < 5:
            return

        consecutive_games = 0

        for game in last_games:
            # Check if the SAME players started at the SAME positions in this game
            stmt = select(PlayerGameStart).filter(
                PlayerGameStart.game_id == game.id,
                PlayerGameStart.team_id == team_id,
                PlayerGameStart.position.in_(ol_positions)
            )
            result = await self.db.execute(stmt)
            starts = result.scalars().all()

            # Convert to map
            game_starters = {s.position: s.player_id for s in starts}

            # Compare with current
            match = True
            for pos in ol_positions:
                # If the starter in the past game is different or missing, streak breaks
                if pos not in game_starters or game_starters[pos] != current_ol_ids.get(pos):
                    match = False
                    break

            if match:
                consecutive_games += 1
            else:
                # Streak broken
                break

        # 3. Apply boost if threshold met
        if consecutive_games >= 5:
            logger.info(f"Applying OL Chemistry Boost for Team {team_id} (Streak: {consecutive_games})")
            for pos, player_id in current_ol_ids.items():
                player = roster.get(player_id)
                if player:
                    if not hasattr(player, "active_modifiers"):
                        player.active_modifiers = {}

                    # Boost Attributes
                    # Using a simple +5 for now as per example
                    player.active_modifiers["pass_block"] = player.active_modifiers.get("pass_block", 0) + 5
                    player.active_modifiers["run_block"] = player.active_modifiers.get("run_block", 0) + 5
                    player.active_modifiers["awareness"] = player.active_modifiers.get("awareness", 0) + 5

    async def record_starters(self, game_id: int, home_team_id: int, away_team_id: int):
        """
        Record the starters for the current game.
        Should be called after the game starts or ends.
        """
        game_stmt = select(Game).where(Game.id == game_id)
        result = await self.db.execute(game_stmt)
        game = result.scalar_one_or_none()

        if not game:
            logger.error(f"Game {game_id} not found when recording starters")
            return

        await self._record_team_starters(game, home_team_id)
        await self._record_team_starters(game, away_team_id)

        await self.db.commit()

    async def _record_team_starters(self, game: Game, team_id: int):
        # Fetch roster
        stmt = select(Player).where(Player.team_id == team_id)
        result = await self.db.execute(stmt)
        players = result.scalars().all()
        roster_list = list(players)

        # Get starters
        starters_map = DepthChartService.get_starting_offense(roster_list, "standard")

        # We focus on OL for now, but could record all
        ol_positions = ["LT", "LG", "C", "RG", "RT"]

        for pos, player in starters_map.items():
            if pos in ol_positions:
                # Check if already recorded
                stmt = select(PlayerGameStart).filter(
                    PlayerGameStart.game_id == game.id,
                    PlayerGameStart.team_id == team_id,
                    PlayerGameStart.position == pos
                )
                result = await self.db.execute(stmt)
                existing = result.scalar_one_or_none()

                if not existing:
                    new_start = PlayerGameStart(
                        player_id=player.id,
                        game_id=game.id,
                        team_id=team_id,
                        season_id=game.season_id,
                        week=game.week,
                        position=pos
                    )
                    self.db.add(new_start)

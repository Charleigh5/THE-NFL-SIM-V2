from app.orchestrator.play_resolver import PlayResolver
from app.orchestrator.play_commands import PassPlayCommand, RunPlayCommand
from app.orchestrator.play_caller import PlayCaller, PlayCallingContext
from app.schemas.play import PlayResult
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.models.player import Player
from app.orchestrator.match_context import MatchContext
from app.orchestrator.kernels.cortex_kernel import GameSituation
from app.core.random_utils import DeterministicRNG

from typing import List, Optional, Callable, Awaitable, Any
import asyncio
import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

logger = logging.getLogger(__name__)

class SimulationOrchestrator:
    """
    Orchestrates the setup and execution of a simulation.
    """
    def __init__(self) -> None:
        # Initialize with a default seed for startup/testing
        self.rng = DeterministicRNG("initial_boot_seed")

        self.play_resolver = PlayResolver(self.rng)
        self.play_caller = PlayCaller(self.rng, aggression=0.5) # Default balanced coach
        self.history: List[PlayResult] = []

        # Game State
        self.is_running = False
        self.current_quarter = 1
        self.time_left = "15:00"
        self.home_score = 0
        self.away_score = 0
        self.possession = "home"  # "home" or "away"
        self.down = 1
        self.distance = 10
        self.yard_line = 25  # 0-100, where 50 is midfield

        # Database Session
        self.db_session: Optional[AsyncSession] = None
        self.current_game_id = None

        # Match Context (Data Hydration)
        self.match_context: Optional[MatchContext] = None

        # Callbacks for WebSocket broadcasting
        self.on_play_complete: Optional[Callable[[PlayResult], Awaitable[None]]] = None
        self.on_game_update: Optional[Callable[[dict], Awaitable[None]]] = None

        # Configuration
        self.play_delay_seconds = 5.0  # Delay between plays for animation
        self.game_config = {}

    async def start_new_game_session(self, home_team_id: int, away_team_id: int, config: Optional[dict] = None, db_session: Optional[AsyncSession] = None) -> None:
        """Initialize a new game session in the database."""
        self.game_config = config or {}
        self.db_session = db_session

        if self.db_session:
            new_game = Game(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                date=datetime.datetime.now(datetime.UTC),
                season=2025,
                week=1,
                is_played=False,
                game_data={"config": config} if config else {}
            )
            self.db_session.add(new_game)
            await self.db_session.commit()
            await self.db_session.refresh(new_game)
            self.current_game_id = new_game.id

            # Initialize Deterministic RNG with Game ID
            self.rng = DeterministicRNG(new_game.id)
            # Update components with new RNG
            self.play_resolver.rng = self.rng
            self.play_caller.rng = self.rng

            # Hydrate Match Context
            logger.info("Hydrating match context", extra={"game_id": new_game.id})

            # Initialize MatchContext with rosters and weather config
            weather_config = self.game_config.get("weather", {"temperature": 70, "condition": "Sunny"})

            # Create MatchContext instance with home/away teams
            self.match_context = MatchContext(home_team_id, away_team_id, self.db_session, weather_config=weather_config)
            await self.match_context.load_rosters()

            # --- Pre-Game Services ---
            try:
                from app.services.pre_game_service import PreGameService
                pre_game_service = PreGameService(self.db_session)

                # 1. Apply Unit Chemistry Boosts
                await pre_game_service.apply_chemistry_boosts(self.match_context)

                # 2. Record Starters (for future chemistry)
                await pre_game_service.record_starters(new_game.id, home_team_id, away_team_id)

                logger.info("Pre-game services executed", extra={"game_id": new_game.id})
            except Exception as e:
                logger.error("Error executing pre-game services", exc_info=e)
            # -------------------------

            # Register players with Kernels
            self.play_resolver.register_players(self.match_context)

            logger.info(
                "Match context hydrated",
                extra={
                    "game_id": new_game.id,
                    "home_roster_size": len(self.match_context.home_roster),
                    "away_roster_size": len(self.match_context.away_roster),
                },
            )
        else:
            # Fallback for no DB (testing)
             weather_config = self.game_config.get("weather", {"temperature": 70, "condition": "Sunny"})
             # This will fail if MatchContext needs DB, but for now assume it's okay if we mock it?
             # Actually MatchContext needs DB to load rosters.
             # So we assume db_session is provided.
             pass

    async def _save_progress(self) -> None:
        """Save current game state and history to database."""
        if not self.db_session or not self.current_game_id:
            return

        try:
            stmt = select(Game).where(Game.id == self.current_game_id)
            result = await self.db_session.execute(stmt)
            game = result.scalar_one_or_none()

            if game:
                game.home_score = self.home_score
                game.away_score = self.away_score
                game.current_quarter = self.current_quarter
                game.time_left = self.time_left

                # Update game data with plays and config
                current_data = dict(game.game_data) if game.game_data else {}
                current_data["plays"] = [p.model_dump() for p in self.history]
                current_data["state"] = self.get_game_state()
                game.game_data = current_data

                await self.db_session.commit()
        except Exception as e:
            logger.exception("Error saving game progress", extra={"game_id": self.current_game_id})
            await self.db_session.rollback()

    async def save_game_result(self) -> None:
        """Finalize the game in the database."""
        if not self.db_session or not self.current_game_id:
            return

        try:
            stmt = select(Game).where(Game.id == self.current_game_id)
            result = await self.db_session.execute(stmt)
            game = result.scalar_one_or_none()

            if game:
                game.is_played = True
                # Save player stats
                await self._save_player_stats()
                await self._save_progress() # Ensure final state is saved

                logger.info("Finalized game result", extra={"game_id": self.current_game_id})
        except Exception as e:
            logger.exception("Error finalizing game", extra={"game_id": self.current_game_id})
        finally:
            # Cleanup Match Context
            self.match_context = None

            if self.db_session:
                # We don't close the session here as it's injected
                self.db_session = None
            self.current_game_id = None

    async def _save_player_stats(self, game: Game = None) -> None:
        """Aggregate and save player stats from game history."""
        if not self.history:
            return

        # If game object not passed, fetch it
        if not game and self.current_game_id:
             stmt = select(Game).where(Game.id == self.current_game_id)
             result = await self.db_session.execute(stmt)
             game = result.scalar_one_or_none()

        if not game: return

        logger.info("Saving player stats", extra={"game_id": game.id})

        # 1. Map player IDs to Team IDs
        player_team_map = {}
        if self.match_context:
            for pid, p in self.match_context.home_roster.items():
                player_team_map[pid] = game.home_team_id
            for pid, p in self.match_context.away_roster.items():
                player_team_map[pid] = game.away_team_id

        # 2. Aggregate Stats
        # Structure: player_id -> {stat_name: value}
        stats_agg = {}

        def get_stats(pid):
            if pid not in stats_agg:
                stats_agg[pid] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0, "pass_ints": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0
                }
            return stats_agg[pid]

        for play in self.history:
            # Passing
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

            # Rushing
            if play.rusher_id:
                s = get_stats(play.rusher_id)
                s["rush_attempts"] += 1
                s["rush_yards"] += play.yards_gained
                if play.is_touchdown:
                    s["rush_tds"] += 1

            # Receiving
            if play.receiver_id:
                s = get_stats(play.receiver_id)
                s["targets"] += 1
                if play.yards_gained > 0 or "complete" in play.description.lower():
                    s["receptions"] += 1
                    s["rec_yards"] += play.yards_gained
                    if play.is_touchdown:
                        s["rec_tds"] += 1

        # 3. Save to DB
        count = 0
        for pid, stats in stats_agg.items():
            team_id = player_team_map.get(pid)
            if not team_id:
                # Fallback: query player if not in match context (shouldn't happen often)
                stmt = select(Player).where(Player.id == pid)
                result = await self.db_session.execute(stmt)
                player = result.scalar_one_or_none()
                if player:
                    team_id = player.team_id

            if not team_id:
                continue

            # Check if exists first
            stmt = select(PlayerGameStats).where(
                PlayerGameStats.player_id == pid,
                PlayerGameStats.game_id == game.id
            )
            result = await self.db_session.execute(stmt)
            pgs = result.scalar_one_or_none()

            if not pgs:
                pgs = PlayerGameStats(
                    player_id=pid,
                    game_id=game.id,
                    team_id=team_id,
                    season_id=game.season_id,
                    **stats
                )
                self.db_session.add(pgs)
            else:
                # Update existing
                for k, v in stats.items():
                    setattr(pgs, k, getattr(pgs, k) + v)

            count += 1

        await self.db_session.commit()
        logger.info("Player stats saved", extra={"game_id": game.id, "player_count": count})

    def run_simulation(self) -> PlayResult:
        """
        Sets up and runs a simple simulation of a single pass play.
        (Legacy method for backward compatibility)
        """
        self.is_running = True
        logger.debug("Setting up simulation scenario: Pass Play")

        # For now, we are not using real player objects
        offense_players = []
        defense_players = []

        # 1. Create a play command
        pass_command = PassPlayCommand(
            offense_players=offense_players,
            defense_players=defense_players,
            depth="short"
        )

        # 2. Resolve the play
        logger.debug("Resolving play")
        result = self.play_resolver.resolve_play(pass_command)
        self.history.append(result)

        # Update State
        if result.is_touchdown:
            self.home_score += 7

        # Mock time decrement (simple logic)
        try:
            minutes, seconds = map(int, self.time_left.split(":"))
            total_seconds = minutes * 60 + seconds - 15 # 15 seconds per play
            if total_seconds < 0: total_seconds = 0
            self.time_left = f"{total_seconds // 60:02d}:{total_seconds % 60:02d}"
        except ValueError:
            self.time_left = "14:45"

        logger.debug("Play resolved")

        self._save_progress()

        return result

    async def run_continuous_simulation(self, num_plays: int = 100, config: Optional[dict] = None) -> None:
        """
        Run a continuous simulation for a specified number of plays.
        Broadcasts each play result via WebSocket.

        Args:
            num_plays: Number of plays to simulate (default: full quarter ~15-20 plays)
            config: Optional configuration dictionary for the simulation
        """
        self.is_running = True
        self.reset_game_state()

        # Start DB session if not already started
        if not self.current_game_id:
            # This requires db_session to be set previously or passed here?
            # run_continuous_simulation signature doesn't take db_session.
            # We assume self.db_session is set or we can't start.
            if not self.db_session:
                 # Try to get one? No, we are async.
                 logger.error("No DB session available for continuous simulation")
                 return
            await self.start_new_game_session(home_team_id=1, away_team_id=2, config=config, db_session=self.db_session)

        logger.info("Starting continuous simulation", extra={"num_plays": num_plays})

        for play_num in range(num_plays):
            if not self.is_running:
                logger.info("Simulation stopped by user")
                break

            # Execute single play
            result = await self._execute_single_play()

            # Broadcast play result
            if self.on_play_complete:
                await self.on_play_complete(result)

            # Broadcast game state update
            if self.on_game_update:
                await self.on_game_update(self.get_game_state())

            # Add delay for frontend animation
            await asyncio.sleep(self.play_delay_seconds)

            # Check if quarter/game is over
            if self._is_quarter_over():
                logger.info("Quarter complete", extra={"quarter": self.current_quarter})
                break

        self.is_running = False
        await self.save_game_result()
        logger.info("Simulation complete")

    async def _execute_single_play(self) -> PlayResult:
        """Execute a single play and update game state."""

        # Get Real Players from MatchContext if available
        offense_players = []
        defense_players = []

        if self.match_context:
            off_team_id = self.match_context.home_team_id if self.possession == "home" else self.match_context.away_team_id
            def_team_id = self.match_context.away_team_id if self.possession == "home" else self.match_context.home_team_id

            # Use default formations for now as PlayCaller hasn't run yet
            offense_players = self.match_context.get_fielded_players(off_team_id, "standard", "OFFENSE")
            defense_players = self.match_context.get_fielded_players(def_team_id, "4-3", "DEFENSE")

        # Build PlayCallingContext
        try:
            minutes, seconds = map(int, self.time_left.split(":"))
            time_left_seconds = minutes * 60 + seconds
        except ValueError:
            time_left_seconds = 900 # 15 mins

        if self.possession == "home":
            distance_to_goal = 100 - self.yard_line
            score_diff = self.home_score - self.away_score
            aggression = self.game_config.get("home_aggression", 0.5)
        else:
            distance_to_goal = self.yard_line
            score_diff = self.away_score - self.home_score
            aggression = self.game_config.get("away_aggression", 0.5)

        context = PlayCallingContext(
            down=self.down,
            distance=self.distance,
            distance_to_goal=distance_to_goal,
            time_left_seconds=time_left_seconds,
            score_diff=score_diff,
            offense_players=offense_players,
            defense_players=defense_players,
            possession=self.possession
        )

        # Update Coach Personality
        self.play_caller.aggression = float(aggression)

        # Select Play
        if self.match_context and hasattr(self.match_context, 'cortex') and self.match_context.cortex:
            # Use Cortex AI
            situation = GameSituation(
                down=self.down,
                distance=self.distance,
                field_position=self.yard_line if self.possession == "home" else 100 - self.yard_line,
                time_remaining=time_left_seconds,
                score_differential=score_diff,
                quarter=self.current_quarter,
                timeouts_left=3 # Placeholder
            )

            coach_philosophy = {
                "aggressiveness": int(aggression * 100),
                "pass_tendency": 50 # Default, could be loaded from Coach model
            }

            play_decision = self.match_context.cortex.call_play(situation, coach_philosophy)
            command = self._convert_decision_to_command(play_decision, context)
            logger.debug(
                "Cortex AI decision",
                extra={"decision": play_decision, "down": self.down, "distance": self.distance},
            )
        else:
            # Legacy PlayCaller
            command = self.play_caller.select_play(context)

        # Resolve play
        result = self.play_resolver.resolve_play(command)
        self.history.append(result)

        # Update game state based on result
        await self._update_game_state(result)

        # Update Fatigue in MatchContext
        if self.match_context:
            self._update_fatigue(offense_players, defense_players, result)

        return result

    def _convert_decision_to_command(self, decision: str, context: PlayCallingContext) -> Any:
        """Convert Cortex decision string to PlayCommand."""
        if decision == "PUNT":
            from app.orchestrator.play_commands import PuntCommand
            return PuntCommand(punting_team=context.offense_players, receiving_team=context.defense_players)

        elif decision == "FG":
            from app.orchestrator.play_commands import FieldGoalCommand
            return FieldGoalCommand(kicking_team=context.offense_players, defense=context.defense_players, distance=context.distance_to_goal + 17)

        elif decision == "HAIL_MARY":
            return PassPlayCommand(offense_players=context.offense_players, defense_players=context.defense_players, depth="deep")

        elif decision.startswith("PASS"):
            depth = "deep" if "DEEP" in decision else "short"
            # Randomly mix in "mid" for variety if "short" is selected
            if depth == "short" and self.rng.random() < 0.3:
                depth = "mid"
            return PassPlayCommand(offense_players=context.offense_players, defense_players=context.defense_players, depth=depth)

        elif decision == "RUN":
            # Random direction for now
            direction = self.rng.choice(["left", "middle", "right"])
            return RunPlayCommand(offense_players=context.offense_players, defense_players=context.defense_players, run_direction=direction)

        else:
            # Fallback
            return RunPlayCommand(offense_players=context.offense_players, defense_players=context.defense_players, run_direction="middle")



    def _update_fatigue(self, offense: List[Player], defense: List[Player], result: PlayResult) -> None:
        """Update fatigue for players involved in the play."""
        if not self.match_context:
            return

        temp = self.match_context.weather_config.get("temperature", 70)

        # Identify key players who exerted more energy
        key_players = set()
        if result.passer_id: key_players.add(result.passer_id)
        if result.rusher_id: key_players.add(result.rusher_id)
        if result.receiver_id: key_players.add(result.receiver_id)

        # Update Offense
        offense_ids = [p.id for p in offense]
        # Key players exert more energy
        key_ids = [pid for pid in offense_ids if pid in key_players]
        other_ids = [pid for pid in offense_ids if pid not in key_players]

        self.match_context.update_fatigue(key_ids, 0.05) # High exertion
        self.match_context.update_fatigue(other_ids, 0.01) # Low exertion

        # Update Defense
        defense_ids = [p.id for p in defense]
        self.match_context.update_fatigue(defense_ids, 0.02) # Medium exertion

    async def _update_game_state(self, result: PlayResult) -> None:
        """Update game state based on play result."""
        # Update yard line
        if self.possession == "home":
            self.yard_line += result.yards_gained
        else:
            self.yard_line -= result.yards_gained

        # Bounds check
        self.yard_line = max(0, min(100, self.yard_line))

        # Update Player Stats (in-memory aggregation removed, using _save_player_stats at end)
        # self._update_player_stats(result)

        # Check for touchdown
        if result.is_touchdown or self.yard_line >= 100 or self.yard_line <= 0:
            if self.possession == "home":
                self.home_score += 7
            else:
                self.away_score += 7

            # Reset to kickoff
            self.yard_line = 25
            self.down = 1
            self.distance = 10
            self.possession = "away" if self.possession == "home" else "home"

        # Check for turnover
        elif result.is_turnover:
            self.possession = "away" if self.possession == "home" else "home"
            self.yard_line = 100 - self.yard_line
            self.down = 1
            self.distance = 10

        # Normal down progression
        else:
            if result.yards_gained >= self.distance:
                # First down!
                self.down = 1
                self.distance = 10
            else:
                self.down += 1
                self.distance -= result.yards_gained

                # Turnover on downs
                if self.down > 4:
                    self.possession = "away" if self.possession == "home" else "home"
                    self.yard_line = 100 - self.yard_line
                    self.down = 1
                    self.distance = 10

        # Update time
        try:
            minutes, seconds = map(int, self.time_left.split(":"))
            total_seconds = minutes * 60 + seconds - result.time_elapsed
            if total_seconds < 0:
                total_seconds = 0
            self.time_left = f"{int(total_seconds // 60):02d}:{int(total_seconds % 60):02d}"
        except (ValueError, AttributeError):
            pass

        # Persist state
        await self._save_progress()

    def _is_quarter_over(self) -> bool:
        """Check if the current quarter is over."""
        try:
            minutes, seconds = map(int, self.time_left.split(":"))
            return minutes == 0 and seconds == 0
        except ValueError:
            return False

    def reset_game_state(self) -> None:
        """Reset game state to initial values."""
        self.current_quarter = 1
        self.time_left = "15:00"
        self.home_score = 0
        self.away_score = 0
        self.possession = "home"
        self.down = 1
        self.distance = 10
        self.yard_line = 25
        self.history = []
        # self.player_stats = {} # Reset stats

    def get_game_state(self) -> dict:
        """Get current game state as a dictionary for broadcasting."""
        return {
            "homeScore": self.home_score,
            "awayScore": self.away_score,
            "quarter": self.current_quarter,
            "timeLeft": self.time_left,
            "possession": self.possession,
            "down": self.down,
            "distance": self.distance,
            "yardLine": self.yard_line
        }

    def get_history(self) -> List[PlayResult]:
        """Return the history of plays in this session."""
        return self.history

    def stop_simulation(self) -> None:
        """Stop the currently running simulation."""
        self.is_running = False

from .play_resolver import PlayResolver
from .play_commands import PassPlayCommand, RunPlayCommand
from .play_caller import PlayCaller, PlayCallingContext
from app.schemas.play import PlayResult
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.models.player import Player
from app.orchestrator.match_context import MatchContext
from app.orchestrator.kernels.cortex_kernel import GameSituation
import random

from typing import List, Optional, Callable, Awaitable, Any
import asyncio
import datetime

class SimulationOrchestrator:
    """
    Orchestrates the setup and execution of a simulation.
    """
    def __init__(self) -> None:
        self.play_resolver = PlayResolver()
        self.play_caller = PlayCaller(aggression=0.5) # Default balanced coach
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
        self.db_session = None
        self.current_game_id = None

        # Match Context (Data Hydration)
        self.match_context: Optional[MatchContext] = None

        # Callbacks for WebSocket broadcasting
        self.on_play_complete: Optional[Callable[[PlayResult], Awaitable[None]]] = None
        self.on_game_update: Optional[Callable[[dict], Awaitable[None]]] = None

        # Configuration
        self.play_delay_seconds = 5.0  # Delay between plays for animation
        self.game_config = {}

    def start_new_game_session(self, home_team_id: int, away_team_id: int, config: Optional[dict] = None) -> None:
        """Initialize a new game session in the database."""
        self.game_config = config or {}
        self.db_session = SessionLocal()
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
        self.db_session.commit()
        self.db_session.refresh(new_game)
        self.current_game_id = new_game.id

        # Hydrate Match Context
        print(f"Hydrating Match Context for Game {new_game.id}...")

        # Initialize MatchContext with rosters and weather config
        weather_config = self.game_config.get("weather", {"temperature": 70, "condition": "Sunny"})

        # Create MatchContext instance with home/away teams
        # MatchContext handles roster loading internally
        self.match_context = MatchContext(home_team_id, away_team_id, self.db_session, weather_config=weather_config)

        # Register players with Kernels (Now handled inside MatchContext init, but PlayResolver needs reference)
        self.play_resolver.register_players(self.match_context)

        print(f"Match Context Hydrated. Home: {len(self.match_context.home_roster)} players, Away: {len(self.match_context.away_roster)} players.")

    def _save_progress(self) -> None:
        """Save current game state and history to database."""
        if not self.db_session or not self.current_game_id:
            return

        try:
            game = self.db_session.query(Game).filter(Game.id == self.current_game_id).first()
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

                self.db_session.commit()
        except Exception as e:
            print(f"Error saving progress: {e}")
            self.db_session.rollback()

    def save_game_result(self) -> None:
        """Finalize the game in the database."""
        if not self.db_session or not self.current_game_id:
            return

        try:
            game = self.db_session.query(Game).filter(Game.id == self.current_game_id).first()
            if game:
                game.is_played = True
                # Save player stats
                self._save_player_stats()
                self._save_progress() # Ensure final state is saved

                print(f"Finalized game result for Game ID {self.current_game_id}")
        except Exception as e:
            print(f"Error finalizing game: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup Match Context
            self.match_context = None

            if self.db_session:
                self.db_session.close()
                self.db_session = None
            self.current_game_id = None

    def _save_player_stats(self, game: Game = None) -> None:
        """Aggregate and save player stats from game history."""
        if not self.history:
            return

        # If game object not passed, fetch it
        if not game and self.current_game_id:
             game = self.db_session.query(Game).filter(Game.id == self.current_game_id).first()

        if not game: return

        print(f"Saving player stats for Game {game.id}...")

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
                player = self.db_session.query(Player).filter(Player.id == pid).first()
                if player:
                    team_id = player.team_id

            if not team_id:
                continue

            # Check if exists first
            pgs = self.db_session.query(PlayerGameStats).filter(
                PlayerGameStats.player_id == pid,
                PlayerGameStats.game_id == game.id
            ).first()

            if not pgs:
                pgs = PlayerGameStats(
                    player_id=pid,
                    game_id=game.id,
                    team_id=team_id,
                    **stats
                )
                self.db_session.add(pgs)
            else:
                # Update existing
                for k, v in stats.items():
                    setattr(pgs, k, getattr(pgs, k) + v)

            count += 1

        self.db_session.commit()
        print(f"Saved stats for {count} players.")

    def run_simulation(self) -> PlayResult:
        """
        Sets up and runs a simple simulation of a single pass play.
        (Legacy method for backward compatibility)
        """
        self.is_running = True
        print("Setting up simulation scenario: Pass Play")

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
        print("Resolving play...")
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

        print("Play resolved.")

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
            self.start_new_game_session(home_team_id=1, away_team_id=2, config=config)

        print(f"Starting continuous simulation for {num_plays} plays...")

        for play_num in range(num_plays):
            if not self.is_running:
                print("Simulation stopped by user")
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
                print(f"Quarter {self.current_quarter} complete")
                break

        self.is_running = False
        self.save_game_result()
        print("Simulation complete")

    async def _execute_single_play(self) -> PlayResult:
        """Execute a single play and update game state."""

        # Get Real Players from MatchContext if available
        offense_players = []
        defense_players = []

        if self.match_context:
            off_side = "home" if self.possession == "home" else "away"
            def_side = "away" if self.possession == "home" else "home"

            # Use default formations for now as PlayCaller hasn't run yet
            offense_players = self.match_context.get_fielded_players(off_side, "standard")
            defense_players = self.match_context.get_fielded_players(def_side, "4-3")

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
        if self.match_context and self.match_context.cortex:
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
            print(f"DEBUG: Cortex AI Decision: {play_decision} (Down: {self.down}, Dist: {self.distance})")
        else:
            # Legacy PlayCaller
            command = self.play_caller.select_play(context)

        # Resolve play
        result = self.play_resolver.resolve_play(command)
        self.history.append(result)

        # Update game state based on result
        self._update_game_state(result)

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
            if depth == "short" and random.random() < 0.3:
                depth = "mid"
            return PassPlayCommand(offense_players=context.offense_players, defense_players=context.defense_players, depth=depth)

        elif decision == "RUN":
            # Random direction for now
            direction = random.choice(["left", "middle", "right"])
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
        for p in offense:
            regulator = self.match_context.get_fatigue(p.id)
            if regulator:
                exertion = 1.0 if p.id in key_players else 0.3
                regulator.update_fatigue(exertion, temp)

        # Update Defense
        for p in defense:
            regulator = self.match_context.get_fatigue(p.id)
            if regulator:
                exertion = 0.4 # Defenders generally react
                regulator.update_fatigue(exertion, temp)

    def _update_game_state(self, result: PlayResult) -> None:
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
        self._save_progress()

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

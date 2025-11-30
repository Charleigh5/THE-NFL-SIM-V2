from .play_resolver import PlayResolver
from .play_commands import PassPlayCommand, RunPlayCommand
from .play_caller import PlayCaller, PlayCallingContext
from app.schemas.play import PlayResult
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.stats import PlayerGameStats
from app.models.player import Player
from app.orchestrator.match_context import MatchContext

from typing import List, Optional, Callable, Awaitable
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
            date=datetime.datetime.utcnow(),
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
        home_roster = self.db_session.query(Player).filter(Player.team_id == home_team_id).all()
        away_roster = self.db_session.query(Player).filter(Player.team_id == away_team_id).all()
        self.match_context = MatchContext(home_roster, away_roster)
        
        # Register players with Kernels
        self.play_resolver.register_players(self.match_context)
        
        print(f"Match Context Hydrated. Home: {len(home_roster)} players, Away: {len(away_roster)} players.")

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
                current_data["plays"] = [p.dict() for p in self.history]
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
            if self.db_session:
                self.db_session.close()
                self.db_session = None
            self.current_game_id = None

    def _save_player_stats(self, game: Game) -> None:
        """Aggregate and save player stats from game history."""
        if not self.history:
            return

        print(f"Saving player stats for Game {game.id}...")
        
        # 1. Map player IDs to Team IDs
        player_team_map = {}
        if self.match_context:
            for p in self.match_context.home_roster:
                player_team_map[p.id] = game.home_team_id
            for p in self.match_context.away_roster:
                player_team_map[p.id] = game.away_team_id
        
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

            # Create PlayerGameStats record
            pgs = PlayerGameStats(
                player_id=pid,
                game_id=game.id,
                team_id=team_id,
                **stats
            )
            self.db_session.add(pgs)
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
            
            off_starters = self.match_context.get_starters(off_side)
            def_starters = self.match_context.get_starters(def_side)
            
            # Pass the dict values for now. 
            offense_players = list(off_starters.values())
            defense_players = list(def_starters.values())
        
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
        command = self.play_caller.select_play(context)
        
        # Resolve play
        result = self.play_resolver.resolve_play(command)
        self.history.append(result)
        
        # Update game state based on result
        self._update_game_state(result)
        
        return result

    def _update_game_state(self, result: PlayResult) -> None:
        """Update game state based on play result."""
        # Update yard line
        if self.possession == "home":
            self.yard_line += result.yards_gained
        else:
            self.yard_line -= result.yards_gained
        
        # Bounds check
        self.yard_line = max(0, min(100, self.yard_line))
        
        # Update Player Stats
        self._update_player_stats(result)
        
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
    
    def _update_player_stats(self, result: PlayResult) -> None:
        """Aggregate stats from the play result."""
        if not hasattr(self, "player_stats"):
            self.player_stats = {} # player_id -> dict of stats

        def get_stat_entry(player_id):
            if player_id not in self.player_stats:
                self.player_stats[player_id] = {
                    "pass_attempts": 0, "pass_completions": 0, "pass_yards": 0, "pass_tds": 0,
                    "rush_attempts": 0, "rush_yards": 0, "rush_tds": 0,
                    "targets": 0, "receptions": 0, "rec_yards": 0, "rec_tds": 0
                }
            return self.player_stats[player_id]

        # Passing
        if result.passer_id:
            stats = get_stat_entry(result.passer_id)
            stats["pass_attempts"] += 1
            if result.yards_gained > 0 or result.is_touchdown: # Simplified completion check
                stats["pass_completions"] += 1
                stats["pass_yards"] += result.yards_gained
                if result.is_touchdown:
                    stats["pass_tds"] += 1

        # Receiving
        if result.receiver_id:
            stats = get_stat_entry(result.receiver_id)
            stats["targets"] += 1
            if result.yards_gained > 0 or result.is_touchdown:
                stats["receptions"] += 1
                stats["rec_yards"] += result.yards_gained
                if result.is_touchdown:
                    stats["rec_tds"] += 1

        # Rushing
        if result.rusher_id:
            stats = get_stat_entry(result.rusher_id)
            stats["rush_attempts"] += 1
            stats["rush_yards"] += result.yards_gained
            if result.is_touchdown:
                stats["rush_tds"] += 1

    def _save_player_stats(self) -> None:
        """Save aggregated player stats to database."""
        if not self.db_session or not self.current_game_id or not hasattr(self, "player_stats"):
            return
            
        try:
            # Get team IDs for players (needed for PlayerGameStats)
            player_ids = list(self.player_stats.keys())
            players = self.db_session.query(Player).filter(Player.id.in_(player_ids)).all()
            player_team_map = {p.id: p.team_id for p in players}

            for player_id, stats in self.player_stats.items():
                team_id = player_team_map.get(player_id)
                if not team_id: continue

                # Check if stat record exists
                pgs = self.db_session.query(PlayerGameStats).filter(
                    PlayerGameStats.player_id == player_id,
                    PlayerGameStats.game_id == self.current_game_id
                ).first()

                if not pgs:
                    pgs = PlayerGameStats(
                        player_id=player_id,
                        game_id=self.current_game_id,
                        team_id=team_id
                    )
                    self.db_session.add(pgs)
                
                # Update stats
                pgs.pass_attempts += stats["pass_attempts"]
                pgs.pass_completions += stats["pass_completions"]
                pgs.pass_yards += stats["pass_yards"]
                pgs.pass_tds += stats["pass_tds"]
                
                pgs.rush_attempts += stats["rush_attempts"]
                pgs.rush_yards += stats["rush_yards"]
                pgs.rush_tds += stats["rush_tds"]
                
                pgs.targets += stats["targets"]
                pgs.receptions += stats["receptions"]
                pgs.rec_yards += stats["rec_yards"]
                pgs.rec_tds += stats["rec_tds"]

            self.db_session.commit()
            print(f"Saved stats for {len(self.player_stats)} players.")
            
        except Exception as e:
            print(f"Error saving player stats: {e}")
            self.db_session.rollback()

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
        self.player_stats = {} # Reset stats
    
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

from .play_resolver import PlayResolver
from .play_commands import PassPlayCommand, RunPlayCommand
from app.schemas.play import PlayResult
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.stats import PlayerGameStats

from typing import List, Optional, Callable, Awaitable
import asyncio
import datetime

class SimulationOrchestrator:
    """
    Orchestrates the setup and execution of a simulation.
    """
    def __init__(self):
        self.play_resolver = PlayResolver()
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
        
        # Callbacks for WebSocket broadcasting
        self.on_play_complete: Optional[Callable[[PlayResult], Awaitable[None]]] = None
        self.on_game_update: Optional[Callable[[dict], Awaitable[None]]] = None
        
        # Configuration
        self.play_delay_seconds = 5.0  # Delay between plays for animation

    def start_new_game_session(self, home_team_id: int, away_team_id: int, config: Optional[dict] = None):
        """Initialize a new game session in the database."""
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
        print(f"Started new game session: ID {self.current_game_id}")

    def _save_progress(self):
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

    def save_game_result(self):
        """Finalize the game in the database."""
        if not self.db_session or not self.current_game_id:
            return

        try:
            game = self.db_session.query(Game).filter(Game.id == self.current_game_id).first()
            if game:
                game.is_played = True
                self._save_progress() # Ensure final state is saved
                print(f"Finalized game result for Game ID {self.current_game_id}")
        except Exception as e:
            print(f"Error finalizing game: {e}")
        finally:
            if self.db_session:
                self.db_session.close()
                self.db_session = None
            self.current_game_id = None

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
    
    async def run_continuous_simulation(self, num_plays: int = 100, config: Optional[dict] = None):
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
        import random
        
        # Simple play calling logic (alternates pass/run)
        offense_players = []
        defense_players = []
        
        if random.random() < 0.6:  # 60% pass, 40% run
            command = PassPlayCommand(
                offense_players=offense_players,
                defense_players=defense_players,
                depth=random.choice(["short", "mid", "deep"])
            )
        else:
            command = RunPlayCommand(
                offense_players=offense_players,
                defense_players=defense_players,
                run_direction=random.choice(["left", "middle", "right"])
            )
        
        # Resolve play
        result = self.play_resolver.resolve_play(command)
        self.history.append(result)
        
        # Update game state based on result
        self._update_game_state(result)
        
        return result

    def _update_game_state(self, result: PlayResult):
        """Update game state based on play result."""
        # Update yard line
        if self.possession == "home":
            self.yard_line += result.yards_gained
        else:
            self.yard_line -= result.yards_gained
        
        # Bounds check
        self.yard_line = max(0, min(100, self.yard_line))
        
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
    
    def reset_game_state(self):
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

    def stop_simulation(self):
        """Stop the currently running simulation."""
        self.is_running = False

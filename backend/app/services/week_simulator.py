"""
Batch simulation service for simulating entire weeks of games.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.game import Game
from app.models.season import Season
from app.orchestrator.simulation_orchestrator import SimulationOrchestrator
from app.schemas.play import PlayResult
import asyncio


class WeekSimulator:
    """
    Simulates all games in a week using the SimulationOrchestrator.
    
    This allows for fast-forwarding through a season by automatically
    simulating multiple games without requiring WebSocket connections.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def simulate_week(
        self,
        season_id: int,
        week: int,
        play_count: int = 100,
        use_fast_sim: bool = True
    ) -> Dict[int, Dict]:
        """
        Simulate all games in a specific week.
        
        Args:
            season_id: ID of the season
            week: Week number to simulate
            play_count: Number of plays per game (default: 100)
            use_fast_sim: If True, skips delays for faster simulation
        
        Returns:
            Dictionary mapping game IDs to game results
        """
        # Get all games for this week
        games = self.db.query(Game).filter(
            Game.season_id == season_id,
            Game.week == week,
            Game.is_played == False
        ).all()
        
        if not games:
            return {"error": "No unplayed games found for this week"}
        
        results = {}
        
        for game in games:
            print(f"Simulating Game {game.id}: Team {game.home_team_id} vs Team {game.away_team_id}")
            
            # Create orchestrator for this game
            orchestrator = SimulationOrchestrator()
            
            if use_fast_sim:
                orchestrator.play_delay_seconds = 0.0  # No delays in fast sim
            
            # Start game session (this will create/update db entry)
            orchestrator.start_new_game_session(
                home_team_id=game.home_team_id,
                away_team_id=game.away_team_id,
                config={"fast_sim": use_fast_sim}
            )
            
            # Run simulation asynchronously
            await self._run_simulation(orchestrator, play_count)
            
            # Update the original game record with the results
            game.is_played = True
            game.home_score = orchestrator.home_score
            game.away_score = orchestrator.away_score
            game.game_data = {
                "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",
                "plays": len(orchestrator.history),
                "quarters": orchestrator.current_quarter
            }
            self.db.commit()
            
            results[game.id] = {
                "home_team_id": game.home_team_id,
                "away_team_id": game.away_team_id,
                "home_score": orchestrator.home_score,
                "away_score": orchestrator.away_score,
                "total_plays": len(orchestrator.history),
                "winner": "home" if orchestrator.home_score > orchestrator.away_score else "away"
            }
            
            print(f"  Result: {orchestrator.home_score}-{orchestrator.away_score}")
        
        return {
            "week": week,
            "games_simulated": len(results),
            "results": results
        }

    async def simulate_game(self, game_id: int, play_count: int = 100, use_fast_sim: bool = True) -> Dict:
        """
        Simulate a single game.
        """
        game = self.db.query(Game).filter(Game.id == game_id).first()
        if not game:
            return {"error": "Game not found"}
            
        if game.is_played:
            return {"error": "Game already played"}
            
        print(f"Simulating Game {game.id}: Team {game.home_team_id} vs Team {game.away_team_id}")
        
        orchestrator = SimulationOrchestrator()
        if use_fast_sim:
            orchestrator.play_delay_seconds = 0.0
            
        orchestrator.start_new_game_session(
            home_team_id=game.home_team_id,
            away_team_id=game.away_team_id,
            config={"fast_sim": use_fast_sim}
        )
        
        await self._run_simulation(orchestrator, play_count)
        
        game.is_played = True
        game.home_score = orchestrator.home_score
        game.away_score = orchestrator.away_score
        game.game_data = {
            "final_score": f"{orchestrator.home_score}-{orchestrator.away_score}",
            "plays": len(orchestrator.history),
            "quarters": orchestrator.current_quarter
        }
        self.db.commit()
        
        return {
            "id": game.id,
            "home_team_id": game.home_team_id,
            "away_team_id": game.away_team_id,
            "home_score": orchestrator.home_score,
            "away_score": orchestrator.away_score,
            "winner": "home" if orchestrator.home_score > orchestrator.away_score else "away"
        }
    
    async def _run_simulation(self, orchestrator: SimulationOrchestrator, num_plays: int) -> None:
        """
        Run the simulation loop for a single game asynchronously.
        
        Executes plays sequentially until the play count is reached or the game ends.
        
        Args:
            orchestrator: The SimulationOrchestrator instance for the game.
            num_plays: Maximum number of plays to simulate.
        """
        orchestrator.is_running = True
        orchestrator.reset_game_state()
        
        for play_num in range(num_plays):
            if not orchestrator.is_running:
                break
            
            # Execute play
            result = await orchestrator._execute_single_play()
            
            # Check if game should end (could add more sophisticated logic here)
            if orchestrator._is_quarter_over():
                # For now, just end after first quarter
                # In future, could simulate all 4 quarters
                break
        
        orchestrator.is_running = False
        orchestrator.save_game_result()
    
    def simulate_full_season(
        self,
        season_id: int,
        start_week: int = 1,
        end_week: Optional[int] = None
    ) -> Dict:
        """
        Simulate multiple weeks at once.
        
        Args:
            season_id: ID of the season
            start_week: Week to start from (default: 1)
            end_week: Week to end at (default: total_weeks in season)
        
        Returns:
            Summary of all simulated weeks
        """
        # Get season info
        season = self.db.query(Season).filter(Season.id == season_id).first()
        if not season:
            return {"error": "Season not found"}
        
        if end_week is None:
            end_week = season.total_weeks
        
        all_results = {}
        
        for week_num in range(start_week, end_week + 1):
            print(f"\n=== SIMULATING WEEK {week_num} ===")
            week_results = self.simulate_week(season_id, week_num)
            all_results[f"week_{week_num}"] = week_results
            
            # Update season's current week
            season.current_week = week_num
            self.db.commit()
        
        return {
            "season_id": season_id,
            "weeks_simulated": list(range(start_week, end_week + 1)),
            "results": all_results
        }

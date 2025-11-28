"""
Play Command Pattern
--------------------
Command pattern implementation for different play types
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.schemas.play import PlayResult





class PlayCommand(ABC):
    """Abstract base class for all play commands"""
    
    def __init__(self, offense_players: List[Any], defense_players: List[Any]):
        self.offense = offense_players
        self.defense = defense_players
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute the play and return result"""
        pass
    
    @abstractmethod
    def get_play_type(self) -> str:
        """Return the type of play"""
        pass


class PassPlayCommand(PlayCommand):
    """Command for passing plays"""
    
    def __init__(self, offense_players: List[Any], defense_players: List[Any], 
                 target_receiver_id: int = None, depth: str = "short"):
        super().__init__(offense_players, defense_players)
        self.target_receiver = target_receiver_id
        self.depth = depth  # short, mid, deep
        
    def get_play_type(self) -> str:
        return f"PASS_{self.depth.upper()}"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """
        Execute a passing play
        This will be called by PlayResolver which integrates all engines
        """
        # Placeholder - actual logic in PlayResolver
        return PlayResult(
            yards_gained=0,
            description=f"Pass play targeting {self.depth} route"
        )


class RunPlayCommand(PlayCommand):
    """Command for running plays"""
    
    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 run_direction: str = "middle"):
        super().__init__(offense_players, defense_players)
        self.run_direction = run_direction  # left, middle, right
        
    def get_play_type(self) -> str:
        return f"RUN_{self.run_direction.upper()}"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute a running play"""
        # Placeholder - actual logic in PlayResolver
        return PlayResult(
            yards_gained=0,
            description=f"Run to the {self.run_direction}"
        )


class KickoffCommand(PlayCommand):
    """Command for kickoffs"""
    
    def __init__(self, kicking_team: List[Any], receiving_team: List[Any]):
        super().__init__(kicking_team, receiving_team)
        
    def get_play_type(self) -> str:
        return "KICKOFF"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute a kickoff"""
        import random
        return_yards = random.randint(15, 30)
        
        return PlayResult(
            yards_gained=return_yards,
            description=f"Kickoff returned to the {return_yards} yard line"
        )


class PuntCommand(PlayCommand):
    """Command for punts"""
    
    def __init__(self, punting_team: List[Any], receiving_team: List[Any]):
        super().__init__(punting_team, receiving_team)
        
    def get_play_type(self) -> str:
        return "PUNT"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute a punt"""
        import random
        punt_distance = random.randint(35, 55)
        return_yards = random.randint(0, 15)
        
        net_yards = -(punt_distance - return_yards)
        
        return PlayResult(
            yards_gained=net_yards,
            description=f"Punt {punt_distance} yards, returned {return_yards} yards"
        )


class FieldGoalCommand(PlayCommand):
    """Command for field goal attempts"""
    
    def __init__(self, kicking_team: List[Any], defense: List[Any], distance: int):
        super().__init__(kicking_team, defense)
        self.distance = distance
        
    def get_play_type(self) -> str:
        return "FIELD_GOAL"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute a field goal attempt"""
        import random
        
        # Simple success calculation based on distance
        base_success = max(0, 100 - (self.distance - 20) * 2)
        is_good = random.randint(0, 100) < base_success
        
        if is_good:
            return PlayResult(
                yards_gained=0,
                description=f"{self.distance}-yard field goal GOOD!",
                is_highlight_worthy=self.distance > 50
            )
        else:
            return PlayResult(
                yards_gained=0,
                is_turnover=True,
                description=f"{self.distance}-yard field goal NO GOOD"
            )


class ExtraPointCommand(PlayCommand):
    """Command for extra point attempts"""
    
    def get_play_type(self) -> str:
        return "EXTRA_POINT"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute an extra point attempt"""
        import random
        is_good = random.randint(0, 100) < 95  # 95% success rate
        
        return PlayResult(
            yards_gained=0,
            description="Extra point " + ("GOOD!" if is_good else "NO GOOD")
        )


class TwoPointConversionCommand(PlayCommand):
    """Command for 2-point conversion attempts"""
    
    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 play_type: str = "pass"):
        super().__init__(offense_players, defense_players)
        self.play_type = play_type  # pass or run
        
    def get_play_type(self) -> str:
        return f"TWO_POINT_{self.play_type.upper()}"
    
    def execute(self, context: Dict[str, Any]) -> PlayResult:
        """Execute a 2-point conversion attempt"""
        import random
        is_successful = random.randint(0, 100) < 45  # ~45% success rate
        
        return PlayResult(
            yards_gained=0,
            is_touchdown=is_successful,
            description=f"2-point conversion attempt ({self.play_type}) " + 
                       ("SUCCESSFUL!" if is_successful else "FAILED")
        )

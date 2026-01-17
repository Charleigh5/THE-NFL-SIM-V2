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

    def __init__(self, offense_players: List[Any], defense_players: List[Any], modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, is_home_team: bool = True, possession: str = "home", start_yard_line: int = 20):
        self.offense = offense_players
        self.defense = defense_players
        self.modifiers = modifiers or {}
        self.play_id = play_id
        self.distance = distance
        self.down = down
        self.yard_line = yard_line
        self.is_home_team = is_home_team
        self.possession = possession
        self.start_yard_line = start_yard_line

    @abstractmethod
    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """Execute the play and return result"""
        pass

    @abstractmethod
    def get_play_type(self) -> str:
        """Return the type of play"""
        pass


class PassPlayCommand(PlayCommand):
    """Command for passing plays"""

    def __init__(self, offense_players: List[Any], defense_players: List[Any],
                 target_receiver_id: Optional[int] = None, depth: str = "short", modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, is_home_team: bool = True, possession: str = "home", start_yard_line: int = 20):
        super().__init__(offense_players, defense_players, modifiers, play_id, distance, down, yard_line, is_home_team, possession, start_yard_line)
        self.target_receiver = target_receiver_id
        self.depth = depth  # short, mid, deep

    def get_play_type(self) -> str:
        return f"PASS_{self.depth.upper()}"

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
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
                 run_direction: str = "middle", modifiers: Optional[Dict[str, Any]] = None, play_id: Optional[str] = None,
                 distance: int = 10, down: int = 1, yard_line: int = 20, is_home_team: bool = True, possession: str = "home", start_yard_line: int = 20):
        super().__init__(offense_players, defense_players, modifiers, play_id, distance, down, yard_line, is_home_team, possession, start_yard_line)
        self.run_direction = run_direction  # left, middle, right

    def get_play_type(self) -> str:
        return f"RUN_{self.run_direction.upper()}"

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
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

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """Execute a kickoff"""
        base_yards = rng.randint(15, 30)

        # Weather impact
        weather = context.get("weather", {})
        if weather:
             # Wind affects kick distance (and thus return starting point)
             # Higher wind speed could lead to shorter kicks (better returns) or touchbacks
             wind_speed = weather.get("wind_speed", 0)
             if wind_speed > 15:
                 # High wind: variability increased
                 base_yards += rng.randint(-5, 5)

        return PlayResult(
            yards_gained=base_yards,
            description=f"Kickoff returned to the {base_yards} yard line"
        )


class PuntCommand(PlayCommand):
    """Command for punts"""

    def __init__(self, punting_team: List[Any], receiving_team: List[Any]):
        super().__init__(punting_team, receiving_team)

    def get_play_type(self) -> str:
        return "PUNT"

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """Execute a punt"""
        punt_distance = rng.randint(35, 55)
        return_yards = rng.randint(0, 15)

        # Weather impact
        weather = context.get("weather", {})
        if weather:
             wind_speed = weather.get("wind_speed", 0)
             temp = weather.get("temperature", 75)

             # Wind affects punt distance
             if wind_speed > 10:
                 punt_distance -= int((wind_speed - 10) * 0.5)

             # Cold air reduces distance
             if temp < 40:
                 punt_distance -= int((40 - temp) * 0.2)

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

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """Execute a field goal attempt"""

        # Simple success calculation based on distance
        base_success = max(0, 100 - (self.distance - 20) * 2)

        # Weather impact
        weather = context.get("weather", {})
        weather_desc = ""
        if weather:
             wind_speed = weather.get("wind_speed", 0)
             temp = weather.get("temperature", 75)
             precip = weather.get("precipitation_type", "None")

             # Wind penalty
             if wind_speed > 10:
                 penalty = (wind_speed - 10) * 1.5
                 base_success -= penalty
                 if penalty > 10: weather_desc = " battling strong winds"

             # Cold penalty
             if temp < 32:
                 base_success -= 5

             # Precip penalty
             if precip in ["Rain", "Snow"]:
                 base_success -= 5

        is_good = rng.randint(0, 100) < base_success

        if is_good:
            return PlayResult(
                yards_gained=0,
                description=f"{self.distance}-yard field goal GOOD!{weather_desc}",
                is_highlight_worthy=self.distance > 50
            )
        else:
            return PlayResult(
                yards_gained=0,
                is_turnover=True,
                description=f"{self.distance}-yard field goal NO GOOD{weather_desc}"
            )


class ExtraPointCommand(PlayCommand):
    """Command for extra point attempts"""

    def get_play_type(self) -> str:
        return "EXTRA_POINT"

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """Execute an extra point attempt"""
        is_good = rng.randint(0, 100) < 95  # 95% success rate

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
        self.executed_command: Optional[PlayCommand] = None

    def get_play_type(self) -> str:
        return f"TWO_POINT_{self.play_type.upper()}"

    def execute(self, context: Dict[str, Any], rng: Any = None) -> PlayResult:
        """
        Execute a 2-point conversion attempt.

        NOTE: This class primarily serves as a wrapper/tag for the orchestrator.
        The actual execution happens by resolving the specific Pass/Run command
        contained within, but applied to the 2-point context (short field).

        If executed directly without a sub-command, it defaults to failure (safe fallback).
        """
        if self.executed_command:
            result = self.executed_command.execute(context, rng)
            # Override checking for 2-point success criteria if needed,
            # but usually PlayResolver handles the rules.
            return result

        # Fallback if no command attached
        return PlayResult(
            yards_gained=0,
            is_touchdown=False,
            description="2-point conversion failed (No Play Selected)"
        )

"""
Game State Manager.

Manages mutable game state: clock, score, possession, downs.
Extracted from SimulationOrchestrator for single responsibility.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class GameStateManager:
    """
    Manages mutable game state during simulation.

    Extracted from SimulationOrchestrator to:
    - Enable isolated unit testing
    - Separate state management from orchestration logic
    - Improve debugging by localizing state mutations
    """

    # Clock State
    quarter: int = 1
    time_left: str = "15:00"  # MM:SS format

    # Score
    home_score: int = 0
    away_score: int = 0

    # Possession State
    possession: str = "home"  # "home" or "away"
    down: int = 1
    distance: int = 10
    yard_line: int = 25  # 0-100, where 50 is midfield

    # Timeouts
    home_timeouts: int = 3
    away_timeouts: int = 3

    # Clock Strategy (from Coaching AI)
    last_clock_strategy: str = "NORMAL"

    # Overtime State (GAME-011)
    ot_possessions: int = 0
    first_possession_score_type: Optional[str] = None  # "FG", "TD", or None

    @property
    def time_left_seconds(self) -> int:
        """Convert time_left to seconds."""
        try:
            minutes, seconds = map(int, self.time_left.split(":"))
            return minutes * 60 + seconds
        except ValueError:
            return 900  # 15 minutes default

    def update_clock(self, seconds_elapsed: float) -> None:
        """Decrement the game clock by the specified seconds."""
        total_seconds = self.time_left_seconds - int(seconds_elapsed)
        total_seconds = max(0, total_seconds)
        self.time_left = f"{total_seconds // 60:02d}:{total_seconds % 60:02d}"

    def advance_quarter(self) -> None:
        """Move to the next quarter and reset clock."""
        self.quarter += 1

        if self.quarter == 5:
            self.time_left = "10:00"  # OT is 10 mins
            self.ot_possessions = 0
            self.first_possession_score_type = None
        else:
            self.time_left = "15:00"

        logger.info(f"Advanced to quarter {self.quarter}")

    def update_score(self, team: str, points: int) -> None:
        """Add points to a team's score."""
        if team == "home":
            self.home_score += points
        elif team == "away":
            self.away_score += points
        else:
            logger.warning(f"Unknown team: {team}")

        # Track score type for OT rules
        if self.quarter >= 5:
            # We assume update_score is called immediately after the scoring play
            # This requires coordination with the caller to know if it was FG or TD
            # For now, we'll infer or let the caller set first_possession_score_type explicitly
            pass

    def update_yard_line(self, yards_gained: int) -> None:
        """
        Update yard line based on yards gained and possession.

        Home team drives from 0 to 100.
        Away team drives from 100 to 0.
        """
        if self.possession == "home":
            self.yard_line += yards_gained
        else:
            self.yard_line -= yards_gained

        # Clamp to valid range
        self.yard_line = max(0, min(100, self.yard_line))

    def update_downs(self, yards_gained: int, first_down_threshold: int = 10) -> bool:
        """
        Update down and distance after a play.

        Returns:
            True if first down achieved, False otherwise.
        """
        self.distance -= yards_gained

        if self.distance <= 0:
            # First down!
            self.down = 1
            self.distance = 10
            return True
        else:
            self.down += 1
            return False

    def handle_turnover(self) -> None:
        """Switch possession after a turnover."""
        self.possession = "away" if self.possession == "home" else "home"
        self.down = 1
        self.distance = 10
        if self.quarter >= 5:
            self.ot_possessions += 1

    def handle_touchdown(self) -> None:
        """Handle touchdown scoring and reset field position."""
        self.update_score(self.possession, 7)  # TD + PAT assumed
        self.yard_line = 25  # Kickoff touchback position
        self.down = 1
        self.distance = 10
        # Possession changes after kickoff (simplified)
        self.possession = "away" if self.possession == "home" else "home"

        if self.quarter >= 5:
             # In OT, a TD usually ends the game, but we track possession changes just in case logic flows
             pass

    def use_timeout(self, team: str) -> bool:
        """
        Use a timeout for the specified team.

        Returns:
            True if timeout was available and used, False otherwise.
        """
        if team == "home" and self.home_timeouts > 0:
            self.home_timeouts -= 1
            return True
        elif team == "away" and self.away_timeouts > 0:
            self.away_timeouts -= 1
            return True
        return False

    def get_score_diff(self) -> int:
        """Get score differential from perspective of possessing team."""
        if self.possession == "home":
            return self.home_score - self.away_score
        else:
            return self.away_score - self.home_score

    def get_distance_to_goal(self) -> int:
        """Get yards to the end zone for the possessing team."""
        if self.possession == "home":
            return 100 - self.yard_line
        else:
            return self.yard_line

    def is_quarter_over(self) -> bool:
        """Check if the current quarter has ended."""
        return self.time_left_seconds <= 0

    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        if self.quarter < 4:
            return False

        # Regulation End
        if self.quarter == 4 and self.time_left_seconds <= 0 and self.home_score != self.away_score:
            return True

        # Overtime Logic (Modified Sudden Death)
        if self.quarter >= 5:
            # Time expired in OT (Tie)
            if self.time_left_seconds <= 0:
                return True

            # Scoring wins
            # Note: Detailed possession logic (FG on 1st vs TD on 1st) is handled in Orchestrator
            # This is a basic check for score discrepancy after "Sudden Death" active
             # If we are in sudden death, any score difference ends it?
             # Not exactly, needs orchestration context.
             # We rely on Orchestrator to check specific OT win conditions and set game over flag
             # This method returns True if it's *obviously* over by time/clock.
            pass

        return False

    @property
    def is_overtime(self) -> bool:
        return self.quarter >= 5

    def reset(self) -> None:
        """Reset all state to initial values."""
        self.quarter = 1
        self.time_left = "15:00"
        self.home_score = 0
        self.away_score = 0
        self.possession = "home"
        self.down = 1
        self.distance = 10
        self.yard_line = 25
        self.home_timeouts = 3
        self.away_timeouts = 3
        self.last_clock_strategy = "NORMAL"
        self.ot_possessions = 0
        self.first_possession_score_type = None

    def to_dict(self) -> Dict[str, Any]:
        """Export state as dictionary for broadcasting."""
        return {
            "quarter": self.quarter,
            "time_left": self.time_left,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "possession": self.possession,
            "down": self.down,
            "distance": self.distance,
            "yard_line": self.yard_line,
            "home_timeouts": self.home_timeouts,
            "away_timeouts": self.away_timeouts,
            "clock_strategy": self.last_clock_strategy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameStateManager":
        """Create instance from dictionary (for loading saved games)."""
        return cls(
            quarter=data.get("quarter", 1),
            time_left=data.get("time_left", "15:00"),
            home_score=data.get("home_score", 0),
            away_score=data.get("away_score", 0),
            possession=data.get("possession", "home"),
            down=data.get("down", 1),
            distance=data.get("distance", 10),
            yard_line=data.get("yard_line", 25),
            home_timeouts=data.get("home_timeouts", 3),
            away_timeouts=data.get("away_timeouts", 3),
            last_clock_strategy=data.get("clock_strategy", "NORMAL"),
        )

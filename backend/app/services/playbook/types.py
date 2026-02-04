from dataclasses import dataclass
from enum import Enum

from .playbook import Play


class AggressionLevel(str, Enum):
    """Offensive coordinator aggression."""
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    AGGRESSIVE = "AGGRESSIVE"


class GameScript(str, Enum):
    """Game flow state."""
    TRAILING = "TRAILING"
    CLOSE = "CLOSE"
    LEADING = "LEADING"
    BLOWOUT = "BLOWOUT"


@dataclass
class GameSituation:
    """Current game context."""
    quarter: int
    time_remaining: int  # seconds
    down: int
    distance: int
    field_position: int  # 0-100 (own goal to opponent goal)
    score_diff: int     # Positive = winning


@dataclass
class PlayCallResult:
    """Output from AI decision."""
    selected_play: Play
    confidence: float  # 0.0-1.0
    reasoning: str

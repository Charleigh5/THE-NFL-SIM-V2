from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, List, Optional

class PlayResult(BaseModel):
    """Result of a play execution"""
    yards_gained: int
    is_touchdown: bool = False
    is_turnover: bool = False
    is_sack: bool = False
    is_penalty: bool = False
    penalty_yards: int = 0
    time_elapsed: float = 40.0  # seconds
    description: str

    # Detailed stats
    passer_id: Optional[int] = None
    receiver_id: Optional[int] = None
    rusher_id: Optional[int] = None
    tackler_ids: List[int] = []

    # Environmental impacts
    weather_impact: float = 0.0
    turf_impact: float = 0.0

    # Injuries and fatigue
    injuries: List[Dict[str, Any]] = []
    fatigue_deltas: Dict[int, float] = {}  # player_id -> fatigue_change

    # XP awards
    xp_awards: Dict[int, int] = {}  # player_id -> xp_gained

    # Society/Media
    headline: Optional[str] = None
    is_highlight_worthy: bool = False

    model_config = ConfigDict(from_attributes=True)

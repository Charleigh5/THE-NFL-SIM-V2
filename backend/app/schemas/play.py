from typing import Any

from pydantic import BaseModel, ConfigDict


class PlayResult(BaseModel):
    """Result of a play execution"""
    yards_gained: int
    is_touchdown: bool = False
    is_turnover: bool = False
    is_sack: bool = False
    is_penalty: bool = False
    is_safety: bool = False
    penalty_yards: int = 0
    time_elapsed: float = 40.0  # seconds
    description: str

    # Detailed stats
    passer_id: int | None = None
    receiver_id: int | None = None
    rusher_id: int | None = None
    tackler_ids: list[int] = []

    # Environmental impacts
    weather_impact: float = 0.0
    turf_impact: float = 0.0

    # Injuries and fatigue
    injuries: list[dict[str, Any]] = []
    fatigue_deltas: dict[int, float] = {}  # player_id -> fatigue_change

    # XP awards
    xp_awards: dict[int, int] = {}  # player_id -> xp_gained

    # Society/Media
    headline: str | None = None
    is_highlight_worthy: bool = False

    # Attribute Interactions (Set 5)
    interaction_events: list[dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)

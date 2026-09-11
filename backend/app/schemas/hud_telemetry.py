"""
In-Game HUD & Telemetry Schemas
================================
Pydantic V2 schemas for live game-day HUD telemetry:
1. Ben Baldwin 4th-down decision payloads
2. Game momentum play-by-play nodes with Win Probability & EPA deltas
3. Multi-drive momentum flow curves
"""

from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict


class FourthDownTelemetryRequest(BaseModel):
    """Request payload for real-time 4th-down decision telemetry."""
    yard_line: int = Field(default=50, ge=1, le=99, description="Field position from own endzone (1-99)")
    yards_to_go: int = Field(default=1, ge=1, le=50, description="Yards required for 1st down")
    score_differential: int = Field(default=0, description="Team score minus opponent score")
    quarter: int = Field(default=4, ge=1, le=5, description="Game quarter (1-4, 5 for OT)")
    time_remaining_seconds: int = Field(default=300, ge=0, le=900, description="Seconds left in current quarter")
    timeouts: int = Field(default=3, ge=0, le=3, description="Timeouts remaining for offense")


class FourthDownTelemetryPayload(BaseModel):
    """Real-time telemetry payload for the floating glassmorphic Baldwin HUD pill."""
    yard_line: int = Field(ge=1, le=99)
    yards_to_go: int = Field(ge=1, le=50)
    score_differential: int
    quarter: int = Field(ge=1, le=5)
    time_remaining_seconds: int = Field(ge=0, le=900)
    recommendation: Literal["GO", "FIELD_GOAL", "PUNT"]
    recommendation_strength: Literal[
        "STRONG_GO", "LEAN_GO", "TOSS_UP", "LEAN_PUNT", "STRONG_PUNT", "STRONG_FG", "LEAN_FG"
    ]
    wp_go: float = Field(ge=0.0, le=1.0)
    wp_fg: float = Field(ge=0.0, le=1.0)
    wp_punt: float = Field(ge=0.0, le=1.0)
    wp_net_gain: float = Field(description="Win probability delta between best and second-best choice")
    conversion_prob: float = Field(ge=0.0, le=1.0)
    fg_make_prob: float = Field(ge=0.0, le=1.0)
    fg_distance: int
    summary: str
    is_garbage_time: bool = False
    model_config = ConfigDict(from_attributes=True)


class GameMomentumPlayNode(BaseModel):
    """Play-by-play node in the game momentum & Win Probability curve."""
    play_index: int
    quarter: int = Field(ge=1, le=5)
    game_clock: str
    down: int = Field(ge=1, le=4)
    distance: int = Field(ge=1, le=99)
    yard_line: int = Field(ge=1, le=99)
    description: str
    home_win_prob: float = Field(ge=0.0, le=1.0)
    away_win_prob: float = Field(ge=0.0, le=1.0)
    play_epa: float
    is_key_event: bool = False
    model_config = ConfigDict(from_attributes=True)


class MomentumFlowResponse(BaseModel):
    """Comprehensive momentum flow response for the active game session."""
    game_id: int
    play_nodes: List[GameMomentumPlayNode]
    current_home_wp: float = Field(ge=0.0, le=1.0)
    current_away_wp: float = Field(ge=0.0, le=1.0)
    home_team_abbr: str
    away_team_abbr: str
    home_score: int = 0
    away_score: int = 0
    model_config = ConfigDict(from_attributes=True)

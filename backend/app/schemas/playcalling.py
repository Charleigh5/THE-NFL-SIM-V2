"""
Play Calling & 4th-Down In-Game Schemas
=======================================
Pydantic V2 schemas for live game interactive coaching, play selection,
Ben Baldwin 4th-down decision analytics, and timeout/clock management.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class PlayCallRequest(BaseModel):
    """Payload to execute an interactive offensive or defensive play call."""
    game_id: int = Field(..., description="Target active simulation game ID")
    team_id: int = Field(..., description="Team making the call")
    play_type: Literal["RUN", "PASS", "FIELD_GOAL", "PUNT", "SPIKE", "KNEEL"]
    concept_id: str = Field(
        ...,
        description="Tactical concept ID (e.g. 'inside_zone', 'slants', 'cover_3', 'fire_zone')"
    )
    tempo: Literal["NORMAL", "HURRY_UP", "CHEW_CLOCK"] = "NORMAL"


class PlayCallResponse(BaseModel):
    """Response returned upon accepting an in-game play call."""
    success: bool
    game_id: int
    team_id: int
    play_type: str
    concept_id: str
    tempo: str
    message: str


class FourthDownRecommendationRequest(BaseModel):
    """Context required to generate Ben Baldwin 4th-down decision modeling."""
    down: int = Field(4, ge=1, le=4, description="Current down (usually 4)")
    distance: int = Field(..., ge=1, le=99, description="Yards to go for first down")
    yardline: int = Field(
        ..., ge=1, le=99,
        description="Distance from own endzone (1 to 99, where 50 is midfield, 80 is opponent 20)"
    )
    score_diff: int = Field(0, description="Score differential: team_score minus opponent_score")
    time_remaining: int = Field(900, ge=0, le=3600, description="Seconds remaining in game/half")
    timeouts: int = Field(3, ge=0, le=3, description="Timeouts remaining for possession team")
    game_id: Optional[int] = Field(None, description="Optional active game ID")


class FourthDownRecommendationResponse(BaseModel):
    """Analytics and win-probability guidance for 4th-down decisions."""
    recommendation: Literal["GO", "FIELD_GOAL", "PUNT"]
    wp_go: float = Field(..., description="Win probability if attempting 4th-down conversion")
    wp_fg: float = Field(..., description="Win probability if attempting field goal")
    wp_punt: float = Field(..., description="Win probability if punting")
    ep_go: float = Field(..., description="Expected points added if attempting conversion")
    ep_fg: float = Field(..., description="Expected points added if kicking field goal")
    ep_punt: float = Field(..., description="Expected points added if punting")
    conversion_prob: float = Field(..., description="Probability of converting 4th down")
    fg_make_prob: float = Field(..., description="Probability of making field goal")
    fg_distance: int = Field(..., description="Total field goal distance in yards")
    recommendation_strength: str = Field(..., description="Strength of analytics recommendation")
    summary: str = Field(..., description="Human-readable coaching summary")


class TimeoutRequest(BaseModel):
    """Request to stop clock and spend an available timeout."""
    game_id: int = Field(..., description="Active game ID")
    team_id: int = Field(..., description="Team calling timeout")


class TimeoutResponse(BaseModel):
    """Outcome of timeout call."""
    success: bool
    game_id: int
    team_id: int
    timeouts_remaining: int
    message: str

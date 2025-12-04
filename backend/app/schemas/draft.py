from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Optional


class HistoricalComparison(BaseModel):
    """Historical player comparison from NFL Stats MCP."""
    model_config = ConfigDict(from_attributes=True)

    comparable_player_name: str = Field(description="Name of historically similar player")
    seasons_active: str = Field(description="Active years (e.g., '2010-2018')")
    career_highlights: str = Field(description="Notable achievements")
    similarity_score: float = Field(ge=0.0, le=1.0, description="How similar (0-1)")


class RosterGapAnalysis(BaseModel):
    """Detailed position group gap analysis."""
    model_config = ConfigDict(from_attributes=True)

    position: str
    current_count: int
    target_count: int
    starter_quality: float = Field(ge=0.0, le=1.0, description="Avg starter rating 0-1")
    priority_level: str = Field(description="CRITICAL, HIGH, MODERATE, LOW")


class AlternativePick(BaseModel):
    """Alternative draft pick suggestion."""
    model_config = ConfigDict(from_attributes=True)

    player_id: int
    player_name: str
    position: str
    overall_rating: int
    reasoning: str
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence 0-1")
    historical_comparison: Optional[HistoricalComparison] = None


class DraftSuggestionRequest(BaseModel):
    """Request for AI-powered draft pick suggestion."""
    model_config = ConfigDict(from_attributes=True)

    team_id: int
    pick_number: int
    available_players: List[int] = Field(description="Player IDs still available")
    include_historical_data: bool = Field(
        default=True,
        description="Fetch NFL historical comparisons via MCP"
    )


class DraftSuggestionResponse(BaseModel):
    """AI-powered draft pick recommendation with analytics."""
    model_config = ConfigDict(from_attributes=True)

    recommended_player_id: int
    player_name: str
    position: str
    overall_rating: int
    reasoning: str
    team_needs: Dict[str, float] = Field(description="Position → Need score (0-1)")
    alternative_picks: List[AlternativePick]
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")

    # Enhanced analytics
    historical_comparison: Optional[HistoricalComparison] = None
    roster_gap_analysis: Optional[List[RosterGapAnalysis]] = None
    draft_value_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=10.0,
        description="Value rating (1-10) based on pick position"
    )
    mcp_data_used: bool = Field(
        default=False,
        description="Whether MCP historical data was available"
    )

class DraftProspect(BaseModel):
    """Draft prospect details."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    position: str
    college: Optional[str] = None
    height: int
    weight: int
    age: int
    overall_rating: int

    # Physical attributes
    speed: int
    acceleration: int
    strength: int
    agility: int

    # Status
    is_rookie: bool
    projected_round: Optional[int] = None

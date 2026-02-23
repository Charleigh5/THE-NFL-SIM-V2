from pydantic import BaseModel, ConfigDict, Field


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
    historical_comparison: HistoricalComparison | None = None


class DraftSuggestionRequest(BaseModel):
    """Request for AI-powered draft pick suggestion."""

    model_config = ConfigDict(from_attributes=True)

    team_id: int
    pick_number: int
    available_players: list[int] = Field(description="Player IDs still available")
    include_historical_data: bool = Field(
        default=True, description="Fetch NFL historical comparisons via MCP"
    )


class DraftSuggestionResponse(BaseModel):
    """AI-powered draft pick recommendation with analytics."""

    model_config = ConfigDict(from_attributes=True)

    recommended_player_id: int
    player_name: str
    position: str
    overall_rating: int
    reasoning: str
    team_needs: dict[str, float] = Field(description="Position → Need score (0-1)")
    alternative_picks: list[AlternativePick]
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")

    # Enhanced analytics
    historical_comparison: HistoricalComparison | None = None
    roster_gap_analysis: list[RosterGapAnalysis] | None = None
    draft_value_score: float | None = Field(
        default=None, ge=0.0, le=10.0, description="Value rating (1-10) based on pick position"
    )
    mcp_data_used: bool = Field(
        default=False, description="Whether MCP historical data was available"
    )


class DraftProspect(BaseModel):
    """Draft prospect details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    position: str
    college: str | None = None
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
    projected_round: int | None = None

    # --- NFL Combine Metrics ---
    forty_yard_dash: float | None = None
    bench_press: int | None = None
    vertical_jump: float | None = None
    broad_jump: int | None = None
    three_cone_drill: float | None = None
    twenty_yard_shuttle: float | None = None

    # --- Genesis Data (Advanced Biometrics) ---
    power_clean_max: int | None = None  # lbs
    gps_speed_max: float | None = None  # mph
    s2_cognition_score: int | None = None  # 0-99
    medical_flags: list[str] | None = None
    genesis_revealed: bool = False

"""Trade-related Pydantic schemas for API request/response validation."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class TradeDecision(StrEnum):
    """Possible GM trade decisions."""

    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    COUNTER = "COUNTER"


class DraftPickInfo(BaseModel):
    """Draft pick information for trade proposals."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, description="Specific DraftPick DB row ID if known")
    round: int = Field(ge=1, le=7, description="Draft round (1-7)")
    year: int = Field(ge=2024, le=2035, description="Draft year")
    original_team_id: int | None = Field(
        default=None, description="Original team that owned the pick (if traded)"
    )


class TradeEvaluationRequest(BaseModel):
    """Request body for trade evaluation endpoint."""

    model_config = ConfigDict(from_attributes=True)

    offering_team_id: int | None = Field(
        default=None, description="Team ID making the offer (required for pick-only trades)"
    )
    offered_player_ids: list[int] = Field(
        default_factory=list, description="Player IDs being offered to the target team"
    )
    requested_player_ids: list[int] = Field(
        default_factory=list, description="Player IDs being requested from the target team"
    )
    target_team_id: int = Field(description="Team ID to evaluate the trade for")
    offered_picks: list[DraftPickInfo] | None = Field(
        default=None, description="Draft picks being offered"
    )
    requested_picks: list[DraftPickInfo] | None = Field(
        default=None, description="Draft picks being requested"
    )


class FactorBreakdownSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    market_tvp: float = 0.0
    need_fit_delta: float = 0.0
    cap_impact_delta: float = 0.0
    window_fit_delta: float = 0.0
    class_fit_delta: float = 0.0
    realism_modifiers_delta: float = 0.0
    gm_threshold: float = 1.00


class TeamSideGradeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    team_id: int
    competitive_window: str = "BUBBLE"
    value_in_tvp: float = 0.0
    value_out_tvp: float = 0.0
    ratio: float = 1.0
    grade: str = "B"
    factors: FactorBreakdownSchema = Field(default_factory=FactorBreakdownSchema)


class CounterOfferSuggestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    add_player_ids: list[int] = Field(default_factory=list)
    add_picks: list[DraftPickInfo] = Field(default_factory=list)
    summary: str = ""


class TradeEvaluationResponse(BaseModel):
    """Response from trade evaluation endpoint."""

    model_config = ConfigDict(from_attributes=True)

    decision: TradeDecision = Field(description="GM's decision on the trade")
    score: float = Field(description="Trade value score (positive = favorable)")
    reasoning: str = Field(description="Explanation of the decision")

    # Additional context
    offered_value: float | None = Field(
        default=None, description="Calculated value of offered assets"
    )
    requested_value: float | None = Field(
        default=None, description="Calculated value of requested assets"
    )
    gm_philosophy: str | None = Field(
        default=None, description="Target team's GM philosophy that influenced decision"
    )

    # CTVE V2 additions
    user_side: TeamSideGradeSchema | None = Field(
        default=None, description="Evaluation and grade from offering user team's perspective"
    )
    ai_side: TeamSideGradeSchema | None = Field(
        default=None, description="Evaluation and grade from receiving AI team's perspective"
    )
    ai_threshold: float | None = Field(
        default=None, description="Target GM's contextual acceptance threshold"
    )
    counter_offer: CounterOfferSuggestion | None = Field(
        default=None, description="Minimal knapsack sweetener to balance a close trade"
    )
    narrative_notes: list[str] = Field(
        default_factory=list, description="Contextual narrative tags (rivalry, comp floor, medical, etc.)"
    )


class TradeOfferRequest(BaseModel):
    """Request body for submitting a formal trade offer."""

    model_config = ConfigDict(from_attributes=True)

    offering_team_id: int | None = Field(
        default=None, description="Team ID making the offer (required for pick-only trades)"
    )
    offered_player_ids: list[int] = Field(
        default_factory=list, description="Player IDs being offered"
    )
    requested_player_ids: list[int] = Field(
        default_factory=list, description="Player IDs being requested"
    )
    target_team_id: int = Field(description="Team to send the offer to")
    offered_picks: list[DraftPickInfo] | None = Field(
        default=None, description="Draft picks being offered"
    )
    requested_picks: list[DraftPickInfo] | None = Field(
        default=None, description="Draft picks being requested"
    )
    message: str | None = Field(
        default=None, max_length=500, description="Optional message to include with offer"
    )


class TradeOfferResponse(BaseModel):
    """Response from submitting a trade offer."""

    model_config = ConfigDict(from_attributes=True)

    offer_id: int = Field(description="Unique ID for tracking the offer")
    status: str = Field(description="Current status: PENDING, ACCEPTED, REJECTED, EXPIRED")
    message: str = Field(description="Status message")


class PlayerTradeInfo(BaseModel):
    """Simplified player info for trade displays."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    position: str
    overall_rating: int
    age: int
    salary: int
    contract_years: int


class TradeOfferStatus(StrEnum):
    """Status of a trade offer."""

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    COUNTERED = "COUNTERED"
    EXPIRED = "EXPIRED"
    WITHDRAWN = "WITHDRAWN"


class TradeAssetRead(BaseModel):
    """Simplified asset info for reading offers."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str = Field(description="'player' or 'pick'")
    name: str
    value: int
    team_id: int
    position: str | None = None


class TradeOfferRead(BaseModel):
    """Schema for reading a trade offer from the database."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    offering_team_id: int
    receiving_team_id: int
    offered_assets: list[TradeAssetRead] = Field(default_factory=list)
    requested_assets: list[TradeAssetRead] = Field(default_factory=list)
    status: TradeOfferStatus
    message: str | None = None
    gm_response: str | None = None
    created_at: str
    expires_at: str | None = None
    parent_offer_id: int | None = None


class PendingOffersResponse(BaseModel):
    """Response for pending offers endpoint."""

    model_config = ConfigDict(from_attributes=True)

    incoming: list[TradeOfferRead] = Field(default_factory=list)
    outgoing: list[TradeOfferRead] = Field(default_factory=list)


class TradeRespondRequest(BaseModel):
    """Request to respond to a trade offer."""

    model_config = ConfigDict(from_attributes=True)

    action: str = Field(description="'accept' or 'reject'")
    message: str | None = Field(default=None, max_length=500)

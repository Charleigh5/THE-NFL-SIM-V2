"""Trade-related Pydantic schemas for API request/response validation."""

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from enum import Enum


class TradeDecision(str, Enum):
    """Possible GM trade decisions."""
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    COUNTER = "COUNTER"


class DraftPickInfo(BaseModel):
    """Draft pick information for trade proposals."""
    model_config = ConfigDict(from_attributes=True)

    round: int = Field(ge=1, le=7, description="Draft round (1-7)")
    year: int = Field(ge=2024, le=2030, description="Draft year")
    original_team_id: Optional[int] = Field(
        default=None,
        description="Original team that owned the pick (if traded)"
    )


class TradeEvaluationRequest(BaseModel):
    """Request body for trade evaluation endpoint."""
    model_config = ConfigDict(from_attributes=True)

    offered_player_ids: List[int] = Field(
        default_factory=list,
        description="Player IDs being offered to the target team"
    )
    requested_player_ids: List[int] = Field(
        default_factory=list,
        description="Player IDs being requested from the target team"
    )
    target_team_id: int = Field(description="Team ID to evaluate the trade for")
    offered_picks: Optional[List[DraftPickInfo]] = Field(
        default=None,
        description="Draft picks being offered"
    )
    requested_picks: Optional[List[DraftPickInfo]] = Field(
        default=None,
        description="Draft picks being requested"
    )


class TradeEvaluationResponse(BaseModel):
    """Response from trade evaluation endpoint."""
    model_config = ConfigDict(from_attributes=True)

    decision: TradeDecision = Field(description="GM's decision on the trade")
    score: float = Field(description="Trade value score (positive = favorable)")
    reasoning: str = Field(description="Explanation of the decision")

    # Additional context
    offered_value: Optional[float] = Field(
        default=None,
        description="Calculated value of offered assets"
    )
    requested_value: Optional[float] = Field(
        default=None,
        description="Calculated value of requested assets"
    )
    gm_philosophy: Optional[str] = Field(
        default=None,
        description="Target team's GM philosophy that influenced decision"
    )


class TradeOfferRequest(BaseModel):
    """Request body for submitting a formal trade offer."""
    model_config = ConfigDict(from_attributes=True)

    offered_player_ids: List[int] = Field(
        default_factory=list,
        description="Player IDs being offered"
    )
    requested_player_ids: List[int] = Field(
        default_factory=list,
        description="Player IDs being requested"
    )
    target_team_id: int = Field(description="Team to send the offer to")
    offered_picks: Optional[List[DraftPickInfo]] = Field(
        default=None,
        description="Draft picks being offered"
    )
    requested_picks: Optional[List[DraftPickInfo]] = Field(
        default=None,
        description="Draft picks being requested"
    )
    message: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional message to include with offer"
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

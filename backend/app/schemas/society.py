"""
Society Engine Schemas (2025/2026 Production Standard)
======================================================
Strict Pydantic V2 schemas for Psychological DNA, Mathematical Tension Engine,
and Tier 3 Agentic Locker Room Council Service.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class PsychologicalDNA(BaseModel):
    """
    Big-Six Psychological Profile for Elite Athletics.
    Values bounded 0 to 100, centered around 50.
    """
    ego: int = Field(default=50, ge=0, le=100, description="Demand for spotlight, targets, and stardom")
    greed: int = Field(default=50, ge=0, le=100, description="Financial motivation and contract leverage urgency")
    loyalty: int = Field(default=50, ge=0, le=100, description="Allegiance to organization and coaching staff")
    resilience: int = Field(default=50, ge=0, le=100, description="Ability to absorb adversity, losses, and fatigue")
    paranoia: int = Field(default=50, ge=0, le=100, description="Sensitivity to benching, scheming, and front office slights")
    professionalism: int = Field(default=50, ge=0, le=100, description="Work ethic, locker room poise, and leadership readiness")

    model_config = ConfigDict(from_attributes=True)


class PlayerBackstory(BaseModel):
    """
    Narrative context and relational linkages for player behavior.
    """
    origin: str = Field(default="", description="Hometown / childhood narrative anchor")
    financial_motive: str = Field(default="", description="Economic driver (e.g. multi-gen wealth, bet on self)")
    career_milestone: str = Field(default="", description="Current athletic ambition or chip on shoulder")
    draft_narrative: str = Field(default="", description="Draft pedigree or underdog journey")
    mentor_id: Optional[int] = Field(default=None, description="Player ID of locker room mentor")
    rival_id: Optional[int] = Field(default=None, description="Player ID of inter-squad or league rival")

    model_config = ConfigDict(from_attributes=True)


class TensionDelta(BaseModel):
    """
    Deterministic weekly delta produced by Tier 1 Mathematical Tension Engine.
    """
    player_id: int
    prior_tension: float
    new_tension: float
    primary_driver: str
    morale_delta: int
    is_active_grievance: bool

    model_config = ConfigDict(from_attributes=True)


class LockerRoomDialogueTurn(BaseModel):
    """
    Single spoken or observed beat in a closed-door multi-agent locker room confrontation.
    """
    speaker_name: str
    speaker_role: str = Field(description="E.g. 'disgruntled_star', 'team_captain', 'head_coach', 'position_coach'")
    speaker_id: Optional[int] = None
    text: str

    model_config = ConfigDict(from_attributes=True)


class LockerRoomConsequences(BaseModel):
    """
    State mutations resulting from a locker room incident.
    """
    morale_deltas: Dict[str, int] = Field(default_factory=dict, description="Player ID string -> morale delta")
    trust_coach_deltas: Dict[str, int] = Field(default_factory=dict, description="Player ID string -> trust in coach delta")
    trust_qb_deltas: Dict[str, int] = Field(default_factory=dict, description="Player ID string -> trust in QB delta")
    trade_requested: bool = Field(default=False, description="Whether active actor officially requested trade")
    team_chemistry_delta: float = Field(default=0.0, description="Net team chemistry shift (-20.0 to +10.0)")
    drama_headline: str = Field(default="", description="Beat reporter or internal memo summary")

    model_config = ConfigDict(from_attributes=True)


class LockerRoomActionOption(BaseModel):
    """
    Actionable choices presented to User (GM / Head Coach) to resolve grievance.
    """
    id: str = Field(description="Unique key: 'promise_targets', 'bench_player', 'address_team', 'explore_trade', 'fine_conduct'")
    label: str
    description: str
    projected_impact: str

    model_config = ConfigDict(from_attributes=True)


class LockerRoomEventResponse(BaseModel):
    """
    Complete payload produced by Tier 2 Gate + Tier 3 Agentic Council.
    """
    team_id: int
    week: int
    active_actors: List[int] = Field(description="Player IDs of aggrieved players (1 to 3)")
    captain_id: Optional[int] = None
    headline: str
    dialogue: List[LockerRoomDialogueTurn]
    consequences: LockerRoomConsequences
    action_options: List[LockerRoomActionOption]
    summary: str

    model_config = ConfigDict(from_attributes=True)


class LockerRoomResolutionRequest(BaseModel):
    """
    User submission to resolve a pending locker room incident.
    """
    team_id: int
    action_id: str
    week: int
    active_actor_ids: List[int]

    model_config = ConfigDict(from_attributes=True)


class LockerRoomResolutionResponse(BaseModel):
    """
    Feedback from applied resolution.
    """
    team_id: int
    action_id: str
    success: bool
    message: str
    updated_chemistry: float

    model_config = ConfigDict(from_attributes=True)

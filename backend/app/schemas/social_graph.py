"""
Social Graph & Media Leaks Schemas
==================================
Pydantic V2 schemas for 2D locker room social network visualization,
clique detection, contract holdouts, and media leak dispatches.
"""

from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict


class GraphNode(BaseModel):
    """A player node positioned in 2D normalized coordinate space."""
    id: int
    name: str
    position: str
    overall_rating: int
    tension_score: float = Field(default=0.0, ge=0.0, le=100.0)
    trust_in_coach: int = Field(default=80, ge=0, le=100)
    clique_id: str = Field(description="E.g. 'OFF_LEADERS', 'DEF_CORE', 'VETERANS', 'REBELS'")
    role: Literal["CAPTAIN", "MENTOR", "STUBBORN_VET", "DISRUPTOR", "NEUTRAL"]
    x: float = Field(description="2D coordinate X [100, 900]")
    y: float = Field(description="2D coordinate Y [100, 500]")
    is_holding_out: bool = Field(default=False, description="True if player is on active contract holdout")
    backstory_summary: Optional[str] = None


class GraphEdge(BaseModel):
    """Relational connection between two players in the locker room."""
    source: int = Field(description="Source player ID")
    target: int = Field(description="Target player ID")
    weight: float = Field(default=0.5, ge=0.0, le=1.0, description="Strength of connection")
    relationship_type: Literal["BOND", "RIVALRY", "MENTORSHIP", "FRICTION"]


class MediaLeakPost(BaseModel):
    """An insider tweet or beat reporter dispatch leaked from the locker room."""
    id: str
    author_name: str
    author_handle: str
    author_avatar: str
    outlet: Literal["ESPN", "NFL_NETWORK", "THE_ATHLETIC", "LOCAL_BEAT"]
    timestamp_str: str
    headline: str
    content: str
    sentiment: Literal["NEGATIVE", "NEUTRAL", "POSITIVE", "SCANDAL"]
    referenced_player_ids: List[int] = Field(default_factory=list)
    leak_source: Literal["ANONYMOUS_PLAYER", "AGENT", "COACHING_STAFF", "FRONT_OFFICE"]


class LockerRoomSocialNetworkResponse(BaseModel):
    """Complete social graph topology and media wire for a franchise."""
    team_id: int
    cliques: Dict[str, str] = Field(description="Clique ID -> Human readable name")
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    active_leaks: List[MediaLeakPost]
    team_morale_index: float
    active_holdouts_count: int
    model_config = ConfigDict(from_attributes=True)


class HoldoutResolutionRequest(BaseModel):
    """Action chosen by GM to respond to an athlete holding out."""
    action: Literal["CONCEDE_CONTRACT", "FINE_DAILY", "PLACE_ON_RESERVE"]
    sweetener_bonus: Optional[int] = Field(default=0, ge=0)

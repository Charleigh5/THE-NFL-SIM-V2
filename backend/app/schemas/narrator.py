from typing import Literal

from pydantic import BaseModel, Field

from app.services.broadcasting_service import BroadcastStyle

PageRouteKey = Literal[
    "dashboard",
    "season",
    "offseason",
    "free-agency",
    "draft",
    "front-office",
    "depth-chart",
    "trade-center",
    "trophy-room",
    "live-sim",
    "medical-center",
    "locker-room",
    "playbook",
    "training",
    "skills",
]


class NarrationContextRequest(BaseModel):
    page: PageRouteKey
    team_id: int = Field(ge=1)
    player_id: int | None = Field(default=None, ge=1)
    game_id: int | None = Field(default=None, ge=1)
    style: BroadcastStyle = BroadcastStyle.ESPN


class FactItem(BaseModel):
    fact_id: str
    category: Literal["last_game", "season", "franchise", "player", "storyline"]
    label: str
    value: str


class FactPacket(BaseModel):
    page: PageRouteKey
    team_name: str
    team_record: str
    season_year: int
    current_week: int
    facts: list[FactItem]


class StructuredAnchorScript(BaseModel):
    script: str = Field(max_length=700)
    facts_used: list[str]
    headline_banner: str = Field(max_length=90)


class NarrationResponse(BaseModel):
    script: str
    headline_banner: str
    cache_key: str
    audio_url: str | None
    voice_source: Literal["voicestudio", "browser"]
    degraded: bool
    style: BroadcastStyle

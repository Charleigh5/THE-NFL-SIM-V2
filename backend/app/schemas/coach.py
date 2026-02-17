from typing import Any

from pydantic import BaseModel, ConfigDict


class CoachBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    offense_rating: int = 50
    defense_rating: int = 50
    development_rating: int = 50
    skills: dict[str, Any] = {}
    traits: list[str] = []
    playbook_offense: str | None = None
    playbook_defense: str | None = None
    philosophy: dict[str, Any] = {}

class CoachCreate(CoachBase):
    team_id: int | None = None

class Coach(CoachBase):
    id: int
    team_id: int | None = None
    xp: int = 0
    level: int = 1

    model_config = ConfigDict(from_attributes=True)

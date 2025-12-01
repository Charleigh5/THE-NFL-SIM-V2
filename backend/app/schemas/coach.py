from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List

class CoachBase(BaseModel):
    first_name: str
    last_name: str
    role: str
    offense_rating: int = 50
    defense_rating: int = 50
    development_rating: int = 50
    skills: Dict[str, Any] = {}
    traits: List[str] = []
    playbook_offense: Optional[str] = None
    playbook_defense: Optional[str] = None
    philosophy: Dict[str, Any] = {}

class CoachCreate(CoachBase):
    team_id: Optional[int] = None

class Coach(CoachBase):
    id: int
    team_id: Optional[int] = None
    xp: int = 0
    level: int = 1

    model_config = ConfigDict(from_attributes=True)

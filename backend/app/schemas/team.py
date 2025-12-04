from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeamBase(BaseModel):
    name: str
    city: str
    abbreviation: str
    conference: str
    division: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    established_year: Optional[int] = None
    stadium_id: Optional[int] = None

    # Medical & Staff
    medical_rating: int = 50
    training_staff_quality: int = 50
    medical_budget: float = 10.0

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

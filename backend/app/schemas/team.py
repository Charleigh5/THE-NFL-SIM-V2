from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str
    city: str
    abbreviation: str
    conference: str
    division: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    elo_rating: float = 1500.0  # Power Ranking
    logo_url: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    established_year: int | None = None
    stadium_id: int | None = None

    # Medical & Staff
    medical_rating: int = 50
    training_staff_quality: int = 50
    medical_budget: float = 10.0


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

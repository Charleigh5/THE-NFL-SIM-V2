from pydantic import BaseModel
from typing import List

class PlayerLeader(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    value: int | float
    stat_type: str  # "passing_yards", "rushing_yards", "receiving_yards"

class LeagueLeaders(BaseModel):
    passing_yards: List[PlayerLeader]
    rushing_yards: List[PlayerLeader]
    receiving_yards: List[PlayerLeader]

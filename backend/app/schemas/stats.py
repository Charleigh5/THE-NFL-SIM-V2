from pydantic import BaseModel, ConfigDict


class PlayerLeader(BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    value: int | float
    stat_type: str  # "passing_yards", "rushing_yards", "receiving_yards"

    model_config = ConfigDict(from_attributes=True)


class LeagueLeaders(BaseModel):
    passing_yards: list[PlayerLeader]
    passing_tds: list[PlayerLeader]
    rushing_yards: list[PlayerLeader]
    rushing_tds: list[PlayerLeader]
    receiving_yards: list[PlayerLeader]
    receiving_tds: list[PlayerLeader]

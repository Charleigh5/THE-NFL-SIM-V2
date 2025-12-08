from pydantic import BaseModel, Field
from typing import Optional, List

class ExternalPlayerStats(BaseModel):
    """
    Schema representing player stats from the external data source (nflreadpy).
    """
    player_id: str = Field(..., alias="player_id")
    player_display_name: str
    position: str
    season: int
    headshot_url: Optional[str] = None

    # Common Stats
    games: int = 0

    # Passing
    completions: int = 0
    attempts: int = 0
    passing_yards: float = 0.0
    passing_tds: int = 0
    interceptions: int = 0
    sack_fumbles: int = 0

    # Rushing
    carries: int = 0
    rushing_yards: float = 0.0
    rushing_tds: int = 0
    rushing_fumbles: int = 0

    # Receiving
    receptions: int = 0
    targets: int = 0
    receiving_yards: float = 0.0
    receiving_tds: int = 0

    # Fantasy/Advanced
    fantasy_points: float = 0.0
    fantasy_points_ppr: float = 0.0

    class Config:
        populate_by_name = True
        extra = "ignore" # Ignore extra fields from nflreadpy we don't care about

class ExternalScheduleGame(BaseModel):
    """
    Schema representing a game in the schedule.
    """
    game_id: str
    season: int
    game_type: str
    week: int
    gameday: str
    weekday: str
    gametime: Optional[str]

    home_team: str
    away_team: str
    home_score: Optional[int]
    away_score: Optional[int]

    location: Optional[str]
    result: Optional[int]
    total: Optional[int]
    overtime: Optional[bool]

    class Config:
        extra = "ignore"

class ExternalPlayerInfo(BaseModel):
    """
    Schema representing roster information.
    """
    gsis_id: Optional[str]
    display_name: Optional[str]
    position: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    birth_date: Optional[str]
    college_name: Optional[str]
    headshot_url: Optional[str]

    class Config:
        extra = "ignore"

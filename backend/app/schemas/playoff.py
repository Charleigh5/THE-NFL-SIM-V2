from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.models.playoff import PlayoffRound, PlayoffConference
from app.schemas.team import Team

class PlayoffMatchupBase(BaseModel):
    season_id: int
    round: PlayoffRound
    conference: PlayoffConference
    matchup_code: str
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    home_team_seed: Optional[int] = None
    away_team_seed: Optional[int] = None
    next_matchup_id: Optional[int] = None

class PlayoffMatchupCreate(PlayoffMatchupBase):
    pass

class PlayoffMatchup(PlayoffMatchupBase):
    id: int
    winner_id: Optional[int] = None
    game_id: Optional[int] = None
    
    home_team: Optional[Team] = None
    away_team: Optional[Team] = None
    winner: Optional[Team] = None

    model_config = ConfigDict(from_attributes=True)

class PlayoffBracket(BaseModel):
    season_id: int
    matchups: List[PlayoffMatchup]

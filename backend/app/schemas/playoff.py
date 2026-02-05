
from pydantic import BaseModel, ConfigDict

from app.models.playoff import PlayoffConference, PlayoffRound
from app.schemas.team import Team


class PlayoffMatchupBase(BaseModel):
    season_id: int
    round: PlayoffRound
    conference: PlayoffConference
    matchup_code: str
    home_team_id: int | None = None
    away_team_id: int | None = None
    home_team_seed: int | None = None
    away_team_seed: int | None = None
    next_matchup_id: int | None = None

class PlayoffMatchupCreate(PlayoffMatchupBase):
    pass

class PlayoffMatchup(PlayoffMatchupBase):
    id: int
    winner_id: int | None = None
    game_id: int | None = None

    home_team: Team | None = None
    away_team: Team | None = None
    winner: Team | None = None

    model_config = ConfigDict(from_attributes=True)

class PlayoffBracket(BaseModel):
    season_id: int
    matchups: list[PlayoffMatchup]

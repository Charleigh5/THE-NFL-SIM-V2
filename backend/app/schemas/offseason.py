from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TeamNeed(BaseModel):
    position: str
    current_count: int
    target_count: int
    need_score: float  # Higher means more needed

class Prospect(BaseModel):
    id: int
    name: str
    position: str
    overall_rating: int
    
    model_config = ConfigDict(from_attributes=True)

class DraftPickSummary(BaseModel):
    round: int
    pick_number: int
    team_id: int
    player_name: str
    player_position: str
    player_overall: int

class DraftPickDetail(BaseModel):
    id: int
    season_id: int
    team_id: int
    original_team_id: int
    round: int
    pick_number: int
    player_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class PlayerProgressionResult(BaseModel):
    player_id: int
    name: str
    position: str
    change: int
    old_rating: int
    new_rating: int
    
    model_config = ConfigDict(from_attributes=True)

class PlayerProgressionSummary(BaseModel):
    player_id: int
    player_name: str
    previous_rating: int
    new_rating: int
    change: int

class FreeAgentSigning(BaseModel):
    player_id: int
    player_name: str
    position: str
    overall_rating: int
    age: int
    team_id: int
    team_name: str
    years: int = 1
    total_salary: float = 0.0
    aav: float = 0.0
    guaranteed_money: float = 0.0
    grade: str = "B"
    competing_offers_count: int = 1
    
    # Optional alias fields
    contract_years: Optional[int] = None
    total_value: Optional[float] = None
    annual_avg: Optional[float] = None
    guaranteed: Optional[float] = None
    signing_grade: Optional[str] = None
    signing_round: Optional[int] = None
    bidding_teams_count: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    def __init__(self, **data):
        if "contract_years" in data and "years" not in data:
            data["years"] = data["contract_years"]
        if "total_value" in data and "total_salary" not in data:
            data["total_salary"] = data["total_value"]
        if "annual_avg" in data and "aav" not in data:
            data["aav"] = data["annual_avg"]
        if "guaranteed" in data and "guaranteed_money" not in data:
            data["guaranteed_money"] = data["guaranteed"]
        if "signing_grade" in data and "grade" not in data:
            data["grade"] = data["signing_grade"]
        if "bidding_teams_count" in data and "competing_offers_count" not in data:
            data["competing_offers_count"] = data["bidding_teams_count"]
        super().__init__(**data)

class FreeAgentMarketPlayer(BaseModel):
    player_id: int
    player_name: str
    position: str
    overall_rating: int
    age: int
    projected_aav: float
    projected_years: int
    tier: str
    top_interested_teams: List[str]
    
    model_config = ConfigDict(from_attributes=True)

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

from pydantic import BaseModel
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
    
    class Config:
        from_attributes = True

class DraftPickSummary(BaseModel):
    round: int
    pick_number: int
    team_id: int
    player_name: str
    player_position: str
    player_overall: int

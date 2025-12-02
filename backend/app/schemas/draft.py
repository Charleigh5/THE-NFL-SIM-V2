from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional


class AlternativePick(BaseModel):
    """Alternative draft pick suggestion."""
    model_config = ConfigDict(from_attributes=True)

    player_id: int
    player_name: str
    position: str
    overall_rating: int
    reasoning: str
    confidence_score: float  # 0.0 to 1.0


class DraftSuggestionRequest(BaseModel):
    """Request for AI-powered draft pick suggestion."""
    model_config = ConfigDict(from_attributes=True)

    team_id: int
    pick_number: int
    available_players: List[int]  # Player IDs still available in draft


class DraftSuggestionResponse(BaseModel):
    """AI-powered draft pick recommendation."""
    model_config = ConfigDict(from_attributes=True)

    recommended_player_id: int
    player_name: str
    position: str
    overall_rating: int
    reasoning: str
    team_needs: Dict[str, float]  # Position -> Need score (0.0 to 1.0)
    alternative_picks: List[AlternativePick]
    confidence_score: float  # Overall confidence in recommendation

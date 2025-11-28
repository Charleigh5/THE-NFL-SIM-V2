from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.player import Player
from app.kernels.genesis.bio_metrics import BiologicalProfile, FatigueRegulator
# from app.kernels.genesis.recruiting import RecruitingEngine  # TODO: Implement RecruitingEngine class
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/genesis", tags=["genesis"])

class BioMetricsResponse(BaseModel):
    fast_twitch_ratio: float
    max_acceleration_cap: float
    hand_size_inches: float
    wingspan_inches: float
    interaction_radius: float
    fumble_risk: float

@router.get("/player/{player_id}/bio-metrics", response_model=BioMetricsResponse)
def get_player_bio_metrics(
    player_id: int, 
    temperature_f: float = 72.0,
    db: Session = Depends(get_db)
):
    """Get biological metrics for a player."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Initialize bio-metrics (could be stored in DB in future)
    # For now, we derive them from existing player stats to ensure consistency
    speed_rating = player.speed if hasattr(player, 'speed') else 70.0
    height_inches = player.height if hasattr(player, 'height') else 72.0
    
    bio = BiologicalProfile(
        fast_twitch_ratio=0.5 + (speed_rating / 200.0),  # Derive from speed
        hand_size_inches=9.0, # Default for now
        wingspan_inches=height_inches * 1.04  # Rough wingspan estimate (height * 1.04 is typical)
    )
    
    return BioMetricsResponse(
        fast_twitch_ratio=bio.fast_twitch_ratio,
        max_acceleration_cap=bio.max_acceleration_cap,
        hand_size_inches=bio.hand_size_inches,
        wingspan_inches=bio.wingspan_inches,
        interaction_radius=bio.interaction_radius,
        fumble_risk=bio.calculate_fumble_risk(temperature_f)
    )

@router.get("/player/{player_id}/fatigue")
def get_player_fatigue(player_id: int, db: Session = Depends(get_db)):
    """Get fatigue status for a player."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
        
    # Create default regulator
    regulator = FatigueRegulator()
    
    return {
        "hrv": regulator.hrv,
        "lactic_acid": regulator.lactic_acid,
        "max_burst_capacity": regulator.max_burst_capacity,
        "home_climate": regulator.home_climate
    }

# TODO: Re-enable once RecruitingEngine is implemented
# @router.post("/recruit/generate")
# def generate_recruit(position: str, db: Session = Depends(get_db)):
#     """Generate a new draft prospect."""
#     recruiting = RecruitingEngine()
#     recruit = recruiting.generate_prospect(position)
#     return recruit

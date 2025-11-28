from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.player import Player
from pydantic import BaseModel

router = APIRouter()

class PlayerDetailSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    jersey_number: int
    overall_rating: int
    age: int
    experience: int
    height: int | None = None
    weight: int | None = None
    team_id: int | None = None
    
    # Attributes
    speed: int
    acceleration: int
    strength: int
    agility: int
    awareness: int

    class Config:
        from_attributes = True

@router.get("/{player_id}", response_model=PlayerDetailSchema)
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific player by ID.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.team import Team
from app.models.player import Player
from pydantic import BaseModel, ConfigDict

router = APIRouter()

# Pydantic models for responses (Simple versions)
class TeamSchema(BaseModel):
    id: int
    city: str
    name: str
    abbreviation: str
    conference: str
    division: str
    wins: int
    losses: int

    model_config = ConfigDict(from_attributes=True)

class PlayerSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str
    jersey_number: int
    overall_rating: int
    age: int
    experience: int

    model_config = ConfigDict(from_attributes=True)

@router.get("/", response_model=List[TeamSchema])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all teams.
    """
    teams = db.query(Team).offset(skip).limit(limit).all()
    return teams

@router.get("/{team_id}", response_model=TeamSchema)
def read_team(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific team by ID.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/{team_id}/roster", response_model=List[PlayerSchema])
def read_team_roster(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the roster (players) for a specific team.
    """
    players = db.query(Player).filter(Player.team_id == team_id).all()
    return players

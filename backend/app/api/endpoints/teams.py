from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.database import get_db
from app.core.error_decorators import handle_errors
from app.models.team import Team
from app.models.player import Player
from pydantic import BaseModel, ConfigDict

router = APIRouter()
logger = logging.getLogger(__name__)

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
@handle_errors
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all teams.
    """
    logger.info(f"Fetching teams (skip={skip}, limit={limit})")
    teams = db.query(Team).offset(skip).limit(limit).all()
    return teams

@router.get("/{team_id}", response_model=TeamSchema)
@handle_errors
def read_team(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific team by ID.
    """
    logger.info(f"Fetching team {team_id}")
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/{team_id}/roster", response_model=List[PlayerSchema])
@handle_errors
def read_team_roster(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the roster (players) for a specific team.
    """
    logger.info(f"Fetching roster for team {team_id}")
    players = db.query(Player).filter(Player.team_id == team_id).all()
    return players

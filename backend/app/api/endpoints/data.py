from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.game import Game
from app.models.team import Team
from app.models.player import Player

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/game-state/{game_id}")
def get_game_state(game_id: int, db: Session = Depends(get_db)):
    """Fetch the current state of a specific game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Use game_data for transient state not in columns
    state = game.game_data or {}
    
    # Determine possession string (home/away) from ID if available
    possession_id = state.get("possession_team_id")
    possession = "home" # Default
    if possession_id:
        if possession_id == game.away_team_id:
            possession = "away"
        elif possession_id == game.home_team_id:
            possession = "home"
    elif "possession" in state:
        possession = state["possession"]
    
    return {
        "game_id": game.id,
        "quarter": state.get("quarter", 1),
        "time_remaining": state.get("time_remaining", 900),
        "score": {"home": game.home_score, "away": game.away_score},
        "possession": possession,
        "down": state.get("down", 1),
        "distance": state.get("distance", 10),
        "yard_line": state.get("yard_line", 25)
    }


@router.get("/teams")
def get_teams(limit: Optional[int] = 32, db: Session = Depends(get_db)):
    """Fetch all teams in the simulation."""
    teams = db.query(Team).limit(limit).all()
    return {
        "teams": [
            {
                "id": t.id,
                "name": t.name,
                "city": t.city,
                "abbreviation": t.abbreviation,
                "conference": t.conference,
                "division": t.division,
                "wins": t.wins,
                "losses": t.losses,
                "ties": t.ties,
                "logo_url": t.logo_url,
                "primary_color": t.primary_color,
                "secondary_color": t.secondary_color
            } for t in teams
        ],
        "count": len(teams)
    }


@router.get("/players")
def get_players(team_id: Optional[int] = None, position: Optional[str] = None, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch players, optionally filtered by team or position."""
    query = db.query(Player)
    
    if team_id:
        query = query.filter(Player.team_id == team_id)
    if position:
        query = query.filter(Player.position == position)
        
    players = query.limit(limit).all()
    
    return {
        "players": [
            {
                "id": p.id,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "position": p.position,
                "team_id": p.team_id,
                "overall_rating": p.overall_rating,
                "jersey_number": p.jersey_number,
                "age": p.age,
                "height": p.height,
                "weight": p.weight,
                "experience": p.experience,
                "image_url": p.image_url
            } for p in players
        ],
        "count": len(players),
        "filters": {"team_id": team_id, "position": position}
    }


@router.get("/logs/{game_id}")
def get_game_logs(game_id: int, db: Session = Depends(get_db)):
    """Fetch play-by-play logs for a specific game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
        
    # Assuming logs are in game_data['plays'] or similar
    # If not, return empty list for now
    logs = (game.game_data or {}).get("plays", [])
    
    return {
        "game_id": game.id,
        "logs": logs,
        "count": len(logs)
    }

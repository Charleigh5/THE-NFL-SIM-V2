from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.models.season import Season, SeasonStatus
from app.models.game import Game
from app.models.team import Team
from app.services.schedule_generator import ScheduleGenerator
from app.services.standings_calculator import StandingsCalculator, TeamStanding
from app.services.week_simulator import WeekSimulator
from app.services.playoff_service import PlayoffService
from app.services.offseason_service import OffseasonService
from app.schemas.playoff import PlayoffMatchup as PlayoffMatchupSchema


router = APIRouter(prefix="/api/season", tags=["season"])


# Pydantic Schemas
class SeasonCreate(BaseModel):
    """Schema for creating a new season."""
    year: int
    start_date: Optional[str] = None  # ISO format date string
    total_weeks: int = 18
    playoff_weeks: int = 4


class SeasonResponse(BaseModel):
    """Schema for season response."""
    id: int
    year: int
    current_week: int
    is_active: bool
    status: str
    total_weeks: int
    playoff_weeks: int
    
    class Config:
        from_attributes = True


class GameResponse(BaseModel):
    """Schema for game response."""
    id: int
    week: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    is_played: bool
    date: datetime
    
    class Config:
        from_attributes = True


@router.post("/init", response_model=SeasonResponse)
def initialize_season(
    season_data: SeasonCreate,
    db: Session = Depends(get_db)
):
    """
    Initialize a new season.
    
    Creates a Season record and generates the full schedule.
    """
    # Check if season already exists
    existing = db.query(Season).filter(Season.year == season_data.year).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Season {season_data.year} already exists"
        )
    
    # Create season
    new_season = Season(
        year=season_data.year,
        current_week=1,
        is_active=True,
        status=SeasonStatus.REGULAR_SEASON,
        total_weeks=season_data.total_weeks,
        playoff_weeks=season_data.playoff_weeks
    )
    db.add(new_season)
    db.flush()  # Get the ID
    
    # Get all teams
    teams = db.query(Team).all()
    if len(teams) < 4:
        raise HTTPException(
            status_code=400,
            detail="Need at least 4 teams to generate a schedule"
        )
    
    # Generate schedule
    generator = ScheduleGenerator(db)
    
    start_date = None
    if season_data.start_date:
        start_date = datetime.fromisoformat(season_data.start_date)
    
    games = generator.generate_schedule(
        season_id=new_season.id,
        teams=teams,
        start_date=start_date
    )
    
    # Add games to database
    for game in games:
        db.add(game)
    
    db.commit()
    db.refresh(new_season)
    
    return new_season


@router.get("/current", response_model=SeasonResponse)
def get_current_season(db: Session = Depends(get_db)):
    """Get the currently active season."""
    season = db.query(Season).filter(Season.is_active == True).first()
    if not season:
        raise HTTPException(status_code=404, detail="No active season found")
    return season


@router.get("/{season_id}", response_model=SeasonResponse)
def get_season(season_id: int, db: Session = Depends(get_db)):
    """Get a specific season by ID."""
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.get("/{season_id}/schedule", response_model=List[GameResponse])
def get_schedule(
    season_id: int,
    week: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get the schedule for a season.
    
    Can optionally filter by week.
    """
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Build query
    query = db.query(Game).filter(Game.season_id == season_id)
    
    if week is not None:
        query = query.filter(Game.week == week)
    
    games = query.order_by(Game.week, Game.date).all()
    return games


@router.get("/{season_id}/standings", response_model=List[TeamStanding])
def get_standings(
    season_id: int,
    conference: Optional[str] = None,
    division: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get standings for a season.
    
    Can optionally filter by conference and/or division.
    """
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    calculator = StandingsCalculator(db)
    
    if division and conference:
        standings = calculator.get_division_standings(season_id, conference, division)
    elif conference:
        standings = calculator.get_conference_standings(season_id, conference)
    else:
        standings = calculator.calculate_standings(season_id)
    
    return standings


@router.post("/{season_id}/advance-week")
def advance_week(season_id: int, db: Session = Depends(get_db)):
    """Advance the season to the next week."""
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    if season.current_week >= season.total_weeks:
        # Move to playoffs or offseason
        if season.status == SeasonStatus.REGULAR_SEASON:
            season.status = SeasonStatus.POST_SEASON
            season.current_week = 1
        else:
            season.status = SeasonStatus.OFF_SEASON
    else:
        season.current_week += 1
    
    db.commit()
    db.refresh(season)
    
    return {
        "season_id": season.id,
        "current_week": season.current_week,
        "status": season.status,
        "message": f"Advanced to week {season.current_week}"
    }


@router.post("/{season_id}/simulate-week")
def simulate_week(
    season_id: int,
    week: Optional[int] = None,
    play_count: int = 100,
    db: Session = Depends(get_db)
):
    """
    Simulate all games in a week.
    
    Args:
        season_id: ID of the season
        week: Week to simulate (default: current week)
        play_count: Number of plays per game (default: 100)
    
    Returns:
        Results for all simulated games
    """
    # Verify season exists
    season = db.query(Season).filter(Season.id == season_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Use current week if not specified
    if week is None:
        week = season.current_week
    
    # Create simulator and run
    simulator = WeekSimulator(db)
    results = simulator.simulate_week(
        season_id=season_id,
        week=week,
        play_count=play_count,
        use_fast_sim=True
    )
    
    # Auto-advance to next week after simulating
    if week == season.current_week and season.current_week < season.total_weeks:
        season.current_week += 1
        db.commit()
    
    return results


@router.post("/{season_id}/playoffs/generate", response_model=List[PlayoffMatchupSchema])
def generate_playoffs(season_id: int, db: Session = Depends(get_db)):
    """Generate the playoff bracket for the season."""
    service = PlayoffService(db)
    try:
        return service.generate_playoffs(season_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{season_id}/playoffs/bracket", response_model=List[PlayoffMatchupSchema])
def get_playoff_bracket(season_id: int, db: Session = Depends(get_db)):
    """Get the current playoff bracket."""
    service = PlayoffService(db)
    return service.get_bracket(season_id)


@router.post("/{season_id}/playoffs/advance")
def advance_playoff_round(season_id: int, db: Session = Depends(get_db)):
    """Advance the playoff round if all games are complete."""
    service = PlayoffService(db)
    try:
        service.advance_round(season_id)
        return {"message": "Advanced playoff round"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{season_id}/offseason/start")
def start_offseason(season_id: int, db: Session = Depends(get_db)):
    """Start the offseason (process contracts, generate draft order)."""
    service = OffseasonService(db)
    try:
        return service.start_offseason(season_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{season_id}/draft/simulate")
def simulate_draft(season_id: int, db: Session = Depends(get_db)):
    """Simulate the rookie draft."""
    service = OffseasonService(db)
    return service.simulate_draft(season_id)


@router.post("/{season_id}/free-agency/simulate")
def simulate_free_agency(season_id: int, db: Session = Depends(get_db)):
    """Simulate free agency signings."""
    service = OffseasonService(db)
    return service.simulate_free_agency(season_id)

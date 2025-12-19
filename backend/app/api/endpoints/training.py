from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

from app.services.training.training_programs import (
    Drill,
    DrillCategory,
    SeasonPhase,
    TrainingProgramService,
    TrainingResult,
    WeeklySchedule,
    CoachingStyle
)

router = APIRouter()
training_service = TrainingProgramService()

class TrainingExecutionRequest(BaseModel):
    player_id: int
    drill_name: str
    coaching_style: str = "smart"
    season_phase: SeasonPhase = SeasonPhase.REGULAR
    player_age: int = 25

@router.get("/drills", response_model=dict)
def get_drills(
    position: str = "QB",
    season: SeasonPhase = SeasonPhase.REGULAR,
    category: Optional[DrillCategory] = None
):
    """Get available drills filtered by position, season phase, and category."""
    drills = training_service.get_available_drills(position, season)

    if category:
        drills = [d for d in drills if d.category == category]

    return {"drills": drills}

@router.get("/styles", response_model=List[CoachingStyle])
def get_coaching_styles():
    """Get all available coaching styles."""
    return [
        CoachingStyle(id="hardo", name="Hard-o", description="Max intensity, high injury risk, max XP", intensity_modifier=1.2, injury_risk_modifier=1.5),
        CoachingStyle(id="smart", name="Smart", description="Balanced approach, optimal for long seasons", intensity_modifier=1.0, injury_risk_modifier=1.0),
        CoachingStyle(id="soft", name="Soft", description="Low intensity, focuses on recovery", intensity_modifier=0.8, injury_risk_modifier=0.5),
    ]

@router.post("/execute", response_model=TrainingResult)
def execute_training(request: TrainingExecutionRequest):
    """Execute a training drill for a player."""
    # Lookup drill
    drills = training_service.get_available_drills("QB", request.season_phase) # TODO: Use real position
    drill = next((d for d in drills if d.name == request.drill_name), None)

    if not drill:
        raise HTTPException(status_code=404, detail=f"Drill '{request.drill_name}' not found")

    result = training_service.execute_training_session(
        player_id=request.player_id,
        drill=drill,
        season_phase=request.season_phase,
        coaching_style_id=request.coaching_style,
        player_age=request.player_age
    )
    return result

@router.get("/schedule", response_model=WeeklySchedule)
def get_schedule(
    position: str,
    season_phase: SeasonPhase = SeasonPhase.REGULAR,
    coaching_style: str = "smart"
):
    """Get the recommended weekly training schedule."""
    return training_service.generate_weekly_schedule(position, season_phase, coaching_style)

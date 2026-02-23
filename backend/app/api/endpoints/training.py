from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.training.drills import (
    Drill,
    DrillCategory,
    SeasonPhase,
    get_drills_for_position,
    get_drills_for_season,
)
from app.services.training.training_programs import (
    TrainingProgramsService,
    TrainingResult,
)

router = APIRouter()
training_service = TrainingProgramsService()


class WeeklySchedule(BaseModel):
    """Weekly training schedule recommendation."""

    position: str
    season_phase: str
    coaching_style: str
    recommended_drills: list[Drill] = Field(default_factory=list)
    total_sessions_per_week: int = 5
    notes: list[str] = Field(default_factory=list)


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
    category: DrillCategory | None = None,
):
    """Get available drills filtered by position, season phase, and category."""
    position_drills = get_drills_for_position(position)
    drills = get_drills_for_season(position_drills, season)

    if category:
        drills = [d for d in drills if d.category == category]

    return {"drills": [d.model_dump() for d in drills]}


@router.get("/styles", response_model=list[dict])
def get_coaching_styles():
    """Get all available coaching styles."""
    return [
        {
            "id": "volume",
            "name": "Volume Training",
            "description": "High repetition approach with lower injury risk",
            "intensity_modifier": 0.9,
            "injury_risk_modifier": 0.7,
        },
        {
            "id": "intensity",
            "name": "High Intensity",
            "description": "Maximum effort with significant injury risk",
            "intensity_modifier": 1.5,
            "injury_risk_modifier": 2.0,
        },
        {
            "id": "smart",
            "name": "Smart Training",
            "description": "Analytics-driven balanced approach",
            "intensity_modifier": 1.1,
            "injury_risk_modifier": 0.8,
        },
        {
            "id": "old_school",
            "name": "Old School",
            "description": "Traditional grit-focused training",
            "intensity_modifier": 1.2,
            "injury_risk_modifier": 1.5,
        },
    ]


@router.post("/execute", response_model=TrainingResult)
def execute_training(request: TrainingExecutionRequest):
    """Execute a training drill for a player."""
    # Lookup drill
    position_drills = get_drills_for_position("QB")  # TODO: Use real position
    drills = get_drills_for_season(position_drills, request.season_phase)
    drill = next((d for d in drills if d.name == request.drill_name), None)

    if not drill:
        raise HTTPException(status_code=404, detail=f"Drill '{request.drill_name}' not found")

    # Note: This is a simplified implementation
    # Full implementation would require player data from database
    result = TrainingResult(
        xp_gains={drill.target_stat: 50.0}, session_grade="B", notes=[f"Completed {drill.name}"]
    )
    return result


@router.get("/schedule", response_model=WeeklySchedule)
def get_schedule(
    position: str, season_phase: SeasonPhase = SeasonPhase.REGULAR, coaching_style: str = "smart"
):
    """Get the recommended weekly training schedule."""
    position_drills = get_drills_for_position(position)
    season_drills = get_drills_for_season(position_drills, season_phase)

    # Recommend top 5 drills
    recommended = season_drills[:5]

    return WeeklySchedule(
        position=position,
        season_phase=season_phase.value,
        coaching_style=coaching_style,
        recommended_drills=recommended,
        total_sessions_per_week=5,
        notes=[f"Recommended {len(recommended)} drills for {position} in {season_phase.value}"],
    )

#!/usr/bin/env python3
"""
Training API Endpoints
======================
REST endpoints for the Training System, consolidating drill catalogues,
coaching philosophy styles, session execution, and weekly schedule generation.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.services.training.drills import (
    Drill,
    DrillCategory,
    SeasonPhase,
    ALL_DRILLS,
    POSITION_DRILL_MAP,
    get_drills_for_position,
    get_drills_for_season,
    get_drills_by_category,
)
from app.services.training.coaching_philosophy import (
    CoachingStyle,
    COACHING_STYLES,
    get_coaching_style,
    get_seasonal_intensity_cap,
)
from app.services.training.training_programs import (
    TrainingProgramsService,
    TrainingResult,
)
from app.kernels.rpg.training import TrainingEngine

router = APIRouter()
training_service = TrainingProgramsService()


# ============================================================================
# SCHEMAS
# ============================================================================

class DrillResponse(BaseModel):
    """Response model for a single drill."""
    name: str
    target_stat: str
    secondary_stats: List[str]
    injury_risk: float
    xp_multiplier: float
    fatigue_cost: float
    category: str
    description: str
    season_filter: List[str]


class DrillListResponse(BaseModel):
    """Response for drill list endpoint."""
    drills: List[Dict[str, Any]]
    total: int
    position_filter: Optional[str] = None
    season_filter: Optional[str] = None
    category_filter: Optional[str] = None


class TrainingExecutionRequest(BaseModel):
    """Request to execute a training session."""
    player_id: int = Field(..., description="Player ID to train")
    drill_name: str = Field(..., description="Name of the drill to execute")
    coaching_style: str = Field("smart", description="Coaching style (volume, intensity, smart, old_school)")
    season_phase: SeasonPhase = Field(SeasonPhase.REGULAR, description="Current season phase")
    player_age: int = Field(25, ge=18, le=50, description="Player's age")


class WeeklySchedule(BaseModel):
    """Weekly training schedule recommendation."""
    position: str
    season_phase: str
    coaching_style: str
    recommended_drills: List[Drill] = Field(default_factory=list)
    total_sessions_per_week: int = 5
    seasonal_intensity_cap: Optional[float] = 1.0
    notes: List[str] = Field(default_factory=list)


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/drills", response_model=dict)
def get_drills(
    position: Optional[str] = Query(None, description="Filter by position (e.g. QB, WR)"),
    season: Optional[SeasonPhase] = Query(None, description="Filter by season phase"),
    category: Optional[DrillCategory] = Query(None, description="Filter by category"),
):
    """Get available drills filtered by position, season phase, and category."""
    drills = ALL_DRILLS

    if position:
        pos_drills = get_drills_for_position(position.upper())
        if pos_drills:
            drills = pos_drills

    if season:
        drills = get_drills_for_season(drills, season)

    if category:
        drills = [d for d in drills if d.category == category]

    serialized_drills = [
        d.model_dump() if hasattr(d, "model_dump") else d.__dict__
        for d in drills
    ]
    return {
        "drills": serialized_drills,
        "total": len(serialized_drills),
        "position_filter": position,
        "season_filter": season.value if season else None,
        "category_filter": category.value if category else None,
    }


@router.get("/styles", response_model=List[dict])
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
    """Execute a training drill for a player using the RPG TrainingEngine."""
    drill = next((d for d in ALL_DRILLS if d.name.lower() == request.drill_name.lower()), None)
    if not drill:
        raise HTTPException(status_code=404, detail=f"Drill '{request.drill_name}' not found")

    try:
        coaching_style = get_coaching_style(request.coaching_style)
    except Exception:
        coaching_style = None

    engine = TrainingEngine()
    engine_result = engine.train_with_drill(
        drill=drill,
        player_age=request.player_age,
        coaching_style=coaching_style,
        season_phase=request.season_phase.value if hasattr(request.season_phase, "value") else str(request.season_phase),
    )

    grade = "A" if engine_result.get("xp_gained", 0) >= 40 else "B" if engine_result.get("xp_gained", 0) >= 20 else "C"
    injury_note = " (Injury occurred during session!)" if engine_result.get("injury_occurred") else ""

    return TrainingResult(
        xp_gains={drill.target_stat: float(engine_result.get("xp_gained", 50.0))},
        session_grade=grade,
        notes=[f"Completed {drill.name}{injury_note}"]
    )


@router.get("/schedule", response_model=WeeklySchedule)
def get_schedule(
    position: str = "QB",
    season_phase: SeasonPhase = SeasonPhase.REGULAR,
    coaching_style: str = "smart"
):
    """Get the recommended weekly training schedule."""
    position_drills = get_drills_for_position(position.upper())
    if not position_drills:
        position_drills = get_drills_for_position("QB")

    season_drills = get_drills_for_season(position_drills, season_phase)
    recommended = season_drills[:5]

    try:
        cap = get_seasonal_intensity_cap(season_phase.value)
    except Exception:
        cap = 1.0

    return WeeklySchedule(
        position=position,
        season_phase=season_phase.value,
        coaching_style=coaching_style,
        recommended_drills=recommended,
        total_sessions_per_week=5,
        seasonal_intensity_cap=cap,
        notes=[f"Recommended {len(recommended)} drills for {position} in {season_phase.value}"]
    )

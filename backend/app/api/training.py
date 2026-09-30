#!/usr/bin/env python3
"""
Training API Router (B-033)
===========================
REST endpoints for the Training System.

Endpoints:
- GET /training/drills - List available drills (B-034)
- POST /training/execute - Execute a training session (B-035)
- GET /training/schedule - Get recommended schedule (B-036)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from app.services.training.drills import (
    Drill,
    SeasonPhase,
    DrillCategory,
    ALL_DRILLS,
    POSITION_DRILL_MAP,
    get_drills_for_position,
    get_drills_for_season,
    get_drills_by_category,
)
from app.services.training.coaching_philosophy import (
    CoachingStyle,
    CoachingStyleName,
    COACHING_STYLES,
    get_coaching_style,
    get_seasonal_intensity_cap,
)
from app.kernels.rpg.training import TrainingEngine

router = APIRouter(prefix="/training", tags=["Training"])


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
    drills: List[DrillResponse]
    total: int
    position_filter: Optional[str] = None
    season_filter: Optional[str] = None
    category_filter: Optional[str] = None


class ExecuteTrainingRequest(BaseModel):
    """Request to execute a training session."""
    player_id: int = Field(..., description="Player ID to train")
    drill_name: str = Field(..., description="Name of the drill to execute")
    coaching_style: Optional[str] = Field(None, description="Coaching style to use")
    season_phase: str = Field("regular", description="Current season phase")
    player_age: int = Field(25, ge=18, le=50, description="Player's age")


class ExecuteTrainingResponse(BaseModel):
    """Response from training execution."""
    player_id: int
    drill_name: str
    xp_gained: float
    target_stat: str
    secondary_stats: List[str]
    injury_occurred: bool
    fatigue_added: float
    final_injury_risk: float
    weekly_load: float
    coaching_style_used: Optional[str] = None


class ScheduleRecommendation(BaseModel):
    """Recommended training schedule."""
    day: str
    drill_name: str
    intensity: str
    notes: str


class ScheduleResponse(BaseModel):
    """Response for schedule recommendation."""
    position: str
    season_phase: str
    coaching_style: str
    recommendations: List[ScheduleRecommendation]
    seasonal_intensity_cap: float


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/drills", response_model=DrillListResponse)
async def get_drills(
    position: Optional[str] = Query(None, description="Filter by position (e.g., QB, WR)"),
    season: Optional[str] = Query(None, description="Filter by season phase"),
    category: Optional[str] = Query(None, description="Filter by drill category"),
) -> DrillListResponse:
    """
    B-034: Get available training drills.

    Returns a list of drills with optional filtering by position, season, or category.
    """
    drills = ALL_DRILLS

    # Filter by position
    if position:
        drills = get_drills_for_position(position.upper())
        if not drills:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown position: {position}. Valid positions: {list(POSITION_DRILL_MAP.keys())}"
            )

    # Filter by season
    if season:
        try:
            season_enum = SeasonPhase(season.lower())
            drills = get_drills_for_season(drills, season_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown season phase: {season}. Valid phases: {[s.value for s in SeasonPhase]}"
            )

    # Filter by category
    if category:
        try:
            category_enum = DrillCategory(category.upper())
            drills = get_drills_by_category(drills, category_enum)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown category: {category}. Valid categories: {[c.value for c in DrillCategory]}"
            )

    # Convert to response format
    drill_responses = [
        DrillResponse(
            name=d.name,
            target_stat=d.target_stat,
            secondary_stats=d.secondary_stats,
            injury_risk=d.injury_risk,
            xp_multiplier=d.xp_multiplier,
            fatigue_cost=d.fatigue_cost,
            category=d.category if isinstance(d.category, str) else d.category.value,
            description=d.description,
            season_filter=[s if isinstance(s, str) else s.value for s in d.season_filter],
        )
        for d in drills
    ]

    return DrillListResponse(
        drills=drill_responses,
        total=len(drill_responses),
        position_filter=position,
        season_filter=season,
        category_filter=category,
    )


@router.post("/execute", response_model=ExecuteTrainingResponse)
async def execute_training(request: ExecuteTrainingRequest) -> ExecuteTrainingResponse:
    """
    B-035: Execute a training session for a player.

    Applies the selected drill with coaching style modifiers and returns results.
    """
    # Find the drill by name
    drill = None
    for d in ALL_DRILLS:
        if d.name.lower() == request.drill_name.lower():
            drill = d
            break

    if not drill:
        raise HTTPException(
            status_code=404,
            detail=f"Drill not found: {request.drill_name}"
        )

    # Get coaching style if specified
    coaching_style = None
    if request.coaching_style:
        try:
            coaching_style = get_coaching_style(request.coaching_style)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Create training engine and execute
    engine = TrainingEngine()
    result = engine.train_with_drill(
        drill=drill,
        player_age=request.player_age,
        coaching_style=coaching_style,
        season_phase=request.season_phase,
    )

    return ExecuteTrainingResponse(
        player_id=request.player_id,
        drill_name=drill.name,
        xp_gained=result["xp_gained"],
        target_stat=result["target_stat"],
        secondary_stats=result["secondary_stats"],
        injury_occurred=result["injury_occurred"],
        fatigue_added=result["fatigue_added"],
        final_injury_risk=result["final_injury_risk"],
        weekly_load=result["weekly_load"],
        coaching_style_used=request.coaching_style,
    )


@router.get("/schedule", response_model=ScheduleResponse)
async def get_training_schedule(
    position: str = Query(..., description="Player position"),
    season_phase: str = Query("regular", description="Season phase"),
    coaching_style: str = Query("smart", description="Coaching philosophy"),
) -> ScheduleResponse:
    """
    B-036: Get recommended weekly training schedule.

    Returns a 7-day training plan based on position, season, and coaching style.
    """
    # Validate inputs
    position_drills = get_drills_for_position(position.upper())
    if not position_drills:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown position: {position}"
        )

    try:
        style = get_coaching_style(coaching_style)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    seasonal_cap = get_seasonal_intensity_cap(season_phase)

    # Build weekly recommendations
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    recommendations = []

    for i, day in enumerate(days):
        if day == "Sunday":
            # Game day
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name="Game Day",
                intensity="game",
                notes="Rest and prepare for game"
            ))
        elif day == "Monday":
            # Recovery
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name="Recovery/Film Study",
                intensity="rest",
                notes="Focus on mental reps and recovery"
            ))
        elif day in ["Tuesday", "Saturday"]:
            # Light days
            mental_drills = [d for d in position_drills if d.category == DrillCategory.MENTAL]
            drill = mental_drills[0] if mental_drills else position_drills[0]
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name=drill.name,
                intensity="light",
                notes="Mental preparation and light technique work"
            ))
        elif day == "Wednesday":
            # Heavy day (if season allows)
            intensity = "heavy" if seasonal_cap >= 0.7 else "moderate"
            technique_drills = [d for d in position_drills if d.category == DrillCategory.TECHNIQUE]
            drill = technique_drills[0] if technique_drills else position_drills[0]
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name=drill.name,
                intensity=intensity,
                notes="Full practice - technique focus"
            ))
        elif day == "Thursday":
            # Moderate day
            drill = position_drills[len(position_drills) // 2]  # Pick a middle drill
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name=drill.name,
                intensity="moderate",
                notes="Situational work and refinement"
            ))
        elif day == "Friday":
            # Walkthrough
            recommendations.append(ScheduleRecommendation(
                day=day,
                drill_name="Walkthrough",
                intensity="light",
                notes="Light walkthrough and mental prep"
            ))

    return ScheduleResponse(
        position=position.upper(),
        season_phase=season_phase,
        coaching_style=style.name if isinstance(style.name, str) else style.name.value,
        recommendations=recommendations,
        seasonal_intensity_cap=seasonal_cap,
    )


@router.get("/styles", response_model=List[dict])
async def get_coaching_styles() -> List[dict]:
    """Get available coaching styles and their properties."""
    return [
        {
            "name": style.name if isinstance(style.name, str) else style.name.value,
            "display_name": style.display_name,
            "description": style.description,
            "xp_multiplier": style.xp_multiplier,
            "injury_risk_multiplier": style.injury_risk_multiplier,
            "fatigue_multiplier": style.fatigue_multiplier,
            "recovery_multiplier": style.recovery_multiplier,
        }
        for style in COACHING_STYLES.values()
    ]

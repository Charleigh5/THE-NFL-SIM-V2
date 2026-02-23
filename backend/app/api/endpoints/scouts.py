#!/usr/bin/env python3
"""
Scouting API Endpoints
======================
REST API for scouting operations including scout assignment,
report retrieval, and draft prospect evaluation.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.scouting.scouting_service import ScoutingService

router = APIRouter(prefix="/api/scouting", tags=["scouting"])

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class ScoutAssignmentRequest(BaseModel):
    """Request to assign a scout to a prospect."""

    scout_id: int
    prospect_id: int


class ScoutAssignmentResponse(BaseModel):
    """Response from scout assignment."""

    success: bool
    message: str


class ScoutingReportResponse(BaseModel):
    """Scouting report with fog-of-war applied."""

    prospect_id: str
    completion: float
    attributes: dict[str, Any]
    strengths: list[str] = []
    weaknesses: list[str] = []


class ScoutInfo(BaseModel):
    """Scout personnel information."""

    scout_id: int
    name: str
    region: str
    specialty: str
    bias: str
    efficiency: int
    accuracy: int


class TeamScoutsResponse(BaseModel):
    """List of team's scouts."""

    team_id: int
    scouts: list[ScoutInfo]


# ============================================================================
# ENDPOINTS
# ============================================================================

# Service instance (in production, use dependency injection)
_scouting_service: ScoutingService | None = None


def get_scouting_service(db: Session = Depends(get_db)) -> ScoutingService:
    """Dependency to get scouting service."""
    global _scouting_service
    # Always create new instance to ensure fresh DB session if needed,
    # or rely on the db session passed in.
    return ScoutingService(db)


@router.get("/scouts/{team_id}", response_model=TeamScoutsResponse)
async def get_team_scouts(team_id: int, service: ScoutingService = Depends(get_scouting_service)):
    """
    Get all scouts for a team.
    """
    db_scouts = service.get_team_scouts(team_id)

    scouts = [
        ScoutInfo(
            scout_id=s.id,
            name=s.name,
            region=s.region or "NATIONAL",
            specialty=s.position_specialty or "GENERALIST",
            bias=s.bias or "NEUTRAL",
            efficiency=s.efficiency,
            accuracy=s.evaluation_ability,
        )
        for s in db_scouts
    ]

    return TeamScoutsResponse(team_id=team_id, scouts=scouts)


@router.post("/assign/{team_id}", response_model=ScoutAssignmentResponse)
async def assign_scout(
    team_id: int,
    request: ScoutAssignmentRequest,
    service: ScoutingService = Depends(get_scouting_service),
):
    """
    Assign a scout to evaluate a prospect.
    """
    success = service.assign_scout(
        team_id=team_id, scout_id=request.scout_id, prospect_id=request.prospect_id
    )

    if not success:
        raise HTTPException(status_code=400, detail="Assignment failed. Verify IDs.")

    return ScoutAssignmentResponse(
        success=True, message=f"Scout {request.scout_id} assigned to Prospect {request.prospect_id}"
    )


@router.get("/report/{team_id}/{prospect_id}", response_model=ScoutingReportResponse)
async def get_scouting_report(
    team_id: int, prospect_id: int, service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get scouting report for a prospect.
    """
    # Fetch report using engine/service
    engine_report = service.generate_report(team_id, prospect_id)

    if not engine_report:
        # If no report, return empty/unknown structure
        return ScoutingReportResponse(
            prospect_id=str(prospect_id), completion=0.0, attributes={}, strengths=[], weaknesses=[]
        )

    # Format for API response
    display_attrs = service.get_formatted_report(team_id, prospect_id)

    return ScoutingReportResponse(
        prospect_id=str(prospect_id),
        completion=engine_report.completion_percentage,
        attributes=display_attrs,
        strengths=engine_report.strengths,
        weaknesses=engine_report.weaknesses,
    )

#!/usr/bin/env python3
"""
Scouting API Endpoints
======================
REST API for scouting operations including scout assignment,
report retrieval, and draft prospect evaluation.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any
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
    scout_id: str
    prospect_id: str


class ScoutAssignmentResponse(BaseModel):
    """Response from scout assignment."""
    success: bool
    scout_id: str
    prospect_id: str
    visits: int
    message: str


class ScoutingReportResponse(BaseModel):
    """Scouting report with fog-of-war applied."""
    prospect_id: str
    scouted: bool
    completion: float
    attributes: Dict[str, Any]
    strengths: List[str] = []
    weaknesses: List[str] = []
    message: Optional[str] = None


class ScoutInfo(BaseModel):
    """Scout personnel information."""
    scout_id: str
    name: str
    region: str
    specialty: str
    efficiency: int
    accuracy: int


class TeamScoutsResponse(BaseModel):
    """List of team's scouts."""
    team_id: int
    scouts: List[ScoutInfo]
    budget_remaining: int


# ============================================================================
# ENDPOINTS
# ============================================================================

# Service instance (in production, use dependency injection)
_scouting_service: Optional[ScoutingService] = None

def get_scouting_service(db: Session = Depends(get_db)) -> ScoutingService:
    """Dependency to get scouting service."""
    global _scouting_service
    if _scouting_service is None:
        _scouting_service = ScoutingService(db)
    return _scouting_service


@router.get("/scouts/{team_id}", response_model=TeamScoutsResponse)
async def get_team_scouts(
    team_id: int,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get all scouts for a team.

    Returns list of scout personnel with their attributes.
    """
    state = service.get_team_state(team_id)

    scouts = [
        ScoutInfo(
            scout_id=s.scout_id,
            name=s.name,
            region=s.region.value,
            specialty=s.specialty.value,
            efficiency=s.efficiency,
            accuracy=s.accuracy
        )
        for s in state.scouts.values()
    ]

    return TeamScoutsResponse(
        team_id=team_id,
        scouts=scouts,
        budget_remaining=state.budget_remaining
    )


@router.post("/assign/{team_id}", response_model=ScoutAssignmentResponse)
async def assign_scout(
    team_id: int,
    request: ScoutAssignmentRequest,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Assign a scout to evaluate a prospect.

    Multiple assignments to the same prospect increase visit count.
    """
    assignment = service.assign_scout(
        team_id=team_id,
        scout_id=request.scout_id,
        prospect_id=request.prospect_id
    )

    if not assignment:
        raise HTTPException(
            status_code=400,
            detail=f"Scout {request.scout_id} not found for team {team_id}"
        )

    return ScoutAssignmentResponse(
        success=True,
        scout_id=assignment.scout_id,
        prospect_id=assignment.prospect_id,
        visits=assignment.visits,
        message=f"Scout assigned with {assignment.visits} visit(s)"
    )


@router.get("/report/{team_id}/{prospect_id}", response_model=ScoutingReportResponse)
async def get_scouting_report(
    team_id: int,
    prospect_id: str,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get scouting report for a prospect.

    Returns fog-of-war applied attributes based on scouting progress.
    Unassigned prospects will show minimal information.
    """
    # In real implementation, we'd fetch true attributes from DB
    # For now, using placeholder
    # TODO: Integrate with actual prospect data
    true_attributes = {
        "speed": 85,
        "strength": 78,
        "agility": 82,
        "throw_power": 90,
        "accuracy": 88,
        "awareness": 75,
    }

    fog_result = service.apply_fog_of_war(
        team_id=team_id,
        prospect_id=prospect_id,
        true_attributes=true_attributes
    )

    return ScoutingReportResponse(
        prospect_id=prospect_id,
        scouted=fog_result.get("scouted", False),
        completion=fog_result.get("completion", 0),
        attributes=fog_result.get("attributes", {}),
        strengths=fog_result.get("strengths", []),
        weaknesses=fog_result.get("weaknesses", []),
        message=fog_result.get("message")
    )


@router.get("/reports/{team_id}")
async def get_all_reports(
    team_id: int,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get all scouting reports for a team.

    Returns summary of all prospects that have been scouted.
    """
    reports = service.get_all_reports(team_id)

    return {
        "team_id": team_id,
        "total_reports": len(reports),
        "reports": [
            {
                "prospect_id": r.player_id,
                "scout_id": r.scout_id,
                "completion": r.completion_percentage,
            }
            for r in reports
        ]
    }


@router.get("/draft-board/{team_id}")
async def get_draft_board_with_fog(
    team_id: int,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get draft board with fog-of-war applied to all prospects.

    This is meant to integrate with the Draft Assistant to show
    which prospects have been scouted and their revealed attributes.
    """
    state = service.get_team_state(team_id)

    # Get all prospects team has scouted
    scouted_prospects = set()
    for assignment in state.assignments.values():
        scouted_prospects.add(assignment.prospect_id)

    return {
        "team_id": team_id,
        "scouted_count": len(scouted_prospects),
        "scouted_prospects": list(scouted_prospects),
        "scouts_available": len(state.scouts),
        "budget_remaining": state.budget_remaining
    }

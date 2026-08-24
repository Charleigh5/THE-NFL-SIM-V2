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
from app.services.draft.scouting_lens_service import scouting_lens_service
from app.schemas.deep_dive import (
    ProspectIntelligence,
    DraftTradeUrgency,
    ScoutBiasLens,
)

router = APIRouter(prefix="/api/scouting", tags=["scouting"])
scouts_router = APIRouter(prefix="/api/scouts", tags=["scouts"])

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
    attributes: Dict[str, Any]
    strengths: List[str] = []
    weaknesses: List[str] = []

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
    scouts: List[ScoutInfo]

# ============================================================================
# ENDPOINTS
# ============================================================================

# Service instance (in production, use dependency injection)
_scouting_service: Optional[ScoutingService] = None

def get_scouting_service(db: Session = Depends(get_db)) -> ScoutingService:
    """Dependency to get scouting service."""
    global _scouting_service
    # Always create new instance to ensure fresh DB session if needed,
    # or rely on the db session passed in.
    return ScoutingService(db)

@router.get("/scouts/{team_id}", response_model=TeamScoutsResponse)
async def get_team_scouts(
    team_id: int,
    service: ScoutingService = Depends(get_scouting_service)
):
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
            accuracy=s.evaluation_ability
        )
        for s in db_scouts
    ]

    return TeamScoutsResponse(
        team_id=team_id,
        scouts=scouts
    )

@router.post("/assign/{team_id}", response_model=ScoutAssignmentResponse)
async def assign_scout(
    team_id: int,
    request: ScoutAssignmentRequest,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Assign a scout to evaluate a prospect.
    """
    success = service.assign_scout(
        team_id=team_id,
        scout_id=request.scout_id,
        prospect_id=request.prospect_id
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Assignment failed. Verify IDs."
        )

    return ScoutAssignmentResponse(
        success=True,
        message=f"Scout {request.scout_id} assigned to Prospect {request.prospect_id}"
    )

@router.get("/report/{team_id}/{prospect_id}", response_model=ScoutingReportResponse)
async def get_scouting_report(
    team_id: int,
    prospect_id: int,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get scouting report for a prospect.
    """
    # Fetch report using engine/service
    engine_report = service.generate_report(team_id, prospect_id)

    if not engine_report:
        # If no report, return empty/unknown structure
        return ScoutingReportResponse(
            prospect_id=str(prospect_id),
            completion=0.0,
            attributes={},
            strengths=[],
            weaknesses=[]
        )

    # Format for API response
    display_attrs = service.get_formatted_report(team_id, prospect_id)

    return ScoutingReportResponse(
        prospect_id=str(prospect_id),
        completion=engine_report.completion_percentage,
        attributes=display_attrs,
        strengths=engine_report.strengths,
        weaknesses=engine_report.weaknesses
    )


@router.get("/report/{prospect_id}", response_model=ScoutingReportResponse)
async def get_scouting_report_single(
    prospect_id: int,
    team_id: Optional[int] = 1,
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get scouting report for a prospect (alias with optional team_id).
    """
    return await get_scouting_report(team_id=team_id or 1, prospect_id=prospect_id, service=service)


# ============================================================================
# MULTI-LENS PROSPECT INTELLIGENCE & DRAFT TRADE URGENCY ENDPOINTS
# ============================================================================

@router.get("/prospects/{prospect_id}/intelligence", response_model=ProspectIntelligence)
async def get_prospect_intelligence(
    prospect_id: int,
    db: Session = Depends(get_db)
):
    """
    Evaluate draft prospect through 4 distinct front-office scouting lenses:
    Consensus, Film Traditionalist, Analytics Department, and Regional Scout.
    """
    from app.models.player import Player

    player = db.query(Player).filter(Player.id == prospect_id).first()
    if player:
        name = f"{player.first_name} {player.last_name}"
        position = player.position.value if hasattr(player.position, 'value') else str(player.position)
        college = getattr(player, 'college', None) or "USC"
        true_ovr = player.overall_rating or 78
        s2_score = int(getattr(player, 's2_cognition', None) or (70 + (true_ovr % 25)))
        speed = float(getattr(player, 'speed', None) or 85.0)
        gps_speed_max = 18.0 + (speed / 100.0) * 4.5
        burst_score = float(getattr(player, 'acceleration', None) or 80.0)
        scheme_fit_pct = 85
    else:
        name = f"Draft Prospect #{prospect_id}"
        position = "QB"
        college = "USC"
        true_ovr = 80
        s2_score = 88
        gps_speed_max = 21.2
        burst_score = 84.0
        scheme_fit_pct = 85

    return scouting_lens_service.evaluate_prospect(
        prospect_id=prospect_id,
        name=name,
        position=position,
        college=college,
        true_ovr=true_ovr,
        s2_score=s2_score,
        gps_speed_max=gps_speed_max,
        burst_score=burst_score,
        scheme_fit_pct=scheme_fit_pct,
    )


@router.get("/trade-urgency/{team_id}", response_model=DraftTradeUrgency)
async def get_draft_trade_urgency(
    team_id: str,
    target_position: str = "QB",
    roster_need_score: float = 0.85,
    remaining_in_tier: int = 2,
    current_pick: int = 5,
):
    """
    Calculate dynamic draft trade-up urgency and package valuation using Jimmy Johnson chart curves.
    """
    return scouting_lens_service.calculate_trade_urgency(
        team_id=str(team_id),
        target_position=target_position,
        roster_need_score=roster_need_score,
        remaining_in_tier=remaining_in_tier,
        current_pick=current_pick,
    )


# ============================================================================
# MIRROR ON /api/scouts FOR URL ROUTE COMPLIANCE
# ============================================================================

@scouts_router.get("/scouts/{team_id}", response_model=TeamScoutsResponse)
async def scouts_alias_get_team_scouts(team_id: int, service: ScoutingService = Depends(get_scouting_service)):
    return await get_team_scouts(team_id=team_id, service=service)

@scouts_router.post("/assign/{team_id}", response_model=ScoutAssignmentResponse)
async def scouts_alias_assign_scout(team_id: int, request: ScoutAssignmentRequest, service: ScoutingService = Depends(get_scouting_service)):
    return await assign_scout(team_id=team_id, request=request, service=service)

@scouts_router.get("/report/{team_id}/{prospect_id}", response_model=ScoutingReportResponse)
async def scouts_alias_get_scouting_report(team_id: int, prospect_id: int, service: ScoutingService = Depends(get_scouting_service)):
    return await get_scouting_report(team_id=team_id, prospect_id=prospect_id, service=service)

@scouts_router.get("/report/{prospect_id}", response_model=ScoutingReportResponse)
async def scouts_alias_get_scouting_report_single(prospect_id: int, team_id: Optional[int] = 1, service: ScoutingService = Depends(get_scouting_service)):
    return await get_scouting_report_single(prospect_id=prospect_id, team_id=team_id, service=service)

@scouts_router.get("/prospects/{prospect_id}/intelligence", response_model=ProspectIntelligence)
async def scouts_alias_get_prospect_intelligence(prospect_id: int, db: Session = Depends(get_db)):
    return await get_prospect_intelligence(prospect_id=prospect_id, db=db)

@scouts_router.get("/trade-urgency/{team_id}", response_model=DraftTradeUrgency)
async def scouts_alias_get_draft_trade_urgency(team_id: str, target_position: str = "QB", roster_need_score: float = 0.85, remaining_in_tier: int = 2, current_pick: int = 5):
    return await get_draft_trade_urgency(team_id=team_id, target_position=target_position, roster_need_score=roster_need_score, remaining_in_tier=remaining_in_tier, current_pick=current_pick)


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
    db: Session = Depends(get_db),
    service: ScoutingService = Depends(get_scouting_service)
):
    """
    Get scouting report for a prospect.

    Returns fog-of-war applied attributes based on scouting progress.
    Unassigned prospects will show minimal information.
    """
    # Fetch real player attributes from database
    from app.models.player import Player
    player = db.query(Player).filter(Player.id == int(prospect_id)).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail=f"Prospect {prospect_id} not found"
        )

    true_attributes = {
        "speed": player.speed,
        "strength": player.strength,
        "agility": player.agility,
        "throw_power": player.throw_power,
        "accuracy": player.throw_accuracy_mid,
        "awareness": player.awareness,
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


# ============================================================================
# AI-POWERED SCOUTING ENDPOINTS
# ============================================================================

from app.schemas.scouting import (  # type: ignore[import-not-found]
    ScoutingReportAI,
    PlayerBackstory,
    ScoutingReportRequest,
    ScoutingReportResponse as AIScoutingReportResponse,
    BatchScoutingRequest,
    BatchScoutingResponse
)
from app.services.ai.scouting_ai import get_scouting_ai_service  # type: ignore[import-not-found]
from datetime import datetime


@router.get("/ai-report/{player_id}", response_model=AIScoutingReportResponse)
async def get_ai_scouting_report(
    player_id: int,
    team_id: Optional[int] = None,
    include_backstory: bool = False,
    db: Session = Depends(get_db)
):
    """
    Generate an AI-powered scouting report for a player.

    Uses Gemini 2.5 Pro to create detailed, position-specific analysis
    with NFL comparisons and draft grade recommendations.

    Args:
        player_id: The player to scout
        team_id: Optional team ID to tailor fit analysis
        include_backstory: Also generate biographical backstory

    Returns:
        AI-generated scouting report with optional backstory
    """
    from app.models.player import Player

    # Fetch player from database
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    # Get team needs if team_id provided
    team_needs = None
    if team_id:
        from app.services.offseason_service import OffseasonService
        offseason_svc = OffseasonService(db)
        needs_list = offseason_svc.get_team_needs(team_id)
        # Extract top 5 positional needs as list of position strings
        team_needs = [need.position for need in needs_list[:5] if need.need_score > 0]

    # Build attributes dict from player
    attributes = {
        "speed": player.speed,
        "strength": player.strength,
        "agility": player.agility,
        "awareness": player.awareness,
        "throw_power": player.throw_power,
        "throw_accuracy_mid": player.throw_accuracy_mid,
        "route_running": player.route_running,
        "catching": player.catching,
        "pass_block": player.pass_block,
        "run_block": player.run_block,
        "tackle": player.tackle,
        "man_coverage": player.man_coverage,
        "zone_coverage": player.zone_coverage,
        "pass_rush_power": player.pass_rush_power,
    }

    # Generate AI report
    ai_service = get_scouting_ai_service()
    report = await ai_service.generate_scouting_report(
        player_name=f"{player.first_name} {player.last_name}",
        position=player.position,
        overall_rating=player.overall_rating,
        college=player.college,
        attributes=attributes,
        team_needs=team_needs
    )

    # Optionally generate backstory
    backstory = None
    if include_backstory:
        backstory = await ai_service.generate_backstory(
            player_name=f"{player.first_name} {player.last_name}",
            position=player.position,
            college=player.college
        )

    return AIScoutingReportResponse(
        player_id=player_id,
        player_name=f"{player.first_name} {player.last_name}",
        position=player.position,
        overall_rating=player.overall_rating,
        report=report,
        backstory=backstory,
        generated_at=datetime.utcnow().isoformat(),
        cached=False
    )


@router.get("/backstory/{player_id}", response_model=PlayerBackstory)
async def get_player_backstory(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate an AI-powered biographical backstory for a player.

    Creates compelling narrative including hometown, personality,
    motivations, and career highlights.
    """
    from app.models.player import Player

    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    ai_service = get_scouting_ai_service()
    return await ai_service.generate_backstory(
        player_name=f"{player.first_name} {player.last_name}",
        position=player.position,
        college=player.college
    )


@router.post("/batch", response_model=BatchScoutingResponse)
async def batch_generate_scouting_reports(
    request: BatchScoutingRequest,
    db: Session = Depends(get_db)
):
    """
    Batch generate AI-powered scouting reports for multiple players.

    Generates reports concurrently for improved performance.
    Returns counts of successful and failed generations.

    Args:
        request: BatchScoutingRequest with list of player_ids and optional team_id

    Returns:
        BatchScoutingResponse with success/failure counts and ID lists
    """
    import asyncio
    from app.models.player import Player

    ai_service = get_scouting_ai_service()

    # Get team needs once if team_id provided
    team_needs = None
    if request.team_id:
        from app.services.offseason_service import OffseasonService
        offseason_svc = OffseasonService(db)
        needs_list = offseason_svc.get_team_needs(request.team_id)
        team_needs = [need.position for need in needs_list[:5] if need.need_score > 0]

    async def generate_for_player(player_id: int) -> tuple[int, bool]:
        """Generate report for a single player, return (id, success)."""
        try:
            player = db.query(Player).filter(Player.id == player_id).first()
            if not player:
                return (player_id, False)

            attributes = {
                "speed": player.speed,
                "strength": player.strength,
                "agility": player.agility,
                "awareness": player.awareness,
                "throw_power": player.throw_power,
                "throw_accuracy_mid": player.throw_accuracy_mid,
            }

            report = await ai_service.generate_scouting_report(
                player_name=f"{player.first_name} {player.last_name}",
                position=player.position,
                overall_rating=player.overall_rating,
                college=player.college,
                attributes=attributes,
                team_needs=team_needs
            )
            return (player_id, report is not None)
        except Exception:
            return (player_id, False)

    # Run all generations concurrently
    results = await asyncio.gather(
        *[generate_for_player(pid) for pid in request.player_ids]
    )

    # Separate successes and failures
    generated = [pid for pid, success in results if success]
    failed = [pid for pid, success in results if not success]

    return BatchScoutingResponse(
        generated_count=len(generated),
        failed_count=len(failed),
        player_ids_generated=generated,
        player_ids_failed=failed
    )


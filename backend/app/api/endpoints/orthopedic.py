"""
Orthopedic RTP & Re-Injury Hazard Endpoints
===========================================
REST endpoints for:
1. 12-week Gompertz tissue repair curves across treatment protocols
2. Elite outside specialist 2nd opinion referrals (Andrews, Kerlan-Jobe, HSS)
3. 60Hz live physics Cortisone hazard evaluations
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.player import Player, InjuryStatus
from app.schemas.orthopedic_rtp import (
    OrthopedicEvaluationResponse,
    SecondOpinionCenter,
    SecondOpinionRequest,
    SecondOpinionConsultResult,
    CortisoneHazardCheckRequest,
    CortisoneHazardCheckResponse,
)
from app.services.orthopedic_engine import orthopedic_engine

router = APIRouter(prefix="/orthopedic", tags=["orthopedic"])


@router.get("/evaluation/{player_id}", response_model=OrthopedicEvaluationResponse)
def get_orthopedic_evaluation(
    player_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate 12-week non-linear Gompertz RTP trajectories and clinical recovery projections
    for an injured player. Evaluates 5 comparative treatment protocols.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    injury = player.injury
    injury_type = (injury.injury_type if injury and injury.injury_type else player.injury_type) or "Acute Musculoskeletal Strain"
    severity = (injury.injury_severity if injury and injury.injury_severity else player.injury_severity) or 3

    # Check active medical flags for Cortisone or Specialist clearance
    flags = dict(injury.medical_flags or {}) if injury else {}
    is_cortisone = flags.get("cortisone_active", False) or player.injury_status == InjuryStatus.QUESTIONABLE
    has_spec = flags.get("specialist_cleared", False)
    spec_center_name = flags.get("specialist_center_name", None)

    # Estimate baseline health from body part
    body_part = "right_leg"
    baseline_health = 55.0
    if player.body_health:
        bh = player.body_health[0] if isinstance(player.body_health, list) and len(player.body_health) > 0 else player.body_health
        baseline_health = getattr(bh, "right_leg_health", 55.0) or 55.0

    durability = player.injury_resistance or 80
    age = player.age or 26
    player_name = f"{player.first_name} {player.last_name}"

    eval_response = orthopedic_engine.generate_rtp_evaluation(
        player_id=player.id,
        injury_type=injury_type,
        body_part=body_part,
        severity_grade=severity,
        baseline_health=baseline_health,
        player_name=player_name,
        player_age=age,
        durability_rating=durability,
        is_cortisone_active=is_cortisone,
        has_specialist_clearance=has_spec,
        specialist_center_name=spec_center_name,
    )

    return eval_response


@router.get("/specialists", response_model=List[SecondOpinionCenter])
def list_specialist_centers():
    """
    Return available elite outside orthopedic consultation centers.
    """
    return orthopedic_engine.get_specialist_centers()


@router.post("/specialists/consult", response_model=SecondOpinionConsultResult)
def consult_specialist(
    request: SecondOpinionRequest,
    db: Session = Depends(get_db),
):
    """
    Dispatch an athlete to an outside orthopedic center of excellence for a second opinion.
    Has a 15% probability of uncovering occult misdiagnoses and applies a 50% complication risk reduction.
    """
    try:
        result = orthopedic_engine.consult_outside_specialist(
            db=db,
            player_id=request.player_id,
            center_id=request.center_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Specialist consultation failed: {str(e)}")


@router.post("/cortisone/check-hazard", response_model=CortisoneHazardCheckResponse)
def check_cortisone_hazard(
    request: CortisoneHazardCheckRequest,
):
    """
    Evaluate 60Hz physics in-game cortisone strain hazard during athletic cuts and tackles.
    Applies acute 2.5x catastrophe multiplier.
    """
    return orthopedic_engine.evaluate_cortisone_in_game_hazard(
        runner_has_cortisone=request.runner_has_cortisone,
        is_sharp_cut=request.is_sharp_cut,
        momentum=request.momentum,
        g_force=request.g_force,
    )

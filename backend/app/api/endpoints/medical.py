from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.medical_service import MedicalService
from app.services.medical.orthopedic_triage_service import orthopedic_triage_service
from app.schemas.deep_dive import (
    MedicalProtocolType,
    OrthopedicProtocolOption,
    TriageDecisionResult,
)

router = APIRouter(prefix="/api/medical", tags=["medical"])

class BodyHealthResponse(BaseModel):
    player_id: int
    head_health: float
    neck_health: float = 100.0
    torso_health: float
    right_arm_health: float
    left_arm_health: float
    right_leg_health: float
    left_leg_health: float
    general_wear: float
    is_injured: bool

def get_medical_service(db: Session = Depends(get_db)) -> MedicalService:
    return MedicalService(db)

@router.get("/player/{player_id}", response_model=BodyHealthResponse)
async def get_player_health(
    player_id: int,
    service: MedicalService = Depends(get_medical_service),
    db: Session = Depends(get_db)
):
    from app.models.player import Player
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if not player.body_health:
        # Initialize if missing
        health = service.initialize_body_health(player_id)
    elif isinstance(player.body_health, list):
        health = player.body_health[0] if len(player.body_health) > 0 else service.initialize_body_health(player_id)
    else:
        health = player.body_health

    return BodyHealthResponse(
        player_id=player_id,
        head_health=health.head_health,
        neck_health=getattr(health, 'neck_health', 100.0) if getattr(health, 'neck_health', None) is not None else 100.0,
        torso_health=health.torso_health,
        right_arm_health=health.right_arm_health,
        left_arm_health=health.left_arm_health,
        right_leg_health=health.right_leg_health,
        left_leg_health=health.left_leg_health,
        general_wear=health.general_wear,
        is_injured=player.injury_status != "HEALTHY"
    )

class ApplyWearRequest(BaseModel):
    player_id: int
    snaps: int
    position: str

@router.post("/apply-wear")
async def apply_wear(
    request: ApplyWearRequest,
    service: MedicalService = Depends(get_medical_service),
    db: Session = Depends(get_db)
):
    from app.models.player import Player
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    service.apply_game_wear(player, request.snaps, request.position)
    return {"status": "success", "message": f"Applied wear to player {request.player_id}"}


class TreatmentDecisionRequest(BaseModel):
    player_id: int
    treatment: str  # "REST", "SURGERY", "PLAY_THROUGH"

class TreatmentDecisionResponse(BaseModel):
    player_id: int
    treatment: str
    recovery_weeks: int
    surgery_risk: Optional[float] = None
    performance_penalty: Optional[Dict[str, int]] = None


@router.post("/treatment", response_model=TreatmentDecisionResponse)
async def apply_treatment(
    request: TreatmentDecisionRequest,
    service: MedicalService = Depends(get_medical_service),
    db: Session = Depends(get_db)
):
    """
    Apply a treatment decision to an injured player.

    Treatment Options:
    - REST: Standard recovery, no risk
    - SURGERY: Faster recovery but surgery risk (5-15% complication)
    - PLAY_THROUGH: Player continues to play with performance penalties
    """
    from app.models.player import Player, InjuryStatus
    import random

    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.injury_status == InjuryStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Player is not injured")

    treatment = request.treatment.upper()
    recovery_weeks = player.weeks_to_recovery
    surgery_risk = None
    performance_penalty = None

    if treatment == "SURGERY":
        # Surgery: 30-50% faster recovery but 5-15% complication risk
        base_risk = 0.05 + (player.injury_severity * 0.01)  # Higher severity = higher risk
        age_risk = max(0, (player.age - 30) * 0.005)  # Older = riskier
        surgery_risk = min(0.20, base_risk + age_risk)

        # Check for complication
        if random.random() < surgery_risk:
            # Complication - adds 2-6 weeks
            added_weeks = random.randint(2, 6)
            recovery_weeks += added_weeks
            player.injury_recurrence_risk += 0.10
        else:
            # Successful surgery - reduce recovery by 30-50%
            reduction = random.uniform(0.30, 0.50)
            recovery_weeks = max(1, int(recovery_weeks * (1 - reduction)))

        player.weeks_to_recovery = recovery_weeks

    elif treatment == "PLAY_THROUGH":
        # Player attempts to play through - set performance penalties
        severity = player.injury_severity
        toughness = player.injury_resistance

        # Calculate penalties based on severity
        penalties = {}
        if severity >= 3:
            penalties["speed"] = -min(15, severity * 2)
            penalties["agility"] = -min(15, severity * 2)
        if severity >= 5:
            penalties["strength"] = -min(10, severity)

        # Toughness reduces penalties
        toughness_reduction = toughness / 200.0  # Max 50% reduction
        performance_penalty = {
            k: int(v * (1 - toughness_reduction)) for k, v in penalties.items()
        }

        player.injury_status = InjuryStatus.QUESTIONABLE

    else:  # REST
        # Standard recovery - no changes to weeks
        player.injury_status = InjuryStatus.OUT

    db.commit()

    return TreatmentDecisionResponse(
        player_id=request.player_id,
        treatment=treatment,
        recovery_weeks=recovery_weeks,
        surgery_risk=surgery_risk,
        performance_penalty=performance_penalty
    )


class InjuredPlayerResponse(BaseModel):
    player_id: int
    first_name: str
    last_name: str
    position: str
    injury_type: Optional[str]
    injury_status: str
    severity: int
    weeks_remaining: int


@router.get("/team/{team_id}/injuries", response_model=List[InjuredPlayerResponse])
async def get_team_injuries(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get all injured players for a team."""
    from app.models.player import Player, InjuryStatus

    injured_players = db.query(Player).filter(
        Player.team_id == team_id,
        Player.injury_status != InjuryStatus.ACTIVE
    ).all()

    return [
        InjuredPlayerResponse(
            player_id=p.id,
            first_name=p.first_name,
            last_name=p.last_name,
            position=p.position,
            injury_type=p.injury_type,
            injury_status=p.injury_status.value if hasattr(p.injury_status, 'value') else str(p.injury_status),
            severity=p.injury_severity or 0,
            weeks_remaining=p.weeks_to_recovery or 0
        )
        for p in injured_players
    ]


class SurgeryRiskResponse(BaseModel):
    player_id: int
    base_risk: float
    age_risk: float
    severity_risk: float
    total_risk: float
    estimated_recovery_reduction: float


@router.get("/surgery-risk/{player_id}", response_model=SurgeryRiskResponse)
async def calculate_surgery_risk(
    player_id: int,
    db: Session = Depends(get_db)
):
    """Calculate surgery risk and potential recovery improvement for a player."""
    from app.models.player import Player, InjuryStatus

    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if player.injury_status == InjuryStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Player is not injured")

    # Base risk: 5%
    base_risk = 0.05

    # Age risk: +0.5% per year over 30
    age_risk = max(0, (player.age - 30) * 0.005)

    # Severity risk: +1% per severity point
    severity_risk = (player.injury_severity or 0) * 0.01

    total_risk = min(0.25, base_risk + age_risk + severity_risk)  # Cap at 25%

    # Estimated recovery reduction (30-50%)
    estimated_reduction = 0.40  # Average 40% faster

    return SurgeryRiskResponse(
        player_id=player_id,
        base_risk=base_risk,
        age_risk=age_risk,
        severity_risk=severity_risk,
        total_risk=total_risk,
        estimated_recovery_reduction=estimated_reduction
    )


# =============================================================================
# 5-PATHWAY ORTHOPEDIC TRIAGE ENDPOINTS
# =============================================================================

class InjuryDiagnosis(BaseModel):
    injury_type: Optional[str] = "Soft Tissue Strain"
    severity: int = 2
    weeks_to_recovery: int = 2
    body_zone: str = "right_leg"
    current_integrity: float = 60.0

class TriageProtocolsResponse(BaseModel):
    player_id: int
    current_diagnosis: InjuryDiagnosis
    protocols: List[OrthopedicProtocolOption]

class TriageDecisionRequest(BaseModel):
    protocol: MedicalProtocolType
    zone_key: Optional[str] = None


@router.get("/players/{player_id}/triage/protocols", response_model=TriageProtocolsResponse)
@router.get("/triage/protocols/{player_id}", response_model=TriageProtocolsResponse)
async def get_player_triage_protocols(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all available 5-pathway orthopedic triage protocols for a player.
    Pathways: REST, PRP_THERAPY, ARTHROSCOPIC_SURGERY, RECONSTRUCTIVE_SURGERY, CORTISONE_STABILIZATION.
    """
    from app.models.player import Player

    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    zone_key = "right_leg"
    bh = None
    if isinstance(player.body_health, list) and len(player.body_health) > 0:
        bh = player.body_health[0]
    elif player.body_health and not isinstance(player.body_health, list):
        bh = player.body_health

    if bh:
        # Find zone with lowest health
        zones = {
            "head": bh.head_health,
            "neck": getattr(bh, "neck_health", 100.0) or 100.0,
            "torso": bh.torso_health,
            "right_arm": bh.right_arm_health,
            "left_arm": bh.left_arm_health,
            "right_leg": bh.right_leg_health,
            "left_leg": bh.left_leg_health,
        }
        zone_key = min(zones, key=zones.get)
        current_integrity = zones[zone_key]
    else:
        current_integrity = 60.0

    baseline_weeks = player.weeks_to_recovery if player.weeks_to_recovery and player.weeks_to_recovery > 0 else 3
    player_age = player.age or 26
    is_x_factor = getattr(player, "development_trait", "") in ["SUPERSTAR", "X_FACTOR", "SUPERSTAR_X_FACTOR"]

    options = orthopedic_triage_service.get_protocol_options(
        zone_key=zone_key,
        current_integrity=current_integrity,
        baseline_weeks=baseline_weeks,
        player_age=player_age,
        is_x_factor=is_x_factor,
    )

    diagnosis = InjuryDiagnosis(
        injury_type=player.injury_type or "Musculoskeletal Trauma",
        severity=player.injury_severity or 2,
        weeks_to_recovery=baseline_weeks,
        body_zone=zone_key,
        current_integrity=round(current_integrity, 1),
    )

    return TriageProtocolsResponse(
        player_id=player_id,
        current_diagnosis=diagnosis,
        protocols=options,
    )


@router.get("/triage/options", response_model=List[OrthopedicProtocolOption])
async def get_triage_protocol_options():
    """Get general clinical protocol options for orthopedic triage."""
    return orthopedic_triage_service.get_protocol_options(
        zone_key="general",
        current_integrity=60.0,
        baseline_weeks=3,
        player_age=26,
    )


@router.post("/players/{player_id}/triage/apply", response_model=TriageDecisionResult)
async def apply_player_triage_protocol(
    player_id: int,
    request: TriageDecisionRequest,
    db: Session = Depends(get_db)
):
    """
    Apply a 5-pathway clinical triage protocol to an injured player.
    Executes recovery calculations, rolls for complication risk, and updates player recovery timetable.
    """
    from app.models.player import Player, InjuryStatus

    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    zone_key = request.zone_key or "right_leg"
    baseline_weeks = player.weeks_to_recovery if player.weeks_to_recovery and player.weeks_to_recovery > 0 else 3
    player_age = player.age or 26
    toughness = player.injury_resistance or 80

    result = orthopedic_triage_service.apply_triage_protocol(
        player_id=player.id,
        zone_key=zone_key,
        protocol=request.protocol,
        baseline_weeks=baseline_weeks,
        player_age=player_age,
        toughness=toughness,
    )

    # Persist decision to DB
    player.weeks_to_recovery = result.projected_recovery_weeks
    player.injury_recurrence_risk = result.re_injury_risk_index

    if request.protocol == MedicalProtocolType.CORTISONE_STABILIZATION:
        player.injury_status = InjuryStatus.QUESTIONABLE
    elif result.projected_recovery_weeks > 0:
        player.injury_status = InjuryStatus.OUT
    else:
        player.injury_status = InjuryStatus.ACTIVE

    db.commit()
    db.refresh(player)

    return result



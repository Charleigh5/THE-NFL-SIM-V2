
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.medical_service import MedicalService

router = APIRouter(prefix="/api/medical", tags=["medical"])

class BodyHealthResponse(BaseModel):
    player_id: int
    head_health: float
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
    else:
        health = player.body_health[0]

    return BodyHealthResponse(
        player_id=player_id,
        head_health=health.head_health,
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
    surgery_risk: float | None = None
    performance_penalty: dict[str, int] | None = None


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
    import random

    from app.models.player import InjuryStatus, Player

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
    injury_type: str | None
    injury_status: str
    severity: int
    weeks_remaining: int


@router.get("/team/{team_id}/injuries", response_model=list[InjuredPlayerResponse])
async def get_team_injuries(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get all injured players for a team."""
    from app.models.player import InjuryStatus, Player

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
    from app.models.player import InjuryStatus, Player

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


from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.coach import Coach, CoachTier
from app.models.team import Team
from app.services.coaching.coaching_dynasty_service import coaching_dynasty_service
from app.schemas.deep_dive import (
    CoachDynastyProfile,
    StaffSynergyBreakdown,
    CoachingSkillNode,
    CoachingBranch,
)

router = APIRouter(prefix="/api/coaches", tags=["coaches"])


# =============================================================================
# SCHEMAS
# =============================================================================

class CoachResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    role: str
    tier: str
    team_id: Optional[int]
    team_name: Optional[str]
    offense_rating: int
    defense_rating: int
    development_rating: int
    playbook_offense: Optional[str]
    playbook_defense: Optional[str]

class CoachListResponse(BaseModel):
    coaches: List[CoachResponse]

class HireCoachRequest(BaseModel):
    coach_id: int
    team_id: int
    role: str  # "Head Coach", "Offensive Coordinator", "Defensive Coordinator"

class FireCoachRequest(BaseModel):
    coach_id: int

class UnlockNodeRequest(BaseModel):
    node_id: str

class CoachCarouselResponse(BaseModel):
    available_coaches: List[CoachResponse]
    hot_seat: List[CoachResponse]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _coach_to_response(coach: Coach, db: Session) -> CoachResponse:
    team_name = None
    if coach.team_id:
        team = db.query(Team).filter(Team.id == coach.team_id).first()
        team_name = f"{team.city} {team.name}" if team else None

    return CoachResponse(
        id=coach.id,
        first_name=coach.first_name,
        last_name=coach.last_name,
        role=coach.role,
        tier=coach.tier.value if hasattr(coach.tier, 'value') else str(coach.tier),
        team_id=coach.team_id,
        team_name=team_name,
        offense_rating=coach.offense_rating,
        defense_rating=coach.defense_rating,
        development_rating=coach.development_rating,
        playbook_offense=coach.playbook_offense,
        playbook_defense=coach.playbook_defense
    )


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/team/{team_id}", response_model=CoachListResponse)
async def get_team_coaches(team_id: int, db: Session = Depends(get_db)):
    """Get all coaches for a specific team."""
    coaches = db.query(Coach).filter(Coach.team_id == team_id).all()
    return CoachListResponse(
        coaches=[_coach_to_response(c, db) for c in coaches]
    )


@router.get("/available", response_model=CoachListResponse)
async def get_available_coaches(db: Session = Depends(get_db)):
    """Get all coaches not currently employed by a team."""
    coaches = db.query(Coach).filter(Coach.team_id == None).all()
    return CoachListResponse(
        coaches=[_coach_to_response(c, db) for c in coaches]
    )


@router.get("/carousel", response_model=CoachCarouselResponse)
async def get_coaching_carousel(db: Session = Depends(get_db)):
    """
    Get the coaching carousel state:
    - Available coaches (unemployed)
    - Hot seat coaches (poor performance, candidates for firing)
    """
    available = db.query(Coach).filter(Coach.team_id == None).all()

    # Hot seat: ROOKIE tier coaches or low combined rating
    hot_seat = db.query(Coach).filter(
        Coach.team_id != None,
        Coach.tier == CoachTier.ROOKIE
    ).all()

    return CoachCarouselResponse(
        available_coaches=[_coach_to_response(c, db) for c in available],
        hot_seat=[_coach_to_response(c, db) for c in hot_seat]
    )


@router.post("/hire")
async def hire_coach(request: HireCoachRequest, db: Session = Depends(get_db)):
    """
    Hire a coach for a team in a specific role.
    If another coach occupies that role, they are automatically fired.
    """
    coach = db.query(Coach).filter(Coach.id == request.coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    if coach.team_id is not None:
        raise HTTPException(status_code=400, detail="Coach is already employed")

    team = db.query(Team).filter(Team.id == request.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Fire existing coach in this role
    existing = db.query(Coach).filter(
        Coach.team_id == request.team_id,
        Coach.role == request.role
    ).first()

    if existing:
        existing.team_id = None  # Fire them

    # Hire new coach
    coach.team_id = request.team_id
    coach.role = request.role
    db.commit()

    return {
        "status": "success",
        "message": f"{coach.first_name} {coach.last_name} hired as {request.role}",
        "fired_coach": f"{existing.first_name} {existing.last_name}" if existing else None
    }


@router.post("/fire")
async def fire_coach(request: FireCoachRequest, db: Session = Depends(get_db)):
    """Fire a coach from their current team."""
    coach = db.query(Coach).filter(Coach.id == request.coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    if coach.team_id is None:
        raise HTTPException(status_code=400, detail="Coach is not employed")

    team_id = coach.team_id
    coach.team_id = None
    db.commit()

    return {
        "status": "success",
        "message": f"{coach.first_name} {coach.last_name} has been fired"
    }


@router.get("/{coach_id}", response_model=CoachResponse)
async def get_coach(coach_id: int, db: Session = Depends(get_db)):
    """Get details for a specific coach."""
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    return _coach_to_response(coach, db)


@router.post("/promote/{coach_id}")
async def promote_coach(
    coach_id: int,
    new_role: str,
    db: Session = Depends(get_db)
):
    """
    Promote a coordinator to Head Coach within their team.
    The old Head Coach is automatically demoted/fired.
    """
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    if coach.team_id is None:
        raise HTTPException(status_code=400, detail="Coach must be employed to be promoted")

    if new_role == "Head Coach":
        # Fire current HC
        current_hc = db.query(Coach).filter(
            Coach.team_id == coach.team_id,
            Coach.role == "Head Coach"
        ).first()

        if current_hc and current_hc.id != coach_id:
            current_hc.team_id = None  # Fire

        coach.role = "Head Coach"
        db.commit()

        return {
            "status": "success",
            "message": f"{coach.first_name} {coach.last_name} promoted to Head Coach",
            "demoted": f"{current_hc.first_name} {current_hc.last_name}" if current_hc else None
        }

    raise HTTPException(status_code=400, detail="Invalid promotion role")


# =============================================================================
# DYNASTY SKILL TREE & STAFF SYNERGY ENDPOINTS
# =============================================================================

@router.get("/{coach_id}/tree", response_model=CoachDynastyProfile)
@router.get("/{coach_id}/dynasty", response_model=CoachDynastyProfile)
async def get_coach_tree(coach_id: int, db: Session = Depends(get_db)):
    """
    Get 3-branch dynasty skill tree profile for a coach.
    Branches: Scheme & Tactics, Player Development, Program Culture.
    """
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    coach_name = f"{coach.first_name} {coach.last_name}"
    role = coach.role or "Head Coach"
    level = coach.level if coach.level and coach.level > 0 else max(1, (coach.offense_rating + coach.defense_rating + coach.development_rating) // 20)
    current_sp = coach.xp // 100 if hasattr(coach, 'xp') and coach.xp else 4

    unlocked_nodes = None
    if coach.skills and isinstance(coach.skills, dict) and "unlocked_nodes" in coach.skills:
        unlocked_nodes = coach.skills.get("unlocked_nodes")

    return coaching_dynasty_service.get_coach_profile(
        coach_id=str(coach.id),
        name=coach_name,
        role=role,
        level=level,
        current_sp=current_sp,
        unlocked_node_ids=unlocked_nodes,
    )


@router.post("/{coach_id}/unlock-node", response_model=CoachDynastyProfile)
@router.post("/{coach_id}/dynasty/unlock", response_model=CoachDynastyProfile)
async def unlock_coach_skill_node(
    coach_id: int,
    request: UnlockNodeRequest,
    db: Session = Depends(get_db)
):
    """
    Unlock a skill tree node for a coach using skill points (SP).
    Enforces prerequisites and DAG dependencies.
    """
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")

    coach_name = f"{coach.first_name} {coach.last_name}"
    role = coach.role or "Head Coach"
    level = coach.level if coach.level and coach.level > 0 else max(1, (coach.offense_rating + coach.defense_rating + coach.development_rating) // 20)
    current_sp = coach.xp // 100 if hasattr(coach, 'xp') and coach.xp else 4

    unlocked_nodes = None
    if coach.skills and isinstance(coach.skills, dict) and "unlocked_nodes" in coach.skills:
        unlocked_nodes = list(coach.skills.get("unlocked_nodes", []))

    profile = coaching_dynasty_service.get_coach_profile(
        coach_id=str(coach.id),
        name=coach_name,
        role=role,
        level=level,
        current_sp=current_sp,
        unlocked_node_ids=unlocked_nodes,
    )

    success = coaching_dynasty_service.unlock_node(profile, request.node_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot unlock node '{request.node_id}'. Ensure prerequisites are met and sufficient SP available."
        )

    # Persist unlocked state to DB
    skills_dict = dict(coach.skills) if coach.skills and isinstance(coach.skills, dict) else {}
    unlocked_list = [nid for nid, n in profile.tree_nodes.items() if n.unlocked]
    skills_dict["unlocked_nodes"] = unlocked_list
    coach.skills = skills_dict
    db.commit()
    db.refresh(coach)

    return profile


@router.get("/staff/synergy/{team_id}", response_model=StaffSynergyBreakdown)
@router.get("/team/{team_id}/synergy", response_model=StaffSynergyBreakdown)
async def get_staff_synergy(team_id: int, db: Session = Depends(get_db)):
    """
    Calculate organizational chemistry and synergy score across HC, OC, and DC.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    team_coaches = db.query(Coach).filter(Coach.team_id == team_id).all()

    hc = next((c for c in team_coaches if c.role == "Head Coach"), None)
    oc = next((c for c in team_coaches if c.role in ["Offensive Coordinator", "OC"]), None)
    dc = next((c for c in team_coaches if c.role in ["Defensive Coordinator", "DC"]), None)

    hc_scheme = hc.playbook_offense if hc and hc.playbook_offense else "WEST_COAST"
    oc_scheme = oc.playbook_offense if oc and oc.playbook_offense else "WEST_COAST"
    dc_scheme = dc.playbook_defense if dc and dc.playbook_defense else "COVER_3_ZONE"

    hc_id = f"HC-{hc.id}" if hc else "HC-01"
    oc_id = f"OC-{oc.id}" if oc else "OC-01"
    dc_id = f"DC-{dc.id}" if dc else "DC-01"

    return coaching_dynasty_service.calculate_staff_synergy(
        hc_scheme=hc_scheme,
        oc_scheme=oc_scheme,
        dc_scheme=dc_scheme,
        hc_id=hc_id,
        oc_id=oc_id,
        dc_id=dc_id,
    )


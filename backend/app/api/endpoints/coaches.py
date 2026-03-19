from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.coach import Coach, CoachTier
from app.models.team import Team

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
    coaches = db.query(Coach).filter(Coach.team_id is None).all()
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
    available = db.query(Coach).filter(Coach.team_id is None).all()

    # Hot seat: ROOKIE tier coaches or low combined rating
    hot_seat = db.query(Coach).filter(
        Coach.team_id is not None,
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

"""
Playbook Familiarity API Endpoints
===================================
Phase 3: B-059, B-060

Provides endpoints for querying and updating player playbook familiarity.
"""


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.player import Player
from app.services.playbook.familiarity import FamiliarityManager

router = APIRouter(prefix="/playbook", tags=["Playbook"])

# Global familiarity manager (in production, this would be scoped to game session)
_familiarity_manager = FamiliarityManager()


# =============================================================================
# SCHEMAS
# =============================================================================

class PlayKnowledge(BaseModel):
    """Schema for individual play knowledge."""
    familiarity: float = Field(..., ge=0.0, le=1.0)
    tier: str
    times_executed: int
    success_rate: float


class FamiliarityResponse(BaseModel):
    """B-059: Response for GET /playbook/familiarity/{player_id}."""
    player_id: int
    experience_years: int
    current_scheme: str | None
    total_plays_known: int
    mastered_plays_count: int
    average_familiarity: float
    plays: dict[str, PlayKnowledge]

    class Config:
        from_attributes = True


class LearnPlayRequest(BaseModel):
    """B-060: Request for POST /playbook/learn."""
    player_id: int
    play_id: str
    success: bool = True
    practice_bonus: float = Field(default=1.0, ge=1.0, le=2.0)


class LearnPlayResponse(BaseModel):
    """B-060: Response for POST /playbook/learn."""
    player_id: int
    play_id: str
    previous_familiarity: float
    new_familiarity: float
    tier: str


class SchemeChangeRequest(BaseModel):
    """Request for POST /playbook/scheme-change."""
    player_id: int
    new_scheme: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/familiarity/{player_id}", response_model=FamiliarityResponse)
async def get_player_familiarity(
    player_id: int,
    db: Session = Depends(get_db)
):
    """
    B-059: Get a player's playbook familiarity data.

    Returns all known plays and their familiarity levels.
    """
    # Verify player exists
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")

    # Get or create familiarity record
    experience = getattr(player, "years_pro", 0)
    familiarity = _familiarity_manager.get_or_create(player_id, experience)

    # Convert to response format
    data = familiarity.to_dict()

    return FamiliarityResponse(
        player_id=data["player_id"],
        experience_years=data["experience_years"],
        current_scheme=data["current_scheme"],
        total_plays_known=data["total_plays_known"],
        mastered_plays_count=data["mastered_plays_count"],
        average_familiarity=data["average_familiarity"],
        plays={
            play_id: PlayKnowledge(**play_data)
            for play_id, play_data in data["plays"].items()
        }
    )


@router.post("/learn", response_model=LearnPlayResponse)
async def learn_play(
    request: LearnPlayRequest,
    db: Session = Depends(get_db)
):
    """
    B-060: Trigger learning for a specific play.

    Used during practice sessions or post-game film study.
    """
    # Verify player exists
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {request.player_id} not found")

    # Get familiarity record
    experience = getattr(player, "years_pro", 0)
    familiarity = _familiarity_manager.get_or_create(request.player_id, experience)

    # Record previous familiarity
    prev_fam = familiarity.get_familiarity(request.play_id)

    # Apply learning
    new_fam = familiarity.learn_play(
        request.play_id,
        success=request.success,
        practice_bonus=request.practice_bonus
    )

    # Get current tier
    play_data = familiarity.play_knowledge.get(request.play_id)
    tier = play_data.tier.value if play_data else "UNKNOWN"

    return LearnPlayResponse(
        player_id=request.player_id,
        play_id=request.play_id,
        previous_familiarity=prev_fam,
        new_familiarity=new_fam,
        tier=tier
    )


@router.post("/scheme-change")
async def apply_scheme_change(
    request: SchemeChangeRequest,
    db: Session = Depends(get_db)
):
    """
    Apply scheme change penalty to a player.

    Used when a player joins a new team or coach changes scheme.
    """
    # Verify player exists
    player = db.query(Player).filter(Player.id == request.player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail=f"Player {request.player_id} not found")

    # Get familiarity record
    experience = getattr(player, "years_pro", 0)
    familiarity = _familiarity_manager.get_or_create(request.player_id, experience)

    # Record previous average
    prev_avg = familiarity.get_average_familiarity()
    prev_scheme = familiarity.current_scheme

    # Apply penalty
    familiarity.apply_scheme_change_penalty(request.new_scheme)

    # Get new average
    new_avg = familiarity.get_average_familiarity()

    return {
        "player_id": request.player_id,
        "previous_scheme": prev_scheme,
        "new_scheme": request.new_scheme,
        "previous_average_familiarity": prev_avg,
        "new_average_familiarity": new_avg,
        "penalty_applied": prev_scheme != request.new_scheme
    }


@router.get("/team/{team_id}/familiarity")
async def get_team_familiarity(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Get average familiarity for all players on a team.

    Useful for coaching analysis.
    """
    # Get all players on team
    players = db.query(Player).filter(Player.team_id == team_id).all()
    if not players:
        raise HTTPException(status_code=404, detail=f"No players found for team {team_id}")

    player_familiarity = []
    for player in players:
        experience = getattr(player, "years_pro", 0)
        familiarity = _familiarity_manager.get_or_create(player.id, experience)
        player_familiarity.append({
            "player_id": player.id,
            "name": f"{player.first_name} {player.last_name}",
            "position": player.position,
            "average_familiarity": familiarity.get_average_familiarity(),
            "mastered_plays": len(familiarity.get_mastered_plays()),
            "total_plays_known": familiarity.get_total_plays_known()
        })

    # Sort by familiarity
    player_familiarity.sort(key=lambda x: x["average_familiarity"], reverse=True)

    total_avg = sum(p["average_familiarity"] for p in player_familiarity) / len(player_familiarity)

    return {
        "team_id": team_id,
        "total_players": len(player_familiarity),
        "team_average_familiarity": total_avg,
        "players": player_familiarity
    }

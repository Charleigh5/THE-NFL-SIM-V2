from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.playbook.gameplan_service import GameplanService

router = APIRouter(prefix="/api/gameplan", tags=["gameplan"])


class GameplanRequest(BaseModel):
    team_id: int
    season_id: int
    week: int
    opponent_id: int
    strategy: dict[str, str]


def get_gameplan_service(db: Session = Depends(get_db)) -> GameplanService:
    return GameplanService(db)


@router.post("/install")
async def install_gameplan(
    request: GameplanRequest, service: GameplanService = Depends(get_gameplan_service)
):
    """
    Install a weekly gameplan.
    """
    gp = service.install_weekly_gameplan(
        team_id=request.team_id,
        season_id=request.season_id,
        week=request.week,
        opponent_id=request.opponent_id,
        strategy=request.strategy,
    )

    return {"status": "success", "gameplan_id": gp.id, "message": "Gameplan installed"}


@router.get("/check-bonus/{gameplan_id}/{opponent_gameplan_id}")
async def check_bonus(
    gameplan_id: int,
    opponent_gameplan_id: int,
    db: Session = Depends(get_db),
    service: GameplanService = Depends(get_gameplan_service),
):
    from app.models.gameplan import Gameplan

    gp = db.query(Gameplan).filter(Gameplan.id == gameplan_id).first()
    opp_gp = db.query(Gameplan).filter(Gameplan.id == opponent_gameplan_id).first()

    if not gp or not opp_gp:
        raise HTTPException(status_code=404, detail="Gameplan not found")

    service.calculate_preparation_bonus(gp, opp_gp)

    return {"off_bonus": gp.prep_bonus_offense, "def_bonus": gp.prep_bonus_defense}

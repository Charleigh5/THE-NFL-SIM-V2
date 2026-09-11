"""
Capology Double-Entry Ledger Endpoints
======================================
REST endpoints exposing double-entry accounting statements,
multi-year outlooks, dry-run simulation, and transaction journaling.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.cap_ledger_service import CapLedgerService, BASE_LEAGUE_YEAR
from app.schemas.cap_ledger import (
    TeamLedgerStatementDTO,
    MultiYearLedgerStatementResponse,
    LedgerSimulateRequest,
    LedgerSimulateResponse,
    CapLedgerTransactionDTO,
)

router = APIRouter(prefix="/api/cap-ledger", tags=["Capology Double-Entry Ledger"])


@router.get(
    "/teams/{team_id}/statement",
    response_model=TeamLedgerStatementDTO,
    summary="Get Team Cap Ledger Statement",
    description="Returns the double-entry accounting balance and transaction history for a specific league year.",
)
def get_team_statement(
    team_id: int,
    league_year: int = Query(default=BASE_LEAGUE_YEAR, description="League Year"),
    db: Session = Depends(get_db),
):
    service = CapLedgerService(db=db)
    return service.get_team_statement(team_id=team_id, league_year=league_year)


@router.get(
    "/teams/{team_id}/multi-year",
    response_model=MultiYearLedgerStatementResponse,
    summary="Get 5-Year Multi-Year Ledger Statement",
    description="Returns consolidated 5-year multi-year outlook directly from double-entry ledger state.",
)
def get_multi_year_statement(
    team_id: int,
    base_year: int = Query(default=BASE_LEAGUE_YEAR, description="Base League Year"),
    db: Session = Depends(get_db),
):
    service = CapLedgerService(db=db)
    return service.get_multi_year_statement(team_id=team_id, base_year=base_year)


@router.post(
    "/simulate",
    response_model=LedgerSimulateResponse,
    summary="Dry-Run Ledger Proposal Simulation",
    description="Simulates a contract transaction dry-run with invariant checks and proof of balance without committing state.",
)
def simulate_proposal(
    request: LedgerSimulateRequest,
    db: Session = Depends(get_db),
):
    service = CapLedgerService(db=db)
    return service.simulate_proposal_isolated(request)


@router.post(
    "/transactions/signing",
    response_model=CapLedgerTransactionDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Book Contract Signing Transaction",
    description="Atomically books a contract signing into the double-entry ledger.",
)
def book_signing(
    team_id: int,
    player_id: int,
    annual_base_salary: int,
    signing_bonus_total: int,
    real_years: int,
    void_years: int = 0,
    player_name: Optional[str] = None,
    league_year: int = BASE_LEAGUE_YEAR,
    db: Session = Depends(get_db),
):
    service = CapLedgerService(db=db)
    try:
        return service.record_contract_signing(
            team_id=team_id,
            player_id=player_id,
            annual_base_salary=annual_base_salary,
            signing_bonus_total=signing_bonus_total,
            real_years=real_years,
            void_years=void_years,
            league_year=league_year,
            player_name=player_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

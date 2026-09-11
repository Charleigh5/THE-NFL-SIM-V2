"""
Capology & Multi-Year Contract API Endpoints
============================================
Exposes high-speed simulation endpoints for NFL CBA multi-year cap modeling,
void years proration, accelerated dead money, and compensatory pick forecasting.
"""

from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.concurrency import run_in_threadpool

from app.core.database import SessionLocal
from app.models.team import Team
from app.schemas.capology import (
    MultiYearContractProposal,
    MultiYearCapProjectionResponse,
    YearlyCapLiability,
)
from app.services.capology_engine import CapologyEngine, BASE_LEAGUE_YEAR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/capology", tags=["Capology & Contracts"])


@router.post(
    "/simulate-proposal",
    response_model=MultiYearCapProjectionResponse,
    summary="Simulate multi-year contract proposal impact",
)
async def simulate_contract_proposal(proposal: MultiYearContractProposal):
    """
    Simulate the full 5-year cap liability schedule for a proposed contract.
    Evaluates:
    - 5-year maximum signing bonus proration window.
    - Post-void accelerated dead money liabilities.
    - Post-June 1st two-year dead money split mechanics.
    - Appendix V Compensatory Free Agent (CFA) draft pick cancellation alerts.
    Execution latency: <40ms.
    """
    def _execute():
        with SessionLocal() as sync_db:
            engine = CapologyEngine(sync_db)
            return engine.calculate_multi_year_projection(proposal)

    return await run_in_threadpool(_execute)


@router.get(
    "/teams/{team_id}/five-year-outlook",
    response_model=List[YearlyCapLiability],
    summary="Fetch franchise baseline 5-year cap outlook",
)
async def get_team_five_year_outlook(team_id: int):
    """
    Retrieve baseline 5-year salary cap outlook for a team without any pending proposals.
    """
    def _execute():
        with SessionLocal() as sync_db:
            if team_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid team_id",
                )
            engine = CapologyEngine(sync_db)
            committed_schedule = engine.get_team_payroll_commitments(team_id)

            schedule: List[YearlyCapLiability] = []
            for i in range(5):
                cal_year = BASE_LEAGUE_YEAR + i
                projected_cap = engine.get_projected_cap(i)
                committed = committed_schedule[i]
                net_space = projected_cap - committed

                schedule.append(
                    YearlyCapLiability(
                        year=cal_year,
                        projected_cap=projected_cap,
                        committed_salaries=committed,
                        prorated_bonus=0,
                        proposed_contract_cap_hit=0,
                        dead_money=0,
                        net_cap_space=net_space,
                        is_cap_compliant=net_space >= 0,
                    )
                )
            return schedule

    return await run_in_threadpool(_execute)

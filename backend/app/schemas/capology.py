"""
Capology & Multi-Year Contract Schemas
======================================
Pydantic V2 schemas for NFL CBA Article 13 salary cap proration,
void years acceleration, and Appendix V compensatory pick formulas.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ContractYearStructure(BaseModel):
    """Annual breakdown for a specific contract year."""
    year_index: int = Field(ge=1, le=7, description="Contract year 1-7")
    calendar_year: int = Field(ge=2024, le=2035)
    base_salary: int = Field(ge=0, description="Cash base salary in dollars")
    prorated_bonus: int = Field(default=0, ge=0, description="Prorated signing bonus portion")
    roster_bonus: int = Field(default=0, ge=0)
    workout_bonus: int = Field(default=0, ge=0)
    is_void_year: bool = Field(default=False, description="True if year is an automatic void trigger")
    cap_hit: int = Field(ge=0, description="Total cap charge for this year")


class MultiYearContractProposal(BaseModel):
    """Proposal parameters submitted by GM to evaluate multi-year cap impact."""
    player_id: int = Field(description="ID of free agent or roster player")
    team_id: int = Field(description="ID of franchise team")
    real_years: int = Field(default=3, ge=1, le=5, description="Active playing contract length")
    void_years: int = Field(default=0, ge=0, le=4, description="CBA void dummy years for proration")
    annual_base_salary: int = Field(default=5_000_000, ge=950_000, le=65_000_000)
    signing_bonus_total: int = Field(default=10_000_000, ge=0, le=150_000_000)
    guaranteed_total: int = Field(default=15_000_000, ge=0)
    post_june_1_designation: bool = Field(
        default=False,
        description="Splits accelerated dead money across 2 league years upon voiding"
    )


class YearlyCapLiability(BaseModel):
    """Projected cap commitment and headroom for a specific league calendar year."""
    year: int = Field(description="League year (e.g. 2026)")
    projected_cap: int = Field(description="Projected NFL hard salary cap in dollars")
    committed_salaries: int = Field(description="Existing team payroll commitments")
    prorated_bonus: int = Field(description="Prorated bonus allocation from proposal")
    proposed_contract_cap_hit: int = Field(description="Total cap hit of proposed contract")
    dead_money: int = Field(description="Accelerated dead money liability (from void triggers)")
    net_cap_space: int = Field(description="Remaining available cap headroom")
    is_cap_compliant: bool = Field(description="True if net_cap_space >= 0")


class CompPickImpact(BaseModel):
    """Evaluation of impact on NFL CBA Appendix V Compensatory Free Agent draft picks."""
    qualifies_as_cfa: bool = Field(description="True if contract APY meets CFA qualifying threshold (~$3.0M+)")
    cfa_tier: Optional[int] = Field(default=None, description="Comp pick round value: 3, 4, 5, 6, or 7")
    cancelled_pick_round: Optional[int] = Field(default=None, description="Round of comp pick forfeited by this signing")
    projected_comp_picks_lost: List[str] = Field(default_factory=list)
    impact_summary: str = Field(description="Human-readable summary of compensatory pick ramifications")


class MultiYearCapProjectionResponse(BaseModel):
    """Full 5-year cap liability schedule and risk evaluation."""
    player_id: int
    team_id: int
    total_contract_value: int
    annual_average_value: int
    proration_years_used: int
    yearly_schedule: List[YearlyCapLiability]
    accelerated_dead_money_void_year: int
    comp_pick_impact: CompPickImpact
    is_fully_compliant: bool = Field(description="True if all 5 projected years maintain non-negative cap room")
    model_config = ConfigDict(from_attributes=True)

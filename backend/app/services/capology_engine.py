"""
Capology Engine Service
=======================
High-performance deterministic NFL CBA salary cap calculator.
Computes multi-year liabilities, 5-year maximum signing bonus proration,
void years dead money acceleration, and Appendix V compensatory pick impacts.
Execution budget: <40ms.
"""

from typing import List, Optional, Tuple, Dict, Any
import math
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.team import Team
from app.models.player import Player
from app.models.player_contract import PlayerContract
from app.schemas.capology import (
    MultiYearContractProposal,
    YearlyCapLiability,
    CompPickImpact,
    MultiYearCapProjectionResponse,
)

# Baseline 2026 NFL Hard Cap with 5.5% annual compound inflation
BASE_LEAGUE_YEAR = 2026
BASE_SALARY_CAP = 255_400_000
ANNUAL_CAP_INFLATION_RATE = 0.055

# Natural payroll decay curve for existing 53-man rosters as contracts expire
ROSTER_DECAY_RATES = [1.00, 0.78, 0.54, 0.32, 0.16]

# Appendix V Compensatory Free Agent APY thresholds
CFA_TIERS = [
    (20_000_000, 3),  # Round 3 pick
    (14_000_000, 4),  # Round 4 pick
    (9_000_000, 5),   # Round 5 pick
    (5_000_000, 6),   # Round 6 pick
    (3_000_000, 7),   # Round 7 pick
]
CFA_MINIMUM_QUALIFYING_APY = 3_000_000


class CapologyEngine:
    """
    Engine executing deterministic multi-year cap modeling adhering to NFL CBA Article 13 & Appendix V.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    @staticmethod
    def get_projected_cap(year_index: int) -> int:
        """
        Compute projected league salary cap for year_index (0 = Base Year, 4 = +4 Years).
        """
        multiplier = (1.0 + ANNUAL_CAP_INFLATION_RATE) ** year_index
        return int(BASE_SALARY_CAP * multiplier)

    def get_team_payroll_commitments(self, team_id: int) -> List[int]:
        """
        Determine baseline committed payroll for the next 5 league years for a team.
        Derives from active player contracts in the database with graceful fallback.
        """
        committed_by_year = [0, 0, 0, 0, 0]

        if self.db:
            try:
                # Query all active players with contracts on this team
                stmt = (
                    select(PlayerContract.contract_years, PlayerContract.contract_salary)
                    .join(Player, Player.id == PlayerContract.player_id)
                    .where(
                        Player.team_id == team_id,
                        PlayerContract.is_retired == False,  # noqa: E712
                    )
                )
                contracts = self.db.execute(stmt).all()

                if contracts:
                    for contract_years, contract_salary in contracts:
                        years = min(max(1, contract_years or 1), 5)
                        salary = contract_salary or 1_000_000
                        for i in range(years):
                            committed_by_year[i] += salary
                    return committed_by_year
            except Exception:
                pass

        # Fallback: Derive from Team model salary cap space
        baseline_payroll = 215_000_000
        if self.db:
            team = self.db.get(Team, team_id)
            if team and team.salary_cap_total and team.salary_cap_space is not None:
                baseline_payroll = max(0, int(team.salary_cap_total - team.salary_cap_space))

        return [int(baseline_payroll * decay) for decay in ROSTER_DECAY_RATES]

    def evaluate_comp_pick_formula(
        self,
        proposal: MultiYearContractProposal,
        team_id: int,
    ) -> CompPickImpact:
        """
        Evaluate NFL CBA Appendix V Compensatory Free Agent draft pick ramifications.
        """
        total_real_money = (proposal.annual_base_salary * proposal.real_years) + proposal.signing_bonus_total
        apy = total_real_money // max(1, proposal.real_years)

        if apy < CFA_MINIMUM_QUALIFYING_APY:
            return CompPickImpact(
                qualifies_as_cfa=False,
                cfa_tier=None,
                cancelled_pick_round=None,
                projected_comp_picks_lost=[],
                impact_summary="Contract does not meet the $3.0M APY threshold. No compensatory draft picks will be cancelled."
            )

        # Determine CFA tier
        assigned_tier = 7
        for threshold, tier in CFA_TIERS:
            if apy >= threshold:
                assigned_tier = tier
                break

        # Simulate compensatory pick cancellation
        cancelled_round = assigned_tier
        projected_lost = [f"{BASE_LEAGUE_YEAR + 1} Round {cancelled_round} Compensatory Pick"]
        summary = (
            f"Signing qualifies as a Tier {assigned_tier} CFA (${apy:,.0f} APY). "
            f"This contract will cancel a projected {BASE_LEAGUE_YEAR + 1} Round {cancelled_round} compensatory draft pick."
        )

        return CompPickImpact(
            qualifies_as_cfa=True,
            cfa_tier=assigned_tier,
            cancelled_pick_round=cancelled_round,
            projected_comp_picks_lost=projected_lost,
            impact_summary=summary,
        )

    def calculate_multi_year_projection(
        self,
        proposal: MultiYearContractProposal,
    ) -> MultiYearCapProjectionResponse:
        """
        Calculate full 5-year multi-year cap schedule under CBA Article 13 rules.
        - Prorates signing bonus over min(real_years + void_years, 5).
        - Accelerates remaining bonus into dead money in the void year.
        - Splits dead money over 2 years if post_june_1_designation is enabled.
        """
        real_years = max(1, min(proposal.real_years, 5))
        void_years = max(0, min(proposal.void_years, 4))

        # CBA Article 13 Section 5(c): Max 5-year proration ceiling
        proration_years = min(real_years + void_years, 5)
        annual_proration = proposal.signing_bonus_total // proration_years if proration_years > 0 else 0

        # Existing payroll commitments for 5 projected years
        committed_schedule = self.get_team_payroll_commitments(proposal.team_id)

        yearly_schedule: List[YearlyCapLiability] = []
        accelerated_dead_money_void_year = 0

        # Unamortized bonus remaining when real contract years expire
        remaining_unamortized_years = max(0, proration_years - real_years)
        total_accelerated_bonus = annual_proration * remaining_unamortized_years

        for i in range(5):
            cal_year = BASE_LEAGUE_YEAR + i
            projected_cap = self.get_projected_cap(i)
            committed_sal = committed_schedule[i]

            proposed_cap_hit = 0
            dead_money = 0
            prorated_bonus_charge = 0

            # 1. Active Contract Years (Player is playing on roster)
            if i < real_years:
                prorated_bonus_charge = annual_proration
                proposed_cap_hit = proposal.annual_base_salary + prorated_bonus_charge

            # 2. Void Year Trigger (Player's contract voids, triggering dead money acceleration)
            elif i == real_years and void_years > 0:
                if proposal.post_june_1_designation and remaining_unamortized_years > 1:
                    # Post-June 1st designation: 1 year of proration hits current year
                    dead_money = annual_proration
                else:
                    # Standard void trigger: All remaining unamortized bonus hits immediately
                    dead_money = total_accelerated_bonus
                accelerated_dead_money_void_year = dead_money

            # 3. Post-Void Second Year (if Post-June 1st designation was elected)
            elif i == (real_years + 1) and void_years > 0 and proposal.post_june_1_designation and remaining_unamortized_years > 1:
                dead_money = total_accelerated_bonus - annual_proration

            net_cap_space = projected_cap - (committed_sal + proposed_cap_hit + dead_money)
            is_compliant = net_cap_space >= 0

            yearly_schedule.append(
                YearlyCapLiability(
                    year=cal_year,
                    projected_cap=projected_cap,
                    committed_salaries=committed_sal,
                    prorated_bonus=prorated_bonus_charge,
                    proposed_contract_cap_hit=proposed_cap_hit,
                    dead_money=dead_money,
                    net_cap_space=net_cap_space,
                    is_cap_compliant=is_compliant,
                )
            )

        # Overall contract figures
        total_contract_value = (proposal.annual_base_salary * real_years) + proposal.signing_bonus_total
        aav = total_contract_value // real_years

        # Compensatory pick evaluation
        comp_impact = self.evaluate_comp_pick_formula(proposal, proposal.team_id)

        # Check compliance across all 5 years
        all_compliant = all(y.is_cap_compliant for y in yearly_schedule)

        return MultiYearCapProjectionResponse(
            player_id=proposal.player_id,
            team_id=proposal.team_id,
            total_contract_value=total_contract_value,
            annual_average_value=aav,
            proration_years_used=proration_years,
            yearly_schedule=yearly_schedule,
            accelerated_dead_money_void_year=accelerated_dead_money_void_year,
            comp_pick_impact=comp_impact,
            is_fully_compliant=all_compliant,
        )

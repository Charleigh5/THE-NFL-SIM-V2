from app.kernels.core.ecs_manager import Component
from typing import List, Dict, Tuple, Any
from pydantic import BaseModel

class ContractYear(BaseModel):
    year: int
    base_salary: float
    signing_bonus_proration: float
    roster_bonus: float
    workout_bonus: float
    
    @property
    def cap_hit(self) -> float:
        return self.base_salary + self.signing_bonus_proration + self.roster_bonus + self.workout_bonus

class CapologistPhysics(Component):
    salary_cap: float = 255.0 # Millions
    current_cap_space: float = 0.0
    dead_money_ledger: Dict[int, float] = {} # Year -> Amount

    def calculate_dead_money_acceleration(self, contract_years: List[ContractYear], current_year: int) -> float:
        """
        Directive 1: Dead Cap Accelerator.
        Instantly sums all future unamortized signing bonuses.
        """
        accelerated_amount = 0.0
        for year in contract_years:
            if year.year >= current_year:
                accelerated_amount += year.signing_bonus_proration
        return accelerated_amount

    def calculate_post_june1_dead_money(self, contract_years: List[ContractYear], current_year: int) -> Tuple[float, float]:
        """
        Directive 1b: Post-June 1st Dead Cap Split.
        When a player is designated as a post-June 1st cut, dead money from unamortized
        signing bonus is split across two league years:
        - Current league year takes only the current year's prorated signing bonus allocation.
        - Following league year absorbs the remaining unamortized signing bonus balance.

        Returns:
            Tuple[float, float]: (current_year_dead, following_year_dead)
        """
        current_year_dead = 0.0
        following_year_dead = 0.0
        for year in contract_years:
            if year.year == current_year:
                current_year_dead += year.signing_bonus_proration
            elif year.year > current_year:
                following_year_dead += year.signing_bonus_proration
        return current_year_dead, following_year_dead

    def record_post_june1_release(self, contract_years: List[ContractYear], current_year: int) -> Tuple[float, float]:
        """
        Applies a post-June 1st release to the dead_money_ledger across two league years.
        """
        current_dead, next_dead = self.calculate_post_june1_dead_money(contract_years, current_year)
        self.dead_money_ledger[current_year] = self.dead_money_ledger.get(current_year, 0.0) + current_dead
        self.dead_money_ledger[current_year + 1] = self.dead_money_ledger.get(current_year + 1, 0.0) + next_dead
        return current_dead, next_dead

    def restructure_contract(self, contract_years: List[ContractYear], current_year: int, amount_to_convert: float) -> List[ContractYear]:
        """
        Directive 2: Restructure Engine (Kick the Can).
        """
        current_contract_year = next((y for y in contract_years if y.year == current_year), None)
        if not current_contract_year or current_contract_year.base_salary < amount_to_convert:
            raise ValueError("Insufficient base salary to restructure")

        current_contract_year.base_salary -= amount_to_convert
        remaining_years = [y for y in contract_years if y.year >= current_year]
        proration_per_year = amount_to_convert / len(remaining_years)

        for year in remaining_years:
            year.signing_bonus_proration += proration_per_year
            
        return contract_years

    def check_financial_risk(self, dead_cap_hit: float) -> float:
        """
        Directive 3: Financial Risk in Utility AI.
        """
        risk_ratio = dead_cap_hit / self.salary_cap
        if risk_ratio > 0.15: return 1.0 # Extreme Risk
        elif risk_ratio > 0.05: return 0.5 # Moderate Risk
        return 0.1 # Low Risk

    def validate_trade_financials(self, team_cap_space: float, incoming_contracts_value: float) -> Tuple[bool, str]:
        """
        Directive 14: Server-Authoritative Validation.
        Ensures trades are mathematically legal under the cap.
        """
        if incoming_contracts_value > team_cap_space:
            return False, f"Trade Rejected: Incoming salary {incoming_contracts_value}M exceeds cap space {team_cap_space}M"
        return True, "Trade Valid"


def calculate_post_june1_dead_money(contract: Any, cut_year: int) -> Tuple[float, float]:
    """
    Module-level function calculating post-June 1st dead money split.
    Compatible with ContractYear lists or Contract objects with a .years attribute.
    """
    if isinstance(contract, list):
        years = contract
    elif hasattr(contract, "years"):
        years = getattr(contract, "years", [])
    else:
        years = []

    current_year_dead = 0.0
    following_year_dead = 0.0
    for y in years:
        y_num = getattr(y, "year", None)
        proration = getattr(y, "signing_bonus_proration", None)
        if proration is None:
            proration = getattr(y, "signing_bonus_prorate", 0.0)

        if y_num == cut_year:
            current_year_dead += float(proration)
        elif y_num is not None and y_num > cut_year:
            following_year_dead += float(proration)

    return current_year_dead, following_year_dead

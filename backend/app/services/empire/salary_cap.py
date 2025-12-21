#!/usr/bin/env python3
"""
Salary Cap Engine Module
========================
NFL salary cap and contract mechanics.

Phase 5: EMPIRE Economic Simulation
- Dynamic cap growth
- Contract structures
- Dead money calculations
- Cap space projections
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from datetime import date


# ============================================================================
# ENUMS
# ============================================================================

class ContractType(str, Enum):
    """Types of player contracts."""
    ROOKIE = "ROOKIE"          # Slotted rookie deal
    VETERAN = "VETERAN"        # Standard vet contract
    FRANCHISE_TAG = "FRANCHISE_TAG"
    TRANSITION_TAG = "TRANSITION_TAG"
    MINIMUM = "MINIMUM"        # Veteran minimum
    PRACTICE_SQUAD = "PRACTICE_SQUAD"


class CapChargeType(str, Enum):
    """Types of cap charges."""
    BASE_SALARY = "BASE_SALARY"
    SIGNING_BONUS = "SIGNING_BONUS"
    ROSTER_BONUS = "ROSTER_BONUS"
    OPTION_BONUS = "OPTION_BONUS"
    INCENTIVE = "INCENTIVE"
    DEAD_MONEY = "DEAD_MONEY"


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass(frozen=True)
class SalaryCapConfig:
    """Configuration for salary cap engine."""
    # Cap floor (minimum spending requirement)
    cap_floor_percentage: float = 0.89  # 89% of cap

    # Rookie wage scale (4 years)
    rookie_contract_years: int = 4

    # Franchise tag percentages (by position)
    franchise_tag_percentages: Dict[str, float] = field(default_factory=lambda: {
        "QB": 0.08,
        "RB": 0.06,
        "WR": 0.07,
        "TE": 0.065,
        "OL": 0.065,
        "DL": 0.065,
        "LB": 0.06,
        "CB": 0.065,
        "S": 0.055,
        "K": 0.03,
        "P": 0.03,
    })

    # Cap carryover limits
    max_cap_carryover: float = float('inf')  # No max in NFL


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ContractYear:
    """Single year of a contract."""
    year: int                    # 1, 2, 3, etc.
    base_salary: int             # In dollars
    signing_bonus_prorate: int = 0
    roster_bonus: int = 0
    option_bonus: int = 0
    workout_bonus: int = 0
    incentives_likely: int = 0
    incentives_unlikely: int = 0
    is_guaranteed: bool = False
    is_void: bool = False        # Void years for spreading bonus

    @property
    def cap_hit(self) -> int:
        """Total cap charge for this year."""
        if self.is_void:
            return self.signing_bonus_prorate
        return (
            self.base_salary +
            self.signing_bonus_prorate +
            self.roster_bonus +
            self.option_bonus +
            self.workout_bonus +
            self.incentives_likely
        )

    @property
    def cash_value(self) -> int:
        """Actual cash paid this year."""
        if self.is_void:
            return 0
        return (
            self.base_salary +
            self.roster_bonus +
            self.option_bonus +
            self.workout_bonus
        )


@dataclass
class Contract:
    """Full player contract."""
    player_id: str
    contract_type: ContractType
    total_value: int             # Total contract value
    guaranteed: int              # Total guaranteed
    years: List[ContractYear] = field(default_factory=list)
    signed_date: Optional[date] = None

    @property
    def current_year(self) -> int:
        """Current contract year (1-indexed)."""
        # Simplified - would use actual date in production
        return 1

    @property
    def remaining_value(self) -> int:
        """Value remaining on contract."""
        current = self.current_year
        return sum(y.cap_hit for y in self.years if y.year >= current)

    @property
    def remaining_guaranteed(self) -> int:
        """Guaranteed money remaining."""
        return sum(
            y.cap_hit for y in self.years
            if y.is_guaranteed and y.year >= self.current_year
        )

    def get_dead_money(self, cut_after_year: int) -> int:
        """Calculate dead money if cut after given year."""
        # All prorated signing bonus accelerates
        remaining_prorate = sum(
            y.signing_bonus_prorate for y in self.years
            if y.year > cut_after_year
        )
        return remaining_prorate


@dataclass
class TeamCapState:
    """Team's salary cap state."""
    team_id: str
    season_year: int
    salary_cap: int              # This year's cap

    # Spending breakdown
    active_cap: int = 0          # Active roster cap
    dead_money: int = 0          # Dead money from cuts
    carryover: int = 0           # Unused cap from last year

    # Contracts
    contracts: Dict[str, Contract] = field(default_factory=dict)

    @property
    def total_cap(self) -> int:
        """Total available cap including carryover."""
        return self.salary_cap + self.carryover

    @property
    def cap_used(self) -> int:
        """Total cap space used."""
        return self.active_cap + self.dead_money

    @property
    def cap_space(self) -> int:
        """Available cap space."""
        return self.total_cap - self.cap_used


# ============================================================================
# SALARY CAP ENGINE
# ============================================================================

class SalaryCapEngine:
    """
    NFL salary cap management engine.

    Handles:
    - Cap calculations
    - Contract creation
    - Dead money
    - Cap projections
    """

    def __init__(self, config: Optional[SalaryCapConfig] = None):
        self.config = config or SalaryCapConfig()

    def create_contract(
        self,
        player_id: str,
        contract_type: ContractType,
        total_value: int,
        years: int,
        guaranteed: int,
        signing_bonus: int = 0,
        front_loaded: bool = False,
        back_loaded: bool = False,
    ) -> Contract:
        """
        Create a new contract with specified structure.

        Args:
            player_id: Player identifier
            contract_type: Type of contract
            total_value: Total contract value
            years: Number of years
            guaranteed: Total guaranteed money
            signing_bonus: Upfront signing bonus
            front_loaded: Higher salary in early years
            back_loaded: Higher salary in later years
        """
        # Calculate base salary distribution
        remaining_value = total_value - signing_bonus

        if front_loaded:
            # Decrease each year
            weights = [years - i for i in range(years)]
        elif back_loaded:
            # Increase each year
            weights = [i + 1 for i in range(years)]
        else:
            # Even distribution
            weights = [1] * years

        total_weight = sum(weights)
        base_salaries = [
            int(remaining_value * w / total_weight)
            for w in weights
        ]

        # Prorate signing bonus across years (max 5 years in NFL)
        prorate_years = min(years, 5)
        prorate_per_year = signing_bonus // prorate_years if prorate_years > 0 else 0

        # Determine guaranteed years
        guaranteed_remaining = guaranteed - signing_bonus

        contract_years = []
        for i in range(years):
            year_guaranteed = guaranteed_remaining > 0
            if year_guaranteed:
                guaranteed_remaining -= base_salaries[i]

            contract_years.append(ContractYear(
                year=i + 1,
                base_salary=base_salaries[i],
                signing_bonus_prorate=prorate_per_year if i < prorate_years else 0,
                is_guaranteed=year_guaranteed,
            ))

        return Contract(
            player_id=player_id,
            contract_type=contract_type,
            total_value=total_value,
            guaranteed=guaranteed,
            years=contract_years,
            signed_date=date.today(),
        )

    def create_rookie_contract(
        self,
        player_id: str,
        draft_position: int,
    ) -> Contract:
        """
        Create slotted rookie contract.

        Value based on draft position.
        """
        # Simplified rookie wage scale (approximate values)
        if draft_position == 1:
            total, guaranteed, bonus = 40_000_000, 30_000_000, 25_000_000
        elif draft_position <= 10:
            total = 35_000_000 - (draft_position - 1) * 2_000_000
            guaranteed = int(total * 0.75)
            bonus = int(total * 0.6)
        elif draft_position <= 32:
            total = 20_000_000 - (draft_position - 10) * 500_000
            guaranteed = int(total * 0.7)
            bonus = int(total * 0.5)
        else:
            # Day 2-3 picks
            total = 10_000_000 - min(draft_position - 32, 200) * 30_000
            guaranteed = int(total * 0.6)
            bonus = int(total * 0.4)

        total = max(total, 3_000_000)

        return self.create_contract(
            player_id=player_id,
            contract_type=ContractType.ROOKIE,
            total_value=total,
            years=4,
            guaranteed=guaranteed,
            signing_bonus=bonus,
        )

    def calculate_franchise_tag(
        self,
        position: str,
        salary_cap: int,
        top_5_avg: Optional[int] = None,
    ) -> int:
        """
        Calculate franchise tag value.

        Higher of:
        - Top 5 at position average
        - Position percentage of cap
        """
        pct = self.config.franchise_tag_percentages.get(position, 0.06)
        cap_percentage_value = int(salary_cap * pct)

        if top_5_avg:
            return max(cap_percentage_value, top_5_avg)
        return cap_percentage_value

    def calculate_dead_money(
        self,
        contract: Contract,
        cut_after_year: int,
    ) -> int:
        """Calculate dead money from cutting a player."""
        return contract.get_dead_money(cut_after_year)

    def calculate_cap_savings(
        self,
        contract: Contract,
        cut_after_year: int,
    ) -> int:
        """Calculate cap savings from cutting a player."""
        if cut_after_year >= len(contract.years):
            return 0

        # Next year's cap hit - dead money
        next_year = contract.years[cut_after_year]
        dead = self.calculate_dead_money(contract, cut_after_year)

        return next_year.cap_hit - dead

    def restructure_contract(
        self,
        contract: Contract,
        reduce_base_by: int,
        current_year: int,
    ) -> Contract:
        """
        Convert base salary to signing bonus.

        Spreads cap hit over remaining years.
        """
        if current_year > len(contract.years):
            return contract

        current = contract.years[current_year - 1]

        # Convert base to bonus
        actual_reduction = min(reduce_base_by, current.base_salary)
        current.base_salary -= actual_reduction

        # Prorate over remaining years (max 5)
        remaining = len(contract.years) - current_year + 1
        prorate_years = min(remaining, 5)
        prorate = actual_reduction // prorate_years

        # Add to signing bonus prorate of remaining years
        for i in range(current_year - 1, min(current_year - 1 + prorate_years, len(contract.years))):
            contract.years[i].signing_bonus_prorate += prorate

        return contract

    def get_historical_cap(self, year: int) -> Optional[int]:
        """
        Get the actual NFL salary cap for a historical year.

        Uses real NFL data from 1994-2025.
        Returns None for 2010 (uncapped year) or years before 1994.
        """
        from app.core.nfl_reference_data import HISTORICAL_SALARY_CAPS
        return HISTORICAL_SALARY_CAPS.get(year)

    def get_cap_for_season(self, year: int) -> int:
        """
        Get salary cap for a season, using historical data when available,
        or projecting forward for future years.
        """
        from app.core.nfl_reference_data import HISTORICAL_SALARY_CAPS, SALARY_CAP_CAGR

        # Use historical data if available
        historical = HISTORICAL_SALARY_CAPS.get(year)
        if historical is not None:
            return historical

        # For years before 1994 or after 2025, project from 2025
        base_year = 2025
        base_cap = HISTORICAL_SALARY_CAPS[base_year]
        if base_cap is None:
            base_cap = 279_200_000

        years_diff = year - base_year
        if years_diff > 0:
            # Project forward
            return int(base_cap * ((1 + SALARY_CAP_CAGR) ** years_diff))
        else:
            # Year before 1994, just return 1994 value
            return HISTORICAL_SALARY_CAPS.get(1994, 34_600_000) or 34_600_000

    def project_cap(
        self,
        current_cap: int,
        years_ahead: int,
    ) -> List[int]:
        """
        Project future salary caps.

        Uses real NFL CAGR (6.97%) from reference data.
        """
        from app.core.nfl_reference_data import SALARY_CAP_CAGR

        caps = [current_cap]
        for _ in range(years_ahead):
            caps.append(int(caps[-1] * (1 + SALARY_CAP_CAGR)))
        return caps[1:]

    def get_cap_summary(self, state: TeamCapState) -> Dict[str, Any]:
        """Get summary of team's cap situation."""
        return {
            "team_id": state.team_id,
            "season": state.season_year,
            "salary_cap": state.salary_cap,
            "carryover": state.carryover,
            "total_cap": state.total_cap,
            "active_cap": state.active_cap,
            "dead_money": state.dead_money,
            "cap_space": state.cap_space,
            "contracts_count": len(state.contracts),
        }


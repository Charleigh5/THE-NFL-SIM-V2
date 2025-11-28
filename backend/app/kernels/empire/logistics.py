from app.kernels.core.ecs_manager import Component
from typing import Dict
from pydantic import Field

class LogisticsEngine(Component):
    # Directive 7: Jock Tax Algorithm
    state_tax_rates: Dict[str, float] = {
        "CA": 0.133, "NY": 0.109, "FL": 0.0, "TX": 0.0, "IL": 0.0495
    }
    
    # Directive 11: Jet Lag
    current_location: str = "Home"
    accumulated_travel_miles: float = 0.0
    circadian_rhythm_penalty: float = 0.0

    def calculate_net_income(self, gross_salary: float, state: str) -> float:
        """
        Directive 7: Calculates real income after Jock Tax.
        """
        tax_rate = self.state_tax_rates.get(state, 0.05) # Default 5%
        return gross_salary * (1.0 - tax_rate)

    def update_travel_fatigue(self, miles_traveled: float, time_zones_crossed: int):
        """
        Directive 11: Jet Lag.
        """
        self.accumulated_travel_miles += miles_traveled
        # 1 Time Zone = 10% penalty recovery delay
        self.circadian_rhythm_penalty = time_zones_crossed * 0.10

class StadiumManager(Component):
    # Directive 9: Stadium Renovation & Upgrades
    stadium_condition: float = 100.0
    renovation_budget: float = 0.0
    
    def perform_renovation(self, cost: float, quality_boost: float):
        if self.renovation_budget >= cost:
            self.renovation_budget -= cost
            self.stadium_condition = min(100.0, self.stadium_condition + quality_boost)
            return True
        return False

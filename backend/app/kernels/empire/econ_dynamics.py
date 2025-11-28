from app.kernels.core.ecs_manager import Component

class CapPhysicist(Component):
    salary_cap: float = 255.0 # In Millions
    dead_money: float = 0.0
    committed_cap: float = 0.0

    def calculate_dead_money_acceleration(self, contract: dict, years_remaining: int) -> float:
        # Accelerate all remaining signing bonus
        bonus_per_year = contract.get("signing_bonus", 0) / contract.get("length", 1)
        return bonus_per_year * years_remaining

class MarketInflator(Component):
    inflation_rate: float = 1.05 # 5% yearly increase

    def adjust_contract_demand(self, base_demand: float, position: str) -> float:
        # QB tax, inflation adjustment
        multiplier = 1.2 if position == "QB" else 1.0
        return base_demand * self.inflation_rate * multiplier


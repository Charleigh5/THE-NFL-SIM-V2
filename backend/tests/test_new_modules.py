import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.data.helmets import HELMET_CATALOG
from app.data.stadiums import STADIUM_DB
from app.kernels.empire.capologist import CapologistPhysics, ContractYear
from app.kernels.cortex.strategy import StrategyEngine, PersonnelGrouping, DefensiveScheme
from app.kernels.cortex.coverage_net import CoverageNet

def test_new_modules():
    print("Testing Reference Data, Capologist, and Strategy...")
    
    # 1. Reference Data
    print(f"Data: Loaded {len(HELMET_CATALOG)} Helmets")
    print(f"Data: Loaded {len(STADIUM_DB)} Stadiums")
    print(f"Data: SoFi Capacity {STADIUM_DB['SOFI'].capacity}")

    # 2. Capologist Physics
    cap = CapologistPhysics()
    contract = [
        ContractYear(year=2025, base_salary=1.0, signing_bonus_proration=5.0, roster_bonus=0, workout_bonus=0),
        ContractYear(year=2026, base_salary=10.0, signing_bonus_proration=5.0, roster_bonus=0, workout_bonus=0),
        ContractYear(year=2027, base_salary=12.0, signing_bonus_proration=5.0, roster_bonus=0, workout_bonus=0)
    ]
    dead_money = cap.calculate_dead_money_acceleration(contract, 2025)
    print(f"Empire: Dead Money Acceleration {dead_money}M")
    
    restructured = cap.restructure_contract(contract, 2026, 9.0)
    print(f"Empire: Restructured 2026 Base {restructured[1].base_salary}M")
    print(f"Empire: Restructured 2026 Bonus {restructured[1].signing_bonus_proration}M")

    # 3. Strategy Engine
    strat = StrategyEngine()
    multiplier = strat.get_schematic_multiplier("INSIDE_ZONE", "RUN_COMMIT")
    print(f"Strategy: Run vs Run Commit Multiplier {multiplier}")
    
    matchup_val = strat.resolve_matchup(PersonnelGrouping.P21, DefensiveScheme.DIME)
    print(f"Strategy: 21 Personnel vs Dime Advantage {matchup_val}")

    # 4. Coverage Models
    cov = CoverageNet()
    defenders = [{'id': 'd1', 'x': 10, 'y': 10}, {'id': 'd2', 'x': 20, 'y': 20}]
    trajectory = {'arrival_x': 12, 'arrival_y': 12}
    target = cov.identify_targeted_defender(trajectory, defenders)
    print(f"Coverage: Targeted Defender {target}")

    print("ALL NEW MODULES VERIFIED")

if __name__ == "__main__":
    test_new_modules()

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.empire.capologist import CapologistPhysics, ContractYear
from app.kernels.empire.logistics import LogisticsEngine, StadiumManager
from app.kernels.empire.owner_ai import OwnerMind, OwnerPersonality

def test_empire_omniscient():
    print("Testing Empire Engine Directives...")
    
    # 1. Capologist
    cap = CapologistPhysics(salary_cap=255.0)
    contract = [
        ContractYear(year=2025, base_salary=1.0, signing_bonus_proration=5.0, roster_bonus=0, workout_bonus=0),
        ContractYear(year=2026, base_salary=10.0, signing_bonus_proration=5.0, roster_bonus=0, workout_bonus=0)
    ]
    
    dead_money = cap.calculate_dead_money_acceleration(contract, 2025)
    print(f"Directive 1: Dead Money Acceleration (2025+) -> {dead_money}M")
    assert dead_money == 10.0 # 5.0 + 5.0
    
    valid, msg = cap.validate_trade_financials(team_cap_space=5.0, incoming_contracts_value=6.0)
    print(f"Directive 14: Trade Validation (Cap 5.0, Incoming 6.0) -> {msg}")
    assert valid is False

    # 2. Logistics
    logistics = LogisticsEngine()
    net_income = logistics.calculate_net_income(10.0, "CA")
    print(f"Directive 7: Jock Tax CA (13.3%) on 10M -> Net {net_income:.2f}M")
    assert net_income < 9.0
    
    logistics.update_travel_fatigue(miles_traveled=3000, time_zones_crossed=3)
    print(f"Directive 11: Jet Lag (3 TZ) -> Penalty {logistics.circadian_rhythm_penalty}")
    assert round(logistics.circadian_rhythm_penalty, 2) == 0.30

    # 3. Owner AI
    owner = OwnerMind(personality=OwnerPersonality.WIN_NOW)
    security = owner.evaluate_job_security(wins=8, playoff_berth=False)
    print(f"Directive 4: Win Now Owner (No Playoffs) -> Job Security {security}")
    assert security < 50.0
    
    meddler = OwnerMind(personality=OwnerPersonality.MEDDLER)
    meddler.issue_mandate(["QB"])
    print(f"Directive 20: Meddler Owner Mandates -> {meddler.active_mandates}")
    assert "Draft QB in Round 1" in meddler.active_mandates

    print("ALL EMPIRE DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_empire_omniscient()

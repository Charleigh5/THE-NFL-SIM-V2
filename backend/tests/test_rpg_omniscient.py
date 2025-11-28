import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.rpg.training import TrainingEngine
from app.kernels.rpg.progression import ProgressionSys

def test_rpg_omniscient():
    print("Testing RPG Engine Directives...")
    
    # 1. Training
    train = TrainingEngine()
    xp = train.train_player(intensity=1.0, injury_risk_mult=1.0)
    print(f"Directive 1: High Intensity Training -> XP {xp}, Fatigue {train.current_fatigue}")
    assert xp == 10.0
    assert train.current_fatigue == 5.0
    
    # 2. Progression
    prog = ProgressionSys(work_ethic=1.5) # Gym Rat
    prog.add_xp(100.0)
    print(f"Directive 5: XP 100 * Work Ethic 1.5 -> Current XP {prog.current_xp}")
    assert prog.current_xp == 150
    
    regression = prog.apply_regression(age=35)
    print(f"Directive 16: Age 35 Regression Check -> {regression}")
    # Random chance, so we just check it runs without error

    print("ALL RPG DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_rpg_omniscient()

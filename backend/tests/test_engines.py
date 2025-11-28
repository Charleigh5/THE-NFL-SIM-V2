import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.physics import BallPhysics, Vector3
from app.engine.blocking import BlockingEngine
from app.engine.defense import PassRushEngine, PassRushMove
from app.engine.special_teams import SpecialTeamsEngine
from app.rpg.progression import ProgressionEngine

def test_ball_physics():
    print("Testing Ball Physics...")
    traj = BallPhysics.calculate_trajectory(v0=25, angle_deg=45, spiral_efficiency=1.0)
    print(f"  Trajectory points: {len(traj)}")
    print(f"  Final distance: {traj[-1]['x']}m")
    assert len(traj) > 0
    assert traj[-1]['x'] > 0

def test_blocking():
    print("\nTesting Blocking Engine...")
    res = BlockingEngine.resolve_pass_block(ol_rating=80, dl_rating=75, ol_technique="KickStep")
    print(f"  Pass Block Result: {res}")
    
    run_res = BlockingEngine.resolve_run_block(ol_strength=80, dl_anchor=70, scheme="Zone")
    print(f"  Run Block Result: {run_res}")
    assert run_res['displacement'] > 0

def test_pass_rush():
    print("\nTesting Pass Rush...")
    res = PassRushEngine.resolve_move(PassRushMove.BULL_RUSH, rusher_rating=90, blocker_rating=80, blocker_weight=300, rusher_strength=95)
    print(f"  Bull Rush Result: {res}")

def test_special_teams():
    print("\nTesting Special Teams...")
    kick = SpecialTeamsEngine.calculate_kick(power=90, accuracy=95, kick_type="FieldGoal")
    print(f"  Kick Distance: {kick['distance']}m")
    print(f"  Hang Time: {kick['hang_time']}s")

def test_rpg():
    print("\nTesting RPG Engine...")
    xp = ProgressionEngine.calculate_xp_gain({"pass_tds": 3, "pass_yards": 300}, "QB")
    print(f"  QB XP Gain: {xp}")
    assert xp > 0

if __name__ == "__main__":
    try:
        test_ball_physics()
        test_blocking()
        test_pass_rush()
        test_special_teams()
        test_rpg()
        print("\nALL TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        exit(1)

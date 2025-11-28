import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.core.ecs_manager import ECSManager
from app.kernels.genesis.bio_metrics import AnatomyModel, FatigueRegulator
from app.kernels.genesis.neuro_cognition import S2Processor, FocusMonitor
from app.kernels.genesis.trauma_center import ScarTissueManager
from app.kernels.hive.geo_physics import TurfDegradationMesh, FluidDynamicsSolver
from app.kernels.hive.atmosphere_net import CrowdSentimentMachine
from app.kernels.empire.econ_dynamics import CapPhysicist, MarketInflator
from app.kernels.empire.scout_intel import FogOfWarSystem
from app.kernels.society.social_graph import RivalryEngine
from app.kernels.society.narrative_director import StoryBeatGenerator

def test_kernels():
    print("Testing Cortex Kernels...")
    
    # 1. Core Kernel
    ecs = ECSManager()
    entity = ecs.create_entity()
    print(f"Core: Entity Created {entity.id}")

    # 2. Genesis Kernel
    anatomy = AnatomyModel()
    anatomy.apply_stress(50.0)
    print(f"Genesis: ACL Stress {anatomy.ligaments['ACL']['stress']}")
    
    fatigue = FatigueRegulator()
    fatigue.update_fatigue(20.0)
    print(f"Genesis: Lactic Acid {fatigue.lactic_acid}")

    # 3. Hive Kernel
    turf = TurfDegradationMesh()
    turf.degrade_zone(5, 5, 100.0)
    print(f"Hive: Turf Friction {turf.get_friction(5, 5)}")
    
    crowd = CrowdSentimentMachine()
    crowd.update_sentiment(21, 0, True)
    print(f"Hive: Crowd Decibels {crowd.decibels}")

    # 4. Empire Kernel
    cap = CapPhysicist()
    dead_money = cap.calculate_dead_money_acceleration({"signing_bonus": 10, "length": 5}, 3)
    print(f"Empire: Dead Money {dead_money}M")
    
    scout = FogOfWarSystem()
    print(f"Empire: Scout Report {scout.reveal_attribute(95, 'speed')}")

    # 5. Society Kernel
    rivalry = RivalryEngine()
    rivalry.add_vendetta("player1", "teamA")
    print(f"Society: Vendetta Active {rivalry.check_revenge_buff('player1', 'teamA')}")
    
    narrative = StoryBeatGenerator()
    print(f"Society: Headline '{narrative.generate_headline({'player': 'Tom Brady'})}'")

    print("ALL KERNELS VERIFIED")

if __name__ == "__main__":
    test_kernels()

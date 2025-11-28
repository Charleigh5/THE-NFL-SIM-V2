import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.core.sim_engine import SimEngine, ECSManager
from app.kernels.core.ai_kernel import AIKernel, Selector, NodeStatus, BehaviorNode

class MockAction(BehaviorNode):
    def tick(self, context):
        return NodeStatus.SUCCESS

def test_core_omniscient():
    print("Testing Core Engine Directives...")
    
    # 1. ECS & Sim Loop
    ecs = ECSManager()
    sim = SimEngine()
    print(f"Directive 2: Time Step -> {sim.time_step}s (10Hz)")
    assert sim.time_step == 0.1
    
    # 2. AI Kernel
    ai = AIKernel()
    
    # Directive 5: Modular BT
    root = Selector([MockAction()])
    ai.behavior_trees["entity_1"] = root
    
    # Directive 4: VIP Profile
    ai.register_vip_profile("entity_1", {"Aggression": 0.9})
    print(f"Directive 4: VIP Profile -> {ai.vip_profiles['entity_1']}")
    assert ai.vip_profiles['entity_1']['Aggression'] == 0.9
    
    # Run Update
    ai.update(0.1)
    print("Directive 18: AI Update Loop Ran Successfully")
    
    # Directive 7: LSTM
    prediction = ai.get_strategic_prediction({})
    print(f"Directive 7: LSTM Prediction (Unloaded) -> {prediction}")
    assert prediction == "Random"

    print("ALL CORE DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_core_omniscient()

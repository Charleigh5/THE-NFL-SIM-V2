from app.kernels.core.ecs_manager import Component
from typing import List, Dict, Any
from enum import Enum

class NodeStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

class BehaviorNode:
    def tick(self, context: Any) -> NodeStatus:
        raise NotImplementedError

class Selector(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children = children
    
    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE

class Sequence(BehaviorNode):
    def __init__(self, children: List[BehaviorNode]):
        self.children = children
    
    def tick(self, context: Any) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

class AIKernel(Component):
    model_config = {"arbitrary_types_allowed": True}
    # Directive 5: Modular Behavior Trees
    behavior_trees: Dict[str, BehaviorNode] = {} # EntityID -> RootNode
    
    # Directive 4: VIP Replication
    vip_profiles: Dict[str, Dict[str, float]] = {} # EntityID -> {Tendency: Value}
    
    # Directive 7: LSTM Strategic Inference (Mock)
    strategy_model_loaded: bool = False

    def register_vip_profile(self, entity_id: str, profile: Dict[str, float]):
        self.vip_profiles[entity_id] = profile

    def update(self, dt: float):
        # Directive 18: Thread Pooling (Simulated here)
        for entity_id, tree in self.behavior_trees.items():
            context = {"dt": dt, "vip": self.vip_profiles.get(entity_id, {})}
            tree.tick(context)

    def get_strategic_prediction(self, game_state: Dict) -> str:
        """
        Directive 7: LSTM Inference.
        """
        if not self.strategy_model_loaded:
            return "Random"
        return "Pass"

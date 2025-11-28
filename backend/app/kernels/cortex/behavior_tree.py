from app.kernels.core.ecs_manager import Component
import enum

class NodeStatus(str, enum.Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    RUNNING = "Running"

class BehaviorNode:
    def tick(self, context: dict) -> NodeStatus:
        raise NotImplementedError

class BehaviorTree(Component):
    def __init__(self, root_node: BehaviorNode):
        self.root = root_node
        self.context = {}

    def update(self):
        self.root.tick(self.context)

class Selector(BehaviorNode):
    def __init__(self, children: list):
        self.children = children

    def tick(self, context: dict) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE

class Sequence(BehaviorNode):
    def __init__(self, children: list):
        self.children = children

    def tick(self, context: dict) -> NodeStatus:
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

from app.kernels.core.ecs_manager import Component
from typing import List, Dict
import time

class ECSManager:
    # Directive 1: ECS Architecture (Cache Locality)
    # Simplified: Using Dicts for components, but structured for iteration
    components: Dict[str, Dict[str, Component]] = {} # ComponentType -> EntityID -> Component

    def add_component(self, entity_id: str, component: Component):
        comp_type = type(component).__name__
        if comp_type not in self.components:
            self.components[comp_type] = {}
        self.components[comp_type][entity_id] = component

    def get_component(self, entity_id: str, comp_type: str) -> Component:
        return self.components.get(comp_type, {}).get(entity_id)

class SimEngine:
    # Directive 2: Fixed Time-Step (10Hz)
    target_fps: int = 10
    time_step: float = 1.0 / 10.0
    
    # Directive 9: Decoupled Physics/AI Kernels
    physics_kernel: 'PhysicsKernel' = None
    ai_kernel: 'AIKernel' = None

    def run_loop(self, duration_seconds: float):
        steps = int(duration_seconds / self.time_step)
        for _ in range(steps):
            self.update(self.time_step)

    def update(self, dt: float):
        # Directive 3: Event-Driven Architecture
        # 1. AI Think
        if self.ai_kernel: self.ai_kernel.update(dt)
        # 2. Physics Move
        if self.physics_kernel: self.physics_kernel.update(dt)

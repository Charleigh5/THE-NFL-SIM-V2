from typing import Dict, List, Type, Any, Optional
import uuid
from pydantic import BaseModel

class Component(BaseModel):
    pass

class Entity(BaseModel):
    id: str
    components: Dict[str, Component] = {}

    def add_component(self, component: Component):
        self.components[component.__class__.__name__] = component

    def get_component(self, component_type: Type[Component]) -> Optional[Component]:
        return self.components.get(component_type.__name__)

class System:
    def update(self, entities: List[Entity], dt: float):
        raise NotImplementedError

class ECSManager:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.systems: List[System] = []

    def create_entity(self) -> Entity:
        entity_id = str(uuid.uuid4())
        entity = Entity(id=entity_id)
        self.entities[entity_id] = entity
        return entity

    def add_system(self, system: System):
        self.systems.append(system)

    def update(self, dt: float):
        # Run systems in strict order: Bio -> Physics -> AI -> Logic
        for system in self.systems:
            system.update(list(self.entities.values()), dt)

from app.kernels.core.ecs_manager import Component
import random
from typing import Dict

class FogOfWarSystem(Component):
    scouting_points: int = 0
    confidence_levels: Dict[str, float] = {
        "speed": 0.2, # Low confidence (wide range)
        "strength": 0.2
    }

    def reveal_attribute(self, true_value: int, attribute: str) -> str:
        confidence = self.confidence_levels.get(attribute, 0.2)
        margin = int((1.0 - confidence) * 20) # e.g. 0.2 conf -> +/- 16
        
        min_val = max(0, true_value - margin)
        max_val = min(100, true_value + margin)
        
        return f"{min_val}-{max_val} (Conf: {int(confidence*100)}%)"

class PsychProfiler(Component):
    def generate_archetype(self) -> str:
        archetypes = ["Mercenary", "Hometown Hero", "Ring Chaser", "Secure Bag"]
        return random.choice(archetypes)


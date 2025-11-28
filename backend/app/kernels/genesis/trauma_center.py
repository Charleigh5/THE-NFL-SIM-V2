from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Optional
from pydantic import Field

class TraumaModel(Component):
    # Directive 8: Medical Fog of War
    hidden_injury_flags: List[str] = Field(default_factory=list) # e.g. "Degenerative Knee"
    mri_revealed: bool = False
    
    # Directive 9: Painkiller Trade-Off
    painkiller_active: bool = False
    
    def reveal_flags(self) -> List[str]:
        """
        Only reveals flags if MRI has been performed (Directive 8).
        """
        if self.mri_revealed:
            return self.hidden_injury_flags
        return []

    def administer_shot(self, anatomy: 'AnatomyModel'):
        """
        Directive 9: The Shot.
        Sets currentHealth to 100% but increases chronicWear by +15.
        """
        self.painkiller_active = True
        anatomy.current_health = 100.0
        anatomy.chronic_wear += 15.0

class ScarTissueManager(Component):
    scars: Dict[str, float] = Field(default_factory=dict) # BodyPart -> StructuralIntegrityPenalty

    def add_scar(self, body_part: str, severity: float):
        current_penalty = self.scars.get(body_part, 0.0)
        # Scars accumulate but have diminishing returns
        self.scars[body_part] = min(50.0, current_penalty + severity)

    def get_structural_integrity(self, body_part: str) -> float:
        return 100.0 - self.scars.get(body_part, 0.0)

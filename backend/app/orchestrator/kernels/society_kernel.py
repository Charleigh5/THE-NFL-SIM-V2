from typing import Dict, Any
from app.kernels.society import TrustGraph, DirectorAI

class SocietyKernel:
    """
    Facade for the Society (Narrative/Chemistry) Engine.
    Manages player relationships and game narratives.
    """
    def __init__(self):
        self.trust_graph = TrustGraph()
        self.director = DirectorAI()

    def update_narrative(self, event_data: Dict[str, Any]):
        if hasattr(self.director, 'process_event'):
            self.director.process_event(event_data)

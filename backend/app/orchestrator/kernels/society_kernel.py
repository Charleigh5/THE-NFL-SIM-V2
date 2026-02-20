from typing import Any

from app.kernels.society import DirectorAI, TrustGraph


class SocietyKernel:
    """
    Facade for the Society (Narrative/Chemistry) Engine.
    Manages player relationships and game narratives.
    """
    def __init__(self):
        self.trust_graph = TrustGraph()
        self.director = DirectorAI()

    def update_narrative(self, event_data: dict[str, Any]):
        if hasattr(self.director, 'process_event'):
            self.director.process_event(event_data)

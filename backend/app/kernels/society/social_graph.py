from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Tuple
from pydantic import Field
import networkx as nx

class TrustGraph(Component):
    model_config = {"arbitrary_types_allowed": True}
    # Directive 1: Weighted Undirected Trust Graph
    # Nodes = PlayerIDs, Edges = Trust (0.0 - 1.0)
    graph: nx.Graph = Field(default_factory=nx.Graph)
    
    # Directive 10: Personality DNA
    personalities: Dict[str, str] = {} # ID -> "Leader", "Volatile", "Stoic"

    def add_trust_edge(self, p1: str, p2: str, trust: float):
        self.graph.add_edge(p1, p2, weight=trust)

    def get_trust(self, p1: str, p2: str) -> float:
        if self.graph.has_edge(p1, p2):
            return self.graph[p1][p2]['weight']
        return 0.5 # Default neutral

    def trigger_mutiny_cascade(self, source_id: str, morale_hit: float) -> int:
        """
        Directive 2: Mutiny Cascade (BFS).
        Returns number of players affected.
        """
        affected_count = 0
        visited = set()
        queue = [(source_id, morale_hit)]
        
        while queue:
            current_id, current_hit = queue.pop(0)
            if current_id in visited: continue
            visited.add(current_id)
            affected_count += 1
            
            # Propagate to neighbors if trust is HIGH (shared sentiment)
            if self.graph.has_node(current_id):
                for neighbor in self.graph.neighbors(current_id):
                    trust = self.graph[current_id][neighbor]['weight']
                    if trust > 0.7: # High trust spreads mutiny
                        decayed_hit = current_hit * 0.8
                        if decayed_hit > 0.1:
                            queue.append((neighbor, decayed_hit))
                            
        return affected_count

class ChemistryLogic(Component):
    # Directive 7: QB Trust Gates Play Resolution
    def can_audible(self, qb_id: str, wr_id: str, trust_graph: TrustGraph) -> bool:
        trust = trust_graph.get_trust(qb_id, wr_id)
        return trust > 0.8 # Need high trust to change route on fly

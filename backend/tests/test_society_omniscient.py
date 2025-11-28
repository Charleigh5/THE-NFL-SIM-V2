import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.kernels.society.social_graph import TrustGraph, ChemistryLogic
from app.kernels.society.narrative import DirectorAI, NemesisSys

def test_society_omniscient():
    print("Testing Society Engine Directives...")
    
    # 1. Social Graph
    graph = TrustGraph()
    graph.add_trust_edge("p1", "p2", 0.9)
    graph.add_trust_edge("p2", "p3", 0.8)
    graph.add_trust_edge("p3", "p4", 0.2) # Low trust, stops cascade
    
    trust = graph.get_trust("p1", "p2")
    print(f"Directive 1: Trust p1-p2 -> {trust}")
    assert trust == 0.9
    
    affected = graph.trigger_mutiny_cascade("p1", morale_hit=10.0)
    print(f"Directive 2: Mutiny Cascade from p1 -> Affected {affected} nodes")
    assert affected >= 3 # p1, p2, p3 (p4 blocked by low trust)

    # 2. Chemistry
    chem = ChemistryLogic()
    can_audible = chem.can_audible("p1", "p2", graph)
    print(f"Directive 7: Audible p1-p2 (Trust 0.9) -> {can_audible}")
    assert can_audible is True

    # 3. Narrative
    director = DirectorAI()
    headline = director.generate_headline("UPSET_WIN", {"winner": "Jets", "loser": "Chiefs"})
    print(f"Directive 5: Headline -> {headline}")
    assert "Jets" in headline
    
    veto = director.check_veto("CUT_PLAYER", {"recent_superbowl_mvp": True})
    print(f"Directive 9: Veto Cut MVP -> {veto}")
    assert veto is True
    
    nemesis = NemesisSys()
    nemesis.register_rivalry("BUF", "MIA")
    print(f"Directive 4: Rivalry BUF-MIA -> {nemesis.is_rivalry_game('BUF', 'MIA')}")
    assert nemesis.is_rivalry_game("BUF", "MIA") is True

    print("ALL SOCIETY DIRECTIVES VERIFIED")

if __name__ == "__main__":
    test_society_omniscient()

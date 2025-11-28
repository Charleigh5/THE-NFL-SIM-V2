from app.kernels.core.ecs_manager import Component
from typing import List, Dict
from pydantic import Field

class NemesisSys(Component):
    # Directive 4: Nemesis System
    rivalries: Dict[str, List[str]] = {} # TeamID -> List[RivalTeamIDs]
    aggression_modifiers: Dict[str, float] = {} # MatchupKey -> Multiplier

    def register_rivalry(self, team_a: str, team_b: str):
        if team_a not in self.rivalries: self.rivalries[team_a] = []
        self.rivalries[team_a].append(team_b)
        
        key = f"{sorted([team_a, team_b])}"
        self.aggression_modifiers[key] = 1.5 # 50% more aggression/penalties

    def is_rivalry_game(self, team_a: str, team_b: str) -> bool:
        return team_b in self.rivalries.get(team_a, [])

class DirectorAI(Component):
    # Directive 5: LLM Narrative Synthesis
    active_storylines: List[str] = Field(default_factory=list)
    
    # Directive 9: Contextual Decision Veto
    veto_power_active: bool = True

    def generate_headline(self, event_type: str, context: Dict) -> str:
        """
        Placeholder for LLM Hook.
        """
        if event_type == "UPSET_WIN":
            return f"Underdogs {context['winner']} shock the world against {context['loser']}!"
        return "Breaking News"

    def check_veto(self, decision: str, context: Dict) -> bool:
        """
        Directive 9: Vetoes decisions that break immersion or narrative logic.
        e.g. Cutting a star player after a Super Bowl win.
        """
        if decision == "CUT_PLAYER" and context.get("recent_superbowl_mvp", False):
            return True # VETOED
        return False

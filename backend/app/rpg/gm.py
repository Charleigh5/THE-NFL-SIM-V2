class GMRPG:
    SKILL_TREES = {
        "Scouting": {
            "TalentSpotter": {"level": 1, "effect": {"scouting_accuracy": 10}},
            "GemFinder": {"level": 1, "effect": {"late_round_potential_reveal": True}}
        },
        "Negotiation": {
            "CapWizard": {"level": 1, "effect": {"contract_demands": -0.1}},
            "Charismatic": {"level": 1, "effect": {"free_agent_interest": 1.2}}
        }
    }
    
    @staticmethod
    def calculate_owner_trust(wins: int, profit: float, expectations: int) -> int:
        """
        Calculate change in owner trust.
        """
        trust_change = 0
        if wins >= expectations:
            trust_change += (wins - expectations) * 5
        else:
            trust_change -= (expectations - wins) * 10
            
        return trust_change

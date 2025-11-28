from app.kernels.core.ecs_manager import Component
from enum import Enum
from typing import List
from pydantic import Field

class OwnerPersonality(Enum):
    WIN_NOW = "Win Now"
    PROFIT_FIRST = "Profit First"
    REBUILDER = "Rebuilder"
    MEDDLER = "Meddler"

class OwnerMind(Component):
    # Directive 4: Owner Personality & Voting
    personality: OwnerPersonality = OwnerPersonality.WIN_NOW
    patience: float = 50.0 # 0-100
    spending_willingness: float = 50.0
    
    # Directive 20: Owner Mandates
    active_mandates: List[str] = Field(default_factory=list) # e.g. "Fire Coach", "Draft QB"

    def evaluate_job_security(self, wins: int, playoff_berth: bool) -> float:
        """
        Returns Job Security (0.0 - 100.0).
        """
        base_security = 50.0
        
        if self.personality == OwnerPersonality.WIN_NOW:
            if not playoff_berth:
                base_security -= 30.0
            else:
                base_security += 20.0
        elif self.personality == OwnerPersonality.REBUILDER:
            base_security += 20.0 # More patient
            
        return max(0.0, min(100.0, base_security))

    def issue_mandate(self, team_needs: List[str]):
        """
        Directive 20: Issues mandates based on personality.
        """
        if self.personality == OwnerPersonality.MEDDLER:
            if "QB" in team_needs:
                self.active_mandates.append("Draft QB in Round 1")

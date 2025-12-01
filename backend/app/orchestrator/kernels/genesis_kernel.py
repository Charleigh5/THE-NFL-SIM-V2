from typing import Dict, Any, List
from app.kernels.genesis.bio_metrics import AnatomyModel, FatigueRegulator

class GenesisKernel:
    """
    Facade for the Genesis (Biological/Injury) Engine.
    Manages player health, fatigue, and injury risks.
    """
    def __init__(self) -> None:
        # In a real system, this would load from a DB or state manager
        self.player_states: Dict[int, Dict[str, Any]] = {}

    def register_player(self, player_id: int, profile_data: Dict[str, Any]) -> None:
        """Initialize biological components for a player."""
        self.player_states[player_id] = {
            "anatomy": AnatomyModel(**profile_data.get("anatomy", {})),
            "fatigue": FatigueRegulator(**profile_data.get("fatigue", {}))
        }

    def calculate_fatigue(self, player_id: int, exertion: float, temperature: float) -> float:
        """
        Update and return current fatigue level for a player.
        Returns: Fatigue percentage (0.0 - 100.0)
        """
        if player_id not in self.player_states:
            return 0.0

        state = self.player_states[player_id]["fatigue"]
        state.update_fatigue(exertion, temperature)
        return state.lactic_acid

    def get_current_fatigue(self, player_id: int) -> float:
        """
        Return current fatigue level for a player without updating it.
        Returns: Fatigue percentage (0.0 - 100.0)
        """
        if player_id not in self.player_states:
            return 0.0

        state = self.player_states[player_id]["fatigue"]
        return state.lactic_acid

    def check_injury_risk(self, player_id: int, impact_force: float, body_part: str) -> Dict[str, Any]:
        """
        Evaluate injury risk based on impact.
        Returns: Dict with 'is_injured', 'injury_type', 'severity'
        """
        if player_id not in self.player_states:
            return {"is_injured": False}

        state = self.player_states[player_id]["anatomy"]
        state.apply_stress(impact_force, body_part)

        if state.current_health < 80.0:
             return {
                 "is_injured": True,
                 "injury_type": "Ligament Sprain",
                 "severity": "Low"
             }
        return {"is_injured": False}

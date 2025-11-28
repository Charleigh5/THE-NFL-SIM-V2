from typing import Dict, Any
from app.kernels.rpg.progression import ProgressionSys

class RPGKernel:
    """
    Facade for the RPG (Player Career) Engine.
    Manages individual player progression and skills.
    """
    def __init__(self):
        self.progression_systems: Dict[int, ProgressionSys] = {}

    def get_player_progression(self, player_id: int) -> ProgressionSys:
        if player_id not in self.progression_systems:
            self.progression_systems[player_id] = ProgressionSys()
        return self.progression_systems[player_id]

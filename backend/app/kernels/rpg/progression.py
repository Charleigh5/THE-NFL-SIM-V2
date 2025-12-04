from app.kernels.core.ecs_manager import Component
from typing import Dict, List, Optional
from pydantic import Field
from app.core.random_utils import DeterministicRNG

class ProgressionSys(Component):
    # Directive 3: Tiered XP Abilities
    current_xp: int = 0
    level: int = 1
    abilities: List[str] = Field(default_factory=list)

    # Directive 5: Work Ethic Modulator
    work_ethic: float = 1.0 # 0.5 (Lazy) to 1.5 (Gym Rat)

    def add_xp(self, amount: float):
        # Modulate by work ethic
        effective_xp = amount * self.work_ethic
        self.current_xp += int(effective_xp)

        # Level Up Check
        if self.current_xp >= self.level * 1000:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.current_xp = 0
        # Unlock ability logic would go here

    def apply_regression(self, age: int, rng: Optional[DeterministicRNG] = None):
        """
        Directive 16: Gradual Regression.
        One trait per season based on age.
        """
        if rng is None:
            rng = DeterministicRNG(0)

        if age > 30:
            # Regression chance increases with age
            chance = (age - 30) * 0.1
            if rng.random() < chance:
                return "Speed -1"
        return None

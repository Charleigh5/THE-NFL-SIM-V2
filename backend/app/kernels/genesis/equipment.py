from app.kernels.core.ecs_manager import Component
from typing import Dict

class EquipmentBio(Component):
    # Directive 15: Equipment Biometric Modification
    # Modifies bio-metrics based on gear (e.g. Visor = +Vision, Heavy Pads = -Speed)
    equipped_gear: Dict[str, str] = {}
    stat_modifiers: Dict[str, float] = {}

    def equip_item(self, slot: str, item_name: str, modifiers: Dict[str, float]):
        self.equipped_gear[slot] = item_name
        for stat, val in modifiers.items():
            self.stat_modifiers[stat] = self.stat_modifiers.get(stat, 0.0) + val

    def get_modified_stat(self, stat_name: str, base_value: float) -> float:
        return base_value + self.stat_modifiers.get(stat_name, 0.0)

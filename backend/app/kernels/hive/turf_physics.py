from app.kernels.core.ecs_manager import Component
from typing import List, Dict, Tuple
from pydantic import Field
import random

class TurfGrid(Component):
    # Directive 1: Turf Degradation Grid (10x10)
    # 100 zones, each with a wear level (0.0 - 1.0)
    grid_resolution: Tuple[int, int] = (10, 10)
    degradation_map: List[List[float]] = Field(default_factory=lambda: [[0.0 for _ in range(10)] for _ in range(10)])
    
    # Directive 17: Geophysical Data
    surface_type: str = "Grass" # Grass or Turf
    moisture_level: float = 0.0 # 0.0 - 1.0

    # Directive 19: Facility Upgrades
    has_heated_field: bool = False
    drainage_quality: float = 0.5 # 0.0 - 1.0

    def degrade_zone(self, x: int, y: int, intensity: float):
        """
        Directive 13: Wear Level favors Power Runners.
        High wear reduces traction for speed cuts but matters less for power runs.
        """
        if 0 <= x < 10 and 0 <= y < 10:
            # Directive 7: Rain Doubles Degradation
            weather_multiplier = 2.0 if self.moisture_level > 0.5 else 1.0
            total_degradation = intensity * weather_multiplier
            self.degradation_map[y][x] = min(1.0, self.degradation_map[y][x] + total_degradation)

    def apply_facility_upgrades(self):
        """
        Directive 19: Upgrades reduce Moisture/Friction loss.
        """
        if self.has_heated_field:
            self.moisture_level = max(0.0, self.moisture_level - 0.3) # Melts snow/dries rain
        
        self.moisture_level = max(0.0, self.moisture_level - (self.drainage_quality * 0.2))

    def get_friction_coefficient(self, x: int, y: int) -> float:
        """
        Directive 2: Slip Events.
        Friction reduces as degradation and moisture increase.
        """
        base_friction = 1.0 if self.surface_type == "Turf" else 0.9
        
        if 0 <= x < 10 and 0 <= y < 10:
            wear = self.degradation_map[y][x]
            # Directive 7: Rain Doubles Degradation Impact
            moisture_penalty = self.moisture_level * 0.3
            wear_penalty = wear * 0.2
            
            return max(0.1, base_friction - wear_penalty - moisture_penalty)
        return base_friction

    def check_slip_event(self, x: int, y: int, speed: float, cut_angle: float) -> bool:
        """
        Directive 2: Slip Logic.
        """
        friction = self.get_friction_coefficient(x, y)
        force_vector = speed * (cut_angle / 90.0) # Simplified physics
        
        # Threshold: If Force > Friction * Normal (simplified to constant)
        slip_threshold = friction * 15.0
        return force_vector > slip_threshold

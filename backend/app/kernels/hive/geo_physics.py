from app.kernels.core.ecs_manager import Component
from typing import List, Tuple

class TurfDegradationMesh(Component):
    grid: List[List[float]] = []

    def __init__(self, width: int = 53, length: int = 120, **data):
        super().__init__(**data)
        # 10x10 grid approximation for now
        if not self.grid:
             self.grid = [[1.0 for _ in range(width)] for _ in range(length)] # Friction Coeff

    def degrade_zone(self, x: int, y: int, traffic: float):
        # Friction drops with traffic
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            self.grid[x][y] = max(0.4, self.grid[x][y] - (traffic * 0.01))

    def get_friction(self, x: int, y: int) -> float:
        # Return friction at coordinates
        return self.grid[int(x)][int(y)] if 0 <= x < len(self.grid) else 1.0

class FluidDynamicsSolver(Component):
    wind_vector: Tuple[float, float] = (0.0, 0.0) # x, y
    air_density: float = 1.225 # kg/m^3

    def calculate_magnus_effect(self, velocity: float, spin: float) -> float:
        # Simplified Magnus force calculation
        # F = S * (w x v)
        return spin * velocity * 0.0004 * self.air_density

